import os
from django.core.management.base import BaseCommand
from content.models import SystemConfig


class Command(BaseCommand):
    help = "Seed environment variables into PostgreSQL SystemConfig DB table."

    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing non-empty SystemConfig values in the database',
        )

    def handle(self, *args, **options):
        overwrite = options.get('overwrite', False)
        initial_configs = [
            # Site & Canonical URLs
            {
                'key': 'CANONICAL_HOST',
                'value': os.environ.get('CANONICAL_HOST', 'www.propertism.in'),
                'category': 'site',
                'is_secret': False,
                'description': 'Primary domain hostname for canonical redirects',
            },
            {
                'key': 'CANONICAL_SCHEME',
                'value': os.environ.get('CANONICAL_SCHEME', 'https'),
                'category': 'site',
                'is_secret': False,
                'description': 'Canonical HTTP scheme (https or http)',
            },
            {
                'key': 'SITE_URL',
                'value': os.environ.get('SITE_URL', 'https://www.propertism.in'),
                'category': 'site',
                'is_secret': False,
                'description': 'Full site base URL used in outbound templates & sitemaps',
            },
            {
                'key': 'ADMIN_EMAIL',
                'value': os.environ.get('ADMIN_EMAIL', 'info@propertism.in'),
                'category': 'site',
                'is_secret': False,
                'description': 'Primary administrator contact inbox',
            },
            {
                'key': 'EXTRA_NOTIFICATION_EMAIL',
                'value': os.environ.get('EXTRA_NOTIFICATION_EMAIL', 'propertism.tamil@gmail.com,tamil@propertism.in'),
                'category': 'site',
                'is_secret': False,
                'description': 'Comma-separated recipient emails for lead alerts',
            },

            # Outbound Email (SMTP)
            {
                'key': 'EMAIL_HOST',
                'value': os.environ.get('EMAIL_HOST', 'smtpout.secureserver.net'),
                'category': 'smtp',
                'is_secret': False,
                'description': 'Outbound SMTP mail server hostname',
            },
            {
                'key': 'EMAIL_PORT',
                'value': os.environ.get('EMAIL_PORT', '587'),
                'category': 'smtp',
                'is_secret': False,
                'description': 'Outbound SMTP server port (587 TLS)',
            },
            {
                'key': 'EMAIL_HOST_USER',
                'value': os.environ.get('EMAIL_HOST_USER', 'tamil@propertism.in'),
                'category': 'smtp',
                'is_secret': False,
                'description': 'Outbound SMTP authentication account email',
            },
            {
                'key': 'EMAIL_HOST_PASSWORD',
                'value': os.environ.get('EMAIL_HOST_PASSWORD', 'PropTami@4'),
                'category': 'smtp',
                'is_secret': True,
                'description': 'Outbound Titan SMTP authentication password',
            },

            # realBOT & AI Settings
            {
                'key': 'REALBOT_INTEGRATION_ENABLED',
                'value': os.environ.get('REALBOT_INTEGRATION_ENABLED', 'True'),
                'category': 'ai_chat',
                'is_secret': False,
                'description': 'Enable/Disable realBOT 24/7 AI chatbot endpoints',
            },
            {
                'key': 'REALBOT_BASE_URL',
                'value': os.environ.get('REALBOT_BASE_URL', 'http://127.0.0.1:8010'),
                'category': 'ai_chat',
                'is_secret': False,
                'description': 'realBOT backend AI service base URL',
            },
            {
                'key': 'DEEPSEEK_API_KEY',
                'value': os.environ.get('DEEPSEEK_API_KEY', ''),
                'category': 'ai_chat',
                'is_secret': True,
                'description': 'DeepSeek API Key for realBOT AI assistant',
            },

            # reCAPTCHA & Security Settings
            {
                'key': 'RECAPTCHA_SITE_KEY',
                'value': os.environ.get('RECAPTCHA_SITE_KEY', '6LfvTkctAAAAAI6HkkGwvyEIAmdrzq6qYy3zb7FM'),
                'category': 'security',
                'is_secret': False,
                'description': 'Google reCAPTCHA v2 Site Key (Public)',
            },
            {
                'key': 'RECAPTCHA_SECRET_KEY',
                'value': os.environ.get('RECAPTCHA_SECRET_KEY', '6LfvTkctAAAAACRtPV3w2dO8IulaVfBUhGB4syyY'),
                'category': 'security',
                'is_secret': True,
                'description': 'Google reCAPTCHA v2 Secret Key (Private)',
            },
            {
                'key': 'RECAPTCHA_FAIL_OPEN',
                'value': os.environ.get('RECAPTCHA_FAIL_OPEN', 'False'),
                'category': 'security',
                'is_secret': False,
                'description': 'Allow lead submissions if Google reCAPTCHA server is unreachable',
            },

            # Analytics
            {
                'key': 'CLARITY_PROJECT_ID',
                'value': os.environ.get('CLARITY_PROJECT_ID', ''),
                'category': 'analytics',
                'is_secret': False,
                'description': 'Microsoft Clarity analytics tracking project ID',
            },
        ]

        created_count = 0
        updated_count = 0

        for cfg in initial_configs:
            existing = SystemConfig.objects.filter(key=cfg['key']).first()
            if existing:
                should_update_value = overwrite or (not existing.value and cfg['value'])
                if should_update_value:
                    existing.value = cfg['value']
                existing.category = cfg['category']
                existing.is_secret = cfg['is_secret']
                existing.description = cfg['description']
                existing.save()
                updated_count += 1
            else:
                SystemConfig.objects.create(
                    key=cfg['key'],
                    value=cfg['value'],
                    category=cfg['category'],
                    is_secret=cfg['is_secret'],
                    description=cfg['description'],
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"[SUCCESS] SystemConfig seeded successfully: {created_count} created, {updated_count} updated."
            )
        )

