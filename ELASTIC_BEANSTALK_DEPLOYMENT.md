# Elastic Beanstalk Deployment Guide - Propertism

## Overview
Simple, managed deployment for your Django site with minimal maintenance.

## Prerequisites
- AWS Account
- Python 3.x installed locally
- Git repository ready

## Step 1: Prepare Your Application

### 1.1 Create Elastic Beanstalk Configuration

Create `.ebextensions` directory in `realtor-web/`:
```bash
mkdir realtor-web/.ebextensions
```

### 1.2 Create Django Configuration File

Create `realtor-web/.ebextensions/01_django.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: realtor_project.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: realtor_project.settings
    PYTHONPATH: /var/app/current:$PYTHONPATH
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: static

container_commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python manage.py migrate --noinput"
    leader_only: true
  02_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"
    leader_only: true
  03_createsu:
    command: "source /var/app/venv/*/bin/activate && python manage.py createsu"
    leader_only: true
```

### 1.3 Create Database Configuration

Create `realtor-web/.ebextensions/02_packages.config`:
```yaml
packages:
  yum:
    postgresql-devel: []
    gcc: []
```

### 1.4 Update Requirements

Update `realtor-web/requirements.txt`:
```txt
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.0
django-modeltranslation==0.18.11
Pillow==10.1.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
whitenoise==6.6.0
gunicorn==21.2.0
```

## Step 2: Update Django Settings

### 2.1 Modify `realtor-web/realtor_project/settings.py`

Add at the top:
```python
import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

Add database configuration:
```python
# Database
if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

Add static files configuration:
```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

# WhiteNoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 2.2 Create Management Command for Superuser

Create `realtor-web/content/management/commands/createsu.py`:
```python
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@propertism.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
```

## Step 3: Deploy to Elastic Beanstalk

### 3.1 Install EB CLI

```bash
pip install awsebcli
```

### 3.2 Initialize Elastic Beanstalk

Navigate to your project:
```bash
cd realtor-web
eb init
```

Follow prompts:
- Select region (e.g., `us-east-1`)
- Application name: `propertism`
- Platform: `Python 3.11`
- SSH: Yes (recommended)

### 3.3 Create Environment

```bash
eb create propertism-prod
```

Options:
- Environment name: `propertism-prod`
- DNS CNAME: `propertism-prod` (or your choice)
- Load balancer: `application`

This will:
- Create EC2 instance
- Set up load balancer
- Configure auto-scaling
- Deploy your application

### 3.4 Add RDS Database (Optional but Recommended)

```bash
eb create propertism-prod --database
```

Or add later:
```bash
eb create propertism-prod
# Then in AWS Console, add RDS to environment
```

Database settings:
- Engine: PostgreSQL
- Instance: db.t3.micro (free tier eligible)
- Storage: 20GB
- Username: `propertism_admin`
- Password: (set a strong password)

## Step 4: Configure Environment Variables

Set environment variables:
```bash
eb setenv \
  SECRET_KEY="your-secret-key-here" \
  DEBUG="False" \
  ALLOWED_HOSTS=".elasticbeanstalk.com,propertism.com,www.propertism.com"
```

Generate a secret key:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 5: Deploy Updates

After making changes:
```bash
cd realtor-web
git add .
git commit -m "Your changes"
eb deploy
```

## Step 6: Access Your Site

Get your URL:
```bash
eb open
```

Access admin panel:
```
https://your-app.elasticbeanstalk.com/en/admin/
Username: admin
Password: admin123
```

## Step 7: Add Custom Domain (Optional)

### 7.1 In AWS Console:
1. Go to Route 53
2. Create hosted zone for your domain
3. Add A record pointing to EB environment
4. Or use CNAME for subdomain

### 7.2 Update Environment:
```bash
eb setenv ALLOWED_HOSTS=".elasticbeanstalk.com,yourdomain.com,www.yourdomain.com"
```

### 7.3 Add SSL Certificate:
1. Go to Certificate Manager
2. Request certificate for your domain
3. In EB Console → Configuration → Load Balancer
4. Add HTTPS listener with certificate

## Monitoring and Management

### View Logs:
```bash
eb logs
```

### SSH into Instance:
```bash
eb ssh
```

### Check Status:
```bash
eb status
```

### View in Console:
```bash
eb console
```

## Cost Estimation

### Free Tier (First 12 months):
- EC2 t3.micro: Free
- RDS db.t3.micro: Free (750 hours/month)
- Load Balancer: ~$16/month
- **Total**: ~$16/month

### After Free Tier:
- EC2 t3.micro: ~$8/month
- RDS db.t3.micro: ~$15/month
- Load Balancer: ~$16/month
- **Total**: ~$40/month

## Backup and Maintenance

### Database Backups:
- Automatic daily backups (RDS)
- Retention: 7 days (configurable)

### Application Updates:
```bash
cd realtor-web
git pull
eb deploy
```

### Scale Up/Down:
```bash
# Scale to 2 instances
eb scale 2

# Scale back to 1
eb scale 1
```

## Troubleshooting

### Deployment Failed:
```bash
eb logs
# Check for errors in logs
```

### Database Connection Issues:
```bash
eb ssh
# Check environment variables
printenv | grep RDS
```

### Static Files Not Loading:
```bash
eb ssh
cd /var/app/current
source /var/app/venv/*/bin/activate
python manage.py collectstatic --noinput
```

### Reset Environment:
```bash
eb terminate propertism-prod
eb create propertism-prod --database
```

## Useful Commands

```bash
# List environments
eb list

# Switch environment
eb use propertism-prod

# View environment info
eb status

# Open in browser
eb open

# View recent logs
eb logs

# SSH into instance
eb ssh

# Deploy changes
eb deploy

# Terminate environment
eb terminate
```

## Security Best Practices

1. **Change default admin password** immediately after first login
2. **Use strong SECRET_KEY** in production
3. **Enable HTTPS** with SSL certificate
4. **Set DEBUG=False** in production
5. **Restrict ALLOWED_HOSTS** to your domains only
6. **Enable MFA** on AWS account
7. **Regular backups** of database
8. **Monitor logs** for suspicious activity

## Next Steps

1. Deploy application: `eb create propertism-prod --database`
2. Set environment variables: `eb setenv SECRET_KEY="..." DEBUG="False"`
3. Access admin panel and change password
4. Add your content through Django admin
5. Configure custom domain (optional)
6. Set up SSL certificate
7. Monitor and maintain

---

**Estimated Setup Time**: 30-45 minutes
**Monthly Cost**: $16-40 (depending on free tier eligibility)
**Maintenance**: Minimal - AWS handles infrastructure

Your site will be live at: `https://propertism-prod.elasticbeanstalk.com`
