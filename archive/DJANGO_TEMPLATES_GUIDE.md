# 🎨 Django Templates Guide - Reusable Components

## What Are Django Templates?

Django templates are **reusable HTML files** with special syntax that lets you:
- Create a master layout (base template)
- Extend it in child pages
- Include reusable components
- Pass dynamic data from views

## 🏗️ Template Inheritance Structure

```
base.html (Master Template)
    ├── home.html (extends base)
    ├── about.html (extends base)
    ├── contact.html (extends base)
    ├── properties/list.html (extends base)
    └── properties/detail.html (extends base)

Reusable Components (included in templates):
    ├── components/_header.html
    ├── components/_footer.html
    ├── components/_property-card.html
    ├── components/_form.html
    └── components/_pagination.html
```

## 📁 Your Template Structure

```
realtor-web/uilayers/templates/
├── base.html                    ← Master template (header, footer, layout)
├── home.html                    ← Homepage (extends base)
├── about.html                   ← About page (extends base)
├── contact.html                 ← Contact page (extends base)
│
├── components/                  ← Reusable components
│   ├── _header.html            ← Navigation bar
│   ├── _footer.html            ← Footer
│   ├── _property-card.html     ← Property display card
│   ├── _form.html              ← Form components
│   └── _pagination.html        ← Page navigation
│
├── properties/                  ← Property pages
│   ├── list.html               ← Property listing page
│   └── detail.html             ← Single property page
│
├── search/                      ← Search pages
│   └── results.html            ← Search results page
│
└── users/                       ← User pages
    ├── login.html              ← Login page
    ├── register.html           ← Registration page
    ├── dashboard.html          ← User dashboard
    ├── profile.html            ← User profile
    ├── my_inquiries.html       ← User inquiries
    ├── my_maintenance.html     ← Maintenance requests
    └── my_tickets.html         ← Support tickets
```

## 🎯 How Template Inheritance Works

### 1. Base Template (Master Layout)

**File**: `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Propertism{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <!-- Include reusable header -->
    {% include "components/_header.html" %}
    
    <!-- Main content area (filled by child templates) -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Include reusable footer -->
    {% include "components/_footer.html" %}
    
    <script src="/static/js/utils.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

**Key Parts**:
- `{% block title %}` - Placeholder for page title
- `{% block content %}` - Placeholder for page content
- `{% include %}` - Insert reusable components
- `{% block scripts %}` - Placeholder for page-specific JavaScript

### 2. Child Template (Extends Base)

**File**: `templates/home.html`

```html
{% extends "base.html" %}

{% block title %}Home - Propertism{% endblock %}

{% block content %}
<div class="hero">
    <div class="container">
        <h1>NRI Property Management Services In India, Chennai</h1>
        <p>We manage your property when you are far from the nation</p>
        <div class="hero-actions">
            <a href="/properties/" class="btn btn-primary">Browse Properties</a>
            <a href="/contact/" class="btn btn-secondary">Contact Us</a>
        </div>
    </div>
</div>

<div class="services-section">
    <div class="container">
        <h2>Our Services</h2>
        <!-- Services content -->
    </div>
</div>

<div class="featured-properties">
    <div class="container">
        <h2>Featured Properties</h2>
        <div class="row">
            {% for property in featured_properties %}
            <div class="col">
                {% include "components/_property-card.html" with property=property %}
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

**Key Parts**:
- `{% extends "base.html" %}` - Inherit from base template
- `{% block title %}` - Override title block
- `{% block content %}` - Fill content block
- `{% for %}` - Loop through data
- `{% include %}` - Insert reusable component

### 3. Reusable Component

**File**: `templates/components/_property-card.html`

```html
<div class="property-card">
    <img src="{{ property.image }}" alt="{{ property.title }}">
    <div class="property-info">
        <h3>{{ property.title }}</h3>
        <p class="location">{{ property.location }}</p>
        <p class="price">₹{{ property.price }}</p>
        <div class="property-meta">
            <span>🛏️ {{ property.bedrooms }} Beds</span>
            <span>🚿 {{ property.bathrooms }} Baths</span>
        </div>
        <a href="/properties/{{ property.id }}/" class="btn btn-primary">View Details</a>
    </div>
</div>
```

**Usage in other templates**:
```html
{% include "components/_property-card.html" with property=property %}
```

## 🔄 Template Syntax Reference

### Variables
```html
{{ variable_name }}              <!-- Display variable -->
{{ property.title }}             <!-- Access object attribute -->
{{ property.price|floatformat:2 }} <!-- Apply filter -->
```

### Tags
```html
{% extends "base.html" %}        <!-- Inherit from template -->
{% block content %}{% endblock %} <!-- Define block -->
{% include "header.html" %}      <!-- Include template -->
{% for item in items %}          <!-- Loop -->
{% if condition %}               <!-- Conditional -->
{% url 'view_name' %}            <!-- Generate URL -->
{% static 'css/style.css' %}     <!-- Static file URL -->
```

### Filters
```html
{{ value|lower }}                <!-- Lowercase -->
{{ value|upper }}                <!-- Uppercase -->
{{ value|title }}                <!-- Title Case -->
{{ value|date:"Y-m-d" }}         <!-- Format date -->
{{ value|default:"N/A" }}        <!-- Default value -->
{{ value|length }}               <!-- Get length -->
{{ value|truncatewords:10 }}     <!-- Truncate text -->
```

### Comments
```html
{# This is a comment #}
{% comment %}
Multi-line comment
{% endcomment %}
```

## 📝 Common Template Patterns

