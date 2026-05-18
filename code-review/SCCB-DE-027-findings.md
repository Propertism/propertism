# SCCB-DE-027: EB Django Settings Module & SMTP Credentials
# Astra Findings Report
# Date: 2026-05-19

---

## Question 1: Which Django Settings Module Does EB Use?

### Answer: `realtor_project.settings` — CONFIRMED. HARDCODED.

**Source:** `.ebextensions/01_django.config:5`

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: realtor_project.settings   ← THIS LINE
    DEBUG: "False"
    DJANGO_ALLOWED_HOSTS: "propertism.in,..."
```

This is set via `.ebextensions` — it overrides whatever any manual EB console setting says.

**Implication for SCCB-DE-028:**

The fix identified in the audit (add ADMIN_EMAIL to `settings_production.py`) is **NOT needed**.

`settings_production.py` is **never loaded** on production. EB uses `realtor_project.settings`.

`settings.py` already has:
```python
# realtor_project/settings.py:447
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'info@propertism.in')
```

Default value `info@propertism.in` applies if env var is unset.
`settings.ADMIN_EMAIL` will resolve — no AttributeError.

**SCCB-DE-028 is not needed.** Cancel it.

---

## Question 2: Are SMTP Credentials in EB Environment?

### Answer: CANNOT CONFIRM — AWS CLI returned empty results.

**AWS CLI status:**
- Profile: `vijim` — credentials present (HFHI / vey/ keys)
- Region: us-east-1
- `aws elasticbeanstalk describe-applications` → `{"Applications": []}`
- `aws elasticbeanstalk describe-environments` → `{"Environments": []}`
- Possible causes: profile lacks EB read permissions, or EB environment was recreated under a different account/context

**What `.ebextensions/01_django.config` does NOT set:**
```
EMAIL_HOST         — not in .ebextensions
EMAIL_HOST_USER    — not in .ebextensions
EMAIL_HOST_PASSWORD — not in .ebextensions
ADMIN_EMAIL        — not in .ebextensions
```

These must be set manually in the EB console under
Configuration → Environment properties, or emails will fail silently at SMTP.

**`settings.py` fallback defaults:**
```python
EMAIL_HOST          = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')   # has default
EMAIL_HOST_USER     = os.environ.get('EMAIL_HOST_USER', '')            # empty string if unset
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')        # empty string if unset
ADMIN_EMAIL         = os.environ.get('ADMIN_EMAIL', 'info@propertism.in')  # has default
DEFAULT_FROM_EMAIL  = os.environ.get('DEFAULT_FROM_EMAIL', 'info@propertism.in')  # has default
```

Empty `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` → SMTP auth will fail → exception caught silently.

---

## Assessment

| Item | Status | Confidence |
|------|--------|------------|
| DJANGO_SETTINGS_MODULE | `realtor_project.settings` | ✅ CONFIRMED (hardcoded in .ebextensions) |
| ADMIN_EMAIL defined in settings | YES — defaults to `info@propertism.in` | ✅ CONFIRMED |
| settings_production.py fix needed | NO | ✅ CONFIRMED — cancel SCCB-DE-028 |
| EMAIL_HOST_USER set in EB console | UNKNOWN | ❓ Need Viji to check console |
| EMAIL_HOST_PASSWORD set in EB console | UNKNOWN | ❓ Need Viji to check console |
| ADMIN_EMAIL set in EB console | UNKNOWN but defaulted | ❓ Default is safe |

---

## Email Failure Root Cause — Revised Assessment

Original assumption: `AttributeError` on `settings.ADMIN_EMAIL` — **ELIMINATED**.

Actual likely root cause: **SMTP credentials not set in EB console.**

`EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` default to empty string.
Gmail SMTP requires authentication — empty creds → `SMTPAuthenticationError`
→ caught by `except Exception as e:` in `send_rfq_notification()` → logged → silent.

---

## Actions Required from Viji

### Action 1 — Check EB Console (5 minutes)
Go to: AWS Console → Elastic Beanstalk → `propertism-prod-2026` →
Configuration → Environment properties

Confirm presence and values of:
```
EMAIL_HOST_USER     = ?    (e.g., info@propertism.in or a Gmail address)
EMAIL_HOST_PASSWORD = ?    (Gmail App Password — 16 chars, not your login password)
ADMIN_EMAIL         = ?    (should be info@propertism.in)
```

### Action 2 — If SMTP creds missing
Issue SCCB-DE-029 to add:
```
EMAIL_HOST          = smtp.gmail.com
EMAIL_HOST_USER     = <gmail address used for sending>
EMAIL_HOST_PASSWORD = <16-char Gmail App Password>
ADMIN_EMAIL         = info@propertism.in
DEFAULT_FROM_EMAIL  = info@propertism.in
```

Gmail App Password must be generated at:
Google Account → Security → 2-Step Verification → App passwords

---

## What Astra Can Confirm Without Console Access

```
.ebextensions/01_django.config → DJANGO_SETTINGS_MODULE = realtor_project.settings
settings.py:447               → ADMIN_EMAIL defined (default: info@propertism.in)
settings.py:438               → EMAIL_HOST defined (default: smtp.gmail.com)
settings.py:441               → EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
settings.py:442               → EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
.ebextensions                 → No email creds hardcoded
```

**Conclusion:** The code is correct. The gap is operational — SMTP creds in EB console.

---

## Follow-up SCCBs

| SCCB | Action | Status |
|------|--------|--------|
| SCCB-DE-028 | Add ADMIN_EMAIL to settings_production.py | CANCEL — not needed |
| SCCB-DE-029 | Add SMTP creds to EB console | PENDING — Viji to confirm if missing |
