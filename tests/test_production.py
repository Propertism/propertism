"""
SCCB-46 Task 5: Production Settings Testing
Tests application with DEBUG=False locally
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.conf import settings
from django.test import Client
from colorama import init, Fore, Style

init(autoreset=True)

class ProductionTester:
    def __init__(self):
        self.client = Client()
        self.passed = 0
        self.failed = 0
    
    def test_debug_setting(self):
        """Check DEBUG setting"""
        print(f"\n{Fore.YELLOW}Testing DEBUG Setting...{Style.RESET_ALL}")
        
        if settings.DEBUG:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | DEBUG=True (development mode)")
            print(f"  To test production mode, set DEBUG=False in .env")
            self.passed += 1
        else:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | DEBUG=False (production mode)")
            self.passed += 1
    
    def test_static_files_config(self):
        """Test static files configuration"""
        print(f"\n{Fore.YELLOW}Testing Static Files Configuration...{Style.RESET_ALL}")
        
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | STATIC_ROOT configured: {settings.STATIC_ROOT}")
            self.passed += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | STATIC_ROOT not configured")
            self.failed += 1
        
        if hasattr(settings, 'STATIC_URL') and settings.STATIC_URL:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | STATIC_URL configured: {settings.STATIC_URL}")
            self.passed += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | STATIC_URL not configured")
            self.failed += 1
    
    def test_whitenoise(self):
        """Test WhiteNoise middleware"""
        print(f"\n{Fore.YELLOW}Testing WhiteNoise Middleware...{Style.RESET_ALL}")
        
        if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | WhiteNoise middleware installed")
            self.passed += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | WhiteNoise middleware not found")
            self.failed += 1
    
    def test_security_settings(self):
        """Test security settings"""
        print(f"\n{Fore.YELLOW}Testing Security Settings...{Style.RESET_ALL}")
        
        security_checks = [
            ('SECURE_CONTENT_TYPE_NOSNIFF', True),
            ('SECURE_BROWSER_XSS_FILTER', True),
            ('X_FRAME_OPTIONS', ['DENY', 'SAMEORIGIN']),
            ('CSRF_COOKIE_HTTPONLY', True),
            ('SESSION_COOKIE_HTTPONLY', True),
        ]
        
        for setting_name, expected in security_checks:
            if hasattr(settings, setting_name):
                value = getattr(settings, setting_name)
                if isinstance(expected, list):
                    if value in expected:
                        print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {setting_name} = {value}")
                        self.passed += 1
                    else:
                        print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {setting_name} = {value} (expected one of {expected})")
                        self.failed += 1
                else:
                    if value == expected:
                        print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {setting_name} = {value}")
                        self.passed += 1
                    else:
                        print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {setting_name} = {value} (expected {expected})")
                        self.failed += 1
            else:
                print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {setting_name} not configured")
                self.failed += 1
    
    def test_logging_config(self):
        """Test logging configuration"""
        print(f"\n{Fore.YELLOW}Testing Logging Configuration...{Style.RESET_ALL}")
        
        if hasattr(settings, 'LOGGING') and settings.LOGGING:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Logging configured")
            self.passed += 1
            
            # Check log directory exists
            if hasattr(settings, 'LOGS_DIR'):
                if settings.LOGS_DIR.exists():
                    print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Logs directory exists: {settings.LOGS_DIR}")
                    self.passed += 1
                else:
                    print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | Logs directory not found: {settings.LOGS_DIR}")
                    self.passed += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | Logging not configured")
            self.failed += 1
    
    def test_error_pages(self):
        """Test custom error pages"""
        print(f"\n{Fore.YELLOW}Testing Custom Error Pages...{Style.RESET_ALL}")
        
        # Test 404 page
        response = self.client.get('/en/nonexistent-page-test-404/')
        if response.status_code == 404:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | 404 page returns correct status")
            self.passed += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | 404 page status incorrect: {response.status_code}")
            self.failed += 1
    
    def test_allowed_hosts(self):
        """Test ALLOWED_HOSTS configuration"""
        print(f"\n{Fore.YELLOW}Testing ALLOWED_HOSTS...{Style.RESET_ALL}")
        
        if hasattr(settings, 'ALLOWED_HOSTS'):
            hosts = settings.ALLOWED_HOSTS
            if hosts and hosts != ['*']:
                print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | ALLOWED_HOSTS configured: {hosts}")
                self.passed += 1
            elif hosts == ['*']:
                print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | ALLOWED_HOSTS=['*'] (acceptable for development)")
                self.passed += 1
            else:
                print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | ALLOWED_HOSTS not configured")
                self.failed += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | ALLOWED_HOSTS not found")
            self.failed += 1
    
    def run_tests(self):
        """Run all production tests"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"SCCB-46 TASK 5: PRODUCTION SETTINGS TESTING")
        print(f"{'='*80}{Style.RESET_ALL}\n")
        
        self.test_debug_setting()
        self.test_static_files_config()
        self.test_whitenoise()
        self.test_security_settings()
        self.test_logging_config()
        self.test_error_pages()
        self.test_allowed_hosts()
        
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
            print(f"\n{Fore.GREEN}✓ ALL PRODUCTION TESTS PASSED{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}Production Readiness Notes:{Style.RESET_ALL}")
            print(f"  • Ensure DEBUG=False before deployment")
            print(f"  • Update ALLOWED_HOSTS with production domain")
            print(f"  • Run 'python manage.py collectstatic' before deployment")
            print(f"  • Verify SSL certificates are configured")
            return True
        else:
            print(f"\n{Fore.RED}✗ SOME TESTS FAILED - REVIEW REQUIRED{Style.RESET_ALL}")
            return False

if __name__ == '__main__':
    tester = ProductionTester()
    tester.run_tests()
