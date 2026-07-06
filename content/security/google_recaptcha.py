"""
SCCB-PROP-SEC-001 — Google reCAPTCHA v2 Verification Service

Handles all communication with Google's siteverify API.
Provider-isolated: only this file needs changing if Google changes their API.
"""

import logging
import urllib.request
import urllib.parse
import urllib.error
import json

from django.conf import settings

logger = logging.getLogger(__name__)

# Accepted hostnames for hostname validation
ACCEPTED_HOSTNAMES = {
    'propertism.in',
    'www.propertism.in',
    'localhost',
    '127.0.0.1',
}

GOOGLE_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
VERIFICATION_TIMEOUT = 5  # seconds


class RecaptchaResult:
    """Structured result from Google reCAPTCHA verification."""

    def __init__(self, success: bool, hostname: str = '', error_codes: list = None, raw: dict = None):
        self.success = success
        self.hostname = hostname
        self.error_codes = error_codes or []
        self.raw = raw or {}

    def __bool__(self):
        return self.success

    def __repr__(self):
        return f'<RecaptchaResult success={self.success} hostname={self.hostname} errors={self.error_codes}>'


class GoogleRecaptchaV2:
    """
    Google reCAPTCHA v2 Checkbox verification provider.

    Usage:
        provider = GoogleRecaptchaV2()
        result = provider.verify(token, remote_ip)
        if result.success:
            # proceed
    """

    def verify(self, token: str, remote_ip: str = '') -> RecaptchaResult:
        """
        POST the reCAPTCHA token to Google's siteverify endpoint.

        Returns a RecaptchaResult. Never raises — all exceptions are caught
        and returned as a failed result so views can decide on fail-open policy.
        """
        secret_key = getattr(settings, 'RECAPTCHA_SECRET_KEY', '')

        if not secret_key:
            logger.warning(
                '[reCAPTCHA] RECAPTCHA_SECRET_KEY is not configured. '
                'Verification will be skipped. Set the key in environment variables.'
            )
            return RecaptchaResult(success=True, error_codes=['secret-key-missing'])

        if not token:
            logger.warning('[reCAPTCHA] Empty token received — verification failed.')
            return RecaptchaResult(success=False, error_codes=['missing-input-response'])

        payload = {
            'secret': secret_key,
            'response': token,
        }
        if remote_ip:
            payload['remoteip'] = remote_ip

        try:
            data = urllib.parse.urlencode(payload).encode('utf-8')
            req = urllib.request.Request(
                GOOGLE_VERIFY_URL,
                data=data,
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=VERIFICATION_TIMEOUT) as response:
                raw = json.loads(response.read().decode('utf-8'))

            success = raw.get('success', False)
            hostname = raw.get('hostname', '')
            error_codes = raw.get('error-codes', [])

            if success and hostname and hostname not in ACCEPTED_HOSTNAMES:
                logger.warning(
                    '[reCAPTCHA] Hostname mismatch: received=%s expected one of %s',
                    hostname, ACCEPTED_HOSTNAMES
                )
                return RecaptchaResult(
                    success=False,
                    hostname=hostname,
                    error_codes=['hostname-mismatch'],
                    raw=raw
                )

            if success:
                logger.info('[reCAPTCHA] Verification passed. hostname=%s', hostname)
            else:
                logger.warning('[reCAPTCHA] Verification failed. errors=%s', error_codes)

            return RecaptchaResult(
                success=success,
                hostname=hostname,
                error_codes=error_codes,
                raw=raw
            )

        except urllib.error.URLError as e:
            logger.error('[reCAPTCHA] Network error contacting Google: %s', e)
            return RecaptchaResult(success=False, error_codes=['network-error'])

        except TimeoutError:
            logger.error('[reCAPTCHA] Timeout after %ds contacting Google.', VERIFICATION_TIMEOUT)
            return RecaptchaResult(success=False, error_codes=['timeout'])

        except Exception as e:
            logger.error('[reCAPTCHA] Unexpected verification error: %s', e)
            return RecaptchaResult(success=False, error_codes=['unexpected-error'])
