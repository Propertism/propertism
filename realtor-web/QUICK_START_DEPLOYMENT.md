# Quick Start Deployment Guide

**For**: Propertism Realty Advisors LLP  
**SCCB-47**: Deployment Preparation  
**Status**: Ready to Deploy

---

## 🚀 Ready to Launch?

You have 3 deployment options. Choose based on your comfort level:

---

## Option 1: Render (Easiest - 30 minutes)

### Step 1: Create Render Account
Visit: https://render.com/

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your Git repository
3. Configure:
   - **Name**: propertism-realtor
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements-production.txt`
   - **Start Command**: `cd realtor-web && gunicorn realtor_project.wsgi:application`

### Step 3: Add Environment Variables
```
DJANGO_SECRET_KEY=<generate new key>
DEBUG=False
DJANGO_ENV=production
DJANGO_ALLOWED_HOSTS=your-app.onrender.com
```

### Step 4: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Copy DATABASE_URL
3. Add to web service environment variables

### Step 5: Deploy
Click "Create Web Service" - Done! ✅

**Cost**: $7/month (app) + $7/month (database) = $14/month

---

## Option 2: Railway (Fastest - 15 minutes)

### Step 1: Create Railway Account
Visit: https://railway.app/

### Step 2: Deploy from GitHub
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository

### Step 3: Add PostgreSQL
1. Click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway auto-connects it

### Step 4: Add Environment Variables
Railway auto-detects Django. Just add:
```
DJANGO_SECRET_KEY=<generate new key>
DEBUG=False
```

### Step 5: Deploy
Automatic! ✅

**Cost**: $5-10/month (pay as you go)

---

## Option 3: Ubuntu VPS (Full Control - 4 hours)

### Prerequisites
- Ubuntu 22.04 server
- SSH access
- Domain name

### Quick Commands

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3.10 python3.10-venv python3-pip nginx postgresql git ufw

# 3. Clone repository
git clone <your-repo> /home/realtor/realtor-web

# 4. Set up virtual environment
python3.10 -m venv /home/realtor/venv
source /home/realtor/venv/bin/activate

# 5. Install requirements
pip install -r requirements-production.txt

# 6. Set up database
sudo -u postgres psql
CREATE DATABASE realtor_db;
CREATE USER realtor_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE realtor_db TO realtor_user;
\q

# 7. Configure environment
nano /home/realtor/realtor-web/realtor-web/.env
# Add all environment variables

# 8. Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# 9. Set up Gunicorn + Nginx
# Follow DEPLOYMENT_GUIDE.md sections 5-6

# 10. Install SSL
sudo certbot --nginx -d yourdomain.com
```

**Full Guide**: See `DEPLOYMENT_GUIDE.md`

**Cost**: $12/month (DigitalOcean/Linode)

---

## After Deployment

### 1. Run Tests
```bash
cd realtor-web/tests
python run_all_tests.py
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Add Content
- Log in to admin panel
- Add company information
- Add properties
- Add team members

### 4. Verify
- [ ] Website loads at your domain
- [ ] SSL certificate active (green padlock)
- [ ] Contact form sends emails
- [ ] All pages load correctly
- [ ] Mobile responsive

---

## Need Help?

**Full Documentation**:
- `DEPLOYMENT_GUIDE.md` - Complete deployment guide
- `HOSTING_PLATFORM_DECISION.md` - Platform comparison
- `PRE_LAUNCH_CHECKLIST.md` - Launch checklist

**Support**: Check troubleshooting section in DEPLOYMENT_GUIDE.md

---

## Recommended Path

1. **Week 1**: Deploy on Render (fast, managed)
2. **Month 3**: Evaluate traffic and costs
3. **Month 6**: Migrate to VPS if needed (cost savings)

---

**Ready to launch?** Choose your platform and follow the steps above! 🚀
