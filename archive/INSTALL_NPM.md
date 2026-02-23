# 🚀 Installation with NPM (No Yarn Required)

## Prerequisites

You need:
- ✅ Node.js (includes npm) - [Download here](https://nodejs.org/)
- ✅ Python 3.11+ - Already installed
- ✅ Git (optional)

## Quick Install

### Option 1: Install Everything at Once

```bash
# From project root
npm run install:all
```

This will install:
- Root dependencies
- Web PWA dependencies (realtor-web/uilayers)
- Mobile app dependencies (realtor-mobile)

### Option 2: Install Manually (Step by Step)

```bash
# 1. Install root dependencies
npm install

# 2. Install web PWA dependencies
cd realtor-web/uilayers
npm install
cd ../..

# 3. Install mobile dependencies
cd realtor-mobile
npm install
cd ..

# 4. Install Python dependencies
cd realtor-web
pip install -r requirements.txt
cd ..
```

## Setup Database

```bash
cd realtor-web

# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

## Run Development Servers

### Option 1: Run All Together

```bash
# Terminal 1: Django backend
cd realtor-web
python manage.py runserver

# Terminal 2: Web + Mobile (from root)
npm run dev
```

### Option 2: Run Individually

```bash
# Django backend
cd realtor-web
python manage.py runserver

# Web PWA only
cd realtor-web/uilayers
npm run dev

# Mobile only
cd realtor-mobile
npm start
```

## Access Points

| Service | URL |
|---------|-----|
| Web PWA | http://localhost:5173 |
| Django Admin | http://localhost:8000/admin |
| API | http://localhost:8000/api/properties/ |
| Mobile | Expo Go app (scan QR) |

## Troubleshooting

### "npm not found"
Install Node.js from https://nodejs.org/ (includes npm)

### "Module not found"
```bash
# Reinstall dependencies
npm run install:all
```

### Port already in use
```bash
# Django: Use different port
python manage.py runserver 8001

# Web: Vite will auto-select next available port
```

## NPM Commands Reference

```bash
# Install all dependencies
npm run install:all

# Run web dev server
npm run web:dev

# Run mobile dev server
npm run mobile:dev

# Run both web + mobile
npm run dev

# Install new package in web
cd realtor-web/uilayers
npm install <package-name>

# Install new package in mobile
cd realtor-mobile
npm install <package-name>
```

## What Gets Installed

### Root (realtor/)
- concurrently (run multiple commands)

### Web PWA (realtor-web/uilayers/)
- react, react-dom
- vite, @vitejs/plugin-react
- tailwindcss, postcss, autoprefixer
- react-router-dom
- axios
- vite-plugin-pwa
- typescript

### Mobile (realtor-mobile/)
- expo
- expo-router
- react-native
- nativewind
- axios

### Backend (realtor-web/)
- Django
- djangorestframework
- djangorestframework-simplejwt
- django-cors-headers
- Pillow
- psycopg2-binary

## Next Steps

1. ✅ Install complete
2. Add sample data via Django admin
3. Test web at http://localhost:5173
4. Test mobile with Expo Go
5. Start building!

---

**No Yarn Required** - Everything works with npm!
