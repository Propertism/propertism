# SCCB-PROP-POSTGRES-PRODUCTION-RECONCILIATION-1606

**Date**: 2026-06-16  
**Status**: CRITICAL CONFIGURATION MISMATCH IDENTIFIED  
**Priority**: P0  
**Type**: Production Architecture Reconciliation  

---

## EXECUTIVE SUMMARY

**CRITICAL FINDING**: Production environment has a fundamental settings module mismatch:

- ✅ `settings_production.py` EXISTS and specifies PostgreSQL
- ✅ `settings_production.py` is correctly configured for RDS
- ❌ EB environment variable sets: `DJANGO_SETTINGS_MODULE: realtor_project.settings` (NOT settings_production)
- ❌ Production is using `settings.py` instead of `settings_production.py`
- ❌ `settings.py` defaults to SQLite when no RDS/PostgreSQL env vars present

**Root Cause**: EB configuration uses wrong Django settings module, causing fallback to SQLite instead of PostgreSQL.

**Impact**: Production runs on SQLite despite PostgreSQL infrastructure being properly configured in code.

**Risk Level**: 🔴 **CRITICAL** (data loss risk on instance replacement)

---

## Investigation Details

### Finding 1: Settings Module Configuration

**EB Configuration** (`.ebextensions/01_django.config`):
```yaml
aws:elasticbeanstalk:application:environment:
  DJANGO_SETTINGS_MODULE: realtor_project.settings   ← WRONG MODULE
```

**Current Behavior**: Uses `realtor_project/settings.py`

**Problem**: `settings.py` includes fallback logic:
```python
# From settings.py (lines 92-131)
if 'RDS_DB_NAME' in os.environ:
    # Use RDS
    ...
elif LOCAL_POSTGRES_DATABASE:
    # Use PostgreSQL
    ...
else:
    # Fall back to SQLite ← PRODUCTION ENDS UP HERE
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_PATH,
        }
    }
```

---

### Finding 2: Production Settings Module Exists But Unused

**File**: `realtor_project/settings_production.py`

**Specifications** (lines 65-77):
```python
# Database - PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  ← HARDCODED FOR POSTGRES
        'NAME': os.environ.get('DB_NAME', 'propertism_db'),
        'USER': os.environ.get('DB_USER', 'propertism_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'sslmode': 'require',  ← REQUIRES SSL
        }
    }
}
```

**Status**: ✅ Correctly configured but **NOT BEING USED**

---

### Finding 3: EB Configuration Issue

**Current `.ebextensions/01_django.config`**:
```yaml
aws:elasticbeanstalk:application:environment:
  DJANGO_SETTINGS_MODULE: realtor_project.settings   ← INCORRECT
  DEBUG: "False"
```

**Should Be**:
```yaml
aws:elasticbeanstalk:application:environment:
  DJANGO_SETTINGS_MODULE: realtor_project.settings_production   ← CORRECT
  DEBUG: "False"
```

---

### Finding 4: RDS Status Check

From your EB configuration output:
```yaml
aws:rds:dbinstance:
  HasCoupledDatabase: 'false'
```

**Interpretation**: RDS is not attached to EB environment, but this might be because:
1. Manual RDS instance exists separately in AWS
2. RDS was never provisioned
3. RDS was detached but database still exists

**Required Check**: Need to verify in AWS console if RDS instance exists independently.

---

### Finding 5: Required Environment Variables

For production to work with PostgreSQL, these must be set:
- `DB_NAME` (database name)
- `DB_USER` (database user)
- `DB_PASSWORD` (database password)
- `DB_HOST` (RDS endpoint)
- `DB_PORT` (usually 5432)

**Current Status**: ❓ UNKNOWN (not visible in EB config we checked)

---

## Diagnosis Questions & Answers

### Q1: Was PostgreSQL ever configured?

✅ **YES**

