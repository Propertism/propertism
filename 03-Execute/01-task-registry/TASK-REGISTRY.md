<!-- AUDIT METADATA -->
<!-- Date: 2026-09-03 -->
<!-- Time: 14:20 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra -->
<!-- Module: 03-propertism -->
<!-- Status: ACTIVE -->
<!-- Git Commit: HEAD (uncommitted) -->

# 📊 OPERATIONAL TASK REGISTRY (SINGLE SOURCE OF TRUTH)

**Module**: `03-propertism`  
**Platform / URL**: `www.propertism.in`  
**Product Owner**: Viji  
**Supervisor**: Astra (Antigravity IDE)  
**Protocol**: S.P.E.C. (03-Execute)  
**Last Updated**: 2026-09-03 14:20 IST  
**Status**: 🟢 ACTIVE  

---

## 📑 Registry Overview

| Epic ID | Epic Description | Target Milestone | Status |
|---|---|---|:---:|
| **EPC-01** | S.P.E.C. Governance & Core Scaffolding | Framework baseline | 🟢 DONE |
| **EPC-02** | Core Domain & Global Directory Synchronization | Inquiry #290 / 249-country sync | 🟢 DONE |
| **EPC-03** | SEO Authority & Conversational RealBot Engine | pSEO & Knowledge Base | 🟢 DONE |
| **EPC-04** | **AWS Lightsail Migration (EB + RDS ➔ Unified Lightsail VPS)** | Cost reduction to $12/mo & Mumbai latency | 🟡 IN PROGRESS |

---

## 🚀 EPIC-04: AWS LIGHTSAIL MIGRATION TASK REGISTRY

### 1. 🛫 Pre-Implementation Tasks (Phase 1: Pre-Cutover Setup — Zero Risk, Zero Downtime)

*Objective: Provision and configure the new Mumbai environment completely ahead of time with zero impact on live production traffic or databases.*

| Task ID | Task Summary | Component | Owner | Status | Gate Check & Verification Evidence |
|---|---|---|:---:|:---:|---|
| **TSK-MIG-01** | **Provision Lightsail Instance & Static IP** | AWS Lightsail (`ap-south-1`) | Viji / Astra | 🟢 DONE | **Target**: Ubuntu 24.04 LTS, 1 GB RAM / 2 vCPU / 40 GB SSD ($7/mo tier).<br>**Evidence**: Static IPv4 `13.207.123.15` attached; instance `propertism-mumbai-01` active; direct SSH verified with Exit 0. |
| **TSK-MIG-02** | **OS Hardening, Swap & Package Stack Installation** | Host OS / Linux | Astra | 🟢 DONE | **Action**: 2 GB swap file enabled (`vm.swappiness=10`); UFW active (`22`, `80`, `443`); PG16 tuned (`shared_buffers=64MB`); Redis 7 tuned (`maxmemory 32mb`); Fail2ban active.<br>**Evidence**: Services active: `postgresql`, `redis-server`, `nginx`, `fail2ban`; 492 MB RAM free + 2048 MB swap. |
| **TSK-MIG-03** | **Codebase Deployment & Database Configuration** | Application / Database | Astra | 🟢 DONE | **Action**: Cloned repo to `/var/www/propertism`; venv & `requirements.txt` installed; `propertism_db` & `propertism_user` configured on local PG16; `.env` configured.<br>**Evidence**: `psql` connection successful; all dependencies verified. |
| **TSK-MIG-04** | **Initial Bootstrap, Gunicorn Daemon & SSL Issuance** | Web Tier / SSL | Astra | 🟢 DONE | **Action**: Initial migrations applied; 236 static files collected; Gunicorn systemd service active (2 workers, 2 threads); Nginx configured on ports 80 & 443; HTTP 200 validated.<br>**Evidence**: `systemctl is-active gunicorn` is `active`; `curl http://13.207.123.15/` returns `HTTP 200 OK`. |
| **TSK-MIG-05** | **Confirm GoDaddy DNS TTL is 300s** | DNS / GoDaddy | Viji | ⚪ READY | **Action**: Verify GoDaddy `@` and `www` A records have TTL set to **300 seconds (5 minutes)** at least 24 hours prior to cutover.<br>**Evidence**: `dig propertism.in +nocmd +noall +answer` displays TTL $\le 300$. |

---

### 2. ⚡ Implementation Tasks (Phase 2: Cutover Window — Scheduled Maintenance: ~20-30 Mins)

*Objective: Authoritatively freeze legacy writes, transfer the 25 MB database, synchronize sequences, verify data parity, and flip DNS.*

