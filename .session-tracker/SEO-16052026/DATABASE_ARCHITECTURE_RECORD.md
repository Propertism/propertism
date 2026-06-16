# DATABASE_ARCHITECTURE_RECORD
## SCCB-PROP-PRODUCTION-STABILIZATION-AND-SEO-ROADMAP-CONSOLIDATION-1606

**Date**: 2026-06-17  
**Status**: DATABASE ARCHITECTURE DOCUMENTED

---

## Database Architecture Overview

### Dual-Environment Design

```
┌─────────────────────────────────────────────────────┐
│ DATABASE ARCHITECTURE - DUAL ENVIRONMENT            │
├─────────────────────────────────────────────────────┤
│                                                      │
│ LOCAL DEVELOPMENT              PRODUCTION           │
│ ───────────────────            ──────────────────   │
│ SQLite (db.sqlite3)            PostgreSQL RDS       │
│ File-based                     AWS Managed          │
│ No configuration               Highly available     │
│ Single process                 Multi-process        │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Production: PostgreSQL RDS Configuration

### RDS Instance Details
```
Instance Identifier: propertism-db-2026
Engine: PostgreSQL
Engine Version: 13+ (Latest supported)
Instance Class: db.t3.micro (cost-optimized)
Storage: 20 GB General Purpose (gp2)
Storage Auto-Scaling: Enabled (up to 100 GB)
Multi-AZ: No (single AZ, us-east-1a)
Public Accessibility: No (private VPC)
```

### RDS Security Configuration
```
Security Group: propertism-rds-sg
Inbound Rules:
  Port 5432: From EB security group only
  
Network: VPC (default)
Subnet: Isolated (no direct internet access)
NAT: EB instance routes through NAT gateway

Encryption:
  At-rest: KMS (AWS managed key)
  In-transit: SSL/TLS required
  Storage encrypted: Yes
```

### RDS Backup Configuration
```
Backup Window: 03:00–04:00 UTC
Retention Period: 7 days
Automatic Backups: Enabled
Manual Snapshots: Available on demand
Point-in-Time Recovery: Enabled (last 7 days)
```

---

## RDS Connection Details

### Connection String
```
Type: PostgreSQL URL (RFC 3986)

Format:
postgresql://[username]:[password]@[host]:[port]/[database]

Example (sanitized):
postgresql://propertismadmin:***@propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com:5432/propertismdb

Components:
  Protocol: postgresql (or postgres)
  Username: propertismadmin
  Password: [AWS managed, in Secrets Manager]
  Host: propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com
  Port: 5432 (standard PostgreSQL)
  Database: propertismdb
```

### Environment Variable Strategy

**In Elastic Beanstalk**:
```bash
# Option 1: Individual RDS variables (set by EB auto-configuration)
RDS_DB_NAME: propertismdb
RDS_USERNAME: propertismadmin
RDS_PASSWORD: [auto-managed]
RDS_HOSTNAME: propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com
RDS_PORT: 5432

# Option 2: DATABASE_URL (explicit connection string)
DATABASE_URL: postgresql://propertismadmin:***@propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com:5432/propertismdb

# Option 3: SSL mode (enforced)
POSTGRES_SSLMODE: require
DATABASE_SSLMODE: require
```

**Priority in Django settings.py**:
```python
# 1. Check RDS_DB_NAME (EB auto-configuration) → USE IF PRESENT
# 2. Check DATABASE_URL → Parse and use if present
# 3. Check POSTGRES_* variables → Build config if present
# 4. Fallback → SQLite (local development only)
```

---

## Local Development: SQLite Configuration

### SQLite File Location
```
Path: {BASE_DIR}/db.sqlite3
Size: ~5-10 MB (typically)
Permissions: 0o666 (read/write)
Storage: Local filesystem (development machine)
```

### SQLite Connection
```
Django Configuration:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

