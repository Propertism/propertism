import os
import django
import json
from django.core.serializers.json import DjangoJSONEncoder

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import BlogPost

# Slugs of the 12 Phase B articles
phase_b_slugs = [
    'nri-property-management-guide-chennai',
    'nri-property-ownership-challenges-chennai',
    'nri-property-checklist-chennai-owners-abroad',
    'nri-real-estate-investment-chennai-guide',
    'nri-property-buying-process-chennai',
    'common-mistakes-nri-property-buyers-chennai',
    'nri-property-services-chennai-guide',
    'end-to-end-nri-property-services-chennai',
    'how-propertism-simplifies-nri-property-ownership',
    'nri-property-tax-chennai-guide',
    'nri-property-legal-compliance-chennai',
    'nri-property-management-company-chennai'
]

posts = BlogPost.objects.filter(slug__in=phase_b_slugs)
data_list = []
for post in posts:
    data_list.append({
        'title': post.title,
        'slug': post.slug,
        'excerpt': post.excerpt,
        'content': post.content,
        'author': post.author,
        'is_published': post.is_published,
        'category': post.category,
        'published_date': post.published_date.isoformat() if post.published_date else None
    })

# Format as python code embedding
serialized_data = json.dumps(data_list, indent=4, cls=DjangoJSONEncoder)

script_content = f"""# Self-contained import script for Phase B blog posts
import os
import django
import json
from django.utils.dateparse import parse_datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import BlogPost

JSON_DATA = '''{serialized_data}'''
DATA = json.loads(JSON_DATA)

created_count = 0
skipped_count = 0

for item in DATA:
    slug = item['slug']
    exists = BlogPost.objects.filter(slug=slug).exists()
    if exists:
        print(f"Skipping existing article: {{slug}}")
        skipped_count += 1
    else:
        print(f"Creating article: {{slug}}")
        pub_date = parse_datetime(item['published_date']) if item['published_date'] else None
        BlogPost.objects.create(
            title=item['title'],
            slug=item['slug'],
            excerpt=item['excerpt'],
            content=item['content'],
            author=item['author'],
            is_published=item['is_published'],
            category=item['category'],
            published_date=pub_date
        )
        created_count += 1

print("========================================")
print(f"Safe Import Summary:")
print(f"Created: {{created_count}}")
print(f"Skipped: {{skipped_count}}")
print("========================================")
"""

output_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'safe_import_phase_b.py')
output_path = os.path.normpath(output_path)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(script_content)

print(f"Generated safe import script at: {output_path}")
