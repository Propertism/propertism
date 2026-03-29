from django.core.management.base import BaseCommand
from django.db import transaction

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
from properties.models import Property, PropertyPhoto, PropertyType


class Command(BaseCommand):
    help = "Populate admin-editable content records so the site feels complete before live content is added."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite matching curated records with the bootstrap values.",
        )

    def handle(self, *args, **options):
        force = options["force"]
        with transaction.atomic():
            self.ensure_company(force=force)
            self.ensure_statistics(force=force)
            self.ensure_services(force=force)
            self.ensure_core_values(force=force)
            self.ensure_expertise_areas(force=force)
            self.ensure_customer_reviews(force=force)
            self.ensure_homepage_card_sections(force=force)
            self.ensure_team(force=force)
            self.ensure_property_types(force=force)
            self.ensure_properties(force=force)
            self.ensure_blog_posts(force=force)

        self.stdout.write(self.style.SUCCESS("Admin bootstrap content is ready."))

    def ensure_company(self, force=False):
        company = CompanyInfo.objects.first() or CompanyInfo()

        curated = {
            "company_name": "Propertism Realty Advisors LLP",
            "tagline": "We manage your property and resources when you are far from the nation.",
            "hero_eyebrow": "Propertism Realty Advisors",
            "hero_title": "NRI Property Management Services In Chennai, India",
            "hero_description": "On-ground support for NRI owners across buying, renting, reporting, and maintenance.",
            "about_mission": (
                "To protect and grow NRI property investments through reliable local execution, "
                "timely reporting, and disciplined owner support."
            ),
            "about_description": (
                "Propertism Realty Advisors LLP supports NRI owners who need dependable help in Chennai for "
                "buying, selling, rentals, maintenance, and long-distance property coordination."
            ),
            "india_office_address": "No. 30, 3rd Floor\nSSR Pankajam Towers\nArunachalam Road, Saligramam",
            "india_office_city": "Chennai",
            "india_office_state": "Tamil Nadu",
            "india_office_pincode": "600093",
            "india_phone_1": "+91 86670 20798",
            "india_phone_2": "+91 98412 01930",
            "india_phone_3": "+91 98418 44452",
            "us_office_address": "46 Berkshire Pl",
            "us_office_city": "Hackensack",
            "us_office_state": "NJ",
            "us_office_zipcode": "07601",
            "us_phone": "+1 518 409 3485",
            "email": "info@propertism.com",
            "facebook_url": "https://facebook.com/propertism",
            "twitter_url": "https://twitter.com/propertism",
            "linkedin_url": "https://linkedin.com/company/propertism",
            "business_hours": "Monday - Saturday: 9:00 AM - 6:00 PM IST",
        }

        stale_values = {
            "hero_title": {"NRI Property Management Services In India, Chennai"},
        }

        for field, value in curated.items():
            current = getattr(company, field, "")
            if force or not current or current in stale_values.get(field, set()):
                setattr(company, field, value)

        if force or not company.logo:
            company.logo = "company/propertism.png"
        if force or not company.hero_image:
            company.hero_image = "hero/propertism-hero1-bg.jpg.jpg"

        company.save()
        self.stdout.write("Ensured company information.")

    def ensure_statistics(self, force=False):
        stats = [
            {"order": 1, "value": "500+", "label": "Properties Managed"},
            {"order": 2, "value": "200+", "label": "Happy NRI Clients"},
            {"order": 3, "value": "10+", "label": "Years of Experience"},
            {"order": 4, "value": "5+", "label": "Cities Covered"},
        ]

        for item in stats:
            stat, created = Statistic.objects.get_or_create(order=item["order"], defaults=item)
            if force and not created:
                stat.value = item["value"]
                stat.label = item["label"]
                stat.is_active = True
                stat.save(update_fields=["value", "label", "is_active"])

        self.stdout.write("Ensured statistics.")

    def ensure_services(self, force=False):
        services = [
            {
                "slug": "real-estate-buy-sell",
                "order": 1,
                "title": "Real Estate Buy & Sell",
                "short_description": "Expert support for acquisition, resale, pricing, and transaction closure in Chennai.",
                "full_description": (
                    "End-to-end buying and selling support for owners and investors, including sourcing, valuation, "
                    "site visits, negotiation, documentation, and transaction coordination."
                ),
                "features": "Property sourcing\nSeller representation\nPricing support\nDeal coordination",
                "icon": "buy-sell",
            },
            {
                "slug": "rental-maintenance",
                "order": 2,
                "title": "Rental & Maintenance",
                "short_description": "Rental operations, tenant follow-through, and preventive upkeep under one team.",
                "full_description": (
                    "Professional support for tenant management, routine maintenance, vendor coordination, inspections, "
                    "and owner reporting so the property stays occupied and well-kept."
                ),
                "features": "Tenant coordination\nVendor management\nPeriodic inspections\nOwner reporting",
                "icon": "rental-maintenance",
            },
            {
                "slug": "industrial-land-services",
                "order": 3,
                "title": "Industrial Land Services",
                "short_description": "Advisory and coordination for industrial land evaluation, purchase, and development.",
                "full_description": (
                    "Specialized support for industrial land opportunities, including market assessment, site diligence, "
                    "documentation review, and coordination for acquisition decisions."
                ),
                "features": "Site assessment\nDocument review\nAcquisition support\nProject coordination",
                "icon": "industrial-land",
            },
            {
                "slug": "nri-coordination-reporting",
                "order": 4,
                "title": "NRI Coordination & Reporting",
                "short_description": "Cross-border updates and decision support for owners managing property from abroad.",
                "full_description": (
                    "A coordination layer for owners, family members, tenants, and vendors, with practical updates that "
                    "keep property decisions moving across time zones."
                ),
                "features": "India-US coordination\nDecision tracking\nStatus updates\nAction planning",
                "icon": "coordination-reporting",
            },
        ]

        for item in services:
            service, created = Service.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "order": item["order"],
                    "title": item["title"],
                    "short_description": item["short_description"],
                    "full_description": item["full_description"],
                    "features": item["features"],
                    "icon": item["icon"],
                    "is_active": True,
                },
            )
            if force and not created:
                service.order = item["order"]
                service.title = item["title"]
                service.short_description = item["short_description"]
                service.full_description = item["full_description"]
                service.features = item["features"]
                service.icon = item["icon"]
                service.is_active = True
                service.save()

        self.stdout.write("Ensured services.")

    def ensure_core_values(self, force=False):
        values = [
            {
                "order": 1,
                "title": "Transparent Reporting",
                "description": "Owners receive practical updates that show what happened, what is pending, and what needs approval.",
                "icon": "TR",
            },
            {
                "order": 2,
                "title": "Reliable Follow-through",
                "description": "Tasks do not stall because the owner is overseas. Local execution keeps work moving.",
                "icon": "RF",
            },
            {
                "order": 3,
                "title": "Disciplined Property Care",
                "description": "From tenant coordination to vendor management, the property stays monitored and maintained.",
                "icon": "PC",
            },
            {
                "order": 4,
                "title": "NRI-first Coordination",
                "description": "Family, owner, tenant, and vendor decisions are coordinated clearly across locations and time zones.",
                "icon": "NC",
            },
        ]

        for item in values:
            value, created = CoreValue.objects.get_or_create(
                order=item["order"],
                defaults={**item, "is_active": True},
            )
            if force and not created:
                value.title = item["title"]
                value.description = item["description"]
                value.icon = item["icon"]
                value.is_active = True
                value.save()

        self.stdout.write("Ensured core values.")

    def ensure_expertise_areas(self, force=False):
        areas = [
            {
                "order": 1,
                "title": "Real Estate Transactions",
                "description": "Market-aware support for buying, selling, pricing, and deal coordination in Chennai.",
            },
            {
                "order": 2,
                "title": "Rental Operations",
                "description": "Tenant onboarding, renewals, rent follow-up, and occupancy continuity for absentee owners.",
            },
            {
                "order": 3,
                "title": "Maintenance Oversight",
                "description": "Vendor coordination, preventive upkeep, and inspection-based action planning.",
            },
            {
                "order": 4,
                "title": "Owner Reporting",
                "description": "Clear updates for owners and families who need dependable visibility from abroad.",
            },
        ]

        for item in areas:
            area, created = ExpertiseArea.objects.get_or_create(
                order=item["order"],
                defaults={**item, "is_active": True},
            )
            if force and not created:
                area.title = item["title"]
                area.description = item["description"]
                area.is_active = True
                area.save()

        self.stdout.write("Ensured expertise areas.")

    def ensure_customer_reviews(self, force=False):
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
            if force or not current or current in stale_values.get(field, set()):
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
            review, created = CustomerReview.objects.get_or_create(
                section=section,
                order=item["order"],
                defaults={**item, "is_active": True},
            )
            if force and not created:
                review.customer_name = item["customer_name"]
                review.customer_location = item["customer_location"]
                review.service_label = item["service_label"]
                review.quote = item["quote"]
                review.rating = item["rating"]
                review.avatar_initials = item["avatar_initials"]
                review.is_active = True
                review.save()

        self.stdout.write("Ensured customer review section.")

    def ensure_homepage_card_sections(self, force=False):
        sections = [
            {
                "slug": "nri-ownership-support",
                "order": 1,
                "eyebrow": "Custom Section",
                "title": "Support Layers Built For NRI Owners",
                "description": (
                    "This section is fully editable from Django admin. Update the heading, copy, "
                    "and cards whenever you want to highlight a new service bundle or campaign."
                ),
                "badge_title": "Admin Managed",
                "badge_text": "Cards and copy can be edited without code changes",
                "cards": [
                    {
                        "order": 1,
                        "eyebrow": "Reporting",
                        "title": "Clear Status Updates",
                        "description": (
                            "Use this card area to highlight recurring updates, inspection notes, "
                            "or reporting promises for owners abroad."
                        ),
                        "footer": "Ideal for trust-building content",
                        "cta_text": "",
                        "cta_url": "",
                    },
                    {
                        "order": 2,
                        "eyebrow": "Execution",
                        "title": "On-Ground Coordination",
                        "description": (
                            "Promote vendor coordination, tenant support, or local follow-through "
                            "with a concise card title and supporting paragraph."
                        ),
                        "footer": "Good fit for service positioning",
                        "cta_text": "",
                        "cta_url": "",
                    },
                    {
                        "order": 3,
                        "eyebrow": "Conversion",
                        "title": "Guide Users To Action",
                        "description": (
                            "Cards can also include optional CTA text and links if you want this "
                            "section to drive users deeper into the site."
                        ),
                        "footer": "Useful for promotions and landing-page style content",
                        "cta_text": "Contact Us",
                        "cta_url": "/#contact-section",
                    },
                ],
            }
        ]

        for item in sections:
            section, created = HomepageCardSection.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "order": item["order"],
                    "eyebrow": item["eyebrow"],
                    "title": item["title"],
                    "description": item["description"],
                    "badge_title": item["badge_title"],
                    "badge_text": item["badge_text"],
                    "is_active": True,
                },
            )
            if force and not created:
                section.order = item["order"]
                section.eyebrow = item["eyebrow"]
                section.title = item["title"]
                section.description = item["description"]
                section.badge_title = item["badge_title"]
                section.badge_text = item["badge_text"]
                section.is_active = True
                section.save()

            for card_item in item["cards"]:
                card, card_created = HomepageCard.objects.get_or_create(
                    section=section,
                    order=card_item["order"],
                    defaults={**card_item, "is_active": True},
                )
                if force and not card_created:
                    card.eyebrow = card_item["eyebrow"]
                    card.title = card_item["title"]
                    card.description = card_item["description"]
                    card.footer = card_item["footer"]
                    card.cta_text = card_item["cta_text"]
                    card.cta_url = card_item["cta_url"]
                    card.is_active = True
                    card.save()

        self.stdout.write("Ensured homepage card sections.")

    def ensure_team(self, force=False):
        members = [
            {
                "order": 1,
                "name": "NRI Client Coordination Desk",
                "role": "Coordination Lead",
                "department": "Client Coordination",
                "bio": (
                    "Coordinates owner approvals, tenant conversations, family updates, and execution timelines so "
                    "property decisions do not stall across time zones."
                ),
                "expertise": "Owner reporting, Tenant coordination, Cross-border communication",
                "photo": "team/ics-11.png",
            },
            {
                "order": 2,
                "name": "Property Operations Desk",
                "role": "Operations Lead",
                "department": "Property Operations",
                "bio": (
                    "Handles inspections, vendor follow-through, maintenance planning, and day-to-day property tasks "
                    "for owners who are not physically present in Chennai."
                ),
                "expertise": "Inspections, Maintenance planning, Vendor follow-through",
                "photo": "team/ics-11.png",
            },
            {
                "order": 3,
                "name": "Advisory & Transactions Desk",
                "role": "Advisory Lead",
                "department": "Real Estate Advisory",
                "bio": (
                    "Supports buying, selling, pricing review, and transaction coordination with a practical focus on "
                    "clarity, responsiveness, and execution."
                ),
                "expertise": "Property advisory, Transaction support, Market coordination",
                "photo": "team/ics-11.png",
            },
        ]

        for item in members:
            member, created = TeamMember.objects.get_or_create(
                order=item["order"],
                defaults={**item, "is_active": True},
            )
            if force and not created:
                member.name = item["name"]
                member.role = item["role"]
                member.department = item["department"]
                member.bio = item["bio"]
                member.expertise = item["expertise"]
                member.photo = item["photo"]
                member.is_active = True
                member.save()

        self.stdout.write("Ensured team members.")

    def ensure_property_types(self, force=False):
        property_types = [
            {
                "slug": "apartment",
                "name": "Apartment",
                "description": "Urban apartments suited for owners and investors.",
                "icon": "apartment",
            },
            {
                "slug": "villa",
                "name": "Villa",
                "description": "Independent homes with stronger family-living appeal.",
                "icon": "villa",
            },
            {
                "slug": "penthouse",
                "name": "Penthouse",
                "description": "Premium residences for high-end buyers and investors.",
                "icon": "penthouse",
            },
        ]

        for item in property_types:
            property_type, created = PropertyType.objects.get_or_create(
                slug=item["slug"],
                defaults=item,
            )
            if force and not created:
                property_type.name = item["name"]
                property_type.description = item["description"]
                property_type.icon = item["icon"]
                property_type.save()

        self.stdout.write("Ensured property types.")

    def ensure_properties(self, force=False):
        property_types = {item.slug: item for item in PropertyType.objects.all()}
        properties = [
            {
                "title": "Luxury Villa in Adyar",
                "description": "A premium family villa in Adyar with clean modern interiors and strong long-term value.",
                "price": "25000000",
                "area": "3700",
                "bedrooms": 4,
                "bathrooms": 4,
                "location": "Adyar",
                "property_type": property_types["villa"],
                "photos": [
                    ("properties/luxury_villa_in_adyar_1.jpg", "Poolside view", True, 1),
                    ("properties/luxury_villa_in_adyar_2.jpg", "Living zone", False, 2),
                    ("properties/luxury_villa_in_adyar_3.jpg", "Interior detail", False, 3),
                ],
            },
            {
                "title": "Premium Apartment in Velachery",
                "description": "A well-finished premium apartment in Velachery suited for rental demand and owner use.",
                "price": "6500000",
                "area": "1200",
                "bedrooms": 2,
                "bathrooms": 2,
                "location": "Velachery",
                "property_type": property_types["apartment"],
                "photos": [
                    ("properties/premium_apartment_in_velachery_1.jpg", "Living area", True, 1),
                    ("properties/premium_apartment_in_velachery_2.jpg", "Bedroom view", False, 2),
                    ("properties/premium_apartment_in_velachery_3.jpg", "Dining detail", False, 3),
                ],
            },
            {
                "title": "Modern Apartment in OMR",
                "description": "A contemporary apartment in OMR with strong appeal for professionals and long-term renters.",
                "price": "4500000",
                "area": "1300",
                "bedrooms": 4,
                "bathrooms": 3,
                "location": "OMR",
                "property_type": property_types["apartment"],
                "photos": [
                    ("properties/modern_apartment_in_omr_1.jpg", "Living room", True, 1),
                    ("properties/modern_apartment_in_omr_2.jpg", "Interior angle", False, 2),
                    ("properties/modern_apartment_in_omr_3.jpg", "Open-plan layout", False, 3),
                ],
            },
            {
                "title": "Spacious Villa in Anna Nagar",
                "description": "A large-format villa in Anna Nagar with privacy, family scale, and strong residential positioning.",
                "price": "35000000",
                "area": "4200",
                "bedrooms": 5,
                "bathrooms": 5,
                "location": "Anna Nagar",
                "property_type": property_types["villa"],
                "photos": [
                    ("properties/spacious_villa_in_anna_nagar_1.jpg", "Exterior view", True, 1),
                    ("properties/spacious_villa_in_anna_nagar_2.jpg", "Entry zone", False, 2),
                    ("properties/spacious_villa_in_anna_nagar_3.jpg", "Interior finish", False, 3),
                ],
            },
            {
                "title": "Luxury Penthouse in Nungambakkam",
                "description": "A high-end penthouse in central Chennai positioned for premium buyers and investor interest.",
                "price": "5500000",
                "area": "2100",
                "bedrooms": 2,
                "bathrooms": 3,
                "location": "Nungambakkam",
                "property_type": property_types["penthouse"],
                "photos": [
                    ("properties/luxury_penthouse_in_nungambakkam_1.jpg", "Penthouse interior", True, 1),
                    ("properties/luxury_penthouse_in_nungambakkam_2.jpg", "Lounge view", False, 2),
                ],
            },
            {
                "title": "Affordable Apartment in Porur",
                "description": "A practical entry apartment in Porur for value-conscious investors and first-time buyers.",
                "price": "8500000",
                "area": "1100",
                "bedrooms": 3,
                "bathrooms": 2,
                "location": "Porur",
                "property_type": property_types["apartment"],
                "photos": [
                    ("properties/affordable_apartment_in_porur_1.jpg", "Apartment exterior", True, 1),
                    ("properties/affordable_apartment_in_porur_2.jpg", "Interior setup", False, 2),
                ],
            },
        ]

        for item in properties:
            property_record, created = Property.objects.get_or_create(
                title=item["title"],
                defaults={
                    "description": item["description"],
                    "price": item["price"],
                    "price_type": "sale",
                    "area": item["area"],
                    "bedrooms": item["bedrooms"],
                    "bathrooms": item["bathrooms"],
                    "location": item["location"],
                    "property_type": item["property_type"],
                    "status": "available",
                    "image": "",
                },
            )
            if force and not created:
                property_record.description = item["description"]
                property_record.price = item["price"]
                property_record.price_type = "sale"
                property_record.area = item["area"]
                property_record.bedrooms = item["bedrooms"]
                property_record.bathrooms = item["bathrooms"]
                property_record.location = item["location"]
                property_record.property_type = item["property_type"]
                property_record.status = "available"
                property_record.image = ""
                property_record.save()

            for image_path, caption, is_primary, sort_order in item["photos"]:
                photo, photo_created = PropertyPhoto.objects.get_or_create(
                    property=property_record,
                    sort_order=sort_order,
                    defaults={
                        "image": image_path,
                        "caption": caption,
                        "is_primary": is_primary,
                    },
                )
                if force and not photo_created:
                    photo.image = image_path
                    photo.caption = caption
                    photo.is_primary = is_primary
                    photo.save()

        self.stdout.write("Ensured properties and photos.")

    def ensure_blog_posts(self, force=False):
        posts = [
            {
                "slug": "nri-property-checklist-chennai",
                "title": "NRI Property Checklist for Owners in Chennai",
                "excerpt": "A practical checklist for NRI owners who need visibility, maintenance discipline, and local follow-through.",
                "content": (
                    "Strong long-distance property ownership starts with clear documentation, periodic inspection, vendor discipline, "
                    "and one accountable coordination layer for the owner and family."
                ),
                "category": "nri",
            },
            {
                "slug": "rental-readiness-for-absentee-owners",
                "title": "Rental Readiness for Absentee Owners",
                "excerpt": "How to keep a Chennai property rental-ready when the owner is overseas.",
                "content": (
                    "Rental performance improves when tenant communication, preventive maintenance, and owner approvals are structured "
                    "before issues become urgent."
                ),
                "category": "tenant",
            },
            {
                "slug": "why-reporting-matters-for-nri-property-management",
                "title": "Why Reporting Matters for NRI Property Management",
                "excerpt": "Consistent reporting is what turns property management from reactive work into decision support.",
                "content": (
                    "Owners abroad need concise updates that show status, pending items, and next actions. Good reporting reduces delay "
                    "and improves confidence in every property decision."
                ),
                "category": "maintenance",
            },
        ]

        for item in posts:
            post, created = BlogPost.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "excerpt": item["excerpt"],
                    "content": item["content"],
                    "author": "Propertism Team",
                    "category": item["category"],
                    "is_published": True,
                },
            )
            if force and not created:
                post.title = item["title"]
                post.excerpt = item["excerpt"]
                post.content = item["content"]
                post.author = "Propertism Team"
                post.category = item["category"]
                post.is_published = True
                post.save()

        self.stdout.write("Ensured blog posts.")
