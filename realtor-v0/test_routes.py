#!/usr/bin/env python
"""Test all routes are configured correctly"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.urls import reverse
from django.test import RequestFactory

# Test routes
routes_to_test = [
    ('home', '/en/'),
    ('services', '/en/services/'),
    ('about', '/en/about/'),
    ('management', '/en/management/'),
    ('contact', '/en/contact/'),
    ('property_list', '/en/properties/'),
]

print("Testing Routes:\n")
print("-" * 60)

for route_name, expected_path in routes_to_test:
    try:
        url = reverse(route_name)
        status = "✅ OK" if url == expected_path else f"⚠️  Got: {url}"
        print(f"{route_name:20} -> {expected_path:30} {status}")
    except Exception as e:
        print(f"{route_name:20} -> {expected_path:30} ❌ ERROR: {e}")

print("-" * 60)
print("\nNote: Routes use language prefix (/en/, /ta/, /hi/)")
