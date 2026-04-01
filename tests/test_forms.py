"""
SCCB-46 Task 2: Form Submission Testing
Tests all forms submit properly with validation
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.test import Client
from content.models import ContactInquiry, Newsletter
from colorama import init, Fore, Style

init(autoreset=True)

class FormTester:
    def __init__(self):
        self.client = Client()
        self.passed = 0
        self.failed = 0
    
    def test_contact_form_valid(self):
        """Test contact form with valid data"""
        print(f"\n{Fore.YELLOW}Testing Contact Form (Valid Data)...{Style.RESET_ALL}")
        
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'service': 'buy',
            'property_type': 'residential',
            'message': 'I am interested in buying a property.'
        }
        
        initial_count = ContactInquiry.objects.count()
        response = self.client.post('/en/contact/', data, follow=True)
        final_count = ContactInquiry.objects.count()
        
        if final_count > initial_count and response.status_code == 200:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Contact form submission successful")
            self.passed += 1
            return True
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | Contact form submission failed")
            self.failed += 1
            return False
    
    def test_contact_form_invalid(self):
        """Test contact form with invalid data"""
        print(f"\n{Fore.YELLOW}Testing Contact Form (Invalid Data)...{Style.RESET_ALL}")
        
        # Missing required fields
        data = {
            'name': '',
            'email': 'invalid-email',
            'message': ''
        }
        
        initial_count = ContactInquiry.objects.count()
        response = self.client.post('/en/contact/', data)
        final_count = ContactInquiry.objects.count()
        
        # Should not create inquiry with invalid data
        if final_count == initial_count:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Validation correctly rejected invalid data")
            self.passed += 1
            return True
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | Validation failed to reject invalid data")
            self.failed += 1
            return False
    
    def test_newsletter_subscription(self):
        """Test newsletter subscription"""
        print(f"\n{Fore.YELLOW}Testing Newsletter Subscription...{Style.RESET_ALL}")
        
        test_email = 'newsletter@example.com'
        
        # Clean up if exists
        Newsletter.objects.filter(email=test_email).delete()
        
        data = {'email': test_email}
        response = self.client.post('/en/newsletter/subscribe/', data, follow=True)
        
        if Newsletter.objects.filter(email=test_email).exists():
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Newsletter subscription successful")
            self.passed += 1
            
            # Clean up
            Newsletter.objects.filter(email=test_email).delete()
            return True
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | Newsletter subscription failed")
            self.failed += 1
            return False
    
    def test_admin_login(self):
        """Test admin login form"""
        print(f"\n{Fore.YELLOW}Testing Admin Login...{Style.RESET_ALL}")
        
        # Test admin login page loads
        response = self.client.get('/en/admin/')
        
        if response.status_code in [200, 302]:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Admin login page accessible")
            self.passed += 1
            return True
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | Admin login page not accessible")
            self.failed += 1
            return False
    
    def run_tests(self):
        """Run all form tests"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"SCCB-46 TASK 2: FORM SUBMISSION TESTING")
        print(f"{'='*80}{Style.RESET_ALL}\n")
        
        self.test_contact_form_valid()
        self.test_contact_form_invalid()
        self.test_newsletter_subscription()
        self.test_admin_login()
        
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
            print(f"\n{Fore.GREEN}✓ ALL FORM TESTS PASSED{Style.RESET_ALL}")
            return True
        else:
            print(f"\n{Fore.RED}✗ SOME TESTS FAILED - REVIEW REQUIRED{Style.RESET_ALL}")
            return False

if __name__ == '__main__':
    tester = FormTester()
    tester.run_tests()
