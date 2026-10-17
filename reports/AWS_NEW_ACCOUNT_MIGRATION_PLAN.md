<!-- AUDIT METADATA -->
<!-- Date: 2026-10-06 -->
<!-- Time: 09:33 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra 1 -->
<!-- Module: 03-propertism -->
<!-- Status: PENDING VIJI HUMAN REVIEW & APPROVAL -->
<!-- Git Commit: HEAD -->

# 🏛️ FORMAL IMPLEMENTATION PLAN & TASK SPECIFICATION
## Epic EPC-06: Database-Backed Dynamic Settings & AWS Account Migration (`03-propertism`)

**Product**: `03-propertism` (Propertism Real Estate Platform)  
**Production Host**: AWS Lightsail VPS (`13.207.123.15` · `ap-south-1` Mumbai)  
**Live URL**: [https://www.propertism.in](https://www.propertism.in)  
**Product Owner & Architect**: Viji  
**Implementation Supervisor**: Astra 1 (Primary Execution Engine)  
**Status**: 🟡 **PENDING VIJI REVIEW & EXPLICIT APPROVAL**

---

## 1. 📌 EXECUTIVE OBJECTIVES & MANDATORY INVARIANTS

### Core Mandates:
1. **Zero Domain & DNS Interruption**: GoDaddy DNS records (`@` and `www`) remain pointing to `13.207.123.15` until the new server on Viji's target AWS account is 100% deployed, populated, tested, and validated.
2. **Git Repository Invariant**: Single source of truth remains `Propertism/propertism` (`main` branch).
3. **AWS Account Migration**: Move production deployment from current AWS Account (`622370466597`) to Viji's target AWS Account **`Propertism-AWS`** (`1320-5873-4957`) with zero downtime.
4. **Zero-AWS-Host-Configuration Subsystem**: Store all application configuration variables, SMTP passwords, API keys, and feature flags inside the PostgreSQL database (`propertism_db`). Any future AWS migration requires **code deployment only, with ZERO environment variable configuration on the AWS host**.

---

## 2. 🏗️ SYSTEMCONFIG DATABASE SUBSYSTEM ARCHITECTURE

### Architecture Blueprint:
- **`SystemConfig` Django Model** in `content/models.py`:
  - `key` (CharField, unique, indexed): e.g. `EMAIL_HOST_PASSWORD`, `REALBOT_INTEGRATION_ENABLED`.
  - `value` (TextField): Storage value (string, boolean, integer, json).
  - `category` (CharField): `site`, `smtp`, `ai_chat`, `security`, `analytics`, `general`.
  - `is_secret` (BooleanField): Masks values in Admin UI (`••••••••`).
  - `description` (CharField): Human-readable guidance.

- **Dynamic Config Manager (`content/utils/config.py`)**:
  - `get_system_config(key, default=None)`: Fetches key from `SystemConfig` table with a 5-minute memory cache.
  - Automatically falls back to defaults or initial seed values during bootstrap.

- **Django Admin Interface (`/admin/content/systemconfig/`)**:
  - Categorized list view with search, filtering, and secret masking.
  - User UI for Viji/admins to update secrets and flags dynamically without SSH access or touching server files.

- **Database Connection Connection Boot Protocol**:
  - The local database (`DATABASES`) connects locally via standard PostgreSQL Unix socket / localhost.
  - Upon startup, all dynamic configuration parameters are read directly from PostgreSQL (`propertism_db`).
  - Because `pg_dump` backs up all PostgreSQL tables, a database restore on any new server restores **100% of environment variables, API credentials, and application flags automatically**.

---

## 3. 📋 DETAILED WORK BREAKDOWN & TASK REGISTRY (EPIC EPC-06)

| Task ID | Task Description | Scope & Component | Verification Gate / Deliverable | Status |
|---|---|---|---|:---:|
| **TSK-CFG-01** | **Create `SystemConfig` DB Model & Migration** | `content/models.py` | Run `makemigrations content` & apply migration cleanly. | ⚪ PLANNED |
| **TSK-CFG-02** | **Implement Dynamic Config Loader Utility** | `content/utils/config.py` | `get_system_config()` with caching & fallbacks verified via unit tests. | ⚪ PLANNED |
| **TSK-CFG-03** | **Implement Django Admin Interface** | `content/admin.py` | Categorized Admin UI with secret masking (`••••••••`). | ⚪ PLANNED |
| **TSK-CFG-04** | **Create Seed Data Management Command** | `content/management/commands/seed_system_config.py` | Command seeds existing `.env` variables into `SystemConfig` table. | ⚪ PLANNED |
| **TSK-CFG-05** | **Refactor `settings.py` for DB Sourcing** | `realtor_project/settings.py` | Sourcing SMTP, AI Chatbot, reCAPTCHA, and site URLs from DB config. | ⚪ PLANNED |
| **TSK-CFG-06** | **Execute Automated Test Suite & Sanity Sweep** | Test Suite | 45/45 unit tests passing with zero regressions. | ⚪ PLANNED |
| **TSK-MIG-15** | **Provision Target AWS Account Lightsail VPS** | Target AWS Account | Ubuntu 24.04 LTS (1GB RAM / 2 vCPU) + Static IP attached. | ⚪ PLANNED |
| **TSK-MIG-16** | **Transfer Database & Dynamic Media Storage** | PostgreSQL / Media | `pg_dump` restored into PG16; `/var/www/propertism_media` rsynced. | ⚪ PLANNED |
| **TSK-MIG-17** | **Deploy Application Code & Web Daemon** | Gunicorn / Nginx | Git pull, virtualenv, Gunicorn systemd daemon & Certbot SSL active. | ⚪ PLANNED |
| **TSK-MIG-18** | **Empirical Validation & Testing Gate** | Testing Gate | Form intake, admin login, Titan SMTP & realBOT verified on new IP. | ⚪ PLANNED |
| **TSK-MIG-19** | **GoDaddy DNS Cutover & CI/CD Secret Update** | DNS / GitHub | Update `@` & `www` A records; update GitHub Action secrets. | ⚪ PLANNED |
| **TSK-MIG-20** | **5-Day Observation & Legacy VPS Decommission** | Governance | Monitor 5 days; terminate old Lightsail instance `13.207.123.15`. | ⚪ PLANNED |

---

## 4. 🧪 4-PART EVIDENCE GATE & SELF-CRITIQUE

### Part 1: Potemkin Defense
- **Verification**: The `SystemConfig` model is backed by real PostgreSQL storage (`content_systemconfig` table) and integrated into Django `settings.py` lookup paths.

### Part 2: Dead-End Prevention
- **Verification**: Fallback mechanisms exist at every layer: if DB is uninitialized, `get_system_config()` returns standard static default values without crashing Django during initial bootstrap.

### Part 3: Data Reality & Storage Security
- **Verification**: Database credentials remain local to PostgreSQL socket. Secrets stored in `SystemConfig` are masked in Admin UI output.

### Part 4: User Journey Integrity
- **Verification**: Customer forms (`/contact/`), landing leads, realBOT chatbot queries, and email alerts function identically before and after DNS cutover.

---

## 5. 🚦 APPROVAL REQUEST TO PRODUCT OWNER (VIJI)

> **To Product Owner Viji**:  
> Please review this written implementation plan report ([`reports/AWS_NEW_ACCOUNT_MIGRATION_PLAN.md`](file:///d:/viji/viji-olivine/03-propertism/reports/AWS_NEW_ACCOUNT_MIGRATION_PLAN.md)).  
> Codebase is currently **100% clean and untouched**.  
> Upon your explicit confirmation, Astra 1 will begin Phase 1 execution (`TSK-CFG-01` through `TSK-CFG-06`).

