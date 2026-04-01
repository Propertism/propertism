"""
SCCB-46 Task 8: Security Scan
Runs Django security checks and basic security validation
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from colorama import init, Fore, Style
import io

init(autoreset=True)

class SecurityTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def test_django_check(self):
        """Run Django's built-in security check"""
        print(f"\n{Fore.YELLOW}Running Django Security Check...{Style.RESET_ALL}")
        
        try:
            # Capture output
            output = io.StringIO()
            call_command('check', '--deploy', stdout=output, stderr=output)
            result = output.getvalue()
            
            if 'System check identified no issues' in result or not result.strip():
                print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Django security check passed")
                self.passed += 1
            else:
                print(f"{Fore.YELLOW}⚠ WARNINGS{Style.RESET_ALL} | Django security check has warnings:")
                print(result)
                self.warnings += 1
        except Exception as e:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | Django security check failed: {e}")
            self.failed += 1
    
    def test_secret_key(self):
        """Check SECRET_KEY configuration"""
        print(f"\n{Fore.YELLOW}Testing SECRET_KEY...{Style.RESET_ALL}")
        
        if settings.SECRET_KEY and len(settings.SECRET_KEY) >= 50:
            if 'django-insecure' not in settings.SECRET_KEY:
                print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | SECRET_KEY properly configured")
                self.passed += 1
            else:
                print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | Using insecure SECRET_KEY (change for production)")
                self.warnings += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | SECRET_KEY too short or missing")
            self.failed += 1
    
    def test_debug_mode(self):
        """Check DEBUG setting"""
        print(f"\n{Fore.YELLOW}Testing DEBUG Mode...{Style.RESET_ALL}")
        
        if settings.DEBUG:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | DEBUG=True (must be False in production)")
            self.warnings += 1
        else:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | DEBUG=False (production ready)")
            self.passed += 1
    
    def test_allowed_hosts(self):
        """Check ALLOWED_HOSTS configuration"""
        print(f"\n{Fore.YELLOW}Testing ALLOWED_HOSTS...{Style.RESET_ALL}")
        
        if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS != ['*']:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | ALLOWED_HOSTS configured: {settings.ALLOWED_HOSTS}")
            self.passed += 1
        elif settings.ALLOWED_HOSTS == ['*']:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | ALLOWED_HOSTS=['*'] (restrict for production)")
            self.warnings += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | ALLOWED_HOSTS not configured")
            self.failed += 1
    
    def test_csrf_protection(self):
        """Check CSRF protection"""
        print(f"\n{Fore.YELLOW}Testing CSRF Protection...{Style.RESET_ALL}")
        
        if 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | CSRF middleware enabled")
            self.passed += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | CSRF middleware missing")
            self.failed += 1
        
        if hasattr(settings, 'CSRF_COOKIE_HTTPONLY') and settings.CSRF_COOKIE_HTTPONLY:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | CSRF_COOKIE_HTTPONLY enabled")
            self.passed += 1
        else:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | CSRF_COOKIE_HTTPONLY not enabled")
            self.warnings += 1
    
    def test_security_headers(self):
        """Check security headers"""
        print(f"\n{Fore.YELLOW}Testing Security Headers...{Style.RESET_ALL}")
        
        headers = [
            ('SECURE_CONTENT_TYPE_NOSNIFF', True),
            ('SECURE_BROWSER_XSS_FILTER', True),
            ('X_FRAME_OPTIONS', ['DENY', 'SAMEORIGIN']),
        ]
        
        for header, expected in headers:
            if hasattr(settings, header):
                value = getattr(settings, header)
                if isinstance(expected, list):
                    if value in expected:
                        print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {header} = {value}")
                        self.passed += 1
                    else:
                        print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | {header} = {value}")
                        self.warnings += 1
                else:
                    if value == expected:
                        print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | {header} = {value}")
                        self.passed += 1
                    else:
                        print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | {header} = {value}")
                        self.warnings += 1
            else:
                print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | {header} not configured")
                self.failed += 1
    
    def test_session_security(self):
        """Check session security"""
        print(f"\n{Fore.YELLOW}Testing Session Security...{Style.RESET_ALL}")
        
        if hasattr(settings, 'SESSION_COOKIE_HTTPONLY') and settings.SESSION_COOKIE_HTTPONLY:
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | SESSION_COOKIE_HTTPONLY enabled")
            self.passed += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | SESSION_COOKIE_HTTPONLY not enabled")
            self.failed += 1
        
        if hasattr(settings, 'SESSION_COOKIE_SAMESITE'):
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | SESSION_COOKIE_SAMESITE = {settings.SESSION_COOKIE_SAMESITE}")
            self.passed += 1
        else:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | SESSION_COOKIE_SAMESITE not configured")
            self.warnings += 1
    
    def test_password_validation(self):
        """Check password validation"""
        print(f"\n{Fore.YELLOW}Testing Password Validation...{Style.RESET_ALL}")
        
        if hasattr(settings, 'AUTH_PASSWORD_VALIDATORS') and settings.AUTH_PASSWORD_VALIDATORS:
            validator_count = len(settings.AUTH_PASSWORD_VALIDATORS)
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | Password validators configured ({validator_count} validators)")
            self.passed += 1
        else:
            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | Password validators not configured")
            self.failed += 1
    
    def test_file_upload_limits(self):
        """Check file upload limits"""
        print(f"\n{Fore.YELLOW}Testing File Upload Limits...{Style.RESET_ALL}")
        
        if hasattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE'):
            size_mb = settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)
            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | FILE_UPLOAD_MAX_MEMORY_SIZE = {size_mb:.1f} MB")
            self.passed += 1
        else:
            print(f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL} | FILE_UPLOAD_MAX_MEMORY_SIZE not configured")
            self.warnings += 1
    
    def run_tests(self):
        """Run all security tests"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"SCCB-46 TASK 8: SECURITY SCAN")
        print(f"{'='*80}{Style.RESET_ALL}\n")
        
        self.test_django_check()
        self.test_secret_key()
        self.test_debug_mode()
        self.test_allowed_hosts()
        self.test_csrf_protection()
        self.test_security_headers()
        self.test_session_security()
        self.test_password_validation()
        self.test_file_upload_limits()
        
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
        
        if self.failed == 0:
            print(f"\n{Fore.GREEN}✓ SECURITY SCAN PASSED{Style.RESET_ALL}")
            if self.warnings > 0:
                print(f"{Fore.YELLOW}⚠ Review warnings before production deployment{Style.RESET_ALL}")
            return True
        else:
            print(f"\n{Fore.RED}✗ SECURITY ISSUES FOUND - MUST FIX BEFORE DEPLOYMENT{Style.RESET_ALL}")
            return False

if __name__ == '__main__':
    tester = SecurityTester()
    tester.run_tests()
