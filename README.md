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

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Useful local URLs:

- Site: `http://localhost:8000/en/`
- Admin: `http://localhost:8000/en/admin/`

## Important Paths

- Session notes: `.session-tracker/SESSION_TRACKER.md`
- Deployment notes: `propertism-last-deployment-notes-29032026.md`
- Deployment scripts: `scripts/`
- Project docs: `documents/`

## Working Rule

Do not treat historical `realtor-web/` paths as current deploy paths.
For current work, use this repository root as the source of truth unless a newer session note explicitly says otherwise.
