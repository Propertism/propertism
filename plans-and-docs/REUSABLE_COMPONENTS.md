# 🧩 Reusable Components & Methods

**Project**: Propertism Django  
**Style Guide**: No emojis, no rounded corners, enterprise-grade

---

## 📁 Component Structure

```
uilayers/templates/
├── base.html                    # Base template with header/footer
├── components/
│   ├── _header.html             # Navigation header
│   ├── _footer.html             # Footer
│   ├── _property-card.html      # Property card component
│   ├── _form.html               # Form wrapper
│   ├── _pagination.html         # Pagination component
│   └── _alert.html              # Alert messages
├── home.html
├── properties/
│   ├── list.html
│   └── detail.html
├── contact.html
├── about.html
└── search/
    └── results.html
```

---

## 🎨 Design System

### Colors (Enterprise Palette)
```css
--primary: #0056b3;
--secondary: #6c757d;
--success: #28a745;
--danger: #dc3545;
--warning: #ffc107;
--info: #17a2b8;
--light: #f8f9fa;
--dark: #343a40;
--border: #dee2e6;
```

### Typography
- **Headings**: 24px, 20px, 18px, 16px, 14px
- **Body**: 14px
- **Font Family**: Arial, Helvetica, sans-serif

### Spacing
- **Container**: 1200px max-width
- **Padding**: 20px
- **Margin**: 15px

### Borders
- **Border Radius**: 0px (no rounded corners)
- **Border Width**: 1px
- **Border Style**: solid

---

## 🧩 Reusable Components

### 1. Header Component
```html
<!-- components/_header.html -->
<header class="header">
    <div class="container">
        <div class="header-content">
            <div class="logo">
                <a href="/">Propertism</a>
            </div>
            <nav class="nav">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/properties/">Properties</a></li>
                    <li><a href="/about/">About</a></li>
                    <li><a href="/contact/">Contact</a></li>
                </ul>
            </nav>
        </div>
    </div>
</header>
```

### 2. Footer Component
```html
<!-- components/_footer.html -->
<footer class="footer">
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h4>Propertism</h4>
                <p>NRI Property Management Services</p>
            </div>
            <div class="footer-section">
                <h4>Contact</h4>
                <p>Chennai, Tamil Nadu</p>
                <p>+91 86670 20798</p>
            </div>
            <div class="footer-section">
                <h4>Quick Links</h4>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/properties/">Properties</a></li>
                    <li><a href="/contact/">Contact</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Propertism. All rights reserved.</p>
        </div>
    </div>
</footer>
```

### 3. Property Card Component
```html
<!-- components/_property-card.html -->
<div class="property-card">
    <div class="property-image">
        <img src="{{ property.image_url }}" alt="{{ property.title }}">
    </div>
    <div class="property-info">
        <h3 class="property-title">
            <a href="{{ property.get_absolute_url }}">{{ property.title }}</a>
        </h3>
        <p class="property-price">{{ property.price }}</p>
        <p class="property-location">{{ property.location }}</p>
        <div class="property-features">
            <span>{{ property.bedrooms }} Beds</span>
            <span>{{ property.bathrooms }} Baths</span>
            <span>{{ property.area }} sqft</span>
        </div>
    </div>
</div>
```

### 4. Form Component
```html
<!-- components/_form.html -->
<form class="form" method="post">
    {% csrf_token %}
    <div class="form-group">
        <label for="{{ form.field.name }}" class="form-label">
            {{ form.field.label }}
        </label>
        {{ form.field }}
        {% if form.field.errors %}
            <div class="form-error">{{ form.field.errors }}</div>
        {% endif %}
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### 5. Pagination Component
```html
<!-- components/_pagination.html -->
<div class="pagination">
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}" class="btn btn-secondary">Previous</a>
    {% endif %}
    
    <span class="pagination-info">
        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
    </span>
    
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}" class="btn btn-secondary">Next</a>
    {% endif %}
</div>
```

### 6. Alert Component
```html
<!-- components/_alert.html -->
<div class="alert alert-{{ alert.type }}">
    {{ alert.message }}
