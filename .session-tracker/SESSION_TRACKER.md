# Propertism - Session Tracker

---

## File Metadata

**Last Updated By**: Amazon Q
**Last Updated On**: April 10, 2026 at 22:15 IST
**Last Update**: SESSION 20 - full production deploy to us-east-1, redirect loop fix, static files fix, admin credentials reset. Site fully live.

---

## Project Overview

**Project:** Propertism Realty Advisors LLP - NRI Property Management Website
**Domain:** propertism.in (GoDaddy)
**Site:** https://www.propertism.in/
**Admin:** https://www.propertism.in/admin/ — `admin / admin123`
**GitHub:** https://github.com/Propertism/propertism (branch: main)
**Latest Commit:** d3feee9

---

## Live Infrastructure (Current - us-east-1)

> Note: Original deployment was us-west-2. Migrated to us-east-1 for lower AWS cost.

### AWS Elastic Beanstalk
- **Application:** propertism-2026
- **Environment:** propertism-prod-2026
- **Region:** us-east-1
- **Platform:** Python 3.11 on Amazon Linux 2023
- **CNAME:** propertism-prod-2026.us-east-1.elasticbeanstalk.com
- **Health:** Green / Ready
- **Latest Deployed Version:** app-d3fe-260410-admin-reset

### CloudFront
- **Distribution ID:** E1GGPU208SQFFT
- **Domain:** d1yv5od4i0bho.cloudfront.net
- **Aliases:** propertism.in, www.propertism.in
- **Origin:** propertism-prod-2026.us-east-1.elasticbeanstalk.com (HTTP only)
- **Origin Request Policy:** AllViewer (forwards all headers)
- **SSL:** Handled by CloudFront — Django must NOT set ENABLE_HTTPS=True

### Database
- **Type:** PostgreSQL on RDS
- **Instance:** propertism-prod-pg (us-east-1)
- **Connection:** via DATABASE_URL env var in EB
- **Password:** stored in AWS Secrets Manager — secret: `propertism/prod/rds-password`
- **SSL Mode:** require

### DNS (GoDaddy)
- CNAME: propertism.in → d1yv5od4i0bho.cloudfront.net
- CNAME: www.propertism.in → d1yv5od4i0bho.cloudfront.net

### SSL Certificate (ACM - us-east-1)
- **Status:** Issued
- **Domains:** propertism.in, www.propertism.in
- **Attached to:** CloudFront distribution

---

## EB Environment Variables (Current)

| Variable | Value |
|---|---|
| DJANGO_SETTINGS_MODULE | realtor_project.settings |
| DJANGO_ALLOWED_HOSTS | propertism.in,www.propertism.in,propertism-prod-2026.us-east-1.elasticbeanstalk.com |
| CANONICAL_HOST | www.propertism.in |
| CANONICAL_SCHEME | https |
| CANONICAL_REDIRECT_HOSTS | propertism.in |
| CANONICAL_SCHEME | https |
| DEBUG | False |
| ENABLE_HTTPS | False (CloudFront handles HTTPS — must stay False) |
| DATABASE_URL | postgresql://...@propertism-db-2026...rds.amazonaws.com:5432/propertismdb |
| POSTGRES_SSLMODE | require |
| CSRF_TRUSTED_ORIGINS | https://propertism.in,https://www.propertism.in,https://propertism-prod-2026.us-east-1.elasticbeanstalk.com |
| DJANGO_SECRET_KEY | (set) |
| PYTHONPATH | /var/app/current:$PYTHONPATH |

> ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD are removed after use. Set them temporarily to reset admin credentials, then remove.

---

## Local Development

```powershell
# Run from repo root
.\scripts\django.cmd check
.\scripts\django.cmd migrate
.\scripts\django.cmd runserver
```

- Python: `C:\Python\python.exe` (requires `C:\Python\django` on PATH for python313.dll)
- Local DB: SQLite fallback when no POSTGRES_* or DATABASE_URL env vars set
- Optional local PostgreSQL: copy `.env.example` to `.env` and fill in POSTGRES_* vars

Local URLs:
- Site: http://localhost:8000/
- Admin: http://localhost:8000/admin/

---

## Deploy to Production

```powershell
cd d:\viji\viji-olivine\03rolledout\01propertism
git add .
git commit -m "your message"
git push origin main
eb deploy propertism-prod-2026 --label "app-XXXX-YYMMDD-description"
```

Deploy runs automatically:
1. `collectstatic --noinput --clear`
2. `migrate` (leader only)
3. `create_or_reset_prod_superuser` (only if ADMIN_* env vars are set)
4. Postdeploy hooks: collectstatic to /var/app/current, db permissions, bootstrap if empty, repair reviews

