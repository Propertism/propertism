# Inquiry Email Audit Report
# SCCB Scope: Inquiry form → save + email to info@propertism.in
# Date: 2026-05-18

---

## 1. Does it save to Inquiries model?

YES — confirmed working.

The `contact()` view in `content/views.py:284` saves to `properties.Inquiry`
(imported as `PropertyInquiry`), NOT `content.ContactInquiry`.

```python
inquiry = PropertyInquiry.objects.create(
    name=request.POST.get("name"),
    email=request.POST.get("email"),
    phone=request.POST.get("phone", ""),
    message=request.POST.get("message"),
    property=None,
    status='pending'
)
```

Admin path: https://propertism.in/admin/properties/inquiry/

---

## 2. Does it trigger email to info@propertism.in?

CODE EXISTS — but PRODUCTION STATUS: UNCERTAIN / LIKELY BROKEN

### The email chain:
```
contact() view [content/views.py:296]
  └── send_rfq_notification(inquiry) [content/views.py:332]
        └── send_mail(
              subject="🚀 New Propertism Lead: ...",
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[settings.ADMIN_EMAIL],   ← RISK HERE
            )
```

---

## 3. Critical Risks Found

### RISK-1: `settings.ADMIN_EMAIL` missing in production settings

`settings_production.py` does NOT define `ADMIN_EMAIL` as a top-level key.
It only references it inside `ADMINS` list:

```python
# settings_production.py
ADMINS = [
    ('Admin', os.environ.get('ADMIN_EMAIL', 'admin@propertism.com')),
]
# NO standalone: ADMIN_EMAIL = ...
```

`settings.py` (dev) correctly defines:
```python
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'info@propertism.in')
```

If production runs `settings_production.py`, then `settings.ADMIN_EMAIL`
raises `AttributeError` → caught silently → NO EMAIL SENT.

### RISK-2: Exception is swallowed silently

```python
# content/views.py:295-299
try:
    send_rfq_notification(inquiry)
except Exception as email_exc:
    logger.error("Failed to send email notification: %s", email_exc)
    # Don't fail the request if email fails
```

Email failure only shows in server logs — invisible to user and Viji.

### RISK-3: Email SMTP credentials may not be set in EB

`settings_production.py:321-322`:
```python
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')   # None if unset
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')   # None if unset
```
If these env vars are not configured in Elastic Beanstalk, SMTP will fail.

### RISK-4: Model/test mismatch (secondary)

Tests in `tests/test_forms.py` count `ContactInquiry.objects.count()` 
but the live view saves to `properties.Inquiry`. Tests may pass but
measure the wrong model.

---

## 4. Fix Required

Add to `settings_production.py` (EMAIL section, after line 323):

```python
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'info@propertism.in')
```

Also verify in AWS EB environment variables:
- `ADMIN_EMAIL` = info@propertism.in
- `EMAIL_HOST_USER` = <gmail address>
- `EMAIL_HOST_PASSWORD` = <gmail app password>

---

## 5. File Locations

| Item | File | Line |
|------|------|------|
| contact() view | content/views.py | 280 |
| send_rfq_notification() | content/views.py | 332 |
| ADMIN_EMAIL (dev) | realtor_project/settings.py | 447 |
| ADMIN_EMAIL (prod — MISSING) | realtor_project/settings_production.py | — |
| ContactInquiry model (unused) | content/models.py | 533 |
| PropertyInquiry model (in use) | properties/models.py | — |

---

## Status Summary

| Check | Status |
|-------|--------|
| Inquiry saves to DB | ✅ Working (properties.Inquiry) |
| Email code exists | ✅ Yes (send_rfq_notification) |
| Email reaches production | ❌ Likely broken — ADMIN_EMAIL missing in settings_production.py |
| SMTP credentials in EB | ❓ Unknown — needs verification |

**Action needed from Viji: confirm which settings file EB uses, then apply fix.**
