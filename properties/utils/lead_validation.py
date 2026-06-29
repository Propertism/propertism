import re
import time
from django.conf import settings
from django.core.cache import cache

class LeadValidator:
    def __init__(self, request, data):
        self.request = request
        self.data = data
        self.config = getattr(settings, 'LEAD_VALIDATION_CONFIG', {})
        self.score = self.config.get('BASE_SCORE', 100)
        self.validation_summary = []
        self.status = "Pending Validation"
        
    def validate(self):
        """Runs the validation rules and computes the final assessment."""
        self._check_honeypot()
        self._check_timing()
        self._check_rate_limit()
        self._check_content_heuristics()
        self._check_business_relevance()
        self._check_contact_info()
        
        self._compute_final_status()
        
        return {
            'confidence_score': max(0, min(100, self.score)),  # Clamp between 0 and 100
            'assessment_status': self.status,
            'validation_summary': self.validation_summary
        }

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
            
        # Spam Keywords
        spam_keywords = self.config.get('SPAM_KEYWORDS', [])
        found_spam = [kw for kw in spam_keywords if kw in message]
        if found_spam:
            self.score -= self.config.get('PENALTY_SPAM_KEYWORD', 30)
            self.validation_summary.append({'text': 'Spam Keywords Found', 'type': 'danger'})
        else:
            self.validation_summary.append({'text': 'No Spam Keywords', 'type': 'success'})
            
        # Promo Keywords
        promo_keywords = self.config.get('PROMO_KEYWORDS', [])
        found_promo = [kw for kw in promo_keywords if kw in message]
        if found_promo:
            self.score -= self.config.get('PENALTY_PROMO_KEYWORD', 15)
            self.validation_summary.append({'text': 'Promotional Language', 'type': 'warning'})

    def _check_business_relevance(self):
        message = self.data.get('message', '').lower()
        if not message:
            return
            
        business_keywords = self.config.get('BUSINESS_KEYWORDS', [])
        found = [kw for kw in business_keywords if kw in message]
        if found:
            self.score += self.config.get('BONUS_BUSINESS_RELEVANCE', 10)
            self.validation_summary.append({'text': 'Relevant Property Intent', 'type': 'success'})
        else:
            self.validation_summary.append({'text': 'Vague Intent', 'type': 'warning'})

    def _check_contact_info(self):
        name = self.data.get('name', '')
        if name:
            self.validation_summary.append({'text': 'Human Name Format', 'type': 'success'})
            
        phone = self.data.get('phone', '')
        if phone:
            digits = re.sub(r'\D', '', phone)
            if len(digits) < 7:
                self.score -= self.config.get('PENALTY_INVALID_PHONE', 15)
                self.validation_summary.append({'text': 'Invalid Phone Format', 'type': 'danger'})
            else:
                self.validation_summary.append({'text': 'Valid Phone Format', 'type': 'success'})
        else:
            self.validation_summary.append({'text': 'Phone Not Provided', 'type': 'warning'})

        email = self.data.get('email', '')
        if email:
            if '@' not in email or '.' not in email.split('@')[-1]:
                self.score -= self.config.get('PENALTY_INVALID_EMAIL', 15)
                self.validation_summary.append({'text': 'Invalid Email Format', 'type': 'danger'})
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
