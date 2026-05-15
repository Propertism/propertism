import logging

from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class PropertismAccountAdapter(DefaultAccountAdapter):
    """
    SCCB-SEC-PRT-1510: Block direct email+password signup.
    Google OAuth is the only registration path.
    """

    def is_open_for_signup(self, request):
        return False


class AdminOnlySocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Blocks Google OAuth completions where the email is not verified by Google.
    Verified accounts proceed normally — auth.User is created by allauth default.
    Admin access is governed separately by AdminAccessMiddleware.
    """

    def pre_social_login(self, request, sociallogin):
        # Check Google's email_verified flag from the OAuth payload.
        extra_data = sociallogin.account.extra_data or {}
        email_verified = extra_data.get('email_verified', False)

        # Fallback: check allauth's own email address list.
        if not email_verified:
            email_verified = any(
                ea.verified for ea in sociallogin.email_addresses
            )

        if not email_verified:
            email = extra_data.get('email', 'unknown')
            logger.warning(
                "Blocked unverified Google OAuth attempt: %s", email
            )
            messages.error(
                request,
                'Your Google account email is not verified. '
                'Please verify your email with Google and try again.',
            )
            raise ImmediateHttpResponse(redirect('/'))
