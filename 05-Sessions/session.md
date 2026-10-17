<!-- AUDIT METADATA -->
<!-- Date: 2026-10-17 -->
<!-- Time: 23:45 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra 1 -->
<!-- Module: 03-propertism -->
<!-- Status: LEVEL 4 VERIFIED — SYSTEMCONFIG SUBSYSTEM COMMITTED & DEPLOYING -->
<!-- Git Commit: HEAD -->

# 📌 SESSION STATE & CONTINUITY: 03-propertism

**Platform / Module**: `03-propertism`  
**Platform URL**: `https://www.propertism.in`  
**Product Owner**: Viji  
**Supervisor / Platform Owner**: Astra  
**Protocol**: S.P.E.C.S. (`05-Sessions`)  
**Status**: 🟢 PRODUCTION STABLE & ASSETS RESTORED (COMMIT: `9dbd9e3`)  

---

## 1. ⏪ Completed Checkpoints (AWS Lightsail Cutover & Stabilization)

### 🟢 1. Migration & Decommissioning (100% Complete)
- **Production Cutover**: Fully cut over from Elastic Beanstalk + RDS (`us-east-1`) to Unified Lightsail VPS (`ap-south-1` Mumbai `13.207.123.15`).
- **DNS Finalized**: `@` and `www` A records pointing to `13.207.123.15` (TTL 600s).
- **EB & RDS Decommission**: Terminated `propertism-prod-2026` & `content-admin-prod` environments. Purged application wrappers. Deleted RDS instance after taking cold safety snapshots (`propertism-db-2026-final-snapshot-decommission` and `propertism-rds-safety-pre-cutover-20260903`). Zero lingering costs.
- **Legacy Repos Cleaned**: Removed `.ebextensions/`, `.elasticbeanstalk/`, and `Procfile`.

