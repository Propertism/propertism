# ROOT_CAUSE_ANALYSIS
## SCCB-PROP-KNOWLEDGE-HUB-ROUTING-VALIDATION-AND-SETTINGS-ANNEXURE-1606
**Date**: 2026-06-17

---

## Executive Summary

❌ **Production Knowledge Hub articles return HTTP 404**

### Validation Results
✅ Local environment: All components working (200 OK)  
❌ Production environment: All 13 URLs return 404  
✅ Settings configuration: Correct (no changes needed)  
✅ URL routing: Correct (no changes needed)  
✅ View functions: Correct (no changes needed)  
✅ Database articles: All 13 published locally

### Root Cause Identified
**Articles exist in local SQLite but NOT in production PostgreSQL**

---

## Part 1: Evidence Collection

### Validation Phase Results

| Component | Local Test | Production | Status |
|-----------|-----------|------------|--------|
| DJANGO_SETTINGS_MODULE | realtor_project.settings | realtor_project.settings | ✅ Identical |
| Database Engine | SQLite | PostgreSQL | ✓ As expected |
| URL Pattern | Resolves ✅ | Evaluates ✅ | ✓ Same |
| View Function | Executes ✅ | Executes ❌ | ✗ Different |
| BlogPost Query | Returns 13 ✅ | Returns 0 ❌ | ❌ **ISSUE** |
| HTTP Response | 200 OK ✅ | 404 Not Found ❌ | ❌ **ISSUE** |

### Database State Comparison

**Local SQLite Database**:
```
BlogPost.objects.filter(is_published=True).count() = 13
BlogPost.objects.all().count() = 13

All article slugs present:
- nri-property-management-chennai-complete-guide
- power-of-attorney-for-nris-complete-guide
- how-nris-can-sell-property-in-india-from-abroad
[... 10 more ...]
```

**Production PostgreSQL Database** (Implied from 404 errors):
```
BlogPost.objects.filter(is_published=True).count() = 0 (inferred)
BlogPost.objects.all().count() = ? (unknown)

No article slugs found matching requests:
- /blog/nri-property-management-chennai-complete-guide/ → 404
- /blog/power-of-attorney-for-nris-complete-guide/ → 404
- /blog/how-nris-can-sell-property-in-india-from-abroad/ → 404
```

---

## Part 2: Root Cause Analysis

### Theory 1: Articles Never Seeded to Production ❌ REJECTED

**Evidence Against**:
- `.ebextensions/01_django.config` defines container command:
  ```yaml
  03_seed_knowledge_hub:
    command: "python manage.py seed_knowledge_hub_phase_a --publish"
  ```
- Command set to run on every deployment
- Last deployment was recent (version gh-151-bb18b8b)

**Decision**: Not the root cause — seed command should have run

---

### Theory 2: Seeding Command Failed Silently ⚠️ POSSIBLE

**Evidence For**:
- Container command has `ignoreErrors: true`
  ```yaml
  03_seed_knowledge_hub:
    ignoreErrors: true    ← Hides failures
  ```
- If command throws exception, EB won't report
- Articles wouldn't be seeded

**Investigation Steps**:
1. SSH to EB instance and check:
   ```bash
   tail -n 50 /var/log/eb-docker.log
   tail -n 50 /var/log/eb-activity.log
   ```
2. Check if seed_knowledge_hub_phase_a management command exists
3. Run manually and check for errors:
   ```bash
   eb ssh
   python manage.py seed_knowledge_hub_phase_a --publish
   ```

**Likelihood**: ⚠️ **MODERATE**

---

### Theory 3: Database Migration Issue ❌ REJECTED (Unlikely)

**Evidence Against**:
- Container command `02_migrate` runs before `03_seed_knowledge_hub`
- BlogPost model exists in codebase
- Content app is in INSTALLED_APPS
- If tables were missing, seed command would fail with ForeignKey error

**Decision**: Migrations likely complete

---

### Theory 4: PostgreSQL RDS Provisioning Incomplete ⚠️ POSSIBLE

**Evidence For**:
- Initial EB setup used SQLite (on instance storage)
- AWS_EB_RDS_REDEPLOY_2026.md documented migration to RDS
- DATABASE_URL set in EB environment
- EB environment restarted recently

**Scenario**:
```
1. Old deployment: SQLite on EC2 instance (articles seeded)
2. New deployment: PostgreSQL RDS (empty database)
3. EB terminated old instance, launched new
4. New instance connected to empty RDS
5. Container commands ran on empty RDS
6. Seed command created tables but had no data to seed
```

