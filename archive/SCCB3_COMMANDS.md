# SCCB-3 Quick Command Reference

## Setup Commands

### Install React Dependencies
```bash
cd realtor-web/uilayers/properties-spa
npm install
```

### Build React SPA
```bash
cd realtor-web/uilayers/properties-spa
npm run build
```

### Add Sample Properties
```bash
cd realtor-web
python manage.py shell < add_sample_properties.py
```

### Collect Static Files
```bash
cd realtor-web
python manage.py collectstatic --noinput
```

### Start Django Server
```bash
cd realtor-web
python manage.py runserver
```

## Development Commands

### Hot Reload React (Dev Mode)
```bash
cd realtor-web/uilayers/properties-spa
npm run dev
# Visit http://localhost:5173
```

### Rebuild After Changes
```bash
cd realtor-web/uilayers/properties-spa
npm run build
```

### Check CMS Status
```bash
cd realtor-web
python manage.py cms check
```

### View Migrations
```bash
cd realtor-web
python manage.py showmigrations cms
```

## Testing Commands

### Test API Endpoint
```bash
curl http://localhost:8000/api/properties/
```

### Test Static Files
```bash
ls realtor-web/static/dist/assets/
# Should show: properties.js, properties.css
```

### Django Shell (Add Properties)
```bash
cd realtor-web
python manage.py shell
```

```python
from properties.models import Property, PropertyType

# Create property type
pt = PropertyType.objects.create(name='Apartment', slug='apartment')

# Create property
Property.objects.create(
    title='Test Property',
    description='Test description',
    price=5000000,
    price_type='sale',
    bedrooms=3,
    bathrooms=2,
    area=1500,
    location='Chennai',
    property_type=pt
)
```

## URLs to Test

### Admin
```
http://localhost:8000/admin/
```

### API Endpoint
```
http://localhost:8000/api/properties/
```

### CMS Page (after creation)
```
http://localhost:8000/en/properties/
```

### React Dev Server
```
http://localhost:5173
```

## Troubleshooting Commands

### Clear Cache
```bash
cd realtor-web
python manage.py clear_cache
```

### Restart Server
```bash
# Press Ctrl+C to stop
cd realtor-web
python manage.py runserver
```

### Rebuild Everything
```bash
# Rebuild React
cd realtor-web/uilayers/properties-spa
npm run build

# Collect static
cd ../..
python manage.py collectstatic --noinput

# Restart server
python manage.py runserver
```

## File Locations

### React Source
```
realtor-web/uilayers/properties-spa/src/
```

### Build Output
```
realtor-web/static/dist/assets/
```

### Django Templates
```
realtor-web/uilayers/templates/properties/
```

### Django Views
```
realtor-web/properties/views.py
```

### AppHook
```
realtor-web/properties/cms_apps.py
```

## Quick Fixes

### React not loading?
```bash
cd realtor-web/uilayers/properties-spa
npm run build
cd ../..
python manage.py collectstatic --noinput
```

### Properties not showing?
```bash
cd realtor-web
python manage.py shell < add_sample_properties.py
```

### AppHook not available?
```bash
cd realtor-web
# Restart server (Ctrl+C then)
python manage.py runserver
```

### Static files 404?
```bash
cd realtor-web
python manage.py collectstatic --noinput
```

---

**Quick Start**: Run these 4 commands to get started:

```bash
cd realtor-web/uilayers/properties-spa && npm install && npm run build
cd ../.. && python manage.py shell < add_sample_properties.py
python manage.py runserver
```

Then visit: `http://localhost:8000/admin/` to create CMS page.
