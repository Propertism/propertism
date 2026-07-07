"""
chat/tests_m212.py — M2.12 Administration & Configuration Management Test Suite.
Tests: sequential model IDs, config validator parsing constraints, cache operations,
       rollback details, imports/exports, and REST API views.

Run with:
    .\\scripts\\django.cmd test chat.tests_m212
"""
import json
from django.test import TestCase
from chat.models import ConfigurationItem, ConfigurationAuditLog
from chat.config_manager import ConfigurationManager, ConfigurationCacheManager, ConfigurationValidator


# ─────────────────────────────────────────────────────────────────────────────
# 1. Model & Registry Tests
# ─────────────────────────────────────────────────────────────────────────────

class ConfigurationModelTests(TestCase):

    def test_config_id_auto_generated_sequentially(self):
        c1 = ConfigurationItem.objects.create(key='test_cfg1', category='Platform', config_type='string', value='val1')
        c2 = ConfigurationItem.objects.create(key='test_cfg2', category='Platform', config_type='string', value='val2')
        self.assertEqual(c1.config_id, 'CFG000001')
        self.assertEqual(c2.config_id, 'CFG000002')

    def test_audit_id_auto_generated_sequentially(self):
        item = ConfigurationItem.objects.create(key='test_cfg', category='Platform', config_type='string', value='val')
        a1 = ConfigurationAuditLog.objects.create(config_item=item, action='created', new_value='val', version=1)
        a2 = ConfigurationAuditLog.objects.create(config_item=item, action='updated', new_value='val2', version=2)
        self.assertEqual(a1.audit_id, 'CFL000001')
        self.assertEqual(a2.audit_id, 'CFL000002')


# ─────────────────────────────────────────────────────────────────────────────
# 2. Config Validator & Cache Manager Tests
# ─────────────────────────────────────────────────────────────────────────────

class ConfigurationValidatorAndCacheTests(TestCase):

    def test_validator_parses_various_types(self):
        self.assertTrue(ConfigurationValidator.validate_and_parse('true', 'boolean'))
        self.assertFalse(ConfigurationValidator.validate_and_parse('0', 'boolean'))
        self.assertEqual(ConfigurationValidator.validate_and_parse('15', 'integer'), 15)
        self.assertEqual(ConfigurationValidator.validate_and_parse('3.14', 'float'), 3.14)
        self.assertEqual(ConfigurationValidator.validate_and_parse('{"k": "v"}', 'json'), {"k": "v"})

    def test_validator_enforces_boundaries_and_fails(self):
        # Numeric min check
        with self.assertRaises(ValueError):
            ConfigurationValidator.validate_and_parse('3', 'integer', {'min': 5})

        # Numeric max check
        with self.assertRaises(ValueError):
            ConfigurationValidator.validate_and_parse('25', 'integer', {'max': 10})

        # Choice string check
        with self.assertRaises(ValueError):
            ConfigurationValidator.validate_and_parse('invalid', 'string', {'choices': ['active', 'hidden']})

    def test_cache_manager_stores_and_populates(self):
        ConfigurationCacheManager.clear()
        ConfigurationCacheManager.set('test_key', 'cached_value')
        self.assertEqual(ConfigurationCacheManager.get('test_key'), 'cached_value')
        ConfigurationCacheManager.delete('test_key')
        self.assertIsNone(ConfigurationCacheManager.get('test_key'))


# ─────────────────────────────────────────────────────────────────────────────
# 3. Central Configuration Manager Tests
# ─────────────────────────────────────────────────────────────────────────────