**Data safety rule:** Normal deploys are code-only. Never seed or restore live data unless user explicitly says `deploy +seed`.

---

## Admin Credentials Reset Procedure

1. Set EB env vars: `ADMIN_USERNAME=admin`, `ADMIN_EMAIL=admin@propertism.in`, `ADMIN_PASSWORD=<new>`
2. Run `eb deploy propertism-prod-2026`
3. Confirm log shows `updated / admin`
4. Remove the three ADMIN_* env vars from EB immediately after

---

## Repository Layout

```
01propertism/               ← repo root (source of truth since April 1, 2026)
├── manage.py
├── Procfile
├── realtor_project/        ← Django project settings, urls, wsgi
├── content/                ← CompanyInfo, middleware, homepage models
├── properties/             ← Property model, currency, pricing
├── uilayers/               ← templates, views
├── users/
├── search/
├── chat/
├── static/                 ← CSS, JS, images
├── media/                  ← hero, properties, team images
├── scripts/                ← django.cmd, django.ps1, create_or_reset_prod_superuser.py
├── .ebextensions/          ← EB config (01_django.config, 02_packages.config)
├── .platform/hooks/postdeploy/  ← 00_collectstatic, 01_fix_db_permissions, 02_bootstrap, 03_repair_reviews
├── .elasticbeanstalk/      ← config.yml (app: propertism-2026, env: propertism-prod-2026, region: us-east-1)
└── .session-tracker/       ← this file
```

> Old sessions referenced `realtor-web/` — that was the pre-April-1 layout. Ignore those paths.

---

## Key Files

| File | Purpose |
|---|---|
| `realtor_project/settings.py` | Main Django settings. DB selection, CANONICAL_HOST, ENABLE_HTTPS guard |
| `realtor_project/urls.py` | URL routing including favicon redirect |
| `content/middleware.py` | HealthCheckMiddleware + CanonicalDomainRedirectMiddleware |
| `content/management/commands/createsu.py` | Creates admin user if none exists |
| `scripts/create_or_reset_prod_superuser.py` | Creates or resets admin user (used by postdeploy hook when ADMIN_* vars set) |
| `.ebextensions/01_django.config` | WSGI path, static file mapping, container commands |
| `.platform/hooks/postdeploy/00_collectstatic_current.sh` | Runs collectstatic into /var/app/current after deploy |
| `.platform/hooks/postdeploy/01_fix_db_permissions.sh` | Media permissions + admin user reset if ADMIN_* vars present |
| `.platform/hooks/postdeploy/02_bootstrap_if_db_looks_empty.sh` | Repopulates content if DB is empty after instance replacement |
| `uilayers/templates/home-premium.html` | Homepage template |
| `uilayers/templates/base.html` | Shared base template (favicon, chat widget) |
| `static/css/propertism-styles.css` | Main stylesheet |
| `static/css/premium-styles.css` | Premium layout styles |
| `static/css/mobile-layout.css` | Mobile overrides |

---

## Homepage Section Order (Approved)

1. home-section (hero)
2. services-section
3. about-section (full description + mission from CompanyInfo)
4. management-section
5. reviews-section (carousel, 3 cards per slide, dot indicators)
6. properties-section (featured properties)
7. blog-section
8. contact-section (quote form + world clock for US/UK/India/Middle East)

---

## Brand Identity

- **Company:** Propertism Realty Advisors LLP
- **Focus:** NRI Property Management in Chennai
- **Primary Color:** Navy Blue `#0F172A`
- **Accent Color:** Gold `#B89A4A`
- **Logo assets:** `static/images/propertism-logo-tm.png`, `propertism-logo-white-tm.png`

---

## Known Operational Notes

1. **ENABLE_HTTPS must stay False** — CloudFront terminates HTTPS and forwards to EB over HTTP. Setting ENABLE_HTTPS=True causes an infinite redirect loop (Django redirects to HTTPS → CloudFront serves HTTP to EB → loop).

2. **Static files need a full eb deploy after env-var-only changes** — Env-var updates restart the instance without running postdeploy hooks, leaving staticfiles/ empty. Always follow env-var changes with a code deploy.

3. **ADMIN_* vars must be passed explicitly in sudo env** — The postdeploy hook sources `/opt/elasticbeanstalk/deployment/env` but `sudo -u webapp env` only forwards vars listed explicitly. ADMIN_USERNAME/EMAIL/PASSWORD must be in the env list in `01_fix_db_permissions.sh`.

4. **PostgreSQL replaced SQLite** — Old sessions mention SQLite at `/var/app/data/db.sqlite3`. That is gone. Production now uses RDS PostgreSQL. SQLite is only the local dev fallback.

