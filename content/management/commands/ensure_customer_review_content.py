from django.core.management.base import BaseCommand

from content.models import CustomerReview, CustomerReviewSection


class Command(BaseCommand):
    help = "Ensure the customer review section and its seeded review cards exist."

    def handle(self, *args, **options):
        section = CustomerReviewSection.objects.first() or CustomerReviewSection()

        curated = {
            "eyebrow": "Customer Reviews",
            "title": "What Our Customers Say",
            "description": (
                "Hear from homeowners across Dubai who trust European Technical for their "
                "home maintenance needs."
            ),
            "badge_title": "Five Star Service",
            "badge_text": "Quality Guaranteed",
            "is_active": True,
        }

        stale_values = {
            "description": {
                "Hear from customers who trust us for responsive, dependable service.",
            },
        }

        for field, value in curated.items():
            current = getattr(section, field, "")
            if not current or current in stale_values.get(field, set()):
                setattr(section, field, value)

        section.save()

        reviews = [
            {
                "order": 1,
                "customer_name": "Sarah Al-Maktoum",
                "customer_location": "Dubai Marina",
                "service_label": "Air Conditioning Repair",
                "quote": (
                    "Absolutely fantastic service! The AC technician arrived on time, "
                    "diagnosed the issue in minutes, and had it fixed within the hour. "
                    "The European quality standards really show. Will definitely use again."
                ),
                "rating": 5,
                "avatar_initials": "S",
            },
            {
                "order": 2,
                "customer_name": "James Richardson",
                "customer_location": "JBR",
                "service_label": "Plumbing & Electrical",
                "quote": (
                    "I have used many handyman services in Dubai, but European Technical is "
                    "in a different league. Professional, punctual, and their work quality is "
                    "outstanding. The 30-day warranty gives extra peace of mind."
                ),
                "rating": 5,
                "avatar_initials": "J",
            },
            {
                "order": 3,
                "customer_name": "Fatima Hassan",
                "customer_location": "Downtown Dubai",
                "service_label": "Emergency Plumbing",
                "quote": (
                    "Called them for an emergency water leak at midnight. They responded "
                    "within 30 minutes and had a plumber at my door in under an hour. "
                    "Saved my apartment from serious damage. Cannot recommend enough!"
                ),
                "rating": 5,
                "avatar_initials": "F",
            },
        ]

        for item in reviews:
            CustomerReview.objects.get_or_create(
                section=section,
                order=item["order"],
                defaults={**item, "is_active": True},
            )

        self.stdout.write(self.style.SUCCESS("Customer review content is ready."))
