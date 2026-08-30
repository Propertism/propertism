# SCCB-PROP-DEFINITIVE-ACTION-PLAN-1606

**Date**: 2026-06-16  
**Authority**: Based on official deployment documents (AWS_EB_RDS_REDEPLOY_2026.md)  
**Status**: READY FOR EXECUTION  

---

## The Situation

**Production is in a partially-migrated state:**

```
Original (March 7, 2026):
  Location: us-west-2
  Database: SQLite
  Status: Initial deployment

Intended (AWS_EB_RDS_REDEPLOY_2026.md):
  Location: us-east-1
  Database: PostgreSQL RDS
  Status: Planned migration

Actual (June 16, 2026):
  Location: us-east-1 ✅
  Database: SQLite ❌ (should be PostgreSQL)
  Status: Migration incomplete
```

---

## Root Cause

The migration guide (`AWS_EB_RDS_REDEPLOY_2026.md`) was created but **Step 1 was never executed**:

```
AWS_EB_RDS_REDEPLOY_2026.md - RDS First Section:

1. Create a PostgreSQL instance in us-east-1     ← NEVER DONE
2. Wait until it is available
3. Capture: endpoint hostname, database name, username, password
4. Build the final DATABASE_URL
```

---

## Definitive Recommendation

### PRIMARY RECOMMENDATION: Complete the PostgreSQL Migration ⭐⭐⭐

**Source**: AWS_EB_RDS_REDEPLOY_2026.md (official redeploy strategy)

**Why**:
1. ✅ This is the documented, intended architecture
2. ✅ Code is already prepared for this path
3. ✅ Environment is already in correct location (us-east-1)
4. ✅ Only missing: RDS instance + one environment variable
5. ✅ No data loss risk
6. ✅ Production-grade reliability

**Timeline**: 2-4 hours

**Steps** (from AWS_EB_RDS_REDEPLOY_2026.md):

1. **Create RDS PostgreSQL instance in us-east-1**
   - Instance class: db.t3.micro (free tier eligible)
   - Database name: propertism_db
   - Master username: propertism_user
   - Master password: (secure)
   - Publicly accessible: Yes (for EB access)
   - Wait for "Available" status

2. **Capture RDS Connection Details**
   - Endpoint hostname: (e.g., propertism-db.xxxxx.us-east-1.rds.amazonaws.com)
   - Port: 5432
   - Database: propertism_db
   - Username: propertism_user
   - Password: (what you set)

3. **Build DATABASE_URL**
   ```
   postgresql://propertism_user:password@propertism-db.xxxxx.us-east-1.rds.amazonaws.com:5432/propertism_db
   ```

4. **Set Environment Variable in EB**
   ```bash
   eb setenv DATABASE_URL="postgresql://propertism_user:password@propertism-db.xxxxx.us-east-1.rds.amazonaws.com:5432/propertism_db"
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```
   (Automatically runs migrations)

6. **Seed Data**
   ```bash
   eb ssh
   source /var/app/venv/*/bin/activate
   cd /var/app/current
   python manage.py seed_knowledge_hub_phase_a --publish
   ```

7. **Verify**
   ```bash
   curl -I https://www.propertism.in/en/blog/nri-property-management-basics/
   ```
   Expected: HTTP 200

---

### ALTERNATIVE: Temporary SQLite (NOT RECOMMENDED)

Only if PostgreSQL is blocked AND Phase-5 must complete in 2 hours.

**Risks**:
- ❌ Data loss on instance replacement
- ❌ No automatic backups
- ❌ Not production-grade

**Must migrate to PostgreSQL within 48 hours**.

---

## Decision Framework

| Factor | PostgreSQL Path | SQLite Path |
|--------|---|---|
| Matches Documented Architecture | ✅ YES (AWS_EB_RDS_REDEPLOY_2026.md) | ❌ NO (not in any guide) |
| Production-Ready | ✅ YES | ❌ NO |
| Data Loss Risk | 🟢 None | 🔴 High (auto-scale) |
| Implementation Time | 2-4 hours | 30 minutes |
| Monthly Cost | ~$15-20 | $0 |
| Operational Support | ✅ AWS RDS managed | ❌ Manual backup needed |
| Alignment with Stated Plans | ✅ 100% | ❌ 0% |

