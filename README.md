# Propertism Realty Advisors LLP

**NRI Property Management Platform**  
Professional real estate services for Non-Resident Indians

---

## 🚀 Quick Start

### Start Development Server
```bash
start.bat
```
Opens: `http://localhost:8000/en/`

### Stop Server
```bash
stop.bat
```
Or close the CMD window

---

## 📁 Project Structure

```
realtor/
├── start.bat                      # Start Django server
├── stop.bat                       # Stop server
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
│
├── realtor-web/                   # Django Backend
│   ├── manage.py                  # Django management
│   ├── realtor_project/           # Project settings
│   ├── content/                   # Content management app
│   ├── properties/                # Properties app
│   ├── users/                     # User management
│   ├── uilayers/                  # Templates & views
│   └── static/                    # CSS, images, JS
│
├── sccbs/                         # Specification files
├── scripts/                       # Utility scripts
└── archive/                       # Historical documentation
```

---

## 🌐 Website Pages

### Public Pages
- **Homepage**: `/en/` - Hero, stats, services, featured properties
- **Properties**: `/en/properties/` - Property listings with pagination
- **Services**: `/en/services/` - Real estate services
- **About**: `/en/about/` - Company info, mission, values
- **Management**: `/en/management/` - Team members, expertise
- **Blog**: `/en/blog/` - Blog posts, newsletter
- **Contact**: `/en/contact/` - Contact form, office locations

### Admin Panel
- **URL**: `http://localhost:8000/en/admin/`
- **Username**: `admin`
- **Password**: `admin123`

---

## 🎨 Design System

### Colors
```
Navy:       #0F172A  (Primary)
Gold:       #B89A4A  (Accent)
White:      #FFFFFF  (Background)
Black:      #111111  (Text)
Gray:       #6B7280  (Secondary)
```

### Typography
- **Headlines**: Playfair Display (Serif)
- **Body**: Inter (Sans-serif)

### Design Principles (SCCB-4 & SCCB-5)
- ✅ Sharp edges (NO rounded corners)
- ✅ NO emojis
- ✅ NO gradients
- ✅ Enterprise-grade aesthetic

---

## 💻 Technology Stack

### Backend
- **Framework**: Django 4.2
- **Database**: SQLite (dev) → PostgreSQL (production)
- **CMS**: Django CMS 4.1
- **API**: Django REST Framework

### Frontend
- **Templates**: Django Templates
- **CSS**: Custom (premium-styles.css)
- **Fonts**: Google Fonts (Playfair Display, Inter)
- **Design**: Responsive, mobile-first

---

## 📊 Content Management

All content is managed through Django Admin:

### CONTENT Section
- **Company Information** - Name, tagline, mission, addresses, phones
- **Statistics** - Homepage stats (properties, clients, years)
- **Services** - Service offerings with descriptions
- **Core Values** - Company values
- **Team Members** - Management team with photos
- **Expertise Areas** - Areas of expertise
- **Blog Posts** - Blog content (ready for future)
- **Newsletter** - Email subscribers
- **Contact Inquiries** - Form submissions

### PROPERTIES Section
- **Properties** - Property listings with details
- **Property Types** - Categories (residential, commercial, etc.)
- **Inquiries** - Property inquiries
- **Maintenance Requests** - Property maintenance
- **Support Tickets** - Customer support

---

## 🔧 Development Workflow

### Daily Development
```bash
1. start.bat                          # Start Django
2. Edit files in realtor-web/
3. Refresh browser to see changes
4. Close CMD window when done
```

### Content Updates
```bash
1. Go to http://localhost:8000/en/admin/
2. Login with admin/admin123
3. Edit content in CONTENT section
4. Refresh website to see changes
```

### Database Changes
```bash
cd realtor-web
python manage.py makemigrations
python manage.py migrate
```

---

## 📝 Important Documents

### In Root
- `README.md` - This file
- `SESSION_SUMMARY_2026-02-23.md` - Latest session summary
- `PRE_PRODUCTION_AUDIT.md` - Production readiness audit

### In Archive
- All historical documentation
- Completed task summaries
- Implementation guides
- Old session summaries

---

## 🚀 Production Deployment

### Current Status
⚠️ **NOT READY FOR PRODUCTION**

See `PRE_PRODUCTION_AUDIT.md` for detailed analysis.

### Critical Issues to Fix
1. Security settings (SECRET_KEY, DEBUG, HTTPS)
2. Database migration (SQLite → PostgreSQL)
3. Image optimization
4. SEO meta tags
5. Performance optimization

### Recommended Hosting
- **Railway.app** (Recommended) - $5-10/month
- **PythonAnywhere** (Free tier available)
- **DigitalOcean** - $12/month

---

## 📞 Company Information

### Propertism Realty Advisors LLP

**India Office**:
- Address: No. 30, 3rd Floor, SSR Pankajam Towers, Arunachalam Road, Saligramam, Chennai, Tamil Nadu - 600093
- Phones: +91 86670 20798, +91 98412 01930, +91 98418 44452

**US Office**:
- Address: 46 Berkshire Pl, Hackensack, NJ 07601
- Phone: +1 518 409 3485

**Email**: info@propertism.com  
**Target Audience**: NRI (Non-Resident Indians)  
**Mission**: "We manage your property and resources when you are far from the nation"

---

## 🔗 Useful Links

### Development
- Django Admin: `http://localhost:8000/en/admin/`
- Django CMS: `http://localhost:8000/en/admin/cms/page/`
- User Dashboard: `http://localhost:8000/en/dashboard/`

### Documentation
- Django Docs: https://docs.djangoproject.com/
- Django CMS Docs: https://docs.django-cms.org/
- Django REST Framework: https://www.django-rest-framework.org/

---

## 🆘 Troubleshooting

### Server Won't Start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /PID <process_id> /F

# Try starting again
start.bat
```

### Database Issues
```bash
cd realtor-web
python manage.py migrate
python manage.py createsuperuser  # If admin lost
```

### Static Files Not Loading
```bash
cd realtor-web
python manage.py collectstatic
```

---

## 📈 Project Status

### ✅ Completed
- Django backend setup
- Content management system
- All website pages (dynamic)
- Admin panel configuration
- Responsive design
- Properties listing
- Contact forms
- Blog structure

### ⏳ In Progress
- Production deployment preparation
- Security hardening
- Performance optimization
- SEO implementation

### 🚀 Future
- Image upload system
- Property filters
- Blog system activation
- Email notifications
- Analytics integration
- Payment integration

---

## 👥 Team

**Developer**: Viji (ERP Developer)  
**AI Assistant**: Manthraa  
**Company**: Propertism Realty Advisors LLP

---

## 📄 License

Proprietary - Propertism Realty Advisors LLP  
All rights reserved.

---

**Last Updated**: February 23, 2026  
**Version**: 1.0.0  
**Status**: Development
