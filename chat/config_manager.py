"""
chat/config_manager.py — M2.12 Administration & Configuration Management Framework.
Implements ConfigurationValidator, ConfigurationCacheManager, and ConfigurationManager.
"""
import json
import re
import logging
from typing import Any, Dict, List, Optional
from chat.models import ConfigurationItem, ConfigurationAuditLog

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Configuration Cache Manager
# ─────────────────────────────────────────────────────────────────────────────

class ConfigurationCacheManager:
    """In-memory cache layer to ensure zero database retrieval latency during runtime conversation streams."""
    _cache: Dict[str, Any] = {}

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        return cls._cache.get(key)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        cls._cache[key] = value

    @classmethod
    def delete(cls, key: str) -> None:
        cls._cache.pop(key, None)

    @classmethod
    def clear(cls) -> None:
        cls._cache.clear()


# ─────────────────────────────────────────────────────────────────────────────
# 2. Configuration Validator
# ─────────────────────────────────────────────────────────────────────────────

class ConfigurationValidator:
    """Validates configuration values against data types and rule boundaries."""

    @staticmethod
    def validate_and_parse(value_str: str, config_type: str, rules: Optional[Dict[str, Any]] = None) -> Any:
        rules = rules or {}

        # 1. Type validation and parsing
        if config_type == 'boolean':
            cleaned = value_str.strip().lower()
            if cleaned in ('true', '1', 'yes', 'on'):
                parsed_val = True
            elif cleaned in ('false', '0', 'no', 'off'):
                parsed_val = False
            else:
                raise ValueError(f"Value '{value_str}' is not a valid boolean.")

        elif config_type == 'integer':
            try:
                parsed_val = int(value_str)
            except ValueError:
                raise ValueError(f"Value '{value_str}' is not a valid integer.")

        elif config_type == 'float':
            try:
                parsed_val = float(value_str)
            except ValueError:
                raise ValueError(f"Value '{value_str}' is not a valid float.")

        elif config_type == 'json':
            try:
                parsed_val = json.loads(value_str)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Value '{value_str}' is not valid JSON: {exc}")

        else:  # string
            parsed_val = value_str

        # 2. Constraint validation
        if config_type in ('integer', 'float'):
            if 'min' in rules:
                if parsed_val < rules['min']:
                    raise ValueError(f"Value {parsed_val} is below minimum allowed ({rules['min']}).")
            if 'max' in rules:
                if parsed_val > rules['max']:
                    raise ValueError(f"Value {parsed_val} exceeds maximum allowed ({rules['max']}).")

        elif config_type == 'string':
            if 'regex' in rules:
                pattern = rules['regex']
                if not re.search(pattern, parsed_val):
                    raise ValueError(f"Value '{parsed_val}' does not match validation pattern: {pattern}")
            if 'choices' in rules:
                if parsed_val not in rules['choices']:
                    raise ValueError(f"Value '{parsed_val}' is not in allowed choices: {rules['choices']}")

        return parsed_val


# ─────────────────────────────────────────────────────────────────────────────
# 3. Central Configuration Manager
# ─────────────────────────────────────────────────────────────────────────────

