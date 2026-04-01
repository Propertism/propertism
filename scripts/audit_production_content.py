import json
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")
os.environ.setdefault("DB_PATH", "/var/app/data/db.sqlite3")

import django

django.setup()

from content.models import (
    BlogPost,
    CompanyInfo,
    CoreValue,
    CustomerReview,
    CustomerReviewSection,
    ExpertiseArea,
    HomepageCard,
    HomepageCardSection,
    Service,
    Statistic,
    TeamMember,
)
from properties.models import Property, PropertyType


def tuples(queryset):
    return [list(item) for item in queryset]


company = CompanyInfo.objects.first()

payload = {
    "company": {
        "hero_title": getattr(company, "hero_title", None),
        "hero_description": getattr(company, "hero_description", None),
        "about_description": getattr(company, "about_description", None),
        "email": getattr(company, "email", None),
    },
    "statistics": tuples(
        Statistic.objects.order_by("order").values_list("order", "value", "label")
    ),
    "services": tuples(
        Service.objects.order_by("order", "title").values_list("order", "slug", "title")
    ),
    "core_values": tuples(
        CoreValue.objects.order_by("order", "title").values_list("order", "title")
    ),
    "expertise_areas": tuples(
        ExpertiseArea.objects.order_by("order", "title").values_list("order", "title")
    ),
    "team_members": tuples(
        TeamMember.objects.order_by("order", "name").values_list("order", "name", "role")
    ),
    "blog_posts": tuples(
        BlogPost.objects.order_by("slug").values_list("slug", "title")
    ),
    "review_sections": tuples(
        CustomerReviewSection.objects.values_list("eyebrow", "title", "description")
    ),
    "reviews": tuples(
        CustomerReview.objects.order_by("order").values_list(
            "order", "customer_name", "service_label"
        )
    ),
    "homepage_card_sections": tuples(
        HomepageCardSection.objects.order_by("order", "slug").values_list(
            "order", "slug", "title"
        )
    ),
    "homepage_cards": tuples(
        HomepageCard.objects.order_by("section__order", "order").values_list(
            "section__slug", "order", "title"
        )
    ),
    "property_types": tuples(
        PropertyType.objects.order_by("slug").values_list("slug", "name")
    ),
    "properties": tuples(
        Property.objects.order_by("title").values_list("title", "location")
    ),
}

print(json.dumps(payload, indent=2, ensure_ascii=True))
