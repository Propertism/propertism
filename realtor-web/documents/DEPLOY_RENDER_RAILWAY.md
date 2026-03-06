# Propertism Django Deploy Guide

This guide is for the Django app in `realtor-web/`.

Verified against the current platform docs on March 6, 2026:
- Render Django deploy docs: `https://render.com/docs/deploy-django`
- Render monorepo support: `https://render.com/docs/monorepo-support`
- Railway Django guide: `https://docs.railway.com/guides/django`
- Railway monorepo docs: `https://docs.railway.com/deployments/monorepo`
- Railway config-as-code docs: `https://docs.railway.com/config-as-code`
- Railway volumes docs: `https://docs.railway.com/guides/volumes`

## Scope

This repository is not using Docker for deployment in this guide.

Use these repo-specific settings:
- Service root directory: `realtor-web`
- Settings module: `realtor_project.settings_production`
- Build command: `pip install -r requirements-production.txt && python manage.py collectstatic --noinput`
- Start command: `gunicorn realtor_project.wsgi:application --bind 0.0.0.0:$PORT`
- Health check path: `/en/`

Use a PostgreSQL database for production.

## Important Project Notes

Before deploying, note these project-specific constraints:

1. `manage.py` and `wsgi.py` default to `realtor_project.settings`, not `realtor_project.settings_production`.
Set `DJANGO_SETTINGS_MODULE=realtor_project.settings_production` on the platform.

2. `settings_production.py` uses `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.
It does not read `DATABASE_URL` directly.

3. The current production cache backend expects Redis via `REDIS_URL`.
If you skip Redis, the app can still boot, but any cache-dependent code will fail when it tries to connect.

4. User-uploaded files go to `realtor-web/media`.
Both Render and Railway use ephemeral filesystem storage by default, so do not rely on local media storage for production uploads unless you add persistent storage or object storage.

## Required Environment Variables

Set these on both Render and Railway:

| Variable | Required | Example |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | Yes | `realtor_project.settings_production` |
| `DJANGO_SECRET_KEY` | Yes | A long random Django secret |
| `DJANGO_ALLOWED_HOSTS` | Yes | `your-app.onrender.com,www.example.com` |
| `CORS_ALLOWED_ORIGINS` | Yes | `https://your-app.onrender.com,https://www.example.com` |
| `DB_NAME` | Yes | `propertism` |
| `DB_USER` | Yes | `propertism_user` |
| `DB_PASSWORD` | Yes | `...` |
| `DB_HOST` | Yes | Database host from the platform |
| `DB_PORT` | Yes | `5432` |
| `REDIS_URL` | Recommended | Redis connection URL |
| `ADMIN_EMAIL` | Recommended | `admin@propertism.com` |
| `EMAIL_HOST` | Optional | `smtp.gmail.com` |
| `EMAIL_PORT` | Optional | `587` |
| `EMAIL_HOST_USER` | Optional | SMTP username |
| `EMAIL_HOST_PASSWORD` | Optional | SMTP password or app password |
| `DEFAULT_FROM_EMAIL` | Optional | `noreply@propertism.com` |
| `SERVER_EMAIL` | Optional | `server@propertism.com` |
| `ADMIN_URL` | Optional | `secure-admin-panel` |

## Render

## 1. Create the PostgreSQL database

In Render:

1. Create a PostgreSQL service first.
2. Open the database details page.
3. Copy the database name, user, password, host, and port.
4. Use those values to populate `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` in the web service.

If you want cache support, add a Redis service and copy its connection URL into `REDIS_URL`.

## 2. Create the web service

In Render:

1. Click `New +`.
2. Choose `Web Service`.
3. Select the GitHub repo `Propertism/propertism`.
4. Branch: `main`.
5. Root Directory: `realtor-web`.
6. Runtime: `Python 3`.
7. Recommended Build Filter include path: `realtor-web/**`.

Use these commands:

```bash
Build Command:
pip install -r requirements-production.txt && python manage.py collectstatic --noinput

Start Command:
gunicorn realtor_project.wsgi:application --bind 0.0.0.0:$PORT
```

Set the health check path to:

```text
/en/
```

## 3. Add environment variables

Minimum recommended values:

```text
DJANGO_SETTINGS_MODULE=realtor_project.settings_production
DJANGO_SECRET_KEY=<generate-a-new-secret>
DJANGO_ALLOWED_HOSTS=<your-service>.onrender.com
CORS_ALLOWED_ORIGINS=https://<your-service>.onrender.com
DB_NAME=<from-render-postgres>
DB_USER=<from-render-postgres>
DB_PASSWORD=<from-render-postgres>
DB_HOST=<from-render-postgres>
DB_PORT=<from-render-postgres>
REDIS_URL=<from-render-redis-optional>
```

If you later add a custom domain, append it to:
- `DJANGO_ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`

