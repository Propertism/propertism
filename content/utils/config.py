import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)


def get_system_config(key, default=None):
    """
    Fetch configuration parameter value from SystemConfig DB table.
    Uses in-memory/cache fallback. Falls back to default if key is not found or DB is initializing.
    """
    cache_key = f"sys_config:{key}"
    cached_val = cache.get(cache_key)
    if cached_val is not None:
        return cached_val

    try:
        from content.models import SystemConfig
        config_item = SystemConfig.objects.filter(key=key).first()
        if config_item and config_item.value:
            val = config_item.value
            cache.set(cache_key, val, timeout=300)  # Cache for 5 minutes
            return val
    except Exception as e:
        logger.debug("Failed to read SystemConfig key %s: %s", key, e)

    return default


def set_system_config(key, value, category='general', is_secret=False, description=''):
    """
    Helper utility to set or update a SystemConfig key-value pair in DB & invalidate cache.
    """
    from content.models import SystemConfig
    obj, created = SystemConfig.objects.update_or_create(
        key=key,
        defaults={
            'value': str(value) if value is not None else '',
            'category': category,
            'is_secret': is_secret,
            'description': description,
        }
    )
    cache_key = f"sys_config:{key}"
    cache.delete(cache_key)
    return obj
