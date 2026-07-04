from django.apps import AppConfig
from django.db.models.signals import post_migrate

def seed_defaults(sender, **kwargs):
    from communications.models import (
        CommunicationLanguage,
        CommunicationChannel,
        CommunicationBrand,
        CommunicationType,
    )
    
    # 1. Seed languages
    languages = [
        ('en', 'English'),
        ('ta', 'Tamil'),
    ]
    for code, name in languages:
        CommunicationLanguage.objects.get_or_create(code=code, defaults={'name': name, 'is_active': True})
    
    # Delete Hindi if it exists
    CommunicationLanguage.objects.filter(code='hi').delete()
        
    # 2. Seed channels
    channels = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
    ]
    for key, name in channels:
        CommunicationChannel.objects.get_or_create(key=key, defaults={'name': name, 'is_active': True})

    # Delete SMS if it exists
    CommunicationChannel.objects.filter(key='sms').delete()
        
    # 3. Seed default types
    types = [
        ('inquiry_received', 'Inquiry Received', 'Triggered when a lead or inquiry is submitted.'),
        ('welcome', 'Welcome', 'Welcome onboarding notification.'),
        ('newsletter', 'Newsletter', 'Newsletter subscription confirmation.'),
        ('otp', 'OTP', 'One-time password for authentication.'),
    ]
    for key, name, desc in types:
        CommunicationType.objects.get_or_create(key=key, defaults={'name': name, 'description': desc})
        
    # 4. Seed default brand
    CommunicationBrand.objects.get_or_create(
        name='Propertism',
        defaults={
            'primary_color': '#0056b3',
            'is_default': True,
            'email_header': '<html><body><div style="font-family: Arial, sans-serif; padding: 20px;">',
            'email_footer': '</div><hr/><p style="font-size: 12px; color: #777;">&copy; 2026 Propertism. All rights reserved.</p></body></html>'
        }
    )

class CommunicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'communications'

    def ready(self):
        post_migrate.connect(seed_defaults, sender=self)
