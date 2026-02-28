#!/usr/bin/env python
"""
Security Configuration Checker for Propertism
Validates security settings before deployment
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.conf import settings

def check_security():
    """Run security checks and report issues"""
    issues = []
    warnings = []
    passed = []
    
    print("\n" + "="*70)
    print("PROPERTISM SECURITY CONFIGURATION CHECK")
    print("="*70 + "\n")
    
    # Check 1: SECRET_KEY
    if settings.SECRET_KEY == 'django-insecure-realtor-project-secret-key-change-in-production':
        issues.append("❌ CRITICAL: Using default SECRET_KEY! Generate a new one.")
    elif 'insecure' in settings.SECRET_KEY.lower():
        issues.append("❌ CRITICAL: SECRET_KEY contains 'insecure'. Generate a new one.")
    else:
        passed.append("✅ SECRET_KEY is configured")
    
    # Check 2: DEBUG
    if settings.DEBUG:
        warnings.append("⚠️  WARNING: DEBUG is True (OK for development, MUST be False for production)")
    else:
        passed.append("✅ DEBUG is False")
    
    # Check 3: ALLOWED_HOSTS
    if '*' in settings.ALLOWED_HOSTS and not settings.DEBUG:
        issues.append("❌ CRITICAL: ALLOWED_HOSTS contains '*' in production mode")
    elif '*' in settings.ALLOWED_HOSTS:
        warnings.append("⚠️  WARNING: ALLOWED_HOSTS contains '*' (OK for development)")
    else:
        passed.append(f"✅ ALLOWED_HOSTS configured: {', '.join(settings.ALLOWED_HOSTS)}")
    
    # Check 4: Database
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3' and not settings.DEBUG:
        issues.append("❌ CRITICAL: Using SQLite in production (use PostgreSQL)")
    elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        warnings.append("⚠️  WARNING: Using SQLite (OK for development, use PostgreSQL for production)")
    else:
        passed.append("✅ Using PostgreSQL database")
    
    # Check 5: HTTPS Settings
    if hasattr(settings, 'SECURE_SSL_REDIRECT'):
        if settings.SECURE_SSL_REDIRECT:
            passed.append("✅ HTTPS redirect enabled")
        else:
            warnings.append("⚠️  WARNING: HTTPS redirect disabled (enable for production)")
    
    # Check 6: Security Headers
    if settings.SECURE_CONTENT_TYPE_NOSNIFF:
        passed.append("✅ Content type nosniff enabled")
    
    if settings.X_FRAME_OPTIONS in ['DENY', 'SAMEORIGIN']:
        passed.append(f"✅ X-Frame-Options set to {settings.X_FRAME_OPTIONS}")
    
    # Check 7: Session Security
    if hasattr(settings, 'SESSION_COOKIE_SECURE'):
        if settings.SESSION_COOKIE_SECURE:
            passed.append("✅ Secure session cookies enabled")
        elif not settings.DEBUG:
            issues.append("❌ CRITICAL: SESSION_COOKIE_SECURE is False in production")
    
    if settings.SESSION_COOKIE_HTTPONLY:
        passed.append("✅ HTTPOnly session cookies enabled")
    
    # Check 8: CSRF Protection
    if hasattr(settings, 'CSRF_COOKIE_SECURE'):
        if settings.CSRF_COOKIE_SECURE:
            passed.append("✅ Secure CSRF cookies enabled")
        elif not settings.DEBUG:
            issues.append("❌ CRITICAL: CSRF_COOKIE_SECURE is False in production")
    
    if settings.CSRF_COOKIE_HTTPONLY:
        passed.append("✅ HTTPOnly CSRF cookies enabled")
    
    # Check 9: Admin URL
    admin_url = getattr(settings, 'ADMIN_URL', 'admin')
    if admin_url == 'admin':
        warnings.append("⚠️  WARNING: Using default admin URL '/admin/' (consider changing)")
    else:
        passed.append(f"✅ Custom admin URL configured: /{admin_url}/")
    
    # Check 10: File Upload Limits
    if hasattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE'):
        max_size_mb = settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)
        passed.append(f"✅ File upload limit: {max_size_mb:.1f} MB")
    
    # Print Results
    print("PASSED CHECKS:")
    print("-" * 70)
    for item in passed:
        print(item)
    
    if warnings:
        print("\n\nWARNINGS:")
        print("-" * 70)
        for item in warnings:
            print(item)
    
    if issues:
        print("\n\n🚨 CRITICAL ISSUES:")
        print("-" * 70)
        for item in issues:
            print(item)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✅ Passed: {len(passed)}")
    print(f"⚠️  Warnings: {len(warnings)}")
    print(f"❌ Critical Issues: {len(issues)}")
    
    if issues:
        print("\n🚨 PRODUCTION READINESS: NOT READY")
        print("Fix all critical issues before deploying to production!")
    elif warnings and not settings.DEBUG:
        print("\n⚠️  PRODUCTION READINESS: REVIEW WARNINGS")
        print("Review warnings before deploying to production.")
    else:
        print("\n✅ PRODUCTION READINESS: GOOD")
        if settings.DEBUG:
            print("(Running in development mode)")
    
    print("="*70 + "\n")
    
    return len(issues) == 0

if __name__ == '__main__':
    try:
        success = check_security()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error running security check: {e}\n")
        sys.exit(1)