| Task ID | Task Summary | Component | Owner | Status | Gate Check & Verification Evidence |
|---|---|---|:---:|:---:|---|
| **TSK-MIG-06** | **Manual Safety Snapshot of Production RDS** | Database / AWS RDS | Astra | 🟢 DONE | **Action**: Trigger manual snapshot `propertism-rds-safety-pre-cutover-20260903` on RDS `propertism-db-2026`.<br>**Evidence**: AWS RDS reports status `available (100% progress)`. |
| **TSK-MIG-07** | **Enumerate & Stop Every Database Writer** | Application Tier / EB | Astra | 🟢 DONE | **Action**: Stopped EB Gunicorn (`sudo systemctl stop web`); confirmed zero active connections on RDS.<br>**Evidence**: `pg_stat_activity` returned `active_connections: 0`. |
| **TSK-MIG-08** | **Dump RDS & Direct Transfer to Lightsail** | Database / Migration | Astra | 🟢 DONE | **Action**: Plain SQL dump (`pg_dump` 17.8) extracted (4.4 MB) without S3 intermediary; transferred to local PC and Lightsail.<br>**Evidence**: `propertism_cutover.sql` verified on Lightsail `/tmp/propertism_cutover.sql`. |
| **TSK-MIG-09** | **Database Restoration & Sequence Synchronization** | Local Database / PG16 | Astra | 🟢 DONE | **Action**: Restored plain SQL into `propertism_db`; ran `sqlsequencereset` across all models.<br>**Evidence**: All sequences reset (`setval` executed for 60+ sequences); Gunicorn restarted. |
| **TSK-MIG-10** | **Database Parity Sanity Check & Media Sync** | Verification / Storage | Astra | 🟢 DONE | **Action**: Query verification: 57 inquiries, 3 properties, 14 users, 25 blogs. Synced 48 media files (34 MB) from S3 to `/var/www/propertism/media/`.<br>**Evidence**: Row counts identical to RDS; media served via Nginx with HTTP 200 OK. |
| **TSK-MIG-11** | **Application Smoke Testing on Lightsail** | QA / Validation | Astra / Viji | 🟢 DONE | **Action**: Tested homepage (329 KB rendered with live data) and Django admin login.<br>**Evidence**: HTTP 200 OK returned on both endpoints with valid CSRF tokens. |
| **TSK-MIG-12** | **Authoritative DNS Switch & Let's Encrypt SSL** | DNS & SSL | Viji / Astra | 🟢 DONE | **Action**: GoDaddy `@` A record updated to `13.207.123.15` (TTL 600s); `www` CNAME pointed to `@`. Issued Let's Encrypt SSL certificate via Certbot.<br>**Evidence**: `https://www.propertism.in` returns HTTP 200 OK with valid SSL expiring Dec 02, 2026. |

---

### 3. 🏁 Post-Implementation Checklist (Phase 3: Post-Cutover & Cooldown)

*Objective: Confirm global propagation, monitor live traffic, maintain zero-risk rollback standby for 5 days, and decommission legacy resources.*

| Task ID | Task Summary | Component | Owner | Status | Gate Check & Verification Evidence |
|---|---|---|:---:|:---:|---|
| **TSK-MIG-13** | **Global DNS Propagation & Live Traffic Verification** | Networking / Nginx | Astra | 🟢 DONE | **Action**: Query public resolvers (`8.8.8.8`, `1.1.1.1`); tail Lightsail `/var/log/nginx/access.log` for incoming organic HTTP requests.<br>**Evidence**: `dig` returns Lightsail Static IP from multiple locations; HTTP 200 requests visible in Nginx log. |
| **TSK-MIG-13** | **5-Day Legacy Stack Freeze & Observation Window** | Governance | Astra / Viji | ⚪ SUPERSEDED | **Action**: Replaced by immediate decommission on explicit PO authorization.<br>**Evidence**: PO requested immediate decommission to stop legacy AWS charges. |
| **TSK-MIG-14** | **Decommission Legacy Elastic Beanstalk & RDS Stack** | Cloud Infrastructure | Astra | 🟢 DONE | **Action**: Terminated EB `propertism-prod-2026`; deleted RDS `propertism-db-2026` with final snapshot; disabled legacy CloudFront `d1yv5od4i0bho`.<br>**Evidence**: RDS status `deleting`; EB status `Terminating`; Deal Engine `content-admin-prod` left untouched. |

---

## 🛠️ Baseline Scaffolding Tasks (Archive)

| Task ID | Epic / Feature | Task Summary | Component | Owner | Status | Gate Check & Verification Evidence |
|---|---|---|---|:---:|:---:|---|
| **TSK-001** | EPC-01 | Module Scaffolding & S.P.E.C. Baseline | Root | Astra | 🟢 DONE | S.P.E.C. folder hierarchy (`01-Scope` through `04-Control`) initialized and verified |
| **TSK-002** | EPC-01 | Technical Architecture & Domain Schemas | `01-Scope/` | Astra | 🟢 DONE | Invariant contracts and data models defined |
| **TSK-003** | EPC-02 | Global Country Directory Synchronization | `properties/` | Astra | 🟢 DONE | 249 canonical country entities synced; Inquiry #290 verified |
| **TSK-004** | EPC-03 | SEO Authority & Conversational RealBot | `chat/`, `search/` | Astra | 🟢 DONE | RealBot knowledge state machine and schema markup verified |
| **TSK-005** | EPC-04 | Lightsail Migration Architecture Hardening | `reports/` | Astra | 🟢 DONE | REV-8.4 completed; Lean 15-Task Runbook adopted |
