# Production Architecture - Chennai Realtor

## Overview
Industry-standard API-first architecture supporting web and mobile clients with a single Django backend.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│              Django Backend (Port 8000)                     │
│                                                             │
│  ┌──────────────────────┐  ┌───────────────────────────┐  │
│  │   REST APIs          │  │   Web Frontend            │  │
│  │   /api/properties/   │  │   /en/ (Django Template)  │  │
│  │   /api/users/        │  │   /en/properties/ (React) │  │
│  │   /api/search/       │  │   /en/admin/ (Django)     │  │
│  │   /api/auth/         │  │   /static/ (Assets)       │  │
│  └──────────────────────┘  └───────────────────────────┘  │
│                                                             │
│  Database: SQLite (dev) / PostgreSQL (prod)                │
└─────────────────────────────────────────────────────────────┘
                    ▲                           ▲
                    │                           │
        ┌───────────┴──────────┐    ┌──────────┴──────────┐
        │                      │    │                     │
┌───────▼────────┐    ┌────────▼────────┐    ┌───────────▼────────┐
│ React Native   │    │ React Web PWA   │    │  Web Browsers      │
│ Mobile App     │    │ (Dev: :5173)    │    │  (Prod: :8000)     │
│ (iOS/Android)  │    │ (Prod: :8000)   │    │                    │
└────────────────┘    └─────────────────┘    └────────────────────┘
```

---

## Components

### 1. Django Backend (realtor-web/)
**Purpose**: Single source of truth for all data and business logic

**Responsibilities**:
- REST API endpoints for mobile and web clients
- Database management (properties, users, search)
- Authentication and authorization
- Admin panel for content management
- Serve static files and templates

**Endpoints**:
```
/api/properties/          → Property listings (GET, POST, PUT, DELETE)
/api/properties/:id/      → Property details
/api/users/               → User management
/api/users/login/         → Authentication
/api/users/register/      → Registration
/api/search/              → Property search
/en/                      → Homepage (Django template)
/en/properties/           → Property search page (React SPA)
/en/about/                → About page (Django template)
/en/contact/              → Contact page (Django template)
/en/admin/                → Django admin panel
```

### 2. React Web PWA (realtor-web/uilayers/)
**Purpose**: Interactive web features with rich UX

**Development**:
- Port 5173 (Vite dev server)
- Hot module replacement
- Fast refresh
- React DevTools

**Production**:
- Built to `realtor-web/static/dist/`
- Served by Django at port 8000
- No separate server needed

**Pages**:
- Property search with filters
- Property detail views
- User dashboard
- Interactive maps

### 3. React Native Mobile (realtor-mobile/)
**Purpose**: Native iOS and Android apps

**Technology**:
- Expo framework
- React Native
- Calls Django APIs only

**Features**:
- Property browsing
- Search and filters
- User authentication
- Push notifications
- Offline support

---

## Development Workflow

### Starting Development

```bash
# Terminal 1: Django Backend
cd realtor-web
python manage.py runserver
# → http://localhost:8000

# Terminal 2: React Web Dev (Optional - for fast development)
cd realtor-web/uilayers
npm run dev
# → http://localhost:5173

# Terminal 3: Mobile App
cd realtor-mobile
npm start
# → Expo Go app
```

### Quick Start Script
```bash
# Use the consolidated script
run-web-only.bat
```

---

## Production Deployment

### Step 1: Build React Web
```bash
cd realtor-web/uilayers
npm run build
# Output: realtor-web/static/dist/
```

### Step 2: Collect Static Files
```bash
cd realtor-web
python manage.py collectstatic --noinput
```

### Step 3: Deploy Django
```bash
# Configure production settings
# Set DEBUG=False
# Configure PostgreSQL
# Set ALLOWED_HOSTS

# Run with Gunicorn
gunicorn realtor_project.wsgi:application --bind 0.0.0.0:8000
```

### Step 4: Configure Mobile App
```typescript
// realtor-mobile/src/services/api.ts
const API_BASE = 'https://yourdomain.com/api'
```

### Step 5: Deploy Mobile
```bash
cd realtor-mobile
eas build --platform all
eas submit --platform all
```

---

## URL Structure

### Production URLs (Single Domain)

```
https://chennairealtor.com/
├── /                          → Homepage (Django template)
├── /en/                       → Homepage (i18n)
├── /en/properties/            → Property search (React SPA)
├── /en/properties/:id/        → Property detail (React SPA)
├── /en/about/                 → About page (Django template)
├── /en/contact/               → Contact page (Django template)
├── /en/admin/                 → Django admin
├── /api/properties/           → API for mobile + web
├── /api/users/                → API for mobile + web
├── /api/search/               → API for mobile + web
└── /static/                   → Static assets
```

### Mobile App Configuration
```
API Base: https://chennairealtor.com/api
```

---

## Data Flow

### Web Client (Browser)
```
User visits /en/
  → Django serves enterprise-home.html (SEO-friendly)
  
User visits /en/properties/
  → Django serves React SPA shell
  → React loads and calls /api/properties/
  → Django returns JSON
  → React renders interactive UI
```

### Mobile Client (iOS/Android)
```
App launches
  → Calls /api/properties/
  → Django returns JSON
  → React Native renders native UI
  
User searches
  → Calls /api/search/?location=Anna+Nagar
  → Django returns filtered JSON
  → React Native updates UI
