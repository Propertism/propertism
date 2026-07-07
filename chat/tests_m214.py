"""
chat/tests_m214.py — M2.14 Security, Authorization & Platform Governance Test Suite.
Tests: sequential model IDs, input sanitization, request validation, rate limiting,
       abuse detection, authorization evaluations, REST APIs, and orchestrator integration.

Run with:
    .\\scripts\\django.cmd test chat.tests_m214
"""
import json
import uuid
import time
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from chat.models import SecurityEvent, SecurityPolicy, RealBotSession
from chat.security_manager import SecurityManager, SecurityPolicyEngine, RateLimiter, AbuseDetector
from chat.orchestrator import ConversationOrchestrator


class SecurityModelTests(TestCase):

    def test_security_event_id_sequential(self):
        e1 = SecurityEvent.objects.create(event_type='session_started', severity='info')
        e2 = SecurityEvent.objects.create(event_type='invalid_request', severity='warning')
        self.assertEqual(e1.event_id, 'SEC000001')
        self.assertEqual(e2.event_id, 'SEC000002')

    def test_security_policy_id_sequential(self):
        p1 = SecurityPolicy.objects.create(policy_key='max_request_length', domain='request', policy_type='limit', value='5000')
        p2 = SecurityPolicy.objects.create(policy_key='blocked_action_types', domain='action', policy_type='rule', value='external')
        self.assertEqual(p1.policy_id, 'SPL000001')
        self.assertEqual(p2.policy_id, 'SPL000002')


class InputSanitizerTests(TestCase):

    def setUp(self):
        self.manager = SecurityManager()

    def test_sanitize_clean_input(self):
        text = "Hello, I want to query property details."
        sanitized, has_threats, threats = self.manager.input_sanitizer.sanitize(text)
        self.assertEqual(sanitized, text)
        self.assertFalse(has_threats)
        self.assertEqual(len(threats), 0)

    def test_sanitize_html_stripping(self):
        text = "<p>Hello <b>World</b>!</p>"
        sanitized, has_threats, threats = self.manager.input_sanitizer.sanitize(text)
        self.assertEqual(sanitized, "Hello World!")
        self.assertFalse(has_threats)

    def test_script_injection_detection(self):
        text = "<script>alert('hack');</script>"
        sanitized, has_threats, threats = self.manager.input_sanitizer.sanitize(text)
        self.assertTrue(has_threats)
        self.assertTrue(any("Script injection" in t for t in threats))

    def test_sql_injection_detection(self):
        text = "1'; DROP TABLE chat_securityevent; --"
        sanitized, has_threats, threats = self.manager.input_sanitizer.sanitize(text)
        self.assertTrue(has_threats)
        self.assertTrue(any("SQL injection" in t for t in threats))

    def test_dangerous_url_scheme_detection(self):
        text = "Click javascript:alert('xss')"
        sanitized, has_threats, threats = self.manager.input_sanitizer.sanitize(text)
        self.assertTrue(has_threats)
        self.assertTrue(any("Dangerous URL scheme" in t for t in threats))


class RequestValidatorTests(TestCase):

    def setUp(self):
        self.manager = SecurityManager()
        SecurityPolicyEngine.clear_cache()
        # Seed policy
        SecurityPolicy.objects.create(
            policy_key='max_request_length',
            domain='request',
            policy_type='limit',
            value='20'
        )
        SecurityPolicyEngine.load_policies()

    def test_request_validation_length_exceeded(self):
        payload = {
            'session_id': 'sess_123',
            'message_text': 'This message is longer than twenty characters.'
        }
        is_valid, violations = self.manager.request_validator.validate(payload)
        self.assertFalse(is_valid)
        self.assertTrue(any("exceeds maximum length" in v for v in violations))

    def test_request_validation_missing_fields(self):
        payload = {
            'session_id': '',
            'message_text': ''
        }
        is_valid, violations = self.manager.request_validator.validate(payload)
        self.assertFalse(is_valid)
        self.assertTrue(any("Message text is required" in v for v in violations))
        self.assertTrue(any("Session ID is required" in v for v in violations))


class RateLimiterTests(TestCase):

    def setUp(self):
        RateLimiter.reset()
        SecurityPolicyEngine.clear_cache()
        SecurityPolicy.objects.create(
            policy_key='rate_limit_requests_per_minute',
            domain='api',
            policy_type='limit',
            value='3'
        )
        SecurityPolicyEngine.load_policies()

    def test_rate_limiting_triggers(self):
        session_id = 'test_rate_sess'
        
        # First 3 requests allowed
        for _ in range(3):
            allowed, count = RateLimiter.check_rate(session_id)
            self.assertTrue(allowed)
            
        # 4th request rate limited
        allowed, count = RateLimiter.check_rate(session_id)
        self.assertFalse(allowed)


class AbuseDetectorTests(TestCase):

    def setUp(self):
        AbuseDetector.reset()
        SecurityPolicyEngine.clear_cache()
        SecurityPolicy.objects.create(
            policy_key='abuse_duplicate_threshold',
            domain='input',
            policy_type='threshold',
            value='3'
        )
        SecurityPolicy.objects.create(
            policy_key='abuse_burst_threshold',
            domain='input',
            policy_type='threshold',
            value='5'
        )
        SecurityPolicy.objects.create(
            policy_key='abuse_burst_window_seconds',
            domain='input',
            policy_type='threshold',
            value='5'
        )
        SecurityPolicyEngine.load_policies()

    def test_abuse_duplicate_detection(self):
        session_id = 'abuse_sess'
        text = "Spam message"
        
        # Send 2 times
        is_abusive, reason = AbuseDetector.check_abuse(session_id, text)
        self.assertFalse(is_abusive)
        is_abusive, reason = AbuseDetector.check_abuse(session_id, text)
        self.assertFalse(is_abusive)
        
        # 3rd time duplicate trigger
        is_abusive, reason = AbuseDetector.check_abuse(session_id, text)
        self.assertTrue(is_abusive)
        self.assertIn("Repeated identical message", reason)


