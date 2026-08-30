# SCCB-PROP-POSTGRES-RESTORATION-STATUS-1606

**Date**: 2026-06-16  
**Status**: IN PROGRESS - CONFIGURATION APPLIED, APP CRASHED (needs recovery)  
**Priority**: P0  

---

## Current Situation

### What We've Done

1. ✅ **Verified EB Environment**
   - Environment: `propertism-prod-2026` in us-east-1
   - Health was Green before changes

2. ✅ **Verified RDS Configuration**
   - `DATABASE_URL` environment variable: **SET** in EB
   - Value: `postgresql://propertismadmin:...@propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com:5432/propertismdb`
   - PostgreSQL RDS instance exists and is accessible

3. ✅ **Updated EB Configuration**
   - `.ebextensions/01_django.config`: Changed `DJANGO_SETTINGS_MODULE` from `settings` → `settings_production`
   - Committed and pushed via git
   - CI/CD automatically deployed (version: `gh-147-4d1521c...`)

4. ✅ **Set EB Environment Variable**
   - `eb setenv DJANGO_SETTINGS_MODULE=realtor_project.settings_production`
   - Applied successfully

### Current Problem

❌ **Application crashed after deployment**
- Latest attempted version tried to use `settings_production.py`
- `settings_production.py` is **incomplete** - missing `allauth` and other apps in `INSTALLED_APPS`
- Application failed to start with allauth error

❌ **EB Health: Red (application not responding)**
- 502 Bad Gateway from production URL
- Application crashed due to missing dependencies in settings file

### Root Cause of Crash

`settings_production.py` is outdated and incomplete:
```python
# Missing apps:
# - allauth
# - allauth.account
# - allauth.socialaccount
# - allauth.socialaccount.providers.google
# - chat
# - nri_assist
```

This caused: `RuntimeError: Model class allauth.account.models.EmailAddress doesn't declare an explicit app_label...`

---

## The Correct Approach

Instead of using the incomplete `settings_production.py`, we should:

1. **Keep using `settings.py`** (which has all apps configured)
2. **Modify `settings.py`** to prioritize `DATABASE_URL` environment variable
3. **Current logic in settings.py is already correct**, but environment variable isn't reaching it in shell

The settings.py already has this:
```python
def _get_local_postgres_config():
    database_url = _get_env_value('DATABASE_URL', 'LOCAL_DATABASE_URL')
    if database_url:
        return _database_config_from_url(database_url)
    # ... fallback logic
```

**The issue**: When Django runs via Gunicorn (production), it WILL have access to DATABASE_URL. But when we SSH and run `manage.py shell` manually, environment variables aren't inherited.

---

## Recovery Plan

### Immediate: Get Application Back Online

1. **Revert to working state**
   ```bash
   eb abortEnvironmentUpdate
   # OR
   git revert d28f156  # Undo the revert, go back to 4d1521c
   ```

2. **Keep the `.ebextensions` change** (which just sets the ENV VAR)

3. **Verify DATABASE_URL is properly configured** in EB environment (it is)

4. **Test that Gunicorn loads DATABASE_URL** correctly

### Permanent: Use settings.py with DATABASE_URL Priority

**Recommendation**: Stop trying to use `settings_production.py`. Instead:

1. Keep `.ebextensions` setting `DJANGO_SETTINGS_MODULE` to `settings` or `settings_production`
2. Ensure `settings.py` prioritizes `DATABASE_URL` when it's set
3. The database selection logic in `settings.py` already does this

**Why this works**:
- In **local development**: No `DATABASE_URL` → SQLite ✅
- In **production EB**: `DATABASE_URL` is set → PostgreSQL via RDS ✅

---

## Status of Changes Made

| Change | Status | Location |
|--------|--------|----------|
| `.ebextensions/01_django.config` updated | ✅ Deployed | Commit: 4d1521c |
| `manage.py` default changed | ⏮️ Reverted | Commit: d28f156 |
| `settings_production.py` attempted | ❌ Failed (incomplete) | Not used |

**Current Deployed Version**: `gh-147-4d1521c...` (has `.ebextensions` change, app crashed due to settings issue)

---

## Next Steps Required

### Step 1: Restore Application Health

Option A (Rollback to last working version):
```bash
eb setenv DJANGO_SETTINGS_MODULE=realtor_project.settings
# App will restart with original settings
```

Option B (Fix settings_production.py):
```
# Add missing apps to INSTALLED_APPS
# Add missing middleware
# Add missing configurations
# (This file needs significant work)
```

**Recommendation**: Option A (rollback is faster)

### Step 2: Verify DATABASE_URL is being used in Production

Once app is healthy, run in production:
```bash
# From Django shell with environment variable visible
python manage.py check  # Should pass
# Migrations should run against PostgreSQL
```

### Step 3: Verify PostgreSQL Connection

```bash
python manage.py migrate  # Should apply migrations to PostgreSQL
python manage.py seed_knowledge_hub_phase_a --publish  # Should seed to PostgreSQL
```

---

## Critical Discovery

**The good news**: RDS PostgreSQL is already properly configured in EB. The DATABASE_URL environment variable is set and ready.

**The issue**: We picked the wrong settings file. `settings_production.py` is not production-ready; it's incomplete.

**The solution**: Use `settings.py` which has all configurations. It already has the logic to use DATABASE_URL when present.

---

## Questions for Clarification

1. **Should we keep the `.ebextensions` change** (DJANGO_SETTINGS_MODULE set to settings_production)?
   - **Recommendation**: No. Use settings.py which has all required configurations.

2. **Is there an updated version of settings_production.py** that's complete?
   - **Recommendation**: Check with team. Current version is incomplete (missing apps/middleware).

3. **Can we just go back to using settings.py as-is**?
   - **Recommendation**: YES. It already has DATABASE_URL logic built in. It will use PostgreSQL when DATABASE_URL is set (production) and SQLite when it's not (local development).

---

## Sign-Off

**Investigation**: ✅ COMPLETE  
**Root Cause**: ✅ IDENTIFIED (settings_production.py incomplete)  
**Immediate Action**: Recover application (rollback settings change)  
**Long-term**: Use settings.py which correctly handles both SQLite (local) and PostgreSQL (production)  

---

**Status Timestamp**: 2026-06-16 06:36 UTC  
**Current App Health**: 🔴 Red (502 Bad Gateway)  
**Approval Needed**: For recovery step (rollback vs fix settings_production.py)
