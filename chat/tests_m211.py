"""
chat/tests_m211.py — M2.11 Analytics, Diagnostics & Observability Framework Test Suite.
Tests: sequential model IDs, event publisher schema saves, aggregate command cache counts,
       metrics calculator, health monitor, and REST API views.

Run with:
    .\\scripts\\django.cmd test chat.tests_m211
"""
import json
import uuid
from django.test import TestCase
from django.utils import timezone
from chat.models import PlatformEvent, MetricAggregate, RealBotSession
from chat.analytics_engine import EventPublisher, EventAggregationEngine, MetricsCalculator, HealthMonitoringFramework


# ─────────────────────────────────────────────────────────────────────────────
# 1. Model & Registry Tests
# ─────────────────────────────────────────────────────────────────────────────

class AnalyticsModelTests(TestCase):

    def test_event_id_auto_generated_sequentially(self):
        e1 = PlatformEvent.objects.create(event_type='test_evt1', provider='platform')
        e2 = PlatformEvent.objects.create(event_type='test_evt2', provider='platform')
        self.assertEqual(e1.event_id, 'EVT000001')
        self.assertEqual(e2.event_id, 'EVT000002')

    def test_aggregate_id_auto_generated_sequentially(self):
        a1 = MetricAggregate.objects.create(
            metric_key='test_key1', window_type='daily',
            window_start=timezone.now(), value=10.0
        )
        a2 = MetricAggregate.objects.create(
            metric_key='test_key2', window_type='daily',
            window_start=timezone.now(), value=20.0
        )
        self.assertEqual(a1.aggregate_id, 'AGG000001')
        self.assertEqual(a2.aggregate_id, 'AGG000002')


# ─────────────────────────────────────────────────────────────────────────────
# 2. Event Publisher & Aggregator Engine Tests
# ─────────────────────────────────────────────────────────────────────────────

class EventPublisherAndAggregatorTests(TestCase):

    def setUp(self):
        self.pub = EventPublisher()
        self.agg = EventAggregationEngine()
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())

    def test_event_publish_persists_successfully(self):
        payload = {'page_path': '/home/'}
        evt = self.pub.publish_event(
            event_type='query_received',
            provider='conversation',
            session_id=str(self.session.session_id),
            payload=payload,
            duration_ms=120
        )
        self.assertEqual(evt.event_type, 'query_received')
        self.assertEqual(evt.payload['page_path'], '/home/')
        self.assertEqual(evt.duration_ms, 120)

    def test_event_aggregation_daily_total(self):
        # 1. Publish 3 conversation_start events
        for _ in range(3):
            self.pub.publish_event(event_type='conversation_start', provider='conversation')

        # 2. Trigger aggregation
        processed = self.agg.aggregate_metrics(window_type='daily')
        self.assertEqual(processed, 3)  # 3 keys mapped in keys_mapping

        # 3. Retrieve check
        agg = MetricAggregate.objects.get(metric_key='conversations_total', window_type='daily')
        self.assertEqual(agg.value, 3.0)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Metrics Calculator & Health Framework Tests
# ─────────────────────────────────────────────────────────────────────────────

class MetricsCalculatorAndHealthTests(TestCase):

    def setUp(self):
        self.pub = EventPublisher()
        self.calc = MetricsCalculator()
        self.health = HealthMonitoringFramework()

    def test_calculator_computes_ratios_correctly(self):
        # Seed events: 2 total conversation_start, 1 inquiry_submitted (duration=5000ms), 1 failed_search
        self.pub.publish_event(event_type='conversation_start', provider='conversation')
        self.pub.publish_event(event_type='conversation_start', provider='conversation')
        self.pub.publish_event(event_type='inquiry_submitted', provider='inquiry', duration_ms=5000)
        self.pub.publish_event(event_type='knowledge_search', provider='knowledge')
        self.pub.publish_event(event_type='failed_search', provider='knowledge')

        metrics = self.calc.compute_all_metrics()

        # Conversation check
        self.assertEqual(metrics['conversation']['total_conversations'], 2)
        self.assertEqual(metrics['conversation']['conversation_completion_rate_percentage'], 50.0)

        # Knowledge check
        self.assertEqual(metrics['knowledge']['knowledge_searches'], 1)
        self.assertEqual(metrics['knowledge']['failed_knowledge_searches'], 1)
        self.assertEqual(metrics['knowledge']['knowledge_coverage_percentage'], 0.0)

        # Inquiry check
        self.assertEqual(metrics['inquiry']['avg_inquiry_completion_time_seconds'], 5.0)

    def test_health_monitor_returns_healthy(self):
        health_status = self.health.check_health()
        self.assertEqual(health_status['status'], 'healthy')
        self.assertEqual(health_status['checks']['database'], 'healthy')


# ─────────────────────────────────────────────────────────────────────────────
# 4. REST API Endpoints Tests
# ─────────────────────────────────────────────────────────────────────────────

class AnalyticsAPIEndpointTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())

    def _post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def test_event_publish_endpoint(self):
        url = '/api/v1/realbot/inquiry/analytics/event/publish/'
        payload = {
            'event_type': 'test_endpoint',
            'provider': 'platform',
            'session_id': str(self.session.session_id),
            'payload': {'key': 'val'},
            'duration_ms': 50
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['event_type'], 'test_endpoint')

    def test_metrics_get_endpoint(self):
        url = '/api/v1/realbot/inquiry/analytics/metrics/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertIn('conversation', data['data'])

    def test_health_get_endpoint(self):
        url = '/api/v1/realbot/inquiry/analytics/health/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'healthy')

    def test_aggregate_trigger_endpoint(self):
        url = '/api/v1/realbot/inquiry/analytics/aggregate/'
        payload = {'window_type': 'daily'}
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['processed_aggregates'], 3)
