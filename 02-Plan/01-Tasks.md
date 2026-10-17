<!-- AUDIT METADATA -->
<!-- Date: 2026-08-29 -->
<!-- Time: 22:20 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra -->
<!-- Module: TEMPLATE -->
<!-- Status: CANONICAL TEMPLATE -->
<!-- Git Commit: HEAD (uncommitted) -->

# 01-Tasks — Work Breakdown Structure (WBS)

**Module**: `03-propertism`  
**Protocol**: S.P.E.C. (02-Plan)  
**Status**: 🟢 ACTIVE  

---

| Task ID | Story | Task Description | Target Component | Owner |
|---|---|---|---|---|
| **TSK-001** | US-01 | Scaffold S.P.E.C. folder hierarchy | Root | Astra |
| **TSK-002** | US-01 | Define Architecture & Schemas | `01-Scope/` | Astra |
| **TSK-003** | US-02 | Implement Core Logic & APIs | `backend/` | Astra |
| **TSK-004** | US-02 | Build UI & Complete User Journey | `frontend/` | Astra |
| **TSK-005** | US-02 | Execute Verification & Control Gate | `04-Control/` | Astra |
| **TSK-CFG-01** | US-06A | Create `SystemConfig` DB Model & Migration | `content/models.py` | Astra |
| **TSK-CFG-02** | US-06A | Implement Dynamic Config Loader Utility | `content/utils/config.py` | Astra |
| **TSK-CFG-03** | US-06A | Implement Django Admin Interface | `content/admin.py` | Astra |
| **TSK-CFG-04** | US-06A | Create Seed Data Management Command | `content/management/` | Astra |
| **TSK-CFG-05** | US-06A | Refactor `settings.py` for DB Sourcing | `realtor_project/` | Astra |
| **TSK-CFG-06** | US-06A | Execute Automated Test Suite & Sanity Sweep | Test Suite | Astra |
| **TSK-MIG-15** | US-06B | Provision Target AWS Account Lightsail VPS | AWS Lightsail | Viji / Astra |
| **TSK-MIG-16** | US-06B | Transfer Database Dump & Dynamic Media | PostgreSQL / Media | Astra |
| **TSK-MIG-17** | US-06B | Deploy Code & Web Server Daemon | Gunicorn / Nginx | Astra |
| **TSK-MIG-18** | US-06B | Empirical Pre-Cutover Validation Gate | Testing Gate | Astra / Viji |
| **TSK-MIG-19** | US-06B | GoDaddy DNS Cutover & GitHub Secrets Update | DNS / GitHub | Viji / Astra |
| **TSK-MIG-20** | US-06B | 5-Day Observation & Legacy VPS Decommission | Infrastructure | Astra / Viji |

