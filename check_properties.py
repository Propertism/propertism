#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from properties.models import Property, PropertyType

print("=== Property Database Check ===")
print(f"Total properties: {Property.objects.count()}")
print(f"Available properties: {Property.objects.filter(status='available').count()}")
print(f"\nProperty Types:")
for pt in PropertyType.objects.all():
    count = Property.objects.filter(property_type=pt).count()
    print(f"  - {pt.name} (slug: {pt.slug}): {count} properties")

print(f"\nPrice Types:")
for price_type in ['sale', 'rent']:
    count = Property.objects.filter(price_type=price_type).count()
    print(f"  - {price_type}: {count} properties")

print(f"\nFlats for Sale Query:")
flats_sale = Property.objects.filter(
    property_type__slug='apartment',
    price_type='sale',
    status='available'
)
print(f"  Found: {flats_sale.count()} properties")
if flats_sale.exists():
    for prop in flats_sale[:5]:
        print(f"    - {prop.title} ({prop.location})")
