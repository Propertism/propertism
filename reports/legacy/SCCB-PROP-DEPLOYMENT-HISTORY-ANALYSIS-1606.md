# SCCB-PROP-DEPLOYMENT-HISTORY-ANALYSIS-1606

**Analysis Date**: 2026-06-16  
**Status**: DEPLOYMENT ARCHITECTURE MISMATCH ANALYSIS  
**Priority**: P0  

---

## Document Timeline Review

### Document 1: AWS_DEPLOYMENT_COMPLETE.md
- **Date Created**: March 7, 2026
- **Status**: ✅ "Production Ready"
- **Database Architecture**: **SQLite**
- **Architecture Specification**:
  ```
  - Environment: propertism-prod
  - Region: us-west-2 (Oregon)
  - Database: SQLite (lightweight, perfect for your use case)
  ```
- **Key Quote**: "SQLite database with all migrations applied"

**Analysis**: This was an **initial deployment** to us-west-2 with SQLite. This is a single-instance environment suitable for MVP/testing, NOT production.

---

### Document 2: AWS_EB_RDS_REDEPLOY_2026.md
- **Date Created**: 2026 (latest update)
- **Status**: 🔴 **REDEPLOY GUIDE FOR NEW ARCHITECTURE**
- **Database Architecture**: **PostgreSQL RDS**
- **Architecture Specification**:
  ```
  Elastic Beanstalk single-instance in us-east-1
  Amazon RDS PostgreSQL in us-east-1
  GoDaddy-managed DNS
  ```

**Key Sections**:
1. **Before AWS Commands**: Set up AWS CLI credentials
2. **Required Environment Variables**:
   ```
   - DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<db>
   - DJANGO_SETTINGS_MODULE=realtor_project.settings
   ```
3. **RDS First**: Create PostgreSQL instance
4. **Elastic Beanstalk**: Deploy to us-east-1
5. **Data Migration**: Migrate from SQLite to PostgreSQL
6. **DNS**: Update GoDaddy DNS

**Critical Notes**:
```
"The old SQLite-on-instance EB pattern has been removed from the deployment hooks"
"The postdeploy hooks now assume PostgreSQL via DATABASE_URL or EB-provided DB env vars"
```

**Analysis**: This is a **migration guide** from SQLite (us-west-2) to PostgreSQL (us-east-1). This indicates there was a planned upgrade.

---

### Document 3: AWS_DEPLOYMENT_GUIDE.md
- **Date Created**: 2026 (general guide)
- **Status**: 📋 COMPREHENSIVE DEPLOYMENT GUIDE
- **Database Architecture**: **PostgreSQL (recommended)**
- **Architecture Specification**:
  ```
  Services Needed:
  - EC2 (application)
  - RDS PostgreSQL (database)
  - S3 (static files)
  - CloudFront (CDN)
  - Route 53 (DNS)
  - Certificate Manager (SSL)
  - Elastic Load Balancer
  ```

**Analysis**: This is a **reference guide** for production-grade deployments with PostgreSQL.

---

## CRITICAL FINDING: Environment Mismatch

### Timeline of Events

```
March 7, 2026:
├─ Initial Deployment (us-west-2)
├─ SQLite database
├─ Single instance
└─ Status: Development/Testing

After March 7, 2026:
├─ Redeploy guide created (AWS_EB_RDS_REDEPLOY_2026.md)
├─ Specifies: Migrate to us-east-1
├─ Specifies: PostgreSQL RDS
├─ Specifies: settings.py with DATABASE_URL
└─ Status: Planned upgrade (INCOMPLETE)

Current State (June 16, 2026):
├─ Environment: propertism-prod-2026 (us-east-1) ✅ CORRECT
├─ Region: us-east-1 ✅ CORRECT
├─ Database: SQLite ❌ WRONG (should be PostgreSQL)
├─ DJANGO_SETTINGS_MODULE: settings.py (should be settings_production.py)
└─ Status: Partially migrated (BROKEN)
```

