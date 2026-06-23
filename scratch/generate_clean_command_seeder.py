import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import BlogPost

batches_mapping = {
    1: [
        'nri-property-management-guide-chennai',
        'nri-property-ownership-challenges-chennai',
        'nri-property-checklist-chennai-owners-abroad'
    ],
    2: [
        'nri-real-estate-investment-chennai-guide',
        'nri-property-buying-process-chennai',
        'common-mistakes-nri-property-buyers-chennai'
    ],
    3: [
        'nri-property-services-chennai-guide',
        'end-to-end-nri-property-services-chennai',
        'how-propertism-simplifies-nri-property-ownership'
    ],
    4: [
        'nri-property-tax-chennai-guide',
        'nri-property-legal-compliance-chennai',
        'nri-property-management-company-chennai'
    ]
}

def get_articles_code(slugs):
    posts = BlogPost.objects.filter(slug__in=slugs)
    # Sort them to match the exact order in mapping
    posts = sorted(posts, key=lambda p: slugs.index(p.slug))
    
    code = "[\n"
    for post in posts:
        code += "    {\n"
        code += f"        \"slug\": {json.dumps(post.slug)},\n"
        code += f"        \"title\": {json.dumps(post.title)},\n"
        code += f"        \"category\": {json.dumps(post.category)},\n"
        code += f"        \"author\": {json.dumps(post.author)},\n"
        code += f"        \"excerpt\": {json.dumps(post.excerpt)},\n"
        code += f"        \"content\": {json.dumps(post.content)},\n"
        code += "    },\n"
    code += "]"
    return code

batch_1_code = get_articles_code(batches_mapping[1])
batch_2_code = get_articles_code(batches_mapping[2])
batch_3_code = get_articles_code(batches_mapping[3])
batch_4_code = get_articles_code(batches_mapping[4])

script_content = f"""\"\"\"
Management command: seed_knowledge_hub_phase_b

Seeds Phase-B NRI Knowledge Hub articles as BlogPost records.
Supports batch-by-batch publication with evergreen SEO slugs.

Usage:
    python manage.py seed_knowledge_hub_phase_b --batch 1 --publish
    python manage.py seed_knowledge_hub_phase_b --batch 2 --publish
    python manage.py seed_knowledge_hub_phase_b --batch 3 --publish
    python manage.py seed_knowledge_hub_phase_b --batch 4 --publish
    python manage.py seed_knowledge_hub_phase_b --all --publish
\"\"\"
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from content.models import BlogPost

# =====================================================================
# CLUSTER 1: NRI Property Chennai (Articles 1-3) — BATCH 1
# =====================================================================
BATCH_1 = {batch_1_code}

# =====================================================================
# CLUSTER 2: NRI Real Estate Chennai (Articles 4-6) — BATCH 2
# =====================================================================
BATCH_2 = {batch_2_code}

# =====================================================================
# CLUSTER 3: NRI Property Services Chennai (Articles 7-9) — BATCH 3
# =====================================================================
BATCH_3 = {batch_3_code}

# =====================================================================
# CLUSTER 4: Property Advisor Chennai NRI (Articles 10-12) — BATCH 4
# =====================================================================
BATCH_4 = {batch_4_code}

class Command(BaseCommand):
    help = "Seed Phase-B Knowledge Hub articles in batches (skips existing slugs)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch",
            type=int,
            choices=[1, 2, 3, 4],
            help="Specify a batch number to seed (1-4)",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Seed all Phase-B batches",
        )
        parser.add_argument(
            "--publish",
            action="store_true",
            help="Mark seeded articles as published (default: draft)",
        )

    def handle(self, *args, **options):
        batch = options.get("batch")
        seed_all = options.get("all")
        publish = options.get("publish")

        if not batch and not seed_all:
            raise CommandError("You must specify either --batch [1-4] or --all.")

        articles_to_seed = []
        if seed_all:
            articles_to_seed = BATCH_1 + BATCH_2 + BATCH_3 + BATCH_4
        else:
            if batch == 1:
                articles_to_seed = BATCH_1
            elif batch == 2:
                articles_to_seed = BATCH_2
            elif batch == 3:
                articles_to_seed = BATCH_3
            elif batch == 4:
                articles_to_seed = BATCH_4

        created_count = skipped = 0

        for data in articles_to_seed:
            post, is_new = BlogPost.objects.get_or_create(
                slug=data["slug"],
                defaults={{
                    "title": data["title"],
                    "category": data["category"],
                    "author": data["author"],
                    "excerpt": data["excerpt"],
                    "content": data["content"],
                    "is_published": publish,
                    "published_date": timezone.now(),
                }}
            )

            if not is_new:
                if publish:
                    post.is_published = True
                    post.published_date = timezone.now()
                    post.save(update_fields=["is_published", "published_date"])
                    self.stdout.write(self.style.SUCCESS(f"  PUBLISHED (updated): {{data['slug']}}"))
                else:
                    self.stdout.write(f"  SKIP (exists): {{data['slug']}}")
                skipped += 1
            else:
                status = "PUBLISHED" if publish else "DRAFT"
                self.stdout.write(self.style.SUCCESS(f"  {{status}}: {{data['slug']}}"))
                created_count += 1

        self.stdout.write(f"\\nDone. Created: {{created_count}}  Skipped: {{skipped}}")
"""

output_path = os.path.join(os.path.dirname(__file__), '..', 'content', 'management', 'commands', 'seed_knowledge_hub_phase_b.py')
output_path = os.path.normpath(output_path)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(script_content)

print(f"Successfully generated clean command at: {output_path}")
