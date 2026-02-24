#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.utils import translation
from content.models import CompanyInfo

company = CompanyInfo.objects.first()

print("=" * 60)
print("TRANSLATION TEST")
print("=" * 60)

# Test English
translation.activate('en')
print(f"\n🇬🇧 ENGLISH (en):")
print(f"   hero_title: {company.hero_title}")
print(f"   hero_title_en: {company.hero_title_en}")

# Test Tamil
translation.activate('ta')
print(f"\n🇮🇳 TAMIL (ta):")
print(f"   hero_title: {company.hero_title}")
print(f"   hero_title_ta: {company.hero_title_ta}")

# Test Hindi
translation.activate('hi')
print(f"\n🇮🇳 HINDI (hi):")
print(f"   hero_title: {company.hero_title}")
print(f"   hero_title_hi: {company.hero_title_hi}")

print("\n" + "=" * 60)
print("If hero_title changes with language, translation works!")
print("=" * 60)
