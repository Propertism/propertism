# SCCB-3 Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Build React SPA (1 min)
```bash
cd realtor-web/uilayers/properties-spa
npm install
npm run build
```

### Step 2: Add Sample Data (30 sec)
```bash
cd ../..
python manage.py shell < add_sample_properties.py
```

### Step 3: Start Server (10 sec)
```bash
python manage.py runserver
```

### Step 4: Create CMS Page (2 min)
1. Visit: `http://localhost:8000/admin/`
2. Click **Pages** → **Add Page**
3. Title: `Properties`, Slug: `properties`
4. Click **Advanced Settings** tab
5. Application: Select **"Properties React SPA"**
6. Click **Save** → **Publish**

### Step 5: View Your Page (10 sec)
```
http://localhost:8000/en/properties/
```

## ✅ What You'll See

- Premium black/white design
- 6 sample properties in grid view
- Grid/Map toggle buttons
- Responsive layout
- Hover effects on property cards

## 📁 Key Files

```
realtor-web/
├── uilayers/properties-spa/     ← React SPA source
│   ├── src/
│   │   ├── App.tsx              ← Main app
│   │   └── components/
│   │       ├── PropertyGrid.tsx ← Property cards
│   │       └── PropertyMap.tsx  ← Google Maps
│   └── package.json
│
├── static/dist/assets/          ← Build output
│   ├── properties.js            ← React bundle
│   └── properties.css           ← Styles
│
├── properties/
│   ├── cms_apps.py              ← AppHook
│   └── views.py                 ← React view
│
└── uilayers/templates/properties/
    └── cms_app.html             ← React mount point
```

## 🔧 Common Commands

### Rebuild React
```bash
cd realtor-web/uilayers/properties-spa
npm run build
```

### Add More Properties
```bash
cd realtor-web
python manage.py shell
```
```python
from properties.models import Property
Property.objects.create(
    title='New Property',
    price=5000000,
    bedrooms=3,
    bathrooms=2,
    area=1500,
    location='Chennai'
)
```

### Test API
```bash
curl http://localhost:8000/api/properties/
```

## 🐛 Troubleshooting

### React not loading?
```bash
cd realtor-web/uilayers/properties-spa
npm run build
```

### No properties showing?
```bash
cd realtor-web
python manage.py shell < add_sample_properties.py
```

### AppHook not available?
```bash
# Restart server (Ctrl+C then)
python manage.py runserver
```

## 📚 Documentation

- **SCCB3_DONE.md** - Completion checklist
- **SCCB3_TESTING_GUIDE.md** - Detailed testing
- **SCCB3_COMMANDS.md** - All commands
- **SCCB3_VISUAL_GUIDE.md** - Design specs

## 🎯 Success Criteria

✅ React SPA builds without errors
✅ Static files exist in `static/dist/assets/`
✅ API returns property data
✅ CMS page created and published
✅ Properties display in grid view
✅ Map view shows Google Maps
✅ Toggle between views works
✅ No console errors

## 🎨 Design Features

- Sharp edges (no rounded corners)
- Black and white colors
- Inter font family
- Hover effects (color inversion)
- Responsive grid (1-3 columns)
- Clean, minimal aesthetic

## 🔗 URLs

| URL | Purpose |
|-----|---------|
| `http://localhost:8000/admin/` | Django admin |
| `http://localhost:8000/api/properties/` | API endpoint |
| `http://localhost:8000/en/properties/` | CMS page |
| `http://localhost:5173` | React dev server |

## ⚡ Performance

- Build time: 1.59s
- Bundle size: 182.47 kB (61.24 kB gzipped)
- Load time: < 1s
- API response: < 500ms

## 🎉 You're Done!

SCCB-3 is now complete. The React SPA is embedded in Django CMS and ready to use.

**Next**: Create more CMS pages or customize the React components!

---

**Status**: ✅ READY
**SCCB**: SCCB-3
**Date**: Feb 22, 2026
