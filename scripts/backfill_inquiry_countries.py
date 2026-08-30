import os
import sys
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")

import django
django.setup()

from properties.models import Inquiry
from properties.country_utils import resolve_country_from_intake

updated_count = 0
total_inquiries = Inquiry.objects.count()
print(f"Starting country backfill for {total_inquiries} inquiries...")

for inq in Inquiry.objects.all():
    code, name = resolve_country_from_intake(
        message=inq.message,
        phone=inq.phone,
        raw_country_code=inq.country_code if (inq.country_code and inq.country_code != "+91") else ""
    )
    inq.country_code = code
    inq.country_name = name
    Inquiry.objects.filter(pk=inq.pk).update(country_code=code, country_name=name)
    updated_count += 1
    print(f"#{inq.id}: {inq.name} -> {name} ({code}) [Phone: {inq.phone}]")

print(f"\nSuccessfully backfilled {updated_count} / {total_inquiries} inquiries.")
