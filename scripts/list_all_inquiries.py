import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")

import django
django.setup()

from properties.models import Inquiry

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

inquiries = Inquiry.objects.all().order_by("-created_at")
print(f"Total inquiries in DB: {len(inquiries)}")
print("-" * 80)
for i in inquiries:
    msg_cleaned = i.message.replace('\n', ' ')[:60]
    print(f"ID: {i.id} | Name: {i.name} | Property: {i.property} | Status: {i.status} | Message: {msg_cleaned}...")
