"""
Test static files and media configuration
SCCB-44 compliance check
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Test static files and media configuration (SCCB-44)'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*70)
        self.stdout.write("STATIC FILES & MEDIA CONFIGURATION TEST (SCCB-44)")
        self.stdout.write("="*70 + "\n")
        
        passed = []
        issues = []
        
        # Check 1: STATIC_URL
        if hasattr(settings, 'STATIC_URL') and settings.STATIC_URL:
            passed.append(f"✅ STATIC_URL: {settings.STATIC_URL}")
        else:
            issues.append("❌ STATIC_URL not configured")
        
        # Check 2: STATIC_ROOT
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            static_root = Path(settings.STATIC_ROOT)
            passed.append(f"✅ STATIC_ROOT: {static_root}")
            
            if static_root.exists():
                passed.append(f"✅ STATIC_ROOT directory exists")
            else:
                issues.append(f"⚠️  STATIC_ROOT directory doesn't exist (will be created by collectstatic)")
        else:
            issues.append("❌ STATIC_ROOT not configured")
        
        # Check 3: STATICFILES_DIRS
        if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
            passed.append(f"✅ STATICFILES_DIRS configured ({len(settings.STATICFILES_DIRS)} directories)")
            for static_dir in settings.STATICFILES_DIRS:
                if Path(static_dir).exists():
                    passed.append(f"   ✅ {static_dir} exists")
                else:
                    issues.append(f"   ❌ {static_dir} doesn't exist")
        else:
            issues.append("❌ STATICFILES_DIRS not configured")
        
        # Check 4: MEDIA_URL
        if hasattr(settings, 'MEDIA_URL') and settings.MEDIA_URL:
            passed.append(f"✅ MEDIA_URL: {settings.MEDIA_URL}")
        else:
            issues.append("❌ MEDIA_URL not configured")
        
        # Check 5: MEDIA_ROOT
        if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
            media_root = Path(settings.MEDIA_ROOT)
            passed.append(f"✅ MEDIA_ROOT: {media_root}")
            
            if media_root.exists():
                passed.append(f"✅ MEDIA_ROOT directory exists")
            else:
                issues.append(f"⚠️  MEDIA_ROOT directory doesn't exist (will be created on first upload)")
        else:
            issues.append("❌ MEDIA_ROOT not configured")
        
        # Check 6: WhiteNoise middleware
        if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
            passed.append("✅ WhiteNoise middleware configured")
        else:
            issues.append("⚠️  WhiteNoise middleware not configured")
        
        # Check 7: File upload limits
        if hasattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE'):
            size_mb = settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)
            passed.append(f"✅ FILE_UPLOAD_MAX_MEMORY_SIZE: {size_mb:.1f} MB")
        else:
            issues.append("⚠️  FILE_UPLOAD_MAX_MEMORY_SIZE not configured")
        
        if hasattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE'):
            size_mb = settings.DATA_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)
            passed.append(f"✅ DATA_UPLOAD_MAX_MEMORY_SIZE: {size_mb:.1f} MB")
        else:
            issues.append("⚠️  DATA_UPLOAD_MAX_MEMORY_SIZE not configured")
        
        # Check 8: Allowed extensions
        if hasattr(settings, 'ALLOWED_IMAGE_EXTENSIONS'):
            passed.append(f"✅ ALLOWED_IMAGE_EXTENSIONS: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}")
        else:
            issues.append("⚠️  ALLOWED_IMAGE_EXTENSIONS not configured")
        
        # Check 9: .gitignore
        gitignore_path = settings.BASE_DIR / '.gitignore'
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if '/staticfiles/' in content and '/media/' in content:
                passed.append("✅ .gitignore configured (staticfiles and media excluded)")
            else:
                issues.append("⚠️  .gitignore missing staticfiles or media exclusions")
        else:
            issues.append("⚠️  .gitignore not found")
        
        # Print results
        self.stdout.write("\nPASSED CHECKS:")
        self.stdout.write("-" * 70)
        for item in passed:
            self.stdout.write(item)
        
        if issues:
            self.stdout.write("\n\nISSUES FOUND:")
            self.stdout.write("-" * 70)
            for item in issues:
                self.stdout.write(item)
        
        # Summary
        self.stdout.write("\n" + "="*70)
        self.stdout.write("SUMMARY")
        self.stdout.write("="*70)
        self.stdout.write(f"✅ Passed: {len(passed)}")
        self.stdout.write(f"⚠️  Issues: {len(issues)}")
        
        if len(issues) == 0:
            self.stdout.write("\n✅ SCCB-44 COMPLIANCE: PASSED")
            self.stdout.write("All static files and media configurations are correct!")
        else:
            self.stdout.write("\n⚠️  SCCB-44 COMPLIANCE: REVIEW NEEDED")
            self.stdout.write("Some configurations need attention.")
        
        self.stdout.write("="*70 + "\n")
        
        # Additional instructions
        self.stdout.write("\nNEXT STEPS:")
        self.stdout.write("-" * 70)
        self.stdout.write("1. Run: python manage.py collectstatic")
        self.stdout.write("2. Test image upload in admin panel")
        self.stdout.write("3. Verify static files serve correctly")
        self.stdout.write("="*70 + "\n")
