"""
Create a demo CMS page to show Django CMS functionality
Run with: python manage.py shell < create_cms_demo_page.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from cms.api import create_page, add_plugin
from cms.models import Page

def create_demo_page():
    """Create a demo CMS page"""
    
    # Check if demo page already exists
    if Page.objects.filter(pagecontent_set__title='CMS Demo').exists():
        print("ℹ️  CMS Demo page already exists")
        page = Page.objects.filter(pagecontent_set__title='CMS Demo').first()
    else:
        # Create a new CMS page
        page = create_page(
            title='CMS Demo',
            template='cms_demo.html',
            language='en',
            slug='cms-demo',
        )
        page.publish('en')
        print("✅ CMS Demo page created")
    
    print(f"\n🎯 Visit: http://localhost:8000/en/cms-demo/?edit")
    print("   Click 'Edit' in the toolbar to start editing!\n")
    
    return page

if __name__ == '__main__':
    create_demo_page()
