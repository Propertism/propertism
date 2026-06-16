# SITEMAP CONTENT VALIDATION

**Generated:** 2026-06-16
**Target:** `https://www.propertism.in/sitemap.xml`

---

## Sitemap Accessibility

| Check | Result |
|-------|--------|
| Sitemap URL | `https://www.propertism.in/sitemap.xml` |
| HTTP Status | **200 OK** ✅ |
| Content Type | `application/xml` |
| Parseable | ✅ Yes |

---

## Blog Articles in Sitemap

| # | URL in Sitemap | Production Status | In Sitemap? |
|---|----------------|-------------------|-------------|
| 1 | `https://www.propertism.in/blog/nri-property-checklist-chennai/` | ✅ 200 OK | ✅ |
| 2 | `https://www.propertism.in/blog/rental-readiness-for-absentee-owners/` | ❌ 404 | ❌ **MISSING** |
| 3 | `https://www.propertism.in/blog/why-reporting-matters-for-nri-property-management/` | ❌ 404 | ❌ **MISSING** |
| 4 | `https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/` | ✅ 200 OK | ✅ |
| 5 | `https://www.propertism.in/blog/how-nris-can-sell-property-in-india-from-abroad/` | ✅ 200 OK | ✅ |
| 6 | `https://www.propertism.in/blog/power-of-attorney-for-nris-complete-guide/` | ✅ 200 OK | ✅ |
| 7 | `https://www.propertism.in/blog/how-to-verify-property-documents-chennai/` | ✅ 200 OK | ✅ |
| 8 | `https://www.propertism.in/blog/patta-transfer-process-explained/` | ✅ 200 OK | ✅ |
| 9 | `https://www.propertism.in/blog/encumbrance-certificate-guide-for-nris/` | ✅ 200 OK | ✅ |
| 10 | `https://www.propertism.in/blog/property-tax-guide-chennai-nris/` | ✅ 200 OK | ✅ |
| 11 | `https://www.propertism.in/blog/capital-gains-tax-property-sale-nris/` | ✅ 200 OK | ✅ |
| 12 | `https://www.propertism.in/blog/tenant-management-guide-overseas-property-owners/` | ✅ 200 OK | ✅ |
| 13 | `https://www.propertism.in/blog/nri-property-maintenance-checklist/` | ✅ 200 OK | ✅ |

---

## Sitemap Quality Checks

| Check | Result |
|-------|--------|
| Duplicate URLs | ✅ None found |
| Malformed URLs | ✅ None found |
| Article count matches production inventory | ✅ 11/11 |
| Missing articles (should be added after sync) | **2** |

---

## Summary

| Metric | Value |
|--------|-------|
| Total URLs in sitemap | **11 blog articles + static pages** |
| Blog articles in sitemap | **11** |
| Blog articles on production | **11** |
| Blog articles missing from sitemap | **2** (not yet on production) |
| Sitemap health | ✅ Good |

---

## Post-Sync Action Required

After the 2 missing articles are synchronized to production:
1. Regenerate sitemap: `python manage.py sitemap`
2. Verify sitemap contains all 13 articles
3. Resubmit to Google Search Console
