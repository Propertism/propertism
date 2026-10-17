"""
SCCB-PROP-SEC-001 — Individual Spam Protection Validators

Each validator is independently testable and returns a
(passed: bool, failure_reason: str) tuple.
"""

import logging
import ipaddress
import time

from django.conf import settings
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

    try:
        count = cache.get(cache_key, 0)
    except Exception as exc:
        # A broken shared cache must not silently turn a mandatory control into
        # an allow-all path.  The caller presents a retry-safe error response.
        logger.error('[SpamProtection] Rate-limit cache unavailable: %s', exc)
        return False, 'rate-limit-cache-unavailable'

    if count >= RATE_LIMIT_MAX:
        logger.warning(
            '[SpamProtection] Rate limit exceeded. ip=%s count=%d',
            ip, count
        )
        return False, f'rate-limit-exceeded:{count}'

    # Increment — set expiry only on first hit
    try:
        if count == 0:
            if cache.set(cache_key, 1, RATE_LIMIT_WINDOW) is False:
                raise RuntimeError('cache refused rate-limit write')
        else:
            if cache.incr(cache_key) is False:
                raise RuntimeError('cache refused rate-limit increment')
    except Exception as exc:
        logger.error('[SpamProtection] Rate-limit cache update failed: %s', exc)
        return False, 'rate-limit-cache-unavailable'

    return True, ''


# --------------------------------------------------------------------------- #
# Helper
# --------------------------------------------------------------------------- #

def _get_ip(request) -> str:
    """Return the rate-limit client IP without trusting arbitrary headers.

    ``X-Forwarded-For`` is accepted only when the immediate peer is explicitly
    configured as a trusted reverse proxy.  Production must provide
    ``TRUSTED_PROXY_IPS`` after its Nginx/Lightsail topology is verified; the
    secure default is the direct peer address.
    """
    remote_addr = request.META.get('REMOTE_ADDR', '0.0.0.0')
    trusted_proxies = getattr(settings, 'TRUSTED_PROXY_IPS', ()) or ()
    if isinstance(trusted_proxies, str):
        trusted_proxies = [item.strip() for item in trusted_proxies.split(',')]

    try:
        peer_is_trusted = ipaddress.ip_address(remote_addr) in {
            ipaddress.ip_address(item) for item in trusted_proxies if item
        }
    except ValueError:
        # A malformed setting must fail safe: ignore forwarded input.
        logger.error('[SpamProtection] Invalid TRUSTED_PROXY_IPS configuration.')
        peer_is_trusted = False

    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if peer_is_trusted and x_forwarded:
        candidate = x_forwarded.split(',')[0].strip()
        try:
            return str(ipaddress.ip_address(candidate))
        except ValueError:
            logger.warning('[SpamProtection] Ignoring malformed X-Forwarded-For.')
    return remote_addr
