<!-- AUDIT METADATA -->
<!-- Date: 2026-10-16 -->
<!-- Timezone: Asia/Kolkata -->
<!-- Product Owner: Viji -->
<!-- Author: Codex (Astra) -->
<!-- Module: 03-propertism -->
<!-- Incident: SCCB-09 -->
<!-- Status: SOURCE-LEVEL FINDINGS COMPLETE — PRODUCTION CAUSATION UNCONFIRMED -->

# Codex findings — Propertism spam injection
## 16 October 2026

**Canonical incident control:** `04-Control/01-sccb/SCCB-09-PROPERTISM-SPAM-INCIDENT-END-TO-END-001.md`  
**Deployment baseline reviewed:** `origin/main` / `c8f03ae209d1102a74a60462159a16168dbe945a` (9 September 2026)  
**Local remediation commit:** `d58003c7215d8a0b8966620ae36bd676d3cd005a` — not deployed  
**Scope:** local source and Git-history trace only. No production endpoint, Lightsail host, database, log, secret, or customer record was accessed.

---

## 1. Executive finding

The deployed code had a **confirmed CAPTCHA-enforcement vulnerability** on public HTML inquiry forms. A request could reach `Inquiry.objects.create()` when CAPTCHA was disabled/skipped, when the CAPTCHA secret was absent, or when Google verification experienced a network failure under the default fail-open policy.

The application also classified suspicious content as `Likely Spam` **after deciding to persist it**. That classification did not prevent insertion or quarantine. Therefore, a high volume of `Likely Spam` rows is consistent with a successful automated submission attack.

**Most likely injection route (moderate confidence):** automated direct POST submissions to the public contact form and/or property inquiry form while one of the CAPTCHA bypass states was active.

**Important limitation:** source code establishes the vulnerable mechanism, but it cannot prove which endpoint or runtime configuration was responsible for the reported approximately 1,400 rows on 13 October 2026. That requires read-only, aggregate-only Lightsail evidence.

---

## 2. Confirmed Inquiry write paths

Only the following three application paths persist `properties.Inquiry` in the reviewed baseline.

| Priority | Public trigger | Execution path | Protection state in deployed baseline | Fit to reported incident |
|---|---|---|---|---|
| High | `POST /contact/` | `content.views.contact()` → `SpamProtectionService.validate()` → `LeadValidator.validate()` → `PropertyInquiry.objects.create()` | CAPTCHA boundary vulnerable; honeypot/timing/rate-limit controls present but insufficient alone | Strong fit for a one-message promotional payload |
| High | `POST /properties/inquiry/` | `properties.views.create_inquiry()` → same service and validator sequence → `Inquiry.objects.create()` | Same vulnerable CAPTCHA boundary | Strong fit; requires a valid property identifier |
| Adjacent risk | realBOT public session/initiate/query flow | conversation confirmation → `InquirySubmissionAdapter.submit()` → `PropertyInquiry.objects.create()` | No HTML CAPTCHA, honeypot, timing validation, or endpoint rate limit in baseline | Technically capable, but no evidence links reported rows to this multi-step route |

### Paths that do not explain `Inquiry` inserts

| Path | Finding |
|---|---|
| `GET /api/inquiries/` | Read-only endpoint. It was a serious PII confidentiality exposure, but cannot create `Inquiry` rows. |
| `POST /chat/submit/` | Creates `ContactMessage`, not `Inquiry`. |
| `POST /api/landing-lead/` | Creates `LandingLead`, not `Inquiry`. |
| Newsletter endpoint | Creates `Newsletter`, not `Inquiry`. |

---

## 3. End-to-end mechanism on public HTML forms

### 3.1 Flow

```text
Unauthenticated external POST
    │
    ├─ /contact/ or /properties/inquiry/
    │
    ├─ SpamProtectionService.validate()
    │   ├─ honeypot
    │   ├─ IP cache rate limit
    │   ├─ form timing
    │   └─ reCAPTCHA (conditional / fail-open in baseline)
    │
    ├─ LeadValidator.validate()
    │   └─ assigns Likely Spam / Review / Genuine classification
    │
    └─ Inquiry.objects.create()
        └─ row persists even if classified Likely Spam
```

### 3.2 Confirmed CAPTCHA bypass or fail-open states

| Condition in deployed baseline | Code behaviour | Effect |
|---|---|---|
| `CAPTCHA_ENABLE` disabled, missing, unreadable, or feature file unavailable | `is_feature_enabled('CAPTCHA_ENABLE', default=False)` returns false | CAPTCHA verification is skipped. |
| `RECAPTCHA_SECRET_KEY` absent | Google provider returned `success=True` with `secret-key-missing` | Submission proceeds as though CAPTCHA passed. |
| Google network error, timeout, or unexpected verification error | `RECAPTCHA_FAIL_OPEN` defaulted to true | Submission proceeds; only a SpamLog entry records `captcha-network-error-fail-open`. |

