"""
chat/tests_m215.py — M2.15 Knowledge Administration Test Suite.
Tests: sequential IDs, quality validation, version histories, comparisons, rollbacks,
       lifecycle transitions, re-indexing triggers, search usage, and API views.

Run with:
    .\\scripts\\django.cmd test chat.tests_m215
"""
import json
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from chat.models import (
    KnowledgeArticle, KnowledgeDocument, KnowledgeVersionHistory,
    KnowledgeLifecycleAuditLog
)
from chat.knowledge_manager import (
    KnowledgeAdministrationManager, KnowledgeValidationFramework,
    KnowledgeVersionManager, KnowledgePublishingFramework
)
from chat.search import KnowledgeSearchEngine


class KnowledgeAdminModelTests(TestCase):

    def test_version_history_id_sequential(self):
        art = KnowledgeArticle.objects.create(page_title='Test Title', source_ref='ref1')
        vh1 = KnowledgeVersionHistory.objects.create(article=art, version=1, title='Title 1')
        vh2 = KnowledgeVersionHistory.objects.create(article=art, version=2, title='Title 2')
        self.assertEqual(vh1.version_id, 'KVH000001')
        self.assertEqual(vh2.version_id, 'KVH000002')

    def test_audit_log_id_sequential(self):
        l1 = KnowledgeLifecycleAuditLog.objects.create(action='registered', article_id='KA000001')
        l2 = KnowledgeLifecycleAuditLog.objects.create(action='edited', article_id='KA000001')
        self.assertEqual(l1.audit_id, 'KLA000001')
        self.assertEqual(l2.audit_id, 'KLA000002')


class QualityValidatorTests(TestCase):

    def setUp(self):
        self.validator = KnowledgeValidationFramework()

    def test_validator_perfect_content(self):
        score, issues = self.validator.validate_content(
            title="Tamil Nadu Property Consulting services",
            main_content="This is the main body content of the services article. It must exceed 20 characters.",
            summary="A short summary of the property consulting services.",
            keywords="property consulting tamil nadu",
            tags="property,consulting"
        )
        self.assertEqual(score, 100.0)
        self.assertEqual(len(issues), 0)

    def test_validator_low_quality(self):
        # Short title, short content, short summary, too few keywords, duplicate keywords
        score, issues = self.validator.validate_content(
            title="Sale",
            main_content="Too short.",
            summary="Brief.",
            keywords="sale sale",
            tags="sale"
        )
        self.assertTrue(score < 50.0)
        self.assertTrue(any("Title is missing" in i for i in issues))
        self.assertTrue(any("Main content is missing" in i for i in issues))
        self.assertTrue(any("Summary is missing" in i for i in issues))
        self.assertTrue(any("Duplicate keywords" in i for i in issues))


class VersionManagerTests(TestCase):

    def setUp(self):
        self.art = KnowledgeArticle.objects.create(
            page_title='Original Title',
            summary='Original Summary',
            main_content='Original main content text exceeds 20 characters.',
            keywords='keywords list',
            tags='tag1',
            version=1,
            status='draft'
        )
        self.v_mgr = KnowledgeVersionManager()

    def test_version_creation_and_comparison(self):
        v1 = self.v_mgr.create_version(article=self.art)
        self.assertEqual(v1.title, 'Original Title')
        
        # Modify article
        self.art.page_title = 'New Title'
        self.art.version = 2
        v2 = self.v_mgr.create_version(article=self.art)
        
        diff = self.v_mgr.compare_versions(v1, v2)
        self.assertIn('title', diff)
        self.assertEqual(diff['title']['v1'], 'Original Title')
        self.assertEqual(diff['title']['v2'], 'New Title')

    def test_rollback_reverts_state(self):
        # Create initial version
        v1 = self.v_mgr.create_version(article=self.art)
        
        # Edit article
        self.art.page_title = 'Edited Title'
        self.art.save()
        
        # Rollback
        success, msg = self.v_mgr.rollback(v1)
        self.assertTrue(success)
        self.art.refresh_from_db()
        self.assertEqual(self.art.page_title, 'Original Title')
        self.assertEqual(self.art.version, 2)  # Version increments on modification/rollback


