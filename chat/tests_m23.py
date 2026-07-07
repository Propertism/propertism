"""
chat/tests_m23.py — M2.3 Internal Knowledge Repository Test Suite
Run with: .\scripts\django.cmd test chat.tests_m23
"""
import json
from django.test import TestCase, override_settings


# ==============================================================================
# MarkdownSectionParser Tests
# ==============================================================================

class MarkdownSectionParserTests(TestCase):

    def setUp(self):
        import tempfile
        self._tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def _make_md(self, content, name="test.md"):
        from pathlib import Path
        p = Path(self._tmpdir) / name
        p.write_text(content, encoding='utf-8')
        return p

    def test_parses_sections_correctly(self):
        """Parser extracts H2 headings as separate sections."""
        from chat.document_parser import MarkdownSectionParser
        content = (
            "# Terms and Conditions\n\nIntro text.\n\n"
            "## Scope of Services\n\nWe provide services.\n\n"
            "## Payment Terms\n\nFees due in 30 days.\n"
        )
        doc = MarkdownSectionParser().parse(self._make_md(content))
        self.assertEqual(doc.title, "Terms and Conditions")
        self.assertEqual(len(doc.sections), 2)
        self.assertEqual(doc.sections[0].heading, "Scope of Services")
        self.assertEqual(doc.sections[1].heading, "Payment Terms")

    def test_intro_captured_as_summary(self):
        """Text before first H2 is captured as intro_summary."""
        from chat.document_parser import MarkdownSectionParser
        content = (
            "# Company Policy\n\nThis document outlines our company policies.\n\n"
            "## Refund Policy\n\nRefunds considered within 30 days.\n"
        )
        doc = MarkdownSectionParser().parse(self._make_md(content))
        self.assertIn("company policies", doc.intro_summary.lower())

    def test_section_slug_generated(self):
        """Section slugs are URL-safe and derived from heading text."""
        from chat.document_parser import MarkdownSectionParser
        content = "# Fee Structure\n\n## Property Management Fees\n\nFees are 10%.\n"
        doc = MarkdownSectionParser().parse(self._make_md(content))
        self.assertEqual(doc.sections[0].section_slug, "property-management-fees")

    def test_content_hash_is_deterministic(self):
        """Same file content always produces the same SHA-256 hash."""
        from chat.document_parser import BaseDocumentParser
        file_path = self._make_md("# Test\n\n## Section\n\nBody.\n")
        h1 = BaseDocumentParser.compute_hash(file_path)
        h2 = BaseDocumentParser.compute_hash(file_path)
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)

    def test_get_parser_for_md_returns_markdown_parser(self):
        """get_parser_for returns MarkdownSectionParser for .md files."""
        from chat.document_parser import get_parser_for, MarkdownSectionParser
        file_path = self._make_md("# Test\n", "doc.md")
        self.assertIsInstance(get_parser_for(file_path), MarkdownSectionParser)

    def test_get_parser_raises_for_unsupported_format(self):
        """get_parser_for raises ValueError for unsupported extensions."""
        from pathlib import Path
        from chat.document_parser import get_parser_for
        with self.assertRaises(ValueError):
            get_parser_for(Path("document.pdf"))


# ==============================================================================
# KnowledgeDocument Model Tests
# ==============================================================================

