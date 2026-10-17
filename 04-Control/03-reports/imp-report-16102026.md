Viji, I completed the local investigation and made the additional local hardening changes. No production system, Lightsail server, database, logs, customer records, secrets, branch, commit, push, or deployment was touched.
Confirmed code-level root causes
1. Deployed HTML form CAPTCHA was bypassable/fail-open
   - In deployed baseline c8f03ae, missing RECAPTCHA_SECRET_KEY returned CAPTCHA success.
   - CAPTCHA could be skipped when CAPTCHA_ENABLE was false/missing/unreadable.
   - CAPTCHA network failures/timeouts could pass with RECAPTCHA_FAIL_OPEN=True.
   - This allowed public form requests to reach Inquiry.objects.create().
2. Likely Spam was classification, not a persistence block
   - Both HTML paths classified the request before persistence, but still stored Likely Spam.
   - Contact notifications were suppressed; property-detail notifications were not. I corrected the property-detail notification gap locally.
3. Rate-limit trust/dependency gaps
   - _get_ip() trusted any caller-provided first X-Forwarded-For value, permitting rate-limit identity spoofing where the app was directly reachable.
   - Cache outages/errors did not have an explicit fail-closed policy for form and realBOT rate limits.
   - Existing default settings have local process cache; a production Redis declaration exists, but the actual Lightsail settings/cache topology is unverified.
4. realBOT baseline risk
   - Baseline had no form-equivalent CAPTCHA/rate controls and hardcoded Genuine/80.
   - d58003c already corrected rate/nonce/timing/turn/replay/duplicate/classification controls. CAPTCHA for realBOT remains consciously deferred (C4).
Inquiry write paths verified
Route/path	Writes Inquiry?	Current protection
POST /contact/	Yes	Spam protection → lead assessment → persistence
POST /properties/inquiry/	Yes	Same protection/assessment sequence
realBOT session/conversation confirmation	Yes	Rate gates + server conversation state + nonce + timing + turns + duplicate guard
POST /chat/submit/	No	Writes ContactMessage
POST /api/landing-lead/	No	Writes LandingLead
GET /api/inquiries/	No	Read-only; separate PII/access-control issue


PropertyInquiry is an import alias of properties.models.Inquiry; both create calls write Django’s default properties_inquiry table.
Local files changed
File	Change
content/security/validators.py	Fail closed on cache read/write failure; accept X-Forwarded-For only when REMOTE_ADDR is in explicit trusted proxy config.
content/security/spam_protection.py	Returns a safe retry message when required rate-limit cache is unavailable.
chat/request_limits.py	Makes realBOT rate limits deny requests on cache failures/refused cache writes.
realtor_project/settings.py	Adds empty-by-default TRUSTED_PROXY_IPS, sourced from environment.
properties/views.py	Suppresses normal lead notification for property inquiries assessed as Likely Spam, while retaining the row for review/audit.
properties/test_security_fixes.py	Adds tests for forwarded-header trust and form cache failure/refused writes.
chat/tests_realbot_security.py	Adds realBOT cache-unavailability denial coverage.
04-Control/01-sccb/SCCB-09-PROPERTISM-SPAM-INCIDENT-END-TO-END-001.md	Added Sections 29.1–29.3 documenting scope, changes, evidence, and blockers.


Test status
- git diff --check on SCCB-09 files: passed.
- Django checks and automated tests: blocked before test discovery.
The project virtual environment is broken: .venv\Scripts\python.exe is bound to a removed Python installation at:
C:\Users\vijay\AppData\Local\Programs\Python\Python311\python.exe
Both manage.py check and the intended targeted suite fail immediately with that interpreter error. No tests executed, and no local test DB was created.
Once Python/venv is repaired, run:
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py test properties.test_security_fixes content.tests.CaptchaVerificationTests properties.tests.InquiryNotificationTests chat.tests_realbot_security
.venv\Scripts\python.exe manage.py test properties.test_security_fixes content.tests.CaptchaVerificationTests properties.tests.InquiryNotificationTests chat.tests_realbot_security chat.tests_m26
Remaining blockers / uncertainty
- Historical production causation remains unconfirmed. The source defect is confirmed, but proving whether /contact/, /properties/inquiry/, or realBOT generated the 13 October rows requires approved read-only Lightsail aggregate evidence.
- TRUSTED_PROXY_IPS must remain empty until the Lightsail/Nginx proxy peer IP is verified. This secure default avoids header spoofing but may aggregate users behind a proxy until configured.
- A shared production cache must be verified; local/default LocMem cannot reliably enforce a distributed multi-worker rate limit.
- There is no approved Inquiry quarantine status/schema. The implemented safe boundary retains Likely Spam rows for audit and prevents their normal notification workflow; automatic deletion or rejection needs an explicit business decision.
- realBOT CAPTCHA remains deferred, not implemented.
Git status
- Current branch: main
- HEAD: d58003c (existing local SCCB-09 remediation commit, not deployed to origin/main)
- New hardening edits are uncommitted.
- The tree already contained substantial unrelated modified/untracked work; it has been preserved.
- Nothing was committed, pushed, merged, deployed, or changed on production.