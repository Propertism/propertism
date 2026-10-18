<!-- AUDIT METADATA -->
<!-- Date: 2026-10-13 -->
<!-- Time: 13:10 IST -->
<!-- Product Owner: Viji -->
<!-- Module: 03-propertism -->
<!-- Status: ACTIVE -->
<!-- Classification: TECHNICAL REFERENCE -->

# Web Crucials — Performance, Security, and Spam Protection Reference

> **Core Engineering Principle:** *"Performance optimization without functional integrity is delivering broken pages faster. Optimize for demonstrable user speed, 100% green Core Web Vitals, comprehensive security controls, and zero operational regressions across business-critical conversion funnels."*

---

## 1. Overview

This technical reference document establishes the operational audit framework, empirical benchmarks, and zero-regression methodology for web performance optimization, security hardening, spam protection, and attack prevention.

Leveraging architectural lessons and production telemetry from **`Propertism.in`**, this document systematically addresses Core Web Vitals, asset optimization, browser rendering, third-party script management, security controls, CAPTCHA implementation, rate limiting, and multi-layer spam protection.

**Document Purpose:**
- Performance audit checklists and scoring frameworks
- Core Web Vitals optimization strategies
- Security and spam protection implementation patterns
- Zero-regression testing protocols
- Real-world case study benchmarks

---

## 2. Performance Audit Checklists & Scoring Framework

To eliminate guesswork, performance optimization is decomposed into three deterministic pillars. Each area is evaluated against Google's official Core Web Vitals thresholds and industry-standard performance budgets.

### Pillar A: Core Web Vitals & Real User Experience (Field & Lab Metrics)

| Section | Area / Metric | Audit Focus & Technical Scope | Target Benchmark / Score |
|---|---|---|---|
| **CWV** | **LCP** (Largest Contentful Paint) | Measures render time of the primary hero image or primary text block in the viewport. | **≤ 2.0s** (Google "Good" threshold is 2.5s) |
| **CWV** | **INP** (Interaction to Next Paint) | Measures responsiveness to user taps, clicks, and keyboard inputs across the session lifecycle. | **≤ 150ms** (Google "Good" threshold is 200ms) |
| **CWV** | **CLS** (Cumulative Layout Shift) | Quantifies unexpected layout shifts caused by unsized media, dynamic banners, or late web fonts. | **≤ 0.05** (Target: 0.00; Max allowable: 0.10) |
| **Server** | **TTFB** (Time to First Byte) | Server processing time, database lookup efficiency, and TLS handshake round-trips. | **≤ 200ms** (Under 400ms on dynamic cold hits) |
| **Score** | **Lighthouse Mobile Score** | Synthetic score under simulated Moto G4 device with throttled 4G network profile. | **≥ 85+ / 100** (Target: 90+ Green Tier) |
| **Score** | **Lighthouse Desktop Score** | Synthetic score evaluated under standard unthrottled desktop browser environment. | **≥ 95+ / 100** |

### Pillar B: Asset Diet, Payload & Network Delivery Pipeline

| Section | Area / Asset Type | Audit Focus & Technical Scope | Target Benchmark / Score |
|---|---|---|---|
| **Media** | **Image Formats & Compression** | Elimination of uncompressed JPEG/PNG assets; migration to next-gen WebP / AVIF formats. | **80%–90% payload reduction** (Hero ≤ 120 KB; cards ≤ 30 KB) |
| **Media** | **Responsive Dimensions & Lazy Loading** | Implementation of native `loading="lazy"`, `decoding="async"`, and explicit `width`/`height` attributes. | **100% media sized**; zero lazy-loading on above-fold hero |
| **Cache** | **HTTP Caching & Fingerprinting** | Fingerprinted asset bundling with `Cache-Control: public, max-age=31536000, immutable`. | **100% static assets cached for 1 Year** |
| **Network** | **Transport Protocol & Compression** | Multiplexed HTTP/2 or HTTP/3 configuration; active Brotli and Gzip server compression. | **Brotli / Gzip enabled** for all text-based MIME types |
| **Fonts** | **Web Font Optimization** | Elimination of render-blocking Google Fonts; adoption of self-hosted WOFF2 with `font-display: swap`. | **≤ 2 font families / ≤ 4 weights total** (≤ 80 KB total font budget) |

### Pillar C: JavaScript Runtime, DOM & 3rd-Party Tag Hygiene

