<!-- AUDIT METADATA -->
<!-- Date: 2026-09-03 -->
<!-- Time: 16:35 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra -->
<!-- Module: 03-propertism -->
<!-- Status: COMPREHENSIVE PROGRESS REPORT -->
<!-- Target: propertism.in (ap-south-1 Mumbai Lightsail) -->

# 📋 AWS LIGHTSAIL MIGRATION — COMPREHENSIVE PROGRESS & EXECUTION REPORT
## Infrastructure Right-Sizing: Elastic Beanstalk + RDS (`us-east-1`) ➔ Unified Lightsail VPS (`ap-south-1`)

**Target Domain**: `propertism.in` / `www.propertism.in`  
**Author**: Astra (Supervisor)  
**Reviewed by**: Viji (Product Owner)  
**Execution Timestamp**: 2026-09-03 (14:00 – 16:35 IST)  
**Active Plan**: Frozen Lean Execution Runbook (15 Tasks)  

---

## 1. Executive Summary & Cost Rationale

The production infrastructure for `propertism.in` was historically running on **AWS Elastic Beanstalk (Python 3.11 AL2023)** paired with **AWS RDS PostgreSQL (17.9)** in **`us-east-1` (N. Virginia)**. 
- **Billing Baseline**: AWS promotional credits ($180.00) were fully exhausted. The forecast monthly cost was **USD 46.53 (~₹4,382 INR/mo)**, driven largely by idle RDS db.t4g.micro compute and Elastic Load Balancing.
- **Latency Baseline**: Cross-continental round-trip time between Indian visitors and `us-east-1` averaged **220–250 ms**.
- **Migration Target**: A unified **Amazon Lightsail VPS** in **`ap-south-1` (Mumbai)** on the **$7.00/mo tier (~₹590 INR/mo)**, delivering an **85% recurring cost reduction** and cutting latency to **~25 ms**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                ARCHITECTURE COMPARISON                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ LEGACY STACK (us-east-1, N. Virginia)     │ NEW STACK (ap-south-1, Mumbai)             │
├───────────────────────────────────────────┼────────────────────────────────────────────┤
│ • AWS Elastic Beanstalk (t3.micro EC2)    │ • AWS Lightsail VPS (propertism-mumbai-01) │
│ • AWS RDS PostgreSQL 17.9 (db.t4g.micro)  │ • Local PostgreSQL 16 (tuned 64MB buffers) │
│ • AWS Classic/App Load Balancer           │ • Local Redis 7 (LRU cache, 32MB cap)      │
│ • AWS S3 Bucket (propertism-media)        │ • Local High-Speed Media (/var/www/media)  │
│ • Cost: ~$46.53 / month (~₹4,380 INR)     │ • Cost: $7.00 / month (~₹590 INR)          │
│ • Latency: ~220 ms                        │ • Latency: ~25 ms                          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Completed Implementation Tasks & Evidence Matrix

### 🟢 Task 1: Provision Lightsail Instance & Static IP (TSK-MIG-01)
- **Instance Identifier**: `propertism-mumbai-01`
- **Region & Availability Zone**: `ap-south-1` (Mumbai, Zone A / `ap-south-1a`)
- **OS Blueprint**: Ubuntu 24.04 LTS (Noble Numbat, 64-bit)
- **Hardware Profile**: 1 GB RAM, 2 vCPUs, 40 GB SSD, 2 TB Transfer ($7/mo)
- **Network Interfaces**:
  - **Static IPv4**: `13.207.123.15` (attached permanently)
  - **Private IPv4**: `172.26.6.70`
  - **Public IPv6**: `2406:da1a:164b:c400:b9b3:ca27:798e:8113`
- **Security Credentials**:
  - Downloaded `LightsailDefaultKey-ap-south-1.pem`.
  - Applied NTFS ACL hardening via `icacls` (restricted exclusively to user `vijay`).
  - Passwordless OpenSSH verified: `Exit 0`.

---

### 🟢 Task 2: OS Hardening, Swap & Package Stack (TSK-MIG-02)
- **Swap Space Provisioned**: 2 GB swap file created at `/swapfile` (`chmod 600`, `vm.swappiness=10`).
  - Total virtual memory capacity expanded to **~3 GB** (preventing OOM spikes).
