# Propertism - Session Tracker

---

## File Metadata

**Last Updated By**: Antigravity (Astra)
**Last Updated On**: May 02, 2026 (Midday)
**Last Update**: SESSION 29 - SOCIAL ARCHITECTURE UNIFICATION. Astra unified the social media architecture for Propertism by transitioning from hardcoded links to a dynamic, model-driven system surgically restricted to the Contact Section. Added Instagram, WhatsApp, and YouTube fields to the CompanyInfo model and updated the Contact UI to be fully dynamic.

---

## Project Overview

**Project:** Propertism Realty Advisors LLP - NRI Property Management Website
**Domain:** propertism.in (GoDaddy)
**Site:** https://www.propertism.in/
**Admin:** https://www.propertism.in/admin/ — `admin / admin123`
**GitHub:** https://github.com/Propertism/propertism (branch: main)
**Latest Commit:** 288d3f7

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
# Run from repo root
git add .
git commit -m "your message"
git push origin main
```

GitHub Actions auto-deploys on every push to `main`. No manual `eb deploy` needed.

### CI/CD
- **Workflow:** `.github/workflows/deploy.yml`
- **IAM User:** `github-actions-propertism` (policy: `AdministratorAccess-AWSElasticBeanstalk`)
- **GitHub Secrets:** `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- **Monitor:** https://github.com/Propertism/propertism/actions

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
3. Confirm log shows `updated / admin` in logs
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

2. **Static files need a full eb deploy after env-var-only changes** — Env-var updates restart the instance without running postdeploy hooks. This is now mitigated by `collectstatic` running in the Procfile before gunicorn on every startup. No manual intervention needed.

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
| 20 | Apr 10 | Full deploy to us-east-1 (cost migration). Fixed redirect loop, static 404s, admin credentials. Site fully live. | ✅ |
| 21 | Apr 10 | Emergency static restore. Permanent fix: collectstatic in Procfile before gunicorn. | ✅ |
| 22 | Apr 11 | **GitHub Actions CI/CD. Every push to main auto-deploys to propertism-prod-2026. IAM user: github-actions-propertism.** | ✅ |
| 23 | Apr 16 | Hero + property images fix. media/ in bundle. Nginx location blocks. | ✅ |
| 24 | Apr 26 | **UI Stabilization & Messaging Refresh. Viewport normalization (100vh fit), centered section headers with 2-line wrap tuning, and footer contact block hardening. Diagnosed media persistence for S3 migration.** | ✅ |
| 25 | Apr 30 | **Homepage polish checkpoint. Section kicker iconography/sizing, About + Contact single-line desktop titles with mobile fallback.** | ✅ |
| 26 | Apr 30 | **PROPERTISM V4 MIGRATION. Full-platform refactor into modular, sharp-grid editorial system.** | ✅ |
| 27 | May 01 | **Hardening Section Typography Unification. Strict V4 typography standards across Management, Reviews, and Insights.** | ✅ |
| 28 | May 01 | **MOBILE V4 STABILIZATION. Normalized global section padding to 24px and hardened editorial stacking.** | ✅ |
| 29 | May 02 | **SOCIAL ARCHITECTURE UNIFICATION. Unified social media architecture via dynamic, model-driven system for Contact Section.** | ✅ |

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

## Session 21 Detail — April 10, 2026

**Trigger:** Site broken immediately after Session 20 — static files 404 again.

**Root Cause:** Removing `ADMIN_*` env vars (cleanup step) restarted the EB instance without running postdeploy hooks → `staticfiles/` empty.

**Immediate Fix:** Full `eb deploy` to trigger postdeploy hooks → `app-d3fe-260410-static-restore`.

**Permanent Fix:** Added `collectstatic --noinput --clear` to `Procfile` before gunicorn:
```
web: python manage.py collectstatic --noinput --clear && gunicorn ...
```
Now runs on every startup — full deploy, env-var restart, instance replacement, or scaling event.

**Commits:**
- `ed83870 Run collectstatic on every startup to survive env-var restarts`

**Deployed:** `app-ed83-260410-procfile-collectstatic`

**Rule added to operational notes:** Any env-var change in EB will restart the instance. Always follow with a full `eb deploy` OR rely on the Procfile collectstatic (now permanent).

---

## Session 24 Detail — April 26, 2026

**Primary Goal:** UI Stabilization, Viewport Hardening, and Messaging Consistency.

**Key Achievements:**

1. **Viewport Normalization**:
   - Created `static/css/viewport-section-normalization.css` to centralize all layout hardening.
   - Removed legacy viewport wrappers (`.hero-viewport-group`) to restore natural scroll flow.
   - Enforced exact `calc(100vh - 130px)` height for Hero to share viewport with 130px Trust Strip.
   - Normalized section density to `1rem` vertical padding for professional vertical rhythm.

2. **Messaging & Alignment Refresh**:
   - Updated About, Management, and Insights sections with authoritative, centered messaging.
   - Implemented `.section-title-centered` and `.section-desc-centered` utility classes.
   - Tuned `max-width` (35ch / 85ch) to force clean 2-line wrapping for primary headlines.
   - Hardcoded specific copy in templates to guarantee visibility regardless of CMS state.

3. **Footer Hardening**:
   - Restyled the office contact block with high-precision typographic weights.
   - Line-1 (Address): Bold `gray-900`.
   - Line-2 (Street): Muted secondary.
   - City Line: Bold `brand-gold`.
   - Phones/Email: Bold brand navy/gold with tight vertical rhythm (`gap: 0.1rem`).

4. **Infrastructure Audit (Media Persistence)**:
   - Identified that property images are lost on CI/CD deploys because they are stored on ephemeral EC2 disk.
   - Verified that `settings_production.py` is ready for S3; user must set `AWS_MEDIA_BUCKET_NAME` and keys in EB to activate.

**Final State:**
- Home Section: Perfectly fits 1 viewport (Hero + Trust Strip) ✅
- All Section Headers: Centered, 2-line wrap ✅
- Footer Contact: High-precision bold/muted treatment ✅
- Media: Audit complete; S3 path confirmed ✅

---

## Next Session Start Checklist

1. `git status` — confirm clean
2. `.\scripts\django.cmd check` — confirm no issues
3. Smoke test: https://www.propertism.in/ and https://www.propertism.in/admin/
4. Check EB health: `eb status propertism-prod-2026`
5. Verify section centering across all break-points (Mobile/Desktop).

Quick recap of what's stable going into the next session:

Site live at https://www.propertism.in/ — Green, viewport stabilized.

Messaging hardcoded for consistency across About/Management/Insights.

Viewport normalization file active and overriding legacy scroll-jacking.

Session tracker is clean and current (Astra Handover).

---

## Session 25 Checkpoint — April 30, 2026

**Status:** Awaiting git push and production verification.

**Work Completed In This Checkpoint:**
- Increased and iconized homepage section kickers for Services, Management, Reviews, Featured Properties, Insights, About, and Contact.
- Tuned kicker spacing for Management and Insights.
- Tightened the Featured Properties CTA spacing.
- Forced the long About and Contact titles into a desktop single-line / mobile wrapped split.
- Refined the lower footer presence band with improved world clock, reach, and office-hours presentation.
- Created `codex-session-3004.md` as the active handoff note.

**Validation:**
- `python manage.py check` passed locally.

**Next Action:**
- User will push current changes, check production, and return for either final wind-down or one more polish pass.
