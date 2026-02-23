# 🪟 Windows Setup Guide

## ✅ Easy Setup for Windows Users

### Prerequisites

1. **Node.js** (includes npm)
   - Download: https://nodejs.org/
   - Install LTS version
   - ✅ Already installed (npm 11.6.0)

2. **Python 3.11+**
   - Download: https://python.org/
   - Check "Add to PATH" during installation
   - ✅ Already installed

3. **Git** (optional)
   - Download: https://git-scm.com/

## 🚀 Quick Install (3 Steps)

### Step 1: Install Dependencies

**Double-click this file:**
```
install.bat
```

This will automatically:
- Install root npm packages
- Install web PWA packages
- Install mobile packages
- Install Python packages

### Step 2: Setup Database

Open Command Prompt or PowerShell:

```bash
cd realtor-web
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Follow prompts to create admin user:
- Username: admin
- Email: admin@example.com
- Password: (your choice)

### Step 3: Run Servers

**Double-click this file:**
```
run-dev.bat
```

This will open 2 windows:
1. Django Backend (port 8000)
2. Web + Mobile (ports 5173, 19000)

## 🌐 Access Your App

Open in browser:
- **Web App**: http://localhost:5173
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/properties/

## 📱 Mobile App Setup

1. Install **Expo Go** on your phone:
   - Android: Google Play Store
   - iOS: App Store

2. Make sure phone and computer are on same WiFi

3. In the "Web + Mobile" window, scan the QR code with:
   - Android: Expo Go app
   - iOS: Camera app

## 🎯 Manual Commands (If Needed)

### Install Everything
```bash
npm install
cd realtor-web\uilayers
npm install
cd ..\..
cd realtor-mobile
npm install
cd ..
cd realtor-web
pip install -r requirements.txt
```

### Run Django Backend
```bash
cd realtor-web
python manage.py runserver
```

### Run Web PWA
```bash
cd realtor-web\uilayers
npm run dev
```

### Run Mobile App
```bash
cd realtor-mobile
npm start
```

### Run Web + Mobile Together
```bash
npm run dev
```

## 🎨 Add Sample Property

1. Open http://localhost:8000/admin
2. Login with your admin credentials
3. Click **Properties** → **Add Property**
4. Fill in:
   - Title: Luxury Villa in Anna Nagar
   - Description: Beautiful 4BHK villa
   - Price: 12500000
   - Price Type: Sale
   - Bedrooms: 4
   - Bathrooms: 3
   - Location: Anna Nagar, Chennai
   - Image: https://images.unsplash.com/photo-1600596542815-ffad4c1539a9
   - Status: Available
5. Click **Save**
6. View at http://localhost:5173/properties

## 🐛 Troubleshooting

### Port Already in Use

**Find process using port:**
```bash
netstat -ano | findstr :8000
```

**Kill process:**
```bash
taskkill /PID <PID> /F
```

**Or use different port:**
```bash
python manage.py runserver 8001
```

### Module Not Found

**Reinstall npm packages:**
```bash
npm run install:all
```

**Reinstall Python packages:**
```bash
cd realtor-web
pip install -r requirements.txt
```

### Python Not Found

1. Install Python from https://python.org/
2. During installation, check "Add Python to PATH"
3. Restart Command Prompt
4. Verify: `python --version`

### npm Not Found

1. Install Node.js from https://nodejs.org/
2. Restart Command Prompt
3. Verify: `npm --version`

### Expo Not Connecting

**Try tunnel mode:**
```bash
cd realtor-mobile
npx expo start --tunnel
```

**Check WiFi:**
- Phone and computer must be on same network
- Disable VPN if active

### Django Errors

**Reset database:**
```bash
cd realtor-web
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**Check for errors:**
```bash
python manage.py check
```

## 📂 Project Structure

```
C:\tamil\realtor\
├── install.bat              ← Double-click to install
├── run-dev.bat              ← Double-click to run
├── package.json             ← npm configuration
├── shared\                  ← Shared code
│   ├── types\
│   ├── utils\
│   └── services\
├── realtor-web\             ← Django + React PWA
│   ├── manage.py
│   ├── requirements.txt
│   ├── realtor_project\
│   ├── properties\
│   ├── users\
│   ├── search\
│   └── uilayers\            ← React PWA
│       ├── package.json
│       ├── vite.config.ts
│       └── src\
└── realtor-mobile\          ← React Native Expo
    ├── package.json
    ├── app.json
    └── app\
```

## 🎯 Development Workflow

### Daily Development

1. **Start servers:**
   - Double-click `run-dev.bat`
   - OR run manually in 2 terminals

2. **Make changes:**
   - Edit files in VS Code
   - Changes auto-reload

3. **Test:**
   - Web: http://localhost:5173
   - Mobile: Expo Go app
   - API: http://localhost:8000/api

4. **Stop servers:**
   - Press Ctrl+C in terminals
   - OR close terminal windows

### Adding New Features

1. **Backend (Django):**
   - Edit models in `realtor-web/properties/models.py`
   - Run: `python manage.py makemigrations`
   - Run: `python manage.py migrate`

2. **Web (React):**
   - Add pages in `realtor-web/uilayers/src/pages/`
   - Add components in `realtor-web/uilayers/src/components/`

3. **Mobile (React Native):**
   - Add screens in `realtor-mobile/app/`
   - Add components in `realtor-mobile/src/modules/`

## 📚 Useful Commands

```bash
# Check versions
npm --version
python --version
node --version

# Django commands
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
python manage.py makemigrations

# npm commands
npm install
npm run dev
npm run web:dev
npm run mobile:dev

# View logs
python manage.py runserver --verbosity 3
```

## ✅ Verification Checklist

- [ ] Node.js installed (npm --version works)
- [ ] Python installed (python --version works)
- [ ] Dependencies installed (npm run install:all)
- [ ] Database migrated (python manage.py migrate)
- [ ] Superuser created (python manage.py createsuperuser)
- [ ] Django running (http://localhost:8000/admin)
- [ ] Web PWA running (http://localhost:5173)
- [ ] Mobile app running (Expo Go)

## 🎉 You're Ready!

Your Chennai Realtor development environment is complete and ready to use on Windows!

---

**Quick Start**: Double-click `install.bat` then `run-dev.bat`
**Need Help?** Check other documentation files
