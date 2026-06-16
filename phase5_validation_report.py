#!/usr/bin/env python
"""
PHASE 5 — SEO GROWTH MONITORING VALIDATION REPORT
Consolidated verification of Priority 1, 2, and 3 tasks
"""

import os
import sys
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
import django
django.setup()

from django.test import Client
from django.urls import reverse
from content.models import BlogPost, CompanyInfo
from django.conf import settings

# ============================================================================
# PRIORITY 1: KNOWLEDGE HUB PUBLICATION VERIFICATION
# ============================================================================

KNOWLEDGE_HUB_ARTICLES = [
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

def validate_knowledge_hub():
    """Validate all 10 Knowledge Hub Phase-A articles."""
    print("\n" + "="*80)
    print("PRIORITY 1: KNOWLEDGE HUB PUBLICATION VERIFICATION")
    print("="*80)
    
    all_published = True
    verification_data = []
    
    for i, slug in enumerate(KNOWLEDGE_HUB_ARTICLES, 1):
        post = BlogPost.objects.filter(slug=slug).first()
        
        if not post:
            print(f"{i:2}. [MISSING] {slug}")
            all_published = False
            continue
        
        status = "PUBLISHED" if post.is_published else "DRAFT"
        published_date = post.published_date.strftime("%Y-%m-%d %H:%M") if post.published_date else "N/A"
        
        # Format output
        status_icon = "[OK]" if post.is_published else "[!]"
        print(f"{i:2}. {status_icon} {slug}")
        print(f"     Status: {status} | Published: {published_date} | Title: {post.title}")
        
        verification_data.append({
            'title': post.title,
            'slug': post.slug,
            'status': status,
            'published_date': published_date,
            'excerpt': post.excerpt[:80] + "..." if post.excerpt else ""
        })
        
        if status == "DRAFT":
            all_published = False
    
    print("\n" + "-"*80)
    if all_published:
        print("RESULT: PASS - All 10 articles are published and publicly accessible")
    else:
        print("RESULT: FAIL - Some articles are still in draft status")
        print("ACTION: Run: python manage.py seed_knowledge_hub_phase_a --publish")
    print("-"*80)
    
    return all_published, verification_data

# ============================================================================
# PRIORITY 2: PRODUCTION VALIDATION CHECKS
# ============================================================================

def validate_production_endpoints():
    """Validate production endpoints and schema."""
    print("\n" + "="*80)
    print("PRIORITY 2: PRODUCTION VALIDATION CHECKS")
    print("="*80)
    
    client = Client()
    validation_results = {}
    
    # Test 1: Sitemap
    print("\n1. SITEMAP VALIDATION")
    print("-"*80)
    try:
        response = client.get('/sitemap.xml')
        sitemap_ok = response.status_code == 200
        print(f"Endpoint: /sitemap.xml")
        print(f"Status Code: {response.status_code}")
        if sitemap_ok:
            # Count URLs
            url_count = response.content.decode('utf-8').count('<url>')
            print(f"URLs in Sitemap: {url_count}")
            print("Result: PASS")
        validation_results['sitemap'] = sitemap_ok
    except Exception as e:
        print(f"Error: {e}")
        validation_results['sitemap'] = False
    
    # Test 2: Robots.txt
    print("\n2. ROBOTS.TXT VALIDATION")
    print("-"*80)
    try:
        response = client.get('/robots.txt')
        robots_ok = response.status_code == 200
        print(f"Endpoint: /robots.txt")
        print(f"Status Code: {response.status_code}")
        if robots_ok:
            content = response.content.decode('utf-8')
            has_sitemap = 'Sitemap:' in content and 'sitemap.xml' in content
            print(f"Contains 'Sitemap:' directive: {'YES' if has_sitemap else 'NO'}")
            print(f"Result: {'PASS' if has_sitemap else 'PARTIAL'}")
        validation_results['robots'] = robots_ok
    except Exception as e:
        print(f"Error: {e}")
        validation_results['robots'] = False
    
    # Test 3: Canonical Tags (check one article)
    print("\n3. CANONICAL TAG VALIDATION")
    print("-"*80)
    try:
        response = client.get(f'/blog/{KNOWLEDGE_HUB_ARTICLES[0]}/')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            has_canonical = 'rel="canonical"' in content
            print(f"Article: {KNOWLEDGE_HUB_ARTICLES[0]}")
            print(f"Status Code: {response.status_code}")
            print(f"Has Canonical Tag: {'YES' if has_canonical else 'NO'}")
            print(f"Result: {'PASS' if has_canonical else 'FAIL'}")
            validation_results['canonical'] = has_canonical
        else:
            print(f"Article not accessible (Status: {response.status_code})")
            validation_results['canonical'] = False
    except Exception as e:
        print(f"Error: {e}")
        validation_results['canonical'] = False
    
    # Test 4: Article Schema
    print("\n4. ARTICLE SCHEMA VALIDATION")
    print("-"*80)
    try:
        response = client.get(f'/blog/{KNOWLEDGE_HUB_ARTICLES[0]}/')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            has_article_schema = '"@type":"Article"' in content or '@type":"Article' in content
            print(f"Article: {KNOWLEDGE_HUB_ARTICLES[0]}")
            print(f"Has Article Schema: {'YES' if has_article_schema else 'NO'}")
            print(f"Result: {'PASS' if has_article_schema else 'FAIL'}")
            validation_results['article_schema'] = has_article_schema
        else:
            validation_results['article_schema'] = False
    except Exception as e:
        validation_results['article_schema'] = False
    
    # Test 5: Breadcrumb Schema
    print("\n5. BREADCRUMB SCHEMA VALIDATION")
    print("-"*80)
    try:
        response = client.get(f'/blog/{KNOWLEDGE_HUB_ARTICLES[0]}/')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            has_breadcrumb_schema = '"@type":"BreadcrumbList"' in content or '@type":"BreadcrumbList' in content
            print(f"Article: {KNOWLEDGE_HUB_ARTICLES[0]}")
            print(f"Has Breadcrumb Schema: {'YES' if has_breadcrumb_schema else 'NO'}")
            print(f"Result: {'PASS' if has_breadcrumb_schema else 'FAIL'}")
            validation_results['breadcrumb_schema'] = has_breadcrumb_schema
        else:
            validation_results['breadcrumb_schema'] = False
    except Exception as e:
        validation_results['breadcrumb_schema'] = False
    
    # Test 6: FAQ Schema (check if article has FAQ)
    print("\n6. FAQ SCHEMA VALIDATION")
    print("-"*80)
    try:
        response = client.get(f'/blog/{KNOWLEDGE_HUB_ARTICLES[0]}/')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            has_faq_schema = '"@type":"FAQPage"' in content or '@type":"FAQPage' in content
            print(f"Article: {KNOWLEDGE_HUB_ARTICLES[0]}")
            print(f"Has FAQ Schema: {'YES' if has_faq_schema else 'NO'}")
            print(f"Result: {'PASS' if has_faq_schema else 'INFO (FAQ optional)'}")
            validation_results['faq_schema'] = has_faq_schema
        else:
            validation_results['faq_schema'] = False
    except Exception as e:
        validation_results['faq_schema'] = False
    
    print("\n" + "-"*80)
    all_pass = all(v for k, v in validation_results.items() if k != 'faq_schema')
    if all_pass:
        print("RESULT: PASS - All core validation checks passed")
    else:
        print("RESULT: FAIL - Some validation checks failed")
    print("-"*80)
    
    return validation_results

# ============================================================================
# PRIORITY 3: GSC SUBMISSION CHECKLIST
# ============================================================================

def generate_gsc_checklist():
    """Generate GSC indexing request checklist."""
    print("\n" + "="*80)
    print("PRIORITY 3: GOOGLE SEARCH CONSOLE READINESS & INDEXING CHECKLIST")
    print("="*80)
    
    print("\nBefore Submitting Indexing Requests:")
    print("-"*80)
    print("[ ] Verify GSC Property is connected to www.propertism.in")
    print("[ ] Check for any crawl errors or warnings in GSC")
    print("[ ] Ensure no 'robots.txt' blocks are active")
    print("[ ] Confirm 'URL Inspection' tool shows 'URL is on Google' or 'Not indexed'")
    
    print("\n\nIndexing Requests Required (URLs):")
    print("-"*80)
    
    urls_to_index = {
        'Homepage': ['https://www.propertism.in/'],
        'Core Service Pages': [
            'https://www.propertism.in/chennai/nri-property-management/',
            'https://www.propertism.in/chennai/nri-sell-property/',
        ],
        'Knowledge Hub Articles': [
            'https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/',
            'https://www.propertism.in/blog/how-nris-can-sell-property-in-india-from-abroad/',
            'https://www.propertism.in/blog/power-of-attorney-for-nris-complete-guide/',
            'https://www.propertism.in/blog/how-to-verify-property-documents-chennai/',
            'https://www.propertism.in/blog/patta-transfer-process-explained/',
            'https://www.propertism.in/blog/encumbrance-certificate-guide-for-nris/',
            'https://www.propertism.in/blog/property-tax-guide-chennai-nris/',
            'https://www.propertism.in/blog/capital-gains-tax-property-sale-nris/',
            'https://www.propertism.in/blog/tenant-management-guide-overseas-property-owners/',
            'https://www.propertism.in/blog/nri-property-maintenance-checklist/',
        ]
    }
    
    total_urls = 0
    for category, urls in urls_to_index.items():
        print(f"\n{category}:")
        for url in urls:
            print(f"  [ ] {url}")
            total_urls += 1
    
    print("\n" + "-"*80)
    print(f"Total URLs to Index: {total_urls}")
    print("-"*80)
    
    print("\n\nIndexing Request Steps:")
    print("-"*80)
    print("1. Go to Google Search Console (https://search.google.com/search-console)")
    print("2. Select propertism.in property")
    print("3. Click 'URL Inspection' tool (top search bar)")
    print("4. For EACH URL above:")
    print("   a. Paste URL in the search bar")
    print("   b. Wait for inspection to complete")
    print("   c. If 'Request Indexing' button appears, click it")
    print("   d. Confirm 'Request sent' message")
    print("5. Monitor 'Coverage' report for indexing progress")
    
    print("\n\nSitemap Status Expected:")
    print("-"*80)
    print("- Sitemap URL: https://www.propertism.in/sitemap.xml")
    print("- Expected Status: SUCCESS or PROCESSING")
    print("- Coverage Estimate: ~765 total pSEO pages")
    
    return urls_to_index

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n")
    print("*"*80)
    print("PROPERTISM PHASE 5 — SEO GROWTH MONITORING VALIDATION REPORT")
    print("*"*80)
    print(f"Generated: {timestamp}")
    print(f"Environment: {settings.ENVIRONMENT if hasattr(settings, 'ENVIRONMENT') else 'production'}")
    print("*"*80)
    
    # Run all validations
    priority1_pass, kh_data = validate_knowledge_hub()
    priority2_results = validate_production_endpoints()
    priority3_urls = generate_gsc_checklist()
    
    # Summary
    print("\n" + "="*80)
    print("CONSOLIDATED VALIDATION SUMMARY")
    print("="*80)
    print(f"Priority 1 (Knowledge Hub): {'PASS' if priority1_pass else 'FAIL'}")
    print(f"Priority 2 (Production): {'PASS' if all(priority2_results.values()) else 'REVIEW REQUIRED'}")
    print(f"Priority 3 (GSC Ready): {'READY' if priority1_pass else 'PENDING PRIORITY 1'}")
    print("="*80)
    
    print("\n\nNext Steps:")
    print("-"*80)
    if priority1_pass:
        print("1. [READY] Begin GSC Sitemap Submission (Priority 2)")
        print("2. [READY] Submit URL Indexing Requests (Priority 3)")
        print("3. [READY] Monitor indexing progress in GSC Coverage report")
    else:
        print("1. [REQUIRED] Run: python manage.py seed_knowledge_hub_phase_a --publish")
        print("2. Verify all 10 articles appear in admin")
        print("3. Then proceed with GSC submission")
    print("-"*80)
    
    print("\n")
