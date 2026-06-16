# SCCB-PROP-KNOWLEDGE-HUB-MISSING-ARTICLES-HANDOFF-1606

## Session Context
- **Date:** 2026-06-16
- **Session:** 34 (SEO Authority Execution)
- **Role:** Platform Integration Lead
- **Scope:** Propertism stabilization — Knowledge Hub missing articles remediation

---

## Problem Statement

Two Knowledge Hub articles that exist in the local SQLite database are **not present on production** (returning 404):

| # | Slug | Title | Production Status |
|---|------|-------|-------------------|
| 1 | `rental-readiness-for-absentee-owners` | Rental Readiness for Absentee Owners | ❌ 404 |
| 2 | `why-reporting-matters-for-nri-property-management` | Why Reporting Matters for NRI Property Management | ❌ 404 |

These are the only 2 out of 13 total BlogPost records that are missing from production.

---

## Root Cause

The articles were created in the local SQLite database (PK=2, PK=3) but were **never deployed** to the production PostgreSQL database. The production database has 11 articles (PK=1, PK=4 through PK=13), missing PK=2 and PK=3.

---

## Deliverables

### 1. Exported JSON — `missing_knowledge_hub_articles.json`
- **Location:** `d:\viji\viji-olivine\03rolledout\01propertism\missing_knowledge_hub_articles.json`
- **S3 Backup:** `s3://olivine-site-673981388490/missing_knowledge_hub_articles.json`
- **Contents:** 2 BlogPost records (PK=2, PK=3) in Django serialized JSON format
- **Encoding:** UTF-8 (handles ₹ and other Unicode characters)

### 2. Import Script — `import_to_production.py`
- **Location:** `d:\viji\viji-olivine\03rolledout\01propertism\scratch\import_to_production.py`
- **S3 Backup:** `s3://olivine-site-673981388490/import_to_production.py`
- **Function:** Safe import script that checks for duplicates before inserting

### 3. Article Details

#### Article 1: Rental Readiness for Absentee Owners
- **Slug:** `rental-readiness-for-absentee-owners`
- **Category:** tenant
- **Author:** Propertism Team
- **Excerpt:** "How to keep a Chennai property rental-ready when the owner is overseas."
- **Content:** 1 sentence (142 chars) — **stub content, needs expansion**
- **Published:** Yes
- **Published Date:** 2026-04-21

#### Article 2: Why Reporting Matters for NRI Property Management
- **Slug:** `why-reporting-matters-for-nri-property-management`
- **Category:** maintenance
- **Author:** Propertism Team
- **Excerpt:** "Consistent reporting is what turns property management from reactive work into decision support."
- **Content:** 1 sentence repeated 4 times (676 chars) — **stub content, needs expansion**
- **Published:** Yes
- **Published Date:** 2026-04-21

---

## Import Instructions (for SSH operator)

```bash
# Step 1: SSH into production from an authorized IP
ssh -i /path/to/propertism-key.pem ec2-user@propertism.com

# Step 2: Download the JSON data file
curl -o /tmp/missing_knowledge_hub_articles.json \
  https://olivine-site-673981388490.s3.amazonaws.com/missing_knowledge_hub_articles.json

# Step 3: Download the import script
curl -o /tmp/import_to_production.py \
  https://olivine-site-673981388490.s3.amazonaws.com/import_to_production.py

# Step 4: Run the import
cd /var/app/current
sudo -u webapp /var/app/venv/*/bin/python /tmp/import_to_production.py

# Step 5: Verify
curl -s -o /dev/null -w "%{http_code}" \
  https://propertism.com/knowledge-hub/rental-readiness-for-absentee-owners/
# Expected: 200

curl -s -o /dev/null -w "%{http_code}" \
  https://propertism.com/knowledge-hub/why-reporting-matters-for-nri-property-management/
# Expected: 200
```

---

## ⚠️ Important Notes

1. **Both articles have stub content** — they are placeholders with 1-4 sentences. Full content expansion is needed for SEO value.
2. **SSH access is restricted** — our current IP is not in the security group whitelist. Import must be done from an authorized IP (122.167.96.150 or 122.167.96.214).
3. **No IAM role** on the EC2 instance — S3 access is via public URL, not instance profile.
4. **After import**, the sitemap should be regenerated and resubmitted to Google Search Console.

---

## Verification Checklist

- [ ] Article 1 returns 200 on production
- [ ] Article 2 returns 200 on production
- [ ] Both articles appear in sitemap
- [ ] Sitemap resubmitted to GSC
- [ ] Content expanded from stub to full article (future work)

---

## Related Documents
- `SEO-16052026/seo-implementation-plan.md` — Master SEO plan
- `SEO-16052026/BLOG_REMEDIATION_DECISION.md` — Remediation decision log
- `SEO-16052026/BLOG_DATA_COMPARISON_REPORT.md` — Local vs production comparison
- `SEO-16052026/PRODUCTION_BLOG_DATA_VERIFICATION.md` — Production verification results
