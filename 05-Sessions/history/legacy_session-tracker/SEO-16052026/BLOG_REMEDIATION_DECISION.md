# BLOG REMEDIATION DECISION

**SCCB**: SCCB-PROP-PRODUCTION-BLOG-DATA-VERIFICATION-1606  
**Date**: 2026-06-16  
**Status**: ⏳ AWAITING APPROVAL

---

## Decision Matrix

### Production Published Count: 11 (> 0)

**Decision: DO NOT reseed the 10 Phase-A articles.**

The production database already contains 11 published articles that are serving correctly (HTTP 200). Re-seeding would create duplicate slugs or overwrite existing content.

---

## Root Cause Analysis

### Previous Contradiction Explained

| Evidence | Finding | Verdict |
|----------|---------|---------|
| Evidence A: `BlogPost.objects.filter(is_published=True).count() = 13` | Local SQLite query | ✅ Correct (local) |
| Evidence B: Production URLs return HTTP 404 | **Partially incorrect** — 11/13 return 200 | ❌ Only 2/13 return 404 |

**Root Cause of 404s**: 2 articles (`rental-readiness-for-absentee-owners` and `why-reporting-matters-for-nri-property-management`) exist in local SQLite but were never seeded to the production database. These are additional articles beyond the original 10 Phase-A set.

---

## Recommended Actions

### Action 1: Seed Missing Articles (2 articles)

The following 2 articles need to be seeded to production:

1. `rental-readiness-for-absentee-owners`
2. `why-reporting-matters-for-nri-property-management`

**Method**: SSH into production (requires access from authorized IP) and run:
```bash
cd /var/app/current
sudo -u webapp /var/app/venv/*/bin/python manage.py shell
```

Then create and publish these 2 articles manually, or deploy a new seed command that includes them.

### Action 2: Verify Sitemap Submission

With 11 articles now confirmed live, submit the sitemap to Google Search Console:
- URL: `https://www.propertism.in/sitemap.xml`
- Ensure all 11 article URLs are included

### Action 3: Monitor GSC Indexing

After sitemap submission:
- Wait 1-2 weeks for indexing
- Monitor GSC for indexed page count
- Track organic impressions and clicks

---

## What NOT To Do

- ❌ **DO NOT** run `seed_knowledge_hub_phase_a --publish` — this would create duplicates
- ❌ **DO NOT** modify database configuration
- ❌ **DO NOT** modify Django settings
- ❌ **DO NOT** deploy code changes (unless adding the 2 missing articles)

---

## Approval Required

- [ ] **Operator approves** seeding the 2 missing articles to production
- [ ] **Operator confirms** sitemap submission to GSC
- [ ] **Operator acknowledges** 11 articles are live and serving correctly

---

*Decision Matrix Complete: 2026-06-16 12:45 UTC*
