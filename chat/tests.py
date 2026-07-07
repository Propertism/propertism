from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class RealBotExchangeTests(TestCase):
    """Test suite for the realBOT token exchange endpoint."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.exchange_url = reverse('chat:exchange_token')

    @override_settings(REALBOT_INTEGRATION_ENABLED=False)
    def test_exchange_disabled(self):
        """When integration is disabled, endpoint should return success=False, status=403."""
        response = self.client.get(self.exchange_url)
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['error']['code'], 'RBOT0001')
        self.assertEqual(data['error']['message'], 'realBOT integration is disabled locally')

    @override_settings(
        REALBOT_INTEGRATION_ENABLED=True,
        REALBOT_BASE_URL='http://127.0.0.1:8010',
        REALBOT_API_KEY='test-key',
        REALBOT_TENANT='propertism',
        REALBOT_PRODUCT='propertism.in',
        REALBOT_DOMAIN='real_estate',
        REALBOT_WIDGET_URL='http://127.0.0.1:8010'
    )
    def test_exchange_enabled_anonymous(self):
        """When enabled and anonymous, returns mock/fallback token and configuration inside data envelope."""
        response = self.client.get(self.exchange_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['data']['enabled'])
        self.assertIn('session_token', data['data'])
        self.assertTrue(data['data']['session_token'].startswith('mock_session_'))
        self.assertEqual(data['data']['user']['email'], 'anonymous_user')
        self.assertFalse(data['data']['user']['is_authenticated'])
        self.assertEqual(data['data']['config']['tenant'], 'propertism')
        self.assertEqual(data['data']['config']['product'], 'propertism.in')
        self.assertEqual(data['data']['config']['widget_url'], 'http://127.0.0.1:8010')

    @override_settings(
        REALBOT_INTEGRATION_ENABLED=True,
        REALBOT_BASE_URL='http://127.0.0.1:8010',
        REALBOT_API_KEY='test-key',
        REALBOT_TENANT='propertism',
        REALBOT_PRODUCT='propertism.in',
        REALBOT_DOMAIN='real_estate',
        REALBOT_WIDGET_URL='http://127.0.0.1:8010'
    )
    def test_exchange_enabled_authenticated(self):
        """When enabled and authenticated, returns mock/fallback token and email user identifier inside data envelope."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.exchange_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['data']['enabled'])
        self.assertEqual(data['data']['user']['email'], 'testuser@example.com')
        self.assertEqual(data['data']['user']['username'], 'testuser')
        self.assertTrue(data['data']['user']['is_authenticated'])

    @override_settings(
        REALBOT_INTEGRATION_ENABLED=True,
        REALBOT_BASE_URL='http://127.0.0.1:8010',
        REALBOT_API_KEY='test-key',
        REALBOT_TENANT='propertism',
        REALBOT_PRODUCT='propertism.in',
        REALBOT_DOMAIN='real_estate',
        REALBOT_WIDGET_URL='http://127.0.0.1:8010'
    )
    def test_correlation_id_present(self):
        """Responses must include the X-Correlation-ID header."""
        response = self.client.get(self.exchange_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('X-Correlation-ID', response.headers)
        data = json.loads(response.content)
        self.assertIn('correlation_id', data)
        self.assertEqual(response.headers['X-Correlation-ID'], data['correlation_id'])

    @override_settings(
        REALBOT_INTEGRATION_ENABLED=True,
        REALBOT_BASE_URL='http://127.0.0.1:8010',
        REALBOT_API_KEY='test-key',
        REALBOT_TENANT='propertism',
        REALBOT_PRODUCT='propertism.in',
        REALBOT_DOMAIN='real_estate',
        REALBOT_WIDGET_URL='http://127.0.0.1:8010'
    )
    def test_health_check_endpoint(self):
        """Health check endpoint must return success=True and environment details."""
        health_url = reverse('chat:health_check')
        response = self.client.get(health_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'operational')
        self.assertEqual(data['data']['database'], 'healthy')
        self.assertTrue(data['data']['integration_enabled'])

    @override_settings(
        REALBOT_INTEGRATION_ENABLED=True,
        REALBOT_BASE_URL='http://127.0.0.1:8010',
        REALBOT_API_KEY='test-key',
        REALBOT_TENANT='propertism',
        REALBOT_PRODUCT='propertism.in',
        REALBOT_DOMAIN='real_estate',
        REALBOT_WIDGET_URL='http://127.0.0.1:8010'
    )
    def test_session_init_with_conversation_id(self):
        """Initializing a session generates session_id and conversation_id."""
        init_url = reverse('chat:init_session')
        response = self.client.post(init_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('session_id', data['data'])
        self.assertIn('conversation_id', data['data'])

    @override_settings(
        REALBOT_INTEGRATION_ENABLED=True,
        REALBOT_BASE_URL='http://127.0.0.1:8010',
        REALBOT_API_KEY='test-key',
        REALBOT_TENANT='propertism',
        REALBOT_PRODUCT='propertism.in',
        REALBOT_DOMAIN='real_estate',
        REALBOT_WIDGET_URL='http://127.0.0.1:8010'
    )
    def test_health_live_endpoint(self):
        """Liveness health check endpoint must return status=alive."""
        health_live_url = reverse('chat:health_live')
        response = self.client.get(health_live_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'alive')

    @override_settings(
        REALBOT_INTEGRATION_ENABLED=True,
        REALBOT_BASE_URL='http://127.0.0.1:8010',
        REALBOT_API_KEY='test-key',
        REALBOT_TENANT='propertism',
        REALBOT_PRODUCT='propertism.in',
        REALBOT_DOMAIN='real_estate',
        REALBOT_WIDGET_URL='http://127.0.0.1:8010',
        REALBOT_API_VERSION='v1'
    )
    def test_health_ready_endpoint(self):
        """Readiness health check endpoint must validate setup and return metrics."""
        health_ready_url = reverse('chat:health_ready')
        response = self.client.get(health_ready_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'ready')
        self.assertEqual(data['data']['database'], 'healthy')
        self.assertEqual(data['data']['configuration'], 'valid')
        self.assertIn('metrics', data['data'])
        self.assertIn('app_startup_count', data['data']['metrics'])

    @override_settings(
        REALBOT_INTEGRATION_ENABLED=True,
        REALBOT_BASE_URL='http://127.0.0.1:8010',
        REALBOT_API_KEY='test-key',
        REALBOT_TENANT='propertism',
        REALBOT_PRODUCT='propertism.in',
        REALBOT_DOMAIN='real_estate',
        REALBOT_WIDGET_URL='http://127.0.0.1:8010',
        REALBOT_API_VERSION='v1'
    )
    def test_version_service_endpoint(self):
        """Version service returns correct metadata, build number, and flags."""
        version_url = reverse('chat:version_service')
        response = self.client.get(version_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['api_version'], 'v1')
        self.assertEqual(data['data']['build_version'], '2.1.1-stable')
        self.assertEqual(data['data']['application_version'], '1.0.0-propertism')
        self.assertTrue(data['data']['feature_flag_status'])

    def test_configuration_validation_errors(self):
        """Validator lists issues for missing parameters and invalid schemas."""
        from chat.validators import validate_realbot_configuration
        with self.settings(
            REALBOT_BASE_URL='invalid-url-format',
            REALBOT_TENANT='',
            REALBOT_PRODUCT='',
            REALBOT_DOMAIN='',
            REALBOT_WIDGET_URL='http://127.0.0.1:8010'
        ):
            is_valid, issues, report = validate_realbot_configuration()
            self.assertFalse(is_valid)
            self.assertTrue(len(issues) > 0)
            self.assertIn("Missing mandatory setting: REALBOT_TENANT", issues)
            self.assertIn("Invalid REALBOT_BASE_URL protocol (must be http/https): invalid-url-format", issues)


# ==============================================================================
# M2.2 — Website Knowledge Base Tests
# ==============================================================================

class KnowledgeArticleModelTests(TestCase):
    """Test suite for KnowledgeArticle model creation and retrieval."""

    def setUp(self):
        from chat.models import KnowledgeArticle
        from django.utils import timezone
        self.article = KnowledgeArticle.objects.create(
            page_title="NRI Property Management Services",
            url="/services/nri-management/",
            category="Service",
            language="en",
            keywords="nri property management services chennai",
            summary="Propertism offers complete NRI property management in Chennai.",
            main_content="Full description of NRI property management services.",
            published_status="published",
            source_type="Website",
            source_ref="Website:service:nri-management",
            search_weight=2.0,
            last_modified=timezone.now(),
        )

    def test_knowledge_article_created(self):
        """KnowledgeArticle records can be created and retrieved by source_ref."""
        from chat.models import KnowledgeArticle
        article = KnowledgeArticle.objects.get(source_ref="Website:service:nri-management")
        self.assertEqual(article.page_title, "NRI Property Management Services")
        self.assertEqual(article.category, "Service")
        self.assertEqual(article.source_type, "Website")

    def test_published_status_default(self):
        """Default published_status is 'published'."""
        self.assertEqual(self.article.published_status, "published")

    def test_str_representation(self):
        """__str__ returns [knowledge_id][source_type:category] page_title format."""
        self.assertIn("Website", str(self.article))
        self.assertIn("Service", str(self.article))
        self.assertIn("NRI Property Management", str(self.article))

    def test_knowledge_id_auto_generated(self):
        """knowledge_id is auto-generated on creation and matches KA format."""
        import re
        self.assertTrue(bool(self.article.knowledge_id))
        self.assertRegex(self.article.knowledge_id, r'^KA\d{6}$')

    def test_knowledge_id_is_unique_across_articles(self):
        """Two different articles receive different knowledge_ids."""
        from chat.models import KnowledgeArticle
        from django.utils import timezone
        article2 = KnowledgeArticle.objects.create(
            page_title="Rental Management",
            url="/services/rental/",
            category="Service",
            keywords="rental management",
            summary="Rental management services.",
            main_content="Rental details.",
            published_status="published",
            source_type="Website",
            source_ref="Website:service:rental",
            search_weight=1.5,
            last_modified=timezone.now(),
        )
        self.assertNotEqual(self.article.knowledge_id, article2.knowledge_id)

    def test_knowledge_id_immutable_on_update(self):
        """knowledge_id does not change when the article is updated."""
        original_id = self.article.knowledge_id
        self.article.summary = "Updated summary content."
        self.article.save()
        self.article.refresh_from_db()
        self.assertEqual(self.article.knowledge_id, original_id)

    def test_knowledge_id_in_search_result(self):
        """SearchMatch includes knowledge_id from the matched article."""
        from chat.search import KnowledgeSearchEngine
        engine = KnowledgeSearchEngine()
        result = engine.search("nri property management")
        self.assertGreater(result.total_found, 0)
        match = result.matches[0]
        self.assertTrue(bool(match.knowledge_id))
        self.assertRegex(match.knowledge_id, r'^KA\d{6}$')


class WebsiteContentIndexerTests(TestCase):
    """Test suite for WebsiteContentIndexer."""

    def _create_service(self, title, slug):
        from content.models import Service
        return Service.objects.create(
            title=title,
            slug=slug,
            short_description=f"{title} short description for NRI owners.",
            full_description=f"{title} full description with all features listed.",
            is_active=True,
        )

    def test_index_services_creates_articles(self):
        """Indexing active services creates KnowledgeArticle records."""
        from chat.models import KnowledgeArticle
        from chat.indexer import WebsiteContentIndexer
        self._create_service("Property Management", "property-management")
        self._create_service("Rental Management", "rental-management")

        indexer = WebsiteContentIndexer()
        result = indexer.index_services()

        self.assertEqual(result.indexed, 2)
        self.assertEqual(result.errors, [])
        self.assertEqual(KnowledgeArticle.objects.filter(category="Service").count(), 2)

    def test_index_all_returns_indexed_count(self):
        """index_all() returns an IndexResult with non-zero total when data exists."""
        from chat.indexer import WebsiteContentIndexer
        self._create_service("Tenant Management", "tenant-management")

        indexer = WebsiteContentIndexer()
        result = indexer.index_all()

        total = result.indexed + result.updated + result.skipped
        self.assertGreater(total, 0)

    def test_index_idempotent_on_second_run(self):
        """Re-indexing same data results in skipped (not duplicate) articles."""
        from chat.models import KnowledgeArticle
        from chat.indexer import WebsiteContentIndexer
        self._create_service("Legal Advisory", "legal-advisory")

        indexer = WebsiteContentIndexer()
        first = indexer.index_services()
        second = indexer.index_services()

        # No new articles on second run — same source_ref
        self.assertEqual(first.indexed, 1)
        self.assertEqual(second.indexed, 0)
        self.assertEqual(KnowledgeArticle.objects.filter(source_ref="Website:service:legal-advisory").count(), 1)

    def test_inactive_services_not_indexed(self):
        """Inactive services are excluded from indexing."""
        from content.models import Service
        from chat.models import KnowledgeArticle
        from chat.indexer import WebsiteContentIndexer
        Service.objects.create(
            title="Inactive Service",
            slug="inactive-service",
            short_description="Should not be indexed.",
            full_description="This service is inactive.",
            is_active=False,
        )
        indexer = WebsiteContentIndexer()
        result = indexer.index_services()
        self.assertEqual(result.indexed, 0)
        self.assertEqual(KnowledgeArticle.objects.filter(source_ref="Website:service:inactive-service").count(), 0)

    def test_index_result_as_dict(self):
        """IndexResult.as_dict() contains expected keys."""
        from chat.indexer import IndexResult
        result = IndexResult(indexed=3, updated=1, skipped=2, errors=["test error"])
        d = result.as_dict()
        self.assertEqual(d["indexed"], 3)
        self.assertEqual(d["updated"], 1)
        self.assertEqual(d["skipped"], 2)
        self.assertEqual(d["total_processed"], 6)
        self.assertEqual(d["errors"], ["test error"])


class KnowledgeSearchEngineTests(TestCase):
    """Test suite for KnowledgeSearchEngine deterministic keyword search."""

    def setUp(self):
        from chat.models import KnowledgeArticle
        from django.utils import timezone
        now = timezone.now()
        KnowledgeArticle.objects.create(
            page_title="NRI Property Management",
            url="/services/nri/",
            category="Service",
            keywords="nri property management services india chennai abroad",
            summary="Complete property management services for NRI clients in Chennai.",
            main_content="We manage property for NRI clients including maintenance and rental.",
            published_status="published",
            source_type="Website",
            source_ref="Website:service:nri",
            search_weight=2.0,
            last_modified=now,
        )
        KnowledgeArticle.objects.create(
            page_title="Contact Propertism",
            url="/contact/",
            category="Contact",
            keywords="contact phone email address office hours",
            summary="Contact us at info@propertism.in or call +91 86670 20798.",
            main_content="India office: Chennai. US office: New Jersey.",
            published_status="published",
            source_type="Website",
            source_ref="Website:company:contact",
            search_weight=1.3,
            last_modified=now,
        )
        KnowledgeArticle.objects.create(
            page_title="Draft Article",
            url="/draft/",
            category="General",
            keywords="draft unpublished hidden",
            summary="This should not appear in search results.",
            main_content="Draft content.",
            published_status="draft",
            source_type="Website",
            source_ref="Website:draft:001",
            search_weight=1.0,
            last_modified=now,
        )

    def test_search_returns_relevant_results(self):
        """Searching for 'nri property' returns the NRI service article."""
        from chat.search import KnowledgeSearchEngine
        engine = KnowledgeSearchEngine()
        result = engine.search("nri property management")
        self.assertGreater(result.total_found, 0)
        titles = [m.page_title for m in result.matches]
        self.assertIn("NRI Property Management", titles)

    def test_search_excludes_draft_articles(self):
        """Draft articles are excluded from search results."""
        from chat.search import KnowledgeSearchEngine
        engine = KnowledgeSearchEngine()
        result = engine.search("draft unpublished")
        refs = [m.source_ref for m in result.matches]
        self.assertNotIn("Website:draft:001", refs)

    def test_search_source_references_populated(self):
        """Source references are returned with every non-empty search result."""
        from chat.search import KnowledgeSearchEngine
        engine = KnowledgeSearchEngine()
        result = engine.search("contact phone email")
        if result.total_found > 0:
            self.assertIsInstance(result.source_references, list)
            self.assertGreater(len(result.source_references), 0)

    def test_search_empty_query_returns_empty(self):
        """Empty query returns an empty SearchResult."""
        from chat.search import KnowledgeSearchEngine
        engine = KnowledgeSearchEngine()
        result = engine.search("")
        self.assertEqual(result.total_found, 0)
        self.assertEqual(result.matches, [])

    def test_search_result_as_dict(self):
        """SearchResult.as_dict() contains expected structure."""
        from chat.search import KnowledgeSearchEngine
        engine = KnowledgeSearchEngine()
        result = engine.search("property")
        d = result.as_dict()
        self.assertIn("query", d)
        self.assertIn("total_found", d)
        self.assertIn("matches", d)
        self.assertIn("source_references", d)


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
class KnowledgeIndexEndpointTests(TestCase):
    """Test suite for GET and POST /api/v1/realbot/knowledge/index/."""

    def setUp(self):
        from chat.models import KnowledgeArticle
        from django.utils import timezone
        KnowledgeArticle.objects.create(
            page_title="About Propertism",
            url="/about/",
            category="About",
            keywords="about company mission",
            summary="Propertism is a premium NRI property management company.",
            main_content="About content.",
            published_status="published",
            source_type="Website",
            source_ref="Website:company:about-test",
            search_weight=1.5,
            last_modified=timezone.now(),
        )
        self.index_url = '/api/v1/realbot/knowledge/index/'

    def test_get_index_stats(self):
        """GET /knowledge/index/ returns article count and category breakdown."""
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('total_articles', data['data'])
        self.assertIn('by_category', data['data'])
        self.assertIn('by_source_type', data['data'])
        self.assertIn('last_indexed', data['data'])
        self.assertGreaterEqual(data['data']['total_articles'], 1)

    def test_post_triggers_reindex(self):
        """POST /knowledge/index/ triggers indexer and returns IndexResult."""
        response = self.client.post(self.index_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('index_result', data['data'])
        idx = data['data']['index_result']
        self.assertIn('indexed', idx)
        self.assertIn('updated', idx)
        self.assertIn('skipped', idx)
        self.assertIn('total_processed', idx)
