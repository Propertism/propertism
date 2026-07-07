import os
from django.conf import settings
from realtor_project.features import is_feature_enabled

def validate_realbot_configuration():
    """
    Validates mandatory realBOT configuration settings and feature flags.
    Returns: (is_valid, issues_list, diagnostics_dict)
    """
    issues = []
    diagnostics = {}

    # 1. Feature Flag Status
    enabled_by_flag = is_feature_enabled("REALBOT_INTEGRATION_ENABLED", default=True)
    enabled_by_env = getattr(settings, "REALBOT_INTEGRATION_ENABLED", False)
    integration_enabled = enabled_by_flag and enabled_by_env
    
    diagnostics["integration_enabled"] = integration_enabled
    diagnostics["enabled_by_flag"] = enabled_by_flag
    diagnostics["enabled_by_env"] = enabled_by_env

    # 2. Check required settings variables
    mandatory_vars = {
        "REALBOT_BASE_URL": getattr(settings, "REALBOT_BASE_URL", None),
        "REALBOT_TENANT": getattr(settings, "REALBOT_TENANT", None),
        "REALBOT_PRODUCT": getattr(settings, "REALBOT_PRODUCT", None),
        "REALBOT_DOMAIN": getattr(settings, "REALBOT_DOMAIN", None),
        "REALBOT_ENVIRONMENT": getattr(settings, "REALBOT_ENVIRONMENT", None),
        "REALBOT_WIDGET_URL": getattr(settings, "REALBOT_WIDGET_URL", None),
        "REALBOT_API_VERSION": getattr(settings, "REALBOT_API_VERSION", None),
    }

    for var_name, value in mandatory_vars.items():
        diagnostics[var_name] = value
        if not value:
            issues.append(f"Missing mandatory setting: {var_name}")

    base_url = mandatory_vars.get("REALBOT_BASE_URL")
    if base_url and not (base_url.startswith("http://") or base_url.startswith("https://")):
        issues.append(f"Invalid REALBOT_BASE_URL protocol (must be http/https): {base_url}")

    widget_url = mandatory_vars.get("REALBOT_WIDGET_URL")
    if widget_url and not (widget_url.startswith("http://") or widget_url.startswith("https://")):
        issues.append(f"Invalid REALBOT_WIDGET_URL protocol (must be http/https): {widget_url}")

    is_valid = len(issues) == 0
    return is_valid, issues, diagnostics
