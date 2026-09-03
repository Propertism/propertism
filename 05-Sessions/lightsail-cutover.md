<!-- AUDIT METADATA -->
<!-- Date: 2026-09-03 -->
<!-- Time: 14:05 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra -->
<!-- Module: 03-propertism -->
<!-- Status: APPROVED LEAN EXECUTION PLAN -->
<!-- Target Region: ap-south-1 (Mumbai) -->
<!-- Instance: 2 GB RAM / 2 vCPU / 60 GB SSD / 3 TB Transfer ($12.00/mo) -->

# 🚀 LIGHTSAIL MIGRATION — LEAN EXECUTION RUNBOOK
## Target: `propertism.in` — Elastic Beanstalk + RDS (`us-east-1`) ➔ Unified Lightsail (`ap-south-1`, 2GB / 2vCPU)

> **Supersedes**: REV-8.4 (all 80 review directives). This is the frozen, lean execution plan. Do not add steps.  
> **Target Cost**: $12.00/mo (~₹1,000 INR/mo) down from ~$40.08/mo.  
> **Latency**: ~25–30 ms from Chennai to Mumbai (down from ~220 ms to N. Virginia).  

---

## ⚠️ RISKS & PRAGMATIC MITIGATIONS

1. **Undetected DB writer survives the "freeze"**:
   - *Mitigation*: Before dump: enumerate every process with prod DB credentials (EB Gunicorn, any worker, cron, systemd timers, admin/laptop connections). Stop all. Confirm via `pg_stat_activity` that no connections remain except your own.
2. **Incomplete/corrupt `pg_dump`**:
   - *Mitigation*: Check exit code 0 and non-trivial file size (`> 5 MB`) before proceeding to restore. Do not restore on a suspect dump.
3. **Mixed-backend traffic after DNS flip**:
   - *Mitigation*: TTL already lowered to 300s 24h prior. After flip, verify propagation via `dig` from 2+ locations before declaring done.
4. **OOM on 2GB instance**:
   - *Mitigation*: Gunicorn capped at 2 sync workers; 2 GB swap file provisioned before app deploy.
5. **Incomplete media transfer**:
   - *Mitigation*: Compare file count + total bytes old vs new, not just "transfer completed."
6. **No rollback path if old stack is torn down early**:
   - *Mitigation*: EB + RDS stay running, untouched, for minimum 5 days post-cutover regardless of how clean the migration looks.

---

## 📋 15-TASK EXECUTION CHECKLIST

### PHASE 1: PRE-CUTOVER SETUP (Zero Production Downtime, Zero Risk)

- [ ] **Task 1: Provision Lightsail Instance**
  - AWS Region: `ap-south-1` (Mumbai).
  - Blueprint: Ubuntu 24.04 LTS.
  - Plan: 2 GB RAM / 2 vCPU / 60 GB SSD / 3 TB Transfer ($12.00/mo bundle).
  - Attach a Static IP to the instance. Note: `<LIGHTSAIL_STATIC_IP>`.
  - Firewall: Open ports 22 (SSH), 80 (HTTP), 443 (HTTPS).

- [ ] **Task 2: OS Hardening, Swap & Package Installation**
  - Create 2 GB swap file (`/swapfile`, `chmod 600`, `mkswap`, `swapon`, `vm.swappiness=10`).
  - Configure UFW firewall (`ufw allow OpenSSH`, `ufw allow 'Nginx Full'`, `ufw enable`).
  - Install packages: Nginx, PostgreSQL 16, Redis 7, Python 3, python3-venv, Gunicorn, Certbot, python3-certbot-nginx.

- [ ] **Task 3: Codebase Deployment & Configuration**
  - Clone repo to `/var/www/propertism`.
  - Create Python virtualenv at `/var/www/propertism/venv` and install `requirements.txt`.
  - Configure local PostgreSQL 16:
    - Create `propertism_db` database and `propertism_user` user with strong password.
    - Bind strictly to `127.0.0.1:5432`.
  - Configure `/var/www/propertism/.env` pointing to local PostgreSQL and Redis (`127.0.0.1`).
  - Permissions: `chown -R www-data:www-data /var/www/propertism`.

- [ ] **Task 4: Initial Bootstrap, Gunicorn & SSL**
  - Run Django migrations on the empty DB: `python manage.py migrate`.
  - Collect static files: `python manage.py collectstatic --noinput`.
  - Create `/etc/systemd/system/gunicorn.service` (2 sync workers, bound to `/run/gunicorn.sock`).
  - Enable and start Gunicorn: `systemctl enable --now gunicorn`.
  - Configure Nginx reverse proxy to Gunicorn socket.
  - Issue Let's Encrypt SSL certificate via Certbot.
  - Confirm app responds with HTTP 200 on `http://127.0.0.1` and via workstation `hosts` override.