---

## Decision: Which Path?

### If you answer YES to ANY of these:
- "We plan to use this as production long-term"
- "Data loss is not acceptable"
- "We want AWS-managed backups"
- "We're prepared to spend 2-4 hours now"

**👉 Choose: PostgreSQL (PRIMARY RECOMMENDATION)**

---

### If you answer YES to ALL of these:
- "Phase-5 MUST complete within 2 hours"
- "RDS provisioning is currently blocked"
- "We accept data loss if instance auto-scales"
- "We commit to RDS migration within 48 hours"

**👉 Choose: Temporary SQLite (with explicit risk acknowledgment)**

---

## Next Steps

### Step 1: Confirm Your Choice

Choose ONE and confirm:

```
[ ] OPTION A: PostgreSQL (RECOMMENDED)
    - Complete migration per AWS_EB_RDS_REDEPLOY_2026.md
    - Production-grade setup
    - 2-4 hours

[ ] OPTION B: Temporary SQLite (ALTERNATIVE)
    - Risk acknowledgment: I accept data loss if instance scales
    - Commit to PostgreSQL migration within 48 hours
    - 30 minutes
```

### Step 2: Execute Chosen Path

If **OPTION A (PostgreSQL)**:
→ Use AWS_EB_RDS_REDEPLOY_2026.md as step-by-step guide

If **OPTION B (SQLite)**:
→ Use SCCB-PROP-KNOWLEDGE-HUB-SQLITE-ACTIVATION-1606.md

### Step 3: Validation

All blog URLs return HTTP 200:
```bash
bash test-all-blog-urls.sh
```

---

## Files Created for This Decision

| Document | Purpose |
|----------|---------|
| `SCCB-PROP-POSTGRES-PRODUCTION-RECONCILIATION-1606.md` | Settings module mismatch analysis |
| `SCCB-PROP-DEPLOYMENT-HISTORY-ANALYSIS-1606.md` | Deployment timeline and history |
| `SCCB-PROP-DEFINITIVE-ACTION-PLAN-1606.md` | This document |
| `AWS_EB_RDS_REDEPLOY_2026.md` | Official migration guide (in documents/) |

---

## Reference Documents

**If choosing PostgreSQL**:
- Primary: `documents/AWS_EB_RDS_REDEPLOY_2026.md`
- Detailed setup: `documents/AWS_DEPLOYMENT_GUIDE.md`

**If choosing SQLite**:
- Primary: `SCCB-PROP-KNOWLEDGE-HUB-SQLITE-ACTIVATION-1606.md`
- URL testing: `test-all-blog-urls.sh`

---

## Critical Reminder

⚠️ **SQLite on EB will lose all data if**:
- Instance is replaced by auto-scaling
- Environment is terminated and recreated
- Deployment triggers new instance

This is not a theoretical risk—it's a guaranteed outcome of EB architecture.

---

## Sign-Off

**Investigation**: ✅ Complete  
**Root Cause**: ✅ Identified (incomplete PostgreSQL migration)  
**Recommendation**: ✅ Definitive (complete the migration)  
**Authority**: ✅ Official deployment documents (AWS_EB_RDS_REDEPLOY_2026.md)  

---

**Status**: ⏳ **AWAITING YOUR DECISION**

**Choose your path and I'll provide detailed step-by-step instructions.**

---

## Quick Decision Matrix

```
Are you committed to production PostgreSQL long-term?
  YES → PostgreSQL (PRIMARY)
  NO  → SQLite (ALTERNATIVE, temporary only)

Do you have 2-4 hours for proper setup?
  YES → PostgreSQL
  NO  → SQLite (with risk acknowledgment)

Is data loss acceptable?
  YES → SQLite
  NO  → PostgreSQL

Are you following AWS_EB_RDS_REDEPLOY_2026.md?
  YES → PostgreSQL
  NO  → SQLite (deviation from planned architecture)
```

**Most boxes = PostgreSQL?** Choose PostgreSQL.  
**Most boxes = SQLite?** Choose SQLite (but understand risks).

---

**Document**: SCCB-PROP-DEFINITIVE-ACTION-PLAN-1606  
**Created**: 2026-06-16 07:10 UTC  
**Status**: Ready for operator decision
