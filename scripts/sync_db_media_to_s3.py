"""
Run once to ensure every media file referenced in the DB exists in S3.
Usage (local, with production DB env vars set):
    python scripts/sync_db_media_to_s3.py
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings_production")
django.setup()

import boto3
from django.conf import settings
from properties.models import PropertyPhoto
from content.models import CompanyInfo, HeroBackgroundImage, TeamMember

BUCKET = os.environ.get("AWS_MEDIA_BUCKET_NAME", "propertism-media-622370466597")
s3 = boto3.client("s3", region_name="us-east-1")

def s3_exists(key):
    try:
        s3.head_object(Bucket=BUCKET, Key=key)
        return True
    except Exception:
        return False

def collect_paths():
    paths = []
    for p in PropertyPhoto.objects.exclude(image=""):
        paths.append(str(p.image))
    for c in CompanyInfo.objects.exclude(logo=""):
        paths.append(str(c.logo))
    for h in HeroBackgroundImage.objects.exclude(image=""):
        paths.append(str(h.image))
    for t in TeamMember.objects.exclude(photo=""):
        paths.append(str(t.photo))
    return list(set(paths))

missing = []
for path in collect_paths():
    key = f"media/{path}" if not path.startswith("media/") else path
    if not s3_exists(key):
        missing.append((path, key))

if not missing:
    print("All DB media paths exist in S3.")
else:
    print(f"{len(missing)} missing file(s):")
    for path, key in missing:
        print(f"  MISSING: {key}")