class AuthorizationManagerTests(TestCase):

    def setUp(self):
        SecurityPolicyEngine.clear_cache()
        SecurityPolicy.objects.create(
            policy_key='blocked_action_types',
            domain='action',
            policy_type='rule',
            value='external_redirect,delete_user'
        )
        SecurityPolicy.objects.create(
            policy_key='restricted_navigation_paths',
            domain='navigation',
            policy_type='rule',
            value='/admin/settings/,/admin/db/'
        )
        SecurityPolicyEngine.load_policies()
        self.manager = SecurityManager()

    def test_authorize_blocked_action(self):
        res = self.manager.authorize('delete_user')
        self.assertFalse(res['is_authorized'])
        self.assertIn("blocked by security policy", res['reason'])

    def test_authorize_restricted_navigation(self):
        res = self.manager.authorize('navigation', {'target_path': '/admin/db/'})
        self.assertFalse(res['is_authorized'])
        self.assertIn("restricted by security policy", res['reason'])

    def test_authorize_valid_action(self):
        res = self.manager.authorize('navigation', {'target_path': '/home/'})
        self.assertTrue(res['is_authorized'])


class OutputValidatorTests(TestCase):

    def setUp(self):
        self.manager = SecurityManager()

    def test_output_validation_detects_traceback(self):
        payload = {
            'reply_text': "Error occurred: Traceback (most recent call last):\nFile 'views.py', line 12",
            'cards': []
        }
        res = self.manager.validate_output(payload)
        self.assertFalse(res['is_safe'])
        self.assertTrue(any("Internal data leak" in issue for issue in res['issues']))


class SecurityAPIEndpointTests(TestCase):

    def setUp(self):
        SecurityPolicyEngine.clear_cache()
        SecurityPolicy.objects.create(
            policy_key='max_request_length',
            domain='request',
            policy_type='limit',
            value='100'
        )
        SecurityPolicyEngine.load_policies()
        SecurityEvent.objects.create(event_type='session_started', severity='info')

    def test_events_endpoint(self):
        url = reverse('chat:security_events_view')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']['events']), 1)

    def test_policies_endpoint(self):
        url = reverse('chat:security_policies_view')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']['policies']), 1)

    def test_validate_endpoint_valid(self):
        url = reverse('chat:security_validate_view')
        payload = {
            'session_id': 'sess_val',
            'message_text': 'Valid query text'
        }
        res = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['data']['is_valid'])

    def test_validate_endpoint_invalid(self):
        url = reverse('chat:security_validate_view')
        payload = {
            'session_id': '',
            'message_text': ''
        }
        res = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertFalse(data['data']['is_valid'])

    def test_analytics_endpoint(self):
        url = reverse('chat:security_analytics_view')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['total_security_events'], 1)

    def test_governance_endpoint(self):
        url = reverse('chat:security_governance_view')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['compliance_status'], "Compliant")


class OrchestratorSecurityIntegrationTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.orch = ConversationOrchestrator()
        SecurityPolicyEngine.clear_cache()
        SecurityPolicy.objects.create(
            policy_key='max_request_length',
            domain='request',
            policy_type='limit',
            value='50'
        )
        SecurityPolicyEngine.load_policies()

    def test_orchestrator_runs_security_and_output_validation_stages(self):
        # Normal process flow runs both stages
        res = self.orch.process_message(
            session_id=str(self.session.session_id),
            message_text="Help request"
        )
        self.assertEqual(res['state'], 'Completed')
        
        # Retrieve trace steps
        from chat.models import WorkflowExecutionStep
        steps = WorkflowExecutionStep.objects.filter(workflow__workflow_id=res['workflow_id']).order_by('created_at')
        self.assertEqual(steps.count(), 15)
        self.assertEqual(steps[0].stage, 'Security Validation')
        self.assertEqual(steps[11].stage, 'Output Validation')

    def test_orchestrator_scrubs_dangerous_output(self):
        # We mock response composition to return a leak/traceback and verify Output Validation stage handles it
        with patch('chat.orchestrator.ConversationOrchestrator._stage_response_composition') as mock_comp:
            def compose_leak(ctx):
                ctx['reply_text'] = "Traceback (most recent call last):\nFile '/app/views.py', line 5"
            mock_comp.side_effect = compose_leak
            
            res = self.orch.process_message(
                session_id=str(self.session.session_id),
                message_text="Trigger compose"
            )
            # The reply should be scrubbed
            self.assertEqual(res['state'], 'Completed')
            self.assertEqual(res['reply_text'], "I'm here to help with Tamil Nadu property consulting. How can I assist you?")
            
            # An audit event for security exception should be registered
            sec_event = SecurityEvent.objects.filter(event_type='security_exception').first()
            self.assertIsNotNone(sec_event)
            self.assertEqual(sec_event.severity, 'critical')