5. **GitHub auth** — Push requires the `Propertism` org account. If push fails with `denied to vijaympgs`, clear the cached Windows credential for github.com and re-authenticate with the correct account.

6. **Media files travel with the repo** — `/media/` is committed and deployed via git/EB bundle. Production serves media from `/var/app/current/media/`.

---

## Session History Summary

| Session | Date | Key Work | Status |
|---|---|---|---|
| 1 | Mar 7 | Repo setup, file cleanup | ✅ |
| 2 | Mar 7 | Initial EB deploy to us-west-2 | ✅ |
| 3 | Mar 7 | DB init, createsu command | ✅ |
| 4 | Mar 7 | Custom domain propertism.in, GoDaddy DNS | ✅ |
| 5 | Mar 7 | Django admin branding (navy/gold) | ✅ |
| 6 | Mar 7 | DB persistence, logo column fix | ✅ |
| 7 | Mar 7 | Media files deployment | ✅ |
| 8 | Mar 7 | Nginx upload limit 20MB | ✅ |
| 9 | Mar 7 | Removed /en/ language prefix from URLs | ✅ |
| 10 | Mar 7 | Static files fix, 502 fix, HTTPS cert issued, vijim.ai integration | ✅ |
| 11 | Mar 7 | HTTPS listener, LB health check middleware, port 443 open | ✅ |
| 12 | Mar | Hero rotation (5 images), review carousel — held for team confirmation | ✅ |
| 13 | Mar 29 | Production recovery, mobile fixes, chat restore, GitHub resync | ✅ |
| 14 | Mar 31 | Hero layout, trust strip, nav reorder | ✅ |
| 15 | Apr 1 | Production guardrails, property currency (INR/USD), property UX, logo assets | ✅ |
| 16 | Apr 3 | RCA, PostgreSQL cutover (RDS), static postdeploy hook, Procfile, local PG support | ✅ |
| 17 | Apr 3 | Favicon fix (base.html + urls.py redirect) | ✅ |
| 18 | Apr 3 | Homepage section reorder, About expansion, property media restore | ✅ |
| 19 | Apr 3 | Alternate section backgrounds, spacing tightening, world clock in footer | ✅ |
| 20 | Apr 10 | **Full deploy to us-east-1 (cost migration). Fixed redirect loop, static 404s, admin credentials. Site fully live.** | ✅ |

---

## Session 20 Detail — April 10, 2026

**Primary Goal:** Deploy all Session 19 changes to production and confirm admin access.

**Issues Found And Fixed:**

| Issue | Root Cause | Fix |
|---|---|---|
| Infinite redirect loop on https://www.propertism.in/ | `ENABLE_HTTPS=True` in EB env → Django SECURE_SSL_REDIRECT=True → CloudFront forwards HTTP to EB → loop | Set `ENABLE_HTTPS=False` via `aws elasticbeanstalk update-environment` |
| All static files 404 after env-var update | Env-var-only update restarted instance without running postdeploy hooks → staticfiles/ empty | Full `eb deploy` to trigger postdeploy hooks and run collectstatic |
| Admin login failing (wrong password) | `ADMIN_*` vars not forwarded through `sudo -u webapp env` in postdeploy hook | Added `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` explicitly to the sudo env call in `01_fix_db_permissions.sh` |

**Deployments:**
1. `app-bb07-260410-session19-final` — initial deploy, triggered redirect loop
2. `app-bb07-260410-static-fix` — after ENABLE_HTTPS fix, restored static files
3. `app-d3fe-260410-admin-reset` — after hook fix, confirmed `updated / admin` in logs

**Final State:**
- https://www.propertism.in/ → 200 OK
- https://www.propertism.in/admin/ → 302 → login (correct)
- All static assets → 200 OK
- Admin login: `admin / admin123` ✅
- ADMIN_* env vars removed from EB after reset ✅
- Git: `d3feee9 Fix postdeploy hook to pass ADMIN_* vars to superuser script`

---

## Next Session Start Checklist

1. `git status` — confirm clean
2. `.\scripts\django.cmd check` — confirm no issues
3. Smoke test: https://www.propertism.in/ and https://www.propertism.in/admin/
4. Check EB health: `eb status propertism-prod-2026`


Quick recap of what's stable going into the next session:

Site live at https://www.propertism.in/ — Green, all static assets loading

Admin working at /admin/ with admin / admin123

PostgreSQL on RDS — no more SQLite instance-loss risk

CloudFront handling HTTPS — ENABLE_HTTPS stays False permanently

Session tracker is clean and current