class PublishingFrameworkTests(TestCase):

    def setUp(self):
        self.art = KnowledgeArticle.objects.create(
            page_title='Damp Course Patta Services in Chennai',
            summary='Valid summary exceeding ten chars.',
            main_content='Valid main content that has a length greater than twenty characters.',
            keywords='patta chennai services',
            source_ref='test-art-ref',
            status='draft'
        )
        self.pub = KnowledgePublishingFramework()

    def test_publish_quality_gate_enforced(self):
        # Make it low quality
        self.art.page_title = 'Sh'
        self.art.main_content = 'Too short.'
        self.art.save()
        
        with self.assertRaises(ValueError):
            self.pub.transition_state(self.art, 'published')

    @patch('chat.knowledge_manager.KnowledgeReindexFramework.trigger_reindex')
    def test_publish_triggers_reindex_on_success(self, mock_reindex):
        # Perfect article meets quality threshold >= 70.0
        success, msg = self.pub.transition_state(self.art, 'published')
        self.assertTrue(success)
        self.assertEqual(self.art.status, 'published')
        self.assertIsNotNone(self.art.published_date)
        mock_reindex.assert_called_once()


class SearchUsageTests(TestCase):

    def setUp(self):
        self.published_art = KnowledgeArticle.objects.create(
            page_title='Chennai Patta Application Guide',
            summary='A guide to apply for Patta in Chennai.',
            main_content='Detailed instructions to get your Patta documents from the GCC portal.',
            keywords='chennai patta GCC guide',
            source_ref='chennai-patta-ref',
            status='published'
        )
        self.draft_art = KnowledgeArticle.objects.create(
            page_title='Draft Chennai Patta Guide',
            summary='A guide to apply for Patta in Chennai.',
            main_content='Detailed instructions to get your Patta documents from the GCC portal.',
            keywords='chennai patta GCC guide',
            source_ref='chennai-patta-ref-draft',
            status='draft'
        )
        self.search_engine = KnowledgeSearchEngine()

    def test_search_only_resolves_published(self):
        res = self.search_engine.search('chennai patta')
        self.assertEqual(res.total_found, 1)
        self.assertEqual(res.matches[0].knowledge_id, self.published_art.knowledge_id)

    def test_search_increments_usage_count(self):
        self.assertEqual(self.published_art.usage_count, 0)
        self.search_engine.search('chennai patta')
        self.published_art.refresh_from_db()
        self.assertEqual(self.published_art.usage_count, 1)


class KnowledgeAdminAPITests(TestCase):

    def setUp(self):
        self.art = KnowledgeArticle.objects.create(
            page_title='Patta Chitta Verification Chennai',
            summary='Verification guide for Patta.',
            main_content='This content explains how to verify Patta Chitta documents.',
            keywords='patta chitta chennai',
            source_ref='verification-guide-ref',
            status='draft'
        )

    def test_list_endpoint(self):
        url = reverse('chat:knowledge_admin_list_view')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']['articles']), 1)

    def test_update_endpoint_create(self):
        url = reverse('chat:knowledge_admin_update_view')
        payload = {
            'page_title': 'New Registered Article',
            'summary': 'New registered summary',
            'main_content': 'New registered main content text body.',
            'keywords': 'registered keywords',
            'source_ref': 'new-article-ref'
        }
        res = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'draft')

    def test_update_endpoint_edit(self):
        url = reverse('chat:knowledge_admin_update_view')
        payload = {
            'knowledge_id': self.art.knowledge_id,
            'page_title': 'Updated Title Name'
        }
        res = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['version'], 2)

    def test_publish_endpoint(self):
        url = reverse('chat:knowledge_admin_publish_view')
        payload = {
            'knowledge_id': self.art.knowledge_id,
            'status': 'published'
        }
        res = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.art.refresh_from_db()
        self.assertEqual(self.art.status, 'published')

    def test_rollback_endpoint(self):
        mgr = KnowledgeAdministrationManager()
        # Create initial version v1
        v1 = mgr.version_mgr.create_version(article=self.art)
        
        # Edit
        mgr.edit_article(self.art, {'page_title': 'Edited title'})
        
        url = reverse('chat:knowledge_admin_rollback_view')
        payload = {'version_id': v1.version_id}
        res = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.art.refresh_from_db()
        self.assertEqual(self.art.page_title, 'Patta Chitta Verification Chennai')

    @patch('chat.knowledge_manager.KnowledgeReindexFramework.trigger_reindex')
    def test_reindex_endpoint(self, mock_reindex):
        mock_reindex.return_value = {'indexed': 5, 'updated': 0, 'skipped': 0, 'errors': []}
        url = reverse('chat:knowledge_admin_reindex_view')
        res = self.client.post(url, json.dumps({}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['indexing_statistics']['indexed'], 5)

    def test_analytics_endpoint(self):
        url = reverse('chat:knowledge_admin_analytics_view')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['total_knowledge_articles'], 1)
