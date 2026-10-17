<!-- AUDIT METADATA -->
<!-- Date: 2026-08-29 -->
<!-- Time: 22:20 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra -->
<!-- Module: TEMPLATE -->
<!-- Status: CANONICAL TEMPLATE -->
<!-- Git Commit: HEAD (uncommitted) -->

# 03-Stories — User Stories & Acceptance Criteria

**Module**: `03-propertism`  
**Protocol**: S.P.E.C. (01-Scope)  
**Status**: 🟢 ACTIVE  

---

## Stories

### US-01: Module Initialization
- **As a**: Platform Architect
- **I want**: `03-propertism` initialized with S.P.E.C. governance
- **So that**: All future tasks are tracked deterministically.
- **Acceptance Criteria**:
  - `01-Scope`, `02-Plan`, `03-Execute`, `04-Control` exist.
  - `TASK-REGISTRY.md` initialized.

### US-02: Core Feature Implementation
- **As a**: System User
- **I want**: Core service capabilities operational
- **So that**: Business deliverables are achieved.
- **Acceptance Criteria**:
  - Deterministic test pass (Exit code 0).
  - Unbroken end-to-end user journey.

### US-06A: Database-Backed System Configuration Subsystem
- **As a**: System Administrator & Platform Owner
- **I want**: All application secrets, SMTP credentials, AI settings, and security flags stored in PostgreSQL database (`propertism_db`) and manageable via Django Admin UI
- **So that**: Future server deployments require zero AWS host-level `.env` configuration.
- **Acceptance Criteria**:
  - `SystemConfig` model & Admin UI created with secret masking (`••••••••`).
  - `get_system_config()` utility implemented with 5-minute caching.
  - `seed_system_config` management command populates DB table from existing settings.
  - 45/45 Django unit tests pass with zero regressions.

### US-06B: Zero-Downtime AWS Account Migration
- **As a**: Product Owner (Viji)
- **I want**: Propertism production server migrated from old AWS account (`622370466597`) to target AWS account
- **So that**: GoDaddy DNS remains unchanged, new IP is fully tested before cutover, and old server is safely decommissioned after 5 days.
- **Acceptance Criteria**:
  - Target AWS account Lightsail instance provisioned with PostgreSQL 16 & Gunicorn.
  - Database dump (`pg_dump`) & dynamic media `/var/www/propertism_media` restored.
  - Pre-cutover verification gate passed (Titan SMTP, realBOT, lead intake verified on new IP).
  - GoDaddy DNS `@` and `www` A records flipped to new Static IP.
  - Old server decommissioned after 5-day observation window.

