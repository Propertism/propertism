import logging
from django.core.management.base import BaseCommand
from chat.models import ActionDefinition
from chat.actions_config import DEFAULT_ACTIONS

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Idempotent seeder for Action Definitions (M2.8 Navigation & Actions Registry)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset Action definitions table before seeding',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING("Resetting Action Definitions table..."))
            ActionDefinition.objects.all().delete()

        created_count = 0
        updated_count = 0

        for action_data in DEFAULT_ACTIONS:
            name = action_data['action_name']
            
            # Lookup or create
            definition, created = ActionDefinition.objects.get_or_create(
                action_name=name,
                defaults={
                    'category': action_data['category'],
                    'action_type': action_data['action_type'],
                    'display_name': action_data['display_name'],
                    'description': action_data.get('description', ''),
                    'target_url': action_data.get('target_url', ''),
                    'target_service': action_data.get('target_service', ''),
                    'supported_parameters': action_data.get('supported_parameters', []),
                    'confirmation_required': action_data.get('confirmation_required', False),
                    'visibility_rules': action_data.get('visibility_rules', {}),
                    'security_level': action_data.get('security_level', 'public'),
                    'status': action_data.get('status', 'active'),
                    'version': action_data.get('version', 1),
                }
            )

            if not created:
                # Update existing definition fields
                definition.category = action_data['category']
                definition.action_type = action_data['action_type']
                definition.display_name = action_data['display_name']
                definition.description = action_data.get('description', '')
                definition.target_url = action_data.get('target_url', '')
                definition.target_service = action_data.get('target_service', '')
                definition.supported_parameters = action_data.get('supported_parameters', [])
                definition.confirmation_required = action_data.get('confirmation_required', False)
                definition.visibility_rules = action_data.get('visibility_rules', {})
                definition.security_level = action_data.get('security_level', 'public')
                definition.status = action_data.get('status', 'active')
                definition.version = action_data.get('version', 1)
                definition.save()
                updated_count += 1
            else:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Action seeding complete. Created: {created_count}, Updated: {updated_count} definitions."
        ))
