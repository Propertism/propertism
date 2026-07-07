"""
chat/tests_m216.py — M2.16 Analytics & Customer Insights Test Suite.
Tests calculations, date ranges, service and country filters, export, dashboards, and recommendations.

Run with:
    .\\scripts\\django.cmd test chat.tests_m216
"""
import csv
import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from chat.models import PlatformEvent, KnowledgeArticle
from chat.insights_manager import BusinessAnalyticsManager, InsightEngine, ReportGenerator


class InsightsModelQueryTests(TestCase):

    def setUp(self):
        # Create events across dates, countries, and services
        self.now = timezone.now()
        self.yesterday = self.now - timezone.timedelta(days=1)
        self.last_week = self.now - timezone.timedelta(days=7)

        # Session 1 (India, NRI advisory service)
        e1 = PlatformEvent.objects.create(
            event_type='conversation_start',
            provider='welcome',
            session_id='session_in_1',
            payload={'country': 'India', 'service_code': 'nri_assist', 'referrer': '/nri-assist/'}
        )
        PlatformEvent.objects.filter(event_id=e1.event_id).update(created_at=self.yesterday)

        e2 = PlatformEvent.objects.create(
            event_type='inquiry_initiated',
            provider='inquiry',
            session_id='session_in_1',
            payload={'country': 'India', 'service_code': 'nri_assist'}
        )
        PlatformEvent.objects.filter(event_id=e2.event_id).update(created_at=self.yesterday)

        e3 = PlatformEvent.objects.create(
            event_type='inquiry_submitted',
            provider='inquiry',
            session_id='session_in_1',
            payload={'country': 'India', 'service_code': 'nri_assist'},
            duration_ms=45000
        )
        PlatformEvent.objects.filter(event_id=e3.event_id).update(created_at=self.now)

        # Session 2 (US, Buy service)
        e4 = PlatformEvent.objects.create(
            event_type='conversation_start',
            provider='welcome',
            session_id='session_us_2',
            payload={'country': 'US', 'service_code': 'buy_property', 'referrer': '/properties/'}
        )
        PlatformEvent.objects.filter(event_id=e4.event_id).update(created_at=self.last_week)

        e5 = PlatformEvent.objects.create(
            event_type='inquiry_initiated',
            provider='inquiry',
            session_id='session_us_2',
            payload={'country': 'US', 'service_code': 'buy_property'}
        )
        PlatformEvent.objects.filter(event_id=e5.event_id).update(created_at=self.last_week)

    def test_date_range_filters(self):
        # Filter for last 2 days
        filters = {
            'start_date': (self.now - timezone.timedelta(days=2)).isoformat(),
            'end_date': (self.now + timezone.timedelta(days=1)).isoformat()
        }
        mgr = BusinessAnalyticsManager(filters=filters)
        summary = mgr.get_executive_summary()
        self.assertEqual(summary['total_conversations'], 1)  # Only Session 1

    def test_country_filter(self):
        mgr = BusinessAnalyticsManager(filters={'country': 'US'})
        summary = mgr.get_executive_summary()
        self.assertEqual(summary['total_conversations'], 1)
        self.assertEqual(summary['inquiry_initiations'], 1)
        self.assertEqual(summary['inquiry_completions'], 0)

    def test_service_filter(self):
        mgr = BusinessAnalyticsManager(filters={'service': 'nri_assist'})
        summary = mgr.get_executive_summary()
        self.assertEqual(summary['total_conversations'], 1)
        self.assertEqual(summary['inquiry_completions'], 1)