Characteristics:
- Single file database
- No server process required
- No authentication needed
- Suitable for 1-2 concurrent users
- Perfect for local development and testing
```

---

## Django Settings Module Configuration

### CRITICAL DECISION: Active Settings Module

**✅ ACTIVE (Production-Ready)**:
```
File: realtor_project/settings.py
Status: COMPLETE
Apps: 28 (all required)
Database Logic: Intelligent fallback (RDS → PostgreSQL → SQLite)
Recommendation: USE THIS IN PRODUCTION
```

**❌ INACTIVE (Incomplete)**:
```
File: realtor_project/settings_production.py
Status: INCOMPLETE
Apps: 16 (missing allauth, chat, nri_assist, sitemaps)
Database Logic: Hardcoded, no fallback
Issues: Causes 502 errors
Recommendation: DO NOT USE (deprecated)
```

### settings.py: Database Selection Logic

**Code Location**: `realtor_project/settings.py` (Lines 120–170)

```python
# Database selection priority (AUTO-DETECTED)
LOCAL_POSTGRES_DATABASE = _get_local_postgres_config()

if 'RDS_DB_NAME' in os.environ:
    # ✅ TIER 1: Production RDS (AWS Elastic Beanstalk)
    database_config = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
    sslmode = _get_env_value('POSTGRES_SSLMODE', 'DATABASE_SSLMODE')
    if sslmode:
        database_config['OPTIONS'] = {'sslmode': sslmode}
    DATABASES = {'default': database_config}
    
elif LOCAL_POSTGRES_DATABASE:
    # ✅ TIER 2: Local PostgreSQL (via DATABASE_URL or POSTGRES_*)
    DATABASES = {
        'default': LOCAL_POSTGRES_DATABASE,
    }
    
else:
    # ✅ TIER 3: SQLite fallback (local development)
    DB_PATH = os.environ.get('DB_PATH', str(BASE_DIR / 'db.sqlite3'))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_PATH,
        }
    }
```

### Helper Functions in settings.py

**Function: `_database_config_from_url(database_url)`**
```python
# Parses DATABASE_URL into Django DATABASES dict
# Supports: postgresql://, postgres://, pgsql://
# Extracts: username, password, host, port, database
# Returns: Django database configuration dict
```

**Function: `_get_local_postgres_config()`**
```python
# Checks for DATABASE_URL first (priority)
# Falls back to POSTGRES_* env vars
# Returns: Django PostgreSQL config or None
```

**Function: `_get_env_value(*names)`**
```python
# Gets first available env var from list
# Case-fallback: POSTGRES_SSLMODE → DATABASE_SSLMODE
# Used for: SSL mode, timeout configs
```

---

## INSTALLED_APPS Configuration

### Production-Ready (settings.py)

```python
INSTALLED_APPS = [
    'modeltranslation',  # MUST be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',  # ✅ SEO SITEMAPS
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # django-allauth (Google OAuth)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Project applications
    'properties.apps.PropertiesConfig',
    'users.apps.UsersConfig',
    'search.apps.SearchConfig',
    'uilayers.apps.UilayersConfig',
    'content.apps.ContentConfig',
    'chat.apps.ChatConfig',        # ✅ CHAT
    'nri_assist.apps.NriAssistConfig',  # ✅ NRI ASSIST
]
```

**Total**: 28 apps (all dependencies satisfied)

### Incomplete (settings_production.py) — DO NOT USE

```python
INSTALLED_APPS = [
    # Missing: modeltranslation
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # ❌ Missing: django.contrib.sitemaps (breaks SEO)
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'properties',
    'users',
    'search',
    'uilayers',
    'content',
    # ❌ Missing: allauth modules (breaks OAuth)
    # ❌ Missing: chat app
    # ❌ Missing: nri_assist app
]
```

**Total**: 16 apps (incomplete, causes crashes)

---

## Database Schema & Migrations

### Django Migrations

**Location**: `{app}/migrations/` directories

```
Each app maintains its own migrations:
├─ properties/migrations/
├─ users/migrations/
├─ content/migrations/
├─ chat/migrations/
├─ nri_assist/migrations/
├─ search/migrations/
└─ uilayers/migrations/
```

**Applied via**:
```bash
python manage.py migrate --noinput
```

**Executed in EB**:
```yaml
container_commands:
  02_migrate:
    command: "python manage.py migrate --noinput"
    leader_only: true
