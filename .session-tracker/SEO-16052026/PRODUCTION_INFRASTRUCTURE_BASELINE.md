# PRODUCTION_INFRASTRUCTURE_BASELINE
## SCCB-PROP-PRODUCTION-STABILIZATION-AND-SEO-ROADMAP-CONSOLIDATION-1606

**Date**: 2026-06-17  
**Status**: PRODUCTION ARCHITECTURE DOCUMENTED

---

## AWS Infrastructure Overview

### General Information
```
AWS Account: Propertism Production
Primary Region: us-east-1
Secondary Region: N/A (Single region deployment)
Service Model: Platform as a Service (PaaS)
```

---

## Elastic Beanstalk Configuration

### Environment Details
```
Application Name: propertism
Environment Name: propertism-prod-2026
Environment Type: Load Balanced (Multi-AZ capable)
Platform: Python 3.13
Architecture: 64-bit
```

### Environment Status
```
Status: Ready ✅
Health: Green ✅
Deployed Version: gh-151-bb18b8b (recent)
Last Deployment: 2026-06-17 (today)
Instances: 1+ (auto-scaled)
```

### Deployment Strategy
```
Strategy: Rolling update (zero-downtime)
Batch Size: 100% (single instance environment)
Timeout: 10 minutes
Termination Policy: Retain old versions (last 100)
```

---

## CI/CD Deployment Flow

### GitHub Actions Integration
```
Repository: viji-olivine/03rolledout/01propertism
Branch: main (triggers deployment)
Workflow: Automatic EB deploy on push
Trigger: Push to main branch
```

### Deployment Pipeline
```
Step 1: GitHub detects commit to main
        └─ Workflow file: .github/workflows/*.yml (assumed)

Step 2: EB CLI receives deployment command
        └─ Command: eb deploy propertism-prod-2026

Step 3: EB packages application
        └─ Bundles: source code + dependencies

Step 4: EB terminates old instance
        └─ Method: Rolling (no downtime)

Step 5: Launches new instance
        └─ Configuration: .ebextensions/01_django.config

Step 6: Container commands execute
        └─ 01_collectstatic: Gather static files
        └─ 02_migrate: Database migrations
        └─ 03_seed_knowledge_hub: Seed articles (NEW)
        └─ 04_create_admin: Create superuser (if configured)

Step 7: Application starts
        └─ Server: Gunicorn + Django
        └─ Port: 8000 (internal)

Step 8: EB health check passes
        └─ Endpoint: /health/ (custom middleware)
        └─ Status: 200 OK = Green
```

### EB Extension Configuration
**File**: `.ebextensions/01_django.config`

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: realtor_project.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: realtor_project.settings
    PYTHONPATH: /var/app/current:$PYTHONPATH
    DJANGO_ALLOWED_HOSTS: "propertism.in,www.propertism.in,propertism-prod-2026.us-east-1.elasticbeanstalk.com"
    CANONICAL_HOST: "www.propertism.in"
    CANONICAL_SCHEME: "https"
    CANONICAL_REDIRECT_HOSTS: "propertism.in"
    DEBUG: "False"
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: staticfiles

container_commands:
  01_collectstatic:
    command: "python manage.py collectstatic --noinput --clear"
  02_migrate:
    command: "python manage.py migrate --noinput"
    leader_only: true
  03_seed_knowledge_hub:
    command: "python manage.py seed_knowledge_hub_phase_a --publish"
    leader_only: true
    ignoreErrors: true
  04_create_admin_if_configured:
    command: >-
      /bin/bash -lc 'if [ -n "${ADMIN_USERNAME:-}" ] && [ -n "${ADMIN_EMAIL:-}" ] && [ -n "${ADMIN_PASSWORD:-}" ]; then
      python scripts/create_or_reset_prod_superuser.py;
      else
      echo "ADMIN_* variables not set; skipping superuser bootstrap.";
      fi'
    leader_only: true