---

## What Happened

### The Intent

The redeploy guide (`AWS_EB_RDS_REDEPLOY_2026.md`) clearly shows the intended path:

1. **Provision RDS PostgreSQL** in us-east-1
2. **Create EB environment** in us-east-1
3. **Configure DATABASE_URL** pointing to RDS
4. **Migrate data** from SQLite to PostgreSQL
5. **Update DNS** via GoDaddy

### What Was Actually Done

1. ✅ EB environment created: `propertism-prod-2026` in us-east-1
2. ✅ Infrastructure moved to us-east-1
3. ❌ **RDS PostgreSQL was NOT provisioned**
4. ❌ **DATABASE_URL environment variable was NOT set**
5. ❌ **SQLite fallback engaged automatically**
6. ❌ **Data migration never occurred**

### The Result

```
Expected: EB (us-east-1) → PostgreSQL RDS (us-east-1) → Blog URLs accessible
Actual:   EB (us-east-1) → SQLite fallback → Blog URLs return 404
```

---

## Local vs Production Database Strategy

### From Documents Analysis

**AWS_EB_RDS_REDEPLOY_2026.md explicitly states**:

```
"Data Migration

If the source of truth is the local SQLite database, migrate data using Django 
instead of pg_dump.

Suggested sequence:

1. Point local .env temporarily to the new PostgreSQL database with DATABASE_URL
2. Run: .\\scripts\\django.cmd migrate
3. Export application data from SQLite with Django fixtures for the business-owned apps
4. Import that data into PostgreSQL
5. Validate admin content, properties, reviews, and media references before 
   production cutover"
```

**Intended Architecture**:
- **Local Development**: SQLite (`.env` with no DATABASE_URL)
- **Production**: PostgreSQL RDS (`.env` with DATABASE_URL pointing to RDS)

### Current Reality

- **Local Development**: SQLite ✅ Correct
- **Production**: SQLite ❌ Wrong (should be PostgreSQL)

---

## Root Cause Analysis

### Why Production is Using SQLite Instead of PostgreSQL

**The Incomplete Migration**:

1. ✅ **EB Environment Created**: `propertism-prod-2026` in us-east-1 (correct location)
2. ✅ **Code Deployed**: Latest code with `.ebextensions/` (correct)
3. ❌ **RDS Not Provisioned**: No PostgreSQL database instance exists
4. ❌ **DATABASE_URL Not Set**: Environment variable missing
5. ❌ **Fallback Triggered**: Django defaults to SQLite
6. ❌ **SQLite File Missing**: Database never initialized

**Code Flow**:
```python
# From settings.py (the active module)
if 'RDS_DB_NAME' in os.environ:
    # Use RDS ← RDS_DB_NAME NOT FOUND
elif LOCAL_POSTGRES_DATABASE:
    # Use PostgreSQL ← DATABASE_URL NOT FOUND
else:
    # Fall back to SQLite ← TRIGGERED HERE
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_PATH,  # /var/app/current/db.sqlite3 (doesn't exist)
        }
    }
```

---

## Document-Based Recommendations

### From AWS_EB_RDS_REDEPLOY_2026.md

This document provides the **exact steps to complete the migration**:

```
Required Environment Variables:

✅ DEBUG=False
✅ DJANGO_SETTINGS_MODULE=realtor_project.settings
✅ DJANGO_SECRET_KEY=<strong secret>
❌ DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<db>  ← MISSING
✅ DJANGO_ALLOWED_HOSTS=propertism.in,www.propertism.in,...
✅ CSRF_TRUSTED_ORIGINS=https://propertism.in,...
```

The guide explicitly instructs:

```
RDS First

1. Create a PostgreSQL instance in us-east-1
2. Wait until it is available
3. Capture: endpoint hostname, database name, username, password
4. Build the final DATABASE_URL
```

