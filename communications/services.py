import logging
from django.utils import timezone
from django.conf import settings
from django.template import Template, Context
from communications.models import (
    CommunicationBrand,
    CommunicationLanguage,
    CommunicationTemplate,
    CommunicationChannel,
    CommunicationPreference,
    CommunicationRequest,
    CommunicationDelivery,
    CommunicationLog,
    CommunicationRetry,
    CommunicationConfiguration,
    CommunicationType,
)

logger = logging.getLogger(__name__)

class LanguageService:
    @staticmethod
    def resolve_language(code):
        try:
            return CommunicationLanguage.objects.get(code=code.lower(), is_active=True)
        except CommunicationLanguage.DoesNotExist:
            # Fallback to English or first active
            lang = CommunicationLanguage.objects.filter(code='en', is_active=True).first()
            if not lang:
                lang = CommunicationLanguage.objects.filter(is_active=True).first()
            return lang


class BrandingService:
    @staticmethod
    def resolve_brand(name=None):
        if name:
            brand = CommunicationBrand.objects.filter(name=name).first()
            if brand:
                return brand
        # Fallback to default
        brand = CommunicationBrand.objects.filter(is_default=True).first()
        if not brand:
            brand = CommunicationBrand.objects.first()
        return brand


class TemplateService:
    @staticmethod
    def render_template(type_key, language_code, context, brand=None):
        # If pre-rendered subject and body are provided, bypass database rendering
        if 'subject' in context and 'body' in context:
            return None, context['subject'], context['body'], context.get('html_body', '')

        lang = LanguageService.resolve_language(language_code)
        if not lang:
            raise ValueError("No active language configuration found.")

        # Find CommunicationType
        comm_type = CommunicationType.objects.filter(key=type_key).first()
        if not comm_type:
            # Create a dynamic type on the fly
            comm_type = CommunicationType.objects.create(
                key=type_key,
                name=type_key.replace('_', ' ').title(),
                description="Auto-generated communication type."
            )

        template = CommunicationTemplate.objects.filter(communication_type=comm_type, language=lang).first()
        if not template and lang.code != 'en':
            # Fall back to English
            en_lang = CommunicationLanguage.objects.filter(code='en').first()
            if en_lang:
                template = CommunicationTemplate.objects.filter(communication_type=comm_type, language=en_lang).first()
        
        if not template:
            # Default fallback template properties if none defined in DB
            template = CommunicationTemplate.objects.create(
                name=f"{comm_type.name} Template",
                communication_type=comm_type,
                subject_template="Update from Propertism",
                body_template="Notification update content:\n\n{% for key, val in context.items %}{{ key }}: {{ val }}\n{% endfor %}",
                language=lang
            )
            
        ctx = Context({'context': context, **context})
        subject = Template(template.subject_template).render(ctx)
        body = Template(template.body_template).render(ctx)
        
        html_body = ""
        if template.html_body_template:
            raw_html = Template(template.html_body_template).render(ctx)
            brand_resolved = template.brand or brand
            if brand_resolved:
                header = Template(brand_resolved.email_header).render(ctx)
                footer = Template(brand_resolved.email_footer).render(ctx)
                html_body = f"{header}{raw_html}{footer}"
            else:
                html_body = raw_html
                
        return template, subject, body, html_body


class TrackingService:
    @staticmethod
    def generate_tracking_reference():
        import uuid
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        uid = uuid.uuid4().hex[:6].upper()
        return f"REF-{ts}-{uid}"


class DeliveryService:
    @staticmethod
    def log_delivery(delivery, status, response_text):
        delivery.status = status
        if status == 'sent':
            delivery.delivery_timestamp = timezone.now()
        elif status == 'failed':
            delivery.last_error = response_text
        delivery.save()
        
        CommunicationLog.objects.create(
            delivery=delivery,
            status=status,
            provider_response=response_text
        )


class RetryService:
    @staticmethod
    def get_max_attempts():
        try:
            config = CommunicationConfiguration.objects.get(key='max_retry_attempts')
            return int(config.value)
        except (CommunicationConfiguration.DoesNotExist, ValueError):
            return 3

    @classmethod
    def schedule_retry(cls, delivery, error_msg):
        max_attempts = cls.get_max_attempts()
        if delivery.retry_count >= max_attempts:
            logger.error("Delivery %s reached max attempts. Marking as permanent failure.", delivery.tracking_reference)
            DeliveryService.log_delivery(delivery, 'failed', f"Max attempts reached. Last error: {error_msg}")
            return False
            
        delivery.retry_count += 1
        delivery.save()
        
        scheduled_time = timezone.now() + timezone.timedelta(minutes=1)
        retry_task = CommunicationRetry.objects.create(
            delivery=delivery,
            scheduled_time=scheduled_time,
            attempt_number=delivery.retry_count,
            status='pending'
        )
        
        CommunicationLog.objects.create(
            delivery=delivery,
            status='retry_scheduled',
            provider_response=f"Scheduled retry attempt {delivery.retry_count} for {scheduled_time}"
        )
        return True


class AcknowledgementService:
    @staticmethod
    def send(communication_type_key, recipient, context, channels=None, brand_name=None, language_code='en', module='propertism'):
        from communications.dispatcher import CommunicationDispatcher

        # Resolve brand and language
        brand = BrandingService.resolve_brand(brand_name or context.get('brand_name'))
        lang = LanguageService.resolve_language(language_code)
        
        # Resolve CommunicationType
        comm_type = CommunicationType.objects.filter(key=communication_type_key).first()
        if not comm_type:
            comm_type = CommunicationType.objects.create(
                key=communication_type_key,
                name=communication_type_key.replace('_', ' ').title(),
                description="Auto-generated communication type."
            )

        # Retrieve/Render template (validates parsing template layout before saving Request)
        try:
            template, _, _, _ = TemplateService.render_template(
                communication_type_key, lang.code, context, brand
            )
        except Exception as e:
            logger.exception("Template resolution failed for type %s", communication_type_key)
            return None

        # Create audit request record
        request = CommunicationRequest.objects.create(
            module=module,
            recipient=recipient,
            template=template,
            context_data=context
        )

        # Autodetect channel if not provided
        if not channels:
            if '@' in recipient:
                channels = ['email']
            else:
                channels = ['whatsapp']

        for channel_key in channels:
            channel = CommunicationChannel.objects.filter(key=channel_key, is_active=True).first()
            if not channel:
                logger.warning("Channel %s is inactive or missing. Skipping.", channel_key)
                continue
                
            # Check preferences
            pref = CommunicationPreference.objects.filter(recipient=recipient, channel=channel).first()
            if pref and not pref.is_opted_in:
                logger.info("Recipient %s has opted out of channel %s", recipient, channel_key)
                continue
                
            # Generate tracking reference and create Delivery tracking entry
            ref = TrackingService.generate_tracking_reference()
            delivery = CommunicationDelivery.objects.create(
                request=request,
                channel=channel,
                status='pending',
                tracking_reference=ref
            )

            # Trigger Asynchronous Dispatch after transaction commits!
            from django.db import transaction
            transaction.on_commit(lambda d_id=delivery.id: CommunicationDispatcher.dispatch_async(d_id))
            
        return request
