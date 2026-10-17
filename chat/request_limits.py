"""Cache-backed rate limits for realBOT public JSON endpoints (SCCB-09 C1)."""

import logging

from django.core.cache import cache

from content.security.validators import _get_ip
from chat.security_manager import SecurityAuditManager

logger = logging.getLogger(__name__)

WINDOW_SECONDS = 600
INIT_PER_IP = 5
MESSAGE_PER_IP = 20
MESSAGE_PER_SESSION = 15
INITIATE_PER_IP = 5


def _bump(cache_key: str, limit: int) -> bool:
    try:
        count = cache.get(cache_key, 0)
    except Exception as exc:
        logger.error('[realBOT] rate-limit cache unavailable: %s', exc)
        return False
    if count >= limit:
        return False
    try:
        if count == 0:
            if cache.set(cache_key, 1, WINDOW_SECONDS) is False:
                raise RuntimeError('cache refused rate-limit write')
        else:
            if cache.incr(cache_key) is False:
                raise RuntimeError('cache refused rate-limit increment')
    except Exception as exc:
        logger.error('[realBOT] rate-limit cache update failed: %s', exc)
        return False
    return True


def _deny(request, session_id, reason):
    try:
        SecurityAuditManager().log_event(
            event_type="rate_limit",
            severity="warning",
            source_ip="",
            session_id=str(session_id or ""),
            request_path=getattr(request, "path", "")[:200],
            details={"reason": reason},
        )
    except Exception:
        logger.info("[realBOT] rate limit %s path=%s", reason, getattr(request, "path", ""))
    return False


def allow_session_init(request) -> bool:
    ip = _get_ip(request)
    if not _bump(f"rbot_init_ip_{ip}", INIT_PER_IP):
        return _deny(request, "", "init-ip")
    return True


def allow_send_message(request, session_id: str) -> bool:
    ip = _get_ip(request)
    if not _bump(f"rbot_msg_ip_{ip}", MESSAGE_PER_IP):
        return _deny(request, session_id, "message-ip")
    if session_id and not _bump(f"rbot_msg_sess_{session_id}", MESSAGE_PER_SESSION):
        return _deny(request, session_id, "message-session")
    return True


def allow_inquiry_initiate(request) -> bool:
    ip = _get_ip(request)
    if not _bump(f"rbot_initq_ip_{ip}", INITIATE_PER_IP):
        return _deny(request, "", "initiate-ip")
    return True
