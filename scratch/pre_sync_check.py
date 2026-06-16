"""
Pre-Sync Validation: Check production BlogPost inventory
"""
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
sys.path.insert(0, '/var/app/current')
import django
django.setup()
from content.models import BlogPost

published = BlogPost.objects.filter(is_published=True)
print(f"Published Count: {published.count()}")
for slug in published.values_list('slug', flat=True):
    print(slug)