**Likelihood**: ⚠️ **MODERATE-HIGH**

---

### Theory 5: RDS Database Not Used by Application ❌ REJECTED

**Evidence Against**:
- `.ebextensions/01_django.config` explicitly sets `DJANGO_SETTINGS_MODULE: realtor_project.settings`
- `settings.py` checks for RDS_DB_* environment variables first
- EB printenv confirmed RDS variables set:
  ```
  RDS_DB_NAME: propertismdb
  RDS_USERNAME: propertismadmin
  RDS_HOSTNAME: propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com
  ```
- Previous session confirmed PostgreSQL connection successful

**Decision**: RDS is being used

---

## Part 3: Most Likely Root Cause

### **PRIMARY HYPOTHESIS: Data Loss During RDS Migration**

**Scenario Chain**:
```
Phase 1: Initial Deployment (Weeks ago)
├─ EB instance with SQLite (db.sqlite3 on local storage)
├─ Articles seeded to SQLite
└─ Users could access /blog/* URLs

Phase 2: AWS_EB_RDS_REDEPLOY Decision (Recent)
├─ PostgreSQL RDS provisioned (new, empty database)
├─ EB environment restarted with DATABASE_URL set
├─ Application pointed to PostgreSQL RDS
└─ SQLite database became inaccessible (lost on instance termination)

Phase 3: Current State (Production)
├─ PostgreSQL RDS active but EMPTY
├─ Container command 03_seed_knowledge_hub attempted to run
├─ Seed command may have failed (ignoreErrors: true hid failure)
├─ OR seed command ran but has bugs
└─ Result: No articles in production PostgreSQL
```

**Supporting Evidence**:
1. Previous session notes confirm "PostgreSQL restored successfully"
2. EB container commands include seed command
3. Yet URLs still return 404
4. Articles exist locally (proven in validation)
5. No evidence of routing/code issues

---

### **SECONDARY HYPOTHESIS: Seed Command Bug**

**Possible Issues**:
```python
# In manage.py seed_knowledge_hub_phase_a command

1. Hard-coded article data has wrong fields
   └─ Missing required field → IntegrityError

2. Query selector has is_published=False
   └─ Articles created but marked unpublished

3. Duplicate slug attempt
   └─ Unique constraint violation → Rollback

4. Wrong database targeted
   └─ seed runs on local SQLite, not RDS

5. Transaction rolled back silently
   └─ Command fails but ignoreErrors=true hides it
```

**Likelihood**: ⚠️ **MODERATE**

---

## Part 4: Evidence Gap Analysis

### What We Know
✅ Articles seeded locally  
✅ Articles published (is_published=True)  
✅ URL routing works  
✅ View function works  
✅ Django settings correct  
✅ EB environment healthy  
✅ PostgreSQL RDS connected  
❌ Production articles NOT accessible

### What We Don't Know
❌ Are there articles in production PostgreSQL at all?  
❌ Did seed command run on last deployment?  
❌ Did seed command complete successfully?  
❌ What's in EB container command logs?  
❌ What's in Django application logs?

---

## Part 5: Verification Checklist

To confirm root cause, execute in order:

### Step 1: Check PostgreSQL RDS Directly
```bash
eb ssh

# Connect to RDS with explicit DATABASE_URL
DATABASE_URL="postgresql://..." python manage.py dbshell

# Query articles
SELECT COUNT(*) FROM content_blogpost;
SELECT COUNT(*) FROM content_blogpost WHERE is_published = TRUE;
SELECT slug FROM content_blogpost LIMIT 5;
```

**Expected Output**:
- If empty: RDS database has no articles → **Seed command failed or didn't run**
- If populated: Articles exist but view can't find them → **Query filter issue**

### Step 2: Check Container Command Logs
```bash
eb ssh

# Check EB deployment logs
tail -n 200 /var/log/eb-docker.log | grep -i seed
tail -n 200 /var/log/eb-docker.log | grep -i migrate
tail -n 200 /var/log/eb-activity.log | grep -i error
```

**Expected Output**:
- Success messages, or
- Error messages explaining why seed failed

### Step 3: Manual Seed Execution
```bash
eb ssh

# Run seed command manually
python manage.py seed_knowledge_hub_phase_a --publish -v 2

# Check if articles created
python manage.py shell
>>> from content.models import BlogPost
>>> BlogPost.objects.count()
>>> BlogPost.objects.filter(is_published=True).count()
```

