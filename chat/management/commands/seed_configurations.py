"""
chat/management/commands/seed_configurations.py — Seeds standard platform configuration items.
"""
from django.core.management.base import BaseCommand
from chat.config_manager import ConfigurationManager


class Command(BaseCommand):
    help = "Seeds initial configuration items registry for M2.12"

    def handle(self, *args, **options):
        configs = [
            {
                'key': 'realbot_enabled',
                'value': 'true',
                'config_type': 'boolean',
                'category': 'PlatformConfiguration',
                'validation_rules': {}
            },
            {
                'key': 'captcha_enabled',
                'value': 'false',
                'config_type': 'boolean',
                'category': 'SecurityConfiguration',
                'validation_rules': {}
            },
            {
                'key': 'session_ttl_minutes',
                'value': '30',
                'config_type': 'integer',
                'category': 'ConversationConfiguration',
                'validation_rules': {'min': 5, 'max': 1440}
            },
            {
                'key': 'max_suggestion_chips',
                'value': '5',
                'config_type': 'integer',
                'category': 'SuggestionConfiguration',
                'validation_rules': {'min': 1, 'max': 10}
            },
            {
                'key': 'max_history_limit',
                'value': '20',
                'config_type': 'integer',
                'category': 'ConversationConfiguration',
                'validation_rules': {'min': 5, 'max': 100}
            }
        ]

        count = 0
        for item in configs:
            ConfigurationManager.update_setting(
                key=item['key'],
                value_str=item['value'],
                category=item['category'],
                config_type=item['config_type'],
                validation_rules=item['validation_rules'],
                modified_by='system_seeder'
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} configuration items."))
