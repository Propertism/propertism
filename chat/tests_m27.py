"""
chat/tests_m27.py — M2.7 Quick Inquiry & Suggestion Framework Test Suite
Covers: Model ID generation, Suggestion Engine, context providers,
        ranking and deduplication, endpoints, click logging, and analytics.

Run with:
    .\\scripts\\django.cmd test chat.tests_m27
"""
import json
import uuid
from unittest.mock import patch
from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from chat.models import (
    RealBotSession, SuggestionDefinition, SuggestionInteractionLog,
    BusinessRule
)
from chat.suggestion_engine import SuggestionEngine, SuggestionContext


# ─────────────────────────────────────────────────────────────────────────────
# 1. Model Tests
# ─────────────────────────────────────────────────────────────────────────────

class SuggestionModelTests(TestCase):

    def test_suggestion_id_auto_generated(self):
        sug = SuggestionDefinition.objects.create(
            display_text='Click Me',
            category='Welcome',
            display_priority=10,
        )
        self.assertEqual(sug.suggestion_id, 'SUG000001')

    def test_suggestion_id_sequential(self):
        s1 = SuggestionDefinition.objects.create(
            display_text='Chip 1', category='Welcome'
        )
        s2 = SuggestionDefinition.objects.create(
            display_text='Chip 2', category='Welcome'
        )
        self.assertEqual(s1.suggestion_id, 'SUG000001')
        self.assertEqual(s2.suggestion_id, 'SUG000002')

    def test_log_id_auto_generated(self):
        session = RealBotSession.objects.create(session_id=uuid.uuid4())
        log = SuggestionInteractionLog.objects.create(
            session=session,
            suggestion_id='SUG000001',
            display_text='Click Me',
            category='Welcome',
            interaction_type='rendered',
        )
        self.assertEqual(log.log_id, 'SGL000001')

    def test_log_id_sequential(self):
        session = RealBotSession.objects.create(session_id=uuid.uuid4())
        l1 = SuggestionInteractionLog.objects.create(
            session=session, suggestion_id='SUG000001',
            display_text='Chip 1', category='Welcome', interaction_type='rendered'
        )
        l2 = SuggestionInteractionLog.objects.create(
            session=session, suggestion_id='SUG000001',
            display_text='Chip 2', category='Welcome', interaction_type='clicked'
        )
        self.assertEqual(l1.log_id, 'SGL000001')
        self.assertEqual(l2.log_id, 'SGL000002')


# ─────────────────────────────────────────────────────────────────────────────
# 2. Ranking & Deduplication Engine Tests
# ─────────────────────────────────────────────────────────────────────────────

class SuggestionRankingDeduplicationTests(TestCase):

    def setUp(self):
        self.sug1 = SuggestionDefinition.objects.create(
            display_text='Explore', category='Welcome', display_priority=20, display_order=1
        )
        self.sug2 = SuggestionDefinition.objects.create(
            display_text='Buy Villa', category='Welcome', display_priority=10, display_order=2
        )
        self.sug3 = SuggestionDefinition.objects.create(
            display_text='Explore', category='Inquiry', display_priority=5, display_order=1
        )
        self.engine = SuggestionEngine()

    def test_ranking_priority_and_order(self):
        items = [self.sug1, self.sug2, self.sug3]
        ranked = self.engine.ranking_engine.rank(items)
        # Priority 5 (sug3) -> Priority 10 (sug2) -> Priority 20 (sug1)
        self.assertEqual(ranked[0].suggestion_id, self.sug3.suggestion_id)
        self.assertEqual(ranked[1].suggestion_id, self.sug2.suggestion_id)
        self.assertEqual(ranked[2].suggestion_id, self.sug1.suggestion_id)

    def test_deduplication_preserves_higher_ranked(self):
        # Explore appears twice: sug3 (priority 5) and sug1 (priority 20)
        items = [self.sug3, self.sug2, self.sug1]
        deduped = self.engine.dedup_engine.deduplicate(items)
        # Should keep sug3 and sug2, but drop sug1
        self.assertEqual(len(deduped), 2)
        display_texts = [d.display_text for d in deduped]
        self.assertIn('Explore', display_texts)
        self.assertIn('Buy Villa', display_texts)
        # Check that Explore corresponds to priority 5
        explore_item = next(d for d in deduped if d.display_text == 'Explore')
        self.assertEqual(explore_item.display_priority, 5)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Context Providers Tests
# ─────────────────────────────────────────────────────────────────────────────

class SuggestionProviderTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        # Seed standard definitions
        self.welcome_chip = SuggestionDefinition.objects.create(
            display_text='Explore Services', category='Welcome', display_priority=10
        )
        self.buy_chip = SuggestionDefinition.objects.create(
            display_text='Buy Property', category='Inquiry', display_priority=20,
            trigger_condition={'intent': 'buy_property'}
        )
        self.nri_chip = SuggestionDefinition.objects.create(
            display_text='Check Eligibility', category='Service', display_priority=10,
            trigger_condition={'service_profile': 'NRI Property Management'}
        )
        self.knowledge_chip = SuggestionDefinition.objects.create(
            display_text='Read Guide', category='Knowledge', display_priority=30
        )
        self.recovery_chip = SuggestionDefinition.objects.create(
            display_text='Restart', category='Recovery', display_priority=50
        )
        self.completion_chip = SuggestionDefinition.objects.create(
            display_text='New Inquiry', category='Completion', display_priority=5
        )
        self.engine = SuggestionEngine()

    def test_welcome_provider_triggered(self):
        ctx = SuggestionContext(session=self.session, intent='greeting')
        sugs = self.engine.get_suggestions(ctx)
        self.assertEqual(sugs[0]['display_text'], 'Explore Services')

    def test_rule_engine_provider_triggered(self):
        ctx = SuggestionContext(session=self.session, intent='buy_property')
        sugs = self.engine.get_suggestions(ctx)
        self.assertEqual(sugs[0]['display_text'], 'Buy Property')

    def test_service_provider_triggered(self):
        ctx = SuggestionContext(
            session=self.session, intent='greeting',
            active_service_profile='NRI Property Management'
        )
        sugs = self.engine.get_suggestions(ctx)
        texts = [s['display_text'] for s in sugs]
        self.assertIn('Check Eligibility', texts)

    def test_knowledge_provider_triggered(self):
        ctx = SuggestionContext(session=self.session, knowledge_resolved=True)
        sugs = self.engine.get_suggestions(ctx)
        self.assertEqual(sugs[0]['display_text'], 'Read Guide')

    def test_recovery_provider_triggered(self):
        ctx = SuggestionContext(session=self.session, intent='unknown_intent')
        sugs = self.engine.get_suggestions(ctx)
        texts = [s['display_text'] for s in sugs]
        self.assertIn('Restart', texts)

    def test_completion_provider_triggered(self):
        ctx = SuggestionContext(session=self.session, inquiry_state='submitted')
        sugs = self.engine.get_suggestions(ctx)
        self.assertEqual(sugs[0]['display_text'], 'New Inquiry')


# ─────────────────────────────────────────────────────────────────────────────
# 4. End-to-End API Endpoint & Analytics Tests
# ─────────────────────────────────────────────────────────────────────────────

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
class SuggestionAPIEndpointTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        # Seed welcome suggestion
        self.chip = SuggestionDefinition.objects.create(
            display_text='Explore Propertism', category='Welcome', display_priority=10
        )
        # Seed rule intent
        BusinessRule.objects.create(
            name='Greeting Rule',
            intent='greeting',
            priority=1,
            positive_keywords='hi,hello,greet',
            min_confidence=0.3,
            action_type='greeting_response',
        )

    def _post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def test_query_endpoint_populates_suggestions_metadata(self):
        url = '/api/v1/realbot/query/'
        payload = {
            'session_id': str(self.session.session_id),
            'message': 'Hi realbot',
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        
        msg_meta = data['data']['message']['metadata']
        self.assertIn('chips', msg_meta)
        self.assertIn('suggestions', msg_meta)
        self.assertIn('Explore Propertism', msg_meta['chips'])
        suggestion_ids = [s['suggestion_id'] for s in msg_meta['suggestions']]
        self.assertIn(self.chip.suggestion_id, suggestion_ids)

    def test_click_tracking_endpoint(self):
        url = '/api/v1/realbot/inquiry/suggestion/click/'
        payload = {
            'session_id': str(self.session.session_id),
            'suggestion_id': self.chip.suggestion_id,
            'display_text': self.chip.display_text,
            'category': self.chip.category,
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])

        # Verify SuggestionInteractionLog has a clicked entry
        log = SuggestionInteractionLog.objects.filter(
            suggestion_id=self.chip.suggestion_id,
            interaction_type='clicked'
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.session.session_id, self.session.session_id)

    def test_analytics_endpoint(self):
        # Render a chip twice, click once
        SuggestionInteractionLog.objects.create(
            session=self.session, suggestion_id=self.chip.suggestion_id,
            display_text=self.chip.display_text, category=self.chip.category,
            interaction_type='rendered'
        )
        SuggestionInteractionLog.objects.create(
            session=self.session, suggestion_id=self.chip.suggestion_id,
            display_text=self.chip.display_text, category=self.chip.category,
            interaction_type='rendered'
        )
        SuggestionInteractionLog.objects.create(
            session=self.session, suggestion_id=self.chip.suggestion_id,
            display_text=self.chip.display_text, category=self.chip.category,
            interaction_type='clicked'
        )

        url = '/api/v1/realbot/inquiry/suggestion/analytics/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])

        # Verify analytics details
        overall = data['data']['overall']
        self.assertEqual(overall['impressions'], 2)
        self.assertEqual(overall['clicks'], 1)
        self.assertEqual(overall['ctr'], 50.0)

        # Verify breakdowns
        by_cat = data['data']['by_category'][0]
        self.assertEqual(by_cat['category'], self.chip.category)
        self.assertEqual(by_cat['impressions'], 2)
        self.assertEqual(by_cat['clicks'], 1)
        self.assertEqual(by_cat['ctr'], 50.0)
