import logging
from django.dispatch import receiver

logger = logging.getLogger(__name__)


try:
    from allauth.account.signals import user_logged_in

    @receiver(user_logged_in)
    def on_google_login(sender, request, user, **kwargs):
        try:
            from allauth.socialaccount.models import SocialAccount
            from .models import NRIAssistEvent
            if SocialAccount.objects.filter(user=user, provider='google').exists():
                forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
                ip = forwarded.split(',')[0].strip() if forwarded else request.META.get('REMOTE_ADDR')
                NRIAssistEvent.objects.create(
                    event_type=NRIAssistEvent.GOOGLE_LOGIN,
                    user=user,
                    metadata={'provider': 'google'},
                    ip_address=ip or None,
                )
        except Exception:
            logger.exception('NRIAssistEvent Google login log failed')

except ImportError:
    pass