class ConfigurationManager:
    """Manages central configurations, audits histories, rollbacks and exports."""

    @classmethod
    def get_setting(cls, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves a typed, cache-backed setting.
        Fallbacks to default value if not found in database.
        """
        cached_val = ConfigurationCacheManager.get(key)
        if cached_val is not None:
            return cached_val

        try:
            item = ConfigurationItem.objects.get(key=key, status='active')
            parsed_val = ConfigurationValidator.validate_and_parse(
                item.value, item.config_type, item.validation_rules
            )
            ConfigurationCacheManager.set(key, parsed_val)
            return parsed_val
        except ConfigurationItem.DoesNotExist:
            if default is not None:
                return default
            return None
        except Exception as exc:
            logger.warning(f"Error parsing configuration key '{key}': {exc}. Returning default fallback.")
            return default

    @classmethod
    def update_setting(
        cls,
        key: str,
        value_str: str,
        modified_by: str = 'admin',
        category: str = 'Platform',
        config_type: str = 'string',
        validation_rules: Optional[Dict[str, Any]] = None
    ) -> ConfigurationItem:
        """
        Updates setting value, increments version, invalidates cache, and writes to audit logs.
        """
        # Fetch or create the setting
        item, created = ConfigurationItem.objects.get_or_create(
            key=key,
            defaults={
                'category': category,
                'config_type': config_type,
                'value': value_str,
                'validation_rules': validation_rules or {},
                'last_modified_by': modified_by
            }
        )

        if not created:
            # Type assertion verification
            ConfigurationValidator.validate_and_parse(value_str, item.config_type, item.validation_rules)

            # Record audit details
            prev_value = item.value
            item.value = value_str
            item.version += 1
            item.last_modified_by = modified_by
            item.save()

            ConfigurationAuditLog.objects.create(
                config_item=item,
                action='updated',
                previous_value=prev_value,
                new_value=value_str,
                version=item.version,
                modified_by=modified_by
            )
        else:
            # Validate new item value
            ConfigurationValidator.validate_and_parse(value_str, config_type, validation_rules)
            ConfigurationAuditLog.objects.create(
                config_item=item,
                action='created',
                previous_value='',
                new_value=value_str,
                version=1,
                modified_by=modified_by
            )

        # Invalidate Cache
        ConfigurationCacheManager.delete(key)
        return item

    @classmethod
    def rollback_setting(cls, key: str, target_version: int, modified_by: str = 'admin') -> ConfigurationItem:
        """
        Rolls back configuration value to target version state.
        """
        try:
            item = ConfigurationItem.objects.get(key=key)
        except ConfigurationItem.DoesNotExist:
            raise ValueError(f"Configuration key '{key}' does not exist.")

        # Find target version inside Audit Log
        try:
            audit = ConfigurationAuditLog.objects.get(config_item=item, version=target_version)
        except ConfigurationAuditLog.DoesNotExist:
            raise ValueError(f"Version {target_version} does not exist in history for key '{key}'.")

        # Validate the value again to ensure safety
        restored_val = audit.new_value
        ConfigurationValidator.validate_and_parse(restored_val, item.config_type, item.validation_rules)

        prev_val = item.value
        item.value = restored_val
        item.version += 1
        item.last_modified_by = modified_by
        item.save()

        # Log rollback event
        ConfigurationAuditLog.objects.create(
            config_item=item,
            action='rollback',
            previous_value=prev_val,
            new_value=restored_val,
            version=item.version,
            modified_by=modified_by
        )

        ConfigurationCacheManager.delete(key)
        return item

    @classmethod
    def export_configurations(cls) -> List[Dict[str, Any]]:
        """
        Returns JSON-serializable list of all config definitions.
        """
        items = ConfigurationItem.objects.all()
        exported = []
        for item in items:
            exported.append({
                'key': item.key,
                'category': item.category,
                'config_type': item.config_type,
                'value': item.value,
                'default_value': item.default_value,
                'validation_rules': item.validation_rules,
                'visibility_level': item.visibility_level,
                'editable': item.editable,
                'requires_approval': item.requires_approval,
                'version': item.version,
                'status': item.status
            })
        return exported

    @classmethod
    def import_configurations(cls, configs_list: List[Dict[str, Any]], modified_by: str = 'admin') -> int:
        """
        Imports settings definitions from exported JSON records list.
        """
        count = 0
        for data in configs_list:
            key = data.get('key')
            if not key:
                continue

            value_str = data.get('value', '')
            config_type = data.get('config_type', 'string')
            category = data.get('category', 'Platform')
            rules = data.get('validation_rules', {})

            cls.update_setting(
                key=key,
                value_str=value_str,
                modified_by=modified_by,
                category=category,
                config_type=config_type,
                validation_rules=rules
            )
            count += 1
        return count
