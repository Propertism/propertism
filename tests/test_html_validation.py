"""
SCCB-46 Task 6: HTML/CSS Validation
Validates HTML structure and semantic correctness
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.test import Client
from colorama import init, Fore, Style
import re

init(autoreset=True)

class HTMLValidator:
    def __init__(self):
        self.client = Client()
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def test_doctype(self, url, name):
        """Check for proper DOCTYPE"""
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        
        if '<!DOCTYPE html>' in content or '<!doctype html>' in content:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {name:20} | DOCTYPE present")
            self.passed += 1
            return True
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {name:20} | DOCTYPE missing")
            self.failed += 1
            return False
    
    def test_html_lang(self, url, name):
        """Check for lang attribute"""
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        
        if 'lang=' in content[:500]:  # Check in first 500 chars
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {name:20} | lang attribute present")
            self.passed += 1
            return True
        else:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | {name:20} | lang attribute missing")
            self.warnings += 1
            return False
    
    def test_meta_charset(self, url, name):
        """Check for charset meta tag"""
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        
        if 'charset=' in content or 'charset =' in content:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {name:20} | Charset meta tag present")
            self.passed += 1
            return True
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {name:20} | Charset meta tag missing")
            self.failed += 1
            return False
    
    def test_title_tag(self, url, name):
        """Check for title tag"""
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
            if title and len(title) > 0:
                print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {name:20} | Title: {title[:40]}")
                self.passed += 1
                return True
            else:
                print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {name:20} | Title tag empty")
                self.failed += 1
                return False
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {name:20} | Title tag missing")
            self.failed += 1
            return False
    
    def test_semantic_html(self, url, name):
        """Check for semantic HTML5 tags"""
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        
        semantic_tags = ['<header', '<nav', '<main', '<footer', '<article', '<section']
        found_tags = [tag for tag in semantic_tags if tag in content]
        
        if len(found_tags) >= 3:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {name:20} | Semantic HTML5 tags used ({len(found_tags)} types)")
            self.passed += 1
            return True
        else:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | {name:20} | Limited semantic HTML5 usage")
            self.warnings += 1
            return False
    
    def test_alt_attributes(self, url, name):
        """Check for alt attributes on images"""
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        
        # Find all img tags
        img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        
        if not img_tags:
            print(f"{Fore.YELLOW}⚠ INFO{Style.RESET_ALL} | {name:20} | No images found")
            self.passed += 1
            return True
        
        missing_alt = 0
        for img in img_tags:
            if 'alt=' not in img.lower():
                missing_alt += 1
        
        if missing_alt == 0:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {name:20} | All images have alt attributes ({len(img_tags)} images)")
            self.passed += 1
            return True
        else:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | {name:20} | {missing_alt}/{len(img_tags)} images missing alt")
            self.warnings += 1
            return False
    
    def test_duplicate_ids(self, url, name):
        """Check for duplicate IDs"""
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        
        # Find all id attributes
        ids = re.findall(r'id=["\']([^"\']+)["\']', content, re.IGNORECASE)
        
        if not ids:
            print(f"{Fore.YELLOW}⚠ INFO{Style.RESET_ALL} | {name:20} | No IDs found")
            self.passed += 1
            return True
        
        unique_ids = set(ids)
        if len(ids) == len(unique_ids):
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {name:20} | No duplicate IDs ({len(ids)} unique)")
            self.passed += 1
            return True
        else:
            duplicates = len(ids) - len(unique_ids)
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {name:20} | {duplicates} duplicate ID(s) found")
            self.failed += 1
            return False
    
    def validate_page(self, url, name):
        """Run all validations on a page"""
        print(f"\n{Fore.CYAN}Validating: {name}{Style.RESET_ALL}")
        self.test_doctype(url, name)
        self.test_html_lang(url, name)
        self.test_meta_charset(url, name)
        self.test_title_tag(url, name)
        self.test_semantic_html(url, name)
        self.test_alt_attributes(url, name)
        self.test_duplicate_ids(url, name)
    
    def run_tests(self):
        """Run all HTML validation tests"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"SCCB-46 TASK 6: HTML/CSS VALIDATION")
        print(f"{'='*80}{Style.RESET_ALL}\n")
        
        pages = [
            ('/en/', 'Home'),
            ('/en/services/', 'Services'),
            ('/en/about/', 'About'),
            ('/en/contact/', 'Contact'),
        ]
        
        for url, name in pages:
            self.validate_page(url, name)
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed + self.warnings
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"TEST SUMMARY")
        print(f"{'='*80}{Style.RESET_ALL}")
        print(f"Total Checks: {total}")
        print(f"{Fore.GREEN}Passed: {self.passed}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Warnings: {self.warnings}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.failed}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Additional Validation:{Style.RESET_ALL}")
        print(f"  • W3C HTML Validator: https://validator.w3.org/")
        print(f"  • W3C CSS Validator: https://jigsaw.w3.org/css-validator/")
        
        if self.failed == 0:
            print(f"\n{Fore.GREEN}✓ HTML VALIDATION PASSED{Style.RESET_ALL}")
            if self.warnings > 0:
                print(f"{Fore.YELLOW}⚠ Review warnings for best practices{Style.RESET_ALL}")
            return True
        else:
            print(f"\n{Fore.RED}✗ HTML VALIDATION FAILED - FIX ERRORS{Style.RESET_ALL}")
            return False

if __name__ == '__main__':
    validator = HTMLValidator()
    validator.run_tests()
