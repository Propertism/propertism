"""
chat/tests_m24.py — M2.4 Rule Engine & Intent Routing Test Suite
Run with:
    .\\scripts\\django.cmd test chat.tests_m24
"""
import json
import uuid
from django.test import TestCase, override_settings
from chat.models import BusinessRule, RuleExecutionLog, RealBotMessage, RealBotSession
from chat.rule_engine import RuleEngine, RuleEvaluator, IntentResult
from chat.action_handlers import ActionDispatcher, ActionResponse


# ==============================================================================
# BusinessRule Model Tests
# ==============================================================================

class BusinessRuleModelTests(TestCase):

    def test_rule_id_auto_generation_format(self):
        """First BusinessRule should get RBR000001."""
        rule = BusinessRule.objects.create(
            name="Greeting",
            intent="greeting",
            action_type="greeting_response"
        )
        self.assertRegex(rule.rule_id, r'^RBR\d{6}$')
        self.assertEqual(rule.rule_id, "RBR000001")

    def test_rule_id_sequential_generation(self):
        """Consecutive BusinessRules get sequential RBR IDs."""
        r1 = BusinessRule.objects.create(name="R1", intent="greeting", action_type="greeting_response")
        r2 = BusinessRule.objects.create(name="R2", intent="goodbye", action_type="farewell_response")
        self.assertEqual(r1.rule_id, "RBR000001")
        self.assertEqual(r2.rule_id, "RBR000002")

    def test_rule_id_immutable(self):
        """Saving an existing rule does not regenerate or update rule_id."""
        rule = BusinessRule.objects.create(name="R1", intent="greeting", action_type="greeting_response")
        original_id = rule.rule_id
        rule.priority = 10
        rule.save()
        rule.refresh_from_db()
        self.assertEqual(rule.rule_id, original_id)

    def test_clean_keyword_lists(self):
        """get_positive_keyword_list returns clean, lowercase, trimmed items."""
        rule = BusinessRule.objects.create(
            name="R1", intent="greeting", action_type="greeting_response",
            positive_keywords=" Hello,  hi, Hey , Namaste ",
            negative_keywords="bye, goodbye ",
            phrase_patterns="good morning, good afternoon"
        )
        self.assertEqual(rule.get_positive_keyword_list(), ["hello", "hi", "hey", "namaste"])
        self.assertEqual(rule.get_negative_keyword_list(), ["bye", "goodbye"])
        self.assertEqual(rule.get_phrase_pattern_list(), ["good morning", "good afternoon"])


# ==============================================================================
# Rule Engine Scoring & Selection Tests
# ==============================================================================

