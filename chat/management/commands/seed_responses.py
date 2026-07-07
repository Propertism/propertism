import logging
from django.core.management.base import BaseCommand
from chat.models import ResponseComponent
from chat.response_config import DEFAULT_COMPONENTS

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Idempotent seeder for Response Components (M2.9 Rich Response Component Registry)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset Response Components table before seeding',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING("Resetting Response Components table..."))
            ResponseComponent.objects.all().delete()

        created_count = 0
        updated_count = 0

        for comp_data in DEFAULT_COMPONENTS:
            name = comp_data['name']
            
            # Lookup or create
            definition, created = ResponseComponent.objects.get_or_create(
                name=name,
                defaults={
                    'component_type': comp_data['component_type'],
                    'display_template': comp_data['display_template'],
                    'content_model': comp_data['content_model'],
                    'data_schema': comp_data['data_schema'],
                    'rendering_priority': comp_data['rendering_priority'],
                    'status': comp_data.get('status', 'active'),
                    'version': comp_data.get('version', 1),
                }
            )

            if not created:
                # Update existing definition fields
                definition.component_type = comp_data['component_type']
                definition.display_template = comp_data['display_template']
                definition.content_model = comp_data['content_model']
                definition.data_schema = comp_data['data_schema']
                definition.rendering_priority = comp_data['rendering_priority']
                definition.status = comp_data.get('status', 'active')
                definition.version = comp_data.get('version', 1)
                definition.save()
                updated_count += 1
            else:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Response component seeding complete. Created: {created_count}, Updated: {updated_count} components."
        ))
