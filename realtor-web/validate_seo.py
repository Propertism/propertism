#!/usr/bin/env python
"""
SEO Validation Script for Propertism
Validates SCCB-43 compliance
"""
import os
import sys
import django
import requests
from bs4 import BeautifulSoup

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def validate_page_seo(url, page_name):
    """Validate SEO elements for a page"""
    print(f"\n{'='*70}")
    print(f"Validating: {page_name}")
    print(f"URL: {url}")
    print('='*70)
    
    client = Client()
    response = client.get(url)
    
    if response.status_code != 200:
        print(f"❌ Page not accessible (Status: {response.status_code})")
        return False
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    issues = []
    passed = []
    
    # Check 1: Title tag
    title = soup.find('title')
    if title and title.string and len(title.string) > 0:
        title_length = len(title.string)
        if 50 <= title_length <= 60:
            passed.append(f"✅ Title tag: {title_length} chars (optimal)")
        elif title_length < 50:
            issues.append(f"⚠️  Title tag: {title_length} chars (too short, aim for 50-60)")
        else:
            issues.append(f"⚠️  Title tag: {title_length} chars (too long, aim for 50-60)")
        print(f"   Title: {title.string[:80]}...")
    else:
        issues.append("❌ Missing title tag")
    
    # Check 2: Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        desc_length = len(meta_desc['content'])
        if 150 <= desc_length <= 160:
            passed.append(f"✅ Meta description: {desc_length} chars (optimal)")
        elif desc_length < 150:
            issues.append(f"⚠️  Meta description: {desc_length} chars (too short, aim for 150-160)")
        else:
            issues.append(f"⚠️  Meta description: {desc_length} chars (too long, aim for 150-160)")
        print(f"   Description: {meta_desc['content'][:80]}...")
    else:
        issues.append("❌ Missing meta description")
    
    # Check 3: Canonical URL
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical and canonical.get('href'):
        passed.append("✅ Canonical URL present")
    else:
        issues.append("❌ Missing canonical URL")
    
    # Check 4: Open Graph tags
    og_tags = {
        'og:title': soup.find('meta', attrs={'property': 'og:title'}),
        'og:description': soup.find('meta', attrs={'property': 'og:description'}),
        'og:image': soup.find('meta', attrs={'property': 'og:image'}),
        'og:url': soup.find('meta', attrs={'property': 'og:url'}),
        'og:type': soup.find('meta', attrs={'property': 'og:type'}),
    }
    
    og_present = sum(1 for tag in og_tags.values() if tag)
    if og_present == 5:
        passed.append("✅ All Open Graph tags present (5/5)")
    else:
        issues.append(f"⚠️  Open Graph tags: {og_present}/5 present")
        for tag_name, tag in og_tags.items():
            if not tag:
                print(f"      Missing: {tag_name}")
    
    # Check 5: Twitter Card tags
    twitter_tags = {
        'twitter:card': soup.find('meta', attrs={'property': 'twitter:card'}),
        'twitter:title': soup.find('meta', attrs={'property': 'twitter:title'}),
        'twitter:description': soup.find('meta', attrs={'property': 'twitter:description'}),
        'twitter:image': soup.find('meta', attrs={'property': 'twitter:image'}),
    }
    
    twitter_present = sum(1 for tag in twitter_tags.values() if tag)
    if twitter_present == 4:
        passed.append("✅ All Twitter Card tags present (4/4)")
    else:
        issues.append(f"⚠️  Twitter Card tags: {twitter_present}/4 present")
    
    # Check 6: Structured Data (JSON-LD)
    json_ld = soup.find_all('script', attrs={'type': 'application/ld+json'})
    if json_ld:
        passed.append(f"✅ Structured data present ({len(json_ld)} schemas)")
    else:
        issues.append("⚠️  No structured data (JSON-LD) found")
    
    # Check 7: Images with alt text
    images = soup.find_all('img')
    images_with_alt = sum(1 for img in images if img.get('alt'))
    if images:
        if images_with_alt == len(images):
            passed.append(f"✅ All images have alt text ({len(images)}/{len(images)})")
        else:
            issues.append(f"⚠️  Images with alt text: {images_with_alt}/{len(images)}")
    
    # Check 8: Lazy loading
    images_with_lazy = sum(1 for img in images if img.get('loading') == 'lazy')
    if images_with_lazy > 0:
        passed.append(f"✅ Lazy loading enabled ({images_with_lazy} images)")
    
    # Print results
    print("\nPassed Checks:")
    for item in passed:
        print(f"  {item}")
    
    if issues:
        print("\nIssues Found:")
        for item in issues:
            print(f"  {item}")
    
    # Score
    total_checks = len(passed) + len(issues)
    score = (len(passed) / total_checks * 100) if total_checks > 0 else 0
    print(f"\nSEO Score: {score:.0f}% ({len(passed)}/{total_checks} checks passed)")
    
    return len(issues) == 0

def main():
    """Run SEO validation on all pages"""
    print("\n" + "="*70)
    print("PROPERTISM SEO VALIDATION (SCCB-43 COMPLIANCE)")
    print("="*70)
    
    pages = [
        ('/en/', 'Home Page'),
        ('/en/services/', 'Services Page'),
        ('/en/about/', 'About Page'),
        ('/en/management/', 'Management Page'),
        ('/en/contact/', 'Contact Page'),
        ('/en/properties/', 'Properties Listing'),
    ]
    
    results = []
    for url, name in pages:
        try:
            passed = validate_page_seo(url, name)
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ Error validating {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "⚠️  NEEDS WORK"
        print(f"{status}: {name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\nOverall: {passed_count}/{total_count} pages passed all checks")
    
    # Check sitemap and robots.txt
    print("\n" + "="*70)
    print("ADDITIONAL SEO CHECKS")
    print("="*70)
    
    client = Client()
    
    # Sitemap
    try:
        response = client.get('/sitemap.xml')
        if response.status_code == 200:
            print("✅ sitemap.xml is accessible")
        else:
            print(f"❌ sitemap.xml returned status {response.status_code}")
    except Exception as e:
        print(f"❌ sitemap.xml error: {e}")
    
    # Robots.txt
    try:
        response = client.get('/robots.txt')
        if response.status_code == 200:
            print("✅ robots.txt is accessible")
            if b'Sitemap:' in response.content:
                print("✅ robots.txt references sitemap")
        else:
            print(f"❌ robots.txt returned status {response.status_code}")
    except Exception as e:
        print(f"❌ robots.txt error: {e}")
    
    print("\n" + "="*70)
    print("SCCB-43 COMPLIANCE CHECK COMPLETE")
    print("="*70 + "\n")
    
    if passed_count == total_count:
        print("🎉 All pages passed SEO validation!")
        return 0
    else:
        print("⚠️  Some pages need SEO improvements.")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nValidation cancelled by user.")
        sys.exit(1)