| Section | Area / Execution | Audit Focus & Technical Scope | Target Benchmark / Score |
|---|---|---|---|
| **JS** | **Render-Blocking Scripts** | Audit of `<head>` scripts; deferral of non-critical JavaScript via `defer` or dynamic module loading. | **0 render-blocking scripts** in critical rendering path |
| **JS** | **TBT** (Total Blocking Time) | Main-thread locking caused by heavy execution loops during page initialization. | **≤ 150ms** (Google "Good" threshold is 200ms) |
| **3rd-Party** | **Analytics, Pixels & Tag Managers** | Isolation of Google Analytics 4, Meta Pixel, Hotjar, and chatbot widgets to `requestIdleCallback`. | **≤ 1.0s total 3rd-party execution time** |
| **DOM** | **DOM Tree Depth & Complexity** | Pruning redundant container `<div>` tags and deeply nested component wrappers. | **Total DOM Nodes ≤ 800** (Max DOM Depth ≤ 32) |
| **Payload** | **Initial Viewport Transfer Budget** | Total transferred data required to render the interactive above-fold viewport. | **Initial Viewport Payload ≤ 800 KB – 1.2 MB** |

---

## 3. Case Study: Propertism.in Performance Optimization

### Background & Architectural Challenge

The platform **`Propertism.in`** is an enterprise real estate discovery and lead generation portal built on Python/Django and PostgreSQL, serving high-net-worth international NRI property investors. Initial field metrics suffered from high bounce rates on mobile networks due to:

1. Massive uncompressed hero photography and team assets (averaging 2.5 MB to 4.0 MB per page).
2. Render-blocking stylesheets and synchronous third-party scripts.
3. High server response times (TTFB > 650ms) caused by cross-region infrastructure routing.
4. Heavy cumulative layout shifts caused by dynamically injected conversational AI widgets and unsized property cards.

### Engineering Interventions Executed

- **Zero-Loss Asset Diet**: Converted all photography to WebP format with automated compression rules, reducing asset sizes by **85%** while maintaining visual fidelity. Implemented explicit aspect ratios to eliminate layout shifts.

- **Protocol & Caching Modernization**: Enabled HTTP/2 protocol multiplexing, tuned TLS session caching, and configured WhiteNoise with `CompressedManifestStaticFilesStorage` to deliver hashed static bundles with 1-year immutable caching (`max-age=31536000`).

- **Critical Rendering Path De-Cluttering**: Decoupled third-party analytics (GA4) and conversational AI engines from initial page boot—moving execution to `requestIdleCallback` after `DOMContentLoaded`.

- **Infrastructure Compute Placement**: Localized compute and database storage to AWS Lightsail Mumbai (`ap-south-1`), cutting cross-region network hops.

### Empirical Before vs. After Results

| Performance Metric | Baseline (Before) | Optimized (After) | Improvement Delta |
|---|:---:|:---:|:---:|
| **Time to First Byte (TTFB)** | ~650 ms | **< 180 ms** | **72% faster server response** |
| **Largest Contentful Paint (LCP)** | 4.8 s (Poor) | **1.6 s (Good)** | **66% faster primary render** |
| **Cumulative Layout Shift (CLS)** | 0.28 (Poor) | **0.02 (Good)** | **92% reduction in layout jumping** |
| **Total Blocking Time (TBT)** | 480 ms | **110 ms** | **77% reduction in CPU freeze** |
| **Total Page Payload** | ~3.8 MB | **~820 KB** | **78% reduction in data transfer** |
| **Lighthouse Mobile Score** | 41 / 100 | **93+ / 100** | **+52 points (Green Tier)** |
| **Lighthouse Desktop Score** | 68 / 100 | **98 / 100** | **+30 points (Green Tier)** |
| **Business Conversion Impact** | High mobile bounce | **Mobile bounce rate dropped by 45%**; lead intake doubled | **2x Conversion Rate** |

---

## 4. Functional Integrity & Zero-Regression Protocol

### Engineering Philosophy

Speed without functional reliability is worthless. If an optimization breaks form validation, disrupts payment workflows, or silences analytics beacons, the speed increase causes immediate revenue loss. 

**4-Step Zero-Regression Engineering Protocol:**

#### Step 1: Pre-Optimization Behavioral Baselines

Before touching a single asset or config line, establish an automated and manual functional test matrix covering all core user journeys:

- Contact and lead intake form submissions (valid and invalid field validation).
- Interactive navigation elements (mobile hamburger menus, drawer toggles, filter dropdowns).
- Dynamic modals, accordion FAQs, and image lightboxes.
- Analytics and conversion event dispatchers (`contact_form_submit`, `whatsapp_click`, `phone_call_click`).

#### Step 2: Dependency-Aware Script Loading (Anti-Breakage Rules)

The primary cause of broken websites during performance sprints is blindly applying `defer` or `async` to scripts that have DOM execution order dependencies.

