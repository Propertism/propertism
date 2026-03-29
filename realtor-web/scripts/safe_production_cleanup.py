import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")
os.environ.setdefault("DB_PATH", "/var/app/data/db.sqlite3")

import django

django.setup()

from content.models import HomepageCard, HomepageCardSection, Service


def deactivate_services():
    slugs = [
        "real-estate-buy-sell",
        "rental-maintenance",
        "nri-coordination-reporting",
    ]

    services = list(Service.objects.filter(slug__in=slugs, is_active=True))
    for service in services:
        service.is_active = False
        service.save(update_fields=["is_active"])

    return [(service.slug, service.title) for service in services]


def deactivate_homepage_cards():
    sections = list(
        HomepageCardSection.objects.filter(slug="nri-ownership-support", is_active=True)
    )
    cards = list(
        HomepageCard.objects.filter(section__slug="nri-ownership-support", is_active=True)
    )

    for section in sections:
        section.is_active = False
        section.save(update_fields=["is_active"])

    for card in cards:
        card.is_active = False
        card.save(update_fields=["is_active"])

    return {
        "sections": [(section.slug, section.title) for section in sections],
        "cards": [(card.section.slug, card.title) for card in cards],
    }


service_results = deactivate_services()
card_results = deactivate_homepage_cards()

print("Deactivated services:")
for slug, title in service_results:
    print(f"- {slug}: {title}")

print("Deactivated homepage card sections:")
for slug, title in card_results["sections"]:
    print(f"- {slug}: {title}")

print("Deactivated homepage cards:")
for slug, title in card_results["cards"]:
    print(f"- {slug}: {title}")
