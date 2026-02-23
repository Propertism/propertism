# 🏗️ Architecture Overview - Chennai Realtor

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MONOREPO ROOT                           │
│                    (Yarn Workspaces)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌───────────┐  ┌───────────┐  ┌───────────┐
        │  SHARED   │  │    WEB    │  │  MOBILE   │
        │   CODE    │  │    PWA    │  │    APP    │
        └───────────┘  └───────────┘  └───────────┘
```

## Detailed Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐         ┌─────────────────────┐       │
│  │   WEB PWA (React)   │         │  MOBILE (RN Expo)   │       │
│  │                     │         │                     │       │
│  │  • Vite + Tailwind  │         │  • Expo Router      │       │
│  │  • React Router     │         │  • NativeWind       │       │
│  │  • PWA Support      │         │  • Native UI        │       │
│  │  • Responsive Grid  │         │  • FlatList         │       │
│  │                     │         │                     │       │
│  │  Port: 5173         │         │  Port: 19000        │       │
│  └─────────────────────┘         └─────────────────────┘       │
│           │                               │                     │
│           └───────────┬───────────────────┘                     │
│                       │                                         │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        │ HTTP/REST
                        │
┌───────────────────────┼─────────────────────────────────────────┐
│                       ▼                                         │
│              ┌─────────────────┐                               │
│              │  SHARED CODE    │                               │
│              │                 │                               │
│              │  • Types (TS)   │                               │
│              │  • Utils        │                               │
│              │  • API Client   │                               │
│              │  • Formatters   │                               │
│              └─────────────────┘                               │
│                       │                                         │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        │ Axios
                        │
┌───────────────────────┼─────────────────────────────────────────┐
│                       ▼          API LAYER                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│              ┌─────────────────────────────┐                    │
│              │   DJANGO REST FRAMEWORK     │                    │
│              │                             │                    │
│              │  • JWT Authentication       │                    │
│              │  • CORS Middleware          │                    │
│              │  • Pagination               │                    │
│              │  • Serializers              │                    │
│              │                             │                    │
│              │  Port: 8000                 │                    │
│              └─────────────────────────────┘                    │
│                       │                                         │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        │ ORM
                        │
┌───────────────────────┼─────────────────────────────────────────┐
│                       ▼          DATA LAYER                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│              ┌─────────────────────────────┐                    │
│              │      DJANGO MODELS          │                    │
│              │                             │                    │
│              │  • Property                 │                    │
│              │  • PropertyType             │                    │
│              │  • PropertyPhoto            │                    │
│              │  • User (Agent/Buyer)       │                    │
│              │  • Inquiry                  │                    │
│              │  • MaintenanceRequest       │                    │
│              │  • SupportTicket            │                    │
│              └─────────────────────────────┘                    │
│                       │                                         │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        │ SQL
                        │
┌───────────────────────┼─────────────────────────────────────────┐
│                       ▼       DATABASE LAYER                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│              ┌─────────────────────────────┐                    │
│              │   SQLite (Dev)              │                    │
│              │   PostgreSQL (Production)   │                    │
│              └─────────────────────────────┘                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Property Listing Flow

```
User Opens App
      │
      ▼
┌─────────────┐
│  Web/Mobile │
│   Component │
└─────────────┘
      │
      │ useEffect()
      ▼
┌─────────────┐
│ api.get()   │
│ /properties │
└─────────────┘
      │
      │ HTTP GET
      ▼
┌─────────────────┐
│ Django View     │
│ property_list() │
└─────────────────┘
      │
      │ ORM Query
      ▼
┌─────────────────┐
│ Property.       │
│ objects.all()   │
└─────────────────┘
      │
      │ SQL
      ▼
┌─────────────────┐
│ Database        │
│ SELECT * FROM   │
│ properties      │
└─────────────────┘
      │
      │ Results
      ▼
┌─────────────────┐
│ Serializer      │
│ PropertySerial  │
└─────────────────┘
      │
      │ JSON
      ▼
┌─────────────────┐
│ Paginator       │
│ 10 items/page   │
└─────────────────┘
      │
      │ Response
      ▼