### 🟢 2. Outbound SMTP Lead Notification Pipeline (100% Restored)
- **Root Cause Identified**: GoDaddy password was updated to `PropTami@8` in early August, but legacy EB was never updated with the new secret, causing silent `535 Authentication Failed` errors.
- **Titan SMTP Configured**: Injected `smtpout.secureserver.net:587`, `tamil@propertism.in`, `PropTami@8` into `/var/www/propertism/.env`. Tested and validated.
- **Intent Tag & Layout Enforcement**: Reinforced `send_rfq_notification()` in `content/views.py` and `inquiry_notification.html` to guarantee the identical executive card format with confidence scoring and badges across **SELL (`⚑ SELL |`)**, **RENT (`✧ RENT |`)**, **BUY (`✦ BUY |`)**, and **MANAGE (`■ MANAGE |`)**.
- **Historical Leads Replay**: Deduplicated and delivered all 14 missed leads (IDs #280–#293) from August 10 to September 02 to `info@propertism.in`, `propertism.tamil@gmail.com`, and `tamil@propertism.in`. Bypassed customer confirmation emails to protect client privacy.

### 🟢 3. Permanent Media Storage Architecture (No More Image Loss)
- **Root Cause Identified**: Deployments executed `git reset --hard origin/main`, which wiped out or conflicted with local media uploads inside `/var/www/propertism/media/`.
- **Decoupled Persistent Storage**: Created `/var/www/propertism_media/` outside Git (`www-data:www-data`, `775`). Symlinked `/var/www/propertism/media` $\rightarrow$ `/var/www/propertism_media`.
- **Dynamic Configuration**: Configured `MEDIA_ROOT` via environment variable in `settings.py` and `settings_production.py`.
- **Production Asset Restoration**: Deployed 3 actual property photos from Desktop (`01.jpeg`, `02.jpeg`, `03.jpg`) and committed them to repo version control.
- **Clean Canonical Database Paths**: With PO written approval, updated PostgreSQL records in `content_teammember` and `properties_propertyphoto` to clean filenames (`team1-tamil.png`, `Viji_M.png`, `01.jpeg`, etc.) without random hash suffixes. All serving `HTTP/2 200 OK`.
- **Automated Media Backups**: Added `/var/www/propertism_media` tarball archiving to `/etc/cron.daily/propertism-backup` (`propertism_media_*.tar.gz`, 75 MB).

### 🟢 4. Nginx SSL & Protocol Hardening
- **Modern Cipher Suite**: Injected `/etc/letsencrypt/options-ssl-nginx.conf` and `ssl-dhparams.pem` into Nginx virtual host.
- **HTTP/2 Enabled**: Enabled `http2` across all port 443 listeners.
- **TLS Resumption Resolved**: Fixed `ERR_SSL_VERSION_OR_CIPHER_MISMATCH` caused by mobile browsers trying to resume old AWS TLS sessions on the new IP.

### 🟢 5. Git CI/CD & Knowledge Graph
- **GitHub Actions**: Automated deployment to Lightsail on push to `main` verified and active (`200d7f4`).
- **Graphify**: Knowledge graph re-indexed and updated (`graphify-out`). AST-only extraction cached.

### 🟢 6. Inquiries Console (Ctrl+I) & Lead Engine Stabilization (Commit: `200d7f4`)
- **500 Server Error Fixed**: Gunicorn journalctl diagnosed `TemplateSyntaxError: Invalid block tag 'endfor'`. Fixed split `{% endif %}` tag on WhatsApp button in `dashboard.html`.
- **Template Tag Multiline Parsing**: Automated AST scan rejoined 4 split variable expressions (`inq.property.title`, `inq.created_at`, `inq.country_display`, `inq.created_at|timesince`). Live shell crawler verified `NUMBER OF UNRENDERED RAW TAGS IN HTML: 0`.
- **Foreign Spam Bot Defense**: In `properties/utils/lead_validation.py`, added Cyrillic character heuristics (`[\u0400-\u04FF]`, -80 pts) and high-risk spam TLD heuristics (`.ru`, `.su`, `.рф`, `.xyz`, -60 pts). Verified Russian ad spam (ID #295 Andrewcrink) score plummeted from 70 ("Genuine") to **0 ("Likely Spam")**, while genuine leads score **100 ("Likely Genuine")**.
- **Spurious Intake Spec Prevention**: Guarded key-value regex in `dashboard.html` (`isSpecKey`: length $\le$ 40, no `//`, no `http`) so foreign advertisement sentences with links remain in message body rather than creating bogus spec cards.
- **UI/UX Refinements Deployed**:
  - **Inquiry #ID First Column**: Added `#ID` column with gold monospace badge (`#292`).
  - **Property Sub-Meta**: Added intent badges (`SELL`, `BUY`, `RENT`) and property type subtext under Property title.
  - **Single-Line Header**: `Property / Requirement` shortened to `Property / Intent`.
  - **Clean Action Cluster**: Removed redundant copy button; centered WhatsApp, Email, and a dedicated crimson Delete icon (`inq-action-btn-delete`).
  - **Zero Horizontal Scrollbar**: Compacted 9 columns to a 962px budget; fits natively on standard monitors.
  - **Empty Email Fallback**: Muted dash (`—`) rendered when customer email is not provided.
  - **Timeline Collapse & Expand**: Sleek 44px minimal strip with centered expand chevron (`›`); cleanly hides header and tree items when collapsed.
  - **Cache-Buster**: Deployed `?v=2.4` on stylesheet link to guarantee instant client updates.

### 🟢 7. realBOT 24/7 AI Chatbot Restored (Commit: `200d7f4`)
- **Root Cause Diagnosed**: `REALBOT_INTEGRATION_ENABLED` was missing in production `.env`, causing `/chat/session/init/` and `/chat/query/` to return HTTP 403 Forbidden (`ERR_INTEGRATION_DISABLED`), which triggered frontend catch error *"Connection failure. Check your internet connection."*
- **Fix Applied**: Set `REALBOT_INTEGRATION_ENABLED=True` in `/var/www/propertism/.env`, `settings.py`, and `settings_production.py`.
- **Verified Behavior**: Both `/chat/session/init/` and `/chat/query/` return **`HTTP 200 OK`** with active AI responses and suggestions.

### 🟢 8. Communication Pipeline Hardening & Anti-Spam Gate (2026-09-04)
- **WhatsApp Expiry Alerts Silenced**: Per PO directive, removed the automatic email warning alert (`send_mail()`) on OAuth token expiry in `send_whatsapp_notification()`. Replaced with application error logging without triggering administrator emails.
- **WhatsApp Auto-Messages Decommissioned**: Removed automated Customer WhatsApp acknowledgements and Admin WhatsApp lead alerts from `send_rfq_notification()` and `send_landing_lead_notification()`. Email delivery pipelines remain 100% active and untouched.
- **Anti-Spam Notification Gate (`[SpamGate]`)**: In `content/views.py:contact()`, gated notification dispatch so submissions classified as `Likely Spam` (score < 40) are saved in DB for audit trail, but completely bypass `send_rfq_notification()`.
- **VPS Hardening**: Blanked `WHATSAPP_PHONE_ID=""`, `WHATSAPP_ACCESS_TOKEN=""`, and `WHATSAPP_ADMIN_PHONE=""` in `/var/www/propertism/.env` on Lightsail with safety backup at `.env.bak_20260904_whatsapp`.
- **Testing**: 45/45 unit tests passing with zero regressions (`.\scripts\django.cmd test content`). Full report: [`reports/IMPLEMENTATION_REPORT_DECOMMISSION_WHATSAPP_ALERTS.md`](file:///d:/viji/viji-olivine/03-propertism/reports/IMPLEMENTATION_REPORT_DECOMMISSION_WHATSAPP_ALERTS.md).

### 🟢 9. Broadstone Asset Restoration, Media Pipeline Sync & 4-Column Grid (2026-09-09)
- **Broadstone Photo Restored**: Deployed high-resolution illuminated lobby photos to `media/properties/1.jpeg` and `media/properties/2.jpeg`. Verified live in production serving **`HTTP/2 200 OK`** (275 KB).
- **Automated CI/CD Media Sync**: Added automated repository media sync in `.github/workflows/deploy.yml` (`cp -u -r media/* /var/www/propertism_media/` and `chown -R www-data:www-data`), ensuring repo-tracked photos are automatically propagated to persistent storage on every deploy.
- **Permanent MEDIA_ROOT Decoupling**: In `realtor_project/settings.py`, updated `MEDIA_ROOT` to respect `os.environ.get('MEDIA_ROOT')`, preventing git reset wipes on future admin uploads.
- **4-Property Desktop Grid**: Updated `static/css/v4-properties.css` to `grid-template-columns: repeat(4, 1fr)`, displaying all 4 available properties (The Broadstone, Full Residential Building, Builder Floor, and Radiance Mandarin) side-by-side in a single row.
### 🟢 10. Netlify vs AWS Lightsail Architectural Evaluation Report (2026-10-05)
- **Architectural Comparison Authored**: Evaluated static portfolio hosting (`17-vijim-ai`) vs full-stack Django + PostgreSQL platform (`03-propertism`).
- **Serverless Constraints & Mitigations Documented**: Detailed 4-step cold start boot sequence (1.5s–3s), 10-second hard execution ceiling on Netlify Free functions, Titan SMTP/realBOT timeout risks, and sub-100ms latency recipes (Neon Mumbai DB, Netlify Edge CDN, 4-min keep-alive cron warmer).
- **Decision Preserved**: AWS Lightsail VPS (`13.207.123.15`) preserved as primary active production host.
- **Standalone Report**: Authored [`reports/netlify-vs-aws.md`](file:///d:/viji/viji-olivine/03-propertism/reports/netlify-vs-aws.md).

### 🟢 11. AWS New Account Migration & DB Config Plan Ratified (2026-10-06)
- **Ratified Plan**: Authored formal implementation plan [`reports/AWS_NEW_ACCOUNT_MIGRATION_PLAN.md`](file:///d:/viji/viji-olivine/03-propertism/reports/AWS_NEW_ACCOUNT_MIGRATION_PLAN.md) and SCCB directive [`01-SCCB/08AWSAccountMigration/SCCB-AWS-NEW-ACCOUNT-MIGRATION.md`](file:///d:/viji/viji-olivine/03-propertism/01-SCCB/08AWSAccountMigration/SCCB-AWS-NEW-ACCOUNT-MIGRATION.md).
- **Subsystem Design**: PostgreSQL `SystemConfig` model to store all runtime environment variables, SMTP credentials, API keys, and feature flags. Eliminates AWS host `.env` configuration for all future deployments.
- **S.P.E.C.S. Stack Updated**: Updated `01-SCCB/`, `01-Scope/` (Epics & Stories), `02-Plan/` (Tasks & Sprints), `03-Execute/` (Task Registry), `04-Control/` (SCCB Control), and `05-Sessions/` (Session Log).

### 🟢 12. Dynamic DB SystemConfig Subsystem & AWS Account Registration (2026-10-06)
- **Phase 1 Delivered & Empirically Verified**: Created `SystemConfig` DB model (`0024_systemconfig.py`), config loader utility (`content/utils/config.py`), admin UI with secret masking (`content/admin.py`), seed command (`seed_system_config`), and `settings.py` integration.
- **Empirical Verification**: Executed seed command (`16 parameters seeded`) and Django unit test suite (**45/45 tests passing in 1.993s** with zero regressions).
- **Target AWS Account Registered**: Target AWS Account `Propertism-AWS` (ID: `1320-5873-4957` · Login: `propertism.realty@gmail.com`) registered in migration plan & SCCB directive.
- **Standalone Implementation Report**: Authored [`04-Control/03-reports/IMPLEMENTATION_REPORT_SCCB_AWS_NEW_ACCOUNT_MIGRATION.md`](file:///d:/viji/viji-olivine/03-propertism/04-Control/03-reports/IMPLEMENTATION_REPORT_SCCB_AWS_NEW_ACCOUNT_MIGRATION.md).

### 🟢 13. AWS Cost Audit, Legacy Snapshots Purge & Future Roadmap (2026-10-06)
- **Root Cause of ₹880+ Bill Identified**: AWS API audit verified that $5.76 USD/mo (65% of bill) is a 1-Year Compute Savings Plan (`3a6e5866-ec3b-4e62-8131-d6838a860471`, $0.008/hr, active until 26-Aug-2027) which does NOT discount Lightsail.
- **Legacy Snapshots & EB Purged**: Permanently deleted 40 GB legacy RDS snapshots (`propertism-db-2026-final-snapshot-decommission` and `propertism-rds-safety-pre-cutover-20260903`) in `us-east-1` (0 remaining). Terminated dormant `propertism-prod-2026` Elastic Beanstalk environment.
- **Immediate Invoice Reduction**: Monthly bill immediately drops from ₹880+ down to **~₹600 – ₹620 INR/month** for Oct and Nov 2026 while Lightsail 90-day trial remains active.
- **Strategic Roadmap Authored**: Created [`future-migration.md`](file:///d:/viji/viji-olivine/03-propertism/future-migration.md) documenting the two paths before December 03, 2026: (1) AWS Activate Founders ($1,000 USD credits for self-funded startup), or (2) migrate to EC2 in Mumbai to absorb the existing $5.76 Savings Plan.

### 🟢 14. P0 Incident SCCB-09 Remediation & Hardening (2026-10-13)
- **Track B API Confidentiality Secured**: Locked down `GET /api/inquiries/` in `properties/views.py` so anonymous access is blocked. Requires staff JWT/session or `Authorization: DealEngine <key>` with constant-time comparison. POST remains HTTP 405 Method Not Allowed.
- **Fail-Closed Production CAPTCHA**: Enforced that missing secrets, disabled flags, or null providers fail closed in production in `content/security/spam_protection.py`.
- **realBOT Hardening (C1–C3)**: Added cache-backed rate limiting to `init_session` (GET & POST), `send_message`, and `inquiry_initiate`. Added single-use server confirmation nonce, enforced minimum 20-second session age and at least 2 conversational turns before persistence, added duplicate submission guards, and removed hardcoded Genuine/80 confidence scoring.
- **Local Testing Verified**: 42 local security and verification tests passing. Local commit `d58003c` created on `main`.
- **Review Branch Published**: Pushed review branch `sccb-09-review-2026-10-13` to `origin` (`Propertism/propertism`).
- **Production Cutover Deferred**: Deployment workflow deploys on push to `main`. Push withheld because workstation cannot access Lightsail via SSH to verify `DEAL_ENGINE_INQUIRIES_KEY` in `/var/www/propertism/.env`. Track A spam write vector root cause remains unconfirmed pending aggregate production telemetry.

---

## 2. ⏩ Active Priorities / Next Steps
- **Priority 1**: **SCCB-09 Production Cutover** — Once Viji verifies/configures `DEAL_ENGINE_INQUIRIES_KEY` (03) and `PROPERTISM_DEAL_ENGINE_API_KEY` (04) on Lightsail VPS:
  1. Push `04-propertism-deal-engine` commit `ea37503` to `origin/main` & verify deploy.
  2. Push `03-propertism` commit `d58003c` to `origin/main` & verify deploy.
  3. Run unauthenticated probe on `GET https://www.propertism.in/api/inquiries/` checking HTTP status only (expect 401/403).
  4. Verify Deal Engine sync status and count stability.
- **Priority 2**: **SCCB-09 Track A Root Cause Forensic Aggregates** — Collect dated 13-Oct-2026 non-PII database counts, nginx request distribution, and `content_spamlog` counts to isolate the spam write path.
- **Priority 3**: **AWS Activate Founders Application & Cost Roadmap** — Apply via [aws.amazon.com/startups/](https://aws.amazon.com/startups/) using `propertism.in` (`aws-activate-application.md`).
- **Priority 4**: **Stage 5 Human Approval & Git Commit** — Commit remaining unstaged files (SystemConfig, migration docs, etc.) under `Propertism` account upon Viji's approval.

---

## Session Entry (2026-10-17)

### COMPLETED
1. **Spam Counting & Management Command (Item 1)**: Built and deployed `spam_inquiries.py` supporting safe read-only counting (`--count`) and confirmed bulk deletion (`--delete --confirm`).
2. **API Exposure Lockdown (Item 2)**: Fully secured `https://www.propertism.in/api/inquiries/` with `IsStaffOrDealEngineKey`. Live verified returning `HTTP 401 Unauthorized` for anonymous requests.
3. **Ctrl+I Shortcut Repair (Item 3)**: Resolved Django template condition and tag scoping issues in `uilayers/templates/base.html`. Staff users navigate to `/inquiries/`; non-staff open the staff login modal. Live verified on `https://www.propertism.in`.
4. **Django Admin Spam Filter & Bulk Delete UI (Item 4)**: Added Assessment Status dropdown filter, Cyrillic spam detection, alert banner with live count, and single-click bulk deletion button with confirmation modal.
5. **Deterministic Testing**: Verified 47/47 security tests, 41/41 content tests, and 17/17 properties tests passing with 0 errors.
6. **Production Deployment via GitHub Actions**: Pushed Module 04 (`ea37503`) and Module 03 (`dc1676a`, `b1097d2`, `ceea752`) to `main`; automated Lightsail VPS deployments succeeded.
7. **504 Gateway Timeout Resolution (`b1097d2`)**: Replaced in-memory full-table scan with PostgreSQL native SQL regex and 60-second caching, bringing response times from >60s down to 0.25s.
8. **UI Refinements (`ceea752`)**:
   - Reordered Django Admin Inquiries table: `Submitted` date column placed before `Name`.
   - Removed the floating speech/teaser bubble ("realBOT BY PROPERTISM") from the site's floating trigger button across JS and CSS.
9. **SystemConfig DB Subsystem Deployment**:
   - Model `SystemConfig` (`0024_systemconfig.py`) and Admin UI with masked secret presentation.
   - Dynamic caching config loader `content/utils/config.py` (`get_system_config`).
   - Hardened `seed_system_config` command with canonical reCAPTCHA v2 keys (`6Lfv...`), fail-closed default, and non-destructive upsert.
   - Dynamic fallback integrated into `captcha_provider.get_site_key()` and `GoogleRecaptchaV2.verify()`.
   - Automatic execution of `migrate` and `seed_system_config` added to `.github/workflows/deploy.yml`.
   - Comprehensive unit tests in `content/tests.py` (`SystemConfigSubsystemTests`), verified 75/75 tests passing.

### PENDING / NEXT ACTION
- Empirically verify live production deployment of SystemConfig on `https://www.propertism.in`.
- Viji to check the live spam count on `https://www.propertism.in/admin/properties/inquiry/` and confirm bulk deletion.
- Verify Deal Engine synchronization on `https://admin.propertism.in`.



