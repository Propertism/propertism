"""
chat/tests_m28.py — M2.8 Navigation and Action Services Framework Test Suite.
Tests: sequential model IDs, parameter resolver, validation constraints,
       dispatcher execution, confirmation workflow, click REST API endpoints,
       and performance CTR metrics/diagnostics logs.

Run with:
    .\\scripts\\django.cmd test chat.tests_m28
"""
import json
import uuid
from django.test import TestCase
from chat.models import ActionDefinition, ActionExecutionLog, RealBotSession
from chat.navigation_services import ActionDispatcher, ParameterResolver, ActionValidator


# ─────────────────────────────────────────────────────────────────────────────
# 1. Model & Registry Tests
# ─────────────────────────────────────────────────────────────────────────────

class ActionModelTests(TestCase):

    def test_action_id_auto_generated_sequentially(self):
        act1 = ActionDefinition.objects.create(
            action_name='action_one', category='Internal', action_type='internal_nav'
        )
        act2 = ActionDefinition.objects.create(
            action_name='action_two', category='Internal', action_type='internal_nav'
        )
        self.assertEqual(act1.action_id, 'ACT000001')
        self.assertEqual(act2.action_id, 'ACT000002')

    def test_log_id_auto_generated_sequentially(self):
        session = RealBotSession.objects.create(session_id=uuid.uuid4())
        log1 = ActionExecutionLog.objects.create(
            session=session, action_id='ACT000001', action_name='action_one'
        )
        log2 = ActionExecutionLog.objects.create(
            session=session, action_id='ACT000001', action_name='action_one'
        )
        self.assertEqual(log1.log_id, 'ACL000001')
        self.assertEqual(log2.log_id, 'ACL000002')


# ─────────────────────────────────────────────────────────────────────────────
# 2. Parameter Resolver & Validation Tests
# ─────────────────────────────────────────────────────────────────────────────

class ActionResolverAndValidatorTests(TestCase):

    def setUp(self):
        self.resolver = ParameterResolver()
        self.validator = ActionValidator()

    def test_parameter_resolver_replaces_correctly(self):
        url = "/properties/{property_id}/documents/{doc_type}/"
        params = {'property_id': '104', 'doc_type': 'sale_deed', 'extra': 'ignore'}
        res = self.resolver.resolve(url, params)
        self.assertEqual(res, "/properties/104/documents/sale_deed/")

    def test_validator_fails_when_action_inactive(self):
        act = ActionDefinition.objects.create(
            action_name='test_inactive', category='Internal', action_type='internal_nav',
            status='inactive'
        )
        errors = self.validator.validate(act, {})
        self.assertIn("is currently inactive", errors[0])

    def test_validator_fails_when_required_parameter_missing(self):
        act = ActionDefinition.objects.create(
            action_name='test_params', category='Internal', action_type='internal_nav',
            supported_parameters=['property_id', 'user_id']
        )
        errors = self.validator.validate(act, {'property_id': '123'})
        self.assertEqual(len(errors), 1)
        self.assertIn("Required parameter 'user_id' is missing", errors[0])

    def test_validator_fails_when_internal_nav_does_not_start_with_slash(self):
        act = ActionDefinition.objects.create(
            action_name='test_internal', category='Internal', action_type='internal_nav',
            target_url='some-relative-page'
        )
        errors = self.validator.validate(act, {})
        self.assertIn("must start with a forward slash", errors[0])


# ─────────────────────────────────────────────────────────────────────────────
# 3. Action Dispatcher & Pluggable Providers Tests
# ─────────────────────────────────────────────────────────────────────────────

class ActionDispatcherTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.dispatcher = ActionDispatcher()

        # Seed test actions
        self.act_home = ActionDefinition.objects.create(
            action_name='nav_home', category='Internal', action_type='internal_nav',
            display_name='Home Page', target_url='/'
        )
        self.act_detail = ActionDefinition.objects.create(
            action_name='nav_detail', category='Internal', action_type='internal_nav',
            display_name='Property Detail', target_url='/properties/{property_id}/',
            supported_parameters=['property_id']
        )
        self.act_wa = ActionDefinition.objects.create(
            action_name='whatsapp_contact', category='Communication', action_type='whatsapp',
            display_name='WhatsApp Support', target_url='https://wa.me/918667020798',
            confirmation_required=True
        )

    def test_dispatch_simple_internal_action(self):
        res = self.dispatcher.dispatch_action('nav_home', session_id=str(self.session.session_id))
        self.assertTrue(res['success'])
        self.assertFalse(res['requires_confirmation'])
        self.assertEqual(res['payload']['url'], '/')
        self.assertEqual(res['payload']['type'], 'navigation')
        
        # Verify log entry created
        log = ActionExecutionLog.objects.filter(action_id=self.act_home.action_id).first()
        self.assertIsNotNone(log)
        self.assertTrue(log.is_validated)
        self.assertTrue(log.is_confirmed)

    def test_dispatch_parameterized_action(self):
        res = self.dispatcher.dispatch_action(
            'nav_detail',
            session_id=str(self.session.session_id),
            parameters={'property_id': '450'}
        )
        self.assertTrue(res['success'])
        self.assertEqual(res['payload']['url'], '/properties/450/')

    def test_dispatch_missing_parameters_logged_as_validation_failure(self):
        res = self.dispatcher.dispatch_action('nav_detail', session_id=str(self.session.session_id))
        self.assertFalse(res['success'])
        self.assertIn("Validation failed", res['error'])

        # Verify validation failure logged
        log = ActionExecutionLog.objects.filter(action_id=self.act_detail.action_id).first()
        self.assertIsNotNone(log)
        self.assertFalse(log.is_validated)

    def test_dispatch_requires_confirmation_flow(self):
        # First attempt: bypass_confirm=False
        res = self.dispatcher.dispatch_action(
            'whatsapp_contact',
            session_id=str(self.session.session_id),
            bypass_confirm=False
        )
        self.assertTrue(res['success'])
        self.assertTrue(res['requires_confirmation'])
        self.assertIn("Yes, Proceed", res['metadata']['chips'])

        # Check execution log states pending confirmation
        log = ActionExecutionLog.objects.filter(action_id=self.act_wa.action_id).first()
        self.assertTrue(log.requires_confirmation)
        self.assertFalse(log.is_confirmed)

        # Second attempt: bypass_confirm=True (confirmed execution)
        res_confirmed = self.dispatcher.dispatch_action(
            'whatsapp_contact',
            session_id=str(self.session.session_id),
            bypass_confirm=True
        )
        self.assertTrue(res_confirmed['success'])
        self.assertFalse(res_confirmed['requires_confirmation'])
        self.assertEqual(res_confirmed['payload']['url'], 'https://wa.me/918667020798')

        # Check execution log states completed
        log_confirmed = ActionExecutionLog.objects.filter(action_id=self.act_wa.action_id).order_by('-created_at').first()
        self.assertTrue(log_confirmed.is_confirmed)


# ─────────────────────────────────────────────────────────────────────────────
# 4. REST API & Analytics Integration Tests
# ─────────────────────────────────────────────────────────────────────────────

class ActionAPIEndpointTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.act = ActionDefinition.objects.create(
            action_name='open_patta', category='GovernmentServices', action_type='external_nav',
            display_name='Patta Online', target_url='https://eservices.tn.gov.in/',
            confirmation_required=True
        )

    def _post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def test_action_execute_endpoint_success_unconfirmed(self):
        url = '/api/v1/realbot/inquiry/action/execute/'
        payload = {
            'action_name': 'open_patta',
            'session_id': str(self.session.session_id),
            'confirm': False
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['data']['requires_confirmation'])

    def test_action_execute_endpoint_success_confirmed(self):
        url = '/api/v1/realbot/inquiry/action/execute/'
        payload = {
            'action_id': self.act.action_id,
            'session_id': str(self.session.session_id),
            'confirm': True
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertFalse(data['data']['requires_confirmation'])
        self.assertEqual(data['data']['payload']['url'], 'https://eservices.tn.gov.in/')

    def test_action_analytics_endpoint(self):
        # Log 2 runs
        ActionExecutionLog.objects.create(
            session=self.session, action_id=self.act.action_id, action_name=self.act.action_name,
            is_validated=True, requires_confirmation=True, is_confirmed=False
        )
        ActionExecutionLog.objects.create(
            session=self.session, action_id=self.act.action_id, action_name=self.act.action_name,
            is_validated=True, requires_confirmation=True, is_confirmed=True
        )

        url = '/api/v1/realbot/inquiry/action/analytics/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])

        # Verify summary stats
        overall = data['data']['overall']
        self.assertEqual(overall['total_executions'], 2)
        self.assertEqual(overall['validated_executions'], 2)
        self.assertEqual(overall['confirmed_executions'], 1)
        self.assertEqual(overall['pending_confirmation'], 1)

        # Verify action breakdowns
        by_action = data['data']['by_action'][0]
        self.assertEqual(by_action['action_id'], self.act.action_id)
        self.assertEqual(by_action['total_executions'], 2)
        self.assertEqual(by_action['validated'], 2)
        self.assertEqual(by_action['confirmed'], 1)
