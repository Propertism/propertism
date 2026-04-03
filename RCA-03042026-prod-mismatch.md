# RCA: Production Site Mismatch Incident

**Document Name:** `RCA-03042026-prod-mismatch.md`  
**Incident Date:** April 3, 2026  
**Affected System:** `propertism.in` production website  
**Environment:** AWS Elastic Beanstalk `propertism-prod`  
**Prepared On:** April 3, 2026

---

## 1. Executive Summary

On April 3, 2026, the Propertism production website appeared to have reverted to an older stage or snapshot. Owners reported that the site was showing fallback copy, empty property listings, and degraded homepage sections, creating the impression that a previous version had been redeployed.

The investigation confirmed that this was **not a code rollback** and **not a Git reversion**. The root cause was a **production data-loss event** following an AWS Elastic Beanstalk EC2 instance replacement on April 2, 2026. Because the application was running on **SQLite stored on instance-local filesystem path `/var/app/data/db.sqlite3` without true persistent storage**, the replacement instance started with a fresh empty database. The latest application code then rendered against missing production content and fell back to default/template values, making the live site look like an old snapshot.

Production has since been restored, verified, and stabilized.

---

## 2. Business Impact

- Owners experienced visible production regression and loss of confidence.
- The homepage appeared to show old/fallback content instead of expected live business content.
- The `/properties/` page appeared empty.
- Reviews, blog, and other admin-managed sections were incomplete or degraded.
- The incident created operational disruption and escalations from site owners.

---

## 3. Incident Symptoms

The following symptoms were observed on the live site:

- Homepage copy resembled older/default content
- Featured properties section was empty
- `/properties/` page showed no active listings
- Review/blog/custom content sections were missing or degraded
- Overall appearance suggested that an old snapshot had been restored

---

## 4. What Was Initially Suspected

The first suspicion was that production had:

- rolled back to an older deployment
- deployed the wrong source bundle
- or picked up an outdated Git snapshot

This was ruled out during the investigation.

---

## 5. Confirmed Findings

### 5.1 No code rollback occurred

Elastic Beanstalk status showed production had remained on the previously deployed April 1 release until the recovery work began:

- Prior release before recovery: `app-5e96-260401_210822069586`
- Environment remained `Ready` and `Green`

This means the site was not serving an older application version from Git or EB history.

### 5.2 A new EB instance was created on April 2, 2026

Elastic Beanstalk logs show a fresh instance bootstrapping on:

- **April 2, 2026 15:52 UTC**

During that startup, the instance ran full Django migrations from scratch. That is strong evidence the application started against a fresh or empty database rather than the previous populated production database.

### 5.3 Production DB storage was not truly persistent

The app uses:

- `DB_PATH=/var/app/data/db.sqlite3`

configured in:

- [01_django.config](d:/viji/viji-olivine/03rolledout/01propertism/.ebextensions/01_django.config)

The so-called persistent DB config:

- [03_persistent_db.config](d:/viji/viji-olivine/03rolledout/01propertism/.ebextensions/03_persistent_db.config)

only creates the directory `/var/app/data`. It does **not** attach a persistent EBS volume, EFS mount, or managed database. Therefore, when the EC2 instance was replaced, the SQLite database file was lost.

### 5.4 The application masked the failure by falling back gracefully

The application did not crash when content records were missing:

- [site_context.py](d:/viji/viji-olivine/03rolledout/01propertism/content/site_context.py) returns `CompanyInfo.objects.first() or CompanyInfo()`
- [views.py](d:/viji/viji-olivine/03rolledout/01propertism/content/views.py) renders empty collections for properties, reviews, team, and blog instead of failing hard

This caused the latest codebase to render fallback/default content, which visually resembled an older site stage.

---

## 6. Root Cause

### Primary Root Cause

**Production content was lost because the site relied on SQLite stored on Elastic Beanstalk instance-local storage without real persistence.**

When AWS Elastic Beanstalk replaced the production EC2 instance on April 2, 2026, the new instance came up with a fresh empty database. The site then rendered using the current codebase but with missing admin-managed content and missing property records.

### Why it looked like an “older version”

The UI was not actually rolled back. Instead:

- business data disappeared
- default model values were used
- empty querysets removed live sections

That combination made the site look like an old snapshot even though the code version was still current.

---

## 7. Contributing Factors

### 7.1 SQLite was used as the production system of record

SQLite can work for simple deployments, but on Elastic Beanstalk it is unsafe as the primary production database when tied to instance-local storage.

### 7.2 No durable storage attachment was configured

There was no:

- Amazon RDS database
- attached persistent EBS volume strategy
- EFS mount
- automated restore-on-replacement process

### 7.3 No alert existed for silent content loss

The environment stayed `Green`, so infrastructure health looked normal even though business content had been lost.

There was no alert for:

- zero properties in production
- empty homepage content models
- empty review/blog sections

### 7.4 Graceful fallback behavior hid the severity

The app prioritized staying online and rendering something. Operationally that helped uptime, but from a business perspective it made the failure appear like a design rollback rather than a data-loss incident.