**Best Practices:**
- Map the JavaScript dependency graph explicitly.
- Framework scripts (e.g., jQuery, Alpine, React) and DOM-dependent libraries are never arbitrarily decoupled from dependent inline blocks.
- Non-critical tracking pixels and conversational widgets are sandboxed in isolated execution contexts using `requestIdleCallback` or dynamic script injection post-render.

#### Step 3: Staging-First Isolation with Low-End Throttling

Zero direct production experimentation. All changes are staged in an isolated test environment mirroring production web server headers (Nginx/CloudFront).

**Testing Protocol:**
- Tests are executed under synthetic 4G mobile throttling and CPU slowdown via Chrome DevTools.
- Cross-browser compatibility is verified across Safari (iOS), Chrome (Android), and Chromium/Firefox desktop engines.

#### Step 4: Dual Verification Gates (Performance + Functional Smoke Tests)

Every code deployment must pass a mandatory two-stage sign-off gate:

- **Gate A (Performance Pass)**: Lighthouse score ≥ 85+ mobile and Core Web Vitals strictly in the Green tier.
- **Gate B (Functional Pass)**: 100% passing automated test suite, zero uncaught JavaScript errors in browser DevTools console, and verified 200 OK responses on all API endpoints.

---

## 5. Security & Spam Protection Framework

### Multi-Layer Defense Architecture

Security and spam protection require defense-in-depth across multiple layers. No single control should be treated as sufficient.

**Layer 1: Client-Side Validation**
- Form field validation (required fields, format checks, length limits)
- JavaScript-based honeypot fields
- Client-side rate limiting indicators

**Layer 2: CAPTCHA Verification**
- Google reCAPTCHA v2 or v3
- hCaptcha or alternative providers
- Server-side token verification (never trust client-only validation)
- Fail-safe behavior (fail closed, not open)
- Proper secret management

**Layer 3: Server-Side Spam Protection**
- Honeypot field validation
- Submission timing checks
- Request origin validation
- Content-based spam detection
- Pattern matching for known spam indicators

**Layer 4: Rate Limiting & Abuse Prevention**
- Per-IP rate limiting
- Per-session rate limiting
- Distributed rate limiting (Redis/Memcached)
- Adaptive rate limiting based on abuse patterns
- Proper IP resolution behind proxies/CDNs

**Layer 5: Authentication & Authorization**
- API endpoint authentication requirements
- Role-based access control (RBAC)
- Token-based authentication for sensitive endpoints
- Service-to-service authentication

**Layer 6: Monitoring & Alerting**
- Real-time spam pattern detection
- Anomaly detection (submission spikes)
- Failed validation logging
- CAPTCHA failure rate monitoring
- Rate limit hit monitoring

---

## 6. CAPTCHA Implementation Best Practices

### Server-Side Verification Requirements

**Critical Rules:**
1. **Never trust client-only validation** — Always verify CAPTCHA tokens server-side
2. **Fail closed, not open** — If verification fails or errors occur, reject the submission
3. **Validate the secret is present** — Missing secrets should cause hard failures, not silent bypasses
4. **Handle network errors securely** — Provider timeouts should reject submissions unless explicitly configured otherwise
5. **Log verification failures** — Track failed verifications for abuse pattern detection

### Configuration Checklist

```python
# Example secure configuration pattern
CAPTCHA_SETTINGS = {
    'PROVIDER': 'google_recaptcha_v2',
    'SITE_KEY': os.environ.get('RECAPTCHA_SITE_KEY'),
    'SECRET_KEY': os.environ.get('RECAPTCHA_SECRET_KEY'),
    'FAIL_OPEN': False,  # CRITICAL: Fail closed for security
    'TIMEOUT': 5.0,  # Provider request timeout
    'MIN_SCORE': 0.5,  # For reCAPTCHA v3
    'VERIFY_HOSTNAME': True,  # Validate request hostname
}

# Startup validation
if not CAPTCHA_SETTINGS['SECRET_KEY']:
    raise ImproperlyConfigured("RECAPTCHA_SECRET_KEY must be set")
```

### Common Vulnerabilities to Avoid

| Vulnerability | Description | Fix |
|---|---|---|
| **Fail-Open Default** | `RECAPTCHA_FAIL_OPEN=True` allows bypasses on errors | Set to `False` in production |
| **Missing Secret Handling** | Missing secret returns success | Hard fail on startup if secret missing |
| **Client-Only Validation** | Only checking token exists, not verifying it | Always verify with provider |
| **Network Error Bypasses** | Timeouts or errors allow submission | Reject on errors unless explicit policy |
| **No Hostname Validation** | Token from wrong domain accepted | Verify hostname matches expected domain |
| **Token Reuse** | Same token accepted multiple times | Validate token freshness and one-time use |

