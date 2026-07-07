"""
chat/management/commands/seed_services.py — M2.5
Idempotent Django management command that loads all 14 Service Profiles into the DB.

Usage:
    .\\scripts\\django.cmd seed_services
    .\\scripts\\django.cmd seed_services --reset
"""
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Seed the ServiceProfile table with all 14 Propertism service definitions (M2.5)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing ServiceProfile records before seeding.',
        )

    def handle(self, *args, **options):
        from chat.models import ServiceProfile
        from chat.services_config import SEED_SERVICES

        if options['reset']:
            count = ServiceProfile.objects.count()
            ServiceProfile.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f"[seed_services] Reset: deleted {count} existing service profiles."
            ))

        created = updated = skipped = 0

        with transaction.atomic():
            for srv_data in SEED_SERVICES:
                name = srv_data['name']
                defaults = {
                    'category':             srv_data['category'],
                    'short_description':    srv_data['short_description'],
                    'detailed_description':  srv_data['detailed_description'],
                    'business_objective':   srv_data['business_objective'],
                    'target_audience':      srv_data['target_audience'],
                    'eligibility':          srv_data.get('eligibility', ''),
                    'required_inputs':      srv_data.get('required_inputs', ''),
                    'advisory_content':     srv_data.get('advisory_content', {}),
                    'faqs':                 srv_data.get('faqs', []),
                    'knowledge_references': srv_data.get('knowledge_references', ''),
                    'related_services':     srv_data.get('related_services', []),
                    'call_to_actions':      srv_data.get('call_to_actions', []),
                    'contact_channels':     srv_data.get('contact_channels', []),
                    'escalation_rules':     srv_data.get('escalation_rules', {}),
                    'navigation_links':     srv_data.get('navigation_links', []),
                    'display_priority':     srv_data.get('display_priority', 50),
                    'status':               'active',
                }

                existing = ServiceProfile.objects.filter(name=name).first()

                if existing is None:
                    # Create new ServiceProfile (service_id auto-generated on save)
                    ServiceProfile.objects.create(name=name, **defaults)
                    self.stdout.write(
                        self.style.SUCCESS(f"  [CREATED] {name}")
                    )
                    created += 1
                else:
                    # Check if any field changed
                    changed = any(
                        getattr(existing, field) != value
                        for field, value in defaults.items()
                        if field not in ('status',)
                    )
                    if changed:
                        for field, value in defaults.items():
                            setattr(existing, field, value)
                        existing.version += 1
                        existing.save()
                        self.stdout.write(
                            self.style.WARNING(f"  [UPDATED] {name} → v{existing.version}")
                        )
                        updated += 1
                    else:
                        self.stdout.write(f"  [SKIP]    {name}")
                        skipped += 1

        total = created + updated + skipped
        self.stdout.write(self.style.SUCCESS(
            f"\n[seed_services] Done. {total} service profiles processed: "
            f"{created} created, {updated} updated, {skipped} unchanged."
        ))

        # Output current total count
        self.stdout.write(
            f"[seed_services] Registry: {ServiceProfile.objects.filter(status='active').count()} active "
            f"({ServiceProfile.objects.count()} total)."
        )
