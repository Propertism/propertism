import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import CompanyInfo
from django.conf import settings

c = CompanyInfo.objects.first()
if c:
    print(f"✅ CompanyInfo found")
    print(f"Hero image field: {c.hero_image}")
    if c.hero_image:
        print(f"Hero image URL: {c.hero_image.url}")
        print(f"Hero image path: {c.hero_image.path}")
        print(f"File exists: {os.path.exists(c.hero_image.path)}")
    else:
        print("❌ No hero image set")
    print(f"\nMEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
else:
    print("❌ No CompanyInfo found")