class RuleEngineTests(TestCase):

    def setUp(self):
        # Seed test rules
        self.r_greet = BusinessRule.objects.create(
            name="Greet", intent="greeting", priority=1,
            positive_keywords="hello,hi,hey",
            min_confidence=0.3, action_type="greeting_response"
        )
        self.r_buy = BusinessRule.objects.create(
            name="Buy", intent="buy_property", priority=10,
            positive_keywords="buy,purchase,villa,house",
            negative_keywords="sell,rent",
            min_confidence=0.4, action_type="service_card"
        )
        self.r_sell = BusinessRule.objects.create(
            name="Sell", intent="sell_property", priority=11,
            positive_keywords="sell,dispose,sale",
            min_confidence=0.4, action_type="service_card"
        )
        self.r_fees = BusinessRule.objects.create(
            name="Fees", intent="fee_structure", priority=12,
            phrase_patterns="fee structure,service charge,how much do you charge",
            min_confidence=0.5, action_type="knowledge_response"
        )
        self.r_unknown = BusinessRule.objects.create(
            name="Fallback", intent="unknown_intent", priority=99,
            action_type="fallback_response"
        )

    def test_basic_keyword_scoring(self):
        """Matching keywords yields correct score and intent resolution."""
        engine = RuleEngine()
        result = engine.evaluate("Hello there, hi!")
        self.assertEqual(result.intent, "greeting")
        self.assertGreater(result.confidence, 0.0)
        self.assertEqual(result.outcome, "resolved")
        self.assertEqual(result.rule_id, self.r_greet.rule_id)

    def test_phrase_patterns_heavily_weighted(self):
        """Exact phrase matches score highly and trigger intent."""
        engine = RuleEngine()
        result = engine.evaluate("what is your fee structure?")
        self.assertEqual(result.intent, "fee_structure")
        self.assertEqual(result.outcome, "resolved")

    def test_negative_keywords_exclusion(self):
        """Exclusion keywords prevent rule matching by penalizing score."""
        engine = RuleEngine()
        # 'buy' matches positive but 'sell' is negative for r_buy
        result = engine.evaluate("I want to buy but first sell my flat")
        # Should not resolve to buy_property due to negative penalty
        self.assertNotEqual(result.intent, "buy_property")

    def test_priority_tie_breaking(self):
        """Higher priority (lower number) breaks ties between equal scores."""
        # Create a conflicting rule with same keywords but lower priority
        r_greet_low = BusinessRule.objects.create(
            name="Greet Low", intent="greeting", priority=5,
            positive_keywords="hello,hi,hey",
            min_confidence=0.3, action_type="greeting_response"
        )
        engine = RuleEngine()
        result = engine.evaluate("hello")
        self.assertEqual(result.rule_id, self.r_greet.rule_id)  # priority 1 wins over 5

    def test_clarification_threshold_logic(self):
        """Close scores within 0.15 trigger clarification workflow."""
        # Create two rules with identical keywords but different intents and priorities
        BusinessRule.objects.create(
            name="Rent A", intent="rental_income", priority=20,
            positive_keywords="rent,tenant", min_confidence=0.4, action_type="service_card"
        )
        BusinessRule.objects.create(
            name="Rent B", intent="property_search", priority=21,
            positive_keywords="rent,tenant", min_confidence=0.4, action_type="service_card"
        )
        engine = RuleEngine()
        result = engine.evaluate("rent a home")
        self.assertEqual(result.outcome, "clarification")
        self.assertEqual(result.intent, "unknown_intent")
        self.assertIn("candidates", result.action_config)
        self.assertEqual(len(result.action_config['candidates']), 2)

    def test_fallback_when_no_rules_match(self):
        """Unknown text falls back gracefully to unknown_intent."""
        engine = RuleEngine()
        result = engine.evaluate("xyzabcrandomtext")
        self.assertEqual(result.outcome, "fallback")
        self.assertEqual(result.intent, "unknown_intent")
        self.assertEqual(result.action_type, "fallback_response")


# ==============================================================================
# Action Dispatcher & Pluggable Handlers Tests
# ==============================================================================

class ActionDispatcherTests(TestCase):

    def test_greeting_response_format(self):
        result = IntentResult(
            intent="greeting", rule_id="RBR000001", confidence=1.0,
            action_type="greeting_response", action_config={"chips": ["A", "B"]},
            outcome="resolved"
        )
        response = ActionDispatcher().dispatch(result, "hello")
        self.assertIn("Welcome", response.text)
        self.assertEqual(response.metadata['chips'], ["A", "B"])

    def test_contact_card_format(self):
        result = IntentResult(
            intent="contact_information", rule_id="RBR000002", confidence=1.0,
            action_type="contact_card",
            action_config={"phone": "123456", "email": "a@b.com", "chips": ["Call"]},
            outcome="resolved"
        )
        response = ActionDispatcher().dispatch(result, "contact details")
        self.assertEqual(response.metadata['contact']['phone'], "123456")
        self.assertEqual(response.metadata['contact']['email'], "a@b.com")

    def test_whatsapp_url_encoding(self):
        result = IntentResult(
            intent="whatsapp", rule_id="RBR000003", confidence=1.0,
            action_type="whatsapp",
            action_config={"phone": "+91 86670 20798", "message": "Interest in buy"},
            outcome="resolved"
        )
        response = ActionDispatcher().dispatch(result, "whatsapp")
        url = response.metadata['action_trigger']['url']
        self.assertIn("wa.me/918667020798", url)
        self.assertIn("Interest%20in%20buy", url)


