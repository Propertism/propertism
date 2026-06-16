"""
Verify all seeded articles.
Run: python scratch/verify_seed.py
"""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import BlogPost

total = BlogPost.objects.count()
published = BlogPost.objects.filter(is_published=True).count()
print(f"Total BlogPosts: {total}")
print(f"Published: {published}")
print()

for bp in BlogPost.objects.filter(is_published=True).order_by("-published_date")[:20]:
    print(f"  [{bp.published_date.strftime('%Y-%m-%d')}] {bp.slug} ({bp.category})")
