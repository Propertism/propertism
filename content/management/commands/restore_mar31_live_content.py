from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from content.models import (
    BlogPost,
    CompanyInfo,
    CoreValue,
    CustomerReview,
    CustomerReviewSection,
    ExpertiseArea,
    HeroBackgroundImage,
    Service,
    Statistic,
    TeamMember,
)


class Command(BaseCommand):
    help = "Restore the March 31, 2026 live Propertism content snapshot into Django models."

    def handle(self, *args, **options):
        with transaction.atomic():
            company = self.restore_company()
            self.restore_hero_backgrounds(company)
            self.restore_statistics()
            self.restore_services()
            self.restore_core_values()
            self.restore_reviews()
            self.restore_team()
            self.restore_expertise_areas()
            self.restore_blog_posts()

        self.stdout.write(self.style.SUCCESS("March 31 live content snapshot restored."))

    def restore_company(self):
        company = CompanyInfo.objects.first() or CompanyInfo()

        company.company_name = "Propertism Realty Advisors LLP"
        company.tagline = "We manage your property and resources when you are far from the nation."
        company.about_mission = (
            "To assist NRI owners with dependable property coordination, reporting, and follow-through in Chennai."
        )
        company.about_description = (
            "We are a team of professionals excelled enough in various prospects, who quench our thirst with "
            "technology-driven solution. Our passion and interest in exploration and learning, lead one to the "
            "other, settling with a lightening thought to assist the Fellowship of properties."
        )

        company.hero_eyebrow = "Propertism Realty Advisors"
        company.hero_eyebrow_color = "#B89A4A"
        company.hero_title = "NRI Property Management Services In Chennai, India"
        company.hero_title_color = "#0F172A"
        company.hero_description = "We manage your property and resources, when you are far from the nation"
        company.hero_description_color = "#475569"
        company.hero_image = "hero/propertism-hero-bg.jpg"
        company.logo = "company/propertism.png"

        company.about_section_eyebrow = "About"
        company.about_section_title = "Property support for owners living abroad."
        company.about_primary_cta_text = "Meet Management"
        company.about_secondary_cta_text = "Request a callback"

        company.proof_section_eyebrow = "Why Owners Stay With Us"
        company.proof_section_title = "Clear updates, reliable follow-through, and local execution."

        company.properties_section_title = "Featured Properties for NRIs"
        company.properties_section_subtitle = "Handpicked premium properties perfect for investment"
        company.properties_section_cta_text = "Request Property Shortlist"

        company.services_section_title = "Services built for NRI ownership"
        company.services_section_description = (
            "Buy, rent, maintain, and monitor property with one coordinated team in Chennai."
        )
        company.services_card_cta_text = "Discuss this service"

        company.management_section_eyebrow = "Management"
        company.management_section_title = "One team coordinating owners, tenants, vendors, and follow-through."
        company.management_section_description = (
            "Practical accountability on the ground matters more than generic advisory. The management team is "
            "structured around execution, reporting, and decision support for owners abroad."
        )

        company.blog_section_eyebrow = "Insights"
        company.blog_section_title = "Useful updates for owners managing from abroad."
        company.blog_section_description = (
            "Short, practical guidance around reporting, rentals, maintenance, and ownership decisions in Chennai."
        )

        company.contact_section_eyebrow = "Get in Touch"
        company.contact_section_title = "Let's discuss your property needs"
        company.contact_section_description = (
            "Whether you're managing from abroad or looking to invest in Chennai, we're here to help. Share your "
            "requirements and we'll provide expert guidance."
        )
        company.contact_primary_cta_text = "Talk to Us"
        company.contact_form_submit_text = "Send My Request"

        company.footer_services_heading = "Service Coverage"
        company.footer_newsletter_heading = "Stay Updated"
        company.footer_newsletter_description = (
            "Subscribe for market insights, NRI ownership updates, and new property opportunities."
        )
        company.footer_newsletter_button_text = "Subscribe"

        company.chat_window_title = "Leave a message"
        company.chat_window_subtitle = "We'll get back to you soon"
        company.chat_submit_text = "Send"
        company.chat_sending_text = "Sending..."
        company.chat_success_title = "Message sent!"
        company.chat_success_message = "Thanks for reaching out. We'll get back to you within 24 hours."

        company.india_office_address = "No. 30, 3rd Floor\nSSR Pankajam Towers\nArunachalam Road, Saligramam"
        company.india_office_city = "Chennai"
        company.india_office_state = "Tamil Nadu"
        company.india_office_pincode = "600093"
        company.india_phone_1 = "+91 86670 20798"
        company.india_phone_2 = "+91 98412 01930"
        company.india_phone_3 = "+91 98418 44452"

        company.us_office_address = "46 Berkshire Pl"
        company.us_office_city = "Hackensack"
        company.us_office_state = "NJ"
        company.us_office_zipcode = "07601"
        company.us_phone = "+1 518 409 3485"

        company.email = "info@propertism.in"
        company.facebook_url = "https://www.facebook.com/PropertismIndia"
        company.twitter_url = "https://x.com/PropertismIndia"
        company.linkedin_url = "https://linkedin.com/company/propertism"
        company.business_hours = "Monday - Sunday: 07:00 - 23:00 IST"
        company.save()

        self.stdout.write("Restored company information.")
        return company

    def restore_hero_backgrounds(self, company):
        backgrounds = [
            (1, "hero/propertism-hero-bg.jpg"),
            (2, "hero/hero2.jpg"),
            (3, "hero/hero3.jpg"),
            (4, "hero/hero4.jpg"),
            (5, "hero/hero5.jpg"),
        ]

        active_orders = []
        for order, image_path in backgrounds:
            active_orders.append(order)
            background, _ = HeroBackgroundImage.objects.get_or_create(
                company=company,
                order=order,
                defaults={"image": image_path, "is_active": True},
            )
            background.image = image_path
            background.is_active = True
            background.save()

        HeroBackgroundImage.objects.filter(company=company).exclude(order__in=active_orders).update(is_active=False)
        self.stdout.write("Restored hero background rotation.")

    def restore_statistics(self):
        stats = [
            {"order": 1, "label": "Years of Experience", "value": "15+"},
            {"order": 2, "label": "Office Locations", "value": "2"},
            {"order": 3, "label": "Properties Managed", "value": "50+"},
            {"order": 4, "label": "Cities Covered", "value": "4"},
        ]

        active_orders = []
        for item in stats:
            active_orders.append(item["order"])
            stat, _ = Statistic.objects.get_or_create(order=item["order"])
            stat.label = item["label"]
            stat.value = item["value"]
            stat.is_active = True
            stat.save()

        Statistic.objects.exclude(order__in=active_orders).update(is_active=False)
        self.stdout.write("Restored homepage statistics.")

    def restore_services(self):
        services = [
            {
                "slug": "real-estate-buy-sell-assistance",
                "order": 1,
                "title": "Real Estate - Buy and Sell assistance",
                "short_description": (
                    "We assist in buying and selling properties, to clients who are interested in investing in a "
                    "property or who want to sell their plot at a profitable price."
                ),
                "full_description": (
                    "We assist in buying and selling properties, to clients who are interested in investing in a "
                    "property or who want to sell their plot at a profitable price. Our team provides comprehensive "
                    "support throughout the transaction process."
                ),
                "features": "Property sourcing\nPricing support\nNegotiation support\nTransaction coordination",
            },
            {
                "slug": "rental-and-apartment-maintenance",
                "order": 2,
                "title": "Rental and Apartment Maintenance",
                "short_description": (
                    "Tenant management is one of the best colored feathers in our hat, we see from the Customer's "
                    "point and give them the best services."
                ),
                "full_description": (
                    "Tenant management is one of the best colored feathers in our hat, we see from the Customer's "
                    "point and give them the best services. We take periodic visits to your place and take care of "
                    "rental cheques deposits and reports."
                ),
                "features": "Tenant management\nPeriodic visits\nDeposit follow-through\nOwner reporting",
            },
            {
                "slug": "land-plot-services",
                "order": 3,
                "title": "Land / Plot Services",
                "short_description": (
                    "Propertism also facilitates land requirements, including the sale and purchase of plots."
                ),
                "full_description": (
                    "Propertism also facilitates land requirements, including the sale and purchase of plots, with "
                    "support around location review, documentation, and buyer-seller coordination."
                ),
                "features": "Plot sourcing\nSale support\nDocument coordination\nLocation review",
            },
            {
                "slug": "industrial-land-services",
                "order": 4,
                "title": "Industrial Land Services",
                "short_description": (
                    "Advisory and coordination for industrial land evaluation, purchase, and development."
                ),
                "full_description": (
                    "Propertism also helps with industrial land requirements, including the sale and purchase of the "
                    "land required for industry plants, according to the requirement analysis."
                ),
                "features": "Requirement analysis\nSite evaluation\nPurchase support\nDevelopment coordination",
            },
        ]

        active_slugs = []
        for item in services:
            active_slugs.append(item["slug"])
            service, _ = Service.objects.get_or_create(slug=item["slug"])
            service.order = item["order"]
            service.title = item["title"]
            service.short_description = item["short_description"]
            service.full_description = item["full_description"]
            service.features = item["features"]
            service.icon = ""
            service.is_active = True
            service.save()

        Service.objects.exclude(slug__in=active_slugs).update(is_active=False)
        self.stdout.write("Restored services.")

    def restore_core_values(self):
        values = [
            {
                "order": 1,
                "title": "Trust & Transparency",
                "description": "Complete transparency in all dealings with regular updates and honest communication.",
                "icon": "TT",
            },
            {
                "order": 2,
                "title": "Professional Excellence",
                "description": "Excellence in every aspect of property management with highest standard of care.",
                "icon": "PE",
            },
            {
                "order": 3,
                "title": "Reliability",
                "description": "Consistent, dependable service with clear accountability at every step.",
                "icon": "RL",
            },
        ]

        active_orders = []
        for item in values:
            active_orders.append(item["order"])
            value, _ = CoreValue.objects.get_or_create(order=item["order"])
            value.title = item["title"]
            value.description = item["description"]
            value.icon = item["icon"]
            value.is_active = True
            value.save()

        CoreValue.objects.exclude(order__in=active_orders).update(is_active=False)
        self.stdout.write("Restored core values.")

    def restore_reviews(self):
        section = CustomerReviewSection.objects.first() or CustomerReviewSection()
        section.eyebrow = "Customer Reviews"
        section.title = "What Our Customers Say"
        section.description = "The NRIs choice for property management and resale. Trusted globally"
        section.badge_title = "Five Star Service"
        section.badge_text = "Quality Guaranteed"
        section.is_active = True
        section.save()

        reviews = [
            {
                "order": 1,
                "customer_name": "Anupama Natarajan",
                "customer_location": "New Zealand",
                "service_label": "Friendly People",
                "quote": (
                    "I am currently using the services of Propertism - NRI Property management services, and really "
                    "happy with the services provided by them. Really friendly people and provide great service for "
                    "their customers. Highly recommend using their services."
                ),
                "rating": 5,
                "avatar_initials": "A",
            },
            {
                "order": 2,
                "customer_name": "Arun Vishnu",
                "customer_location": "USA",
                "service_label": "Professional and Responsive",
                "quote": (
                    "Mr Tamilselvan is very professional and responsive. When I decided to sell my Chennai apartment, "
                    "he helped me in cleaning, painting, and putting the apartment on the market for sale. After "
                    "finding the buyer, he coordinated the entire registration process with different departments and "
                    "helped to navigate through all of them without much of my involvement. Being far away from the "
                    "property, communication is very important for me, and he was reachable and responsive through "
                    "email and mobile. The registration went smoothly with my physical presence only for a couple of "
                    "days, and I cannot imagine anybody doing better than Mr Tamilselvan."
                ),
                "rating": 5,
                "avatar_initials": "A",
            },
            {
                "order": 3,
                "customer_name": "Raja Lakshman",
                "customer_location": "Australia",
                "service_label": "Finding a suitable Buyer",
                "quote": (
                    "I am an NRI and Mr. Tamilselvan was very helpful in finding a suitable buyer for my property "
                    "inherited from my parents. He is very professional in his dealings. Helped us with all the "
                    "steps, like obtaining the encumbrance certificate, TDS by the buyer, document preparation, "
                    "registration, etc. And many things he has done behind the scenes without me knowing. Thanks a lot."
                ),
                "rating": 5,
                "avatar_initials": "R",
            },
        ]

        active_orders = []
        for item in reviews:
            active_orders.append(item["order"])
            review, _ = CustomerReview.objects.get_or_create(section=section, order=item["order"])
            review.customer_name = item["customer_name"]
            review.customer_location = item["customer_location"]
            review.service_label = item["service_label"]
            review.quote = item["quote"]
            review.rating = item["rating"]
            review.avatar_initials = item["avatar_initials"]
            review.is_active = True
            review.save()

        CustomerReview.objects.filter(section=section).exclude(order__in=active_orders).update(is_active=False)
        self.stdout.write("Restored customer reviews.")

    def restore_team(self):
        team = [
            {
                "order": 1,
                "name": "Mr. Tamilselvan",
                "role": "Managing Partner",
                "department": "Property Acquisition & Management",
                "bio": (
                    "Mr. Tamilselvan possesses rich domain knowledge with respect to land and properties. His "
                    "experience is about 15 years in this field. His fields of excellence include land acquisitions "
                    "with varied experience from top companies like Sri Kumaran Properties and Builders where he was "
                    "the managing partner. Everonn Education Limited is his next company where he worked on the same "
                    "vertical that includes property acquisition. He was the regional manager for the property "
                    "acquisition vertical at People Combine. Now, he is all set with Propertism to give his fullest "
                    "of all experience to serve clients for property management. His skills include land acquisitions, "
                    "property managements, building contract managements, property development, negotiations, etc. "
                    "which encompasses the property business coupled with management tactics. He is a MBA grad from "
                    "Symbiosis Centre of Distance Learning."
                ),
                "expertise": (
                    "Land Acquisitions, Property Management, Building Contract Management, Property Development, "
                    "Negotiations"
                ),
                "photo": "team/ics-11.png",
            },
            {
                "order": 2,
                "name": "Mr. Lawrence Manickam",
                "role": "Technology Partner",
                "department": "Technology & Innovation",
                "bio": (
                    "Propertism involves cutting-edge technologies, and Lawrence has 15 years of experience in IT "
                    "industry. Right now, he is based out of New York, who owns Tecneto - http://www.tecneto.com/ "
                    "and Realneeds - www.realneeds.org located in India and NY. He kick-started his career as a "
                    "programmer with iGateGlobalSolutions and has considerable experience in Data warehousing domain. "
                    "His skills includes much experiments with business intelligence, business objects, and a lot "
                    "more; that enhanced his skillset. He is one of the pillars of Propertism who will be supporting "
                    "on every strand with his vast knowledge. He possesses an Engineering degree from Bharathidasan "
                    "University."
                ),
                "expertise": "Business Intelligence, Data Warehousing, Technology Strategy, Software Development",
                "photo": "team/ics-11.png",
            },
            {
                "order": 3,
                "name": "Mr. Raju Packianathan",
                "role": "Co-Founder",
                "department": "Business Strategy & Entrepreneurship",
                "bio": (
                    "Raju is the first-generation entrepreneur, who is the co-founder of Quadruple Group of "
                    "Companies - www.quadruplegroup.com formed in 2008 and is one of the leading IT firms with "
                    "100+ employees. Raju has about 18 years of experience with information technology and "
                    "entrepreneurial skills. He firmly believes that everything is possible with technology and "
                    "pitches in with ideas to explore with technology alignment. His skills encircle the well-known "
                    "tactics for business strategy planning, entrepreneur skillset, and customer engagement "
                    "activities. He holds an MBA degree with marketing specialization from Madurai Kamaraj "
                    "University."
                ),
                "expertise": "Business Strategy Planning, Entrepreneurship, Customer Engagement, Technology Alignment",
                "photo": "team/ics-11.png",
            },
        ]

        active_names = []
        for item in team:
            active_names.append(item["name"])
            member, _ = TeamMember.objects.get_or_create(order=item["order"])
            member.name = item["name"]
            member.role = item["role"]
            member.department = item["department"]
            member.bio = item["bio"]
            member.expertise = item["expertise"]
            member.photo = item["photo"]
            member.is_active = True
            member.save()

        TeamMember.objects.exclude(name__in=active_names).update(is_active=False)
        self.stdout.write("Restored team members.")

    def restore_expertise_areas(self):
        areas = [
            {
                "order": 1,
                "title": "NRI Property Management",
                "description": "Specialized services for Non-Resident Indians managing properties in Chennai.",
            },
            {
                "order": 2,
                "title": "Real Estate Transactions",
                "description": "End-to-end support for buying and selling properties.",
            },
            {
                "order": 3,
                "title": "Tenant Management",
                "description": "Thorough tenant verification and ongoing relationship management.",
            },
        ]

        active_orders = []
        for item in areas:
            active_orders.append(item["order"])
            area, _ = ExpertiseArea.objects.get_or_create(order=item["order"])
            area.title = item["title"]
            area.description = item["description"]
            area.is_active = True
            area.save()

        ExpertiseArea.objects.exclude(order__in=active_orders).update(is_active=False)
        self.stdout.write("Restored expertise areas.")

    def restore_blog_posts(self):
        published_at = timezone.make_aware(datetime(2026, 3, 12, 10, 0, 0))
        posts = [
            {
                "slug": "why-reporting-matters-for-nri-property-management",
                "title": "Why Reporting Matters for NRI Property Management",
                "excerpt": "Consistent reporting is what turns property management from reactive work into decision support.",
                "content": (
                    "Owners abroad need concise updates that show status, pending items, and next actions. Good "
                    "reporting reduces delay and improves confidence in every property decision."
                ),
                "category": "maintenance",
            },
            {
                "slug": "rental-readiness-for-absentee-owners",
                "title": "Rental Readiness for Absentee Owners",
                "excerpt": "How to keep a Chennai property rental-ready when the owner is overseas.",
                "content": (
                    "Rental performance improves when tenant communication, preventive maintenance, and owner "
                    "approvals are structured before issues become urgent."
                ),
                "category": "tenant",
            },
            {
                "slug": "nri-property-checklist-chennai",
                "title": "NRI Property Checklist for Owners in Chennai",
                "excerpt": (
                    "A practical checklist for NRI owners who need visibility, maintenance discipline, and "
                    "local follow-through."
                ),
                "content": (
                    "Strong long-distance property ownership starts with clear documentation, periodic inspection, "
                    "vendor discipline, and one accountable coordination layer for the owner and family."
                ),
                "category": "nri",
            },
        ]

        active_slugs = []
        for item in posts:
            active_slugs.append(item["slug"])
            post, _ = BlogPost.objects.get_or_create(slug=item["slug"])
            post.title = item["title"]
            post.excerpt = item["excerpt"]
            post.content = item["content"]
            post.author = "Propertism Team"
            post.category = item["category"]
            post.is_published = True
            post.save()
            BlogPost.objects.filter(pk=post.pk).update(
                published_date=published_at,
                updated_date=published_at,
            )

        BlogPost.objects.exclude(slug__in=active_slugs).update(is_published=False)
        self.stdout.write("Restored blog posts.")