### 3.3 Why the residual checks did not prevent a bulk attack

- **Honeypot:** a bot avoids detection simply by leaving the hidden field blank.
- **Form timing:** missing or malformed `form_render_time` passes; it is not evidence of a human user.
- **Rate limit:** five posts per IP per ten-minute window does not stop a distributed bot network. Its production effectiveness also depends on the active cache backend and correct proxy trust.
- **Client IP:** code trusts the first `X-Forwarded-For` value, which must be validated against the production reverse-proxy configuration.
- **Lead classification:** suspicious content is labelled only after the prior security gate permits the request. The row is intentionally retained for audit, rather than rejected or quarantined.

---

## 4. Why the HTML form route is the leading hypothesis

The incident description reports Russian-language promotional/scam text containing `share.google` links, with roughly 1,400 entries in one day.

That shape is consistent with a bot making independent, one-shot public form submissions. The public contact and property inquiry forms accept the message fields directly and persist them in one request once the CAPTCHA boundary is bypassed.

This is more consistent with the report than realBOT, which requires a session, multiple collected fields, a transition to confirmation, and a confirmation message. This comparison is a likelihood judgement only; it does not prove the actual route.

---

## 5. realBOT adjacent injection risk

The deployed realBOT route was independently unsafe:

- Its public JSON endpoints were CSRF-exempt.
- It could persist `Inquiry` after a conversation confirmation.
- The adapter did not invoke `SpamProtectionService`; there was no HTML CAPTCHA, honeypot, or timing barrier.
- It had no request-rate limits on session initialization, message submission, or inquiry initiation.
- It hardcoded `confidence_score = 80` and `assessment_status = 'Genuine'`.

This is a valid separate injection risk. It cannot, however, be named as the cause of the 13 October event without production evidence that affected rows have a `form_source` beginning with `realBOT` or corresponding realBOT conversation data.

---

## 6. SCCB-09 local remediation status

The local SCCB-09 change set (`d58003c`) addresses the identified weaknesses but is **not in production**:

| Control | Local remediation |
|---|---|
| CAPTCHA defaults | Fail-closed by default; forced fail-closed in production. |
| Missing CAPTCHA secret | Fails verification instead of returning success. |
| Disabled/null CAPTCHA provider | Fails closed in production. |
| realBOT request flood | Cache-backed limits added for session init, messages, and inquiry initiation. |
| realBOT persistence | Single-use nonce, minimum 20 seconds, two engine turns, duplicate guard. |
| realBOT classification | Removes hardcoded Genuine/80; uses lead validation or leaves pending validation. |
| Inquiry read API | Restricts read access to staff/session or the approved server-to-server Deal Engine key. |

The deployment remains deliberately gated by service-key verification and the approved SCCB-09 cutover order. No conclusion in this report authorizes deployment or a production data change.

---

## 7. Evidence required to establish the actual 13 October root cause

Collect the following from Lightsail using read-only, aggregate-only commands. Do not print inquiry bodies, names, emails, phones, IP addresses, tokens, secrets, or database credentials.

1. **Inquiry aggregates:** 13 October 2026, Asia/Kolkata — counts by hour, `form_source`, and `assessment_status`.
2. **Pattern aggregates:** count promotional-pattern matches (for example, `share.google`, relevant campaign marker, or Cyrillic indicator) grouped by `form_source` and hour.
3. **SpamLog aggregates:** counts by failure reason, form name, request path, and hour, especially CAPTCHA failures and `captcha-network-error-fail-open`.
4. **Nginx aggregates:** request counts by path, method, status, and hour for `/contact/`, `/properties/inquiry/`, realBOT endpoints, and `/api/inquiries/`.
5. **Runtime posture, no values:** Django settings module; CAPTCHA enabled/provider flags; whether site and secret keys were set; fail-open flag; cache backend; and realBOT enablement.
6. **realBOT correlation:** count rows whose `form_source` begins `realBOT`, plus aggregate counts of confirmed inquiry conversations for the same period.

---

## 8. Final conclusion

### Confirmed

The deployed public HTML inquiry paths had a CAPTCHA enforcement defect: they could accept and persist automated requests when CAPTCHA was skipped, missing its secret, or failed open. Post-persistence lead classification allowed suspicious records to remain in the Inquiry table.

### Most likely

The reported spam injection came through high-volume automated POSTs to `/contact/` and/or `/properties/inquiry/` during one of those CAPTCHA bypass conditions.

### Not confirmed

The exact endpoint, exact runtime condition, precise count, source IP distribution, and any contribution from realBOT are not yet proven. `GET /api/inquiries/` is not a spam write path.

**Incident state:** SCCB-09 Track A remains **OPEN** until the production aggregate evidence is reconciled with these write paths.

