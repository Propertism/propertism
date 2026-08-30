import os
import sys
import re
import json

sys.path.insert(0, "/var/app/current")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")

import django
django.setup()

from properties.models import Inquiry
from properties.country_utils import resolve_country_from_intake, COUNTRY_DIRECTORY

total = Inquiry.objects.count()
updated = 0
changed = 0

print(f"Starting country sync for {total} production inquiries...\n")

for inq in Inquiry.objects.all().order_by("-id"):
    old_code = inq.country_code or ""
    old_name = inq.country_name or ""
    
    # If inquiry already has a valid international code (like +352), preserve it
    code, name = resolve_country_from_intake(
        message=inq.message,
        phone=inq.phone,
        raw_country_code=old_code if (old_code and old_code != "+91") else ""
    )
    
    if old_code != code or old_name != name:
        changed += 1
        print(f"UPDATED: #{inq.id} | {inq.name} | Phone: {inq.phone} | Old: {old_code} ({old_name}) -> New: {code} ({name})")
    
    Inquiry.objects.filter(pk=inq.pk).update(country_code=code, country_name=name)
    updated += 1

print(f"\nFinished! Processed {updated}/{total} inquiries. {changed} records updated in database.")