</div>
```

---

## 🛠️ Reusable Methods

### JavaScript Utility Functions
```javascript
// static/js/utils.js

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Get URL parameter
function getUrlParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}
```

### Python Utility Functions
```python
# uilayers/utils.py

from django.utils.text import slugify

def generate_slug(text):
    """Generate URL-friendly slug from text"""
    return slugify(text)

def format_price(price):
    """Format price with currency symbol"""
    return f"₹{price:,.0f}"

def get_property_type_icon(property_type):
    """Get icon for property type"""
    icons = {
        'house': 'home',
        'villa': 'villa',
        'apartment': 'building',
        'plot': 'land',
        'commercial': 'building',
        'industrial': 'factory'
    }
    return icons.get(property_type, 'property')
```

---

## 📐 CSS Utility Classes
```css
/* static/css/utilities.css */

/* Layout */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin: 0 -15px;
}

.col {
    flex: 1;
    padding: 0 15px;
}

/* Typography */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.font-bold { font-weight: bold; }
.font-medium { font-weight: 500; }
.font-light { font-weight: 300; }

/* Spacing */
.p-0 { padding: 0; }
.p-1 { padding: 10px; }
.p-2 { padding: 20px; }
.p-3 { padding: 30px; }

.m-0 { margin: 0; }
.m-1 { margin: 10px; }
.m-2 { margin: 20px; }
.m-3 { margin: 30px; }

/* Colors */
.text-primary { color: #0056b3; }
.text-secondary { color: #6c757d; }
.text-success { color: #28a745; }
.text-danger { color: #dc3545; }

.bg-primary { background-color: #0056b3; }
.bg-secondary { background-color: #6c757d; }
.bg-light { background-color: #f8f9fa; }

/* Borders */
.border { border: 1px solid #dee2e6; }
.border-0 { border: none; }

/* Display */
.d-flex { display: flex; }
.d-block { display: block; }
.d-none { display: none; }

/* Flex */
.flex-row { flex-direction: row; }
.flex-col { flex-direction: column; }
.justify-center { justify-content: center; }
.align-center { align-items: center; }
```

---

## 📋 Template Inheritance

### Base Template
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Propertism{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="stylesheet" href="/static/css/utilities.css">
</head>
<body>
    {% include "components/_header.html" %}
    
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>
    
    {% include "components/_footer.html" %}
    
    <script src="/static/js/utils.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Page Template Example
```html
<!-- home.html -->
{% extends "base.html" %}

{% block title %}Home - Propertism{% endblock %}

{% block content %}
<div class="container">
    <div class="hero">
        <h1>Welcome to Propertism</h1>
        <p>NRI Property Management Services In India, Chennai</p>
    </div>
    
    <div class="featured-properties">
        <h2>Featured Properties</h2>
        <div class="row">
            {% for property in featured_properties %}
                {% include "components/_property-card.html" %}
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

---

## 🎯 Component Usage Pattern

### Always Use Components
```html
<!-- BAD: Inline code -->
<div class="property-card">
    <img src="{{ property.image_url }}" alt="{{ property.title }}">
    <h3>{{ property.title }}</h3>
    <p>{{ property.price }}</p>
</div>

<!-- GOOD: Reusable component -->
{% include "components/_property-card.html" with property=property %}
```

### Always Use Utility Classes
```html
<!-- BAD: Custom CSS -->
<div style="margin: 20px; padding: 20px; text-align: center;">
    <h2 style="font-weight: bold;">Title</h2>
</div>

<!-- GOOD: Utility classes -->
<div class="container p-2 text-center">
    <h2 class="font-bold">Title</h2>
</div>
```

---

## ✅ Best Practices

1. **Always use reusable components** - Never duplicate HTML
2. **Use utility classes** - For consistent styling
3. **Keep templates DRY** - Don't repeat yourself
4. **Use template inheritance** - Base templates for layout
5. **No emojis** - Professional enterprise design
6. **No rounded corners** - Sharp, clean design
7. **Responsive** - Mobile-first approach
8. **Accessible** - Semantic HTML, ARIA labels

---

**Last Updated**: February 22, 2026
