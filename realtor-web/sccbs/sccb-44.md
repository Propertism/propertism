SCCB ID: SCCB-44
SCCB Number: SCCB-44_STATIC_FILES_AND_MEDIA_INFRASTRUCTURE
Date (IST): 25-02-2026
Canonical Location: governance-canon/web/SCCB-44_STATIC_FILES_AND_MEDIA_INFRASTRUCTURE.md
Authority: Viji (Product Owner) + Mindra (Architecture Guard)
Applies To: Manthraa (Codex – Web Implementation)
Status: ✅ IMPLEMENTED (100% Complete)

**Implementation Date**: February 25, 2026  
**Completion Status**: 100% (6/6 tasks complete)

---

## 📁 IMPLEMENTATION FILES (Internal Tracking)

### Documentation
- `realtor-web/STATIC_FILES_COMPLETE.md` - Full implementation guide

### Configuration
- `realtor-web/realtor_project/settings.py` - Static/media configuration
- `realtor-web/realtor_project/settings_production.py` - WhiteNoise production config
- `realtor-web/.gitignore` - Excludes staticfiles/ and media/

### Validators
- `realtor-web/properties/validators.py` - Image validation utilities
  - `validate_image_file()` - General image validation
  - `validate_document_file()` - Document validation
  - `validate_property_image()` - Property-specific validation
  - `sanitize_filename()` - Security sanitization
  - `get_upload_path()` - Upload path generation

### Management Commands
- `realtor-web/properties/management/commands/test_static_media.py` - Configuration test

### Dependencies
- `whitenoise==6.6.0` - Already installed
- `pillow==10.1.0` - Already installed

### Directories
- `realtor-web/static/` - Source static files (version controlled)
- `realtor-web/staticfiles/` - Collected static (NOT in git)
- `realtor-web/media/` - User uploads (NOT in git)

---

## PURPOSE

Establish a secure, scalable, and production-ready static and media handling system for the Realtor Website.

This phase ensures:

* Static assets load reliably in production
* Media uploads are validated and secure
* Performance is optimized
* Deployment is stable

This is infrastructure-level correctness, not optional enhancement.

---

## PHASE 5 — STATIC FILES & MEDIA

---

## 1️⃣ Configure Static Files Collection (🔴 CRITICAL)

### Objective

Ensure production static assets are properly collected and served.

### Implementation Requirements

In Django settings:

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

Before deployment:

```
python manage.py collectstatic --noinput
```

Production must serve only from:

```
/staticfiles/
```

Never serve from development directories.

---

## 2️⃣ Set Up Media Files Storage (🔴 CRITICAL)

### Objective

Separate uploaded media from static assets.

In settings:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

Rules:

* Property images must be stored under:
  media/properties/
* User uploads must never mix with static/
* Media directory must NOT be version controlled

Add to `.gitignore`:

```
media/
staticfiles/
```

---

## 3️⃣ Configure WhiteNoise for Static (🟡 HIGH)

### Objective

Serve static files efficiently without requiring separate CDN initially.

Install:

```
pip install whitenoise
```

In `settings.py`:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ...
]
```

Enable compressed storage:

```python
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

Benefits:

* Gzip compression
* Cache busting via hashed filenames
* Long-term caching headers

---

## 4️⃣ Set Up Image Upload System (🟡 HIGH)

### Requirements

Property model must include:

```python
image = models.ImageField(upload_to="properties/")
```

Enable Pillow:

```
pip install pillow
```

Upload system must:

* Store images under media/properties/
* Support multiple images per property
* Prevent file name collisions

---

## 5️⃣ Add Image Validation (🟢 MEDIUM)

### Required Validation Rules

* Only allow:
  JPEG, PNG, WebP
* Reject:
  SVG (unless sanitized)
  Executable disguised as image
* Validate content-type and file signature
* Reject corrupted files

Example:

```python
from django.core.exceptions import ValidationError

def validate_image(file):
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("Image too large (max 5MB)")
```

---

## 6️⃣ Configure File Size Limits (🟢 MEDIUM)

Backend limits:

```python
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
```

Server (Nginx):

```
client_max_body_size 10M;
```

Frontend:

* Show upload progress
* Prevent upload above limit
* Display clear error messages

---

## SECURITY REQUIREMENTS

* Media directory must not allow script execution
* No direct upload to static/
* No public directory listing
* Validate file extension AND MIME type

---

## PERFORMANCE REQUIREMENTS

* Convert images to WebP where possible
* Lazy load property images
* Use responsive image sizes
* Compress large images automatically

---

## ACCEPTANCE CHECKLIST

Manthraa must confirm:

[ ] STATIC_ROOT configured correctly
[ ] collectstatic works in production
[ ] MEDIA_ROOT separated from static
[ ] WhiteNoise configured and verified
[ ] Property image upload functional
[ ] Image validation enforced
[ ] File size limits configured
[ ] No media tracked in Git

---

## GOVERNANCE RULE

Static = Code-controlled
Media = User-controlled

They must NEVER mix.

Any mixing is considered a production integrity violation.

---

This SCCB locks the foundation for production-grade static and media management.

END OF SCCB