class KnowledgeDocumentModelTests(TestCase):

    def _make_doc(self, slug, source_type="Policy"):
        from chat.models import KnowledgeDocument
        return KnowledgeDocument.objects.create(
            title=slug.replace('-', ' ').title(),
            doc_slug=slug,
            file_path=f"{slug}.md",
            source_type=source_type,
            category="General",
        )

    def test_doc_id_auto_generated_in_doc_format(self):
        """doc_id is auto-generated in DOC000001 format on creation."""
        doc = self._make_doc("test-policy")
        self.assertRegex(doc.doc_id, r'^DOC\d{6}$')

    def test_doc_id_unique_across_documents(self):
        """Two documents receive different doc_ids."""
        d1 = self._make_doc("doc-alpha")
        d2 = self._make_doc("doc-beta", "Terms")
        self.assertNotEqual(d1.doc_id, d2.doc_id)

    def test_doc_id_immutable_on_update(self):
        """doc_id does not change when version is bumped."""
        doc = self._make_doc("fee-structure", "FeeStructure")
        original_id = doc.doc_id
        doc.version = 2
        doc.save()
        doc.refresh_from_db()
        self.assertEqual(doc.doc_id, original_id)

    def test_is_changed_detects_content_change(self):
        """is_changed returns True for different hash, False for same hash."""
        from chat.models import KnowledgeDocument
        doc = KnowledgeDocument.objects.create(
            title="Terms", doc_slug="terms-chg-test", file_path="terms.md",
            source_type="Terms", category="General", content_hash="abc123",
        )
        self.assertTrue(doc.is_changed("def456"))
        self.assertFalse(doc.is_changed("abc123"))

    def test_str_includes_all_key_identifiers(self):
        """__str__ includes doc_id, title, version, source_type."""
        doc = self._make_doc("company-policies")
        s = str(doc)
        self.assertIn("DOC", s)
        self.assertIn("Company Policies", s)
        self.assertIn("v1", s)
        self.assertIn("Policy", s)


# ==============================================================================
# DocumentIndexer Tests
# ==============================================================================

class DocumentIndexerTests(TestCase):

    def test_index_all_documents_creates_articles(self):
        """index_all_documents() creates KA records for all seed docs in manifest."""
        import json, os
        from django.conf import settings
        from chat.models import KnowledgeArticle, KnowledgeDocument
        from chat.indexer import DocumentIndexer
        
        with open(os.path.join(settings.BASE_DIR, 'chat', 'knowledge_docs', 'manifest.json'), 'r') as f:
            expected_count = len(json.load(f).get('documents', []))
            
        result = DocumentIndexer().index_all_documents()
        self.assertEqual(result.errors, [], f"Errors: {result.errors}")
        self.assertEqual(KnowledgeDocument.objects.count(), expected_count)
        source_types = set(KnowledgeArticle.objects.values_list('source_type', flat=True))
        self.assertIn('Terms', source_types)
        self.assertIn('FeeStructure', source_types)
        self.assertIn('Policy', source_types)

    def test_index_is_idempotent(self):
        """Re-indexing unchanged files skips all sections."""
        from chat.indexer import DocumentIndexer
        DocumentIndexer().index_all_documents()
        second = DocumentIndexer().index_all_documents()
        self.assertEqual(second.indexed, 0)
        self.assertEqual(second.updated, 0)
        self.assertGreater(second.skipped, 0)

    def test_document_version_increments_on_content_change(self):
        """Version increments when file content changes."""
        import tempfile, shutil
        from pathlib import Path
        from chat.models import KnowledgeDocument
        from chat.indexer import DocumentIndexer
        tmpdir = tempfile.mkdtemp()
        try:
            p = Path(tmpdir) / "ver-test.md"
            p.write_text("# Doc\n\n## Section\n\nOriginal.\n", encoding='utf-8')
            indexer = DocumentIndexer()
            indexer.index_document(
                file_path=p, source_type="Markdown", category="General",
                doc_slug="ver-test-m23", title="Version Test",
            )
            doc = KnowledgeDocument.objects.get(doc_slug="ver-test-m23")
            self.assertEqual(doc.version, 1)

            p.write_text("# Doc\n\n## Section\n\nUpdated content.\n", encoding='utf-8')
            indexer.index_document(
                file_path=p, source_type="Markdown", category="General",
                doc_slug="ver-test-m23", title="Version Test",
            )
            doc.refresh_from_db()
            self.assertEqual(doc.version, 2)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_section_articles_have_valid_knowledge_ids(self):
        """All indexed internal articles carry a valid KA knowledge_id."""
        from chat.models import KnowledgeArticle
        from chat.indexer import DocumentIndexer
        DocumentIndexer().index_all_documents()
        articles = KnowledgeArticle.objects.filter(
            source_type__in=['Terms', 'FeeStructure', 'Policy']
        )
        self.assertGreater(articles.count(), 0)
        for a in articles:
            self.assertRegex(a.knowledge_id, r'^KA\d{6}$',
                             f"Bad knowledge_id on {a.source_ref}")


# ==============================================================================
# Unified Search Tests (M2.2 + M2.3)
# ==============================================================================

