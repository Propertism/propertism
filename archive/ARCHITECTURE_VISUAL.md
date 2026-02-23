# Architecture Visual Guide

## 🎯 The Big Picture

```
                    CHENNAI REALTOR PLATFORM
                    ========================

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    DJANGO BACKEND (Port 8000)                   │
│                    Single Source of Truth                       │
│                                                                 │
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │                          │  │                          │   │
│  │      REST APIs           │  │    Web Frontend          │   │
│  │      =========           │  │    =============         │   │
│  │                          │  │                          │   │
│  │  /api/properties/        │  │  /en/                    │   │
│  │  /api/users/             │  │  /en/properties/         │   │
│  │  /api/search/            │  │  /en/about/              │   │
│  │  /api/auth/              │  │  /en/contact/            │   │
│  │                          │  │  /en/admin/              │   │
│  │  Returns JSON            │  │  Returns HTML            │   │
│  │                          │  │                          │   │
│  └──────────────────────────┘  └──────────────────────────┘   │
│                                                                 │
│  Database: SQLite (dev) / PostgreSQL (prod)                    │
│  Static Files: /static/dist/ (React build output)              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                    ▲                           ▲
                    │                           │
                    │                           │
        ┌───────────┴──────────┐    ┌──────────┴──────────┐
        │                      │    │                     │
        │                      │    │                     │
┌───────▼────────┐    ┌────────▼────────┐    ┌───────────▼────────┐
│                │    │                 │    │                    │
│  React Native  │    │  React Web PWA  │    │   Web Browsers     │
│  Mobile App    │    │  (Development)  │    │   (Production)     │
│                │    │                 │    │                    │
│  iOS/Android   │    │  Port 5173      │    │   Port 8000        │
│  Expo Go       │    │  Hot Reload     │    │   SEO-Friendly     │
│                │    │  Fast Refresh   │    │   Server-Rendered  │
│                │    │                 │    │                    │
│  Calls:        │    │  Calls:         │    │   Receives:        │
│  /api/*        │    │  /api/*         │    │   /en/*            │
│                │    │                 │    │                    │
└────────────────┘    └─────────────────┘    └────────────────────┘
```

---

## 🔄 Data Flow Examples

### Example 1: User Visits Homepage

```
┌─────────┐
│ Browser │
└────┬────┘
     │
     │ 1. GET http://localhost:8000/en/
     │
     ▼
┌─────────────────┐
│ Django Backend  │
│                 │
│ 2. Renders      │
│    enterprise-  │
│    home.html    │
│                 │
│ 3. Returns HTML │
└────┬────────────┘
     │
     │ 4. HTML with embedded CSS/JS
     │
     ▼
┌─────────┐
│ Browser │ 5. Displays homepage
└─────────┘    (SEO-friendly, fast load)
```

### Example 2: User Searches Properties (Web)

```
┌─────────┐
│ Browser │
└────┬────┘
     │
     │ 1. GET http://localhost:8000/en/properties/
     │
     ▼
┌─────────────────┐
│ Django Backend  │
│                 │
│ 2. Returns      │
│    React SPA    │
│    shell HTML   │
└────┬────────────┘
     │
     │ 3. HTML + React bundle
     │
     ▼
┌─────────┐
│ Browser │ 4. React loads
└────┬────┘
     │
     │ 5. React calls: GET /api/properties/?location=Anna+Nagar
     │
     ▼
┌─────────────────┐
│ Django Backend  │
│                 │
│ 6. Queries DB   │
│                 │
│ 7. Returns JSON │
└────┬────────────┘
     │
     │ 8. JSON: [{ id: 1, title: "...", ... }]
     │
     ▼
┌─────────┐
│ Browser │ 9. React renders property cards
└─────────┘    (Interactive, filterable)
```

### Example 3: Mobile App Searches Properties

```
┌──────────────┐
│ Mobile App   │
│ (iOS/Android)│
└──────┬───────┘
       │
       │ 1. User types "Anna Nagar"
       │
       │ 2. App calls: GET http://localhost:8000/api/search/?q=Anna+Nagar
       │
       ▼
┌─────────────────┐
│ Django Backend  │
│                 │
│ 3. Queries DB   │
│                 │
│ 4. Returns JSON │
└────┬────────────┘
     │
     │ 5. JSON: [{ id: 1, title: "...", ... }]
     │
     ▼
┌──────────────┐
│ Mobile App   │ 6. React Native renders native UI
└──────────────┘    (Smooth, native performance)
```

