# AWS Post-Deploy Fixes: Disappearing Media Files

## The Issue
After every new deployment to the production environment, any images uploaded via the Django Admin panel (such as team member photos and property images) disappear and have to be manually re-uploaded.

## Root Cause Analysis
The production environment is currently configured to store uploaded media files on the local filesystem of the server/container rather than using a persistent cloud storage service like Amazon S3.

In `realtor_project/settings_production.py` (lines 155-192), the application uses `FileSystemStorage` and saves images to a local `media/` folder. This fallback occurs if:
1. The `USE_LOCAL_STORAGE` environment variable is explicitly set to `"1"`.
2. The AWS S3 environment variables (`AWS_MEDIA_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) are missing.

When hosting on a modern platform (like AWS Elastic Beanstalk, Docker, or Heroku), the local file system is **ephemeral** (temporary). 
During a deployment cycle:
1. A fresh server/container is created from the source code repository.
2. The old server/container is destroyed.
3. Because the `media/` folder and its contents were created *after* the previous container started and are not tracked in the Git repository, they are completely wiped out when the old container is destroyed.

## Required Fixes (To-Do)
To permanently resolve this issue, the application must be decoupled from the ephemeral local filesystem and configured to use Amazon S3 for media storage.

**Steps to implement:**
1. **Verify Packages:** Ensure `django-storages` and `boto3` are included in `requirements.txt`.
2. **Environment Configuration:** 
   - Ensure the `USE_LOCAL_STORAGE` environment variable is **not** set to `"1"` on the production server.
   - Configure the following environment variables in the production environment with valid AWS credentials and an S3 bucket:
     - `AWS_MEDIA_BUCKET_NAME`
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`
     - `AWS_S3_REGION_NAME`
3. **Data Migration (Optional):** If there are existing images you wish to keep, they will need to be manually migrated/uploaded to the new S3 bucket so they are accessible once the app switches to S3 storage.

*Note: No code changes have been made yet as per the current request.*
