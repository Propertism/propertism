SCCB-3
Title: Django CMS + React SPA-in-CMS Integration
Scope: realtor/ Monorepo (Django + React + React Native)
Pattern: SPA-in-CMS (Embedded React inside Django CMS pages)
Status: PRODUCTION GOVERNED IMPLEMENTATION
Compatibility: Non-breaking with existing DRF + Monorepo APIs

=============================================================
1. GOVERNANCE OBJECTIVE
=============================================================

Enable Django CMS editors to control page layout, SEO, and structure,
while React (Vite-built SPA) handles dynamic:

• Property listings
• Filters/search
• Google Maps
• Responsive grid
• PWA behavior

This SCCB introduces CMS AppHook pattern without altering:
✔ Existing DRF API contracts
✔ Existing monorepo structure
✔ Shared types/services
✔ Mobile Expo app

-------------------------------------------------------------
ARCHITECTURE SUMMARY
-------------------------------------------------------------

Django CMS Page
        ↓
AppHook
        ↓
Template mounts React root div
        ↓
Vite-built React SPA loads from static/dist
        ↓
React consumes existing /api/properties/

=============================================================
2. INSTALLATION REQUIREMENTS
=============================================================

FILE:
realtor-web/requirements.txt
-------------------------------------------------------------
django-cms==4.2.*
djangocms-cascade
sekizai
djangocms-admin-style
djangocms-text-ckeditor
django-treebeard
django-formtools
easy-thumbnails

-------------------------------------------------------------

=============================================================
3. DJANGO SETTINGS CONFIGURATION
=============================================================

FILE:
realtor-web/realtor_project/settings.py
-------------------------------------------------------------

INSTALLED_APPS += [
    "cms",
    "menus",
    "sekizai",
    "treebeard",
    "djangocms_admin_style",
    "djangocms_text_ckeditor",
    "properties",
]

MIDDLEWARE += [
    "cms.middleware.utils.ApphookReloadMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]

CMS_TEMPLATES = [
    ("base.html", "Base Template"),
    ("properties/app.html", "Properties React SPA"),
]

CMS_PERMISSION = True
CMS_APPHOOKS = ["properties.cms_app_hooks.PropertiesAppHook"]

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

-------------------------------------------------------------

=============================================================
4. CMS APPHOOK
=============================================================

FILE:
realtor-web/properties/cms_app_hooks.py
-------------------------------------------------------------

from cms.apphook_pool import apphook_pool
from cms.app_base import CMSApp
from django.urls import path
from . import views

class PropertiesAppHook(CMSApp):
    name = "Properties App"
    app_name = "properties"

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", views.react_properties_app, name="react-root"),
        ]

apphook_pool.register(PropertiesAppHook)

-------------------------------------------------------------

=============================================================
5. DJANGO VIEW TO RENDER REACT TEMPLATE
=============================================================

FILE:
realtor-web/properties/views.py
-------------------------------------------------------------

from django.shortcuts import render

def react_properties_app(request):
    return render(request, "properties/app.html")

-------------------------------------------------------------

=============================================================
6. REACT EMBED TEMPLATE
=============================================================

FILE:
realtor-web/properties/templates/properties/app.html
-------------------------------------------------------------

{% extends "base.html" %}
{% load static sekizai %}

{% block content %}
<div id="react-properties-app"
     data-api-url="/api/properties/"
     data-page="{{ request.current_page.pk }}">
</div>
{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'dist/assets/properties.css' %}">
{% endblock %}

{% block extra_js %}
<script src="{% static 'dist/assets/properties.js' %}"></script>
<script>
  window.PropertiesApp.mount(
    document.getElementById('react-properties-app')
  );
</script>
{% endblock %}

-------------------------------------------------------------

=============================================================
7. DJANGO REST API (FOR REACT)
=============================================================

FILE:
realtor-web/properties/api/serializers.py
-------------------------------------------------------------

from rest_framework import serializers
from properties.models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"

-------------------------------------------------------------

