# BLOG DATA COMPARISON REPORT

**SCCB**: SCCB-PROP-PRODUCTION-BLOG-DATA-VERIFICATION-1606  
**Date**: 2026-06-16  
**Status**: ✅ COMPLETE

---

## Local vs Production Comparison

| Metric | Local SQLite | Production (propertism.in) |
|--------|-------------|---------------------------|
| **Total Articles** | 13 | 11 (confirmed via URL access) |
| **Published Articles** | 13 | 11 |
| **Slug Count** | 13 | 11 |
| **Database Engine** | SQLite (local) | SQLite (standalone EC2, no RDS) |
| **HTTP 200 OK** | N/A | 11/13 |
| **HTTP 404** | N/A | 2/13 |

---

## Slug-by-Slug Comparison

| # | Slug | Local SQLite | Production URL | Status |
|---|------|-------------|----------------|--------|
| 1 | `nri-property-maintenance-checklist` | ✅ Published | ✅ 200 OK | ✅ Match |
| 2 | `tenant-management-guide-overseas-property-owners` | ✅ Published | ✅ 200 OK | ✅ Match |
| 3 | `capital-gains-tax-property-sale-nris` | ✅ Published | ✅ 200 OK | ✅ Match |
| 4 | `property-tax-guide-chennai-nris` | ✅ Published | ✅ 200 OK | ✅ Match |
| 5 | `encumbrance-certificate-guide-for-nris` | ✅ Published | ✅ 200 OK | ✅ Match |
| 6 | `patta-transfer-process-explained` | ✅ Published | ✅ 200 OK | ✅ Match |
| 7 | `how-to-verify-property-documents-chennai` | ✅ Published | ✅ 200 OK | ✅ Match |
| 8 | `power-of-attorney-for-nris-complete-guide` | ✅ Published | ✅ 200 OK | ✅ Match |
| 9 | `how-nris-can-sell-property-in-india-from-abroad` | ✅ Published | ✅ 200 OK | ✅ Match |
| 10 | `nri-property-management-chennai-complete-guide` | ✅ Published | ✅ 200 OK | ✅ Match |
| 11 | `nri-property-checklist-chennai` | ✅ Published | ✅ 200 OK | ✅ Match |
| 12 | `rental-readiness-for-absentee-owners` | ✅ Published | ❌ 404 | ❌ Missing |
| 13 | `why-reporting-matters-for-nri-property-management` | ✅ Published | ❌ 404 | ❌ Missing |

---

## Analysis

### Matched Articles (11)
All 10 original Phase-A articles plus `nri-property-checklist-chennai` are present and accessible on production. These were successfully seeded and published.

### Missing Articles (2)
`rental-readiness-for-absentee-owners` and `why-reporting-matters-for-nri-property-management` exist in the local SQLite database but return 404 on production. These are likely additional articles that were created locally but never deployed/ seeded to the production server.

### Infrastructure Note
The production server is a standalone EC2 instance (`olivine-demo-backend`) in `us-east-1` with no Elastic Beanstalk environment and no RDS PostgreSQL instance. It appears to be using SQLite as its database engine.

---

*Comparison Complete: 2026-06-16 12:45 UTC*
