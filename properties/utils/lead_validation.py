import re
import time
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class LeadValidator:
    def __init__(self, request, data):
        self.request = request
        self.data = data
        self.config = getattr(settings, 'LEAD_VALIDATION_CONFIG', {})
        self.score = self.config.get('BASE_SCORE', 100)
        self.validation_summary = []
        self.status = "Pending Validation"
        
        # International inquiry detection flags
        self.has_international_context = False
        self.country_code = data.get('country_code', '') or data.get('contact_country_code', '')
        self.phone = data.get('phone', '')
        
        # Check if inquiry appears to be international
        self._detect_international_context()
        
    def validate(self):
        """Runs the validation rules and computes the final assessment."""
        # Log start of validation for monitoring
        inquiry_id = self.data.get('inquiry_id', 'NEW')
        name = self.data.get('name', 'Unknown')
        email = self.data.get('email', 'Unknown')
        
        logger.info(f"[VALIDATION-START] Inquiry: {inquiry_id}, Name: {name}, Email: {email}, International: {self.has_international_context}")
        
        initial_score = self.score
        
        self._check_honeypot()
        self._check_timing()
        self._check_rate_limit()
        self._check_content_heuristics()
        self._check_business_relevance()
        self._check_contact_info()
        
        self._compute_final_status()
        
        # Calculate score change for monitoring
        score_change = self.score - initial_score
        
        # Log detailed results for monitoring and debugging
        logger.info(
            f"[VALIDATION-END] Inquiry: {inquiry_id}, Final Score: {self.score}, "
            f"Status: {self.status}, Score Change: {score_change}, "
            f"International: {self.has_international_context}, "
            f"Rules Triggered: {len(self.validation_summary)}"
        )
        
        # Log critical decisions (Likely Spam classification)
        if self.status == "Likely Spam":
            logger.warning(
                f"[SPAM-CLASSIFICATION] Inquiry: {inquiry_id} classified as Likely Spam. "
                f"Score: {self.score}, Name: {name}, Email: {email}, "
                f"International: {self.has_international_context}"
            )
        
        return {
            'confidence_score': max(0, min(100, self.score)),  # Clamp between 0 and 100
            'assessment_status': self.status,
            'validation_summary': self.validation_summary
        }

    def _detect_international_context(self):
        """Detect if inquiry appears to be from an international client."""
        # Non-India country codes indicate international inquiry
        non_india_codes = ['+1', '+44', '+65', '+61', '+971', '+48', '+49', '+33', '+39', '+81', '+82', '+86', '+7']
        
        previous_international_status = self.has_international_context
        
        if self.country_code:
            if any(self.country_code.startswith(code) for code in non_india_codes):
                self.has_international_context = True
                self.validation_summary.append({'text': f'International Inquiry ({self.country_code})', 'type': 'info'})
                logger.info(f"[INTERNATIONAL-DETECTED] Country Code: {self.country_code}")
            elif self.country_code.startswith('+91'):
                logger.info(f"[INDIA-DETECTED] Country Code: {self.country_code}")
        
        # Also check phone number for non-India prefixes
        if self.phone:
            international_prefixes = ['+1', '+44', '+65', '+61', '+971', '+48', '+49', '+33', '+39', '+81', '+82', '+86', '+7']
            if any(self.phone.startswith(prefix) for prefix in international_prefixes):
                self.has_international_context = True
                logger.info(f"[INTERNATIONAL-DETECTED] Phone Prefix: {self.phone[:5]}...")
            elif self.phone.startswith('+91'):
                logger.info(f"[INDIA-DETECTED] Phone Prefix: {self.phone[:5]}...")
        
        # Log context change for monitoring
        if self.has_international_context != previous_international_status:
            logger.info(f"[CONTEXT-CHANGE] International status changed to: {self.has_international_context}")
                
    def _check_honeypot(self):
        honeypot_field = self.config.get('HONEYPOT_FIELD_NAME', 'website_url_check')
        honeypot_value = self.data.get(honeypot_field, '')
        if honeypot_value:
            penalty = self.config.get('PENALTY_HONEYPOT', 80)
            self.score -= penalty
            self.validation_summary.append({'text': 'Hidden field populated (Bot Behavior)', 'type': 'danger'})
            
    def _check_timing(self):
        min_time = self.config.get('MIN_SUBMISSION_TIME_SECONDS', 2)
        try:
            render_time = float(self.data.get('form_render_time', 0))
            if render_time > 0:
                elapsed = time.time() - render_time
                if elapsed < min_time:
                    penalty = self.config.get('PENALTY_FAST_SUBMISSION', 40)
                    self.score -= penalty
                    self.validation_summary.append({'text': f'Suspiciously fast submission ({elapsed:.1f}s)', 'type': 'danger'})
        except ValueError:
            pass

    def _check_rate_limit(self):
        ip = self._get_client_ip()
        session_key = self.request.session.session_key or 'no-session'
        cache_key = f"rate_limit_{ip}_{session_key}"
        
        count = cache.get(cache_key, 0)
        max_requests = self.config.get('RATE_LIMIT_MAX_REQUESTS', 5)
        
        if count >= max_requests:
            penalty = self.config.get('PENALTY_RATE_LIMIT', 30)
            self.score -= penalty
            self.validation_summary.append({'text': 'Rate limit exceeded', 'type': 'danger'})
        
        cache.set(cache_key, count + 1, timeout=self.config.get('RATE_LIMIT_WINDOW_SECONDS', 600))

    def _check_content_heuristics(self):
        message = self.data.get('message', '').lower()
        if not message:
            self.validation_summary.append({'text': 'Message Body Empty', 'type': 'warning'})
            return
            
        # URL check
        url_count = message.count('http://') + message.count('https://') + message.count('www.')
        max_urls = self.config.get('MAX_HYPERLINKS', 1)
        if url_count > max_urls:
            self.score -= self.config.get('PENALTY_MULTIPLE_URLS', 40)
            self.validation_summary.append({'text': f'External URL Detected ({url_count})', 'type': 'danger'})
        elif url_count == 0:
            self.validation_summary.append({'text': 'No Suspicious URLs', 'type': 'success'})

        # Cyrillic / Foreign Non-Target Script Spam Check
        # Reduced penalty for Cyrillic - legitimate international inquiries may contain Cyrillic
        # Only penalize if excessive Cyrillic content
        cyrillic_chars = len(re.findall(r'[\u0400-\u04FF]', message))
        total_chars = len(message)
        if cyrillic_chars > 0:
            cyrillic_ratio = cyrillic_chars / max(total_chars, 1)
            # Only penalize if more than 50% of content is Cyrillic
            if cyrillic_ratio > 0.5:
                penalty = min(40, int(80 * cyrillic_ratio))  # Max 40 instead of 80
                self.score -= penalty
                self.validation_summary.append({'text': f'Excessive Cyrillic Script Detected ({cyrillic_ratio:.0%})', 'type': 'danger'})
                # Log Cyrillic penalty for monitoring
                logger.info(
                    f"[CYRILLIC-PENALTY] Ratio: {cyrillic_ratio:.2%}, Penalty: {penalty}, "
                    f"International: {self.has_international_context}"
                )
            else:
                self.validation_summary.append({'text': 'Minimal Cyrillic Content', 'type': 'info'})
                # Log minimal Cyrillic for monitoring
                logger.info(
                    f"[CYRILLIC-MINIMAL] Ratio: {cyrillic_ratio:.2%}, No penalty, "
                    f"International: {self.has_international_context}"
                )

        # High-risk Spam TLDs Check
        # Removed .xyz, .top, .work from high-risk list - these are legitimate TLDs
        # Added pattern to check for URLs with suspicious context
        high_risk_tlds = r'\.(ru|su|рф)\b'
        # Check for TLDs in suspicious context (e.g., promotion/ads)
        tld_pattern = re.compile(rf'(?:http|https|www)[^\s]*{high_risk_tlds}[^\s]*', re.IGNORECASE)
        tld_matches = list(tld_pattern.finditer(message))
        if tld_matches:
            # Penalize per suspicious URL found
            penalty_per_url = 20  # Reduced from 60
            total_penalty = min(40, penalty_per_url * len(tld_matches))
            self.score -= total_penalty
            self.validation_summary.append({'text': f'High-Risk TLD URLs Found ({len(tld_matches)})', 'type': 'danger'})
            # Log TLD penalty for monitoring
            logger.info(
                f"[TLD-PENALTY] URLs: {len(tld_matches)}, Penalty: {total_penalty}, "
                f"International: {self.has_international_context}"
            )
        else:
            # Also check for standalone TLD mentions without URLs
            standalone_tlds = re.findall(rf'\b[a-z0-9]+\.(ru|su|рф)\b', message, re.IGNORECASE)
            if standalone_tlds:
                self.score -= 15  # Small penalty for TLD mentions
                self.validation_summary.append({'text': 'High-Risk TLD Mentioned', 'type': 'warning'})
                # Log standalone TLD for monitoring
                logger.info(
                    f"[TLD-MENTION] Domains: {len(standalone_tlds)}, Penalty: 15, "
                    f"International: {self.has_international_context}"
                )
            
        # Context-aware spam keyword detection
        spam_keywords = self.config.get('SPAM_KEYWORDS', [])
        found_spam = []
        
        for keyword in spam_keywords:
            # Check if keyword appears in suspicious context
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, message):
                found_spam.append(keyword)
        
        if found_spam:
            penalty = self.config.get('PENALTY_SPAM_KEYWORD', 30)
            # Reduce penalty for international inquiries (they might use different phrasing)
            if self.has_international_context:
                penalty = penalty // 2  # Halve penalty for international
                self.validation_summary.append({'text': f'Spam Keywords Found (International context)', 'type': 'warning'})
            else:
                self.validation_summary.append({'text': f'Spam Keywords Found ({len(found_spam)})', 'type': 'danger'})
            self.score -= penalty
        else:
            self.validation_summary.append({'text': 'No Spam Keywords', 'type': 'success'})
            
        # Promo Keywords - less strict for international inquiries
        promo_keywords = self.config.get('PROMO_KEYWORDS', [])
        found_promo = [kw for kw in promo_keywords if kw in message]
        if found_promo:
            penalty = self.config.get('PENALTY_PROMO_KEYWORD', 15)
            # Reduce penalty for international inquiries
            if self.has_international_context:
                penalty = penalty // 2  # Halve penalty
                self.validation_summary.append({'text': 'Marketing Language (International context)', 'type': 'info'})
            else:
                self.validation_summary.append({'text': 'Promotional Language', 'type': 'warning'})
            self.score -= penalty

    def _check_business_relevance(self):
        message = self.data.get('message', '').lower()
        if not message:
            return
            
        business_keywords = self.config.get('BUSINESS_KEYWORDS', [])
        found = [kw for kw in business_keywords if kw in message]
        
        # International inquiries might use different terminology
        if found:
            bonus = self.config.get('BONUS_BUSINESS_RELEVANCE', 10)
            # Give extra bonus for international with relevant intent
            if self.has_international_context:
                bonus += 5  # Extra bonus for international with clear intent
                self.validation_summary.append({'text': f'Relevant Property Intent (International +{bonus})', 'type': 'success'})
            else:
                self.validation_summary.append({'text': f'Relevant Property Intent (+{bonus})', 'type': 'success'})
            self.score += bonus
        else:
            # Less strict for international inquiries
            if self.has_international_context:
                self.validation_summary.append({'text': 'General Intent (International)', 'type': 'info'})
                # Small bonus for international even without specific keywords
                self.score += 5
            else:
                self.validation_summary.append({'text': 'Vague Intent', 'type': 'warning'})

    def _check_contact_info(self):
        name = self.data.get('name', '')
        if name:
            # Be more lenient with international name formats
            if self.has_international_context:
                self.validation_summary.append({'text': 'Name Provided (International)', 'type': 'info'})
            else:
                self.validation_summary.append({'text': 'Human Name Format', 'type': 'success'})
            
        phone = self.data.get('phone', '')
        if phone:
            digits = re.sub(r'\D', '', phone)
            if len(digits) < 7:
                # Be more lenient for international inquiries
                if self.has_international_context:
                    self.validation_summary.append({'text': 'Phone Format Review (International)', 'type': 'warning'})
                else:
                    self.score -= self.config.get('PENALTY_INVALID_PHONE', 15)
                    self.validation_summary.append({'text': 'Invalid Phone Format', 'type': 'danger'})
            else:
                self.validation_summary.append({'text': 'Valid Phone Format', 'type': 'success'})
        else:
            # Less strict warning for international inquiries
            if self.has_international_context:
                self.validation_summary.append({'text': 'Phone Optional (International)', 'type': 'info'})
            else:
                self.validation_summary.append({'text': 'Phone Not Provided', 'type': 'warning'})

        email = self.data.get('email', '')
        if email:
            if '@' not in email or '.' not in email.split('@')[-1]:
                # Be more lenient for international inquiries
                if self.has_international_context:
                    self.validation_summary.append({'text': 'Email Format Review (International)', 'type': 'warning'})
                else:
                    self.score -= self.config.get('PENALTY_INVALID_EMAIL', 15)
                    self.validation_summary.append({'text': 'Invalid Email Format', 'type': 'danger'})
            else:
                # Bonus for valid email from international clients
                if self.has_international_context:
                    self.score += 5  # Small bonus for international with valid email
                    self.validation_summary.append({'text': 'Valid Email (International)', 'type': 'success'})
                else:
                    self.validation_summary.append({'text': 'Valid Email Format', 'type': 'success'})
        elif self.data.get('form_source') != 'Quick Inquiry':
            # Less strict for international inquiries
            if self.has_international_context:
                self.validation_summary.append({'text': 'Email Optional (International)', 'type': 'info'})
            else:
                self.validation_summary.append({'text': 'Email Not Provided', 'type': 'warning'})

    def _compute_final_status(self):
        ranges = self.config.get('RANGES', {})
        score = max(0, min(100, self.score))
        
        if score >= ranges.get('LIKELY_GENUINE', 90):
            self.status = "Likely Genuine"
        elif score >= ranges.get('GENUINE', 70):
            self.status = "Genuine"
        elif score >= ranges.get('REVIEW_RECOMMENDED', 40):
            self.status = "Review Recommended"
        else:
            self.status = "Likely Spam"
            
    def _get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return self.request.META.get('REMOTE_ADDR')
