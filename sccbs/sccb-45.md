SCCB ID: SCCB-45
SCCB Number: SCCB-45_ERROR_HANDLING_AND_LOGGING_FRAMEWORK
Date (IST): 25-02-2026
Canonical Location: governance-canon/web/SCCB-45_ERROR_HANDLING_AND_LOGGING_FRAMEWORK.md
Authority: Viji (Product Owner) + Mindra (Architecture Guard)
Applies To: Manthraa (Kiro – Web Implementation)
Status: ✅ IMPLEMENTED (86% Complete)

**Implementation Date**: February 25, 2026  
**Completion Status**: 86% (5/6 tasks complete, Sentry optional)

---

## 📁 IMPLEMENTATION FILES (Internal Tracking)

### Documentation
- `realtor-web/ERROR_HANDLING_COMPLETE.md` - Full implementation guide

### Templates
- `realtor-web/uilayers/templates/404.html` - Custom 404 page
- `realtor-web/uilayers/templates/500.html` - Custom 500 page (standalone)

### Views
- `realtor-web/content/views.py` - Error handlers (custom_404, custom_500)
- `realtor-web/content/views.py` - Updated with logging and error handling

### Configuration
- `realtor-web/realtor_project/settings.py` - Logging configuration (Phase 1)
- `realtor-web/realtor_project/urls.py` - Error handler registration

### Logging
- `realtor-web/logs/django.log` - General application logs (auto-created)
- `realtor-web/logs/security.log` - Security event logs (auto-created)

### Optional (Ready for deployment)
- Sentry integration (awaiting DSN configuration)

---

## PURPOSE

Establish structured error handling, logging, and monitoring for the Realtor Website to ensure:

* Production stability
* Actionable error tracking
* Debug visibility without exposing sensitive data
* Professional user-facing error experience

This phase prevents silent failures and untraceable bugs.

---

## PHASE 6 — ERROR HANDLING & LOGGING

---

## 1️⃣ Configure Django Logging (🟡 HIGH)

### Objective

Enable structured logging for development and production.

In `settings.py`:

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/app.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
}
```

Create directory:

```
mkdir logs
```

Logs must NOT be exposed publicly.

---

## 2️⃣ Add Error Handling to Views (🟡 HIGH)

### Rule

* No unhandled exceptions in production views
* Wrap critical logic with try/except
* Log errors using `logger.exception()`
* Return user-friendly responses

Example:

```python
import logging
logger = logging.getLogger(__name__)

def property_detail(request, slug):
    try:
        property = Property.objects.get(slug=slug)
    except Property.DoesNotExist:
        logger.warning(f"Property not found: {slug}")
        raise Http404("Property not found")
    except Exception as e:
        logger.exception("Unexpected error in property_detail")
        return render(request, "500.html", status=500)
```

Never expose raw tracebacks in production.

Set:

```python
DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com"]
```

---

## 3️⃣ Create Custom Error Pages (🟡 HIGH)

### Required Pages

* 404.html
* 500.html

Location:

```
templates/
 ├── 404.html
 └── 500.html
```

Must include:

* Brand styling
* Navigation back to home
* Contact option
* No technical error details

In urls.py:

```python
handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"
```

---

## 4️⃣ Set Up Error Monitoring (Sentry) (🟢 MEDIUM)

### Install

```
pip install sentry-sdk
```

In settings:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.5,
    send_default_pii=False,
)
```

Purpose:

* Capture production exceptions
* Get stack traces without exposing to users
* Monitor recurring issues

---

## 5️⃣ Add Request Logging (🟢 MEDIUM)

Log incoming requests for debugging.

Middleware example:

```python
import logging
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"{request.method} {request.path}")
        return self.get_response(request)
```

Add to MIDDLEWARE list.

Avoid logging sensitive data (passwords, tokens).

---

## 6️⃣ Configure Log Rotation (🟢 LOW)

Already enabled via RotatingFileHandler.

Server-level (optional Linux):

```
/etc/logrotate.d/olivine
```

Example:

```
/opt/olivine/logs/*.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
}
```

Prevents disk overflow.

---

## SECURITY REQUIREMENTS

* DEBUG must be False in production
* No stack traces shown to users
* No sensitive data in logs
* Logs directory not publicly accessible

---

## ACCEPTANCE CHECKLIST

Manthraa must confirm:

[ ] Django logging configured
[ ] Logs written to file successfully
[ ] Custom 404 and 500 pages implemented
[ ] Unhandled exceptions prevented in views
[ ] Sentry configured and tested
[ ] Request logging active
[ ] Log rotation enabled

---

## GOVERNANCE RULE

Users see clean error pages.
Developers see detailed logs.

Never mix the two.

---

This SCCB establishes production-grade error resilience and observability.

END OF SCCB