## 4. Run migrations

Preferred:

- Use Render's pre-deploy command if your service plan supports it:

```bash
python manage.py migrate
```

Fallback:

- Open the Render shell after the first successful deploy and run:

```bash
python manage.py migrate
python manage.py createsuperuser
```

If you must run migrations during build, append `&& python manage.py migrate` to the build command, but a pre-deploy or manual migration step is cleaner.

## 5. Verify

Check:

1. `https://<your-service>.onrender.com/en/`
2. `https://<your-service>.onrender.com/en/admin/` or your custom `ADMIN_URL`
3. Static files load correctly.
4. Contact form submissions work.

## Railway

## 1. Create the project and database

In Railway:

1. Create a new project from the GitHub repo `Propertism/propertism`.
2. Add a PostgreSQL service.
3. Optional but recommended: add a Redis service.

Railway exposes PostgreSQL values as service variables such as:
- `PGDATABASE`
- `PGUSER`
- `PGPASSWORD`
- `PGHOST`
- `PGPORT`

## 2. Configure the web service

For the Django service:

1. Set Root Directory to `realtor-web`.
2. Set the Start Command explicitly.
3. Generate a public domain from the `Networking` tab.
4. Recommended Watch Path: `realtor-web/**`.

Use:

```bash
Start Command:
gunicorn realtor_project.wsgi:application --bind 0.0.0.0:$PORT
```

For builds, Railway's Python buildpack/Nixpacks should detect the service automatically, but for this repo the safer explicit build command is:

```bash
pip install -r requirements-production.txt && python manage.py collectstatic --noinput
```

If your Railway service exposes separate build and deploy hooks, use `python manage.py migrate` as the pre-deploy command.

## 3. Add environment variables

Set these variables on the Django service:

```text
DJANGO_SETTINGS_MODULE=realtor_project.settings_production
DJANGO_SECRET_KEY=<generate-a-new-secret>
DJANGO_ALLOWED_HOSTS=<your-service>.up.railway.app
CORS_ALLOWED_ORIGINS=https://<your-service>.up.railway.app
DB_NAME=${{Postgres.PGDATABASE}}
DB_USER=${{Postgres.PGUSER}}
DB_PASSWORD=${{Postgres.PGPASSWORD}}
DB_HOST=${{Postgres.PGHOST}}
DB_PORT=${{Postgres.PGPORT}}
REDIS_URL=${{Redis.REDIS_URL}}
```

If you are not attaching Redis, remove `REDIS_URL` from the example, but keep in mind the current production cache backend expects it.

If you later add a custom domain, append it to:
- `DJANGO_ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`

## 4. Run migrations

Preferred:

```bash
python manage.py migrate
```

Then create the first admin user:

```bash
python manage.py createsuperuser
```

You can run both through Railway's shell/CLI or a pre-deploy command.

## 5. Verify

Check:

1. `https://<your-service>.up.railway.app/en/`
2. `https://<your-service>.up.railway.app/en/admin/` or your custom `ADMIN_URL`
3. Static files load correctly.
4. Database-backed pages work after migrations.

## Post-Deploy Checklist

Use this for both platforms:

1. Home page loads at `/en/`.
2. Admin login works.
3. `Company Information` content is visible on the site.
4. `python manage.py migrate` has completed successfully.
5. `python manage.py createsuperuser` has been run.
6. Contact form creates `Contact Inquiry` rows in admin.
7. `DJANGO_ALLOWED_HOSTS` includes every live hostname.
8. `CORS_ALLOWED_ORIGINS` includes every frontend origin that will call this backend.
9. Email settings are configured if the project will send email in production.
10. Media persistence is addressed before enabling real uploads.

## Recommended Values For This Repo

Use these first:

```text
ADMIN_URL=secure-admin-panel
ADMIN_EMAIL=admin@propertism.com
DEFAULT_FROM_EMAIL=noreply@propertism.com
SERVER_EMAIL=server@propertism.com
```

## Troubleshooting

### App boots with development settings

Cause:
- `DJANGO_SETTINGS_MODULE` was not set.

Fix:

```text
DJANGO_SETTINGS_MODULE=realtor_project.settings_production
```

### Database connection error on startup

Cause:
- One or more of `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` is missing or wrong.

Fix:
- Re-copy the values from the platform database service.
- Do not assume `DATABASE_URL` is enough for this codebase.

### Static files missing

Cause:
- `collectstatic` did not run in the build.

Fix:

```bash
python manage.py collectstatic --noinput
```

### Cache or Redis errors

Cause:
- `REDIS_URL` is unset and code hits the Redis cache backend.

Fix:
- Add a Redis service and set `REDIS_URL`.

### Uploads disappear after redeploy

Cause:
- Media is stored on ephemeral disk.

Fix:
- Add persistent storage or move media to object storage.
