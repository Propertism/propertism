#!/usr/bin/env python
"""
Production Blog Diagnostic Script

Run this on production to verify blog articles and URL routing.
Usage: python manage.py shell < check_production_blog.py
"""

from django.urls import reverse
from content.models import BlogPost
from django.test import Client

print("\n" + "="*70)
print("PRODUCTION BLOG DIAGNOSTIC")
print("="*70)

# Check 1: Articles in database
print("\n1. CHECKING DATABASE FOR PUBLISHED ARTICLES")
print("-" * 70)
published_count = BlogPost.objects.filter(is_published=True).count()
print(f"Published articles in database: {published_count}")

if published_count == 0:
    print("⚠️  NO PUBLISHED ARTICLES FOUND")
    print("Action required: Run 'python manage.py seed_knowledge_hub_phase_a --publish'")
else:
    print("✓ Articles found in database")

# Check 2: Verify specific articles
print("\n2. VERIFYING SPECIFIC ARTICLES")
print("-" * 70)

test_slugs = [
    'nri-property-management-chennai-complete-guide',
    'how-nris-can-sell-property-in-india-from-abroad',
    'power-of-attorney-for-nris-complete-guide',
    'how-to-verify-property-documents-chennai',
    'patta-transfer-process-explained',
    'encumbrance-certificate-guide-for-nris',
    'property-tax-guide-chennai-nris',
    'capital-gains-tax-property-sale-nris',
    'tenant-management-guide-overseas-property-owners',
    'nri-property-maintenance-checklist',
]

found_count = 0
for slug in test_slugs:
    article = BlogPost.objects.filter(slug=slug, is_published=True).first()
    if article:
        print(f"✓ {slug}")
        found_count += 1
    else:
        print(f"✗ {slug} - NOT FOUND or NOT PUBLISHED")

print(f"\nResult: {found_count}/10 articles found and published")

# Check 3: URL routing
print("\n3. CHECKING URL ROUTING")
print("-" * 70)

try:
    test_url = reverse('blog_post', kwargs={'slug': 'nri-property-management-chennai-complete-guide'})
    print(f"✓ URL routing works")
    print(f"  Route: /blog/nri-property-management-chennai-complete-guide/")
    print(f"  Resolved to: {test_url}")
except Exception as e:
    print(f"✗ URL routing error: {e}")

# Check 4: View accessibility
print("\n4. TESTING VIEW ACCESSIBILITY (via Django test client)")
print("-" * 70)

client = Client()
test_slug = 'nri-property-management-chennai-complete-guide'
test_url = f'/blog/{test_slug}/'

try:
    response = client.get(test_url)
    print(f"Testing: {test_url}")
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ View is accessible and returns 200 OK")
    elif response.status_code == 404:
        print("✗ View returns 404 NOT FOUND")
        print("  Possible causes:")
        print("    - URL not in urlpatterns")
        print("    - View not configured correctly")
        print("    - Article not published in this environment")
    else:
        print(f"⚠️  Unexpected status: {response.status_code}")
except Exception as e:
    print(f"✗ Error testing view: {e}")

# Check 5: All blog articles list
print("\n5. ALL PUBLISHED BLOG ARTICLES")
print("-" * 70)

all_articles = BlogPost.objects.filter(is_published=True).order_by('slug')
if all_articles.exists():
    for i, article in enumerate(all_articles, 1):
        print(f"{i}. {article.slug}")
        print(f"   Title: {article.title}")
        print(f"   URL: /blog/{article.slug}/")
else:
    print("No published articles found")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

if published_count == 10 and found_count == 10:
    print("✓ ALL SYSTEMS OPERATIONAL")
    print("  - 10/10 articles found in database")
    print("  - URL routing configured")
    print("  - Ready for production testing")
elif published_count == 0:
    print("✗ CRITICAL: NO ARTICLES IN DATABASE")
    print("  Action: python manage.py seed_knowledge_hub_phase_a --publish")
elif published_count > 0 and found_count < 10:
    print("⚠️  PARTIAL: Some articles missing")
    print(f"  Found: {found_count}/10")
    print("  Action: Check individual article status")
else:
    print("⚠️  CHECK DETAILS ABOVE")

print("="*70 + "\n")
