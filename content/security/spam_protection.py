"""
SCCB-PROP-SEC-001 — SpamProtectionService

The single entry point for all form spam protection.
Views call this service; they never implement verification directly.

Usage in views:
    from content.security.spam_protection import SpamProtectionService

    service = SpamProtectionService(request)
    result = service.validate(form_name='General Inquiry')
    if not result.passed:
        if result.rate_limited:
            return HttpResponse(status=429)
        # re-render the form with result.error_message
"""

import logging

from content.security.validators import (
    validate_honeypot,
    validate_submission_time,
    validate_rate_limit,
    _get_ip,
)
from content.security.captcha_provider import get_captcha_provider

logger = logging.getLogger(__name__)


class SpamProtectionResult:
    """Structured outcome returned from SpamProtectionService.validate()."""

    def __init__(
        self,
        passed: bool,
        failure_reason: str = '',
        error_message: str = '',
        rate_limited: bool = False,
        captcha_failed: bool = False,
        google_error_codes: list = None,
        confidence_boost: int = 0,
    ):
        self.passed = passed
        self.failure_reason = failure_reason
        self.error_message = error_message
        self.rate_limited = rate_limited
        self.captcha_failed = captcha_failed
        self.google_error_codes = google_error_codes or []
        self.confidence_boost = confidence_boost  # Applied to assessment when CAPTCHA passes

    def __bool__(self):
        return self.passed


class SpamProtectionService:
    """
    Centralized spam protection orchestrator.

    Layers:
        1. Honeypot validation
        2. Submission timing validation
        3. IP rate limiting
        4. reCAPTCHA verification (provider-agnostic)
        5. Spam logging
    """

    def __init__(self, request):
        self.request = request

    def validate(self, form_name: str = 'Unknown Form') -> SpamProtectionResult:
        """
        Run all protection layers in sequence.
        Short-circuits on first failure (except fail-open CAPTCHA errors).
        """
        ip = _get_ip(self.request)
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:200]
        path = self.request.path
        referer = self.request.META.get('HTTP_REFERER', '')[:200]

        # ── Layer 2: Honeypot ──────────────────────────────────────────── #
        passed, reason = validate_honeypot(self.request)
        if not passed:
            self._log_spam(form_name, ip, user_agent, path, referer, reason)
            return SpamProtectionResult(
                passed=False,
                failure_reason=reason,
                error_message='',  # Silent reject for honeypot
            )

        # ── Layer 3: Rate Limiting ─────────────────────────────────────── #
        passed, reason = validate_rate_limit(self.request)
        if not passed:
            self._log_spam(form_name, ip, user_agent, path, referer, reason)
            return SpamProtectionResult(
                passed=False,
                failure_reason=reason,
                error_message='Too many submissions. Please try again later.',
                rate_limited=True,
            )

        # ── Layer 4: Submission Timing ─────────────────────────────────── #
        passed, reason = validate_submission_time(self.request)
        if not passed:
            self._log_spam(form_name, ip, user_agent, path, referer, reason)
            return SpamProtectionResult(
                passed=False,
                failure_reason=reason,
                error_message='Please take a moment to fill in the form completely.',
            )

        # ── Layer 1: reCAPTCHA Verification ───────────────────────────── #
        from realtor_project.features import is_feature_enabled
        captcha_enabled = is_feature_enabled('CAPTCHA_ENABLE', default=False)
        if captcha_enabled:
            token = self.request.POST.get('g-recaptcha-response', '')
            provider = get_captcha_provider()
            recaptcha_result = provider.verify(token, remote_ip=ip)

            if not recaptcha_result.success:
                error_codes = recaptcha_result.error_codes
                is_network_error = any(
                    e in error_codes for e in ('network-error', 'timeout', 'unexpected-error')
                )

                fail_open = getattr(
                    __import__('django.conf', fromlist=['settings']).settings,
                    'RECAPTCHA_FAIL_OPEN',
                    True,
                )

                if is_network_error and fail_open:
                    logger.warning(
                        '[SpamProtection] reCAPTCHA network error — fail-open. '
                        'ip=%s form=%s errors=%s',
                        ip, form_name, error_codes
                    )
                    self._log_spam(
                        form_name, ip, user_agent, path, referer,
                        'captcha-network-error-fail-open',
                        google_error_codes=error_codes,
                    )
                    # Fail-open: allow the enquiry through
                else:
                    self._log_spam(
                        form_name, ip, user_agent, path, referer,
                        'captcha-failed',
                        google_error_codes=error_codes,
                    )
                    return SpamProtectionResult(
                        passed=False,
                        failure_reason='captcha-failed',
                        error_message='Please complete the security verification before submitting your enquiry.',
                        captcha_failed=True,
                        google_error_codes=error_codes,
                    )
            else:
                logger.info(
                    '[SpamProtection] reCAPTCHA passed. form=%s ip=%s',
                    form_name, ip
                )
                return SpamProtectionResult(
                    passed=True,
                    confidence_boost=10,  # Reward verified submissions
                )

        logger.info('[SpamProtection] All layers passed. form=%s ip=%s', form_name, ip)
        return SpamProtectionResult(passed=True)

    def _log_spam(
        self,
        form_name: str,
        ip: str,
        user_agent: str,
        path: str,
        referer: str,
        failure_reason: str,
        google_error_codes: list = None,
        confidence_score: int = 0,
    ):
        """Write a SpamLog entry. Failures are silent — never block the request."""
        try:
            from content.models import SpamLog
            SpamLog.objects.create(
                ip_address=ip,
                user_agent=user_agent[:500],
                form_name=form_name[:100],
                request_path=path[:200],
                referer=referer[:200],
                failure_reason=failure_reason[:200],
                google_error_code=','.join(google_error_codes or [])[:100],
                confidence_score=confidence_score,
            )
        except Exception as e:
            logger.error('[SpamProtection] Failed to write SpamLog: %s', e)
