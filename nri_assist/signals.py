import logging
from django.dispatch import receiver

logger = logging.getLogger(__name__)


try:
    from allauth.account.signals import user_logged_in, user_signed_up

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

    @receiver(user_signed_up)
    def on_user_signed_up(request, user, **kwargs):
        try:
            from communications.services import AcknowledgementService
            name = user.get_full_name() or user.username
            AcknowledgementService.send(
                communication_type_key='welcome',
                recipient=user.email,
                context={
                    'name': name,
                    'email': user.email
                },
                channels=['email'],
                module='nri_assist_signup'
            )
        except Exception:
            logger.exception('Failed to send welcome email for registered user %s', user.email)

except ImportError:
    pass
