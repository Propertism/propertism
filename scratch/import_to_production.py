"""
Import script for production EC2 instance.
Run this on the production server via SSH.

Usage:
  # First, download the JSON file to the server:
  curl -o /tmp/missing_knowledge_hub_articles.json https://olivine-site-673981388490.s3.amazonaws.com/missing_knowledge_hub_articles.json
  
  # Or if curl is not available:
  wget -O /tmp/missing_knowledge_hub_articles.json https://olivine-site-673981388490.s3.amazonaws.com/missing_knowledge_hub_articles.json
  
  # Then run this script:
  cd /var/app/current
  sudo -u webapp /var/app/venv/*/bin/python /tmp/import_to_production.py
"""

import json
import os
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
sys.path.insert(0, '/var/app/current')
import django
django.setup()

from django.core import serializers
from content.models import BlogPost

# Load the exported articles
json_path = '/tmp/missing_knowledge_hub_articles.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} articles from {json_path}")

for item in data:
    slug = item['fields']['slug']
    title = item['fields']['title']
    
    # Check if article already exists
    if BlogPost.objects.filter(slug=slug).exists():
        print(f"  SKIP: {slug} - already exists in production")
        continue
    
    # Deserialize and save
    obj = next(serializers.deserialize('json', json.dumps([item])))
    obj.save()
    print(f"  IMPORTED: {slug} - {title}")

# Verify
count = BlogPost.objects.filter(slug__in=[
    'rental-readiness-for-absentee-owners',
    'why-reporting-matters-for-nri-property-management'
]).count()
print(f"\nVerification: {count}/2 articles now present in production")
