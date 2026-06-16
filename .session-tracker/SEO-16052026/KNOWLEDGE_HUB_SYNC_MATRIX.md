# KNOWLEDGE HUB SYNC MATRIX

**Generated:** 2026-06-16 (Updated 13:25 IST)
**Local DB:** SQLite (`db.sqlite3`)
**Production DB:** PostgreSQL RDS (`propertism-db-2026`)

---

## Reconciliation Matrix

| PK | Slug | Local | Production (PostgreSQL) | Action |
|----|------|-------|------------------------|--------|
| 1 | `nri-property-checklist-chennai` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 2 | `rental-readiness-for-absentee-owners` | ✅ Published | ❌ NOT FOUND (not in DB) | **SYNCHRONIZATION REQUIRED** |
| 3 | `why-reporting-matters-for-nri-property-management` | ✅ Published | ❌ NOT FOUND (not in DB) | **SYNCHRONIZATION REQUIRED** |
| 4 | `nri-property-management-chennai-complete-guide` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 5 | `how-nris-can-sell-property-in-india-from-abroad` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 6 | `power-of-attorney-for-nris-complete-guide` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 7 | `how-to-verify-property-documents-chennai` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 8 | `patta-transfer-process-explained` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 9 | `encumbrance-certificate-guide-for-nris` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 10 | `property-tax-guide-chennai-nris` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 11 | `capital-gains-tax-property-sale-nris` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 12 | `tenant-management-guide-overseas-property-owners` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| 13 | `nri-property-maintenance-checklist` | ✅ Published | ✅ Published (200 OK) | **NO ACTION REQUIRED** |
| — | `NRI-Property-Sale-in-India` | ❌ Not in local | ✅ Published (200 OK) | **PRODUCTION ONLY** |
| — | `GCC-Absentee-Property-Flagging` | ❌ Not in local | ✅ Published (200 OK) | **PRODUCTION ONLY** |

---

## Summary

| Category | Count | Details |
|----------|-------|---------|
| Present in Both | **11** | PK=1, 4-13 |
| Missing in Production | **2** | PK=2, 3 (rental-readiness, why-reporting) |
| Production Only | **2** | NRI-Property-Sale-in-India, GCC-Absentee-Property-Flagging |
| **Total (Local)** | **13** | |
| **Total (Production)** | **13** | |

---

## Articles Requiring Synchronization

### Article 1: Rental Readiness for Absentee Owners
- **PK:** 2
- **Slug:** `rental-readiness-for-absentee-owners`
- **Category:** tenant
- **Content:** Stub (142 chars) — needs expansion
- **Production URL:** `https://www.propertism.in/blog/rental-readiness-for-absentee-owners/`

### Article 2: Why Reporting Matters for NRI Property Management
- **PK:** 3
- **Slug:** `why-reporting-matters-for-nri-property-management`
- **Category:** maintenance
- **Content:** Stub (676 chars, repeated text) — needs expansion
- **Production URL:** `https://www.propertism.in/blog/why-reporting-matters-for-nri-property-management/`

---

## Production-Only Articles (Not in Local SQLite)

### Article A: NRI Property Sale in India
- **Slug:** `NRI-Property-Sale-in-India`
- **Production URL:** `https://www.propertism.in/blog/NRI-Property-Sale-in-India/`
- **Status:** ✅ 200 OK

### Article B: GCC Absentee Property Flagging
- **Slug:** `GCC-Absentee-Property-Flagging`
- **Production URL:** `https://www.propertism.in/blog/GCC-Absentee-Property-Flagging/`
- **Status:** ✅ 200 OK