---

## 🌍 Development vs Production

### Development Environment

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                        │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Django     │  │    React     │  │    Mobile    │ │
│  │   Port 8000  │  │   Port 5173  │  │   Expo Go    │ │
│  │              │  │              │  │              │ │
│  │  APIs +      │  │  Hot Reload  │  │  Test on     │ │
│  │  Templates   │  │  Fast Dev    │  │  Device      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Production Environment

```
┌─────────────────────────────────────────────────────────┐
│                   PRODUCTION SERVER                     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Django (Port 8000)                    │  │
│  │                                                  │  │
│  │  ├── APIs (/api/*)                              │  │
│  │  ├── Web Pages (/en/*)                          │  │
│  │  ├── Static Files (/static/*)                   │  │
│  │  └── Admin (/en/admin/)                         │  │
│  │                                                  │  │
│  │  Everything served from single Django instance  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         ▲
                         │
                         │ HTTPS (Port 443)
                         │
        ┌────────────────┴────────────────┐
        │                                 │
┌───────▼────────┐              ┌─────────▼────────┐
│  Mobile Apps   │              │   Web Browsers   │
│  (App Stores)  │              │   (Internet)     │
└────────────────┘              └──────────────────┘
```

---

## 📱 Mobile App Architecture

```
┌─────────────────────────────────────────────────────────┐
│              REACT NATIVE MOBILE APP                    │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │                  App Screens                     │  │
│  │                                                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │  │
│  │  │  Home    │  │Properties│  │ Profile  │      │  │
│  │  │  Screen  │  │  Screen  │  │  Screen  │      │  │
│  │  └──────────┘  └──────────┘  └──────────┘      │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                               │
│                         │ Uses                          │
│                         ▼                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │              API Service Layer                   │  │
│  │                                                  │  │
│  │  const API_BASE = 'http://localhost:8000/api'   │  │
│  │                                                  │  │
│  │  fetchProperties()                               │  │
│  │  searchProperties(query)                         │  │
│  │  loginUser(credentials)                          │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                               │
└─────────────────────────┼───────────────────────────────┘
                          │
                          │ HTTP Requests
                          │
                          ▼
                  ┌───────────────┐
                  │ Django APIs   │
                  │ Port 8000     │
                  └───────────────┘
```

---

## 🎨 Web Frontend Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  WEB FRONTEND                           │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Marketing Pages (Django Templates)       │  │
│  │                                                  │  │
│  │  /en/           → enterprise-home.html           │  │
│  │  /en/about/     → about.html                     │  │
│  │  /en/contact/   → contact.html                   │  │
│  │                                                  │  │
│  │  ✓ SEO-friendly (server-rendered)               │  │
│  │  ✓ Fast initial load                            │  │
│  │  ✓ Google can crawl                             │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Interactive Features (React SPA)            │  │
│  │                                                  │  │
│  │  /en/properties/    → React property search      │  │
│  │  /en/properties/:id → React property details     │  │
│  │  /en/dashboard/     → React user dashboard       │  │
│  │                                                  │  │
│  │  ✓ Rich interactivity                           │  │
│  │  ✓ Smooth transitions                           │  │
│  │  ✓ Real-time updates                            │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication Flow

```
┌──────────┐
│  Client  │ (Web or Mobile)
└────┬─────┘
     │
     │ 1. POST /api/users/login/
     │    { email, password }
     │
     ▼
┌─────────────────┐
│ Django Backend  │
│                 │
│ 2. Verify       │
│    credentials  │
│                 │
│ 3. Generate     │
│    JWT token    │
└────┬────────────┘
     │
     │ 4. Return { token, user }
     │
     ▼
┌──────────┐
│  Client  │ 5. Store token
└────┬─────┘
     │
     │ 6. Subsequent requests:
     │    Authorization: Bearer <token>
     │
     ▼
┌─────────────────┐
│ Django Backend  │ 7. Verify token
│                 │ 8. Return protected data
└─────────────────┘
```

---

## 📦 Build & Deployment Process

