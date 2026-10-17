"""SCCB-09 realBOT C1–C3 regression tests."""

import json
import uuid
from datetime import timedelta
from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils import timezone

from chat.models import RealBotSession, InquiryConversationSession
from chat.inquiry_engine import InquiryConversationEngine
from chat.request_limits import allow_session_init
from properties.models import Inquiry


def _session():
    return RealBotSession.objects.create(session_id=uuid.uuid4())


def _full_ics(session):
    return InquiryConversationSession.objects.create(
        realbot_session=session,
        state='collecting_information',
        source='manual_chat',
        collected_data={
            'customer_name': 'Raj Kumar',
            'country': 'Singapore',
            'mobile_number': '+65 91234567',
            'service_required': 'Buy Property',
            'inquiry_message': 'Looking for a villa in Chennai.',
            '_engine_turns': 2,
        },
        expires_at=timezone.now() + timedelta(minutes=30),
    )


def _prepare_confirm(ics):
    engine = InquiryConversationEngine()
    engine._transition_to_confirmation(ics)
    InquiryConversationSession.objects.filter(pk=ics.pk).update(
        created_at=timezone.now() - timedelta(seconds=25)
    )
    ics.refresh_from_db()
    return (ics.collected_data or {}).get('_submit_nonce')


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
class RealbotC1C3Tests(TestCase):
    def setUp(self):
        cache.clear()
        self.session = _session()

    def _post(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    @patch('content.views.send_rfq_notification')
    def test_legitimate_two_turn_submit_after_20s(self, mock_notify):
        ics = _full_ics(self.session)
        nonce = _prepare_confirm(ics)
        engine = InquiryConversationEngine()
        engine.process_message(ics, 'Yes, Submit', submit_nonce=nonce)
        ics.refresh_from_db()
        self.assertEqual(ics.state, 'submitted')
        inq = Inquiry.objects.get(pk=ics.submitted_inquiry_id)
        self.assertIn('realBOT', inq.form_source)
        self.assertNotEqual((inq.confidence_score, inq.assessment_status), (80, 'Genuine'))

    @patch('content.views.send_rfq_notification')
    def test_missing_nonce_does_not_persist(self, mock_notify):
        ics = _full_ics(self.session)
        _prepare_confirm(ics)
        engine = InquiryConversationEngine()
        engine.process_message(ics, 'Yes, Submit', submit_nonce=None)
        self.assertEqual(Inquiry.objects.count(), 0)
        ics.refresh_from_db()
        self.assertNotEqual(ics.state, 'submitted')

    @patch('content.views.send_rfq_notification')
    def test_reused_nonce_does_not_duplicate(self, mock_notify):
        ics = _full_ics(self.session)
        nonce = _prepare_confirm(ics)
        engine = InquiryConversationEngine()
        engine.process_message(ics, 'Yes, Submit', submit_nonce=nonce)
        self.assertEqual(Inquiry.objects.count(), 1)
        engine.process_message(ics, 'Yes, Submit', submit_nonce=nonce)
        self.assertEqual(Inquiry.objects.count(), 1)

    @patch('content.views.send_rfq_notification')
    def test_incomplete_ics_does_not_persist(self, mock_notify):
        ics = InquiryConversationSession.objects.create(
            realbot_session=self.session,
            state='awaiting_confirmation',
            collected_data={'customer_name': 'Only Name', '_engine_turns': 2},
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        InquiryConversationSession.objects.filter(pk=ics.pk).update(
            created_at=timezone.now() - timedelta(seconds=25)
        )
        engine = InquiryConversationEngine()
        engine.process_message(ics, 'yes', submit_nonce='x')
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_session_init_rate_limited(self):
        url = '/chat/session/init/'
        last = None
        for _ in range(6):
            last = self.client.get(url)
        self.assertEqual(last.status_code, 429)

    def test_send_message_rate_limited(self):
        url = '/chat/query/'
        last = None
        for i in range(21):
            last = self._post(url, {
                'session_id': str(self.session.session_id),
                'message': f'hello {i}',
            })
        self.assertEqual(last.status_code, 429)
        self.assertEqual(Inquiry.objects.count(), 0)

    @patch('chat.request_limits.cache.get', side_effect=Exception('cache down'))
    def test_session_init_fails_closed_when_rate_limit_cache_is_unavailable(self, mock_get):
        request = self.client.get('/chat/session/init/').wsgi_request
        self.assertFalse(allow_session_init(request))
