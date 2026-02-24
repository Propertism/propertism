import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.views import get_company_context

context = get_company_context()
company = context.get('company')

print("=== CONTEXT TEST ===")
print(f"Company object: {company}")
if company:
    print(f"Hero image field: {company.hero_image}")
    print(f"Hero image bool: {bool(company.hero_image)}")
    if company.hero_image:
        print(f"Hero image URL: {company.hero_image.url}")
    else:
        print("❌ Hero image is empty/None")
else:
    print("❌ No company in context")
