# PRODUCTION POSTGRES ARTICLE INVENTORY

**Generated:** 2026-06-16 (Updated 13:26 IST)
**Method 1:** URL-based validation against `https://www.propertism.in/blog/{slug}/`
**Method 2:** Direct PostgreSQL query via `eb ssh` (sudo python manage.py shell)

---

## Production Article Inventory (via PostgreSQL Query)

| # | Slug | HTTP Status | In PostgreSQL |
|---|------|-------------|---------------|
| 1 | `nri-property-checklist-chennai` | 200 ✅ | ✅ Published |
| 2 | `nri-property-management-chennai-complete-guide` | 200 ✅ | ✅ Published |
| 3 | `how-nris-can-sell-property-in-india-from-abroad` | 200 ✅ | ✅ Published |
| 4 | `power-of-attorney-for-nris-complete-guide` | 200 ✅ | ✅ Published |
| 5 | `how-to-verify-property-documents-chennai` | 200 ✅ | ✅ Published |
| 6 | `patta-transfer-process-explained` | 200 ✅ | ✅ Published |
| 7 | `encumbrance-certificate-guide-for-nris` | 200 ✅ | ✅ Published |
| 8 | `property-tax-guide-chennai-nris` | 200 ✅ | ✅ Published |
| 9 | `capital-gains-tax-property-sale-nris` | 200 ✅ | ✅ Published |
| 10 | `tenant-management-guide-overseas-property-owners` | 200 ✅ | ✅ Published |
| 11 | `nri-property-maintenance-checklist` | 200 ✅ | ✅ Published |
| 12 | `rental-readiness-for-absentee-owners` | 404 ❌ | ❌ NOT FOUND |
| 13 | `why-reporting-matters-for-nri-property-management` | 404 ❌ | ❌ NOT FOUND |
| — | `NRI-Property-Sale-in-India` | 200 ✅ | ✅ Published (production only) |
| — | `GCC-Absentee-Property-Flagging` | 200 ✅ | ✅ Published (production only) |

---

## Summary

| Metric | Value |
|--------|-------|
| Total BlogPost records in production (PostgreSQL) | **13** (confirmed via direct query) |
| Published articles in production | **13** |
| Matching local SQLite articles | **11** |
| Missing from production (need sync) | **2** |
| Production-only articles (not in local) | **2** |
| Total local articles | **13** |

---

## Notes

- Production database is PostgreSQL RDS (`propertism-db-2026`) — confirmed via `eb ssh` direct query.
- Direct PostgreSQL query executed via: `sudo /var/app/venv/staging-LQM1lest/bin/python -c "import os,re; data=open('/opt/elasticbeanstalk/deployment/env').read(); [os.environ.__setitem__(k,v) for k,v in re.findall(r'^([A-Z_]+)=(.*)$',data,re.M)]; ..."`
- Production has 2 articles NOT in local SQLite: `NRI-Property-Sale-in-India` and `GCC-Absentee-Property-Flagging`
- The 2 missing articles (`rental-readiness-for-absentee-owners`, `why-reporting-matters-for-nri-property-management`) do NOT exist in PostgreSQL at all (not even as drafts)
- URL validation uses `/blog/{slug}/` pattern (confirmed as the correct production URL pattern).
- The `/insights/` page returns 404 — not deployed on production.
- The `/blog/` page returns 200 — this is the active blog listing page.
- Sitemap at `/sitemap.xml` returns 200 and contains 11 blog articles (the 2 missing ones are absent).