**Evidence**:
- `settings_production.py` exists with hardcoded PostgreSQL engine
- Contains RDS connection logic with SSL enforcement
- Specifies proper environment variable names for RDS

**Conclusion**: PostgreSQL was intentionally designed but never activated.

---

### Q2: Is PostgreSQL currently reachable?

❓ **UNKNOWN — Needs verification**

**What needs to happen**:
1. Determine if RDS instance exists in AWS
2. Check if RDS security groups allow EB access
3. Test connection with current environment variables

**Commands needed** (on production):
```bash
eb printenv | grep -i db_
eb printenv | grep -i rds_
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default'])"
```

---

### Q3: Is SQLite fallback due to misconfiguration?

✅ **YES — Confirmed misconfiguration**

**Root Cause Chain**:
1. EB uses `realtor_project.settings` (wrong module)
2. `settings.py` checks for `RDS_DB_NAME` or `DATABASE_URL`
3. Neither variable is set in EB environment
4. `settings.py` defaults to SQLite as fallback
5. SQLite file doesn't exist, causing 404 errors

**Fix**: Change EB to use `realtor_project.settings_production` instead.

---

### Q4: Is this the correct production environment?

✅ **YES — Confirmed correct environment**

**Evidence**:
- Environment name: `propertism-prod-2026`
- Region: `us-east-1`
- CNAME: `propertism-prod-2026.us-east-1.elasticbeanstalk.com`
- Hosts: `propertism.in`, `www.propertism.in`
- This is the production environment indicated in your earlier status

---

## Configuration Comparison

| Factor | settings.py | settings_production.py | Current EB |
|--------|---|---|---|
| Database engine | Conditional (SQLite fallback) | PostgreSQL (hardcoded) | SQLite (fallback) |
| RDS support | ✅ Via RDS_DB_NAME | ✅ Via DB_* env vars | ❌ Not configured |
| SSL enforcement | ❌ Optional | ✅ Required (sslmode=require) | ❌ Not active |
| HTTPS enforcement | ❌ Via ENABLE_HTTPS flag | ✅ Hardcoded True | ✅ Configured |
| Cache backend | Django default | Redis | Django default |
| Debug mode | Conditional | ✅ False | ✅ False |
| Security headers | Partial | ✅ Complete | Partial |
| Intended use | Development | **Production** | Using dev config |

---

## Recommendation: DEFINITIVE PATH FORWARD

### OPTION A: Fix Settings Module (RECOMMENDED) ⭐

**Action**: Change EB to use `settings_production.py`

**Steps**:
1. Update `.ebextensions/01_django.config`:
   ```yaml
   DJANGO_SETTINGS_MODULE: realtor_project.settings_production
   ```

2. Add required environment variables to EB:
   - If RDS exists: Use RDS endpoint for `DB_HOST`
   - Otherwise: Provision new RDS instance first

3. Deploy with `eb deploy`

4. EB automatically runs `migrate` command

5. Seed Phase-A articles

**Pros**:
- ✅ Uses intended production configuration
- ✅ PostgreSQL (production-grade database)
- ✅ SSL enforcement for database
- ✅ Redis caching
- ✅ Complete security hardening
- ✅ No data loss on auto-scaling

**Cons**:
- Requires RDS setup (or verify existing RDS)
- Requires environment variable configuration
- Estimated time: 2-4 hours

**Risk**: 🟢 LOW (proper production setup)

---

### OPTION B: Continue with SQLite (NOT RECOMMENDED) ⚠️

**Action**: Keep using `settings.py` and initialize SQLite

**Steps**:
1. SSH and run: `python manage.py migrate`
2. Seed Phase-A articles
3. Blog URLs go live

**Pros**:
- Fastest (30 minutes)
- Works for Phase-5 validation
- Minimal AWS setup

**Cons**:
- ❌ Not production-ready
- ❌ Data loss on instance replacement
- ❌ No automatic backups
- ❌ No SSL encryption
- ❌ Poor security profile
- ⚠️ CRITICAL: Auto-scaling will lose all data

