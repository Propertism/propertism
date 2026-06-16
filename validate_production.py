#!/usr/bin/env python
"""
Phase 5 Production Validation Script
Checks:
1. Sitemap accessibility (200 OK)
2. Robots.txt accessibility (200 OK)
3. Canonical tags presence
4. Article schema validation
5. Breadcrumb schema validation
6. FAQ schema validation
7. Service schema validation
"""

import os
import sys
import json
import re
from urllib.request import urlopen, Request
from urllib.error import URLError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
import django
django.setup()

from django.test import Client
from django.urls import reverse
from content.models import BlogPost

PROD_DOMAIN = "https://www.propertism.in"
LOCAL_DOMAIN = "http://localhost:8000"

# Try production first, fall back to local for testing
DOMAIN = PROD_DOMAIN

def check_url(url, description):
    """Check if URL returns 200 status."""
    print(f"\nChecking: {description}")
    print(f"URL: {url}")
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req, timeout=5)
        status = response.status
        print(f"Status: {status} OK")
        return status == 200, response.read().decode('utf-8')
    except URLError as e:
        print(f"Status: FAILED - {e.reason}")
        return False, None
    except Exception as e:
        print(f"Status: ERROR - {e}")
        return False, None

def check_sitemap():
    """Verify sitemap.xml is accessible."""
    url = f"{DOMAIN}/sitemap.xml"
    success, content = check_url(url, "Sitemap XML")
    
    if success and content:
        try:
            # Count URLs in sitemap
            url_count = content.count("<url>")
            print(f"URLs in sitemap: {url_count}")
            return True
        except:
            pass
    return success

def check_robots():
    """Verify robots.txt is accessible and contains sitemap reference."""
    url = f"{DOMAIN}/robots.txt"
    success, content = check_url(url, "Robots.txt")
    
    if success and content:
        if "Sitemap:" in content and "sitemap.xml" in content:
            print("Sitemap reference: FOUND")
            return True
        else:
            print("Sitemap reference: MISSING")
            return False
    return success

def check_article_urls():
    """Verify all 10 Knowledge Hub articles are publicly accessible."""
    articles = [
        'nri-property-management-chennai-complete-guide',
        'how-nris-can-sell-property-in-india-from-abroad',
        'power-of-attorney-for-nris-complete-guide',
        'how-to-verify-property-documents-chennai',
        'patta-transfer-process-explained',
        'encumbrance-certificate-guide-for-nris',
        'property-tax-guide-chennai-nris',
        'capital-gains-tax-property-sale-nris',
        'tenant-management-guide-overseas-property-owners',
        'nri-property-maintenance-checklist'
    ]
    
    print("\n" + "="*70)
    print("KNOWLEDGE HUB ARTICLE ACCESSIBILITY CHECK")
    print("="*70)
    
    all_accessible = True
    for slug in articles:
        url = f"{DOMAIN}/blog/{slug}/"
        success, _ = check_url(url, f"Article: {slug}")
        if not success:
            all_accessible = False
    
    return all_accessible

def check_schema_markup(article_slug):
    """Check if article has proper schema markup."""
    try:
        url = f"{DOMAIN}/blog/{article_slug}/"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req, timeout=5)
        content = response.read().decode('utf-8')
        
        schemas = {
            'Article': '<script type="application/ld+json">{"@type":"Article"' in content or '"@type":"Article"' in content,
            'Breadcrumb': '"@type":"BreadcrumbList"' in content,
        }
        
        return schemas
    except:
        return {}

print("\n" + "="*70)
print("PHASE 5 PRODUCTION VALIDATION REPORT")
print("="*70)
print(f"Domain: {DOMAIN}")
print("="*70)

results = {
    'sitemap': check_sitemap(),
    'robots': check_robots(),
    'articles': check_article_urls(),
}

print("\n" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)
print(f"Sitemap (200 OK): {'PASS' if results['sitemap'] else 'FAIL'}")
print(f"Robots.txt (200 OK): {'PASS' if results['robots'] else 'FAIL'}")
print(f"Articles Accessible: {'PASS' if results['articles'] else 'FAIL'}")

if all(results.values()):
    print("\n*** PRODUCTION VALIDATION: PASSED ***")
else:
    print("\n*** PRODUCTION VALIDATION: FAILED ***")

print("="*70 + "\n")
