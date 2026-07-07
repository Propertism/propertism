from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    verbose_name = 'Live Chat Messages'

    def ready(self):
        # Prevent multiple execution in dev mode
        import os
        from django.conf import settings
        if os.environ.get('RUN_MAIN') == 'true' or not settings.DEBUG:
            from chat.validators import validate_realbot_configuration
            from chat.metrics import InfrastructureMetrics
            import logging
            
            # Increment startup count metric
            InfrastructureMetrics.increment("app_startup_count")
            
            # Run startup validation
            is_valid, issues, report = validate_realbot_configuration()
            
            logger = logging.getLogger('chat')
            
            # Generate structured startup diagnostics banner
            banner = [
                "==================================================",
                "       realBOT INTEGRATION FRAMEWORK INITIALIZED   ",
                "==================================================",
                f"  realBOT Version      : 2.1.1-stable",
                f"  API Version          : {settings.REALBOT_API_VERSION}",
                f"  Environment          : {settings.REALBOT_ENVIRONMENT}",
                f"  Feature status       : {'ENABLED' if report['integration_enabled'] else 'DISABLED'}",
                f"  Configuration status : {'VALID' if is_valid else 'INVALID'}",
            ]
            if not is_valid:
                banner.append("  Issues Identified    :")
                for issue in issues:
                    banner.append(f"    - {issue}")
                    InfrastructureMetrics.increment("configuration_errors")
            banner.append("==================================================")
            
            for line in banner:
                logger.info(line)
                
            # Fail fast if integration is enabled but has invalid settings
            if not is_valid and report['integration_enabled']:
                from django.core.exceptions import ImproperlyConfigured
                raise ImproperlyConfigured(f"realBOT Configuration Hardening Failure: {', '.join(issues)}")
