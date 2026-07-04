import logging
from concurrent.futures import ThreadPoolExecutor
from django.db import transaction
from communications.providers import SMTPProvider, WhatsAppProvider, SMSProvider

logger = logging.getLogger(__name__)

# Pre-initialized thread pool for background dispatches
executor = ThreadPoolExecutor(max_workers=5)

class CommunicationDispatcher:
    _providers = {
        'email': SMTPProvider(),
        'whatsapp': WhatsAppProvider(),
        'sms': SMSProvider(),
    }

    @classmethod
    def register_provider(cls, channel_key, provider):
        """Allows registering new transport channels at runtime."""
        cls._providers[channel_key] = provider

    @classmethod
    def dispatch_async(cls, delivery_id):
        """Asynchronously dispatch a delivery in a background thread."""
        from django.conf import settings
        is_async = getattr(settings, 'COMMUNICATIONS_ASYNC', True)
        if is_async:
            logger.info("Scheduling delivery ID %s for background processing...", delivery_id)
            executor.submit(cls.dispatch, delivery_id)
        else:
            logger.info("Executing delivery ID %s synchronously...", delivery_id)
            cls.dispatch(delivery_id)

    @classmethod
    def dispatch(cls, delivery_id):
        """Synchronously execute a delivery dispatch (run by the background thread)."""
        from communications.models import CommunicationDelivery
        from communications.services import DeliveryService, RetryService, TemplateService, BrandingService

        # Fetch delivery within its own transaction context
        with transaction.atomic():
            try:
                delivery = CommunicationDelivery.objects.select_related(
                    'request', 'channel', 'request__template', 'request__template__brand'
                ).get(id=delivery_id)
            except CommunicationDelivery.DoesNotExist:
                logger.error("Delivery ID %s not found. Skipping dispatch.", delivery_id)
                return

            if delivery.status == 'sent':
                logger.info("Delivery %s is already sent. Skipping.", delivery.tracking_reference)
                return

        # Resolve provider
        provider_key = delivery.channel.key
        provider = cls._providers.get(provider_key)
        if not provider:
            error_msg = f"No provider configured for channel: {provider_key}"
            logger.error(error_msg)
            with transaction.atomic():
                delivery = CommunicationDelivery.objects.get(id=delivery_id)
                DeliveryService.log_delivery(delivery, 'failed', error_msg)
            return

        # Render template content
        try:
            req = delivery.request
            brand = BrandingService.resolve_brand(req.context_data.get('brand_name'))
            lang_code = req.context_data.get('language_code', 'en')
            
            # Resolve and render template details
            template, subject, body, html_body = TemplateService.render_template(
                req.template.communication_type.key if req.template else 'default',
                lang_code,
                req.context_data,
                brand
            )
        except Exception as e:
            error_msg = f"Template rendering failure: {str(e)}"
            logger.exception(error_msg)
            with transaction.atomic():
                delivery = CommunicationDelivery.objects.get(id=delivery_id)
                DeliveryService.log_delivery(delivery, 'failed', error_msg)
            return

        # Execute provider send outside database transaction to avoid locking during network request
        try:
            logger.info("Dispatching delivery %s via provider %s...", delivery.tracking_reference, provider_key)
            result = provider.send(
                recipient=req.recipient,
                subject=subject,
                body=body,
                html_body=html_body if provider_key == 'email' else None
            )
            
            # Log success in transaction
            with transaction.atomic():
                delivery = CommunicationDelivery.objects.get(id=delivery_id)
                DeliveryService.log_delivery(delivery, 'sent', result)
                logger.info("Delivery %s sent successfully.", delivery.tracking_reference)
        except Exception as exc:
            error_msg = str(exc)
            logger.error("Provider send failure on delivery %s: %s", delivery.tracking_reference, error_msg)
            
            # Schedule retry in transaction
            with transaction.atomic():
                delivery = CommunicationDelivery.objects.get(id=delivery_id)
                RetryService.schedule_retry(delivery, error_msg)
