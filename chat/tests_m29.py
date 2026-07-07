"""
chat/tests_m29.py — M2.9 Rich Response Framework Test Suite.
Tests: sequential model IDs, template resolution, schema validation constraints,
       priority composition, click REST API endpoints, and composition analytics.

Run with:
    .\\scripts\\django.cmd test chat.tests_m29
"""
import json
import uuid
from django.test import TestCase
from chat.models import ResponseComponent, ResponseCompositionLog, RealBotSession
from chat.response_framework import ResponseBuilder, ResponseValidator, ResponseTemplateEngine, ResponseCompositionEngine


# ─────────────────────────────────────────────────────────────────────────────
# 1. Model & Registry Tests
# ─────────────────────────────────────────────────────────────────────────────

class ResponseModelTests(TestCase):

    def test_component_id_auto_generated_sequentially(self):
        c1 = ResponseComponent.objects.create(
            name='comp_one', component_type='text'
        )
        c2 = ResponseComponent.objects.create(
            name='comp_two', component_type='text'
        )
        self.assertEqual(c1.component_id, 'RSP000001')
        self.assertEqual(c2.component_id, 'RSP000002')

    def test_log_id_auto_generated_sequentially(self):
        session = RealBotSession.objects.create(session_id=uuid.uuid4())
        log1 = ResponseCompositionLog.objects.create(
            session=session, composition=[]
        )
        log2 = ResponseCompositionLog.objects.create(
            session=session, composition=[]
        )
        self.assertEqual(log1.log_id, 'RSL000001')
        self.assertEqual(log2.log_id, 'RSL000002')


# ─────────────────────────────────────────────────────────────────────────────
# 2. Schema Validation & Template Resolution Tests
# ─────────────────────────────────────────────────────────────────────────────

class ResponseValidationAndTemplateTests(TestCase):

    def setUp(self):
        self.validator = ResponseValidator()
        self.template_engine = ResponseTemplateEngine()

    def test_template_resolves_brackets(self):
        template = "Title: {title}\nValue: {value}"
        params = {'title': 'My FAQ', 'value': 'Apply Patta'}
        res = self.template_engine.resolve(template, params)
        self.assertEqual(res, "Title: My FAQ\nValue: Apply Patta")

    def test_template_resolves_lists_comma_separated(self):
        template = "Options: {options}"
        params = {'options': ['One', 'Two', 'Three']}
        res = self.template_engine.resolve(template, params)
        self.assertEqual(res, "Options: One, Two, Three")

    def test_validator_fails_when_field_missing(self):
        comp = ResponseComponent.objects.create(
            name='test_fields', component_type='card',
            data_schema=['phone', 'email']
        )
        errors = self.validator.validate(comp, {'phone': '12345'})
        self.assertEqual(len(errors), 1)
        self.assertIn("Missing required data field 'email'", errors[0])

    def test_validator_fails_when_inactive(self):
        comp = ResponseComponent.objects.create(
            name='test_inactive', component_type='text', status='inactive'
        )
        errors = self.validator.validate(comp, {})
        self.assertIn("is currently inactive", errors[0])


# ─────────────────────────────────────────────────────────────────────────────
# 3. Composition Engine Tests
# ─────────────────────────────────────────────────────────────────────────────

class ResponseCompositionTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.builder = ResponseBuilder()

        # Seed registry
        self.c_text = ResponseComponent.objects.create(
            name='plain_text', component_type='text',
            display_template='{text}', data_schema=['text'],
            rendering_priority=5
        )
        self.c_chips = ResponseComponent.objects.create(
            name='suggestion_chips', component_type='chips',
            display_template='Options: {chips}', data_schema=['chips'],
            rendering_priority=50
        )
        self.c_error = ResponseComponent.objects.create(
            name='error_card', component_type='alert',
            display_template='Error: {error_message}', data_schema=['error_message'],
            rendering_priority=1
        )

    def test_composition_priority_ordering(self):
        # We request them out of order: chips first, then text, then error
        requested = [
            {'name': 'suggestion_chips', 'parameters': {'chips': ['Buy', 'Sell']}},
            {'name': 'plain_text', 'parameters': {'text': 'Hello world'}},
            {'name': 'error_card', 'parameters': {'error_message': 'Required parameter missing'}}
        ]

        res = self.builder.build_composed_response(requested, session_id=str(self.session.session_id))
        self.assertTrue(res['success'])

        # Composed text should order: error (priority 1) -> text (priority 5) -> chips (priority 50)
        expected_text = (
            "Error: Required parameter missing\n\n"
            "Hello world\n\n"
            "Options: Buy, Sell"
        )
        self.assertEqual(res['text'], expected_text)

        # Log check
        log = ResponseCompositionLog.objects.filter(session=self.session).first()
        self.assertIsNotNone(log)
        self.assertTrue(log.is_validated)

    def test_composition_fails_validation_and_logs(self):
        # Missing 'text' key inside plain_text component
        requested = [
            {'name': 'plain_text', 'parameters': {}}
        ]
        res = self.builder.build_composed_response(requested, session_id=str(self.session.session_id))
        self.assertFalse(res['success'])
        self.assertIn("Missing required data field 'text'", res['errors'][0])

        log = ResponseCompositionLog.objects.filter(session=self.session).first()
        self.assertIsNotNone(log)
        self.assertFalse(log.is_validated)


# ─────────────────────────────────────────────────────────────────────────────
# 4. REST API & Analytics Integration Tests
# ─────────────────────────────────────────────────────────────────────────────

class ResponseAPIEndpointTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.comp = ResponseComponent.objects.create(
            name='info_card', component_type='alert',
            display_template='Info: {info_message}', data_schema=['info_message'],
            rendering_priority=4
        )

    def _post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def test_list_components_endpoint(self):
        url = '/api/v1/realbot/inquiry/response/components/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data'][0]['name'], 'info_card')

    def test_compose_endpoint_success(self):
        url = '/api/v1/realbot/inquiry/response/compose/'
        payload = {
            'session_id': str(self.session.session_id),
            'components': [
                {'name': 'info_card', 'parameters': {'info_message': 'System Upgrade Scheduled'}}
            ]
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['text'], 'Info: System Upgrade Scheduled')
        self.assertEqual(data['data']['rich_components'][0]['name'], 'info_card')

    def test_compose_endpoint_validation_failure(self):
        url = '/api/v1/realbot/inquiry/response/compose/'
        payload = {
            'session_id': str(self.session.session_id),
            'components': [
                {'name': 'info_card', 'parameters': {}}
            ]
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.content)
        self.assertFalse(data['success'])
        self.assertIn("Composition validation failed", data['error']['message'])

    def test_response_analytics_endpoint(self):
        # 1 valid, 1 invalid composition logs
        ResponseCompositionLog.objects.create(
            session=self.session, composition=[], is_validated=True
        )
        ResponseCompositionLog.objects.create(
            session=self.session, composition=[], is_validated=False
        )

        url = '/api/v1/realbot/inquiry/response/analytics/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])

        overall = data['data']['overall']
        self.assertEqual(overall['total_compositions'], 2)
        self.assertEqual(overall['valid_compositions'], 1)
        self.assertEqual(overall['invalid_compositions'], 1)
        self.assertEqual(overall['success_rate_percentage'], 50.0)
