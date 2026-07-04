import logging
from django.core.mail import send_mail
from django.conf import settings
from content.views import send_whatsapp_notification

logger = logging.getLogger(__name__)

class ChannelProvider:
    """Abstract base class for all communication channel providers."""
    def send(self, recipient, subject, body, html_body=None):
        raise NotImplementedError("Subclasses must implement the send method.")


class SMTPProvider(ChannelProvider):
    """SMTP provider utilizing Django's built-in email backend."""
    def send(self, recipient, subject, body, html_body=None):
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Propertism Admin <tamil@propertism.in>')
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[recipient],
            html_message=html_body if html_body else None,
            fail_silently=False
        )
        return "SMTP Send Success"


class WhatsAppProvider(ChannelProvider):
    """WhatsApp provider utilizing Meta Cloud API integration."""
    def send(self, recipient, subject, body, html_body=None):
        clean_recipient = "".join(filter(str.isdigit, recipient))
        send_whatsapp_notification(body, clean_recipient)
        return "WhatsApp API Send Success"


class SMSProvider(ChannelProvider):
    """SMS provider stub for future API integration."""
    def send(self, recipient, subject, body, html_body=None):
        logger.info("[SMS PROVIDER STUB] Sending SMS to %s: %s", recipient, body)
        return "SMS Send Success (Stub)"
