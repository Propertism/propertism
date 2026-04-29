from django.db import transaction

def run():
    with transaction.atomic():
        update_company_info()
        update_homepage_cards()
        update_services()
        update_statistics()
        update_reviews_section()
        update_expertise()
    print("Audit injection completed.")

def update_company_info():
    from content.models import CompanyInfo

    obj = CompanyInfo.objects.first()
    if not obj:
        print("No CompanyInfo found.")
        return

    obj.tagline = "We manage, protect & grow your Chennai property — even if you’re 10,000 km away."
    obj.hero_description = "End-to-end property management for NRIs with complete transparency, reporting, and on-ground execution."
    
    # SCCB-019 Point 6: Conversion-driven contact copy
    obj.contact_section_title = "Let’s manage your Chennai property — stress-free."
    obj.contact_section_description = "End-to-end support for NRIs. Transparent, reliable, on-ground execution."
    
    obj.save()
    print("Company Info updated with SCCB-019 copy.")

def update_homepage_cards():
    from content.models import HomepageCard

    cards = HomepageCard.objects.all().order_by("id")
    if not cards.exists():
        print("No HomepageCard found.")
        return

    mapping = [
        ("Trusted by NRIs Worldwide",
         "Serving property owners across US, UK, UAE and beyond with reliable on-ground execution."),

        ("End-to-End Management",
         "From tenant handling to maintenance and reporting — everything handled seamlessly."),

        ("Transparent Reporting",
         "Stay updated with regular reports, inspections, and real-time communication.")
    ]

    for card, data in zip(cards, mapping):
        card.title = data[0]
        card.description = data[1]
        card.save()
    print(f"{len(mapping)} Homepage cards updated.")

def update_services():
    from content.models import Service

    services = Service.objects.all().order_by("id")
    if not services.exists():
        print("No Service found.")
        return

    mapping = [
        ("Complete NRI Property Care",
         "End-to-end property management including tenant handling, maintenance, inspections, and monthly reporting."),

        ("Rental Income Management",
         "Maximize your rental returns with tenant sourcing, rent optimization, and seamless collection."),

        ("Property Sale & Exit Service",
         "End-to-end support for selling your property including valuation, listing, negotiation, and legal coordination.")
    ]

    for service, data in zip(services, mapping):
        service.title = data[0]
        service.short_description = data[1]

        # If CTA field exists
        if hasattr(service, "cta_text"):
            service.cta_text = "Discuss This Plan"

        service.save()
    print(f"{len(mapping)} Services updated.")

def update_statistics():
    from content.models import Statistic

    stats = Statistic.objects.all().order_by("id")
    if not stats.exists():
        print("No Statistic found.")
        return

    mapping = [
        ("10+", "Years Experience"),
        ("100+", "NRI Clients"),
        ("500+", "Properties Managed")
    ]

    for stat, data in zip(stats, mapping):
        stat.value = data[0]
        stat.label = data[1]
        stat.save()
    print(f"{len(mapping)} Statistics updated.")

def update_reviews_section():
    from content.models import CustomerReviewSection

    obj = CustomerReviewSection.objects.first()
    if not obj:
        print("No CustomerReviewSection found.")
        return

    if hasattr(obj, "title"):
        obj.title = "Trusted by NRI Property Owners Worldwide"

    if hasattr(obj, "description"):
        obj.description = "Real experiences from clients who trust us to manage their properties from across the globe."

    obj.save()
    print("Reviews Section updated.")

def update_expertise():
    from content.models import ExpertiseArea

    areas = ExpertiseArea.objects.all().order_by("id")
    if not areas.exists():
        print("No ExpertiseArea found.")
        return

    mapping = [
        ("NRI Property Management",
         "Specialized services for overseas property owners with complete remote handling."),

        ("Rental & Tenant Management",
         "Efficient tenant sourcing, rent collection, and issue resolution."),

        ("Property Sale Advisory",
         "Strategic support for selling properties with maximum value and minimal hassle.")
    ]

    for area, data in zip(areas, mapping):
        area.title = data[0]
        area.description = data[1]
        area.save()
    print(f"{len(mapping)} Expertise areas updated.")

if __name__ == "__main__":
    run()
