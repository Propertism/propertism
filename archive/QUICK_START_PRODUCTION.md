# Quick Start Guide - Production Ready Setup

## 🚀 What You Have

A production-ready real estate platform with:
- **Django Backend**: REST APIs + Web templates
- **React Web**: Interactive property search
- **React Native Mobile**: iOS/Android apps
- **Single Backend**: All clients share Django APIs

---

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

---

## ⚡ Quick Start (5 Minutes)

### 1. Start Development Servers

```bash
# Run this script
run-web-only.bat
```

This starts:
- Django backend on port 8000 (APIs + web pages)
- React dev server on port 5173 (optional, for hot reload)

### 2. Access the Application

**Production URL** (use this):
```
http://localhost:8000/en/
```

**Development URL** (React hot reload):
```
http://localhost:5173/
```

**Admin Panel**:
```
http://localhost:8000/en/admin/
Username: admin
Password: admin123
```

**API Endpoints**:
```
http://localhost:8000/api/properties/
http://localhost:8000/api/users/
http://localhost:8000/api/search/
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────┐
│   Django Backend (Port 8000)        │
│   ├── REST APIs (/api/*)            │
│   ├── Web Pages (/en/*)             │
│   └── Admin (/en/admin/)            │
└─────────────────────────────────────┘
         ▲              ▲
         │              │
    ┌────┴────┐    ┌────┴────┐
    │ Mobile  │    │   Web   │
    │   App   │    │ Browser │
    └─────────┘    └─────────┘
```

---

## 📱 Mobile App Setup

### 1. Navigate to Mobile Directory
```bash
cd realtor-mobile
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Expo
```bash
npm start
```

### 4. Configure API Base
The mobile app is already configured to use:
```typescript
// realtor-mobile/src/services/api.ts
const API_BASE = 'http://localhost:8000/api'
```

For production, change to:
```typescript
const API_BASE = 'https://yourdomain.com/api'
```

---

## 🌐 Web Development

### Option 1: Use Django Templates (Recommended for Production)
```bash
# Just run Django
cd realtor-web
python manage.py runserver
# Visit: http://localhost:8000/en/
```

**Benefits**:
- SEO-friendly (server-side rendering)
- Fast initial page load
- No build step needed
- Production-ready

### Option 2: Use React Dev Server (For Development)
```bash
# Terminal 1: Django backend
cd realtor-web
python manage.py runserver

# Terminal 2: React dev server
cd realtor-web/uilayers
npm run dev
# Visit: http://localhost:5173/
```

**Benefits**:
- Hot module replacement
- Fast refresh
- React DevTools
- Instant updates

---

## 🔨 Building for Production

### Automated Build
```bash
build-production.bat
```

This will:
1. Build React app → `realtor-web/static/dist/`
2. Collect Django static files
3. Run migrations
4. Run tests

### Manual Build
```bash
# 1. Build React
cd realtor-web/uilayers
npm run build

# 2. Collect static files
cd ..
python manage.py collectstatic --noinput

# 3. Run migrations
python manage.py migrate

