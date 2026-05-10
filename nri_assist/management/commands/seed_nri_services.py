from django.core.management.base import BaseCommand
from nri_assist.models import NRIService

SEED_DATA = [
    # Property Care
    ('Scheduled property inspections', 'PROPERTY_CARE', 'Regular inspections of your property with detailed reports and photos.', 0),
    ('Photo and video updates', 'PROPERTY_CARE', 'Visual documentation of property condition shared directly with you.', 1),
    ('Utility coordination', 'PROPERTY_CARE', 'Managing electricity, water, and maintenance utilities on your behalf.', 2),
    ('Tenant coordination', 'PROPERTY_CARE', 'Handling tenant communications, requests, and issue resolution.', 3),
    ('Vacant property monitoring', 'PROPERTY_CARE', 'Security monitoring and upkeep for unoccupied properties.', 4),
    # Sale Assistance
    ('Listing optimisation', 'SALE', 'Professional listing preparation and pricing strategy to attract serious buyers.', 0),
    ('Buyer filtering', 'SALE', 'Qualifying buyer interest and shortlisting serious enquiries.', 1),
    ('Site visit coordination', 'SALE', 'Arranging and overseeing property viewings on your behalf.', 2),
    ('Offer coordination', 'SALE', 'Managing offers, counteroffers, and negotiation communications.', 3),
    ('Documentation tracking', 'SALE', 'Tracking paperwork, legal documents, and transaction milestones.', 4),
    # Acquisition Assistance
    ('Area shortlisting', 'ACQUISITION', 'Research and recommendation of suitable areas matching your criteria.', 0),
    ('Builder and project verification', 'ACQUISITION', 'Due diligence on developers, approvals, and project credentials.', 1),
    ('Site visit representation', 'ACQUISITION', 'In-person site visits and reporting on your behalf.', 2),
    ('Negotiation assistance', 'ACQUISITION', 'Professional negotiation support for price and terms.', 3),
    ('Legal coordination support', 'ACQUISITION', 'Guidance through legal processes, documentation, and registration.', 4),
    # Priority Coordination
    ('Dedicated coordination support', 'PRIORITY', 'A single point of contact for all your property needs.', 0),
    ('Faster response handling', 'PRIORITY', 'Priority turnaround for requests and queries.', 1),
    ('Family and vendor coordination', 'PRIORITY', 'Managing coordination with family members and service vendors locally.', 2),
    ('End-to-end assistance support', 'PRIORITY', 'Full-service support across all stages of your property journey.', 3),
]


class Command(BaseCommand):
    help = 'Seed initial NRI service catalog'

    def handle(self, *args, **options):
        created = 0
        for name, category, description, sort_order in SEED_DATA:
            _, was_created = NRIService.objects.get_or_create(
                name=name,
                category=category,
                defaults={'description': description, 'sort_order': sort_order, 'is_active': True},
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(
            f'NRI Services seeded: {created} created, {len(SEED_DATA) - created} already existed.'
        ))
