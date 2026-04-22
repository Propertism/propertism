# Media Storage Setup Guide - Prevent Image Loss on Deployment

## Problem
After each deployment to Elastic Beanstalk, property images disappear because they're stored locally in the `media/` directory, which gets overwritten during deployment.

## Solution: AWS S3 Media Storage

### Step 1: Create an S3 Bucket for Media Files

1. Go to AWS S3 Console: https://s3.console.aws.amazon.com/
2. Click "Create bucket"
3. Bucket name: `propertism-media` (or your preferred name)
4. Region: `us-east-1` (same as your EB environment)
5. **Block Public Access settings**: Uncheck "Block all public access" (we need public read access for images)
6. Click "Create bucket"

### Step 2: Configure Bucket Policy for Public Read Access

1. Go to your bucket → Permissions → Bucket Policy
2. Add this policy (replace `propertism-media` with your bucket name):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::propertism-media/*"
        }
    ]
}
```

### Step 3: Configure CORS for the Bucket

1. Go to your bucket → Permissions → CORS
2. Add this configuration:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

### Step 4: Install Required Python Package

The `django-storages` package is already in your requirements.txt. If not, add it:

```bash
pip install django-storages boto3
```

### Step 5: Set Environment Variables in Elastic Beanstalk

1. Go to Elastic Beanstalk Console
2. Select your environment
3. Configuration → Software → Environment properties
4. Add these variables:

```
AWS_MEDIA_BUCKET_NAME=propertism-media
AWS_S3_REGION_NAME=us-east-1
AWS_ACCESS_KEY_ID=<your-aws-access-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
```

**Note**: The IAM user needs these permissions:
- `s3:PutObject`
- `s3:GetObject`
- `s3:DeleteObject`
- `s3:ListBucket`

### Step 6: Migrate Existing Media Files to S3

Run this command locally to upload existing media files:

```bash
python manage.py collectstatic --noinput  # For static files
aws s3 sync media/ s3://propertism-media/ --acl public-read
```

Or use the AWS Console to manually upload the `media/` folder contents to your S3 bucket.

### Step 7: Deploy and Test

1. Deploy your application
2. Upload a test property image through admin
3. Verify the image URL points to S3: `https://propertism-media.s3.amazonaws.com/...`
4. Deploy again and verify images persist

---

## Alternative Solution: Persistent EBS Volume (Not Recommended)

If you can't use S3, you can configure a persistent EBS volume, but this has limitations:
- Only works with single-instance environments
- More complex to manage
- Not recommended for production

---

## Verification Checklist

- [ ] S3 bucket created
- [ ] Bucket policy configured for public read
- [ ] CORS configured
- [ ] Environment variables set in EB
- [ ] Existing media files migrated to S3
- [ ] Test upload works
- [ ] Images persist after deployment

---

## Current Configuration

Your settings.py already has the S3 configuration ready:

```python
_S3_MEDIA_BUCKET = os.environ.get('AWS_MEDIA_BUCKET_NAME', '')
if _S3_MEDIA_BUCKET:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = _S3_MEDIA_BUCKET
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{_S3_MEDIA_BUCKET}.s3.amazonaws.com'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
```

Once you set `AWS_MEDIA_BUCKET_NAME` in your environment variables, S3 storage will automatically activate!

---

## Cost Estimate

S3 storage is very affordable:
- Storage: ~$0.023 per GB/month
- Requests: ~$0.005 per 1,000 PUT requests
- Data transfer: First 100 GB/month free

For a typical real estate site with 1000 property images (~5GB), expect ~$0.12/month.