```
┌─────────────────────────────────────────────────────────┐
│                  DEVELOPMENT                            │
│                                                         │
│  1. Edit React code in realtor-web/uilayers/src/       │
│  2. See changes at http://localhost:5173/ (hot reload) │
│  3. Test APIs at http://localhost:8000/api/            │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         │
                         │ When ready for production
                         ▼
┌─────────────────────────────────────────────────────────┐
│                     BUILD                               │
│                                                         │
│  1. npm run build (in uilayers/)                        │
│     → Compiles React to static files                    │
│     → Output: realtor-web/static/dist/                  │
│                                                         │
│  2. python manage.py collectstatic                      │
│     → Collects all static files                         │
│     → Ready for production serving                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         │
                         │ Deploy
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  PRODUCTION                             │
│                                                         │
│  Django serves everything from port 8000:               │
│  ├── /api/*        → REST APIs                          │
│  ├── /en/*         → Web pages                          │
│  ├── /static/*     → Static files (React build)         │
│  └── /en/admin/    → Admin panel                        │
│                                                         │
│  Mobile apps connect to: https://yourdomain.com/api     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Port Usage Summary

```
┌──────────────────────────────────────────────────────────┐
│                    PORT USAGE                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Port 8000 (Django)                                      │
│  ==================                                      │
│  ✓ Used in development                                  │
│  ✓ Used in production                                   │
│  ✓ Serves APIs (/api/*)                                 │
│  ✓ Serves web pages (/en/*)                             │
│  ✓ Serves static files (/static/*)                      │
│  ✓ Mobile apps connect here                             │
│  ✓ Web browsers connect here                            │
│                                                          │
│  THIS IS YOUR PRODUCTION SERVER                          │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Port 5173 (Vite/React)                                  │
│  ======================                                  │
│  ✓ Used ONLY in development                             │
│  ✗ NOT used in production                               │
│  ✓ Hot module replacement                               │
│  ✓ Fast refresh                                         │
│  ✓ React DevTools                                       │
│                                                          │
│  THIS IS OPTIONAL FOR DEVELOPMENT                        │
│  (Makes React development faster)                        │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Port 19000 (Expo)                                       │
│  =================                                       │
│  ✓ Used for mobile development                          │
│  ✓ Expo Dev Tools                                       │
│  ✓ QR code for device testing                           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Scenarios

### Scenario 1: Deploy to Heroku

```
1. Build React:
   cd realtor-web/uilayers
   npm run build

2. Commit changes:
   git add .
   git commit -m "Production build"

3. Deploy:
   git push heroku main

4. Update mobile app:
   API_BASE = 'https://yourapp.herokuapp.com/api'
```

### Scenario 2: Deploy to AWS EC2

```
1. Build React:
   npm run build

2. Set up server:
   - Install Python, PostgreSQL
   - Clone repository
   - Install dependencies

3. Configure Nginx:
   - Reverse proxy to port 8000
   - Serve static files
   - SSL certificate

4. Run with Gunicorn:
   gunicorn realtor_project.wsgi:application

5. Update mobile app:
   API_BASE = 'https://yourdomain.com/api'
```

### Scenario 3: Deploy to DigitalOcean

```
1. Use App Platform
2. Connect GitHub repository
3. Configure build command:
   cd realtor-web/uilayers && npm run build && cd .. && python manage.py collectstatic --noinput
4. Configure run command:
   gunicorn realtor_project.wsgi:application
5. Update mobile app API base
```

---

## ✅ Quick Reference

### Development Commands
```bash
# Start everything
run-web-only.bat

# Django only
cd realtor-web && python manage.py runserver

# React dev only
cd realtor-web/uilayers && npm run dev

# Mobile app
cd realtor-mobile && npm start
```

### Production Commands
```bash
# Build everything
build-production.bat

# Or manually:
cd realtor-web/uilayers && npm run build
cd .. && python manage.py collectstatic --noinput
python manage.py migrate
```

### URLs
```
Development:
- Django: http://localhost:8000/en/
- React:  http://localhost:5173/
- APIs:   http://localhost:8000/api/

Production:
- Everything: https://yourdomain.com/
```

---

**This architecture ensures**:
- ✅ Single backend for all clients
- ✅ SEO-friendly web pages
- ✅ Rich interactive features
- ✅ Native mobile performance
- ✅ Easy deployment
- ✅ Scalable infrastructure