- **Security & Firewall**:
  - Linux UFW enabled: Inbound denied by default; TCP `22`, `80`, `443` allowed.
  - Fail2ban service enabled and running.
  - AWS Lightsail IPv4 Firewall configured: Ports `22` (SSH), `80` (HTTP), `443` (HTTPS) open.
- **Base Packages Installed**:
  - `nginx` (1.24.0), `postgresql-16`, `postgresql-client-16`, `redis-server` (7.x), `python3.12`, `python3.12-venv`, `libpq-dev`, `certbot`, `python3-certbot-nginx`.
- **Low-Footprint Engine Tuning**:
  - PostgreSQL 16: `shared_buffers = 64MB`, `max_connections = 25`.
  - Redis: `maxmemory 32mb`, `maxmemory-policy allkeys-lru`.
- **Telemetry Verification**:
  - Active RAM used: **418 MB**; Free physical RAM: **492 MB**; Free swap: **2,048 MB**.

---

### 🟢 Task 3: Codebase Deployment & Local PostgreSQL Configuration (TSK-MIG-03)
- **Directory Layout**: Application root established at `/var/www/propertism`.
- **Git Synchronization**: Pulled repository directly from GitHub `https://github.com/Propertism/propertism.git`.
- **Virtual Environment**: Isolated Python 3.12 venv initialized at `/var/www/propertism/venv`.
  - Upgraded pip and installed all 19 required production packages:
    - `Django==4.2.16`, `djangorestframework==3.14.0`, `psycopg2-binary==2.9.9`, `gunicorn==21.2.0`, `django-allauth==65.16.0`, `whitenoise==6.6.0`, `boto3==1.34.69`, `Pillow==10.1.0`.
- **PostgreSQL 16 Setup**:
  - Database: `propertism_db`
  - User: `propertism_user`
  - Privileges: Schema `public` ownership and all permissions granted.
  - Connection verified via localhost socket and TCP `127.0.0.1:5432`.
- **Production Environment (`/var/www/propertism/.env`)**:
  - Configured with `DJANGO_ENV=production`, `DEBUG=False`, strong cryptographic `SECRET_KEY`, `USE_LOCAL_STORAGE=1`, and `POSTGRES_*` pointing to `127.0.0.1:5432`.
  - File permissions locked down to `600` owned by `ubuntu:www-data`.

---

### 🟢 Task 4: Bootstrap, Gunicorn Daemon, Nginx & Live Verification (TSK-MIG-04)
- **Database Schema Provisioning**:
  - Executed `./venv/bin/python manage.py migrate --noinput`.
  - All **50+ core migrations** applied cleanly across `auth`, `account`, `chat` (M2.1-M2.7), `communications`, `content`, `properties`, `sites`, `socialaccount`, and `users`.
- **Static Asset Compilation**:
  - Executed `collectstatic --noinput` ➔ **236 static files** collected into `/var/www/propertism/staticfiles`.
- **Gunicorn Systemd Daemon**:
  - Created `/etc/systemd/system/gunicorn.service` (2 sync workers, 2 threads, bound to `127.0.0.1:8000`, User `www-data`).
  - Enabled and active on boot (`systemctl enable --now gunicorn`).
- **Nginx Reverse Proxy**:
  - Configured `/etc/nginx/sites-available/propertism` proxying to `127.0.0.1:8000`.
  - Direct local serving with 30-day client caching for `/static/` and `/media/`.
  - SSL listener enabled on port 443.
- **Verification Evidence**:
  - `curl -I http://127.0.0.1/` ➔ **`HTTP/1.1 200 OK`** (Content-Length: 217,571 bytes).
  - `curl -I http://13.207.123.15/` ➔ **`HTTP/1.1 200 OK`** (latency < 20 ms).
  - `curl -k -I https://13.207.123.15/` ➔ **`HTTP/1.1 200 OK`** over SSL.
  - `curl -I http://13.207.123.15/static/admin/css/base.css` ➔ **`HTTP 200 OK`**.

---

### 🟢 Task 6: Manual Safety Snapshot of Production RDS (TSK-MIG-06)
- **Snapshot ID**: `propertism-rds-safety-pre-cutover-20260903`
- **Source Instance**: `propertism-db-2026` (`us-east-1`)
- **Status**: **`available (100% progress)`**
- **Purpose**: Guaranteed zero-risk fallback insurance. If any issue arises, RDS can be restored from this exact snapshot.

---