class DashboardBuilderTests(TestCase):

    def setUp(self):
        # Knowledge events
        PlatformEvent.objects.create(
            event_type='knowledge_search',
            provider='knowledge',
            session_id='sess_kb',
            payload={'query': 'chennai patta'}
        )
        PlatformEvent.objects.create(
            event_type='article_resolved',
            provider='knowledge',
            session_id='sess_kb',
            payload={'article_title': 'Patta Chitta Verification'}
        )
        PlatformEvent.objects.create(
            event_type='knowledge_search',
            provider='knowledge',
            session_id='sess_kb',
            payload={'query': 'unknown property tax'}
        )
        PlatformEvent.objects.create(
            event_type='failed_search',
            provider='knowledge',
            session_id='sess_kb',
            payload={'query': 'unknown property tax'}
        )
        # Create Article in DB
        KnowledgeArticle.objects.create(page_title='Patta Chitta Verification', source_ref='ref1')

        # Suggestion click
        PlatformEvent.objects.create(event_type='suggestion_displayed', provider='suggestion')
        PlatformEvent.objects.create(
            event_type='suggestion_clicked',
            provider='suggestion',
            payload={'display_text': 'NRI Tax Advisory'}
        )

        # Action execute
        PlatformEvent.objects.create(
            event_type='action_executed',
            provider='action',
            payload={'action_name': 'whatsapp'}
        )

    def test_all_dashboards_render(self):
        mgr = BusinessAnalyticsManager()
        data = mgr.build_dashboard_data()

        # Verification of dashboards presence
        self.assertIn('executive', data)
        self.assertIn('customer_journey', data)
        self.assertIn('inquiry', data)
        self.assertIn('knowledge', data)
        self.assertIn('service', data)
        self.assertIn('conversation', data)
        self.assertIn('search', data)
        self.assertIn('conversion', data)

        # Knowledge Metrics verification
        kb = data['knowledge']
        self.assertEqual(kb['knowledge_searches'], 2)
        self.assertEqual(kb['failed_knowledge_searches'], 1)
        self.assertEqual(kb['knowledge_coverage_percentage'], 50.0)
        self.assertIn('Patta Chitta Verification', kb['most_viewed_articles'])

        # Suggestion Metrics CTR verification
        conv = data['conversion']
        self.assertEqual(conv['suggestion_ctr'], 100.0)
        self.assertEqual(conv['action_clicks']['whatsapp'], 1)


class InsightRecommendationsTests(TestCase):

    def test_recommendations_low_coverage(self):
        # Build dashboard data mock representing high failure
        data = {
            'inquiry': {'inquiry_initiated': 0, 'inquiry_abandoned_rate': 0.0},
            'knowledge': {
                'knowledge_searches': 10,
                'knowledge_coverage_percentage': 50.0,
                'missing_knowledge_requests': ['chennai patta', 'fee structure']
            },
            'conversion': {'suggestion_ctr': 25.0}
        }
        engine = InsightEngine(data)
        recs = engine.generate_recommendations()
        self.assertTrue(any(r['id'] == 'REC002' for r in recs))
        self.assertTrue(any('Search coverage is low' in r['observation'] for r in recs))


class InsightsAPITests(TestCase):

    def setUp(self):
        # Create minimum events for API checks
        PlatformEvent.objects.create(
            event_type='conversation_start',
            provider='welcome',
            session_id='sess_api_1',
            payload={'country': 'India', 'service_code': 'nri_assist'}
        )

    def test_dashboard_endpoint(self):
        url = reverse('chat:insights_dashboard_view')
        res = self.client.get(url, {'country': 'India'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['executive']['total_conversations'], 1)

    def test_report_endpoint(self):
        url = reverse('chat:insights_report_view')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertIn('report_generated_at', data['data'])

    def test_export_endpoint(self):
        url = reverse('chat:insights_export_view')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'], 'text/csv')
        self.assertTrue(res['Content-Disposition'].startswith('attachment;'))
        
        # Verify CSV is parseable
        content = res.content.decode('utf-8')
        reader = csv.reader(content.splitlines())
        rows = list(reader)
        self.assertTrue(len(rows) > 1)
        self.assertEqual(rows[0][0], 'Metric Category')

    def test_recommendations_endpoint(self):
        url = reverse('chat:insights_recommendations_view')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['data']['recommendations']) > 0)
