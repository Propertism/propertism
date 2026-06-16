#!/usr/bin/env python3
"""
Pre-Sync Validation: Check production BlogPost inventory via PostgreSQL
Usage: sudo -u webapp python3 /tmp/pre_sync_check_v2.py
"""
import os
import sys

# Read EB environment variables
env_file = '/opt/elasticbeanstalk/deployment/env'
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, val = line.split('=', 1)
                os.environ[key] = val

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
sys.path.insert(0, '/var/app/current')

import django
django.setup()

from content.models import BlogPost

published = BlogPost.objects.filter(is_published=True)
print(f"Published Count: {published.count()}")
for slug in published.values_list('slug', flat=True):
    print(f"  {slug}")

total = BlogPost.objects.count()
print(f"Total BlogPost records: {total}")
