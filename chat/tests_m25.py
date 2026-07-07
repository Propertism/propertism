"""
chat/tests_m25.py — M2.5 Service Coverage Framework Test Suite
Run with:
    .\\scripts\\django.cmd test chat.tests_m25
"""
import json
import uuid
from django.test import TestCase, override_settings
from chat.models import ServiceProfile, RealBotSession, BusinessRule
from chat.service_builder import ServiceResponseBuilder
from chat.action_handlers import ActionDispatcher, ActionResponse


# ==============================================================================
# ServiceProfile Model Tests
# ==============================================================================

class ServiceProfileModelTests(TestCase):

    def test_service_id_auto_generation(self):
        """First ServiceProfile should get SRV000001."""
        srv = ServiceProfile.objects.create(
            name="Buy Property",
            category="Property Acquisition",
            short_description="Short desc",
            detailed_description="Detailed desc",
            business_objective="Obj",
            target_audience="Audience"
        )
        self.assertEqual(srv.service_id, "SRV000001")

    def test_service_id_sequential(self):
        """Consecutive ServiceProfiles get sequential SRV IDs."""
        s1 = ServiceProfile.objects.create(
            name="S1", category="Cat", short_description="D",
            detailed_description="D", business_objective="O", target_audience="A"
        )
        s2 = ServiceProfile.objects.create(
            name="S2", category="Cat", short_description="D",
            detailed_description="D", business_objective="O", target_audience="A"
        )
        self.assertEqual(s1.service_id, "SRV000001")
        self.assertEqual(s2.service_id, "SRV000002")

    def test_service_id_immutable(self):
        """Saving an existing profile preserves the service_id."""
        srv = ServiceProfile.objects.create(
            name="S1", category="Cat", short_description="D",
            detailed_description="D", business_objective="O", target_audience="A"
        )
        original_id = srv.service_id
        srv.display_priority = 5
        srv.save()
        srv.refresh_from_db()
        self.assertEqual(srv.service_id, original_id)


# ==============================================================================
# ServiceResponseBuilder Parsing Tests
# ==============================================================================

class ServiceResponseBuilderTests(TestCase):

    def setUp(self):
        self.profile = ServiceProfile.objects.create(
            name="Buy Property",
            category="Property Acquisition",
            short_description="Buying assist.",
            detailed_description="Detailed lifespan buy guidance.",
            business_objective="Safe buying.",
            target_audience="Homebuyers.",
            eligibility="Min budget of ₹30 Lakhs, Income proof",
            required_inputs="PAN Card, Aadhaar Card, Parent deeds",
            advisory_content={
                'overview': 'General buy overview details.',
                'benefits': 'Legal safety, structural audit checks, registration guide',
                'process': '1. Sourcing → 2. Verification → 3. Agreement',
                'pricing': '1% commission fee.',
                'limitations': 'No unapproved layouts matching CMDA/DTCP.'
            },
            faqs=[
                {'q': 'What is fee?', 'a': '1% of registration.'}
            ],
            call_to_actions=[
                {'label': 'Schedule Viewing', 'action': 'property_viewing'}
            ]
        )

    def test_detect_documents_subtopic(self):
        """Query containing 'documents' or 'pan card' returns required inputs section."""
        builder = ServiceResponseBuilder()
        res = builder.build_response(self.profile, "what documents are required?")
        self.assertIn("PAN Card", res['text'])
        self.assertIn("Aadhaar Card", res['text'])

    def test_detect_process_subtopic(self):
        """Query containing 'process' returns formatted step list."""
        builder = ServiceResponseBuilder()
        res = builder.build_response(self.profile, "what is the buying process steps?")
        self.assertIn("1. Sourcing", res['text'])
        self.assertIn("2. Verification", res['text'])

    def test_detect_pricing_subtopic(self):
        """Query containing 'fees' or 'charges' returns pricing details."""
        builder = ServiceResponseBuilder()
        res = builder.build_response(self.profile, "how much are the fees and charges?")
        self.assertIn("1% commission fee.", res['text'])

    def test_default_overview_fallback(self):
        """Broad queries without subtopic keywords return overview/details description."""
        builder = ServiceResponseBuilder()
        res = builder.build_response(self.profile, "tell me about this service")
        self.assertIn("Detailed lifespan buy guidance.", res['text'])
        self.assertIn("Safe buying.", res['text'])


# ==============================================================================
# End-to-End Service Integration & API Tests
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
class SendMessageServiceIntegrationTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        
        # Seed Rule
        BusinessRule.objects.create(
            name="Buy Rule", intent="buy_property", priority=1,
            positive_keywords="buy,purchase", min_confidence=0.3,
            action_type="service_card"
        )
        
        # Seed Service Profile matching INTENT_TO_SERVICE_MAP lookup for intent "buy_property"
        self.profile = ServiceProfile.objects.create(
            name="Buy Property",
            category="Property Acquisition",
            short_description="Buying assist.",
            detailed_description="Detailed buying guidance.",
            business_objective="Safe buying.",
            target_audience="Homebuyers.",
            eligibility="Min budget of ₹30 Lakhs",
            required_inputs="PAN, Aadhaar",
            advisory_content={
                'process': '1. Sourcing → 2. Verification',
            },
            call_to_actions=[
                {'label': 'Schedule Viewing', 'action': 'property_viewing'}
            ]
        )

    def test_send_message_routes_to_service_profile(self):
        """Querying 'buy property' should resolve intent 'buy_property', fetch profile, and build response."""
        url = '/api/v1/realbot/query/'
        payload = {
            "session_id": str(self.session.session_id),
            "message": "tell me how to buy property"
        }
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        msg = data['data']['message']
        
        # Verify text is generated dynamically from Service Profile
        self.assertIn("Buy Property", msg['text'])
        self.assertIn("Property Acquisition", msg['text'])
        
        # Verify metadata properties populated from Service Profile
        self.assertEqual(msg['metadata']['service']['service_id'], self.profile.service_id)
        self.assertEqual(msg['metadata']['call_to_actions'][0]['label'], 'Schedule Viewing')


class ServiceAdminEndpointsTests(TestCase):

    def setUp(self):
        self.s1 = ServiceProfile.objects.create(
            name="Service A", category="Cat A", short_description="Desc",
            detailed_description="Desc", business_objective="Obj", target_audience="Aud"
        )
        self.s2 = ServiceProfile.objects.create(
            name="Service B", category="Cat B", short_description="Desc",
            detailed_description="Desc", business_objective="Obj", target_audience="Aud"
        )

    def test_list_services(self):
        response = self.client.get('/api/v1/realbot/services/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['total_services'], 2)

    def test_services_diagnostics(self):
        response = self.client.get('/api/v1/realbot/services/diagnostics/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['active'], 2)
        self.assertEqual(data['data']['inactive'], 0)