class ConfigurationManagerEngineTests(TestCase):

    def setUp(self):
        ConfigurationCacheManager.clear()

    def test_get_setting_resolves_and_caches(self):
        ConfigurationItem.objects.create(
            key='session_ttl', category='Platform',
            config_type='integer', value='30'
        )
        val = ConfigurationManager.get_setting('session_ttl')
        self.assertEqual(val, 30)

        # Check in memory cache
        cached = ConfigurationCacheManager.get('session_ttl')
        self.assertEqual(cached, 30)

    def test_update_setting_creates_audit_log(self):
        ConfigurationManager.update_setting('max_chips', '5', category='Platform', config_type='integer')
        item = ConfigurationItem.objects.get(key='max_chips')
        self.assertEqual(item.value, '5')
        self.assertEqual(item.version, 1)

        # Update again
        ConfigurationManager.update_setting('max_chips', '7')
        item.refresh_from_db()
        self.assertEqual(item.value, '7')
        self.assertEqual(item.version, 2)

        # Audit check
        logs = ConfigurationAuditLog.objects.filter(config_item=item)
        self.assertEqual(logs.count(), 2)

    def test_rollback_setting_reverts_values(self):
        ConfigurationManager.update_setting('mode', 'test', category='Platform', config_type='string')
        ConfigurationManager.update_setting('mode', 'live')
        
        # Rollback to V1
        item = ConfigurationManager.rollback_setting('mode', 1)
        self.assertEqual(item.value, 'test')
        self.assertEqual(item.version, 3)

    def test_import_and_export_framework(self):
        configs = [
            {
                'key': 'nri_mode', 'value': 'true',
                'config_type': 'boolean', 'category': 'Platform'
            }
        ]
        imported = ConfigurationManager.import_configurations(configs)
        self.assertEqual(imported, 1)

        val = ConfigurationManager.get_setting('nri_mode')
        self.assertTrue(val)

        exported = ConfigurationManager.export_configurations()
        self.assertTrue(any(e['key'] == 'nri_mode' for e in exported))


# ─────────────────────────────────────────────────────────────────────────────
# 4. REST API Endpoint Tests
# ─────────────────────────────────────────────────────────────────────────────

class ConfigurationAPIEndpointTests(TestCase):

    def setUp(self):
        ConfigurationCacheManager.clear()

    def _post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def test_get_setting_endpoint(self):
        ConfigurationItem.objects.create(
            key='welcome_msg', category='Platform',
            config_type='string', value='hello'
        )
        url = '/api/v1/realbot/inquiry/config/get/?key=welcome_msg'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['value'], 'hello')

    def test_update_setting_endpoint(self):
        url = '/api/v1/realbot/inquiry/config/update/'
        payload = {
            'key': 'history_limit',
            'value': 15,
            'modified_by': 'admin_test'
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['value'], '15')

    def test_rollback_setting_endpoint(self):
        # Seed and update
        ConfigurationManager.update_setting('temp_flag', 'false', category='Platform', config_type='boolean')
        ConfigurationManager.update_setting('temp_flag', 'true')

        url = '/api/v1/realbot/inquiry/config/rollback/'
        payload = {
            'key': 'temp_flag',
            'version': 1,
            'modified_by': 'rollback_tester'
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['value'], 'false')

    def test_audit_history_endpoint(self):
        ConfigurationManager.update_setting('audited_val', 'first', category='Platform', config_type='string')
        url = '/api/v1/realbot/inquiry/config/audit/?key=audited_val'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']['history']), 1)

    def test_export_import_endpoints(self):
        # 1. Export check
        url_export = '/api/v1/realbot/inquiry/config/export/'
        resp_export = self.client.get(url_export)
        self.assertEqual(resp_export.status_code, 200)
        data_export = json.loads(resp_export.content)
        self.assertTrue(data_export['success'])

        # 2. Import check
        url_import = '/api/v1/realbot/inquiry/config/import/'
        payload_import = [
            {
                'key': 'imported_key',
                'value': 'imported_val',
                'config_type': 'string',
                'category': 'Platform'
            }
        ]
        resp_import = self._post_json(url_import, payload_import)
        self.assertEqual(resp_import.status_code, 200)
        data_import = json.loads(resp_import.content)
        self.assertTrue(data_import['success'])
        self.assertEqual(data_import['data']['imported_count'], 1)
