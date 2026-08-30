# KNOWLEDGE HUB URL VALIDATION

**Generated:** 2026-06-16
**Target:** `https://www.propertism.in`

---

## URL Pattern Discovery

Three URL patterns were tested against production:

| Pattern | Result |
|---------|--------|
| `/knowledge-hub/{slug}/` | ❌ All 404 |
| `/blog/{slug}/` | ✅ 11/13 OK |
| `/insights/{slug}/` | ❌ All 404 |

**Confirmed production URL pattern:** `/blog/{slug}/`

---

## Article URL Validation Matrix

| # | URL | HTTP Status | Result |
|---|-----|-------------|--------|
| 1 | `https://www.propertism.in/blog/nri-property-checklist-chennai/` | 200 | ✅ |
| 2 | `https://www.propertism.in/blog/rental-readiness-for-absentee-owners/` | 404 | ❌ |
| 3 | `https://www.propertism.in/blog/why-reporting-matters-for-nri-property-management/` | 404 | ❌ |
| 4 | `https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/` | 200 | ✅ |
| 5 | `https://www.propertism.in/blog/how-nris-can-sell-property-in-india-from-abroad/` | 200 | ✅ |
| 6 | `https://www.propertism.in/blog/power-of-attorney-for-nris-complete-guide/` | 200 | ✅ |
| 7 | `https://www.propertism.in/blog/how-to-verify-property-documents-chennai/` | 200 | ✅ |
| 8 | `https://www.propertism.in/blog/patta-transfer-process-explained/` | 200 | ✅ |
| 9 | `https://www.propertism.in/blog/encumbrance-certificate-guide-for-nris/` | 200 | ✅ |
| 10 | `https://www.propertism.in/blog/property-tax-guide-chennai-nris/` | 200 | ✅ |
| 11 | `https://www.propertism.in/blog/capital-gains-tax-property-sale-nris/` | 200 | ✅ |
| 12 | `https://www.propertism.in/blog/tenant-management-guide-overseas-property-owners/` | 200 | ✅ |
| 13 | `https://www.propertism.in/blog/nri-property-maintenance-checklist/` | 200 | ✅ |

---

## Additional Page Validation

| URL | HTTP Status | Result |
|-----|-------------|--------|
| `https://www.propertism.in/` | 200 | ✅ |
| `https://www.propertism.in/blog/` | 200 | ✅ |
| `https://www.propertism.in/insights/` | 404 | ❌ |
| `https://www.propertism.in/sitemap.xml` | 200 | ✅ |

---

## Summary

| Metric | Value |
|--------|-------|
| Total article URLs tested | **13** |
| HTTP 200 OK | **11** |
| HTTP 404 Not Found | **2** |
| Success rate | **84.6%** |