# 4. Test
python manage.py runserver
# Visit: http://localhost:8000/en/
```

---

## 📂 Project Structure

```
realtor/
├── realtor-web/                    # Django backend + web
│   ├── manage.py
│   ├── realtor_project/            # Settings
│   ├── properties/                 # Properties app
│   ├── users/                      # Users app
│   ├── search/                     # Search app
│   ├── uilayers/                   # React web frontend
│   │   ├── src/                    # React source
│   │   └── dist/                   # Build output
│   ├── templates/                  # Django templates
│   │   └── enterprise-home.html    # Homepage
│   └── static/                     # Static files
│
├── realtor-mobile/                 # React Native mobile
│   ├── app/                        # Expo Router
│   ├── src/                        # Components
│   └── package.json
│
├── run-web-only.bat                # Start dev servers
├── build-production.bat            # Build for production
└── PRODUCTION_ARCHITECTURE.md      # Full architecture docs
```

---

## 🎯 URL Structure

### Web Pages (Django Templates)
```
/en/                    → Homepage (enterprise-home.html)
/en/about/              → About page
/en/contact/            → Contact page
/en/admin/              → Django admin
```

### Interactive Features (React SPA)
```
/en/properties/         → Property search (React)
/en/properties/:id/     → Property details (React)
```

### API Endpoints (For Mobile + Web)
```
/api/properties/        → List properties
/api/properties/:id/    → Property details
/api/users/login/       → User login
/api/users/register/    → User registration
/api/search/            → Search properties
```

---

## 🔑 Key Concepts

### Port 8000 (Production)
- Django serves everything
- APIs at `/api/*`
- Web pages at `/en/*`
- Static files at `/static/*`
- **This is what you deploy**

### Port 5173 (Development Only)
- React dev server
- Hot reload for fast development
- **Not used in production**
- Optional during development

### Mobile App
- Uses APIs at `/api/*` only
- Doesn't care about web frontend
- Works with port 8000 in dev
- Points to production domain in prod

---

## 🚢 Deployment Checklist

### Pre-Deployment
- [ ] Run `build-production.bat`
- [ ] Test at `http://localhost:8000/en/`
- [ ] Verify APIs work: `/api/properties/`
- [ ] Check admin panel: `/en/admin/`

### Production Configuration
- [ ] Set `DEBUG=False` in settings.py
- [ ] Configure PostgreSQL database
- [ ] Set `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure email backend
- [ ] Set up SSL certificate

### Deployment
- [ ] Deploy Django to server
- [ ] Configure Nginx reverse proxy
- [ ] Set up domain DNS
- [ ] Test production URLs
- [ ] Update mobile app API base

### Post-Deployment
- [ ] Monitor error logs
- [ ] Check performance
- [ ] Test mobile app connectivity
- [ ] Verify SEO meta tags

---

## 🐛 Troubleshooting

### Django won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process
taskkill /F /PID <process_id>
```

### React build fails
```bash
cd realtor-web/uilayers
rm -rf node_modules
npm install
npm run build
```

### Static files not loading
```bash
cd realtor-web
python manage.py collectstatic --clear --noinput
```

### Mobile app can't connect to API
```typescript
// Check API base URL
// realtor-mobile/src/services/api.ts

// For local development:
const API_BASE = 'http://localhost:8000/api'

// For Android emulator:
const API_BASE = 'http://10.0.2.2:8000/api'

// For physical device (same network):
const API_BASE = 'http://192.168.1.x:8000/api'
```

---

## 📚 Additional Resources

- **Full Architecture**: See `PRODUCTION_ARCHITECTURE.md`
- **SCCB Design Docs**: See `sccbs/` folder
- **Django Docs**: See `realtor-web/documents/`
- **API Spec**: See `realtor-web/documents/BACKEND_API_SPEC.md`

---

## 🎨 Design System

The application follows SCCB-4 and SCCB-5 design principles:

- **NO rounded corners** - Sharp edges only
- **NO emojis** - Professional text
- **NO gradients** - Solid colors
- **Navy/Gold/White** color palette
- **Playfair Display** + **Inter** fonts
- **Enterprise-grade** aesthetic

---

## 💡 Development Tips

### Fast React Development
```bash
# Use port 5173 for instant updates
cd realtor-web/uilayers
npm run dev
```

### API Testing
```bash
# Use Django REST Framework browsable API
http://localhost:8000/api/properties/
```

### Database Management
```bash
# Create superuser
python manage.py createsuperuser

# Reset database
python manage.py flush

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Add Sample Data
```bash
cd realtor-web
python add_sample_properties.py
```

---

## 🎯 Next Steps

1. **Customize Content**
   - Update homepage copy in `enterprise-home.html`
   - Add real property images
   - Configure contact information

2. **Enhance Features**
   - Add property filters
   - Implement user authentication
   - Add favorites/wishlist
   - Integrate payment gateway

3. **Optimize Performance**
   - Enable caching
   - Optimize images (WebP)
   - Set up CDN
   - Configure Redis

4. **Deploy to Production**
   - Choose hosting (AWS, DigitalOcean, Heroku)
   - Configure domain
   - Set up SSL
   - Deploy mobile apps to stores

---

## 📞 Support

For issues or questions:
1. Check `PRODUCTION_ARCHITECTURE.md`
2. Review Django logs
3. Check browser console
4. Test API endpoints directly

---

**Status**: Production Ready ✅
**Last Updated**: February 22, 2026
**Architecture**: API-First Hybrid (Django + React + React Native)
