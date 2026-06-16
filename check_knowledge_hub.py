#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import BlogPost

articles = [
    'nri-property-management-chennai-complete-guide',
    'how-nris-can-sell-property-in-india-from-abroad',
    'power-of-attorney-for-nris-complete-guide',
    'how-to-verify-property-documents-chennai',
    'patta-transfer-process-explained',
    'encumbrance-certificate-guide-for-nris',
    'property-tax-guide-chennai-nris',
    'capital-gains-tax-property-sale-nris',
    'tenant-management-guide-overseas-property-owners',
    'nri-property-maintenance-checklist'
]

print("\n" + "=" * 70)
print("KNOWLEDGE HUB PHASE-A ARTICLE STATUS CHECK")
print("=" * 70)

published_count = 0
draft_count = 0
missing_count = 0

for i, slug in enumerate(articles, 1):
    post = BlogPost.objects.filter(slug=slug).first()
    if post:
        status = "PUBLISHED" if post.is_published else "DRAFT"
        pub_date = post.published_date.strftime("%Y-%m-%d %H:%M")
        if post.is_published:
            published_count += 1
            print(f"{i:2}. [PUBLISHED] {slug}")
            print(f"    Date: {pub_date}")
        else:
            draft_count += 1
            print(f"{i:2}. [DRAFT] {slug}")
    else:
        missing_count += 1
        print(f"{i:2}. [MISSING] {slug}")

print("=" * 70)
print(f"Summary: Published={published_count}, Draft={draft_count}, Missing={missing_count}")
print("=" * 70)

if missing_count > 0:
    print("\nACTION REQUIRED: Run `python manage.py seed_knowledge_hub_phase_a --publish`")
elif draft_count > 0:
    print("\nACTION REQUIRED: Run `python manage.py seed_knowledge_hub_phase_a --publish`")
else:
    print("\nSTATUS: All 10 articles are published and ready for indexing.")
print()