---

## 8. Recovery Actions Taken

### 8.1 Production investigation

Verified:

- live site degradation
- EB environment status
- currently deployed version
- codebase state
- boot logs showing fresh instance startup and migration flow

### 8.2 Content recovery deployment

Added and deployed a post-deploy recovery hook:

- [02_bootstrap_if_db_looks_empty.sh](d:/viji/viji-olivine/03rolledout/01propertism/.platform/hooks/postdeploy/02_bootstrap_if_db_looks_empty.sh)

This hook detects a production DB state where key content groups are missing and runs:

- `manage.py bootstrap_admin_content`

to repopulate:

- company info
- statistics
- services
- core values
- expertise areas
- customer reviews
- homepage card sections
- team members
- property types
- properties and property photos
- blog posts

### 8.3 Review content cleanup

During recovery, it was found that the bootstrap review section still contained unrelated placeholder content from another project. That was corrected in:

- [bootstrap_admin_content.py](d:/viji/viji-olivine/03rolledout/01propertism/content/management/commands/bootstrap_admin_content.py)

and a targeted repair hook was added:

- [03_repair_stale_customer_reviews.sh](d:/viji/viji-olivine/03rolledout/01propertism/.platform/hooks/postdeploy/03_repair_stale_customer_reviews.sh)

### 8.4 Final production verification

Verified after recovery:

- homepage repopulated
- `/properties/` repopulated
- review section corrected
- environment health remained `Green`

Final live application version after recovery:

- `app-b84e-260403_102423442741`

Final Git commit pushed to `origin/main`:

- `b84e83f`

---

## 9. Important Limitation Of Recovery

The recovery restored the curated bootstrap dataset from the repository, not necessarily the exact owner-entered production content that existed before the data-loss event.

This is an important distinction for the report:

- **The site was recovered functionally and visually**
- **The original live admin-managed records were not guaranteed recoverable**

Because no durable production database backup was attached to the replaced instance, exact live records could not be guaranteed restored from that lost instance.

---

## 10. Timeline

### April 1, 2026

- Known good production deploy completed
- Version: `app-5e96-260401_210822069586`

### April 2, 2026 at 15:52 UTC

- Elastic Beanstalk replacement instance bootstrapped
- Logs show full Django migration execution on a fresh DB

### April 3, 2026

- Owners reported production mismatch / apparent rollback
- Live checks confirmed:
  - empty properties
  - degraded homepage content
  - fallback/default copy showing

### April 3, 2026 recovery sequence

- Recovery hook deployed and executed
- Bootstrap content restored
- Review placeholders repaired
- Final verified live version:
  - `app-b84e-260403_102423442741`

---

## 11. Corrective Actions Completed

- Investigated and ruled out code rollback
- Identified data-loss mechanism from EB instance replacement
- Restored production content visibility
- Added production recovery hooks for empty-content states
- Repaired stale seeded review content
- Pushed recovery changes to GitHub

---

## 12. Preventive Actions Required

### Critical

1. Migrate production database from SQLite to a true persistent managed database
   - Recommended: **Amazon RDS PostgreSQL**

2. Implement automated backups and tested restore procedure

3. Add monitoring/alerting for business-data failure conditions
   - zero available properties
   - empty company info
   - empty reviews
   - empty blog posts

### Important

4. Add startup/health validation that fails loudly if production content is unexpectedly empty

5. Separate demo/bootstrap content from business-owned production content

6. Maintain a documented incident recovery runbook

### Optional but useful

7. Add a dashboard or admin audit command that checks production model counts after each deploy

---

## 13. Final Conclusion

This incident was caused by **production data loss after Elastic Beanstalk instance replacement**, not by a code rollback to an old Git snapshot.

The site looked like it had reverted because:

- the latest code remained deployed
- the production SQLite database was lost
- the application rendered fallback/default values when live records were missing

The immediate production issue has been resolved, but the deeper architectural risk remains until production is moved off SQLite-on-instance storage and onto a truly persistent database platform.

---

## 14. Reference Files

- [01_django.config](d:/viji/viji-olivine/03rolledout/01propertism/.ebextensions/01_django.config)
- [03_persistent_db.config](d:/viji/viji-olivine/03rolledout/01propertism/.ebextensions/03_persistent_db.config)
- [site_context.py](d:/viji/viji-olivine/03rolledout/01propertism/content/site_context.py)
- [views.py](d:/viji/viji-olivine/03rolledout/01propertism/content/views.py)
- [02_bootstrap_if_db_looks_empty.sh](d:/viji/viji-olivine/03rolledout/01propertism/.platform/hooks/postdeploy/02_bootstrap_if_db_looks_empty.sh)
- [03_repair_stale_customer_reviews.sh](d:/viji/viji-olivine/03rolledout/01propertism/.platform/hooks/postdeploy/03_repair_stale_customer_reviews.sh)
- [bootstrap_admin_content.py](d:/viji/viji-olivine/03rolledout/01propertism/content/management/commands/bootstrap_admin_content.py)
