#!/usr/bin/env python
"""Post-import validation: Verify all articles in production."""
import os
import re
import sys

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

print("=== ALL ARTICLES IN PRODUCTION ===")
for a in BlogPost.objects.all().order_by('id'):
    print(f"ID={a.id} | slug={a.slug} | published={a.is_published}")

print(f"\n=== COUNTS ===")
print(f"Total all: {BlogPost.objects.count()}")
print(f"Total published: {BlogPost.objects.filter(is_published=True).count()}")

print(f"\n=== DELTA ARTICLES ===")
for slug in ['rental-readiness-for-absentee-owners', 'why-reporting-matters-for-nri-property-management']:
    a = BlogPost.objects.filter(slug=slug).first()
    if a:
        print(f"{slug}: EXISTS, published={a.is_published}")
    else:
        print(f"{slug}: MISSING")

print(f"\n=== PRODUCTION-ONLY ARTICLES ===")
for slug in ['NRI-Property-Sale-in-India', 'GCC-Absentee-Property-Flagging']:
    a = BlogPost.objects.filter(slug=slug).first()
    if a:
        print(f"{slug}: EXISTS, published={a.is_published}")
    else:
        print(f"{slug}: MISSING")
