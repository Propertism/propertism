#!/usr/bin/env python
"""Pre-import validation: Check if missing articles exist in production."""
import os
import re
import sys

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

# Check total published count
total = BlogPost.objects.filter(is_published=True).count()
print(f"Total published articles: {total}")

# Check the two missing slugs
slugs = [
    'rental-readiness-for-absentee-owners',
    'why-reporting-matters-for-nri-property-management',
]

for slug in slugs:
    exists = BlogPost.objects.filter(slug=slug).exists()
    published = BlogPost.objects.filter(slug=slug, is_published=True).exists()
    print(f"{slug}: exists={exists}, published={published}")

# Check production-only articles are preserved
prod_only = ['NRI-Property-Sale-in-India', 'GCC-Absentee-Property-Flagging']
for slug in prod_only:
    exists = BlogPost.objects.filter(slug=slug).exists()
    published = BlogPost.objects.filter(slug=slug, is_published=True).exists()
    print(f"{slug}: exists={exists}, published={published}")