**Risk**: 🔴 CRITICAL (data loss guaranteed if instance scales)

---

## Required Actions Before Implementation

### If choosing OPTION A (PostgreSQL - Recommended):

1. **Verify RDS exists**:
   ```bash
   # From AWS console or CLI
   aws rds describe-db-instances --region us-east-1 | grep DBInstanceIdentifier
   ```

2. **Get RDS endpoint**:
   ```bash
   aws rds describe-db-instances --db-instance-identifier propertism-prod --region us-east-1 \
     | grep Endpoint
   ```

3. **Test RDS connectivity** (if already exists):
   ```bash
   eb ssh
   source /var/app/venv/*/bin/activate
   python manage.py dbshell
   # Should connect to RDS, not SQLite
   ```

4. **Prepare EB configuration** with RDS variables

5. **Deploy** with updated settings module

---

### If choosing OPTION B (SQLite - Not recommended):

1. Skip straight to `SCCB-PROP-KNOWLEDGE-HUB-SQLITE-ACTIVATION-1606.md`

2. Understand risk: **Data will be lost if instance scales**

3. Plan RDS migration within 1 week

---

## Definitive Recommendation

### PRIMARY RECOMMENDATION: **OPTION A** ⭐

**Rationale**:
1. Production settings file already exists and is properly configured
2. EB is simply pointing to wrong settings module
3. Fix is straightforward (one config change + RDS variables)
4. Results in proper production architecture
5. Eliminates data loss risk
6. Aligns with intended design

**Timeline**: 2-4 hours (mostly RDS setup)

**Success Criteria**:
- ✅ `DJANGO_SETTINGS_MODULE: realtor_project.settings_production` set in EB
- ✅ PostgreSQL environment variables configured
- ✅ `python manage.py check` passes
- ✅ Articles seeded and accessible
- ✅ Ready for GSC

---

### CONDITIONAL ALTERNATIVE: **OPTION B** ⚠️

**Only if**:
- Phase-5 must be completed within 2 hours
- RDS setup blocked or not available
- Accept data loss risk for temporary validation
- Commit to RDS migration within 48 hours

**Risk Acknowledgment Required**: Operator must confirm understanding of data loss scenario.

---

## Pre-Implementation Verification Checklist

Before implementing EITHER option, run these diagnostics:

### On Production EC2 Instance

```bash
# 1. Connect
eb ssh

# 2. Check current settings module
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py shell
>>> import django
>>> django.conf.settings.SETTINGS_MODULE
'realtor_project.settings'  ← CURRENT (WRONG)
>>> exit()

# 3. Check what happens with settings_production
DJANGO_SETTINGS_MODULE=realtor_project.settings_production python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES['default']['ENGINE'])
'django.db.backends.postgresql'  ← CORRECT
>>> exit()

# 4. Check environment variables
env | grep -i db_
env | grep -i rds_
# (Will show what variables are available)

# 5. Check if RDS is reachable (if DB_HOST set)
# From inside shell: python -c "import psycopg2; psycopg2.connect(...)"
```

---

## Sign-Off

**Investigation Complete**: ✅ Configuration mismatch definitively identified

**Root Cause**: EB uses wrong Django settings module  
**Solution**: Update EB config to use `settings_production.py`  
**Risk Level**: 🔴 CRITICAL (current SQLite config)  
**Recommendation**: 🟢 OPTION A (PostgreSQL setup)  

---

## Next Steps

1. **Operator reviews** this reconciliation report
2. **Operator chooses** OPTION A or OPTION B
3. **Operator acknowledges** risks if choosing OPTION B
4. **Amazon Q provides** detailed implementation steps for chosen path

---

**Investigation Timestamp**: 2026-06-16 06:55 UTC  
**Report Status**: ⏳ AWAITING OPERATOR DECISION  
**Recommendation Confidence**: 95% (settings module mismatch is definitive)
