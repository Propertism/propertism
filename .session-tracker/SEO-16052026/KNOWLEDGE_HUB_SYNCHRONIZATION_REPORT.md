# KNOWLEDGE HUB SYNCHRONIZATION REPORT

**Generated:** 2026-06-16
**Method:** Option A — Targeted synchronization via management command

---

## Synchronization Summary

| Metric | Value |
|--------|-------|
| Articles requiring sync | **2** |
| Articles synchronized | **0** (pending operator action) |
| Articles skipped (already exist) | **0** |
| Errors | **0** |

---

## Synchronization Method

**Approved Approach:** Option A — Targeted synchronization command

A custom management command has been prepared that will:
1. Connect to production PostgreSQL via `DATABASE_URL`
2. Check if each article already exists by slug
3. Insert only genuinely missing articles
4. Preserve all existing production content

---

## Synchronization Artifacts

### 1. Exported JSON Data
- **File:** `missing_knowledge_hub_articles.json`
- **S3 Location:** `s3://olivine-site-673981388490/missing_knowledge_hub_articles.json`
- **Contents:** 2 BlogPost records (PK=2, PK=3) in Django serialized JSON format

### 2. Import Script
- **File:** `scratch/import_to_production.py`
- **S3 Location:** `s3://olivine-site-673981388490/import_to_production.py`
- **Features:** Duplicate checking, safe insert, verification

---

## Execution Instructions

```bash
# From an authorized SSH IP (122.167.96.150 or 122.167.96.214):

# Step 1: SSH into production
ssh -i /path/to/propertism-key.pem ec2-user@propertism.com

# Step 2: Download artifacts
curl -o /tmp/missing_knowledge_hub_articles.json \
  https://olivine-site-673981388490.s3.amazonaws.com/missing_knowledge_hub_articles.json

curl -o /tmp/import_to_production.py \
  https://olivine-site-673981388490.s3.amazonaws.com/import_to_production.py

# Step 3: Run import
cd /var/app/current
sudo -u webapp /var/app/venv/*/bin/python /tmp/import_to_production.py

# Step 4: Verify
curl -s -o /dev/null -w "%{http_code}" \
  https://www.propertism.in/blog/rental-readiness-for-absentee-owners/
# Expected: 200

curl -s -o /dev/null -w "%{http_code}" \
  https://www.propertism.in/blog/why-reporting-matters-for-nri-property-management/
# Expected: 200
```

---

## ⚠️ Post-Synchronization Actions Required

1. **Regenerate sitemap** — Run `python manage.py sitemap --ping` or equivalent
2. **Resubmit to GSC** — Submit updated sitemap to Google Search Console
3. **Content expansion** — Both articles have stub content and need full article expansion for SEO value
