#!/usr/bin/env python
"""Safe delta import: Import only missing articles, skip duplicates."""
import os
import re
import sys
import json
from django.core import serializers

# Load env from EB deployment env file
env_file = '/opt/elasticbeanstalk/deployment/env'
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            m = re.match(r'^([A-Z_]+)=(.*)$', line.strip())
            if m:
                os.environ[m.group(1)] = m.group(2)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
sys.path.insert(0, '/var/app/current')

import django
django.setup()

from content.models import BlogPost

with open('/tmp/missing_articles.json') as f:
    objects = list(serializers.deserialize('json', f.read()))

imported = 0
skipped = 0

for obj in objects:
    slug = obj.object.slug
    if BlogPost.objects.filter(slug=slug).exists():
        print(f"Skipping {slug} (already exists)")
        skipped += 1
    else:
        obj.save()
        print(f"Imported {slug}")
        imported += 1

print(f"\nSummary: {imported} imported, {skipped} skipped")
