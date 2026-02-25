# Go-Live Execution Guide

**Project**: Propertism Realty Advisors LLP  
**SCCB**: SCCB-49 Compliance  
**Version**: 1.0  
**Date**: February 25, 2026  
**Status**: Final Release Gate

---

## ⚠️ CRITICAL: Read This First

This is a controlled production launch. Follow steps in exact order.

**Do NOT skip any step.**

**Estimated Time**: 4-6 hours (including monitoring)

---

## Table of Contents

1. [Pre-Launch Preparation](#pre-launch-preparation)
2. [Deploy to Staging](#deploy-to-staging)
3. [Test Staging Thoroughly](#test-staging-thoroughly)
4. [Create Pre-Launch Backup](#create-pre-launch-backup)
5. [Load Seed Data to Production](#load-seed-data-to-production)
6. [Point Domain to Production](#point-domain-to-production)
7. [Verify HTTPS](#verify-https)
8. [Test Production Functionality](#test-production-functionality)
9. [Monitor for 24 Hours](#monitor-for-24-hours)
10. [Rollback Strategy](#rollback-strategy)

---

## Pre-Launch Preparation

### Checklist Before Starting

- [ ] All SCCBs completed (43-48)
- [ ] All tests passing
- [ ] Deployment documentation reviewed
- [ ] Hosting platform ready
- [ ] Domain purchased
- [ ] Email service configured
- [ ] Backup strategy in place
- [ ] Team notified of launch window

### Required Information

Gather these before starting:

```
Domain: _________________
Server IP: _________________
Database Password: _________________
Email API Key: _________________
Admin Email: _________________
Emergency Contact: _________________
```

### Launch Window

Choose a low-traffic time:
- **Recommended**: Tuesday-Thursday, 2-4 AM local time
- **Avoid**: Friday, weekends, holidays
- **Duration**: 4-6 hours

---

## 1. Deploy to Staging

### Option A: Staging Subdomain (Recommended)

**URL**: `staging.yourdomain.com`

#### DNS Configuration

Add DNS record:
```
Type: A
Name: staging
Value: YOUR_SERVER_IP
TTL: 3600
```

#### Nginx Configuration

Create `/etc/nginx/sites-available/staging`:

```nginx
server {
    listen 80;
    server_name staging.yourdomain.com;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/realtor/realtor-web/realtor-web/staticfiles/;
    }

    location /media/ {
        alias /home/realtor/realtor-web/realtor-web/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/staging /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### SSL for Staging

```bash
sudo certbot --nginx -d staging.yourdomain.com
```

#### Environment Configuration

Update `.env`:
```env
DEBUG=False
DJANGO_ENV=staging
DJANGO_ALLOWED_HOSTS=staging.yourdomain.com
```

#### Deploy

```bash
cd /home/realtor/realtor-web/realtor-web
git pull origin main
source /home/realtor/venv/bin/activate
pip install -r requirements-production.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

#### Verify Staging

Visit: `https://staging.yourdomain.com`

---

### Option B: Render/Railway Staging

Most managed platforms support staging environments:

**Render**:
1. Create new Web Service
2. Name: `propertism-staging`
3. Environment: Staging
4. Deploy

**Railway**:
1. Duplicate project
2. Rename to `propertism-staging`
3. Deploy

---

## 2. Test Staging Thoroughly

### Automated Tests

```bash
cd /home/realtor/realtor-web/tests
python run_all_tests.py
```

Expected: All tests pass ✅

### Manual Testing Checklist

#### Pages (All Languages)

- [ ] Home page (EN)
- [ ] Home page (TA)
- [ ] Home page (HI)
- [ ] Services page
- [ ] About page
- [ ] Management page
- [ ] Contact page
- [ ] Blog page
- [ ] Property listings
- [ ] Property detail page

#### Forms

- [ ] Contact form submission
  - Fill all fields
  - Submit
  - Verify success message
  - Check email received
- [ ] Newsletter subscription
  - Enter email
  - Submit
  - Verify success message

#### Admin Panel

- [ ] Admin login (`/secure-admin-panel/`)
- [ ] Create property
- [ ] Upload property image
- [ ] Edit property
- [ ] Delete property (test only)
- [ ] View contact inquiries
- [ ] View newsletter subscriptions

#### SEO & Performance

- [ ] View page source - check meta tags
- [ ] Check sitemap.xml
- [ ] Check robots.txt
- [ ] Run Lighthouse audit (score > 80)
- [ ] Check mobile responsiveness

#### Browser Testing

- [ ] Chrome (desktop)
- [ ] Safari (desktop)
- [ ] Firefox (desktop)
- [ ] Chrome (mobile)
- [ ] Safari (iOS)

#### Error Handling

- [ ] Visit non-existent page (404)
- [ ] Check custom 404 page displays
- [ ] No console errors
- [ ] No broken images
- [ ] No broken links

### Performance Check

```bash
# Check response time
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://staging.yourdomain.com
```

Target: < 2 seconds

### Security Check

```bash
cd /home/realtor/realtor-web/realtor-web
python manage.py check --deploy
```

Expected: No critical issues

---

## 3. Create Pre-Launch Backup

### Full System Backup

```bash
#!/bin/bash
# Pre-launch backup script

BACKUP_DIR="/home/realtor/pre-launch-backup"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

echo "Creating pre-launch backup..."

# Backup database
if command -v pg_dump &> /dev/null; then
    pg_dump -U realtor_user realtor_db > $BACKUP_DIR/db_prelaunch_$DATE.sql
    echo "✓ Database backed up"
fi

# Backup SQLite (if using)
if [ -f "db.sqlite3" ]; then
    cp db.sqlite3 $BACKUP_DIR/db_sqlite_prelaunch_$DATE.sqlite3
    echo "✓ SQLite backed up"
fi

# Backup media files
tar -czf $BACKUP_DIR/media_prelaunch_$DATE.tar.gz media/
echo "✓ Media files backed up"

# Backup environment
cp .env $BACKUP_DIR/env_prelaunch_$DATE.backup
echo "✓ Environment backed up"

# Backup Nginx config
sudo cp /etc/nginx/sites-available/realtor $BACKUP_DIR/nginx_prelaunch_$DATE.conf
echo "✓ Nginx config backed up"

# Create backup manifest
cat > $BACKUP_DIR/MANIFEST.txt << EOF
Pre-Launch Backup
Date: $(date)
Database: db_prelaunch_$DATE.sql
Media: media_prelaunch_$DATE.tar.gz
Environment: env_prelaunch_$DATE.backup
Nginx: nginx_prelaunch_$DATE.conf
EOF

echo ""
echo "✓ Pre-launch backup complete"
echo "Location: $BACKUP_DIR"
ls -lh $BACKUP_DIR
```

Save as `pre_launch_backup.sh` and run:

```bash
chmod +x pre_launch_backup.sh
./pre_launch_backup.sh
```

### Off-Site Backup (Critical)

Upload to S3/Backblaze:

```bash
# AWS S3
aws s3 sync /home/realtor/pre-launch-backup/ s3://your-bucket/pre-launch/

# Or Backblaze B2
b2 sync /home/realtor/pre-launch-backup/ b2://your-bucket/pre-launch/
```

### Verify Backup

```bash
# Check backup files exist
ls -lh /home/realtor/pre-launch-backup/

# Verify database backup size
du -h /home/realtor/pre-launch-backup/db_prelaunch_*.sql
```

Expected: Database backup > 1 KB

---

## 4. Load Seed Data to Production

### Create Superuser

```bash
cd /home/realtor/realtor-web/realtor-web
source /home/realtor/venv/bin/activate
python manage.py createsuperuser
```

Enter:
- Username: `admin`
- Email: `your-email@example.com`
- Password: (strong password)

### Add Company Information

1. Log in to admin: `https://yourdomain.com/secure-admin-panel/`
2. Go to "Company Info"
3. Add:
   - Company name: Propertism Realty Advisors LLP
   - Tagline: Your trusted real estate partner
   - Description: (company description)
   - Contact information
   - Office addresses (Chennai, Hackensack)
   - Phone numbers
   - Email addresses

### Upload Hero Image

1. In Company Info
2. Upload hero background image
3. Verify image displays on homepage

### Add Sample Properties

Add at least 3 properties:

**Property 1: Luxury Villa**
- Title: Luxury 3BHK Villa in Chennai
- Type: Residential
- Listing Type: Sale
- Price: ₹1,50,00,000
- Bedrooms: 3
- Bathrooms: 3
- Area: 2000 sq ft
- Description: (detailed description)
- Upload 3-5 images

**Property 2: Modern Apartment**
- Title: Modern 2BHK Apartment in Anna Nagar
- Type: Residential
- Listing Type: Rent
- Price: ₹25,000/month
- Bedrooms: 2
- Bathrooms: 2
- Area: 1200 sq ft

**Property 3: Commercial Space**
- Title: Prime Commercial Space in T Nagar
- Type: Commercial
- Listing Type: Sale
- Price: ₹2,00,00,000
- Area: 1500 sq ft

### Add Team Members

1. Go to "Team Members"
2. Add key team members with:
   - Name
   - Position
   - Photo
   - Bio

### Verify Seed Data

Visit homepage and verify:
- [ ] Company information displays
- [ ] Hero image shows
- [ ] Properties display
- [ ] Team members show (if on homepage)

---

## 5. Point Domain to Production

### Step 1: Reduce TTL (24 hours before)

In your domain registrar:
1. Find DNS settings
2. Change TTL to 300 (5 minutes)
3. Wait 24 hours for propagation

### Step 2: Update DNS A Record

Change:
```
Type: A
Name: @
Value: YOUR_PRODUCTION_SERVER_IP
TTL: 300
```

Also update www:
```
Type: A
Name: www
Value: YOUR_PRODUCTION_SERVER_IP
TTL: 300
```

### Step 3: Verify DNS Propagation

```bash
# Check DNS
nslookup yourdomain.com

# Check from multiple locations
# Visit: https://www.whatsmydns.net/
```

Expected: Shows your server IP

### Step 4: Wait for Propagation

- Minimum: 5 minutes (with TTL=300)
- Maximum: 48 hours (worst case)
- Typical: 15-30 minutes

### Step 5: Test Domain

```bash
curl -I http://yourdomain.com
```

Expected: Response from your server

---

## 6. Verify HTTPS

### Check SSL Certificate

```bash
# Test SSL
curl -I https://yourdomain.com
```

Expected: `HTTP/2 200` or `HTTP/1.1 200`

### Browser Test

Visit in browser:
- `https://yourdomain.com`
- `https://www.yourdomain.com`

Check for:
- [ ] Green padlock icon
- [ ] Valid certificate
- [ ] No mixed content warnings
- [ ] HTTPS redirect from HTTP works

### SSL Labs Test

Visit: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com

Target: A or A+ rating

### Test from Multiple Devices

- [ ] Desktop Chrome
- [ ] Desktop Safari
- [ ] Desktop Firefox
- [ ] Mobile Chrome
- [ ] Mobile Safari
- [ ] Incognito/Private mode

---

## 7. Test Production Functionality

### Critical Path Testing

#### Test 1: Homepage

- [ ] Visit `https://yourdomain.com`
- [ ] Page loads in < 3 seconds
- [ ] Hero image displays
- [ ] Properties display
- [ ] No console errors
- [ ] Language switcher works

#### Test 2: Contact Form

- [ ] Go to Contact page
- [ ] Fill all fields:
  - Name: Test User
  - Email: test@example.com
  - Phone: +1234567890
  - Service: Buy
  - Message: Test inquiry
- [ ] Submit form
- [ ] Verify success message
- [ ] Check email received

#### Test 3: Newsletter

- [ ] Enter email in newsletter form
- [ ] Submit
- [ ] Verify success message

#### Test 4: Property Listings

- [ ] Go to Properties page
- [ ] Verify properties display
- [ ] Click on a property
- [ ] Verify detail page loads
- [ ] Images display correctly

#### Test 5: Admin Panel

- [ ] Visit `/secure-admin-panel/`
- [ ] Log in with superuser
- [ ] Create test property
- [ ] Upload image
- [ ] Save
- [ ] Verify on frontend
- [ ] Delete test property

#### Test 6: Multi-Language

- [ ] Switch to Tamil (TA)
- [ ] Verify content translates
- [ ] Switch to Hindi (HI)
- [ ] Verify content translates
- [ ] Switch back to English (EN)

#### Test 7: SEO

- [ ] View page source
- [ ] Verify meta tags present
- [ ] Visit `/sitemap.xml`
- [ ] Visit `/robots.txt`

### Performance Test

Run Lighthouse:
1. Open Chrome DevTools (F12)
2. Go to Lighthouse tab
3. Run audit
4. Verify scores:
   - Performance: > 80
   - Accessibility: > 90
   - Best Practices: > 90
   - SEO: > 90

### Error Log Check

```bash
# Check for errors
sudo tail -50 /home/realtor/realtor-web/realtor-web/logs/django.log | grep ERROR
```

Expected: No critical errors

---

## 8. Monitor for 24 Hours

### Hour 1: Intensive Monitoring

Check every 15 minutes:

```bash
# System status
./scripts/system_status.sh

# Error logs
sudo tail -f /home/realtor/realtor-web/realtor-web/logs/django.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Hours 2-6: Regular Monitoring

Check every hour:
- [ ] Website accessible
- [ ] No error spikes
- [ ] CPU usage normal (< 80%)
- [ ] Memory usage normal (< 85%)
- [ ] Disk space sufficient (< 90%)

### Hours 6-24: Periodic Monitoring

Check every 4 hours:
- [ ] Uptime monitor status
- [ ] Error log review
- [ ] Performance metrics
- [ ] User feedback (if any)

### Monitoring Checklist

```bash
# Create monitoring log
cat > /home/realtor/launch_monitoring.log << EOF
Launch Monitoring Log
Started: $(date)

Hour 1: _____ (Status: OK/Issues)
Hour 2: _____ (Status: OK/Issues)
Hour 4: _____ (Status: OK/Issues)
Hour 8: _____ (Status: OK/Issues)
Hour 12: _____ (Status: OK/Issues)
Hour 24: _____ (Status: OK/Issues)

Issues Found:
-
-
-

Actions Taken:
-
-
-
EOF
```

### Alert Configuration

Ensure alerts are active:
- [ ] UptimeRobot monitoring
- [ ] Email alerts configured
- [ ] Backup verification running
- [ ] Error log monitoring

---

## 9. Rollback Strategy

### When to Rollback

Rollback immediately if:
- Site is completely down for > 5 minutes
- Critical functionality broken (forms, admin)
- Data loss detected
- Security breach detected
- Performance degradation > 50%

### Rollback Procedure

#### Step 1: Stop Services

```bash
sudo systemctl stop gunicorn
sudo systemctl stop nginx
```

#### Step 2: Restore Database

```bash
# PostgreSQL
psql -U realtor_user realtor_db < /home/realtor/pre-launch-backup/db_prelaunch_*.sql

# SQLite
cp /home/realtor/pre-launch-backup/db_sqlite_prelaunch_*.sqlite3 db.sqlite3
```

#### Step 3: Restore Media Files

```bash
cd /home/realtor/realtor-web/realtor-web
rm -rf media/
tar -xzf /home/realtor/pre-launch-backup/media_prelaunch_*.tar.gz
```

#### Step 4: Restore Environment

```bash
cp /home/realtor/pre-launch-backup/env_prelaunch_*.backup .env
```

#### Step 5: Restore Nginx Config

```bash
sudo cp /home/realtor/pre-launch-backup/nginx_prelaunch_*.conf /etc/nginx/sites-available/realtor
sudo nginx -t
```

#### Step 6: Restart Services

```bash
sudo systemctl start gunicorn
sudo systemctl start nginx
```

#### Step 7: Verify Rollback

```bash
curl -I https://yourdomain.com
```

#### Step 8: Notify Team

Send notification:
```
Subject: Production Rollback Executed

Rollback completed at: [TIME]
Reason: [REASON]
Status: [STABLE/INVESTIGATING]
Next steps: [ACTIONS]
```

### Rollback Time Target

- **Target**: < 15 minutes
- **Maximum**: 30 minutes

---

## Post-Launch Checklist

### Immediate (Hour 1)

- [ ] All critical tests passed
- [ ] No errors in logs
- [ ] Contact form working
- [ ] Admin panel accessible
- [ ] Performance acceptable

### Day 1

- [ ] 24-hour monitoring complete
- [ ] No critical issues
- [ ] Backup verification passed
- [ ] Analytics tracking verified
- [ ] Uptime 99.9%+

### Week 1

- [ ] Review analytics data
- [ ] Check search console
- [ ] Review user feedback
- [ ] Optimize based on metrics
- [ ] Plan improvements

---

## Emergency Contacts

```
Developer: _________________
Phone: _________________
Email: _________________

Hosting Support: _________________
Phone: _________________

Domain Registrar: _________________
Phone: _________________

Email Service: _________________
Support: _________________
```

---

## Sign-Off

### Pre-Launch Sign-Off

**Developer**: _________________  
**Date**: _________________  
**Staging Tested**: [ ] YES  [ ] NO  
**Backup Created**: [ ] YES  [ ] NO  
**Ready for Launch**: [ ] YES  [ ] NO

### Post-Launch Sign-Off

**Developer**: _________________  
**Date**: _________________  
**Launch Time**: _________________  
**Issues Found**: _________________  
**Status**: [ ] SUCCESS  [ ] ROLLBACK  [ ] PARTIAL

### 24-Hour Sign-Off

**Developer**: _________________  
**Date**: _________________  
**Uptime**: _____%  
**Critical Issues**: _________________  
**Status**: [ ] STABLE  [ ] MONITORING  [ ] ISSUES

---

**Document Version**: 1.0  
**Last Updated**: February 25, 2026  
**SCCB Compliance**: SCCB-49 ✅  
**Status**: Ready for Go-Live Execution
