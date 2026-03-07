# Quick Deploy to AWS Elastic Beanstalk

## Prerequisites
```bash
pip install awsebcli
```

## Deploy Steps

### 1. Navigate to project
```bash
cd realtor-web
```

### 2. Initialize EB (First time only)
```bash
eb init
```
- Region: Choose closest to your users (e.g., us-east-1)
- Application name: `propertism`
- Platform: Python 3.11
- SSH: Yes

### 3. Create environment with database
```bash
eb create propertism-prod --database
```
- Database engine: postgres
- Instance: db.t3.micro
- Username: propertism_admin
- Password: (set strong password)

### 4. Set environment variables
```bash
# Generate secret key first
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set variables
eb setenv SECRET_KEY="paste-generated-key-here" DEBUG="False" ALLOWED_HOSTS=".elasticbeanstalk.com"
```

### 5. Open your site
```bash
eb open
```

### 6. Access admin
```
URL: https://your-app.elasticbeanstalk.com/en/admin/
Username: admin
Password: admin123
```

**IMPORTANT**: Change admin password immediately!

## Update Deployment

After making changes:
```bash
cd realtor-web
eb deploy
```

## Useful Commands

```bash
eb status          # Check environment status
eb logs            # View logs
eb ssh             # SSH into instance
eb open            # Open in browser
eb console         # Open AWS console
eb terminate       # Delete environment
```

## Cost
- Free tier: ~$16/month (load balancer only)
- After free tier: ~$40/month

## Support
See `ELASTIC_BEANSTALK_DEPLOYMENT.md` for detailed guide.
