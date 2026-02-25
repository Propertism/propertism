# Monitoring & Analytics Guide

**Project**: Propertism Realty Advisors LLP  
**SCCB**: SCCB-48 Compliance  
**Version**: 1.0  
**Date**: February 25, 2026

---

## Table of Contents

1. [Google Analytics Setup](#google-analytics-setup)
2. [Uptime Monitoring](#uptime-monitoring)
3. [Performance Monitoring](#performance-monitoring)
4. [Backup Monitoring](#backup-monitoring)
5. [Alert Notifications](#alert-notifications)
6. [Security Monitoring](#security-monitoring)
7. [Dashboard Setup](#dashboard-setup)

---

## Google Analytics Setup

### Step 1: Create GA4 Property

1. Visit: https://analytics.google.com/
2. Click "Admin" (bottom left)
3. Click "Create Property"
4. Fill in:
   - **Property name**: Propertism Realty Advisors
   - **Reporting time zone**: Asia/Kolkata (IST)
   - **Currency**: INR (Indian Rupee)
5. Click "Next"
6. Fill in business details
7. Click "Create"

### Step 2: Get Measurement ID

1. In Admin → Data Streams
2. Click "Add stream" → "Web"
3. Enter:
   - **Website URL**: https://yourdomain.com
   - **Stream name**: Propertism Website
4. Click "Create stream"
5. Copy the **Measurement ID** (format: G-XXXXXXXXXX)

### Step 3: Add to Django Template

Edit `realtor-web/uilayers/templates/base.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Place this in the `<head>` section, before the closing `</head>` tag.

### Step 4: Exclude Admin Traffic

Add to the script:

```javascript
{% if not user.is_staff %}
gtag('config', 'G-XXXXXXXXXX');
{% endif %}
```

### Step 5: Track Contact Form Submissions

In `realtor-web/content/views.py`, add after successful form submission:

```python
# Track contact form submission in GA
if request.method == 'POST' and inquiry:
    # GA event will be tracked via client-side if needed
    pass
```

Or add client-side event in contact form template:

```javascript
<script>
function trackContactSubmit() {
    gtag('event', 'contact_form_submit', {
        'event_category': 'engagement',
        'event_label': 'Contact Form'
    });
}
</script>
```

### Step 6: Verify Installation

1. Visit your website
2. Open GA4 → Reports → Realtime
3. You should see your visit in real-time
4. Wait 24-48 hours for full data

### Conversion Goals

Set up these events in GA4:

- **contact_form_submit** - Contact form submission
- **newsletter_subscribe** - Newsletter subscription
- **property_view** - Property detail page view
- **phone_click** - Phone number click (if tracked)

---

## Uptime Monitoring

### Option 1: UptimeRobot (Recommended - Free)

**Why**: Free for up to 50 monitors, 5-minute checks

#### Setup Steps

1. Visit: https://uptimerobot.com/
2. Sign up for free account
3. Click "Add New Monitor"
4. Configure:
   - **Monitor Type**: HTTPS
   - **Friendly Name**: Propertism Website
   - **URL**: https://yourdomain.com
   - **Monitoring Interval**: 5 minutes
5. Add alert contacts:
   - Email: your-email@example.com
6. Click "Create Monitor"

#### What to Monitor

Create monitors for:
- Main website: `https://yourdomain.com`
- Admin panel: `https://yourdomain.com/secure-admin-panel/`
- API endpoint: `https://yourdomain.com/api/properties/`

#### Alert Settings

- Alert when down for: 2 minutes
- Send alerts via: Email + SMS (optional)
- Alert frequency: Every time

---

### Option 2: BetterStack (Better Features)

**Why**: Better dashboard, status pages, incident management

#### Setup Steps

1. Visit: https://betterstack.com/
2. Sign up (free tier available)
3. Create new monitor
4. Configure similar to UptimeRobot
5. Set up status page (public or private)

**Cost**: Free for 1 monitor, $10/month for more

---

### Option 3: Pingdom (Enterprise)

**Why**: Advanced features, detailed reports

**Cost**: $10/month minimum

---

## Performance Monitoring

### Option 1: Simple Server Monitoring (Free)

For Ubuntu VPS:

#### Install Monitoring Tools

```bash
# Install htop for real-time monitoring
sudo apt install htop

# Install netdata for web dashboard
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

#### Access Netdata Dashboard

Visit: `http://YOUR_SERVER_IP:19999`

**Secure it**:
```bash
sudo nano /etc/netdata/netdata.conf
```

Change:
```ini
[web]
    bind to = 127.0.0.1
```

Then access via SSH tunnel:
```bash
ssh -L 19999:localhost:19999 user@your-server
```

Visit: `http://localhost:19999`

---

### Option 2: New Relic (Recommended for Production)

#### Setup Steps

1. Visit: https://newrelic.com/
2. Sign up (free tier: 100GB/month)
3. Install Python agent:

```bash
pip install newrelic
```

4. Get license key from New Relic dashboard
5. Generate config:

```bash
newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini
```

6. Update Gunicorn command:

```bash
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn realtor_project.wsgi:application
```

7. Update systemd service file to include New Relic

---

### Option 3: Datadog (Enterprise)

**Cost**: $15/host/month

More comprehensive but expensive.

---

### Metrics to Monitor

**Critical**:
- CPU usage (alert if > 80% for 5 minutes)
- Memory usage (alert if > 85%)
- Disk space (alert if > 90%)
- Response time (alert if > 2 seconds)

**Important**:
- Database connections
- Error rate (500 errors)
- Request rate
- Cache hit rate

---

## Backup Monitoring

### Automated Backup Script

Create `/home/realtor/backup_monitor.sh`:

```bash
#!/bin/bash

# Configuration
BACKUP_DIR="/home/realtor/backups"
LOG_FILE="/home/realtor/logs/backup.log"
EMAIL="your-email@example.com"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR
mkdir -p /home/realtor/logs

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
}

# Function to send alert
send_alert() {
    echo "$1" | mail -s "Backup Alert - Propertism" $EMAIL
}

log_message "Starting backup process..."

# Backup PostgreSQL database
if pg_dump -U realtor_user realtor_db > $BACKUP_DIR/db_$DATE.sql; then
    log_message "Database backup successful: db_$DATE.sql"
    DB_SIZE=$(du -h $BACKUP_DIR/db_$DATE.sql | cut -f1)
    log_message "Database backup size: $DB_SIZE"
else
    log_message "ERROR: Database backup failed!"
    send_alert "Database backup failed on $(date)"
    exit 1
fi

# Backup media files
if tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/realtor/realtor-web/realtor-web/media/; then
    log_message "Media backup successful: media_$DATE.tar.gz"
    MEDIA_SIZE=$(du -h $BACKUP_DIR/media_$DATE.tar.gz | cut -f1)
    log_message "Media backup size: $MEDIA_SIZE"
else
    log_message "ERROR: Media backup failed!"
    send_alert "Media backup failed on $(date)"
    exit 1
fi

# Backup environment file
cp /home/realtor/realtor-web/realtor-web/.env $BACKUP_DIR/env_$DATE.backup
log_message "Environment file backed up"

# Remove backups older than 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
log_message "Old backups cleaned up (>7 days)"

# Calculate total backup size
TOTAL_SIZE=$(du -sh $BACKUP_DIR | cut -f1)
log_message "Total backup directory size: $TOTAL_SIZE"

log_message "Backup process completed successfully"

# Send success notification (optional)
# send_alert "Backup completed successfully on $(date). Total size: $TOTAL_SIZE"

exit 0
```

Make it executable:
```bash
chmod +x /home/realtor/backup_monitor.sh
```

### Schedule Daily Backups

```bash
crontab -e
```

Add:
```cron
# Daily backup at 2 AM
0 2 * * * /home/realtor/backup_monitor.sh

# Weekly full backup on Sunday at 3 AM
0 3 * * 0 /home/realtor/backup_monitor.sh
```

### Backup Verification Script

Create `/home/realtor/verify_backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/home/realtor/backups"
EMAIL="your-email@example.com"
TODAY=$(date +%Y%m%d)

# Check if today's backup exists
if ls $BACKUP_DIR/db_${TODAY}*.sql 1> /dev/null 2>&1; then
    echo "✓ Backup found for today"
    exit 0
else
    echo "✗ No backup found for today!" | mail -s "ALERT: Backup Missing" $EMAIL
    exit 1
fi
```

Schedule verification:
```cron
# Check backup at 3 AM (after backup runs)
0 3 * * * /home/realtor/verify_backup.sh
```

### Off-Site Backup (Recommended)

**Option 1: AWS S3**
```bash
# Install AWS CLI
pip install awscli

# Configure
aws configure

# Sync backups to S3
aws s3 sync /home/realtor/backups/ s3://your-bucket/backups/
```

**Option 2: Backblaze B2** (Cheaper)
```bash
# Install B2 CLI
pip install b2

# Sync backups
b2 sync /home/realtor/backups/ b2://your-bucket/backups/
```

Add to cron after backup:
```cron
0 4 * * * aws s3 sync /home/realtor/backups/ s3://your-bucket/backups/
```

---

## Alert Notifications

### Option 1: Email Alerts (Built-in)

Already configured if you have email service set up.

Test email alerts:
```bash
echo "Test alert" | mail -s "Test Alert" your-email@example.com
```

If `mail` command not available:
```bash
sudo apt install mailutils
```

---

### Option 2: Slack Notifications

#### Setup Steps

1. Create Slack workspace or use existing
2. Create channel: `#propertism-alerts`
3. Add Incoming Webhook:
   - Go to: https://api.slack.com/apps
   - Create New App → From scratch
   - Name: Propertism Alerts
   - Add Incoming Webhooks
   - Activate Incoming Webhooks
   - Add New Webhook to Workspace
   - Select channel: `#propertism-alerts`
   - Copy Webhook URL

#### Send Alerts to Slack

Create `/home/realtor/slack_alert.sh`:

```bash
#!/bin/bash

WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
MESSAGE="$1"

curl -X POST -H 'Content-type: application/json' \
--data "{\"text\":\"$MESSAGE\"}" \
$WEBHOOK_URL
```

Usage:
```bash
./slack_alert.sh "Server is down!"
```

---

### Option 3: Telegram Notifications

#### Setup Steps

1. Create Telegram bot:
   - Message @BotFather on Telegram
   - Send `/newbot`
   - Follow instructions
   - Copy bot token

2. Get your chat ID:
   - Message your bot
   - Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Find your chat ID

#### Send Alerts to Telegram

Create `/home/realtor/telegram_alert.sh`:

```bash
#!/bin/bash

BOT_TOKEN="YOUR_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"
MESSAGE="$1"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
-d chat_id="${CHAT_ID}" \
-d text="${MESSAGE}"
```

---

## Security Monitoring

### Monitor Failed Login Attempts

Add to Django settings:

```python
# settings.py

LOGGING = {
    # ... existing config ...
    'loggers': {
        'django.security': {
            'handlers': ['security'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
```

### Monitor 500 Errors

Check error logs daily:
```bash
sudo tail -f /home/realtor/realtor-web/realtor-web/logs/django.log | grep ERROR
```

### Monitor Suspicious Requests

Install fail2ban:
```bash
sudo apt install fail2ban

# Configure
sudo nano /etc/fail2ban/jail.local
```

Add:
```ini
[nginx-limit-req]
enabled = true
filter = nginx-limit-req
action = iptables-multiport[name=ReqLimit, port="http,https", protocol=tcp]
logpath = /var/log/nginx/error.log
findtime = 600
bantime = 7200
maxretry = 10
```

---

## Dashboard Setup

### Create Monitoring Dashboard

Create `/home/realtor/status.sh`:

```bash
#!/bin/bash

echo "=========================================="
echo "Propertism System Status"
echo "=========================================="
echo ""

# System Info
echo "Server: $(hostname)"
echo "Date: $(date)"
echo ""

# Uptime
echo "Uptime: $(uptime -p)"
echo ""

# Disk Usage
echo "Disk Usage:"
df -h / | tail -1
echo ""

# Memory Usage
echo "Memory Usage:"
free -h | grep Mem
echo ""

# CPU Load
echo "CPU Load:"
uptime | awk -F'load average:' '{print $2}'
echo ""

# Gunicorn Status
echo "Gunicorn Status:"
systemctl is-active gunicorn
echo ""

# Nginx Status
echo "Nginx Status:"
systemctl is-active nginx
echo ""

# Last Backup
echo "Last Backup:"
ls -lht /home/realtor/backups/ | head -2
echo ""

echo "=========================================="
```

Run daily:
```bash
./status.sh | mail -s "Daily Status Report" your-email@example.com
```

---

## Quick Setup Checklist

- [ ] Google Analytics installed and verified
- [ ] UptimeRobot monitor created
- [ ] Backup script configured
- [ ] Backup cron job scheduled
- [ ] Backup verification script set up
- [ ] Email alerts configured
- [ ] Slack/Telegram alerts (optional)
- [ ] Performance monitoring chosen
- [ ] Security monitoring enabled
- [ ] Daily status report scheduled

---

## Monitoring URLs

**Google Analytics**: https://analytics.google.com/  
**UptimeRobot**: https://uptimerobot.com/dashboard  
**Server Monitoring**: http://localhost:19999 (via SSH tunnel)

---

**Last Updated**: February 25, 2026  
**SCCB Compliance**: SCCB-48 ✅  
**Status**: Ready for Implementation
