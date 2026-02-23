# Realtor Monorepo

Production codebase for Realtor with Django backend, React web app, and Expo React Native mobile app.

## Repository Layout

```text
realtor/
|-- package.json
|-- scripts/
|-- shared/
|   |-- services/
|   |-- types/
|   `-- utils/
|-- realtor-web/
|   |-- manage.py
|   |-- requirements.txt
|   |-- realtor_project/
|   |-- properties/
|   |-- users/
|   |-- search/
|   |-- middleware/
|   |-- documents/
|   |-- plans-and-docs/
|   `-- uilayers/
|       |-- package.json
|       `-- src/
`-- realtor-mobile/
    |-- app/
    |   |-- _layout.tsx
    |   |-- (tabs)/
    |   |   |-- _layout.tsx
    |   |   |-- index.tsx
    |   |   |-- profile.tsx
    |   |   |-- search/index.tsx
    |   |   `-- properties/index.tsx
    |   `-- (auth)/
    |       |-- _layout.tsx
    |       |-- login.tsx
    |       `-- register.tsx
    |-- src/
    |   |-- modules/
    |   |   |-- properties/
    |   |   |-- users/
    |   |   |-- search/
    |   |   `-- shared/
    |   |-- components/
    |   |-- hooks/
    |   |-- services/api.ts
    |   |-- store/
    |   |-- utils/
    |   |-- constants/
    |   `-- types/
    |-- assets/
    |-- docs/
    |-- middleware.ts
    |-- metro.config.js
    |-- tailwind.config.js
    `-- tsconfig.json
```

## Workspaces

Root `package.json` workspaces:
- `realtor-web/uilayers`
- `realtor-mobile`

## Prerequisites

- Node.js 18+
- Yarn 1.x
- Python 3.10+
- pip

## Setup

```bash
# From repo root
cd realtor
yarn install

# Django dependencies
cd realtor-web
pip install -r requirements.txt
```

## Backend Setup (Django)

```bash
cd realtor-web
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend runs at `http://localhost:8000`.

## Run Web + Mobile

```bash
# From repo root
cd realtor
yarn dev
```

- Web (Vite): `http://localhost:5173`
- Mobile (Expo): starts via Expo CLI (QR in terminal)

You can also run individually:

```bash
yarn web:dev
yarn mobile:dev
```

## API Notes

- Web and mobile should call Django endpoints under `/api/`.
- Mobile API client lives at `realtor-mobile/src/services/api.ts`.
- Update API base URLs for local device testing (Android emulator/iOS simulator/physical device).

## Current Status

- Monorepo split is in place: `realtor-web` + `realtor-mobile`.
- Mobile route scaffold is created with Expo Router tabs/auth groups.
- Module folders are created for `properties`, `users`, and `search`.
