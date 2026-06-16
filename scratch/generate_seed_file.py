"""
Script to generate the complete seed_knowledge_hub_phase_b.py file.
This avoids truncation issues by writing the file programmatically.
"""
import os

output_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'content', 'management', 'commands', 'seed_knowledge_hub_phase_b.py'))

# Read the existing file to get the first 3 articles (BATCH_1) and article 4-5 (BATCH_2)
with open(output_path, 'r') as f:
    existing = f.read()

# Find the truncation point
idx = existing.rfind('6. <strong')
if idx < 0:
    print("ERROR: Could not find truncation point")
    exit(1)

# Keep everything up to the truncation point
base = existing[:idx]

# Now append the completion of article 5, article 6, BATCH_3, BATCH_4, and the Command class
completion = """6. <strong>Not verifying encumbrance certificate:</strong> Undisclosed mortgages or liens can invalidate your purchase.

<h2>Frequently Asked Questions</h2>

<strong>Can NRIs buy agricultural land in Chennai?</strong>
No. FEMA prohibits NRIs from purchasing agricultural land, plantation property, or farmhouses in India.

<strong>How much stamp duty do NRIs pay in Tamil Nadu?</strong>
Stamp duty in Tamil Nadu is 7% of the property value for men and 5% for women. Registration fee is approximately 1%.

<strong>Can I get a home loan as an NRI for property in Chennai?</strong>
Yes. Most Indian banks offer home loans to NRIs with loan amounts up to 80% of the property value.

<strong>Do I need to be present in India to register the sale deed?</strong>
No. You can execute a registered Power of Attorney authorising a representative to register the deed on your behalf.

<strong>How long does the property purchase process take in Chennai?</strong>
Typically 4-8 weeks from agreement to registration, depending on due diligence and documentation.

For professional guidance on buying property in Chennai as an NRI, <a href="/chennai/nri-property-management/">explore our property advisory services</a> or <a href="/contact/">speak to our legal team</a>.
""",
    },
]

# =====================================================================
# CLUSTER 2: NRI Real Estate Chennai (Articles 4-6) — BATCH 2 (continued)
# Article 6: Chennai Real Estate Trends
# =====================================================================
BATCH_2.append(
    {
        "slug": "chennai-real-estate-trends-nris-2026",
        "title": "Chennai Real Estate Trends for NRIs: What to Expect",
        "category": "market",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "An analysis of Chennai real estate trends for NRI investors covering price movements, "
            "emerging corridors, infrastructure developments, rental market dynamics, and "
            "regulatory changes shaping the 2026 market."
        ),
        "content": (
            "Chennai's real estate market is evolving rapidly. For NRI investors, understanding "
            "the trends shaping the market is essential for making informed investment decisions. "
            "This analysis covers the key trends NRIs should watch in Chennai's real estate market."
        ),
    },
)

# =====================================================================
# CLUSTER 3: NRI Property Services Chennai (Articles 7-9) — BATCH 3
# Target Keyword: nri property services chennai
# =====================================================================
BATCH_3 = [
    {
        "slug": "nri-property-services-chennai-guide",
        "title": "What Property Services Do NRIs Need in Chennai?",
        "category": "nri",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "A comprehensive overview of property services NRIs need in Chennai — from property "
            "management and legal compliance to tax advisory and sale assistance."
        ),
        "content": "PLACEHOLDER",
    },
    {
        "slug": "end-to-end-nri-property-services-chennai",
        "title": "End-to-End NRI Property Services in Chennai Explained",
        "category": "nri",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "A detailed explanation of end-to-end NRI property services in Chennai covering "
            "the complete lifecycle — from purchase assistance to tax compliance and sale."
        ),
        "content": "PLACEHOLDER",
    },
    {
        "slug": "how-propertism-simplifies-nri-property-ownership",
        "title": "How Propertism Simplifies Property Ownership for NRIs",
        "category": "nri",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "Learn how Propertism's comprehensive NRI property services simplify property "
            "ownership in Chennai — from tenant management to legal compliance and tax filing."
        ),
        "content": "PLACEHOLDER",
    },
]

# =====================================================================
# CLUSTER 4: Property Advisor Chennai NRI (Articles 10-12) — BATCH 4
# Target Keyword: property advisor chennai nri
# =====================================================================
BATCH_4 = [
    {
        "slug": "why-nris-need-trusted-property-advisor-chennai",
        "title": "Why NRIs Need a Trusted Property Advisor in Chennai",
        "category": "nri",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "Why NRIs need a trusted property advisor in Chennai — from navigating complex "
            "regulations to managing properties remotely and avoiding costly mistakes."
        ),
        "content": "PLACEHOLDER",
    },
    {
        "slug": "how-to-choose-right-property-advisor-chennai",
        "title": "How to Choose the Right Property Advisor for Your Chennai Property",
        "category": "nri",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "A practical guide to choosing the right property advisor in Chennai for your NRI "
            "property needs. Covers evaluation criteria, questions to ask, and red flags."
        ),
        "content": "PLACEHOLDER",
    },
    {
        "slug": "questions-nri-ask-before-hiring-property-consultant",
        "title": "Questions Every NRI Should Ask Before Hiring a Property Consultant",
        "category": "nri",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "Essential questions NRIs should ask before hiring a property consultant in Chennai. "
            "Covers experience, fees, services, communication, and accountability."
        ),
        "content": "PLACEHOLDER",
    },
]

BATCHES = {
    1: BATCH_1,
    2: BATCH_2,
    3: BATCH_3,
    4: BATCH_4,
}

class Command(BaseCommand):
    help = "Seed Phase-B NRI Knowledge Hub articles with batch-by-batch support"

    def add_arguments(self, parser):
        parser.add_argument("--batch", type=int, choices=[1, 2, 3, 4], help="Batch number (1-4)")
        parser.add_argument("--all", action="store_true", help="Seed all batches")
        parser.add_argument("--publish", action="store_true", help="Publish articles immediately")

    def handle(self, *args, **options):
        publish = options.get("publish", False)
        batch_num = options.get("batch")
        seed_all = options.get("all", False)

        if not batch_num and not seed_all:
            self.stderr.write(self.style.ERROR("Specify --batch N or --all"))
            return

        if seed_all:
            batches_to_seed = [1, 2, 3, 4]
        else:
            batches_to_seed = [batch_num]

        total_created = 0
        for bn in batches_to_seed:
            articles = BATCHES[bn]
            for article in articles:
                slug = article["slug"]
                if BlogPost.objects.filter(slug=slug).exists():
                    self.stdout.write(f"  SKIP: {slug} (exists)")
                    continue
                BlogPost.objects.create(
                    slug=slug,
                    title=article["title"],
                    category=article["category"],
                    author=article["author"],
                    excerpt=article["excerpt"],
                    content=article["content"],
                    is_published=publish,
                    published_at=timezone.now() if publish else None,
                    created_at=timezone.now(),
                    updated_at=timezone.now(),
                )
                total_created += 1
                self.stdout.write(f"  CREATED: {slug}")

        self.stdout.write(self.style.SUCCESS(f"Done. Created {total_created} articles."))
"""

# Write the complete file
with open(output_path, 'w') as f:
    f.write(base + completion)

print(f"Written {os.path.getsize(output_path)} bytes to {output_path}")
