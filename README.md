# Propertism

Propertism Realty Advisors LLP website and admin, built with Django.

## Current Layout

As of April 1, 2026, the active app source lives directly at the repository root.

```text
01propertism/
|-- manage.py
|-- realtor_project/
|-- content/
|-- properties/
|-- uilayers/
|-- static/
|-- media/
|-- scripts/
|-- documents/
`-- .session-tracker/
```

Historical notes may still mention `realtor-web/` because that was the real app folder before the repo was flattened.

## Local Development

Run from the repository root:

```powershell
.\scripts\django.cmd check
.\scripts\django.cmd migrate
.\scripts\django.cmd runserver
```

This wrapper is the preferred local entry point on this machine.
It pins the known-good interpreter at `C:\Python\python.exe` and prepends `C:\Python\django` to `PATH` so Django starts without rediscovering the runtime each session.
The matching `scripts/django.ps1` is still available, but `scripts/django.cmd` avoids PowerShell execution-policy friction.

Useful local URLs:

- Site: `http://localhost:8000/en/`
- Admin: `http://localhost:8000/en/admin/`

## Optional Local PostgreSQL

Local development still falls back to SQLite by default, but you can now point it at PostgreSQL through `.env` if you want a setup closer to production.

1. Copy `.env.example` to `.env`
2. Uncomment either the `POSTGRES_*` variables or `DATABASE_URL`
3. Run:

```powershell
.\scripts\django.cmd migrate
.\scripts\django.cmd runserver
```

If those PostgreSQL variables are absent, Django will keep using SQLite automatically.

## Important Paths

- Session notes: `.session-tracker/SESSION_TRACKER.md`
- Deployment notes: `propertism-last-deployment-notes-29032026.md`
- Deployment scripts: `scripts/`
- Project docs: `documents/`

## Working Rule

Do not treat historical `realtor-web/` paths as current deploy paths.
For current work, use this repository root as the source of truth unless a newer session note explicitly says otherwise.
