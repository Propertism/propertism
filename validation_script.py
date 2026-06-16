#!/usr/bin/env python
"""
Comprehensive validation script for SCCB-PROP-KNOWLEDGE-HUB-ROUTING-VALIDATION-AND-SETTINGS-ANNEXURE-1606
Phase 1: Settings Validation
Phase 2: BlogPost & Routing Validation
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.conf import settings
from django.test import Client
from django.urls import resolve
from content.models import BlogPost
import traceback

print("=" * 80)
print("PHASE 1 - DJANGO SETTINGS VALIDATION")
print("=" * 80)

# Check environment variables
print(f"\nEnvironment Variables:")
print(f"  DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT SET')}")
print(f"  DJANGO_ENV: {os.environ.get('DJANGO_ENV', 'NOT SET')}")
print(f"  DEBUG: {os.environ.get('DEBUG', 'NOT SET')}")
db_url = os.environ.get('DATABASE_URL', 'NOT SET')
if db_url != 'NOT SET':
    db_url = db_url[:50] + "..." if len(db_url) > 50 else db_url
print(f"  DATABASE_URL: {db_url}")

# Check active settings
print(f"\nActive Django Settings:")
print(f"  DEBUG: {settings.DEBUG}")
print(f"  DATABASES['default']['ENGINE']: {settings.DATABASES['default']['ENGINE']}")
db_name = settings.DATABASES['default'].get('NAME', 'N/A')
if isinstance(db_name, str) and len(db_name) > 60:
    db_name = db_name[:60] + "..."
print(f"  DATABASES['default']['NAME']: {db_name}")
print(f"  DATABASES['default']['HOST']: {settings.DATABASES['default'].get('HOST', 'N/A')}")
print(f"  DATABASES['default']['PORT']: {settings.DATABASES['default'].get('PORT', 'N/A')}")

# Check if PostgreSQL or SQLite
if 'postgresql' in settings.DATABASES['default']['ENGINE']:
    print(f"  ✓ PostgreSQL configured")
elif 'sqlite3' in settings.DATABASES['default']['ENGINE']:
    print(f"  ✓ SQLite configured")

print("\n" + "=" * 80)
print("PHASE 2 - BLOGPOST DATABASE VALIDATION")
print("=" * 80)

# Count total and published
total_posts = BlogPost.objects.count()
published_posts = BlogPost.objects.filter(is_published=True).count()
print(f"\nBlogPost Count:")
print(f"  Total in database: {total_posts}")
print(f"  Published (is_published=True): {published_posts}")

# List all published articles
print(f"\nPublished Article Slugs:")
slugs_list = list(BlogPost.objects.filter(is_published=True).values_list('slug', 'title'))
if slugs_list:
    for i, (slug, title) in enumerate(slugs_list, 1):
        print(f"  {i}. {slug}")
        print(f"     Title: {title}")
else:
    print(f"  ✗ No published articles found!")

# Test specific article
print(f"\nTesting specific article lookup:")
test_slug = 'nri-property-management-chennai-complete-guide'
try:
    post = BlogPost.objects.get(slug=test_slug, is_published=True)
    print(f"  ✓ Found: {test_slug}")
    print(f"    - Title: {post.title}")
    print(f"    - is_published: {post.is_published}")
    print(f"    - Published Date: {post.published_date}")
except BlogPost.DoesNotExist:
    print(f"  ✗ NOT FOUND: {test_slug}")

print("\n" + "=" * 80)
print("PHASE 3 - URL ROUTING VALIDATION")
print("=" * 80)

# Test URL resolution
print(f"\nTesting URL routing:")

# Test blog post URL pattern
test_url = f'/blog/{test_slug}/'
print(f"\n  URL: {test_url}")

try:
    match = resolve(test_url)
    print(f"  ✓ Resolved to view: {match.func.__name__}")
    print(f"    - View module: {match.func.__module__}")
    print(f"    - URL name: {match.url_name}")
    print(f"    - Kwargs: {match.kwargs}")
except Exception as e:
    print(f"  ✗ Resolution failed: {e}")

print("\n" + "=" * 80)
print("PHASE 4 - HTTP REQUEST TEST (Django Test Client)")
print("=" * 80)

client = Client()
print(f"\nTesting HTTP GET {test_url}:")

try:
    response = client.get(test_url)
    print(f"  Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"  ✓ SUCCESS - Article accessible")
        # Try to find context data
        if hasattr(response, 'context') and response.context:
            post_obj = response.context.get('post')
            if post_obj:
                print(f"    - Post title in context: {post_obj.title}")
    elif response.status_code == 404:
        print(f"  ✗ 404 NOT FOUND")
        print(f"    Reason: Article exists in DB but URL routing issue detected")
    else:
        print(f"  ✗ Unexpected status code: {response.status_code}")
        
except Exception as e:
    print(f"  ✗ Request failed: {e}")
    traceback.print_exc()

print("\n" + "=" * 80)
print("PHASE 5 - INSIGHTS PAGE TEST")
print("=" * 80)

print(f"\nTesting /insights/ URL:")
try:
    response = client.get('/insights/')
    print(f"  Status Code: {response.status_code}")
    if response.status_code == 302:
        print(f"  ✓ Redirect detected")
        print(f"    Location: {response.get('Location', 'N/A')}")
    elif response.status_code == 200:
        print(f"  ✓ Page loads")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 80)
print("END OF VALIDATION")
print("=" * 80)
