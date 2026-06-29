import json
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

FEATURE_FLAGS_FILE = os.path.join(settings.BASE_DIR, 'feature_flags.json')

def is_feature_enabled(feature_name, default=False):
    """
    Reads the feature flag from feature_flags.json.
    Returns the boolean value for the given feature_name.
    """
    try:
        if os.path.exists(FEATURE_FLAGS_FILE):
            with open(FEATURE_FLAGS_FILE, 'r') as f:
                flags = json.load(f)
                # Ensure we strictly return a boolean
                return bool(flags.get(feature_name, default))
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {FEATURE_FLAGS_FILE}")
    except Exception as e:
        logger.error(f"Error reading feature flag {feature_name}: {e}")
        
    return default
