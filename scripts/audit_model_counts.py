import json
import os
import sys
from collections import defaultdict


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")

import django  # noqa: E402

django.setup()

from django.apps import apps  # noqa: E402
from django.db import DatabaseError  # noqa: E402


TARGET_MODELS = [
    ("content", "CompanyInfo"),
    ("content", "HeroBackgroundImage"),
    ("content", "Statistic"),
    ("content", "Service"),
    ("content", "CoreValue"),
    ("content", "CustomerReviewSection"),
    ("content", "CustomerReview"),
    ("content", "HomepageCardSection"),
    ("content", "HomepageCard"),
    ("content", "TeamMember"),
    ("content", "ExpertiseArea"),
    ("content", "BlogPost"),
    ("content", "Newsletter"),
    ("content", "ContactInquiry"),
    ("properties", "PropertyType"),
    ("properties", "Property"),
    ("properties", "PropertyPhoto"),
    ("properties", "Inquiry"),
    ("properties", "MaintenanceRequest"),
    ("properties", "SupportTicket"),
    ("properties", "ContactMessage"),
]


def get_model_count(model):
    try:
        return model.objects.count(), None
    except DatabaseError as exc:
        return None, str(exc)


def build_report():
    report = {
        "all_models": [],
        "by_app": defaultdict(list),
        "validation": [],
    }

    target_counts = {}

    for model in apps.get_models():
        count, error = get_model_count(model)
        row = {
            "app": model._meta.app_label,
            "model": model.__name__,
            "db_table": model._meta.db_table,
            "count": count,
            "status": "error" if error else ("empty" if count == 0 else "populated"),
        }
        if error:
            row["error"] = error
        report["all_models"].append(row)
        report["by_app"][model._meta.app_label].append(row)

    for app_label, model_name in TARGET_MODELS:
        model = apps.get_model(app_label, model_name)
        count, error = get_model_count(model)
        target_counts[(app_label, model_name)] = {"count": count, "error": error}

    company_info_count = target_counts[("content", "CompanyInfo")]["count"]
    hero_background_count = target_counts[("content", "HeroBackgroundImage")]["count"]
    populated_content_models = [
        key for key, value in target_counts.items()
        if key[0] == "content" and key[1] != "CompanyInfo" and (value["count"] or 0) > 0
    ]
    populated_property_models = [
        key for key, value in target_counts.items()
        if key[0] == "properties" and (value["count"] or 0) > 0
    ]

    if company_info_count == 0:
        report["validation"].append(
            {
                "level": "warning",
                "message": "CompanyInfo is empty, so homepage/company-driven fields are falling back to defaults.",
            }
        )
    else:
        report["validation"].append(
            {
                "level": "ok",
                "message": "CompanyInfo has at least one record, so homepage/company-driven fields can render from admin data.",
            }
        )

    if hero_background_count == 0:
        report["validation"].append(
            {
                "level": "warning",
                "message": "HeroBackgroundImage is empty, so the homepage will use the fallback hero image from CompanyInfo if present.",
            }
        )
    else:
        report["validation"].append(
            {
                "level": "ok",
                "message": f"HeroBackgroundImage has {hero_background_count} record(s), so homepage hero rotation is data-driven.",
            }
        )

    if populated_content_models:
        report["validation"].append(
            {
                "level": "ok",
                "message": (
                    "Other content models are populated even if CompanyInfo is empty. "
                    "That means sections like services, blog, reviews, or team can still render real data."
                ),
            }
        )

    if populated_property_models:
        report["validation"].append(
            {
                "level": "ok",
                "message": (
                    "Property-side models are populated, so homepage property cards and related admin data are not empty."
                ),
            }
        )

    report["by_app"] = dict(report["by_app"])
    return report


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2))