```

---

## Benefits of This Architecture

### ✅ Single Backend
- One codebase for business logic
- Consistent data across platforms
- Easier maintenance

### ✅ API-First Design
- Mobile and web share same APIs
- Easy to add new clients (desktop app, CLI, etc.)
- Clear separation of concerns

### ✅ SEO-Friendly
- Marketing pages are server-rendered
- Google can crawl Django templates
- Fast initial page load

### ✅ Rich Interactivity
- React for complex features
- Smooth user experience
- Modern web standards

### ✅ Mobile Native
- True native performance
- Platform-specific features
- App store distribution

---

## Technology Stack

### Backend
- **Framework**: Django 4.2+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **API**: Django REST Framework
- **CMS**: Django CMS 4.1
- **Auth**: Django authentication

### Web Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router
- **State**: React Context / Zustand

### Mobile Frontend
- **Framework**: React Native
- **Platform**: Expo
- **Navigation**: Expo Router
- **Styling**: NativeWind (Tailwind for RN)

---

## Environment Configuration

### Development (.env.development)
```env
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
API_BASE_URL=http://localhost:8000/api
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (.env.production)
```env
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname
API_BASE_URL=https://chennairealtor.com/api
ALLOWED_HOSTS=chennairealtor.com,www.chennairealtor.com
SECRET_KEY=<strong-secret-key>
```

---

## Port Usage

### Development
- **8000**: Django backend (APIs + templates)
- **5173**: React dev server (optional, for fast dev)
- **19000**: Expo dev server (mobile)

### Production
- **8000**: Django only (serves everything)
- **443**: HTTPS (Nginx reverse proxy)

---

## File Structure

```
realtor/
├── realtor-web/                    # Django backend + web frontend
│   ├── manage.py
│   ├── realtor_project/            # Django settings
│   ├── properties/                 # Properties app
│   ├── users/                      # Users app
│   ├── search/                     # Search app
│   ├── uilayers/                   # React web frontend
│   │   ├── src/                    # React source
│   │   ├── dist/                   # Build output (gitignored)
│   │   └── package.json
│   ├── templates/                  # Django templates
│   │   └── enterprise-home.html
│   ├── static/                     # Static files
│   │   └── dist/                   # React build output
│   └── requirements.txt
│
├── realtor-mobile/                 # React Native mobile app
│   ├── app/                        # Expo Router pages
│   ├── src/                        # Shared components
│   ├── app.json                    # Expo config
│   └── package.json
│
└── shared/                         # Shared utilities (optional)
    └── utils/
```

---

## API Documentation

### Properties API

**List Properties**
```http
GET /api/properties/
Response: [
  {
    "id": 1,
    "title": "Anna Nagar Residence",
    "location": "Anna Nagar",
    "price": 14500000,
    "bedrooms": 4,
    "bathrooms": 3,
    "area": 3200,
    "images": [...]
  }
]
```

**Get Property**
```http
GET /api/properties/:id/
Response: {
  "id": 1,
  "title": "Anna Nagar Residence",
  ...
}
```

**Search Properties**
```http
GET /api/search/?location=Anna+Nagar&min_price=1000000&max_price=5000000
Response: [...]
```

### Users API

**Register**
```http
POST /api/users/register/
Body: {
  "email": "user@example.com",
  "password": "secure123",
  "name": "John Doe"
}
```

**Login**
```http
POST /api/users/login/
Body: {
  "email": "user@example.com",
  "password": "secure123"
}
Response: {
  "token": "...",
  "user": {...}
}
```

---

## Testing Strategy

### Backend Tests
```bash
cd realtor-web
python manage.py test
```

### Web Frontend Tests
```bash
cd realtor-web/uilayers
npm run test
```

### Mobile Tests
```bash
cd realtor-mobile
npm run test
```

### E2E Tests
```bash
# Playwright or Cypress
npm run test:e2e
```

---

## Monitoring & Analytics

### Backend
- Django Debug Toolbar (dev)
- Sentry (error tracking)
- New Relic (performance)

### Web
- Google Analytics
- Hotjar (user behavior)
- Lighthouse (performance)

### Mobile
- Firebase Analytics
- Crashlytics
- App Store Analytics

---

## Security Considerations

### API Security
- CORS configuration
- Rate limiting
- JWT authentication
- HTTPS only in production

### Data Protection
- SQL injection prevention (Django ORM)
- XSS prevention (React escaping)
- CSRF tokens
- Secure password hashing

---

## Scaling Strategy

### Horizontal Scaling
- Load balancer (Nginx)
- Multiple Django instances
- Redis for caching
- CDN for static files

### Database Scaling
- PostgreSQL read replicas
- Connection pooling
- Query optimization
- Database indexing

---

## Deployment Checklist

### Pre-Deployment
- [ ] Build React web app
- [ ] Run Django migrations
- [ ] Collect static files
- [ ] Update environment variables
- [ ] Test API endpoints
- [ ] Run security checks

### Deployment
- [ ] Deploy Django to server
- [ ] Configure Nginx reverse proxy
- [ ] Set up SSL certificate
- [ ] Configure domain DNS
- [ ] Test production URLs

### Post-Deployment
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Test mobile app connectivity
- [ ] Verify SEO meta tags
- [ ] Test user flows

---

**Status**: Production Ready ✅
**Last Updated**: February 22, 2026
**Architecture**: API-First Hybrid (Django + React Web + React Native Mobile)
