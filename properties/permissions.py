"""Inquiry API permissions — staff JWT/session or Deal Engine service key."""

import hmac
import hashlib

from django.conf import settings
from rest_framework.permissions import BasePermission


DEAL_ENGINE_SCHEME = "DealEngine"


def _digest(value: str) -> bytes:
    return hashlib.sha256(value.encode("utf-8")).digest()


def _configured_keys():
    active = (getattr(settings, "DEAL_ENGINE_INQUIRIES_KEY", None) or "").strip()
    previous = (getattr(settings, "DEAL_ENGINE_INQUIRIES_KEY_PREVIOUS", None) or "").strip()
    keys = []
    if active:
        keys.append(active)
    if previous and previous != active:
        keys.append(previous)
    return keys


def extract_deal_engine_key(request):
    header = request.META.get("HTTP_AUTHORIZATION") or ""
    parts = header.split(None, 1)
    if len(parts) != 2:
        return None
    scheme, value = parts[0].strip(), parts[1].strip()
    if scheme != DEAL_ENGINE_SCHEME or not value:
        return None
    return value


def service_key_is_valid(request) -> bool:
    provided = extract_deal_engine_key(request)
    if not provided:
        return False
    for configured in _configured_keys():
        if hmac.compare_digest(_digest(provided), _digest(configured)):
            return True
    return False


class IsStaffOrDealEngineKey(BasePermission):
    """Allow staff users (JWT or session) or a valid DealEngine service key.

    An empty/missing DEAL_ENGINE_INQUIRIES_KEY does not open anonymous access.
    The key is checked only here — it is not a global authentication backend.
    """

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated and user.is_staff:
            return True
        return service_key_is_valid(request)