### 🟢 Non-Blocking Production Database Dump (Triple-Layer Backup)
- **Dump Tooling**: PostgreSQL 17.8 client installed on Elastic Beanstalk EC2 to match RDS engine version 17.9.
- **Extraction Command**:
  ```bash
  pg_dump -h propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com \
          -U propertismadmin -d propertismdb -F c -b -v \
          -f /tmp/propertism_prod_backup_20260903.dump
  ```
- **Backup Locations**:
  1. **AWS Cloud**: RDS Snapshot `propertism-rds-safety-pre-cutover-20260903`.
  2. **Local Hard Drive**: `d:\viji\viji-olivine\03-propertism\propertism_prod_backup_20260903.dump` (630 KB).
  3. **Mumbai Lightsail Server**: `/tmp/propertism_prod_backup_20260903.dump` (617 KB, transferred and ready for restore).
- **Data Integrity**: Verified live table counts on RDS:
  - `properties_inquiry`: **57 records**
  - `properties_property`: **3 records**
  - `auth_user`: **14 records**

---

### 🟢 Media Asset Migration (Task 10 Completed Ahead of Time)
- **Source S3 Bucket**: `propertism-media-622370466597`
- **Volume**: **48 media files**, totaling **33.96 MB** (logos, hero gifs, team bios, property photos).
- **Local Storage**: Synchronized to `d:\viji\viji-olivine\03-propertism\media_backup/`.
- **Lightsail Storage**: Deployed directly into `/var/www/propertism/media/` (`www-data:www-data`, permissions `755`).
- **Live HTTP Validation**:
  - `curl -I http://13.207.123.15/media/company/propertism-logo.png` ➔ **`HTTP 200 OK`** (6.34 MB served directly by Nginx at line speed).

---

### 🟢 Repository Governance, Author Identity & CI/CD Protection
1. **GitHub Actions De-escalation**:
   - Disabled automated deployment to Elastic Beanstalk in `.github/workflows/deploy.yml` (`workflow_dispatch` manual trigger only).
   - Eliminated noisy 11-minute failure notification emails.
2. **Repository Author Configuration**:
   - Local Git config set to `Propertism <info@propertism.in>` for `03-propertism`.
   - Global Git config preserved as `Viji M <vijaymgs@gmail.com>` for `olivine` and other repositories.
3. **Secret Leak Prevention**:
   - Hardened `.gitignore` to strictly exclude `*.pem`, `*.key`, `*.dump`, `*.sql`, `media_backup/`, and operational screenshots.

---

## 3. Remaining Cutover Steps (Execution Window: ~10 Minutes)

| Task | Action | Estimated Duration | Owner | Status |
|---|---|:---:|:---:|:---:|
| **TSK-MIG-07** | Stop EB web worker (`sudo systemctl stop web`) to enforce zero writes | 1 min | Astra | ⚪ READY |
| **TSK-MIG-08** | Verify zero connections on RDS (`pg_stat_activity`) | 1 min | Astra | ⚪ READY |
| **TSK-MIG-09** | Restore dump into `propertism_db` on Lightsail via `pg_restore` | 2 mins | Astra | ⚪ READY |
| **TSK-MIG-09b**| Reset database sequences (`python manage.py sqlsequencereset`) | 1 min | Astra | ⚪ READY |
| **TSK-MIG-10** | Verify database parity on Lightsail (57 inquiries, 3 properties) | 1 min | Astra | ⚪ READY |
| **TSK-MIG-11** | Smoke test Django admin and inquiry submission on Mumbai | 2 mins | Viji / Astra | ⚪ READY |
| **TSK-MIG-12** | Switch GoDaddy DNS A records (`@` and `www`) to `13.207.123.15` | 2 mins | Viji | ⚪ READY |
| **TSK-MIG-12b**| Issue official Let's Encrypt SSL (`sudo certbot --nginx`) | 1 min | Astra | ⚪ READY |
| **TSK-MIG-13** | Keep legacy EB + RDS untouched for 5-day observation window | - | - | ⚪ PLANNED |

---

## 4. Sign-Off & Verification

- **Current Operational Health**: All services active on Lightsail Mumbai (`13.207.123.15`).
- **Rollback Preparedness**: 100% available. RDS snapshot taken, local dump secured on disk, legacy EB untouched.
- **Proceed Authorization**: Standing by for Product Owner sign-off to execute final database restore and DNS switch.
