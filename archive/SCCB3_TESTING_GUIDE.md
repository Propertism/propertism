# SCCB-3 Testing Guide

## Quick Start Testing

### Step 1: Add Sample Properties

```bash
cd realtor-web
python manage.py shell < add_sample_properties.py
```

This will create:
- 3 property types (Apartment, Villa, Independent House)
- 6 sample properties with images from Unsplash

### Step 2: Start Django Server

```bash
python manage.py runserver
```

### Step 3: Test API Endpoint

Open browser: `http://localhost:8000/api/properties/`

You should see JSON response with 6 properties.

### Step 4: Create CMS Page

1. Go to: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Click **Pages** in sidebar
4. Click **Add Page** button
5. Fill in:
   - **Title**: Properties
   - **Slug**: properties
6. Click **Advanced Settings** tab
7. **Application**: Select "Properties React SPA"
8. Click **Save**
9. Click **Publish** button (top right)

### Step 5: View React SPA

Go to: `http://localhost:8000/en/properties/`

You should see:
- Premium black/white design
- Grid/Map toggle buttons
- 6 property cards with:
  - Property images
  - Title and location
  - Price in INR format
  - Bedrooms, bathrooms, area
  - Hover effect (black background, white text)

## What to Test

### ✅ Visual Design
- [ ] Sharp edges (no rounded corners)
- [ ] Black and white color scheme
- [ ] Inter font family
- [ ] Clean, minimal layout
- [ ] Responsive grid (1 col mobile, 2 col tablet, 3 col desktop)

### ✅ Functionality
- [ ] Grid view shows property cards
- [ ] Map view shows Google Maps
- [ ] Toggle between Grid/Map works
- [ ] Property data loads from API
- [ ] Images display correctly
- [ ] Prices formatted as INR (₹)
- [ ] Hover effects work on cards

### ✅ Integration
- [ ] CMS page loads without errors
- [ ] React app mounts in CMS template
- [ ] Static files (JS/CSS) load correctly
- [ ] API endpoint returns data
- [ ] No console errors

## Troubleshooting

### Properties not showing?

**Check API:**
```bash
curl http://localhost:8000/api/properties/
```

**Add properties manually:**
```bash
python manage.py shell
>>> from properties.models import Property, PropertyType
>>> PropertyType.objects.create(name='Apartment', slug='apartment')
>>> Property.objects.create(
...     title='Test Property',
...     description='Test',
...     price=5000000,
...     bedrooms=3,
...     bathrooms=2,
...     area=1500,
...     location='Chennai'
... )
```

### React app not loading?

**Check static files:**
```bash
ls realtor-web/static/dist/assets/
# Should show: properties.js, properties.css
```

**Rebuild React SPA:**
```bash
cd realtor-web/uilayers/properties-spa
npm run build
```

**Collect static files:**
```bash
cd realtor-web
python manage.py collectstatic --noinput
```

### CMS page 404?

**Check URL pattern:**
- Correct: `http://localhost:8000/en/properties/`
- Wrong: `http://localhost:8000/properties/`

CMS uses i18n patterns, so `/en/` prefix is required.

### AppHook not available?

**Restart Django server:**
```bash
# Ctrl+C to stop
python manage.py runserver
```

**Check AppHook registration:**
```bash
python manage.py cms check
```

## Browser Console Checks

Open browser DevTools (F12) and check:

### Console Tab
- No JavaScript errors
- Should see: "React app mounted" or similar

### Network Tab
- `/api/properties/` returns 200 status
- `properties.js` loads successfully
- `properties.css` loads successfully
- Images load from Unsplash

### Elements Tab
- `<div id="react-properties-app">` exists
- React components rendered inside

## Performance Checks

### Build Size
```
properties.js: 182.47 kB (61.24 kB gzipped)
properties.css: 7.23 kB (2.13 kB gzipped)
```

### Load Time
- Initial page load: < 1s
- API response: < 500ms
- React mount: < 200ms

## Next Steps After Testing

Once everything works:

1. **Add More Properties**: Use Django admin to add real properties
2. **Customize Design**: Edit `PropertyGrid.tsx` for layout changes
3. **Add Filters**: Implement location, price, bedroom filters
4. **Property Details**: Add modal or detail page
5. **Google Maps Integration**: Add property markers on map
6. **Search**: Implement search functionality

## Development Workflow

### Make Changes to React
```bash
cd realtor-web/uilayers/properties-spa
# Edit src/components/PropertyGrid.tsx
npm run build
# Refresh browser
```

### Make Changes to Django
```bash
cd realtor-web
# Edit properties/views.py or templates
# Django auto-reloads, just refresh browser
```

### Hot Reload Development
```bash
cd realtor-web/uilayers/properties-spa
npm run dev
# Visit http://localhost:5173 for hot reload
```

## Success Criteria

✅ CMS page created and published
✅ React SPA loads in CMS page
✅ Properties display in grid view
✅ Map view shows Google Maps
✅ Toggle between views works
✅ Premium design matches specification
✅ No console errors
✅ API integration working

---

**Status**: Ready for Testing
**SCCB**: SCCB-3 Complete