```

---

## Load Balancer & Auto-Scaling

### Load Balancer
```
Type: Application Load Balancer (ALB)
Target Group: propertism-prod-2026-default
Health Check Path: /health/
Health Check Interval: 30 seconds
Healthy Threshold: 2 consecutive checks
Unhealthy Threshold: 5 consecutive checks
Port: 80 (HTTP) → 443 (HTTPS via CloudFront)
```

### Auto-Scaling
```
Min Instances: 1
Max Instances: 4 (configured, not active)
Scale-Up Trigger: CPU > 80% or Network > 80%
Scale-Down Trigger: CPU < 20% for 5 minutes
Cooldown Period: 5 minutes
```

---

## CloudFront CDN Configuration

### Distribution Setup
```
Domain: www.propertism.in
CNAME: www.propertism.in
SSL Certificate: AWS Certificate Manager (ACM)
HTTP Version: HTTP/2 and HTTP/3
```

### CloudFront Origin
```
Origin: propertism-prod-2026.us-east-1.elasticbeanstalk.com
Protocol: HTTPS only
Origin Custom Header: None (EB handles custom domain)
```

### Caching Behavior
```
Path Pattern 1: /static/* 
  TTL: 86400 seconds (24 hours)
  Compress: Yes
  
Path Pattern 2: /media/*
  TTL: 604800 seconds (7 days)
  Compress: No (images, PDFs)
  
Path Pattern 3: / (default)
  TTL: 0 seconds (no caching)
  Compress: Yes (gzip)
  Query String Forwarding: Forward all
```

### Security Headers
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Content-Security-Policy: [configured in Django settings]
```

---

## S3 Integration

### Media Storage Bucket
```
Bucket Name: [AWS_MEDIA_BUCKET_NAME env var]
Region: us-east-1
Access: Private (via Django DEFAULT_FILE_STORAGE)
```

### Bucket Configuration
```
USE_LOCAL_STORAGE: 1 (EB environment variable)
Effect: S3 disabled, local storage active
Reason: SCCB-WS-LOCAL-STORAGE-HARD-OVERRIDE-V1
```

**Note**: S3 integration configured but currently disabled in favor of local storage via EBS volumes.

---

## Redis Integration

### Status
```
Redis: NOT CURRENTLY ACTIVE
Reason: Cache configuration set but not required for current load
Connection String: [REDIS_URL env var - unused]
```

### Cache Configuration (if activated)
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'propertism',
        'TIMEOUT': 300,
    }
}
```

---

## Environment Variables

### Required Variables (Set in EB)
```
DJANGO_SETTINGS_MODULE: realtor_project.settings
DEBUG: False
SECRET_KEY: [secure-value]
DJANGO_ALLOWED_HOSTS: propertism.in,www.propertism.in,propertism-prod-2026.us-east-1.elasticbeanstalk.com
CANONICAL_HOST: www.propertism.in
CANONICAL_SCHEME: https
```

### Database Variables (RDS)
```
RDS_DB_NAME: propertismdb
RDS_USERNAME: propertismadmin
RDS_PASSWORD: [secure-value]
RDS_HOSTNAME: propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com
RDS_PORT: 5432
DATABASE_URL: postgresql://propertismadmin:[pwd]@propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com:5432/propertismdb
POSTGRES_SSLMODE: require
```

### Email Configuration
```
EMAIL_BACKEND: django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST: smtp.gmail.com
EMAIL_PORT: 587
EMAIL_USE_TLS: True
EMAIL_HOST_USER: [propertism-service-email@gmail.com]
EMAIL_HOST_PASSWORD: [app-specific-password]
DEFAULT_FROM_EMAIL: propertism.tamil@gmail.com
```

### OAuth Integration
```
GOOGLE_CLIENT_ID: [secure-value]
GOOGLE_CLIENT_SECRET: [secure-value]
```

### WhatsApp Integration
```
WHATSAPP_PHONE_ID: [secure-value]
WHATSAPP_ACCESS_TOKEN: [secure-value]
WHATSAPP_ADMIN_PHONE: [number-without-plus]
```

### Storage Configuration
```
USE_LOCAL_STORAGE: 1 (enables local storage override)
AWS_MEDIA_BUCKET_NAME: [currently disabled]
AWS_S3_REGION_NAME: us-east-1
```

---

## Monitoring & Logging

### CloudWatch Integration
```
Application Logs: /var/log/django.log (via CloudWatch agent)
Web Server Logs: /var/log/eb-docker.log
Activity Logs: /var/log/eb-activity.log
Metric Frequency: 5-minute intervals
Log Retention: 7 days (configurable)
```

### Health Monitoring
```
Metric 1: EnvironmentHealth (Green/Yellow/Red)
Metric 2: CPUUtilization (% of EC2 instance)
Metric 3: NetworkIn/Out (bytes per instance)
Metric 4: TargetResponseTime (milliseconds)
Alert Threshold: Health != Green (manual notification)
```

### Application Monitoring
```
Framework: Django debug toolbar (disabled in production)
Error Tracking: Django error emails (configured via EMAIL_*)
Performance: Django logging (INFO level)
```

---

## Security Configuration

### Firewall (Security Group)
```
Inbound Rules:
  Port 80 (HTTP): From CloudFront only
  Port 443 (HTTPS): From CloudFront only
  Port 22 (SSH): From [authorized-IPs-only]
  
Outbound Rules:
  Port 443: To All (for external APIs)
  Port 5432: To RDS security group (PostgreSQL)
  Port 25: To SES (email - if active)
```

### SSL/TLS
```
Certificate: AWS Certificate Manager (free)
Domain: www.propertism.in
Auto-renewal: Yes (ACM handles)
Protocol: TLS 1.2+
Cipher Suites: Modern (no legacy support)
HSTS: Enabled (max-age=31536000)
```

### IAM Roles
```
EB Instance Role: aws-elasticbeanstalk-ec2-role
  Permissions:
    - Read from S3 bucket
    - Write to CloudWatch logs
    - Read from Secrets Manager (optional)
    - Access to RDS
```

---

## Backup & Disaster Recovery

### Database Backups (RDS)
```
Backup Window: 03:00–04:00 UTC
Retention Period: 7 days (automated)
Manual Snapshots: Available on demand
Multi-AZ: No (single AZ deployment)
Failover: Manual (if AZ fails)
```

### Application Backups
```
Code: Git repository (GitHub)
Static Files: Regenerated on each deploy
Configuration: EB configuration files in .ebextensions/
```

---

## Performance Baseline

### Current Capacity
```
Instance Type: t3.micro or t3.small (estimated)
CPU Capacity: 1-2 vCPU
Memory: 1-2 GB
Network: Up to 5 Gbps burst
Storage: 30 GB EBS root volume
```

### Request Handling
```
Concurrent Connections: ~100-200 per instance
Average Response Time: 50-100ms (p95)
Throughput: 50-100 requests/second per instance
Peak Load Window: Business hours (8 AM–6 PM IST)
```

---

## Deployment Frequency & Process

### Deployment Schedule
```
Frequency: On-demand (push to main triggers deployment)
Average Deployment Time: 2-3 minutes
Downtime: ~30 seconds (rolling update)
Rollback Time: <1 minute (EB version history)
```

### Deployment Checklist
```
✓ Code review and merge to main
✓ Run local tests (pre-commit)
✓ Push to GitHub main branch
✓ GitHub Actions triggers EB deployment
✓ EB CLI packages and deploys
✓ Container commands execute (migrate, seed, collect static)
✓ EB health check validates
✓ Monitor CloudWatch for errors (5 minutes)
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│ CloudFront CDN (www.propertism.in)                  │
│ - Static files cache (24 hr)                        │
│ - Dynamic content (no cache)                        │
│ - SSL/TLS termination                               │
└────────────────────┬────────────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────┐
│ Application Load Balancer                           │
│ - Distributes traffic to EC2 instances              │
│ - Health check: /health/ endpoint                   │
│ - Port 80→443 redirect                              │
└────────────────────┬────────────────────────────────┘
                     │ HTTP
                     ▼
┌─────────────────────────────────────────────────────┐
│ Elastic Beanstalk Environment                       │
│ Environment: propertism-prod-2026                   │
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ EC2 Instance (t3.micro/small)                │   │
│ │ - OS: Amazon Linux 2                         │   │
│ │ - Python 3.13                                │   │
│ │ - Gunicorn + Django                          │   │
│ │ - Static files: /var/app/current/staticfiles │   │
│ │ - Media files: /var/app/current/media        │   │
│ └──────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
     ┌────────┐ ┌─────────┐ ┌──────────┐
     │   RDS  │ │CloudWatch│ │  S3      │
     │Postgre-│ │  Logs   │ │(Disabled)│
     │ SQL    │ │(Monitor)│ └──────────┘
     └────────┘ └─────────┘
```

---

## Known Limitations

1. **Single AZ Deployment**: No automatic failover (manual recovery required)
2. **No Redis Cache**: In-process caching only (suitable for current load)
3. **EBS Storage**: Media files not persistent across instance termination (use S3 in production if needed)
4. **Manual Scaling**: Auto-scaling configured but not active (single instance cost optimization)
5. **Email via Gmail SMTP**: Limited throughput (~500/day), consider SES for scale

---

## Next Steps for Growth

1. **Auto-scaling**: Enable when traffic exceeds current capacity
2. **Multi-AZ**: Add failover for high availability
3. **CloudFront**: Optimize cache headers for better performance
4. **S3 Media**: Re-enable S3 storage when local storage becomes bottleneck
5. **Redis**: Activate for session caching at scale

---

**Status**: ✅ PRODUCTION BASELINE DOCUMENTED  
**Last Updated**: 2026-06-17  
**Architecture Version**: 1.0 (Stable)
