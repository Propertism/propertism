# ⚡ QUICK START - Chennai Realtor

## 🚀 3-Step Setup

### 1️⃣ Install Dependencies (5 minutes)
```bash
# Install Node packages (web + mobile)
npm run install:all

# OR install manually:
npm install
cd realtor-web/uilayers && npm install
cd ../../realtor-mobile && npm install

# Install Python packages (Django)
cd realtor-web
pip install -r requirements.txt
```

### 2️⃣ Setup Database (2 minutes)
```bash
cd realtor-web

# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (your choice)
```

### 3️⃣ Run Everything (1 minute)
```bash
# Terminal 1: Django Backend
cd realtor-web
python manage.py runserver

# Terminal 2: Web + Mobile (from root)
npm run dev
```

## 🌐 Open These URLs

| What | URL | Use For |
|------|-----|---------|
| **Web App** | http://localhost:5173 | Browse properties |
| **Django Admin** | http://localhost:8000/admin | Add properties |
| **API** | http://localhost:8000/api/properties/ | Test API |
| **Mobile** | Expo Go App | Scan QR code |

## 📱 Mobile Setup

1. Install **Expo Go** on your phone (Play Store/App Store)
2. Run `yarn mobile:dev` from project root
3. Scan QR code with Expo Go (Android) or Camera (iOS)

## 🎯 Add Sample Property

1. Go to http://localhost:8000/admin
2. Login with your superuser credentials
3. Click **Properties** → **Add Property**
4. Fill in:
   - Title: "Luxury Villa in Anna Nagar"
   - Price: 12500000
   - Price Type: Sale
   - Bedrooms: 4
   - Bathrooms: 3
   - Location: "Anna Nagar, Chennai"
   - Image: https://images.unsplash.com/photo-1600596542815-ffad4c1539a9
   - Status: Available
5. Save
6. Refresh http://localhost:5173/properties

## 🐛 Common Issues

**Port already in use?**
```bash
# Kill process on port 8000
# Windows: netstat -ano | findstr :8000
# Then: taskkill /PID <PID> /F

# Or use different port
python manage.py runserver 8001
```

**Module not found?**
```bash
# Reinstall dependencies
npm run install:all
cd realtor-web && pip install -r requirements.txt
```

**Expo not connecting?**
- Ensure phone and computer on same WiFi
- Try: `cd realtor-mobile && npx expo start --tunnel`

## 📊 Project Structure

```
realtor/
├── shared/              ← Shared code (types, utils)
├── realtor-web/
│   ├── Django Backend   ← API (port 8000)
│   └── uilayers/        ← React PWA (port 5173)
└── realtor-mobile/      ← Expo app (port 19000)
```

## 🎨 Key Features

✅ Chennai INR formatting (₹5.2Cr, ₹45L)
✅ Mobile-first responsive design
✅ PWA (installable web app)
✅ REST API with pagination
✅ JWT authentication
✅ React Native mobile app
✅ Shared TypeScript types

## 📚 Full Documentation

- `README.md` - Overview
- `SETUP_GUIDE.md` - Detailed setup
- `PRODUCTION_READY.md` - Complete feature list

## 🎯 Next Steps

1. ✅ Setup complete
2. Add sample properties via admin
3. Test web app at localhost:5173
4. Test mobile app with Expo Go
5. Start customizing!

---

**Need Help?** Check `SETUP_GUIDE.md` for detailed instructions.