```

### Key Tables (Content App)

```
content_blogpost
├─ id (PK)
├─ title
├─ slug (UNIQUE)
├─ excerpt
├─ content
├─ featured_image
├─ author
├─ published_date
├─ updated_date
├─ is_published ← CRITICAL FIELD
└─ category

content_companyinfo
├─ id (PK)
├─ company_name
├─ tagline
├─ hero_title
└─ [100+ fields for site configuration]

content_landinglead
├─ id (PK)
├─ phone
├─ email
├─ property_city
├─ intent_type
├─ lead_stage
├─ lead_score
└─ qualification_data (JSON)
```

---

## SSL/TLS Configuration

### PostgreSQL SSL Mode

**Requirement**: `sslmode = require`

```
POSTGRES_SSLMODE: require
DATABASE_SSLMODE: require

Meaning:
- Connection MUST be encrypted
- Invalid certificate → Connection rejected
- Protects against man-in-the-middle attacks
- Required by AWS RDS best practices
```

### Certificate Verification

```
AWS RDS uses: AWS-managed certificates
Validation: Automatic (psycopg2 driver handles)
Root CA: Bundled with PostgreSQL drivers
No manual certificate download required
```

---

## Connection Pool Configuration

### Current Settings

```python
CONN_MAX_AGE: 600 seconds (10 minutes)
# Django closes idle connections after 10 minutes
# RDS automatically recycles at 15 minutes
# Prevents stale connection errors
```

### For Production Scaling

```python
# When upgrading to production scale:
CONN_MAX_AGE: 300 seconds (5 minutes) # More frequent refresh
# or use persistent pool:
import psycopg2.pool
DATABASES['default']['CONN'] = psycopg2.pool.SimpleConnectionPool(1, 20, ...)
```

---

## Data Integrity & Constraints

### Foreign Keys

```python
# All ForeignKey fields enforce referential integrity:
- CASCADE: Delete related records when parent deleted
- PROTECT: Prevent deletion if related records exist
- SET_NULL: Set field to NULL when parent deleted

Current strategy: CASCADE (keeps data consistent)
```

### Unique Constraints

```python
# BlogPost.slug: UNIQUE (no duplicate article URLs)
# Newsletter.email: UNIQUE (no duplicate subscriptions)
# User.email: UNIQUE (one email per account)
```

### Data Validation

```python
# Enforced at multiple levels:
1. Django ORM (model.full_clean())
2. Database constraints (CHECK, UNIQUE, NOT NULL)
3. Application logic (views, serializers)
```

---

## Backup & Recovery Strategy

### Automated Backups (RDS)

```
Frequency: Daily
Retention: 7 days
Window: 03:00–04:00 UTC (chosen for low-traffic hours)
Backup Type: Full snapshot (not incremental)
Storage: AWS S3 (automatically managed)
```

### Manual Snapshots

```bash
# Take snapshot via AWS Console:
1. Go to RDS → Databases → propertism-db-2026
2. Click "Actions" → "Create snapshot"
3. Name: propertism-db-backup-2026-06-17
4. Stored indefinitely until manually deleted
```

### Point-in-Time Recovery (PITR)

```
Enabled: Yes
Recovery Window: 7 days (last 7 days recoverable)
Granularity: 1 minute intervals
Use case: Recover from accidental delete/update
```

### Restore Procedure (if needed)

```bash
# Via AWS Console:
1. Go to RDS → Automated backups
2. Select backup → "Restore to point in time"
3. Choose recovery point
4. Create new RDS instance
5. Update Django DATABASE_URL to new instance
6. Test connectivity
7. Verify data integrity
```

---

## Monitoring & Performance

### Slow Query Logging

```sql
-- PostgreSQL slow query log
log_min_duration_statement = 1000  -- Log queries > 1 second
log_lock_waits = on                -- Log lock waits
log_connections = on               -- Log all connections
log_disconnections = on             -- Log disconnections
```

### Key Metrics

```
Connections: Active / Max (5/100 typical)
CPU: %age used (should stay <50%)
Storage: GB used / Total (5/20 typical)
IOPS: Read/write per second (auto-scaled)
Latency: Network + Query time (target <50ms)
```

### CloudWatch Metrics

```
AWS CloudWatch monitors:
- DBConnections
- CPUUtilization
- DatabaseConnections
- ReadLatency
- WriteLatency
- StorageSpace
```

---

## Migration Path: SQLite → PostgreSQL

### What Happened (Recent)

```
Timeline:
1. Initial: SQLite on EC2 instance (db.sqlite3)
   - Articles seeded to SQLite