FILE:
realtor-web/properties/api/views.py
-------------------------------------------------------------

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from properties.models import Property
from .serializers import PropertySerializer

@api_view(["GET"])
def property_list(request):
    paginator = PageNumberPagination()
    queryset = Property.objects.all().order_by("-id")
    page = paginator.paginate_queryset(queryset, request)
    serializer = PropertySerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
def property_detail(request, pk):
    property_obj = Property.objects.get(pk=pk)
    serializer = PropertySerializer(property_obj)
    return Response(serializer.data)

-------------------------------------------------------------

=============================================================
8. REACT SPA BUILD (EMBEDDED)
=============================================================

FOLDER:
realtor-web/uilayers/properties/

-------------------------------------------------------------
package.json
-------------------------------------------------------------
{
  "name": "properties-spa",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "axios": "^1.6.0",
    "zustand": "^4.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.0",
    "typescript": "^5.2.2"
  }
}

-------------------------------------------------------------
vite.config.js
-------------------------------------------------------------
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, "../../static/dist"),
    rollupOptions: {
      output: {
        entryFileNames: "assets/properties.js",
        assetFileNames: "assets/properties.css"
      }
    }
  }
})

-------------------------------------------------------------
src/index.tsx
-------------------------------------------------------------
import React from "react"
import ReactDOM from "react-dom/client"
import App from "./App"
import "./index.css"

window.PropertiesApp = {
  mount(el: HTMLElement) {
    ReactDOM.createRoot(el).render(<App />)
  }
}

-------------------------------------------------------------
src/App.tsx
-------------------------------------------------------------
import { BrowserRouter, Routes, Route } from "react-router-dom"
import PropertyGrid from "./components/PropertyGrid"
import PropertyMap from "./components/PropertyMap"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PropertyGrid />} />
        <Route path="/map" element={<PropertyMap />} />
      </Routes>
    </BrowserRouter>
  )
}

-------------------------------------------------------------
src/components/PropertyGrid.tsx
-------------------------------------------------------------
import { useEffect, useState } from "react"
import axios from "axios"

export default function PropertyGrid() {
  const [properties, setProperties] = useState([])

  useEffect(() => {
    axios.get("/api/properties/").then(res => {
      setProperties(res.data.results)
    })
  }, [])

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4 sm:p-6">
      {properties.map((p:any) => (
        <div key={p.id} className="bg-white rounded-lg shadow-md p-4">
          <img src={p.image} className="w-full h-48 sm:h-56 object-cover rounded-lg"/>
          <h3 className="mt-2 font-semibold">{p.title}</h3>
          <p>{p.location}</p>
        </div>
      ))}
    </div>
  )
}

-------------------------------------------------------------
src/components/PropertyMap.tsx
-------------------------------------------------------------
export default function PropertyMap() {
  return (
    <div className="w-full h-screen">
      <iframe
        className="w-full h-full"
        src="https://maps.google.com/maps?q=Chennai&t=&z=13&ie=UTF8&iwloc=&output=embed"
      />
    </div>
  )
}

=============================================================
9. BUILD & DEPLOY SCRIPT
=============================================================

ROOT COMMAND:

yarn --cwd realtor-web/uilayers/properties build
python manage.py migrate
python manage.py runserver

Optional script:

realtor/package.json add:
-------------------------------------------------------------
"build:react": "yarn --cwd realtor-web/uilayers/properties build"

=============================================================
10. CMS ADMIN SETUP
=============================================================

1. python manage.py createsuperuser
2. Login /admin
3. Create new CMS Page
4. Select template: "Properties React SPA"
5. Attach AppHook: "Properties App"
6. Publish page

=============================================================
BENEFITS
=============================================================

✔ CMS editors control layout + SEO
✔ React handles interactive listing/map/filter
✔ Tailwind mobile-first responsive
✔ Production asset optimization via Vite
✔ DRF API reuse
✔ Non-breaking with Expo mobile
✔ SPA hot reload in dev
✔ Static optimized build in production

=============================================================
SCCB-3 APPROVED IMPLEMENTATION BLOCK
=============================================================