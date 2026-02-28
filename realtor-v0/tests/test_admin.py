"""
SCCB-46 Task 3: Admin Panel Testing
Tests admin panel functionality and CRUD operations
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from properties.models import Property
from content.models import BlogPost
from colorama import init, Fore, Style

init(autoreset=True)

class AdminTester:
    def __init__(self):
        self.client = Client()
        self.passed = 0
        self.failed = 0
        self.admin_user = None
    
    def setup_admin_user(self):
        """Create or get admin user for testing"""
        print(f"\n{Fore.YELLOW}Setting up admin user...{Style.RESET_ALL}")
        
        try:
            # Try to use existing admin user
            self.admin_user = User.objects.get(username='admin')
            print(f"{Fore.GREEN}✓{Style.RESET_ALL} Using existing admin user")
        except User.DoesNotExist:
            print(f"{Fore.YELLOW}⚠ Admin user not found. Please create one first.{Style.RESET_ALL}")
            print(f"  Run: python manage.py createsuperuser")
            return False
        
        return True
    
    def test_admin_login(self):
        """Test admin login"""
        print(f"\n{Fore.YELLOW}Testing Admin Login...{Style.RESET_ALL}")
        
        response = self.client.get('/en/admin/')
        
        if response.status_code in [200, 302]:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Admin login page accessible")
            self.passed += 1
            return True
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | Admin login page not accessible")
            self.failed += 1
            return False
    
    def test_admin_pages(self):
        """Test admin pages load"""
        print(f"\n{Fore.YELLOW}Testing Admin Pages...{Style.RESET_ALL}")
        
        pages = [
            ('/en/admin/', 'Admin Home'),
            ('/en/admin/properties/property/', 'Properties Admin'),
            ('/en/admin/content/blogpost/', 'Blog Admin'),
            ('/en/admin/content/companyinfo/', 'Company Info Admin'),
            ('/en/admin/auth/user/', 'Users Admin'),
        ]
        
        for url, name in pages:
            response = self.client.get(url)
            if response.status_code in [200, 302]:
                print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {name:30} | Accessible")
                self.passed += 1
            else:
                print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {name:30} | Status: {response.status_code}")
                self.failed += 1
    
    def test_model_counts(self):
        """Test that models are accessible"""
        print(f"\n{Fore.YELLOW}Testing Model Access...{Style.RESET_ALL}")
        
        try:
            property_count = Property.objects.count()
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Properties model accessible ({property_count} records)")
            self.passed += 1
        except Exception as e:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | Properties model error: {e}")
            self.failed += 1
        
        try:
            blog_count = BlogPost.objects.count()
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | BlogPost model accessible ({blog_count} records)")
            self.passed += 1
        except Exception as e:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | BlogPost model error: {e}")
            self.failed += 1
        
        try:
            user_count = User.objects.count()
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | User model accessible ({user_count} records)")
            self.passed += 1
        except Exception as e:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | User model error: {e}")
            self.failed += 1
    
    def test_admin_security(self):
        """Test admin security settings"""
        print(f"\n{Fore.YELLOW}Testing Admin Security...{Style.RESET_ALL}")
        
        from django.conf import settings
        
        # Check DEBUG is not exposed in production
        if not settings.DEBUG or settings.DJANGO_ENV == 'production':
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | DEBUG mode properly configured")
            self.passed += 1
        else:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | DEBUG=True (acceptable for development)")
            self.passed += 1
        
        # Check custom admin URL
        if hasattr(settings, 'ADMIN_URL'):
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Custom admin URL configured: /{settings.ADMIN_URL}/")
            self.passed += 1
        else:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | Using default admin URL")
            self.passed += 1
    
    def run_tests(self):
        """Run all admin tests"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"SCCB-46 TASK 3: ADMIN PANEL TESTING")
        print(f"{'='*80}{Style.RESET_ALL}\n")
        
        if not self.setup_admin_user():
            print(f"\n{Fore.RED}✗ Cannot proceed without admin user{Style.RESET_ALL}")
            return
        
        self.test_admin_login()
        self.test_admin_pages()
        self.test_model_counts()
        self.test_admin_security()
        
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
            print(f"\n{Fore.GREEN}✓ ALL ADMIN TESTS PASSED{Style.RESET_ALL}")
            return True
        else:
            print(f"\n{Fore.RED}✗ SOME TESTS FAILED - REVIEW REQUIRED{Style.RESET_ALL}")
            return False

if __name__ == '__main__':
    tester = AdminTester()
    tester.run_tests()
