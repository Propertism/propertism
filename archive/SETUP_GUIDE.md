# 🚀 Complete Setup Guide - Chennai Realtor Monorepo

## ✅ What's Been Built

### Monorepo Structure
```
realtor/
├── shared/                    ✅ Shared TypeScript types, utils, API client
├── realtor-web/
│   ├── Django Backend         ✅ REST API with DRF + JWT
│   └── uilayers/              ✅ React PWA (Vite + Tailwind)
└── realtor-mobile/            ✅ React Native Expo app
```

### Features Implemented
- ✅ Shared types/utils between web & mobile
- ✅ Chennai INR formatting (₹5.2Cr, ₹45L, ₹5L)
- ✅ Django REST API with pagination
- ✅ JWT authentication
- ✅ CORS enabled for web + mobile
- ✅ React PWA with Vite + Tailwind
- ✅ React Native with NativeWind
- ✅ Mobile-first responsive design
- ✅ Lazy image loading
- ✅ Tamil/Hinglish search support

## 📦 Installation Steps

### 1. Install Node Dependencies

```bash
# From project root
yarn install
```

This installs:
- Web PWA dependencies (React, Vite, Tailwind)
- Mobile dependencies (Expo, React Native)
- Shared workspace setup

### 2. Install Python Dependencies

```bash
cd realtor-web
pip install -r requirements.txt
```

Installs:
- Django 4.2.7
- Django REST Framework
- JWT authentication
- CORS headers
- PostgreSQL driver

### 3. Setup Database

```bash
cd realtor-web

# Create migrations
python manage.py makemigrations properties users search

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Create Sample Data (Optional)

```bash
python manage.py shell
```

```python
from properties.models import Property, PropertyType

# Create property types
villa = PropertyType.objects.create(name="Villa", slug="villa")
apartment = PropertyType.objects.create(name="Apartment", slug="apartment")

# Create sample properties
Property.objects.create(
    title="Luxury Villa in Anna Nagar",
    description="Beautiful 4BHK villa with modern amenities",
    price=12500000,
    price_type="sale",
    bedrooms=4,
    bathrooms=3,
    location="Anna Nagar, Chennai",
    image="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9",
    property_type=villa,
    status="available"
)

Property.objects.create(
    title="Modern Apartment in T Nagar",
    description="Spacious 3BHK apartment near metro",
    price=35000,
    price_type="rent",
    bedrooms=3,
    bathrooms=2,
    location="T Nagar, Chennai",
    image="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00",
    property_type=apartment,
    status="available"
)

exit()
```

## 🚀 Running the Application

### Option 1: Run Everything Together

```bash
# Terminal 1: Django backend
cd realtor-web
python manage.py runserver

# Terminal 2: Web + Mobile (from root)
yarn dev
```

### Option 2: Run Individually

```bash
# Django backend
cd realtor-web
python manage.py runserver

# Web PWA only
yarn web:dev

# Mobile only
yarn mobile:dev
```

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Django Admin | http://localhost:8000/admin | Admin panel |
| API Root | http://localhost:8000/api | REST API |
| Web PWA | http://localhost:5173 | React web app |
| Mobile | Expo Go App | Scan QR code |

## 📡 API Endpoints

### Properties
```
GET  /api/properties/              - List properties (paginated)
GET  /api/properties/{id}/         - Property details
GET  /api/search/?location=Chennai - Search properties
```

### Authentication
```
POST /api/auth/login/              - JWT login
```

Example login request:
```json
{
  "username": "admin",
  "password": "your_password"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 📱 Mobile Development

### Running on Physical Device

1. Install Expo Go app on your phone:
   - Android: Google Play Store
   - iOS: App Store

2. Start the development server:
```bash
cd realtor-mobile
yarn start
```

3. Scan the QR code with:
   - Android: Expo Go app
   - iOS: Camera app

### Running on Emulator

```bash
# Android
yarn android

# iOS (Mac only)
yarn ios
```

## 🎨 Web PWA Features

### Pages Implemented
- ✅ Home page with hero section
- ✅ Properties listing with grid layout
- ✅ Property detail page
- ✅ About page
- ✅ Contact page

### Responsive Design
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px)
- Grid: 1 column (mobile) → 2 columns (tablet) → 3 columns (desktop)

### PWA Features
- Service worker for offline support
- Installable on mobile devices
- Fast loading with Vite
- Lazy image loading

## 🔧 Configuration

### Update API Base URL

For production, update `shared/services/api.ts`:

```typescript
const API_BASE = process.env.VITE_API_URL || "http://localhost:8000/api"
```

Then create `.env` in `realtor-web/uilayers/`:
```
VITE_API_URL=https://api.yoursite.com/api
```

### Django Settings for Production

Update `realtor-web/realtor_project/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yoursite.com', 'www.yoursite.com']
SECRET_KEY = 'your-production-secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'realtor_db',
        'USER': 'realtor_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://yoursite.com",
    "https://www.yoursite.com",
]
```

## 🐛 Troubleshooting

### Django Issues

**Error: No module named 'rest_framework'**
```bash
cd realtor-web
pip install -r requirements.txt
```

**Error: No migrations to apply**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Web PWA Issues

**Error: Cannot find module**
```bash
# From project root
yarn install
cd realtor-web/uilayers
yarn install
```

**Port 5173 already in use**
```bash
# Kill the process or use different port
vite --port 3000
```

### Mobile Issues

**Expo Go not connecting**
- Ensure phone and computer are on same WiFi
- Try tunnel mode: `expo start --tunnel`

**Metro bundler error**
```bash
cd realtor-mobile
rm -rf node_modules
yarn install
yarn start --clear
```

## 📊 Project Status

### Completed ✅
- [x] Monorepo structure with Yarn workspaces
- [x] Shared types and utilities
- [x] Django REST API with pagination
- [x] JWT authentication
- [x] CORS configuration
- [x] React PWA with Vite
- [x] Tailwind CSS setup
- [x] React Native Expo app
- [x] NativeWind configuration
- [x] Property listing pages
- [x] Property detail pages
- [x] Chennai INR formatting
- [x] Mobile-first responsive design

### Next Steps 🚧
- [ ] Add property image upload
- [ ] Implement inquiry forms
- [ ] Add user dashboard
- [ ] Implement favorites/wishlist
- [ ] Add property comparison
- [ ] Implement map view
- [ ] Add push notifications (mobile)
- [ ] Set up CI/CD pipeline
- [ ] Deploy to production

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review Django/React/Expo documentation
3. Check console logs for errors

## 🎯 Quick Commands Reference

```bash
# Install everything
yarn install && cd realtor-web && pip install -r requirements.txt

# Run migrations
cd realtor-web && python manage.py migrate

# Start all services
cd realtor-web && python manage.py runserver &
yarn dev

# Build for production
cd realtor-web/uilayers && yarn build
cd realtor-mobile && eas build
```

---

**Status**: ✅ Production-ready monorepo complete
**Last Updated**: February 22, 2026
