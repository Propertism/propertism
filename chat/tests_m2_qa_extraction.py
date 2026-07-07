import json
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from content.models import CompanyInfo, TeamMember, Service, CustomerReview, CustomerReviewSection, BlogPost
from properties.models import Property, PropertyType
from chat.models import KnowledgeArticle, ExtractedKnowledgeCandidate, KnowledgeLifecycleAuditLog
from chat.knowledge_extractor import (
    generate_synonyms,
    generate_question_variants,
    WebsiteConversationalExtractor,
    KnowledgeReconciliationEngine
)

class KnowledgeConversationalExtractionTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Seed basic company info
        self.company = CompanyInfo.objects.create(
            company_name="Propertism",
            tagline="Premium Property Management for NRIs",
            about_description="Propertism offers premium real estate advisory services.",
            about_mission="To make property management stress-free for global Indians.",
            email="info@propertism.in",
            india_phone_1="+91 86670 20798",
            india_office_address="123 Anna Salai",
            india_office_state="Tamil Nadu",
            india_office_pincode="600002"
        )
        
        # Seed an active team member
        self.member = TeamMember.objects.create(
            name="Tamilselvan",
            role="Founder & Asset Management Lead",
            bio="Tamilselvan has 15+ years of experience in Chennai property management.",
            expertise="Legal Due Diligence, Land Acquisition",
            department="Asset Management",
            is_active=True,
            order=1
        )
        
        # Seed an active service
        self.service = Service.objects.create(
            title="Rental Management",
            slug="rental-management",
            short_description="Professional tenant screening and rent collection.",
            full_description="Detailed services covering Chennai properties.",
            features="Tenant sourcing, quarterly inspection report",
            is_active=True,
            order=1
        )
        
        # Seed property type
        self.ptype = PropertyType.objects.create(name="Villa", slug="villa")
        # Seed available property
        self.prop = Property.objects.create(
            title="Sleek Beach Villa",
            property_type=self.ptype,
            location="East Coast Road, Chennai",
            price=7500000,
            description="Luxury beachside villa along ECR.",
            status="available"
        )
        
        # Seed testimonial
        self.sec = CustomerReviewSection.objects.create(title="Happy Clients", is_active=True)
        self.review = CustomerReview.objects.create(
            section=self.sec,
            customer_name="Vijay",
            customer_location="San Jose, CA",
            service_label="Rental Management",
            quote="Great service and timely updates.",
            rating=5,
            is_active=True
        )
        
        # Seed blog post with FAQ items
        self.post = BlogPost.objects.create(
            title="Guide to NRI Property Services",
            slug="guide-nri-services",
            excerpt="Excerpt overview",
            content="""
            <h2>Frequently Asked Questions</h2>
            <strong>How do you verify tenants?</strong> We run background checks.
            <strong>What is NRI Assist?</strong> A custom service for global Indians.
            """,
            author="Propertism Team",
            is_published=True
        )

    def test_synonym_generator(self):
        syns = generate_synonyms("Tamilselvan", "Founder & Asset Management Lead")
        self.assertIn("Tamilselvan", syns)
        self.assertIn("Tamil Selvan", syns)
        self.assertIn("Mr. Tamilselvan", syns)
        self.assertIn("Advisor Tamilselvan", syns)
        self.assertIn("Relationship Manager", syns)

    def test_question_variants_generator(self):
        variants = generate_question_variants("Team", "Tamilselvan", "Who is Tamilselvan?")
        self.assertIn("Tell me about Tamilselvan.", variants)
        self.assertIn("Who is Mr. Tamilselvan?", variants)
        self.assertNotIn("Who is Tamilselvan?", variants)  # Primary question excluded from variants list

    def test_extractor_extracts_entities(self):
        extractor = WebsiteConversationalExtractor()
        entities = extractor.extract_all_entities()
        
        # Verify entity categories are extracted
        types = [e['entity_type'] for e in entities]
        self.assertIn('Company', types)
        self.assertIn('Team', types)
        self.assertIn('Service', types)
        self.assertIn('Property', types)
        self.assertIn('Testimonial', types)
        self.assertIn('FAQ', types)
        self.assertIn('Navigation', types)
        self.assertIn('GovLink', types)
        
        # Verify Tamilselvan was extracted
        team_ents = [e for e in entities if e['entity_type'] == 'Team']
        tamil_ent = next((e for e in team_ents if e['entity_name'] == "Tamilselvan"), None)
        self.assertIsNotNone(tamil_ent)
        self.assertEqual(tamil_ent['primary_question'], "Who is Tamilselvan?")

    def test_reconciliation_new_candidate(self):
        extractor = WebsiteConversationalExtractor()
        raw_candidates = extractor.extract_all_entities()
        
        reconciler = KnowledgeReconciliationEngine()
        candidates, report = reconciler.reconcile_all(raw_candidates)
        
        # Initially, with empty KnowledgeArticle table, everything is classified as 'new_candidate'
        # EXCEPT duplicates
        new_cnt = sum(1 for c in candidates if c.classification == 'new_candidate')
        self.assertTrue(new_cnt > 0)
        self.assertEqual(report['knowledge_gaps_detected'], new_cnt)

    def test_reconciliation_existing_no_action(self):
        # Create an existing matching article
        KnowledgeArticle.objects.create(
            source_ref="Conversational:Team:tamilselvan:KC000002",
            page_title="Who is Tamilselvan?",
            summary="Tamilselvan serves as Founder & Asset Management Lead at Propertism. Tamilselvan has 15+ years of experience in Chennai property management.",
            keywords="tamilselvan founder & asset management lead team advisor expertise bio specialization",
            main_content="answer content",
            published_status="published",
            status="published",
            modified_by="admin"
        )
        
        extractor = WebsiteConversationalExtractor()
        raw_candidates = extractor.extract_all_entities()
        
        reconciler = KnowledgeReconciliationEngine()
        candidates, report = reconciler.reconcile_all(raw_candidates)
        
        tamil_candidate = next((c for c in candidates if c.entity_name == "Tamilselvan"), None)
        self.assertIsNotNone(tamil_candidate)
        self.assertEqual(tamil_candidate.classification, "existing_no_action")

    def test_reconciliation_existing_update(self):
        # Create a matching article but with outdated summary
        art = KnowledgeArticle.objects.create(
            source_ref="Conversational:Team:tamilselvan:KC000002",
            page_title="Who is Tamilselvan?",
            summary="Outdated bio info.",
            keywords="tamilselvan founder & asset management lead team advisor expertise bio specialization",
            main_content="answer content",
            published_status="published",
            status="published",
            modified_by="admin"  # default system/admin user
        )
        
        extractor = WebsiteConversationalExtractor()
        raw_candidates = extractor.extract_all_entities()
        
        reconciler = KnowledgeReconciliationEngine()
        candidates, report = reconciler.reconcile_all(raw_candidates)
        
        tamil_candidate = next((c for c in candidates if c.entity_name == "Tamilselvan"), None)
        self.assertIsNotNone(tamil_candidate)
        self.assertEqual(tamil_candidate.classification, "existing_update")

    def test_reconciliation_preserves_manually_curated_knowledge(self):
        # Create a matching article that was modified by a human administrator (modified_by is NOT admin/system)
        art = KnowledgeArticle.objects.create(
            source_ref="Conversational:Team:tamilselvan:KC000002",
            page_title="Who is Tamilselvan?",
            summary="Manually curated premium bio info.",
            keywords="tamilselvan founder & asset management lead team advisor expertise bio specialization",
            main_content="answer content",
            published_status="published",
            status="published",
            modified_by="viji"  # Manual curation identifier
        )
        
        extractor = WebsiteConversationalExtractor()
        raw_candidates = extractor.extract_all_entities()
        
        reconciler = KnowledgeReconciliationEngine()
        candidates, report = reconciler.reconcile_all(raw_candidates)
        
        tamil_candidate = next((c for c in candidates if c.entity_name == "Tamilselvan"), None)
        self.assertIsNotNone(tamil_candidate)
        self.assertEqual(tamil_candidate.classification, "review_required")
        self.assertEqual(report['manual_review_items'], 1)

    def test_api_trigger_extraction(self):
        url = reverse('chat:knowledge_extraction_trigger')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('reconciliation_report', data['data'])
        self.assertTrue(data['data']['candidates_count'] > 0)

    def test_api_candidates_list(self):
        # Populate candidates first
        ExtractedKnowledgeCandidate.objects.create(
            candidate_id="KC000001",
            entity_type="Team",
            entity_name="Tamilselvan",
            primary_question="Who is Tamilselvan?",
            canonical_answer="bio text",
            classification="new_candidate",
            status="draft"
        )
        url = reverse('chat:knowledge_extraction_candidates')
        response = self.client.get(url, {'status': 'draft', 'entity_type': 'Team'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']['candidates']), 1)
        self.assertEqual(data['data']['candidates'][0]['candidate_id'], "KC000001")

    def test_api_candidate_update(self):
        c = ExtractedKnowledgeCandidate.objects.create(
            candidate_id="KC000001",
            entity_type="Team",
            entity_name="Tamilselvan",
            primary_question="Who is Tamilselvan?",
            canonical_answer="bio text",
            classification="new_candidate",
            status="draft"
        )
        url = reverse('chat:knowledge_extraction_update')
        payload = {
            'candidate_id': "KC000001",
            'canonical_answer': "Updated bio answer text",
            'keywords': "new keywords"
        }
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        c.refresh_from_db()
        self.assertEqual(c.canonical_answer, "Updated bio answer text")
        self.assertEqual(c.keywords, "new keywords")

    def test_api_candidate_approve_and_publish(self):
        c = ExtractedKnowledgeCandidate.objects.create(
            candidate_id="KC000001",
            entity_type="Team",
            entity_name="Tamilselvan",
            primary_question="Who is Tamilselvan?",
            alternative_questions=json.dumps(["Who handles Chennai advisory?", "Introduce Tamilselvan."]),
            canonical_answer="Founder & Advisor bio details",
            classification="new_candidate",
            status="draft",
            search_weight=1.5
        )
        url = reverse('chat:knowledge_extraction_approve')
        payload = {
            'candidate_ids': ["KC000001"],
            'user': 'viji'
        }
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Verify candidate updated status
        c.refresh_from_db()
        self.assertEqual(c.status, 'approved')
        self.assertIsNotNone(c.matched_article)
        
        # Verify KnowledgeArticle created in repository
        art = c.matched_article
        self.assertEqual(art.page_title, "Who is Tamilselvan?")
        self.assertEqual(art.summary, "Founder & Advisor bio details")
        self.assertEqual(art.search_weight, 1.5)
        self.assertEqual(art.modified_by, "viji")
        self.assertIn("Who handles Chennai advisory?", art.main_content)

    def test_api_candidate_reject(self):
        c = ExtractedKnowledgeCandidate.objects.create(
            candidate_id="KC000001",
            entity_type="Team",
            entity_name="Tamilselvan",
            primary_question="Who is Tamilselvan?",
            canonical_answer="bio text",
            classification="new_candidate",
            status="draft"
        )
        url = reverse('chat:knowledge_extraction_reject')
        payload = {
            'candidate_ids': ["KC000001"]
        }
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        c.refresh_from_db()
        self.assertEqual(c.status, 'rejected')
