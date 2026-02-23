# Django CMS 4.x Access Guide

## Important: Django CMS 4.x Works Differently

In Django CMS 4.x, pages are NOT managed through the Django admin sidebar. Instead, they're managed through the CMS toolbar on the frontend.

## How to Create a CMS Page

### Step 1: Start the Server
```bash
cd realtor-web
python manage.py runserver
```

### Step 2: Visit the Root URL
```
http://localhost:8000/
```

### Step 3: Login via CMS Toolbar
1. You'll see a toolbar at the top of the page
2. Click "Login" in the toolbar
3. Enter your superuser credentials

### Step 4: Create a Page
1. After login, the CMS toolbar will show more options
2. Click "Create" or "Page" in the toolbar
3. Select "New Page"
4. Fill in:
   - Title: "Properties"
   - Slug: "properties"
5. In Advanced Settings:
   - Template: Select "Properties React SPA"
   - Application: Select "Properties React SPA"
6. Click "Save"
7. Click "Publish" in the toolbar

### Step 5: View Your Page
```
http://localhost:8000/en/properties/
```

## Alternative: Use Management Command

We've created a management command to create the page programmatically:

```bash
cd realtor-web
python manage.py create_cms_page
```

Then visit: `http://localhost:8000/en/properties/`

## Troubleshooting

### No CMS Toolbar Showing?
1. Make sure you're logged in as superuser
2. Check that `DEBUG = True` in settings.py
3. Clear browser cache and reload

### Can't Login?
Create a superuser:
```bash
python manage.py createsuperuser
```

### Page Not Found?
The URL pattern is: `http://localhost:8000/en/properties/`
Note the `/en/` language prefix!

## Direct Access (Bypass CMS Page Creation)

Since we have the React SPA built and the AppHook configured, you can also access the properties directly through the AppHook URL:

```
http://localhost:8000/en/properties/
```

This should work even without creating a CMS page, as the AppHook is registered.

## What You Should See

Once you access `/en/properties/`, you should see:
- Premium black/white design
- 6 property cards in grid view
- Grid/Map toggle buttons
- Responsive layout
- Hover effects

## Next Steps

1. Start the server: `python manage.py runserver`
2. Visit: `http://localhost:8000/en/properties/`
3. If it works, you're done!
4. If not, try creating the CMS page via the toolbar

---

**Note**: Django CMS 4.x moved away from the traditional admin interface for page management. Everything is now done through the frontend toolbar for a better editing experience.
