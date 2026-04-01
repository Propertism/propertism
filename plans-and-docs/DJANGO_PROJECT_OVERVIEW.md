# 🏠 Propertism Django Project Overview

**Project**: New Propertism Website  
**Framework**: Django 4.2.7  
**Database**: PostgreSQL  
**API**: Django REST Framework

---

## 📁 Project Structure

```
realtor/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
│
├── realtor_project/                   # Project settings
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Root URL configuration
│   └── wsgi.py                        # WSGI configuration
│
├── properties/                        # Property management app
│   ├── __init__.py
│   ├── models.py                      # Property, PropertyType, PropertyPhoto
│   ├── views.py                       # Property views
│   ├── urls.py                        # Property URLs
│   └── serializers.py                 # API serializers
│
├── users/                             # User management app
│   ├── __init__.py
│   ├── models.py                      # Agent, Buyer models
│   ├── views.py                       # User views
│   ├── urls.py                        # User URLs
│   └── serializers.py                 # API serializers
│
├── search/                            # Search functionality app
│   ├── __init__.py
│   ├── models.py                      # SearchHistory model
│   ├── views.py                       # Search views
│   └── urls.py                        # Search URLs
│
├── middleware/                        # Custom middleware
│   └── __init__.py
│
├── uilayers/                          # UI layer app
│   ├── __init__.py
│   ├── views.py                       # Frontend views
│   ├── urls.py                        # Frontend URLs
│   └── templates/                     # HTML templates
│       ├── home.html
│       ├── about.html
│       ├── contact.html
│       ├── properties/
│       ├── users/
│       └── search/
│
├── documents/                         # Documentation
│
├── static/                            # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
└── plans-and-docs/                    # Project plans and docs
    └── DJANGO_PROJECT_OVERVIEW.md
```

---

## 🗄️ Database Models

### Property Models

**PropertyType**
- name, slug, description, icon
- Created for property categories (House, Villa, Apartment, etc.)

**Property**
- title, description, price, area
- bedrooms, bathrooms, location
- property_type (FK), status
- created_at, updated_at

**PropertyPhoto**
- property (FK), image, caption
- is_primary, sort_order

### User Models

**Agent**
- user (OneToOne), phone, bio
- photo, license_number, verified

**Buyer**
- user (OneToOne), phone, preferences

### Search Models

**SearchHistory**
- user (FK), query, results_count
- created_at

---

## 🔌 API Endpoints

### Properties API
- `GET /api/properties/` - List properties
- `GET /api/properties/{id}/` - Get property details
- `POST /api/properties/` - Create property (admin)
- `PUT /api/properties/{id}/` - Update property (admin)
- `DELETE /api/properties/{id}/` - Delete property (admin)

### Users API
- `GET /api/users/agents/` - List agents
- `GET /api/users/agents/{id}/` - Get agent details
- `POST /api/users/agents/` - Create agent (admin)

### Search API
- `GET /api/search/` - Search properties

---

## 🎨 Frontend Pages

### Public Pages
- `/` - Homepage
- `/about/` - About page
- `/contact/` - Contact page
- `/properties/` - Property listings
- `/properties/{id}/` - Property details
- `/search/` - Search results

### Admin Pages (Django Admin)
- `/admin/` - Django admin panel
- Property management
- User management
- Search history

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Edit `realtor_project/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'realtor_db',
        'USER': 'realtor_user',
        'PASSWORD': 'realtor_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

### 6. Access
- Frontend: http://localhost:8000
- Admin: http://localhost:8000/admin

---

## 📊 Key Features

- ✅ Property listings with photos
- ✅ User profiles (agents, buyers)
- ✅ Search functionality
- ✅ Contact forms
- ✅ Admin panel
- ✅ Responsive design
- ✅ REST API

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL
- **API**: Django REST Framework
- **Images**: Pillow
- **Frontend**: HTML/CSS/JS (Django templates)

---

## 📝 Next Steps

1. Install Django and dependencies
2. Configure PostgreSQL database
3. Run migrations
4. Create initial data
5. Start development

---

**Status**: Project structure created  
**Ready to start**: Yes