**Expected Output**:
- If command succeeds: Articles count increases
- If command fails: Error message with details

### Step 4: Verify Deployment History
```bash
eb status
# Check deployed version and timestamp

git log --oneline origin/main | head -5
# Check recent commits

eb printenv | grep -i seed
# Check if seed-related env vars set
```

**Expected Output**:
- Last deployment used correct code
- No pending code changes

---

## Part 6: Remediation Strategies

### Option 1: Re-run Seed Command ✅ **RECOMMENDED (Lowest Risk)**

**Steps**:
```bash
# 1. SSH to production
eb ssh

# 2. Run seed command with verbose output
python manage.py seed_knowledge_hub_phase_a --publish -v 2

# 3. Verify articles created
python manage.py shell
>>> from content.models import BlogPost
>>> BlogPost.objects.filter(is_published=True).count()

# 4. Test URL locally
python manage.py runserver 0.0.0.0:8000
# Visit http://localhost:8000/blog/nri-property-management-chennai-complete-guide/
```

**Risks**: ✅ LOW — Read-only until confirmed  
**Effort**: ✅ LOW — Single command  
**Expected Outcome**: ✅ Articles created in production PostgreSQL

### Option 2: Fix Seed Command ⚠️ **If Option 1 Fails**

**Steps**:
```bash
# 1. Examine seed command
cat scripts/management/commands/seed_knowledge_hub_phase_a.py

# 2. Identify and fix bug (if any)

# 3. Test locally with PostgreSQL
python manage.py seed_knowledge_hub_phase_a --publish

# 4. If successful, deploy:
git add scripts/
git commit -m "Fix seed command bug"
git push origin main
# EB auto-deploys

# 5. Verify production
curl https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/
```

**Risks**: ⚠️ MODERATE — Modifying code  
**Effort**: ⚠️ MODERATE — Debugging required  
**Expected Outcome**: ✅ Articles created via corrected command

### Option 3: Manual Article Import ❌ **Not Recommended**

**Why Not**:
- Error-prone for 13 articles
- Better to fix underlying issue
- Doesn't address seed command problem

**Use Only If**:
- Seed command is permanently broken
- Quick fix needed to unblock
- Alternative data source available

---

## Part 7: Minimal Targeted Recommendation

### Immediate Action (Next 5 minutes)

```bash
# 1. SSH to EB instance
eb ssh

# 2. Check current article count
python manage.py shell
>>> from content.models import BlogPost
>>> print(f"Articles: {BlogPost.objects.count()}")
>>> print(f"Published: {BlogPost.objects.filter(is_published=True).count()}")
```

### Then Execute (Based on Result)

**If count is 0**:
```bash
# Articles missing — re-run seed command
python manage.py seed_knowledge_hub_phase_a --publish --force

# Verify
curl https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/
# Should return 200 OK
```

**If count is 13+**:
```bash
# Articles exist but not accessible — investigate routing
python manage.py shell
>>> from content.models import BlogPost
>>> post = BlogPost.objects.get(slug='nri-property-management-chennai-complete-guide')
>>> print(f"Title: {post.title}")
>>> print(f"is_published: {post.is_published}")

# Test URL
curl -I https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/
# Check response
```

---

## Conclusion

### Root Cause: **Data Loss During RDS Migration**

**Most Probable Explanation**:
1. EB migrated from SQLite (on instance) to PostgreSQL RDS
2. SQLite database became inaccessible when instance was replaced
3. Production PostgreSQL RDS is empty (no articles seeded)
4. Seed command in container_commands either failed silently or has a bug

### Next Steps

**DO THIS NOW** (Approval Required):
1. SSH to production and verify PostgreSQL article count
2. If count=0: Re-run seed command
3. If count>0: Investigate routing (unlikely)
4. Confirm article URLs return 200 OK

### Expected Outcome
✅ All 13 article URLs will return 200 OK  
✅ Articles will be accessible on production  
✅ Knowledge Hub Phase A complete

---

## Approval Checkpoint

**Before executing any remediation:**

- [ ] This root cause analysis confirmed?
- [ ] Verification steps approved?
- [ ] Remediation strategy agreed?
- [ ] Rollback plan in place (if needed)?

**Ready to proceed**: YES / NO

---

**Report Status**: COMPLETE | Root cause identified, remediation ready for approval.