- [ ] **Task 5: Confirm GoDaddy DNS TTL is 300s**
  - Check `@` and `www` A records in GoDaddy DNS.
  - Ensure TTL is set to **300 seconds (5 minutes)** at least 24h prior to cutover.

---

### PHASE 2: CUTOVER EXECUTION (Scheduled Maintenance Window: ~20-30 Mins)

- [ ] **Task 6: Take Manual Safety Snapshot of RDS**
  - Trigger manual snapshot in AWS RDS Console or CLI: `propertism-rds-safety-pre-cutover`.
  - Confirm status reaches `available` before touching anything.

- [ ] **Task 7: Enumerate & Stop Every DB Writer**
  - Stop Gunicorn on Elastic Beanstalk (or set `MAINTENANCE_MODE=true` in EB environment).
  - Stop any background workers / celery / timers if active.
  - Connect to RDS as `postgres` and verify `pg_stat_activity`:
    ```sql
    SELECT pid, usename, client_addr, application_name, state 
    FROM pg_stat_activity 
    WHERE datname = 'propertism_db' AND pid <> pg_backend_pid();
    ```
  - Confirm **0 active application connections remain**.

- [ ] **Task 8: Dump & Direct Transfer (No S3 Round-Trip)**
  - Run `pg_dump`:
    ```bash
    pg_dump -h <RDS_ENDPOINT> -U postgres -d propertism_db -F c -b -v -f /tmp/propertism_cutover.dump
    ```
  - Confirm exit code is `0` and file size is `> 5 MB`.
  - `scp` directly to Lightsail:
    ```bash
    scp /tmp/propertism_cutover.dump ubuntu@<LIGHTSAIL_STATIC_IP>:/tmp/
    ```

- [ ] **Task 9: Restore on Lightsail & Reset Sequences**
  - Restore on Lightsail local PostgreSQL:
    ```bash
    pg_restore -U postgres -d propertism_db --clean --if-exists -v /tmp/propertism_cutover.dump
    ```
  - Reset all Django sequences using built-in command:
    ```bash
    cd /var/www/propertism
    ./venv/bin/python manage.py sqlsequencereset properties users chat | sudo -u postgres psql -d propertism_db
    ```

- [ ] **Task 10: Quick Parity & Media Verification**
  - Run sanity count checks in `psql -d propertism_db`:
    - `SELECT count(*) FROM properties_inquiry;` (Must match old DB, ~290).
    - `SELECT count(*) FROM properties_property;` (Must match old DB).
    - `SELECT count(*) FROM auth_user;` (Must match old DB).
    - Eye-ball latest 3 inquiries to ensure data integrity.
  - Sync media directly:
    ```bash
    rsync -avz /path/to/media/ ubuntu@<LIGHTSAIL_STATIC_IP>:/var/www/propertism/media/
    ```
  - Compare file counts and total directory bytes (`du -sh /var/www/propertism/media`).

- [ ] **Task 11: Application Smoke Checks on Lightsail**
  - Log into Django Admin (`/admin/`).
  - Submit a test inquiry on the website (via hosts override or direct IP).
  - Verify email alert and WhatsApp notification dispatch.
  - Confirm test inquiry appears in database and admin dashboard.

---

### PHASE 3: GO-LIVE & COOLDOWN

- [ ] **Task 12: Flip GoDaddy DNS**
  - Update GoDaddy `@` and `www` A records to `<LIGHTSAIL_STATIC_IP>`.
  - Delete any legacy IPv6 (AAAA) records pointing to old EB/CloudFront if present.

- [ ] **Task 13: Confirm Propagation & Live Traffic**
  - Check propagation: `dig +short propertism.in @8.8.8.8` and `dig +short propertism.in @1.1.1.1`.
  - Monitor `/var/log/nginx/access.log` on Lightsail to confirm live organic traffic is hitting the new server.

- [ ] **Task 14: 5-Day Standby Cooldown (The Real Rollback Net)**
  - **Do NOT delete or decommission Elastic Beanstalk or RDS.**
  - Leave both running untouched and idle for **minimum 5 days**.
  - If any critical issue emerges, rollback is trivial: point GoDaddy DNS back to EB/CloudFront.

- [ ] **Task 15: Decommission Legacy Infrastructure**
  - After 5 completely clean operational days:
    - Terminate Elastic Beanstalk environment.
    - Delete RDS instance (with final snapshot retained).
    - Monthly spend drops to **$12.00/month**.
