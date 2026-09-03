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
| **TSK-MIG-03** | **Codebase Deployment & Database Configuration** | Application / Database | Astra | ⚪ READY | **Action**: Clone repo to `/var/www/propertism`; setup Python venv & `requirements.txt`; create `propertism_db` and `propertism_user` with SCRAM-SHA-256 on `127.0.0.1:5432`; configure `/var/www/propertism/.env`.<br>**Evidence**: `psql -U propertism_user -h 127.0.0.1 propertism_db` connects successfully. |
| **TSK-MIG-04** | **Initial Bootstrap, Gunicorn Daemon & SSL Issuance** | Web Tier / SSL | Astra | ⚪ READY | **Action**: Run migrations on empty DB (`migrate`); `collectstatic --noinput`; configure `gunicorn.service` (2 sync workers bound to `/run/gunicorn.sock`); configure Nginx reverse proxy; issue Let's Encrypt SSL via Certbot.<br>**Evidence**: `systemctl is-active gunicorn`, `sudo nginx -t`, `curl http://127.0.0.1` returns HTTP 200. |
| **TSK-MIG-05** | **Confirm GoDaddy DNS TTL is 300s** | DNS / GoDaddy | Viji | ⚪ READY | **Action**: Verify GoDaddy `@` and `www` A records have TTL set to **300 seconds (5 minutes)** at least 24 hours prior to cutover.<br>**Evidence**: `dig propertism.in +nocmd +noall +answer` displays TTL $\le 300$. |

---

### 2. ⚡ Implementation Tasks (Phase 2: Cutover Window — Scheduled Maintenance: ~20-30 Mins)

*Objective: Authoritatively freeze legacy writes, transfer the 25 MB database, synchronize sequences, verify data parity, and flip DNS.*

| Task ID | Task Summary | Component | Owner | Status | Gate Check & Verification Evidence |
|---|---|---|:---:|:---:|---|
| **TSK-MIG-06** | **Manual Safety Snapshot of Production RDS** | AWS RDS (`us-east-1`) | Astra / Viji | ⚪ READY | **Action**: Create manual snapshot `propertism-rds-safety-pre-cutover`.<br>**Evidence**: Snapshot status confirmed as `available` in RDS console before proceeding. |
| **TSK-MIG-07** | **Enumerate & Stop Every Database Writer** | Web Tier / Database | Astra | ⚪ READY | **Action**: Stop Gunicorn on Elastic Beanstalk (or set `MAINTENANCE_MODE=true`); stop any background workers/cron; check `pg_stat_activity` on RDS.<br>**Evidence**: `SELECT count(*) FROM pg_stat_activity WHERE datname='propertism_db' AND pid <> pg_backend_pid();` returns **`0`**. |
| **TSK-MIG-08** | **Dump RDS & Direct Transfer to Lightsail** | Database / Network | Astra | ⚪ READY | **Action**: Run `pg_dump -h <RDS> -U postgres -d propertism_db -F c -b -v -f /tmp/propertism_cutover.dump`; direct `scp` to Lightsail (no S3 detour).<br>**Evidence**: Exit code `0`; file size `> 5 MB`; SHA-256 match between source and target. |
| **TSK-MIG-09** | **Database Restoration & Sequence Synchronization** | PostgreSQL / Django | Astra | ⚪ READY | **Action**: Run `pg_restore -U postgres -d propertism_db --clean --if-exists -v /tmp/propertism_cutover.dump`; run `python manage.py sqlsequencereset properties users chat \| sudo -u postgres psql -d propertism_db`.<br>**Evidence**: `pg_restore` completes with zero fatal errors; sequences aligned with `max(id)`. |
| **TSK-MIG-10** | **Database Parity Sanity Check & Media Direct Sync** | Database / Media | Astra | ⚪ READY | **Action**: Sanity check row counts (`Inquiry` ~290, `Property`, `User`); eyeball latest 3 inquiries; sync media via `rsync -avz` and verify directory bytes.<br>**Evidence**: Row counts identical to old RDS; `du -sh /var/www/propertism/media` matches source. |
| **TSK-MIG-11** | **Application Smoke Testing on Lightsail** | Full Stack | Astra | ⚪ READY | **Action**: Submit test inquiry via hosts override or direct IP; test Django Admin login; verify email alert & WhatsApp dispatch.<br>**Evidence**: Test inquiry persisted in DB with correct country code; notification emails received. |
| **TSK-MIG-12** | **Authoritative DNS Switch to Lightsail** | GoDaddy DNS | Viji | ⚪ READY | **Action**: Update GoDaddy `@` and `www` A records to `<LIGHTSAIL_STATIC_IP>`; remove any stale IPv6 (AAAA) records pointing to old EB/CloudFront.<br>**Evidence**: GoDaddy DNS dashboard displays Lightsail Static IP. |

---

### 3. 🏁 Post-Implementation Checklist (Phase 3: Post-Cutover & Cooldown)

*Objective: Confirm global propagation, monitor live traffic, maintain zero-risk rollback standby for 5 days, and decommission legacy resources.*

| Task ID | Task Summary | Component | Owner | Status | Gate Check & Verification Evidence |
|---|---|---|:---:|:---:|---|
| **TSK-MIG-13** | **Global DNS Propagation & Live Traffic Verification** | Networking / Nginx | Astra | ⚪ READY | **Action**: Query public resolvers (`8.8.8.8`, `1.1.1.1`); tail Lightsail `/var/log/nginx/access.log` for incoming organic HTTP requests.<br>**Evidence**: `dig` returns Lightsail Static IP from multiple locations; HTTP 200 requests visible in Nginx log. |
| **TSK-MIG-14** | **5-Day Standby Cooldown (The Real Rollback Net)** | Elastic Beanstalk / RDS | Astra / Viji | ⚪ READY | **Mandatory Rule**: Do NOT delete EB or RDS. Leave both running untouched and idle for **minimum 5 days**.<br>**Evidence**: If critical failure occurs, revert GoDaddy DNS in 60s. Daily error log check on Lightsail. |
| **TSK-MIG-15** | **Controlled Decommissioning of Legacy Stack** | AWS Billing / Decommission | Viji / Astra | ⚪ READY | **Action**: After 5 clean days: take final safety snapshot of RDS; delete RDS instance; terminate Elastic Beanstalk environment.<br>**Evidence**: Monthly AWS bill drops from ~$40.08/mo to **$12.00/mo** (or $0.00 during initial trial). |

---

## 🛠️ Baseline Scaffolding Tasks (Archive)

| Task ID | Epic / Feature | Task Summary | Component | Owner | Status | Gate Check & Verification Evidence |
|---|---|---|---|:---:|:---:|---|
| **TSK-001** | EPC-01 | Module Scaffolding & S.P.E.C. Baseline | Root | Astra | 🟢 DONE | S.P.E.C. folder hierarchy (`01-Scope` through `04-Control`) initialized and verified |
| **TSK-002** | EPC-01 | Technical Architecture & Domain Schemas | `01-Scope/` | Astra | 🟢 DONE | Invariant contracts and data models defined |
| **TSK-003** | EPC-02 | Global Country Directory Synchronization | `properties/` | Astra | 🟢 DONE | 249 canonical country entities synced; Inquiry #290 verified |
| **TSK-004** | EPC-03 | SEO Authority & Conversational RealBot | `chat/`, `search/` | Astra | 🟢 DONE | RealBot knowledge state machine and schema markup verified |
| **TSK-005** | EPC-04 | Lightsail Migration Architecture Hardening | `reports/` | Astra | 🟢 DONE | REV-8.4 completed; Lean 15-Task Runbook adopted |