---

## 7. Rate Limiting Implementation Patterns

### Per-IP Rate Limiting

```python
# Example Django implementation with cache backend
from django.core.cache import cache
from django.http import HttpResponseForbidden

def rate_limit_check(request, key_prefix, max_attempts, time_window):
    """
    Check if request exceeds rate limit.
    
    Args:
        request: Django request object
        key_prefix: Cache key prefix (e.g., 'contact_form')
        max_attempts: Maximum attempts allowed
        time_window: Time window in seconds
    
    Returns:
        tuple: (is_allowed, remaining_attempts)
    """
    client_ip = get_client_ip(request)
    cache_key = f"rate_limit:{key_prefix}:{client_ip}"
    
    attempts = cache.get(cache_key, 0)
    
    if attempts >= max_attempts:
        return False, 0
    
    # Increment with atomic operation
    cache.set(cache_key, attempts + 1, time_window)
    
    return True, max_attempts - attempts - 1

def get_client_ip(request):
    """Extract client IP, handling proxies/CDNs."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Take first IP (original client)
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
```

### Distributed Rate Limiting Considerations

**For Multi-Instance Deployments:**
- Use Redis or Memcached for shared cache backend
- Ensure atomic increment operations
- Consider race conditions in distributed systems
- Implement cache connection failure handling

**Rate Limit Configuration Examples:**

| Endpoint Type | Rate Limit | Time Window | Reasoning |
|---|---|---|---|
| Contact Forms | 5 submissions | 10 minutes | Prevent spam while allowing legitimate retries |
| API Read Endpoints | 100 requests | 1 minute | Balance performance and abuse prevention |
| Authentication Attempts | 5 attempts | 15 minutes | Prevent brute force attacks |
| Password Reset | 3 requests | 1 hour | Prevent email bombing |

---

## 8. API Security Hardening

### Authentication & Authorization Checklist

**Public API Endpoint Review:**

```python
# INSECURE — Avoid this pattern
@api_view(['GET'])
@permission_classes([AllowAny])  # ❌ Exposes all data
def list_sensitive_data(request):
    queryset = SensitiveModel.objects.all()
    serializer = SensitiveSerializer(queryset, many=True)
    return Response(serializer.data)

# SECURE — Use proper authentication
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # ✅ Requires authentication
def list_sensitive_data(request):
    # Further restrict by user permissions
    queryset = SensitiveModel.objects.filter(user=request.user)
    serializer = MinimalSerializer(queryset, many=True)  # ✅ Minimal fields
    return Response(serializer.data)
```

**API Security Audit Questions:**

1. **Authentication**: Does the endpoint require authentication?
2. **Authorization**: Are users restricted to their own data?
3. **Field Exposure**: Does the serializer expose only necessary fields?
4. **Pagination**: Are large result sets properly paginated?
5. **Rate Limiting**: Is the endpoint rate limited?
6. **Input Validation**: Are all inputs validated and sanitized?
7. **Error Handling**: Do errors expose sensitive information?
8. **Logging**: Are access attempts logged for audit?

### Serializer Field Minimization

```python
# INSECURE — Exposes internal fields
class InsecureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'  # ❌ Exposes all fields including internal ones

# SECURE — Explicit field list
class SecureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = [  # ✅ Only expose necessary fields
            'id',
            'created_at',
            'service_type',
            # Exclude: email, phone, message, internal_notes, spam_score
        ]
```

---

## 9. Attack Prevention Strategies

### Common Attack Vectors & Mitigations

| Attack Type | Description | Mitigation Strategy |
|---|---|---|
| **Spam Flooding** | Mass submission of junk enquiries | Multi-layer validation + CAPTCHA + rate limiting |
| **Credential Stuffing** | Automated login attempts with stolen credentials | Rate limiting + CAPTCHA + account lockout |
| **API Data Scraping** | Unauthorized data harvesting | Authentication + rate limiting + pagination |
| **DDoS** | Overwhelming server with requests | Rate limiting + CDN + WAF |
| **SQL Injection** | Malicious database queries | Parameterized queries + ORM + input validation |
| **XSS** | Injecting malicious scripts | Output escaping + CSP headers + input sanitization |
| **CSRF** | Unauthorized state-changing requests | CSRF tokens + SameSite cookies |
| **Email Bombing** | Mass form submissions to spam victim emails | Rate limiting + email verification + CAPTCHA |

### Defense-in-Depth Implementation

