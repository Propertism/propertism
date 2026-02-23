# Quick Reference Card

## 🚀 Start Development
```bash
run-web-only.bat
```

## 🌐 URLs

### Production (Use This)
```
http://localhost:8000/en/              # Homepage
http://localhost:8000/en/properties/   # Property search
http://localhost:8000/en/admin/        # Admin panel
http://localhost:8000/api/properties/  # API
```

### Development (Optional)
```
http://localhost:5173/                 # React hot reload
```

## 📱 Mobile App
```bash
cd realtor-mobile
npm start
```
API: `http://localhost:8000/api`

## 🔨 Build Production
```bash
build-production.bat
```

## 📊 Architecture
```
Django (Port 8000)
├── APIs (/api/*)
├── Web Pages (/en/*)
└── Static Files (/static/*)
        ▲           ▲
        │           │
    Mobile      Web Browser
```

## 🎯 Key Points
- **Port 8000**: Production server (deploy this)
- **Port 5173**: Dev only (hot reload)
- **Mobile**: Uses APIs from port 8000
- **No impact**: Mobile app unchanged

## 📚 Documentation
- `PRODUCTION_ARCHITECTURE.md` - Full architecture
- `QUICK_START_PRODUCTION.md` - Getting started
- `ARCHITECTURE_VISUAL.md` - Visual diagrams
- `CONSOLIDATION_COMPLETE.md` - What changed

## ✅ Status
**Production Ready** - Deploy anytime!
