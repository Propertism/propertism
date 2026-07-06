# SCCB-PROP-SEC-001 — Enterprise Spam Protection Framework with Google reCAPTCHA v2

---

## Change Classification

**Security Enhancement**

## Objective

Replace the existing arithmetic CAPTCHA with a reusable, enterprise-grade spam protection framework using Google reCAPTCHA v2 ("I'm not a robot") while preserving all existing spam prevention mechanisms. The implementation shall be provider-agnostic, centrally managed, configurable, and reusable across all current and future public forms.

---

## Scope

This SCCB applies to all public-facing forms including, but not limited to:

* General Contact Form
* Quick Inquiry / Callback Form
* Property Detail Enquiry Form
* Any future forms that include the shared validation component

---

## Existing Controls (Retain)

The following security mechanisms shall remain operational:

* Honeypot hidden field validation
* Submission timing validation
* Existing IP rate limiting
* Existing spam confidence scoring
* Server-side validation
* Existing feature flag framework

These controls shall operate together with reCAPTCHA and shall not be removed.

---

## Architecture Requirements

Implement a centralized spam protection architecture rather than individual per-view validation.

Recommended structure:

```
content/security/
    spam_protection.py
    captcha_provider.py
    google_recaptcha.py
    validators.py
```

All form submissions shall pass through a single `SpamProtectionService` responsible for:

1. Honeypot validation
2. Submission timing validation
3. Rate limiting
4. reCAPTCHA verification
5. Spam logging
6. Unified validation response

Views must not directly implement reCAPTCHA verification.

---

## Google reCAPTCHA

**Provider:** Google reCAPTCHA v2 Checkbox ("I'm not a robot")

The implementation shall support placeholder configuration until production keys are available.

Production keys shall never be committed to source control.

Environment variables only:

```
RECAPTCHA_SITE_KEY
RECAPTCHA_SECRET_KEY
```

Settings shall read both values from environment variables.

Do not store any keys inside `feature_flags.json`.

---

## Feature Flags

Extend `feature_flags.json` with behaviour flags only.

Required flags:

* `CAPTCHA_ENABLE`
* `CAPTCHA_PROVIDER`
* `CAPTCHA_TEST_MODE`

Example provider values:

* `google_v2`
* `turnstile`
* `none`

The provider abstraction shall allow future migration without major code changes.

---

## Google Verification Requirements

The verification service shall:

* POST to Google's `siteverify` endpoint
* Use a request timeout (maximum 5 seconds)
* Validate HTTP response
* Validate `success=true`
* Validate returned hostname
* Record returned error codes
* Handle network exceptions gracefully

Accepted hostnames:

* `propertism.in`
* `www.propertism.in`
* `localhost`

---

## Failover Behaviour

The implementation shall support configurable fail-open behaviour.

If Google's verification service is unavailable due to:

* timeout
* DNS failure
* network interruption
* temporary Google outage

the application shall:

* allow the enquiry to continue when configured
* record a warning log
* create a spam log entry

This behaviour shall be configurable through settings.

---

## Shared Template Component

Replace the existing arithmetic CAPTCHA component with a reusable reCAPTCHA template include.

The shared validation include shall automatically protect every form that uses it.

No form shall require duplicate implementation.

---

## Spam Logging

Create a reusable `SpamLog` model for security auditing.

Required fields:

| Field | Type |
|---|---|
| `timestamp` | DateTimeField (auto) |
| `ip_address` | GenericIPAddressField |
| `user_agent` | TextField |
| `form_name` | CharField(100) |
| `request_path` | CharField(200) |
| `referer` | CharField(200) |
| `failure_reason` | CharField(200) |
| `google_error_code` | CharField(100) |
| `confidence_score` | IntegerField |

`SpamLog` shall be visible within Django Admin.

---

## Logging

Application logging shall include:

**INFO**
* CAPTCHA rendered
* CAPTCHA passed

**WARNING**
* CAPTCHA failed
* Spam detected

**ERROR**
* Google verification unavailable
* Verification exceptions
* Unexpected verification failures

---

## Analytics

Expose security events for future reporting.

Track:

* CAPTCHA shown
* CAPTCHA passed
* CAPTCHA failed
* Spam blocked

The implementation shall be compatible with future DMC security dashboards.

---

## Deployment Requirements

Update:

* `.env.example`
* Deployment documentation
* AWS Elastic Beanstalk environment configuration guide

Required environment variables:

```
RECAPTCHA_SITE_KEY
RECAPTCHA_SECRET_KEY
```

Secrets shall never be committed to Git.

---

## Rollback

Setting:

```json
"CAPTCHA_ENABLE": false
```

shall immediately disable CAPTCHA enforcement without requiring code removal.

---

## Testing Requirements

| # | Test Case | Expected Result |
|---|---|---|
| T1 | Valid CAPTCHA token submitted | Form submits successfully |
| T2 | Missing CAPTCHA (no checkbox tick) | Rejected with error message |
| T3 | Invalid CAPTCHA token | Rejected with error message |
| T4 | Expired CAPTCHA token | Rejected with error message |
| T5 | Honeypot field populated | Silent reject, SpamLog entry |
| T6 | Rate limit exceeded | HTTP 429 |
| T7 | Submission time too fast (< 2s) | Rejected, SpamLog entry |
| T8 | Google timeout (> 5s) | Fail-open, enquiry proceeds, SpamLog warning |
| T9 | Google outage (network failure) | Fail-open, enquiry proceeds, SpamLog warning |
| T10 | Hostname mismatch | Rejected, SpamLog entry |
| T11 | Mobile browser | Widget renders, tappable |
| T12 | Desktop browser | Widget renders, clickable |
| T13 | CAPTCHA_ENABLE = false | No widget shown, form works normally |
| T14 | Provider abstraction (CAPTCHA_PROVIDER flag) | Correct provider loaded |

---

## Acceptance Criteria

Implementation shall be considered complete only when:

- [ ] All public forms are protected by the centralized framework
- [ ] Existing anti-spam mechanisms (honeypot, timing, rate limit, confidence score) remain intact
- [ ] Validation is centralized in `content/security/`
- [ ] Provider abstraction is implemented (`CAPTCHA_PROVIDER` flag)
- [ ] Secrets are environment-variable driven — no hardcoding
- [ ] SpamLog model created and admin-registered
- [ ] `.env.example` updated with new required variables
- [ ] `feature_flags.json` extended with `CAPTCHA_PROVIDER` flag
- [ ] Production can be enabled by configuring Google keys only — no further code changes
- [ ] All T1–T14 tests pass

---

*This SCCB supersedes the original SCCB-reCaptcha specification document.*
*Sign-off record is maintained in: `SCCB-PROP-SEC-001-SIGNOFF.md`*
