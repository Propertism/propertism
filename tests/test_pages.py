"""
SCCB-46 Task 1: Page Load Testing
Tests all pages load correctly without errors
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from properties.models import Property
from content.models import BlogPost
from colorama import init, Fore, Style

init(autoreset=True)

class PageLoadTester:
    def __init__(self):
        self.client = Client()
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def test_url(self, name, url, expected_status=200):
        """Test a single URL"""
        try:
            response = self.client.get(url)
            status = response.status_code
            
            if status == expected_status:
                self.passed += 1
                self.results.append({
                    'name': name,
                    'url': url,
                    'status': status,
                    'passed': True
                })
                print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {name:30} | {url:40} | Status: {status}")
                return True
            else:
                self.failed += 1
                self.results.append({
                    'name': name,
                    'url': url,
                    'status': status,
                    'passed': False,
                    'error': f'Expected {expected_status}, got {status}'
                })
                print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {name:30} | {url:40} | Status: {status} (expected {expected_status})")
                return False
        except Exception as e:
            self.failed += 1
            self.results.append({
                'name': name,
                'url': url,
                'passed': False,
                'error': str(e)
            })
            print(f"{Fore.RED}✗ ERROR{Style.RESET_ALL} | {name:30} | {url:40} | {str(e)}")
            return False
    
    def run_tests(self):
        """Run all page load tests"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"SCCB-46 TASK 1: PAGE LOAD TESTING")
        print(f"{'='*80}{Style.RESET_ALL}\n")
        
        # Test static pages (English)
        print(f"{Fore.YELLOW}Testing Static Pages (English)...{Style.RESET_ALL}")
        self.test_url("Home (EN)", "/en/")
        self.test_url("Services (EN)", "/en/services/")
        self.test_url("About (EN)", "/en/about/")
        self.test_url("Management (EN)", "/en/management/")
        self.test_url("Contact (EN)", "/en/contact/")
        self.test_url("Blog (EN)", "/en/blog/")
        
        # Test static pages (Tamil)
        print(f"\n{Fore.YELLOW}Testing Static Pages (Tamil)...{Style.RESET_ALL}")
        self.test_url("Home (TA)", "/ta/")
        self.test_url("Services (TA)", "/ta/services/")
        
        # Test static pages (Hindi)
        print(f"\n{Fore.YELLOW}Testing Static Pages (Hindi)...{Style.RESET_ALL}")
        self.test_url("Home (HI)", "/hi/")
        self.test_url("Services (HI)", "/hi/services/")
        
        # Test API endpoints
        print(f"\n{Fore.YELLOW}Testing API Endpoints...{Style.RESET_ALL}")
        self.test_url("Properties API", "/api/properties/")
        self.test_url("Search API", "/api/search/")
        
        # Test SEO files
        print(f"\n{Fore.YELLOW}Testing SEO Files...{Style.RESET_ALL}")
        self.test_url("Sitemap", "/sitemap.xml")
        self.test_url("Robots.txt", "/robots.txt")
        
        # Test property detail pages (if properties exist)
        print(f"\n{Fore.YELLOW}Testing Dynamic Pages...{Style.RESET_ALL}")
        properties = Property.objects.filter(status='available')[:3]
        if properties.exists():
            for prop in properties:
                self.test_url(f"Property: {prop.title[:20]}", f"/en/properties/{prop.slug}/")
        else:
            print(f"{Fore.YELLOW}⚠ No properties found to test{Style.RESET_ALL}")
        
        # Test blog posts (if exist)
        blog_posts = BlogPost.objects.filter(is_published=True)[:2]
        if blog_posts.exists():
            for post in blog_posts:
                self.test_url(f"Blog: {post.title[:20]}", f"/en/blog/{post.slug}/")
        else:
            print(f"{Fore.YELLOW}⚠ No blog posts found to test{Style.RESET_ALL}")
        
        # Test 404 page
        print(f"\n{Fore.YELLOW}Testing Error Pages...{Style.RESET_ALL}")
        self.test_url("404 Page", "/en/nonexistent-page/", expected_status=404)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"TEST SUMMARY")
        print(f"{'='*80}{Style.RESET_ALL}")
        print(f"Total Tests: {total}")
        print(f"{Fore.GREEN}Passed: {self.passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.failed}{Style.RESET_ALL}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if self.failed == 0:
            print(f"\n{Fore.GREEN}✓ ALL PAGE LOAD TESTS PASSED{Style.RESET_ALL}")
            return True
        else:
            print(f"\n{Fore.RED}✗ SOME TESTS FAILED - REVIEW REQUIRED{Style.RESET_ALL}")
            return False

if __name__ == '__main__':
    tester = PageLoadTester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)