### 1. Loop Through Items
```html
{% for property in properties %}
    <div class="property">
        <h3>{{ property.title }}</h3>
        <p>{{ property.price }}</p>
    </div>
{% empty %}
    <p>No properties found.</p>
{% endfor %}
```

### 2. Conditional Display
```html
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}
```

### 3. Include with Context
```html
{% include "components/_property-card.html" with property=property %}
```

### 4. URL Generation
```html
<a href="{% url 'property_detail' property.id %}">View Property</a>
```

### 5. Static Files
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

## 🎨 How Views Pass Data to Templates

**File**: `realtor-web/uilayers/views.py`

```python
from django.shortcuts import render
from properties.models import Property

def home(request):
    # Get data from database
    featured_properties = Property.objects.filter(status='available')[:3]
    
    # Pass data to template
    context = {
        'featured_properties': featured_properties,
    }
    
    # Render template with context
    return render(request, 'home.html', context)
```

**In template** (`home.html`):
```html
{% for property in featured_properties %}
    <h3>{{ property.title }}</h3>
{% endfor %}
```

## ✅ Benefits of Template Inheritance

### 1. DRY (Don't Repeat Yourself)
- Write header/footer once
- Use on all pages
- Change once, update everywhere

### 2. Consistent Design
- All pages share same layout
- Same navigation everywhere
- Uniform styling

### 3. Easy Maintenance
- Update header → All pages updated
- Change footer → All pages updated
- Modify base → All pages affected

### 4. Reusable Components
- Property card used in multiple places
- Forms used in contact, login, register
- Pagination used in all listings

## 📋 Adding a New Page (Step by Step)

### Step 1: Create Template
**File**: `templates/services.html`

```html
{% extends "base.html" %}

{% block title %}Services - Propertism{% endblock %}

{% block content %}
<div class="container">
    <h1>Our Services</h1>
    <p>We offer comprehensive property management services...</p>
</div>
{% endblock %}
```

### Step 2: Create View
**File**: `uilayers/views.py`

```python
def services(request):
    return render(request, 'services.html')
```

### Step 3: Add URL
**File**: `uilayers/urls.py`

```python
urlpatterns = [
    path('services/', views.services, name='services'),
]
```

### Step 4: Link to Page
**In any template**:
```html
<a href="{% url 'services' %}">Our Services</a>
```

Done! Your new page automatically has header, footer, and styling!

## 🔧 Customizing Components

### Update Header for All Pages
**File**: `templates/components/_header.html`

```html
<header class="site-header">
    <div class="container">
        <div class="logo">
            <a href="/">Propertism</a>
        </div>
        <nav class="main-nav">
            <a href="/">HOME</a>
            <a href="/properties/">PROPERTIES</a>
            <a href="/about/">ABOUT</a>
            <a href="/contact/">CONTACT</a>
            {% if user.is_authenticated %}
                <a href="/dashboard/">DASHBOARD</a>
                <a href="/logout/">LOGOUT</a>
            {% else %}
                <a href="/login/">LOGIN</a>
                <a href="/register/">SIGN UP</a>
            {% endif %}
        </nav>
    </div>
</header>
```

This header appears on ALL pages automatically!

## 🎯 Template Best Practices

### 1. Use Meaningful Block Names
```html
{% block page_title %}{% endblock %}
{% block hero_section %}{% endblock %}
{% block main_content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

### 2. Keep Components Small
- One component = One purpose
- `_property-card.html` - Just property card
- `_form.html` - Just form elements
- `_pagination.html` - Just pagination

### 3. Use Descriptive Variable Names
```html
{{ property.title }}           <!-- Good -->
{{ p.t }}                      <!-- Bad -->

{{ user.full_name }}           <!-- Good -->
{{ u.n }}                      <!-- Bad -->
```

### 4. Add Comments
```html
{# Featured properties section #}
<div class="featured-properties">
    {% for property in featured_properties %}
        {# Display each property card #}
        {% include "components/_property-card.html" %}
    {% endfor %}
</div>
```

### 5. Handle Empty States
```html
{% for property in properties %}
    <div class="property">{{ property.title }}</div>
{% empty %}
    <p>No properties available at the moment.</p>
{% endfor %}
```

## 🚀 Your Current Setup

### What You Have
- ✅ Base template with header/footer
- ✅ Multiple page templates (home, about, contact)
- ✅ Reusable components (property card, forms, pagination)
- ✅ Property listing and detail pages
- ✅ User pages (login, register, dashboard)

### What You Can Do
1. **Edit any template** - Changes reflect immediately
2. **Add new pages** - Extend base.html
3. **Create components** - Make reusable pieces
4. **Pass data from views** - Display dynamic content
5. **Customize styling** - Edit CSS files

## 📚 Quick Reference

### File Locations
```
Templates:     realtor-web/uilayers/templates/
Views:         realtor-web/uilayers/views.py
URLs:          realtor-web/uilayers/urls.py
Static Files:  realtor-web/static/
CSS:           realtor-web/static/css/
JavaScript:    realtor-web/static/js/
```

### Common Commands
```bash
# View template in browser
http://localhost:8000/

# Edit template
code realtor-web/uilayers/templates/home.html

# Restart Django (if needed)
cd realtor-web
python manage.py runserver
```

## 🎉 Summary

Django templates are **reusable HTML files** that:
- Use inheritance (base → child)
- Include components (header, footer, cards)
- Display dynamic data from views
- Keep your code DRY and maintainable

**Change one file → Update all pages!** That's the power of template inheritance! 🚀

---

**File Location**: `DJANGO_TEMPLATES_GUIDE.md`
**Last Updated**: February 22, 2026
**For**: Chennai Realtor Project
