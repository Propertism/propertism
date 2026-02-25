# Deployment Guide - Propertism Realty Advisors LLP

**SCCB-47 Compliance Document**  
**Version**: 1.0  
**Date**: February 25, 2026  
**Status**: Production Ready

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Hosting Platform Options](#hosting-platform-options)
3. [Server Setup (Ubuntu 22.04)](#server-setup-ubuntu-2204)
4. [Database Setup](#database-setup)
5. [Application Deployment](#application-deployment)
6. [SSL Configuration](#ssl-configuration)
7. [Email Configuration](#email-configuration)
8. [Domain Configuration](#domain-configuration)
9. [Post-Deployment Verification](#post-deployment-verification)
10. [Backup & Maintenance](#backup--maintenance)
11. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Information
- [ ] Domain name purchased
- [ ] Hosting platform account created
- [ ] Email service credentials (SendGrid/Mailgun)
- [ ] Server access (SSH key or password)
- [ ] Database credentials

### Local Requirements
- Python 3.10+
- Git
- SSH client

---

## Hosting Platform Options

### Recommended: Ubuntu VPS (Production Stack)

**Providers:**
- DigitalOcean Droplet ($12/month)
- Linode ($12/month)
- Vultr ($12/month)
- AWS EC2 (t3.small)

**Stack:**
- Ubuntu 22.04 LTS
- Nginx (Reverse Proxy)
- Gunicorn (WSGI Server)
- PostgreSQL 14+
- Systemd (Service Manager)

### Alternative: Managed Platforms

**Render** (Recommended for simplicity)
- Automatic SSL
- Managed PostgreSQL
- Zero-config deployment
- $7/month starter

**Railway**
- Git-based deployment
- Automatic SSL
- Built-in PostgreSQL
- $5/month

**DigitalOcean App Platform**
- Managed deployment
- Auto-scaling
- Built-in monitoring
- $12/month

---

## Server Setup (Ubuntu 22.04)

### 1. Initial Server Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3.10 python3.10-venv python3-pip nginx postgresql postgresql-contrib git ufw

# Create application user
sudo adduser realtor
sudo usermod -aG sudo realtor
su - realtor
```

### 2. Configure Firewall

```bash
# Enable UFW
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### 3. Install Python Dependencies

```bash
# Create virtual environment
cd /home/realtor
python3.10 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

---

## Database Setup

### Option 1: PostgreSQL (Production)

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE realtor_db;
CREATE USER realtor_user WITH PASSWORD 'STRONG_PASSWORD_HERE';
ALTER ROLE realtor_user SET client_encoding TO 'utf8';
ALTER ROLE realtor_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE realtor_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE realtor_db TO realtor_user;
\q

# Test connection
psql -U realtor_user -d realtor_db -h localhost
```

### Option 2: SQLite (Initial Launch)

SQLite is acceptable for initial launch with low traffic.
Migrate to PostgreSQL when:
- Traffic exceeds 100 concurrent users
- Database size exceeds 1 GB
- You need concurrent writes

---

## Application Deployment

### 1. Clone Repository

```bash
cd /home/realtor
git clone <YOUR_REPO_URL> realtor-web
cd realtor-web
```

### 2. Create Environment File

```bash
nano .env
```

Add the following:

```env
# Django Settings
DJANGO_SECRET_KEY=<GENERATE_NEW_SECRET_KEY>
DEBUG=False
DJANGO_ENV=production
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
DATABASE_URL=postgresql://realtor_user:PASSWORD@localhost:5432/realtor_db

# Or SQLite (for initial launch)
# DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=<YOUR_SENDGRID_API_KEY>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Admin Configuration
ADMIN_URL=secure-admin-panel
```

### 3. Install Dependencies

```bash
source /home/realtor/venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Test Application

```bash
python manage.py runserver 0.0.0.0:8000
# Visit http://YOUR_SERVER_IP:8000
# Press Ctrl+C to stop
```

---

## Gunicorn Configuration

### 1. Create Gunicorn Socket

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Add:

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### 2. Create Gunicorn Service

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=realtor
Group=www-data
WorkingDirectory=/home/realtor/realtor-web/realtor-web
EnvironmentFile=/home/realtor/realtor-web/realtor-web/.env
ExecStart=/home/realtor/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          realtor_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 3. Start Gunicorn

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

---

## Nginx Configuration

### 1. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/realtor
```

Add:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/realtor/realtor-web/realtor-web/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/realtor/realtor-web/realtor-web/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }
}
```

### 2. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/realtor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## SSL Configuration

### Using Certbot (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### Verify SSL

Visit: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com

Target: A or A+ rating

---

## Email Configuration

### SendGrid Setup

1. Create SendGrid account: https://sendgrid.com/
2. Create API key with "Mail Send" permissions
3. Add to `.env`:

```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=<YOUR_API_KEY>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Test Email

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email from Propertism.',
    'noreply@yourdomain.com',
    ['your-email@example.com'],
    fail_silently=False,
)
```

---

## Domain Configuration

### DNS Records

Add these records at your domain registrar:

```
Type    Name    Value                   TTL
A       @       YOUR_SERVER_IP          3600
A       www     YOUR_SERVER_IP          3600
```

### Verify DNS

```bash
nslookup yourdomain.com
nslookup www.yourdomain.com
```

Both should return your server IP.

---

## Post-Deployment Verification

### Checklist

- [ ] Website loads at https://yourdomain.com
- [ ] SSL certificate is valid (green padlock)
- [ ] All pages load correctly
- [ ] Contact form sends emails
- [ ] Admin panel accessible at /secure-admin-panel/
- [ ] Static files load correctly
- [ ] Images display properly
- [ ] Language switcher works (EN/TA/HI)
- [ ] No console errors
- [ ] Mobile responsive

### Run Tests

```bash
cd /home/realtor/realtor-web/realtor-web/tests
python run_all_tests.py
```

---

## Backup & Maintenance

### Database Backup (PostgreSQL)

```bash
# Create backup script
nano /home/realtor/backup.sh
```

Add:

```bash
#!/bin/bash
BACKUP_DIR="/home/realtor/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U realtor_user realtor_db > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/realtor/realtor-web/realtor-web/media/

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

```bash
chmod +x /home/realtor/backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
0 2 * * * /home/realtor/backup.sh
```

### Update Application

```bash
cd /home/realtor/realtor-web
git pull origin main
source /home/realtor/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

## Troubleshooting

### Gunicorn Not Starting

```bash
sudo journalctl -u gunicorn
sudo systemctl status gunicorn
```

### Nginx Errors

```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -U realtor_user -d realtor_db -h localhost

# Check Django database settings
python manage.py dbshell
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## Security Checklist

- [ ] DEBUG=False in production
- [ ] SECRET_KEY in environment variable
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enforced
- [ ] Firewall enabled (UFW)
- [ ] Database not publicly accessible
- [ ] Admin URL changed from /admin/
- [ ] Strong passwords used
- [ ] Regular backups configured
- [ ] Security headers enabled

---

## Support Contacts

**Developer**: Viji  
**Email**: [your-email]  
**Documentation**: This file

---

**Last Updated**: February 25, 2026  
**SCCB Compliance**: SCCB-47 ✅  
**Status**: Production Ready
