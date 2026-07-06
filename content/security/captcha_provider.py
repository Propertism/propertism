"""
SCCB-PROP-SEC-001 — CAPTCHA Provider Abstraction Layer

Allows switching between reCAPTCHA providers (google_v2, turnstile, none)
via CAPTCHA_PROVIDER feature flag — without any view-level code changes.
"""

import logging

logger = logging.getLogger(__name__)

# Registry of available providers
_PROVIDERS = {}


def _load_providers():
    """Lazily load providers to avoid circular imports."""
    global _PROVIDERS
    if not _PROVIDERS:
        from content.security.google_recaptcha import GoogleRecaptchaV2
        _PROVIDERS = {
            'google_v2': GoogleRecaptchaV2,
            'none': None,
        }


class NullProvider:
    """No-op provider used when CAPTCHA_PROVIDER=none or CAPTCHA_ENABLE=false."""

    def verify(self, token: str, remote_ip: str = ''):
        from content.security.google_recaptcha import RecaptchaResult
        logger.info('[CaptchaProvider] NullProvider: verification bypassed (CAPTCHA disabled or provider=none).')
        return RecaptchaResult(success=True, error_codes=['captcha-disabled'])


def get_captcha_provider():
    """
    Return the correct CAPTCHA provider instance based on feature flags.

    CAPTCHA_ENABLE = false  → NullProvider (no verification)
    CAPTCHA_PROVIDER = google_v2  → GoogleRecaptchaV2
    CAPTCHA_PROVIDER = none  → NullProvider
    """
    from realtor_project.features import is_feature_enabled
    captcha_enabled = is_feature_enabled('CAPTCHA_ENABLE', default=False)
    if not captcha_enabled:
        return NullProvider()

    provider_name = is_feature_enabled('CAPTCHA_PROVIDER', default='google_v2')
    # is_feature_enabled returns bool for boolean flags — handle string flags too
    if isinstance(provider_name, bool):
        provider_name = 'google_v2'

    _load_providers()
    provider_class = _PROVIDERS.get(str(provider_name))

    if provider_class is None:
        logger.info('[CaptchaProvider] Provider=%s maps to NullProvider.', provider_name)
        return NullProvider()

    return provider_class()


def get_site_key() -> str:
    """Return the reCAPTCHA site key for template rendering."""
    from django.conf import settings
    from realtor_project.features import is_feature_enabled
    captcha_enabled = is_feature_enabled('CAPTCHA_ENABLE', default=False)
    if not captcha_enabled:
        return ''
    return getattr(settings, 'RECAPTCHA_SITE_KEY', '')
