#!/usr/bin/env python
"""
Test if Tamil content exists in database on live server
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import CompanyInfo
from django.utils import translation

print("=" * 60)
print("TESTING TRANSLATION ON LIVE SERVER")
print("=" * 60)

# Get company info
company = CompanyInfo.objects.first()

if not company:
    print("❌ No company info found in database!")
    exit(1)

print("\n📊 DATABASE FIELDS:")
print(f"hero_title (default): {company.hero_title}")
print(f"hero_title_en: {company.hero_title_en}")
print(f"hero_title_ta: {company.hero_title_ta}")
print(f"hero_title_hi: {company.hero_title_hi}")

print("\n🌍 TESTING LANGUAGE ACTIVATION:")

# Test English
translation.activate('en')
print(f"\nEN (activated): {company.hero_title}")

# Test Tamil
translation.activate('ta')
print(f"TA (activated): {company.hero_title}")

# Test Hindi
translation.activate('hi')
print(f"HI (activated): {company.hero_title}")

print("\n" + "=" * 60)

if company.hero_title_ta and 'சென்னை' in company.hero_title_ta:
    print("✅ Tamil content EXISTS in database!")
else:
    print("❌ Tamil content MISSING from database!")

if company.hero_title_hi and 'चेन्नई' in company.hero_title_hi:
    print("✅ Hindi content EXISTS in database!")
else:
    print("❌ Hindi content MISSING from database!")

print("=" * 60)
