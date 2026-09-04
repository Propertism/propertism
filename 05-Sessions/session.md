<!-- AUDIT METADATA -->
<!-- Date: 2026-09-04 -->
<!-- Time: 12:55 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra -->
<!-- Module: 03-propertism -->
<!-- Status: WHATSAPP DECOMMISSIONED & SPAM GATE HARDENED (LEVEL 4 VERIFIED) -->
<!-- Git Commit: HEAD (uncommitted) -->

# 📌 SESSION STATE & CONTINUITY: 03-propertism

**Platform / Module**: `03-propertism`  
**Platform URL**: `https://www.propertism.in`  
**Product Owner**: Viji  
**Supervisor / Platform Owner**: Astra  
**Protocol**: S.P.E.C.S. (`05-Sessions`)  
**Status**: 🟢 PRODUCTION STABLE & HARDENED (COMMIT: `200d7f4`)  

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

---

## 2. ⏩ Active Priorities / Next Steps
- **Priority 1**: **Sister Site Deal Ingestion** — Ensure Deal Engine consumes `https://www.propertism.in/api/inquiries/` cleanly.
- **Priority 2**: **Frontend Synchronization** — Synchronize and align property listing APIs with `04-propertism-deal-engine`.
- **Priority 3**: **SEO Authority & Meta Verification** — Periodic audit of OpenGraph tags, sitemaps, and SSR performance.
