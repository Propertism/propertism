# AWS Deployment Guide for Propertism

## Prerequisites
- AWS Account
- AWS CLI installed and configured
- Domain name (optional but recommended)
- GitHub repository access

## Recommended Architecture

### Services Needed:
1. **EC2** - Application server
2. **RDS PostgreSQL** - Database
3. **S3** - Static files and media storage
4. **CloudFront** - CDN for static assets
5. **Route 53** - DNS management (if using custom domain)
6. **Certificate Manager** - SSL/TLS certificates
7. **Elastic Load Balancer** - Load balancing and SSL termination

## Deployment Steps

### 1. Prepare Your Application

Create a production settings file:


```bash
# In realtor-web/realtor_project/
# Create settings_production.py
```

### 2. Set Up RDS PostgreSQL Database

1. Go to AWS RDS Console
2. Create PostgreSQL database
3. Choose instance type (t3.micro for testing, t3.small+ for production)
4. Note down: endpoint, port, database name, username, password
5. Configure security group to allow connections from EC2

### 3. Set Up S3 Bucket for Static Files

1. Create S3 bucket (e.g., `propertism-static`)
2. Enable public access for static files
3. Configure CORS if needed
4. Create IAM user with S3 access
5. Note down: Access Key ID and Secret Access Key

### 4. Launch EC2 Instance

**Instance Configuration:**
- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.small (minimum) or t3.medium (recommended)
- Storage: 20GB minimum
- Security Group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

**Connect to EC2:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 5. Install Dependencies on EC2

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx postgresql-client -y

# Install supervisor for process management
sudo apt install supervisor -y
```

### 6. Deploy Application

```bash
# Create application directory
sudo mkdir -p /var/www/propertism
sudo chown ubuntu:ubuntu /var/www/propertism
cd /var/www/propertism

# Clone repository
git clone https://github.com/Propertism/propertism.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
cd realtor-web
pip install -r requirements.txt

# Install additional production packages
pip install django-storages boto3
```

### 7. Configure Environment Variables

Create `.env` file:
```bash
nano /var/www/propertism/realtor-web/.env
```

Add:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,your-ec2-ip

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=propertism_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=5432

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=propertism-static
AWS_S3_REGION_NAME=us-east-1

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 8. Update Django Settings

Create `realtor-web/realtor_project/settings_production.py`:
```python
from .settings import *
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# AWS S3 Settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Static files
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media files
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 9. Run Migrations and Collect Static Files

```bash
cd /var/www/propertism/realtor-web
source ../venv/bin/activate

# Set production settings
export DJANGO_SETTINGS_MODULE=realtor_project.settings_production

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (uploads to S3)
python manage.py collectstatic --noinput
```

### 10. Configure Gunicorn

Create gunicorn config:
```bash
sudo nano /etc/supervisor/conf.d/propertism.conf
```

Add:
```ini
[program:propertism]
directory=/var/www/propertism/realtor-web
command=/var/www/propertism/venv/bin/gunicorn realtor_project.wsgi:application --bind 127.0.0.1:8000 --workers 3
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/propertism.log
environment=DJANGO_SETTINGS_MODULE="realtor_project.settings_production"
```

Start supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start propertism
```

### 11. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/propertism
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        # Served from S3/CloudFront
        return 301 https://your-bucket.s3.amazonaws.com$request_uri;
    }

    location /media/ {
        # Served from S3/CloudFront
        return 301 https://your-bucket.s3.amazonaws.com$request_uri;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/propertism /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 12. Set Up SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 13. Configure CloudFront (Optional but Recommended)

1. Go to CloudFront Console
2. Create distribution
3. Origin: Your S3 bucket
4. Configure caching behavior
5. Update Django settings to use CloudFront URL

## Cost Estimation

### Monthly Costs (Approximate):
- **EC2 t3.small**: $15-20
- **RDS db.t3.micro**: $15-20
- **S3 Storage**: $1-5 (depends on usage)
- **Data Transfer**: $5-10
- **Total**: ~$40-60/month

### Cost Optimization:
- Use Reserved Instances for EC2/RDS (save 30-40%)
- Enable S3 lifecycle policies
- Use CloudFront to reduce data transfer costs
- Monitor with AWS Cost Explorer

## Monitoring and Maintenance

### Set Up CloudWatch:
1. Enable detailed monitoring on EC2
2. Create alarms for CPU, memory, disk
3. Set up log groups for application logs

### Backup Strategy:
1. Enable automated RDS backups
2. Create RDS snapshots weekly
3. Backup S3 bucket with versioning
4. Store database dumps in S3

### Update Process:
```bash
cd /var/www/propertism
git pull origin main
source venv/bin/activate
cd realtor-web
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart propertism
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Enable MFA on AWS account
- [ ] Configure security groups properly
- [ ] Enable AWS WAF for DDoS protection
- [ ] Set up AWS Secrets Manager for sensitive data
- [ ] Enable VPC for network isolation
- [ ] Configure backup and disaster recovery
- [ ] Set up monitoring and alerting
- [ ] Enable SSL/TLS everywhere
- [ ] Regular security updates

## Troubleshooting

### Check Application Status:
```bash
sudo supervisorctl status propertism
sudo tail -f /var/log/propertism.log
```

### Check Nginx:
```bash
sudo nginx -t
sudo systemctl status nginx
sudo tail -f /var/nginx/error.log
```

### Database Connection:
```bash
psql -h your-rds-endpoint -U your_user -d propertism_db
```

## Alternative: AWS Elastic Beanstalk

For easier deployment, consider Elastic Beanstalk:

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create environment: `eb create propertism-prod`
4. Deploy: `eb deploy`

This handles EC2, load balancing, and auto-scaling automatically.

## Support Resources

- AWS Documentation: https://docs.aws.amazon.com/
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- AWS Free Tier: https://aws.amazon.com/free/

---

**Note**: This is a general guide. Adjust based on your specific requirements, traffic expectations, and budget.
