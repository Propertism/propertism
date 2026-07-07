"""
chat/tests_m210.py — M2.10 Conversation Memory & Context Management Test Suite.
Tests: sequential model IDs, variable schema type checks, expiration TTL policy,
       topic switching stack pops, API views, and analytics aggregation.

Run with:
    .\\scripts\\django.cmd test chat.tests_m210
"""
import json
import time
import uuid
from django.test import TestCase
from chat.models import ConversationContext, ContextUpdateLog, RealBotSession
from chat.context_manager import ConversationContextManager, TopicManager, ContextResolutionEngine, ContextValidator


# ─────────────────────────────────────────────────────────────────────────────
# 1. Model & Registry Tests
# ─────────────────────────────────────────────────────────────────────────────

class ContextModelTests(TestCase):

    def test_context_id_auto_generated_sequentially(self):
        s1 = RealBotSession.objects.create(session_id=uuid.uuid4())
        s2 = RealBotSession.objects.create(session_id=uuid.uuid4())
        
        c1 = ConversationContext.objects.create(session=s1)
        c2 = ConversationContext.objects.create(session=s2)
        
        self.assertEqual(c1.context_id, 'CTX000001')
        self.assertEqual(c2.context_id, 'CTX000002')

    def test_log_id_auto_generated_sequentially(self):
        s = RealBotSession.objects.create(session_id=uuid.uuid4())
        c = ConversationContext.objects.create(session=s)
        
        l1 = ContextUpdateLog.objects.create(context=c, action='updated')
        l2 = ContextUpdateLog.objects.create(context=c, action='topic_switch')
        
        self.assertEqual(l1.log_id, 'CTL000001')
        self.assertEqual(l2.log_id, 'CTL000002')


# ─────────────────────────────────────────────────────────────────────────────
# 2. Variable Framework & Expiration Tests
# ─────────────────────────────────────────────────────────────────────────────

class ContextVariableTests(TestCase):

    def setUp(self):
        self.mgr = ConversationContextManager()
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.context = self.mgr.get_or_create_context(self.session.session_id)

    def test_variable_type_validation_success(self):
        variables = {
            'username': {'value': 'Vijay', 'type': 'str'},
            'age': {'value': 30, 'type': 'int'},
            'is_nri': {'value': True, 'type': 'bool'},
            'interests': {'value': ['Patta', 'GCC Tax'], 'type': 'list'}
        }
        errors = self.mgr.update_variables(self.context, variables)
        self.assertEqual(len(errors), 0)

        # Retrieve check
        self.assertEqual(self.mgr.get_variable(self.context, 'username'), 'Vijay')
        self.assertEqual(self.mgr.get_variable(self.context, 'age'), 30)
        self.assertEqual(self.mgr.get_variable(self.context, 'is_nri'), True)

    def test_variable_type_validation_failure(self):
        # Age expects int, passing string
        variables = {
            'age': {'value': 'thirty', 'type': 'int'}
        }
        errors = self.mgr.update_variables(self.context, variables)
        self.assertEqual(len(errors), 1)
        self.assertIn("Type validation failed for key 'age'", errors[0])

    def test_expiration_policy(self):
        # Store variable with 1 second TTL
        variables = {
            'temp_code': {'value': 'XYZ123', 'type': 'str', 'ttl': 1}
        }
        self.mgr.update_variables(self.context, variables)
        
        # Verify it exists initially
        self.assertEqual(self.mgr.get_variable(self.context, 'temp_code'), 'XYZ123')
        
        # Wait for expiration
        time.sleep(2)
        
        # Retrieve check (should be gone)
        val = self.mgr.get_variable(self.context, 'temp_code')
        self.assertIsNone(val)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Topic Switch & Stack Restoration Tests
# ─────────────────────────────────────────────────────────────────────────────

class TopicSwitchTests(TestCase):

    def setUp(self):
        self.mgr = ConversationContextManager()
        self.topic_mgr = TopicManager()
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.context = self.mgr.get_or_create_context(self.session.session_id)

    def test_topic_switches_and_restores_correctly(self):
        # Set initial topic
        self.context.current_topic = 'welcome'
        self.context.save()

        # Switch to topic: inquiry
        self.topic_mgr.switch_topic(self.context, 'inquiry')
        self.assertEqual(self.context.current_topic, 'inquiry')
        self.assertEqual(self.context.previous_topic, 'welcome')

        # Switch to side topic: pricing
        self.topic_mgr.switch_topic(self.context, 'pricing')
        self.assertEqual(self.context.current_topic, 'pricing')
        self.assertEqual(self.context.previous_topic, 'inquiry')

        # Pop pricing to restore inquiry
        restored = self.topic_mgr.restore_previous_topic(self.context)
        self.assertEqual(restored, 'inquiry')
        self.assertEqual(self.context.current_topic, 'inquiry')

        # Pop inquiry to restore welcome
        restored = self.topic_mgr.restore_previous_topic(self.context)
        self.assertEqual(restored, 'welcome')
        self.assertEqual(self.context.current_topic, 'welcome')


# ─────────────────────────────────────────────────────────────────────────────
# 4. REST API & Analytics Tests
# ─────────────────────────────────────────────────────────────────────────────

class ContextAPIEndpointTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())

    def _post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def test_get_context_endpoint(self):
        url = f'/api/v1/realbot/inquiry/context/get/?session_id={self.session.session_id}'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['conversation_state'], 'idle')

    def test_update_context_endpoint(self):
        url = '/api/v1/realbot/inquiry/context/update/'
        payload = {
            'session_id': str(self.session.session_id),
            'intent': 'explore_services',
            'service': 'property_management',
            'variables': {
                'city': {'value': 'Chennai', 'type': 'str'}
            }
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        
        snapshot = data['data']
        self.assertEqual(snapshot['active_intent'], 'explore_services')
        self.assertEqual(snapshot['active_service'], 'property_management')
        self.assertEqual(snapshot['variables']['city'], 'Chennai')

    def test_switch_topic_endpoint(self):
        # 1. Switch
        url = '/api/v1/realbot/inquiry/context/switch-topic/'
        payload = {
            'session_id': str(self.session.session_id),
            'new_topic': 'patta_documents'
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['current_topic'], 'patta_documents')

        # 2. Restore
        payload = {
            'session_id': str(self.session.session_id),
            'restore': True
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['current_topic'], '')

    def test_analytics_endpoint(self):
        # Populate context and update logs
        mgr = ConversationContextManager()
        context = mgr.get_or_create_context(self.session.session_id)
        context.active_intent = 'buy_property'
        context.save()

        ContextUpdateLog.objects.create(context=context, action='topic_switch')

        url = '/api/v1/realbot/inquiry/context/analytics/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])

        overall = data['data']['overall']
        self.assertEqual(overall['total_contexts'], 1)
        self.assertEqual(overall['total_topic_switches'], 1)
        self.assertEqual(data['data']['intents_breakdown']['buy_property'], 1)