┌─────────────────┐
│ Component       │
│ setState()      │
└─────────────────┘
      │
      │ Render
      ▼
┌─────────────────┐
│ PropertyCard    │
│ Grid Display    │
└─────────────────┘
```

## Technology Stack

```
┌──────────────────────────────────────────────────────────┐
│                    FRONTEND                              │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Web PWA                    Mobile App                   │
│  ├─ React 18.2              ├─ React Native 0.73        │
│  ├─ TypeScript 5.2          ├─ Expo 50                  │
│  ├─ Vite 5.0                ├─ Expo Router 3.4          │
│  ├─ Tailwind CSS 3.4        ├─ NativeWind 4.0           │
│  ├─ React Router 6.20       ├─ TypeScript 5.1           │
│  ├─ Axios 1.6               └─ Axios 1.6                │
│  └─ Vite PWA Plugin                                      │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                    BACKEND                               │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ├─ Django 4.2.7                                         │
│  ├─ Django REST Framework 3.14                           │
│  ├─ JWT Authentication (simplejwt 5.3)                   │
│  ├─ CORS Headers 4.3                                     │
│  ├─ Pillow 10.1 (images)                                 │
│  └─ psycopg2 2.9 (PostgreSQL)                            │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                    DATABASE                              │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Development:  SQLite 3                                  │
│  Production:   PostgreSQL 15+                            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## API Endpoints

```
┌─────────────────────────────────────────────────────────┐
│                   REST API                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Properties                                             │
│  ├─ GET  /api/properties/          List (paginated)    │
│  ├─ GET  /api/properties/{id}/     Detail              │
│  └─ GET  /api/search/              Search              │
│                                                         │
│  Authentication                                         │
│  └─ POST /api/auth/login/          JWT Login           │
│                                                         │
│  Admin                                                  │
│  └─ GET  /admin/                   Django Admin        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    PRODUCTION                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────┐         ┌────────────┐                  │
│  │   Vercel   │         │   Render   │                  │
│  │            │         │            │                  │
│  │  React PWA │◄───────►│  Django    │                  │
│  │  (Static)  │   API   │  (Server)  │                  │
│  └────────────┘         └────────────┘                  │
│                               │                          │
│                               │                          │
│                         ┌─────▼──────┐                   │
│                         │ PostgreSQL │                   │
│                         │  Database  │                   │
│                         └────────────┘                   │
│                                                          │
│  ┌────────────┐                                          │
│  │ Play Store │                                          │
│  │ App Store  │                                          │
│  │            │                                          │
│  │ React      │                                          │
│  │ Native APK │                                          │
│  └────────────┘                                          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Security Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. HTTPS/SSL                                            │
│     └─ All traffic encrypted                             │
│                                                          │
│  2. CORS                                                 │
│     └─ Allowed origins only                              │
│                                                          │
│  3. JWT Authentication                                   │
│     ├─ Access token (24h)                                │
│     └─ Refresh token (7d)                                │
│                                                          │
│  4. Django Security                                      │
│     ├─ CSRF protection                                   │
│     ├─ XSS protection                                    │
│     ├─ SQL injection protection (ORM)                    │
│     └─ Clickjacking protection                           │
│                                                          │
│  5. Input Validation                                     │
│     ├─ Pydantic schemas                                  │
│     └─ DRF serializers                                   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Performance Optimizations

```
┌──────────────────────────────────────────────────────────┐
│                  PERFORMANCE                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Frontend                                                │
│  ├─ Vite (fast dev server)                               │
│  ├─ Code splitting                                       │
│  ├─ Lazy loading images                                  │
│  ├─ PWA caching                                          │
│  └─ Optimized bundles                                    │
│                                                          │
│  Backend                                                 │
│  ├─ Database indexing                                    │
│  ├─ Query optimization                                   │
│  ├─ Pagination (10/page)                                 │
│  └─ API response caching                                 │
│                                                          │
│  Mobile                                                  │
│  ├─ FlatList virtualization                              │
│  ├─ Image optimization                                   │
│  └─ Minimal bundle size                                  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

**Architecture Status**: ✅ Production-Ready
**Last Updated**: February 22, 2026
