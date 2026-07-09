"""
SCCB-PROP-SEC-001 — Individual Spam Protection Validators

Each validator is independently testable and returns a
(passed: bool, failure_reason: str) tuple.
"""

import logging
import time

from django.core.cache import cache

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Honeypot Validator (Layer 2)
# --------------------------------------------------------------------------- #

def validate_honeypot(request) -> tuple[bool, str]:
    """
    Check the honeypot field. Bots fill it; humans never see it.
    Returns (True, '') if clean — (False, reason) if triggered.
    """
    honeypot_value = request.POST.get('website_url_check', '')
    if honeypot_value:
        logger.warning(
            '[SpamProtection] Honeypot triggered. ip=%s ua=%s value=%s',
            _get_ip(request),
            request.META.get('HTTP_USER_AGENT', '')[:80],
            honeypot_value[:40],
        )
        return False, 'honeypot-triggered'
    return True, ''


# --------------------------------------------------------------------------- #
# Submission Timing Validator (Layer 4)
# --------------------------------------------------------------------------- #

MINIMUM_SUBMISSION_SECONDS = 1


def validate_submission_time(request) -> tuple[bool, str]:
    """
    Reject submissions that arrive faster than a human can read the form.
    Relies on the hidden form_render_time field (Unix epoch).
    """
    render_time_str = request.POST.get('form_render_time', '')
    if not render_time_str:
        # Field absent — can't validate; pass through
        return True, ''

    try:
        render_time = int(render_time_str)
        elapsed = int(time.time()) - render_time
        if elapsed < MINIMUM_SUBMISSION_SECONDS:
            logger.warning(
                '[SpamProtection] Submission too fast: elapsed=%ds threshold=%ds ip=%s',
                elapsed, MINIMUM_SUBMISSION_SECONDS, _get_ip(request)
            )
            return False, f'submission-too-fast:{elapsed}s'
    except (ValueError, TypeError):
        pass  # Malformed value — ignore

    return True, ''


# --------------------------------------------------------------------------- #
# IP Rate Limiter (Layer 3)
# --------------------------------------------------------------------------- #

RATE_LIMIT_MAX = 5         # max submissions
RATE_LIMIT_WINDOW = 600    # seconds (10 minutes)
RATE_LIMIT_CACHE_PREFIX = 'spam_rl_'


def validate_rate_limit(request) -> tuple[bool, str]:
    """
    Enforce max 5 form submissions per IP per 10 minutes.
    Uses Django's cache backend.
    """
    ip = _get_ip(request)
    cache_key = f'{RATE_LIMIT_CACHE_PREFIX}{ip}'

    count = cache.get(cache_key, 0)
    if count >= RATE_LIMIT_MAX:
        logger.warning(
            '[SpamProtection] Rate limit exceeded. ip=%s count=%d',
            ip, count
        )
        return False, f'rate-limit-exceeded:{count}'

    # Increment — set expiry only on first hit
    if count == 0:
        cache.set(cache_key, 1, RATE_LIMIT_WINDOW)
    else:
        cache.incr(cache_key)

    return True, ''


# --------------------------------------------------------------------------- #
# Helper
# --------------------------------------------------------------------------- #

def _get_ip(request) -> str:
    """Extract real IP, respecting X-Forwarded-For from load balancers."""
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')