**Layer 1: Infrastructure**
- CDN with DDoS protection (CloudFlare, AWS CloudFront)
- Web Application Firewall (WAF)
- Geographic restrictions where appropriate

**Layer 2: Network**
- Rate limiting at load balancer/reverse proxy
- IP allowlisting/denylisting
- Connection limiting

**Layer 3: Application**
- Django security middleware
- CAPTCHA verification
- Spam detection services
- Rate limiting per user/IP/session

**Layer 4: Data**
- Input validation and sanitization
- Output encoding
- Parameterized database queries
- Principle of least privilege

**Layer 5: Monitoring**
- Real-time alerting on anomalies
- Log aggregation and analysis
- Security event monitoring
- Performance monitoring

---

## 10. Testing & Validation Protocol

### Security Testing Checklist

**Pre-Deployment Security Tests:**

- [ ] **Authentication Bypass Tests**
  - Attempt to access protected endpoints without authentication
  - Test with expired tokens
  - Test with invalid tokens

- [ ] **Authorization Tests**
  - Attempt to access other users' data
  - Test role-based access control boundaries
  - Verify least-privilege enforcement

- [ ] **CAPTCHA Bypass Tests**
  - Submit without CAPTCHA token
  - Submit with invalid token
  - Submit with expired token
  - Verify server-side verification occurs

- [ ] **Rate Limiting Tests**
  - Exceed rate limits and verify rejection
  - Test distributed rate limiting across instances
  - Verify cache backend behavior

- [ ] **Spam Protection Tests**
  - Submit with honeypot field filled
  - Submit with suspicious content patterns
  - Submit too quickly after page load
  - Verify all validation layers execute

- [ ] **Input Validation Tests**
  - Test boundary conditions
  - Test injection attempts (SQL, XSS, etc.)
  - Test malformed data
  - Verify sanitization

### Performance Testing Checklist

**Pre-Deployment Performance Tests:**

- [ ] **Lighthouse Audit**
  - Mobile score ≥ 85
  - Desktop score ≥ 95
  - All Core Web Vitals in Green tier

- [ ] **Load Testing**
  - Sustained traffic at 2x normal load
  - Spike testing for traffic bursts
  - Verify graceful degradation

- [ ] **Functional Regression Tests**
  - All form submissions work
  - All interactive elements function
  - Analytics tracking fires correctly
  - No JavaScript console errors

---

## 11. Monitoring & Alerting

### Key Metrics to Monitor

**Performance Metrics:**
- Page load time (P50, P95, P99)
- Time to First Byte (TTFB)
- Largest Contentful Paint (LCP)
- Cumulative Layout Shift (CLS)
- Interaction to Next Paint (INP)
- JavaScript error rate

**Security Metrics:**
- Failed authentication attempts
- CAPTCHA failure rate
- Rate limit hits
- Spam detection triggers
- Unauthorized API access attempts
- Suspicious traffic patterns

**Business Metrics:**
- Form submission rate
- Conversion rate
- Bounce rate
- Mobile vs. desktop performance gap

### Alert Thresholds

| Metric | Warning Threshold | Critical Threshold | Action |
|---|---|---|---|
| Spam submissions | 50/hour | 100/hour | Review and potentially tighten controls |
| CAPTCHA failures | 20% | 40% | Investigate potential bot attack |
| Rate limit hits | 100/hour | 500/hour | Review rate limit policies |
| Failed auth attempts | 50/hour | 200/hour | Potential credential stuffing attack |
| Page load time | > 3s | > 5s | Performance investigation |
| Error rate | > 1% | > 5% | Immediate investigation |

---

## 12. Continuous Improvement

### Regular Audit Schedule

**Weekly:**
- Review spam logs and patterns
- Check rate limiting effectiveness
- Monitor performance metrics

**Monthly:**
- Full Lighthouse audit
- Security vulnerability scan
- Review and update rate limits
- Analyze attack patterns

**Quarterly:**
- Complete security penetration test
- Performance optimization review
- CAPTCHA effectiveness analysis
- Update threat model

### Best Practices Maintenance

1. **Stay Updated**: Keep dependencies and security libraries current
2. **Monitor CVEs**: Subscribe to security advisories for all components
3. **Test Regularly**: Automated security and performance testing in CI/CD
4. **Document Changes**: Maintain clear audit trail of all security changes
5. **Train Team**: Regular security awareness and best practices training

---

**Document Status:** ✅ ACTIVE — Technical Reference  
**Last Updated:** 2026-10-13 13:10 IST  
**Next Review:** 2027-01-13  
**Owner:** Viji M / Olivine Platform Engineering