2. Migration Decision: AWS_EB_RDS_REDEPLOY_2026.md
   - Set up PostgreSQL RDS
   - EB environment restarted with RDS variables
   - SQLite database lost (instance terminated)

3. Current: PostgreSQL RDS active (empty or with incomplete data)
   - Seed command may have failed or not run
   - Articles not visible on production URLs
```

### Data Loss Prevention (Going Forward)

```
Strategy:
1. Always take RDS snapshot before major changes
2. Keep PITR enabled (7-day window minimum)
3. Test migrations in staging first
4. Back up data to S3 before instance termination
5. Use EB environment cloning for safe testing
```

---

## Security Best Practices

### Database Credentials

```
Storage: AWS Secrets Manager or EB environment vars
Rotation: Quarterly (manual update recommended)
Backup: Stored encrypted in AWS
Access: Only EB instance role can access
```

### Network Isolation

```
Public Access: DISABLED
VPC: Private subnet
Security Group: Allows only EB instance
Route: Through NAT gateway (outbound only)
```

### Query Audit

```
Who made changes: PostgreSQL pg_stat_user_tables
When: published_date and updated_date fields
What: Django admin logs (if enabled)
How: Application code review
```

---

## Decision: Why PostgreSQL Over SQLite

### Production Choice: PostgreSQL RDS

```
✅ Advantages:
- Multi-user concurrent access
- ACID compliance (data integrity)
- Advanced query optimization
- Automatic failover (with Multi-AZ)
- Built-in backups
- SSL encryption
- Connection pooling
- Horizontal scaling
- AWS managed (no ops overhead)

❌ SQLite Limitations:
- Single-writer lock (concurrent requests slow)
- File I/O overhead
- No built-in backups
- Instance storage lost on termination
- No encryption
```

### Development: SQLite Fallback

```
✅ Advantages:
- Zero configuration
- No server process
- Perfect for local development
- Easy testing (create/destroy DB quickly)
- Portable (one file)
- Same Django ORM (code reuse)

❌ RDS in Dev Overhead:
- Expensive ($10-20/month minimum)
- Adds network latency
- Harder to reset for testing
- Not needed for 1-2 developers
```

---

## Current Architecture Decision: LOCKED

### ✅ CONFIRMED PRODUCTION DATABASE

```
Database: PostgreSQL RDS
Instance: propertism-db-2026
Region: us-east-1
Status: ✅ LOCKED (no changes without explicit approval)
```

### ✅ CONFIRMED SETTINGS MODULE

```
Module: realtor_project/settings.py
Status: ✅ LOCKED (production-ready, complete)
Alternative: settings_production.py ❌ DEPRECATED (incomplete)
```

### ✅ CONFIRMED MIGRATION APPROACH

```
Strategy: Django ORM migrations (managed via EB container commands)
Status: ✅ LOCKED (reliable, tested)
Database Updates: Via "02_migrate" container command
```

---

## Future Considerations

### Scaling to Multi-AZ

```
When: Traffic exceeds 1000 req/sec OR 500 concurrent users
Cost: +$50-100/month
Benefit: Automatic failover, 99.95% uptime
Implementation: Click "Modify" in RDS console
```

### Read Replicas

```
When: Read-heavy workload (lots of reporting)
Cost: +$50-100/month per replica
Benefit: Distribute read queries across replicas
Implementation: RDS Read Replica creation
```

### Auto-Scaling Storage

```
Current: Manual (up to 100 GB configured)
Future: Enable automatic scaling
Trigger: Storage > 80% utilization
Max: 1000 GB (configurable)
```

---

**Status**: ✅ DATABASE ARCHITECTURE DOCUMENTED  
**Last Updated**: 2026-06-17  
**Database Version**: PostgreSQL 13+  
**Settings Module**: realtor_project/settings.py (v1.0)