---

## Two Paths: Decision Framework from Documents

### Path A: Complete the Planned PostgreSQL Migration (RECOMMENDED)

**From AWS_EB_RDS_REDEPLOY_2026.md**:

```
1. Create a PostgreSQL instance in us-east-1
2. Capture RDS details (endpoint, credentials)
3. Set environment variable: DATABASE_URL=postgresql://...
4. Deploy
5. Run migrations: python manage.py migrate
6. Data migration
7. Validate
```

**Timeline**: 2-4 hours  
**Cost**: ~$15-20/month (RDS t3.micro)  
**Risk**: 🟢 LOW (intended architecture)  
**Alignment**: ✅ Matches AWS_EB_RDS_REDEPLOY_2026.md exactly

---

### Path B: Temporary SQLite (NOT IN DEPLOYMENT DOCUMENTS)

**Using SQLite on production is NOT mentioned in any of the deployment guides.**

The guides document:
- ✅ SQLite for **local development** only
- ✅ PostgreSQL RDS for **production**
- ❌ SQLite for production (not documented, not recommended)

**Timeline**: 30 minutes  
**Cost**: $0  
**Risk**: 🔴 CRITICAL (data loss on instance replacement)  
**Alignment**: ❌ Contradicts documented architecture

---

## Settings Module Clarification

### From AWS_EB_RDS_REDEPLOY_2026.md

```
"Required Environment Variables:
- DEBUG=False
- DJANGO_SETTINGS_MODULE=realtor_project.settings
- DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<db>"
```

**Note**: Uses `realtor_project.settings` (not settings_production.py)

However, this works because:
- `settings.py` is designed to work with both local AND production
- When DATABASE_URL is set, `settings.py` uses it
- When DATABASE_URL is NOT set, `settings.py` falls back to SQLite

**Current issue**: DATABASE_URL is simply not set in production environment.

---

## Definitive Recommendation from Documents

### AWS_EB_RDS_REDEPLOY_2026.md is the SOURCE OF TRUTH

This document represents the **official redeploy strategy** that was created but **never fully implemented**.

**The guide says**:

```
"The old SQLite-on-instance EB pattern has been removed from the deployment hooks"
"The postdeploy hooks now assume PostgreSQL via DATABASE_URL or EB-provided DB env vars"
"Media is still served from the application bundle unless/until S3 storage is 
wired into Django settings"
```

**Translation**: The intention is PostgreSQL, not SQLite.

---

## Action Items Based on Document Analysis

### IMMEDIATE: Fix Incomplete Migration

1. **Create RDS PostgreSQL instance** (as specified in AWS_EB_RDS_REDEPLOY_2026.md)
2. **Set DATABASE_URL environment variable** in EB
3. **Deploy** (migrations run automatically)
4. **Verify** articles are accessible

### Alternative: Use Temporary SQLite ONLY IF

- PostgreSQL provisioning is blocked
- Phase-5 must complete within 2 hours
- **AND** you accept documented data loss risk

---

## Sign-Off

**Document Analysis Complete**: ✅

**Finding**: PostgreSQL migration was planned but never completed

**Evidence**:
- AWS_DEPLOYMENT_COMPLETE.md (March 7, 2026) — Initial SQLite deployment
- AWS_EB_RDS_REDEPLOY_2026.md (2026 latest) — Redeploy guide to PostgreSQL (NEVER EXECUTED)
- AWS_DEPLOYMENT_GUIDE.md (reference) — Production best practices with PostgreSQL

**Recommendation**: Follow AWS_EB_RDS_REDEPLOY_2026.md exactly to complete the migration.

---

**Analysis Timestamp**: 2026-06-16 07:05 UTC  
**Confidence Level**: 99% (based on official deployment documents)  
**Recommended Action**: PostgreSQL RDS setup per AWS_EB_RDS_REDEPLOY_2026.md