# ==============================================================================
# End-to-End Send Message & Admin API Tests
# ==============================================================================

@override_settings(
    REALBOT_INTEGRATION_ENABLED=True,
    REALBOT_BASE_URL='http://127.0.0.1:8010',
    REALBOT_API_KEY='test-key',
    REALBOT_TENANT='propertism',
    REALBOT_PRODUCT='propertism.in',
    REALBOT_DOMAIN='real_estate',
    REALBOT_WIDGET_URL='http://127.0.0.1:8010',
    REALBOT_ENVIRONMENT='test',
    REALBOT_API_VERSION='v1',
)
class SendMessageRuleEngineTests(TestCase):

    def setUp(self):
        # Create session
        self.session = RealBotSession.objects.create(
            session_id=uuid.uuid4()
        )
        # Seed basic greeting rule
        BusinessRule.objects.create(
            name="Greeting Rule", intent="greeting", priority=1,
            positive_keywords="hello,hi,hey", min_confidence=0.3,
            action_type="greeting_response", action_config={"chips": ["Buy", "Sell"]}
        )
        BusinessRule.objects.create(
            name="Fallback Rule", intent="unknown_intent", priority=99,
            action_type="fallback_response", action_config={"chips": ["Help"]}
        )

    def test_query_greeting_resolves_greeting_intent_with_chips(self):
        """POST to send_message with 'hello' triggers RuleEngine and returns GreetingResponse."""
        url = '/api/v1/realbot/query/'
        payload = {
            "session_id": str(self.session.session_id),
            "message": "hello there"
        }
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        msg = data['data']['message']
        self.assertIn("Welcome", msg['text'])
        self.assertEqual(msg['metadata']['chips'], ["Buy", "Sell"])
        
        # Verify metadata audit tracking
        rb_meta = msg['metadata']['realbot']
        self.assertEqual(rb_meta['intent'], 'greeting')
        self.assertEqual(rb_meta['outcome'], 'resolved')

    def test_query_fallback_writes_execution_log(self):
        """POST to send_message with random text resolves to unknown_intent and creates log."""
        url = '/api/v1/realbot/query/'
        payload = {
            "session_id": str(self.session.session_id),
            "message": "dfkjhaskjdfhaksjdfh"
        }
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Verify log entry in DB
        logs = RuleExecutionLog.objects.filter(session_id=self.session.session_id)
        self.assertEqual(logs.count(), 1)
        log = logs.first()
        self.assertEqual(log.resolved_intent, 'unknown_intent')
        self.assertEqual(log.outcome, 'fallback')


class RuleAdminEndpointTests(TestCase):

    def setUp(self):
        # Create a few rules and one execution log
        self.r1 = BusinessRule.objects.create(name="Rule One", intent="greeting", priority=1, action_type="greeting_response")
        self.r2 = BusinessRule.objects.create(name="Rule Two", intent="goodbye", priority=2, action_type="farewell_response")
        RuleExecutionLog.objects.create(
            query="hello", matched_rule=self.r1, resolved_intent="greeting",
            confidence_score=1.0, rules_evaluated=2, outcome="resolved"
        )

    def test_list_rules(self):
        response = self.client.get('/api/v1/realbot/rules/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['total_rules'], 2)

    def test_rules_diagnostics(self):
        response = self.client.get('/api/v1/realbot/rules/diagnostics/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['rules']['total'], 2)
        self.assertEqual(data['data']['executions']['total'], 1)

    def test_rules_logs(self):
        response = self.client.get('/api/v1/realbot/rules/logs/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['total_logged'], 1)
