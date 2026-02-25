"""
SCCB-46: Master Test Runner
Runs all testing suites and generates comprehensive report
"""
import os
import sys
import subprocess
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

def run_test_script(script_name, description):
    """Run a test script and return success status"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"Running: {description}")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    try:
        # Get the directory where this script is located (tests folder)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, script_name)
        
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=script_dir,
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"{Fore.RED}✗ Error running {script_name}: {e}{Style.RESET_ALL}")
        return False

def main():
    """Run all test suites"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"SCCB-46: COMPREHENSIVE TESTING & QA PROTOCOL")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    tests = [
        ('test_pages.py', 'Task 1: Page Load Testing'),
        ('test_forms.py', 'Task 2: Form Submission Testing'),
        ('test_admin.py', 'Task 3: Admin Panel Testing'),
        ('test_mobile.py', 'Task 4: Mobile Responsiveness'),
        ('test_production.py', 'Task 5: Production Settings'),
        ('test_html_validation.py', 'Task 6: HTML Validation'),
        ('test_security.py', 'Task 8: Security Scan'),
    ]
    
    results = {}
    
    for script, description in tests:
        success = run_test_script(script, description)
        results[description] = success
    
    # Print final summary
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"FINAL TEST SUMMARY")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed
    
    for test, success in results.items():
        status = f"{Fore.GREEN}✓ PASS{Style.RESET_ALL}" if success else f"{Fore.RED}✗ FAIL{Style.RESET_ALL}"
        print(f"{status} | {test}")
    
    print(f"\n{Fore.CYAN}Overall Results:{Style.RESET_ALL}")
    print(f"  Passed: {Fore.GREEN}{passed}/{len(results)}{Style.RESET_ALL}")
    print(f"  Failed: {Fore.RED}{failed}/{len(results)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Manual Testing Required:{Style.RESET_ALL}")
    print(f"  □ Task 7: Browser Compatibility (Chrome, Safari, Firefox, Edge)")
    print(f"  □ Task 9: Performance Testing (Lighthouse/PageSpeed)")
    print(f"  □ Task 10: Unit Tests (python manage.py test)")
    
    if failed == 0:
        print(f"\n{Fore.GREEN}✓ ALL AUTOMATED TESTS PASSED{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Complete manual tests before deployment{Style.RESET_ALL}")
        return 0
    else:
        print(f"\n{Fore.RED}✗ SOME TESTS FAILED - REVIEW REQUIRED{Style.RESET_ALL}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