class UnifiedSearchTests(TestCase):

    def setUp(self):
        from chat.models import KnowledgeArticle
        from chat.indexer import DocumentIndexer
        from django.utils import timezone
        DocumentIndexer().index_all_documents()
        KnowledgeArticle.objects.create(
            page_title="NRI Property Management",
            url="/services/nri/",
            category="Service",
            keywords="nri property management services chennai",
            summary="Complete NRI property management services.",
            main_content="We manage property for NRI clients.",
            published_status="published",
            source_type="Website",
            source_ref="Website:service:nri-m23-test",
            search_weight=2.0,
            last_modified=timezone.now(),
        )

    def test_unified_search_finds_internal_doc(self):
        """source_types=None finds internal Policy/Terms articles."""
        from chat.search import KnowledgeSearchEngine
        result = KnowledgeSearchEngine().search("refund policy", source_types=None)
        self.assertGreater(result.total_found, 0)
        self.assertTrue(any(
            m.source_type in {'Policy', 'Terms', 'FeeStructure'}
            for m in result.matches
        ))

    def test_unified_search_finds_website_article(self):
        """source_types=None also returns website articles."""
        from chat.search import KnowledgeSearchEngine
        result = KnowledgeSearchEngine().search("nri property management", source_types=None)
        refs = [m.source_ref for m in result.matches]
        self.assertIn("Website:service:nri-m23-test", refs)

    def test_source_type_filter_restricts_to_website(self):
        """source_types=['Website'] excludes all internal documents."""
        from chat.search import KnowledgeSearchEngine
        result = KnowledgeSearchEngine().search("management", source_types=['Website'])
        for m in result.matches:
            self.assertEqual(m.source_type, 'Website')

    def test_document_ref_populated_for_internal_section(self):
        """document_ref is non-empty for matched internal sections."""
        from chat.search import KnowledgeSearchEngine
        result = KnowledgeSearchEngine().search("payment fee management", source_types=None)
        if result.total_found > 0:
            doc_refs = [m.document_ref for m in result.matches if m.document_ref]
            self.assertGreater(len(doc_refs), 0)

    def test_as_dict_includes_document_ref_in_all_matches(self):
        """as_dict() always includes document_ref key in each match dict."""
        from chat.search import KnowledgeSearchEngine
        result = KnowledgeSearchEngine().search("services", source_types=None)
        for match_dict in result.as_dict().get('matches', []):
            self.assertIn('document_ref', match_dict)


# ==============================================================================
# Document Index Endpoint Tests
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
class DocumentIndexEndpointTests(TestCase):

    def setUp(self):
        from chat.indexer import DocumentIndexer
        DocumentIndexer().index_all_documents()
        self.documents_url = '/api/v1/realbot/knowledge/documents/'
        self.index_url = '/api/v1/realbot/knowledge/index/'

    def test_get_document_list_returns_three_documents(self):
        """GET /knowledge/documents/ returns all indexed documents in manifest."""
        import json, os
        from django.conf import settings
        
        with open(os.path.join(settings.BASE_DIR, 'chat', 'knowledge_docs', 'manifest.json'), 'r') as f:
            expected_count = len(json.load(f).get('documents', []))
            
        response = self.client.get(self.documents_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['total_documents'], expected_count)

    def test_get_document_list_source_type_filter(self):
        """?source_type=Terms returns only Terms documents."""
        response = self.client.get(f"{self.documents_url}?source_type=Terms")
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        for doc in data['data']['documents']:
            self.assertEqual(doc['source_type'], 'Terms')

    def test_get_document_list_includes_valid_doc_id(self):
        """Each returned document has a valid DOC format doc_id."""
        response = self.client.get(self.documents_url)
        data = json.loads(response.content)
        for doc in data['data']['documents']:
            self.assertRegex(doc['doc_id'], r'^DOC\d{6}$')

    def test_post_reindex_returns_website_and_document_breakdown(self):
        """POST /knowledge/index/ returns combined result with website and documents keys."""
        response = self.client.post(self.index_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        idx = data['data']['index_result']
        self.assertIn('documents', idx)
        self.assertIn('website', idx)
        self.assertIn('indexed', idx)
        self.assertIn('total_processed', idx)
