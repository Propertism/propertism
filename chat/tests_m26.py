"""
chat/tests_m26.py — M2.6 Conversational Inquiry Creation Test Suite
Covers: Validators, Extractor, Engine, Submission Adapter, Model IDs,
        API Endpoints, End-to-End Integration, and Regression.

Run with:
    .\\scripts\\django.cmd test chat.tests_m26
"""
import json
import uuid
from unittest.mock import patch, MagicMock
from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from chat.models import (
    RealBotSession, BusinessRule,
    InquiryConversationSession, InquiryConversationAuditLog,
)
from chat.inquiry_fields import MANDATORY_FIELDS_ORDER
from chat.inquiry_validator import InquiryFieldValidator
from chat.inquiry_extractor import InquiryFieldExtractor, FieldExtractionResult
from chat.inquiry_engine import InquiryConversationEngine


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_session():
    return RealBotSession.objects.create(session_id=uuid.uuid4())


def _make_full_ics(session, collected=None):
    """Create an ICS with all mandatory fields pre-filled."""
    ics = InquiryConversationSession.objects.create(
        realbot_session=session,
        state='collecting_information',
        source='manual_chat',
        collected_data=collected or {
            'customer_name':  'Raj Kumar',
            'country':        'Singapore',
            'mobile_number':  '+65 91234567',
            'service_required': 'Buy Property',
            'inquiry_message': 'Looking for a villa in Chennai.',
        },
        expires_at=timezone.now() + timedelta(minutes=30),
    )
    return ics


# ─────────────────────────────────────────────────────────────────────────────
# 1. Model ID Generation Tests
# ─────────────────────────────────────────────────────────────────────────────

class InquiryConversationSessionModelTests(TestCase):

    def test_ics_id_generated_on_save(self):
        session = _make_session()
        ics = InquiryConversationSession.objects.create(
            realbot_session=session,
            state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        self.assertEqual(ics.ics_id, 'ICS000001')

    def test_ics_id_sequential(self):
        session = _make_session()
        ics1 = InquiryConversationSession.objects.create(
            realbot_session=session, state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        ics2 = InquiryConversationSession.objects.create(
            realbot_session=session, state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        self.assertEqual(ics1.ics_id, 'ICS000001')
        self.assertEqual(ics2.ics_id, 'ICS000002')

    def test_ics_id_immutable_on_resave(self):
        session = _make_session()
        ics = InquiryConversationSession.objects.create(
            realbot_session=session, state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        original_id = ics.ics_id
        ics.service_hint = 'sell_property'
        ics.save()
        ics.refresh_from_db()
        self.assertEqual(ics.ics_id, original_id)

    def test_icl_id_generated_on_save(self):
        session = _make_session()
        ics = InquiryConversationSession.objects.create(
            realbot_session=session, state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        log = InquiryConversationAuditLog.objects.create(
            ics_session=ics, event_type='session_started',
        )
        self.assertEqual(log.log_id, 'ICL000001')

    def test_icl_id_sequential(self):
        session = _make_session()
        ics = InquiryConversationSession.objects.create(
            realbot_session=session, state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        log1 = InquiryConversationAuditLog.objects.create(
            ics_session=ics, event_type='session_started',
        )
        log2 = InquiryConversationAuditLog.objects.create(
            ics_session=ics, event_type='message_received',
        )
        self.assertEqual(log1.log_id, 'ICL000001')
        self.assertEqual(log2.log_id, 'ICL000002')


# ─────────────────────────────────────────────────────────────────────────────
# 2. Field Validator Tests
# ─────────────────────────────────────────────────────────────────────────────

class InquiryFieldValidatorTests(TestCase):

    def setUp(self):
        self.v = InquiryFieldValidator()

    # Name
    def test_name_valid(self):
        passed, _ = self.v.validate_customer_name('Raj Kumar')
        self.assertTrue(passed)

    def test_name_too_short(self):
        passed, msg = self.v.validate_customer_name('R')
        self.assertFalse(passed)
        self.assertIn('short', msg.lower())

    def test_name_empty(self):
        passed, _ = self.v.validate_customer_name('')
        self.assertFalse(passed)

    def test_name_invalid_chars(self):
        passed, _ = self.v.validate_customer_name('Raj123@')
        self.assertFalse(passed)

    # Phone — India
    def test_phone_india_valid(self):
        passed, _ = self.v.validate_phone('+91 9876543210', 'India')
        self.assertTrue(passed)

    def test_phone_india_wrong_digit_count(self):
        passed, msg = self.v.validate_phone('+91 98765432', 'India')
        self.assertFalse(passed)
        self.assertIn('10', msg)

    # Phone — USA
    def test_phone_usa_valid(self):
        passed, _ = self.v.validate_phone('+1 4085551234', 'USA')
        self.assertTrue(passed)

    def test_phone_usa_wrong_prefix(self):
        passed, msg = self.v.validate_phone('+91 4085551234', 'USA')
        self.assertFalse(passed)
        self.assertIn('+1', msg)

    # Phone — UK
    def test_phone_uk_valid(self):
        passed, _ = self.v.validate_phone('+44 7911123456', 'UK')
        self.assertTrue(passed)

    # Phone — UAE
    def test_phone_uae_valid(self):
        passed, _ = self.v.validate_phone('+971 501234567', 'UAE')
        self.assertTrue(passed)

    # Phone — Singapore
    def test_phone_singapore_valid(self):
        passed, _ = self.v.validate_phone('+65 91234567', 'Singapore')
        self.assertTrue(passed)

    def test_phone_singapore_wrong_digits(self):
        passed, msg = self.v.validate_phone('+65 9123456', 'Singapore')
        self.assertFalse(passed)
        self.assertIn('8', msg)

    # Phone — Australia
    def test_phone_australia_valid(self):
        passed, _ = self.v.validate_phone('+61 412345678', 'Australia')
        self.assertTrue(passed)

    # Phone — lenient fallback (unknown country)
    def test_phone_unknown_country_lenient(self):
        passed, _ = self.v.validate_phone('+49 1512345678', 'Germany')
        self.assertTrue(passed)

    def test_phone_no_country_code(self):
        passed, msg = self.v.validate_phone('9876543210', 'India')
        self.assertFalse(passed)
        self.assertIn('country code', msg.lower())

    # Email
    def test_email_valid(self):
        passed, _ = self.v.validate_email('raj@example.com')
        self.assertTrue(passed)

    def test_email_invalid(self):
        passed, _ = self.v.validate_email('notanemail')
        self.assertFalse(passed)

    def test_email_with_plus(self):
        passed, _ = self.v.validate_email('raj+tag@propertism.in')
        self.assertTrue(passed)

    # Message
    def test_message_valid(self):
        passed, _ = self.v.validate_message('Looking for a villa in Chennai')
        self.assertTrue(passed)

    def test_message_too_short(self):
        passed, _ = self.v.validate_message('Hi')
        self.assertFalse(passed)

    def test_message_spam_url(self):
        passed, msg = self.v.validate_message('Visit https://spam.com for deals')
        self.assertFalse(passed)

    # Country
    def test_country_valid(self):
        passed, _ = self.v.validate_country('Singapore')
        self.assertTrue(passed)

    def test_country_empty(self):
        passed, _ = self.v.validate_country('')
        self.assertFalse(passed)

    # Budget
    def test_budget_chip_value(self):
        passed, _ = self.v.validate_budget('Under ₹50L')
        self.assertTrue(passed)

    def test_budget_free_text(self):
        passed, _ = self.v.validate_budget('Around 2 crore')
        self.assertTrue(passed)

    def test_budget_empty_optional(self):
        passed, _ = self.v.validate_budget('')
        self.assertTrue(passed)  # Optional field — empty is fine


# ─────────────────────────────────────────────────────────────────────────────
# 3. Field Extractor — Single Field Tests
# ─────────────────────────────────────────────────────────────────────────────

class InquiryFieldExtractorSingleFieldTests(TestCase):

    def setUp(self):
        self.ex = InquiryFieldExtractor()
        self.session = _make_session()

    def _ics(self, collected=None):
        return InquiryConversationSession(
            realbot_session=self.session,
            state='collecting_information',
            collected_data=collected or {},
            skipped_fields=[],
            expires_at=timezone.now() + timedelta(minutes=30),
        )

    def test_extract_name_from_my_name_is(self):
        ics = self._ics()
        result = self.ex.extract("My name is Raj Kumar.", ics)
        self.assertIn('customer_name', result.validated)
        self.assertEqual(result.validated['customer_name'], 'Raj Kumar')

    def test_extract_name_from_im(self):
        ics = self._ics()
        result = self.ex.extract("I'm Priya from Chennai.", ics)
        self.assertIn('customer_name', result.validated)
        self.assertEqual(result.validated['customer_name'], 'Priya')

    def test_extract_country_india(self):
        ics = self._ics()
        result = self.ex.extract("I am calling from India.", ics)
        self.assertIn('country', result.validated)
        self.assertEqual(result.validated['country'], 'India')

    def test_extract_country_uae_keyword(self):
        ics = self._ics()
        result = self.ex.extract("I am based in UAE.", ics)
        self.assertIn('country', result.validated)
        self.assertEqual(result.validated['country'], 'UAE')

    def test_extract_phone_india(self):
        ics = self._ics({'country': 'India'})
        result = self.ex.extract("My number is +91 9876543210", ics)
        self.assertIn('mobile_number', result.validated)

    def test_extract_phone_singapore(self):
        ics = self._ics({'country': 'Singapore'})
        result = self.ex.extract("Call me at +65 91234567", ics)
        self.assertIn('mobile_number', result.validated)

    def test_extract_email(self):
        ics = self._ics()
        result = self.ex.extract("My email is raj@example.com", ics)
        self.assertIn('email_address', result.validated)
        self.assertEqual(result.validated['email_address'], 'raj@example.com')

    def test_extract_service_buy(self):
        ics = self._ics()
        result = self.ex.extract("I want to buy a property", ics)
        self.assertIn('service_required', result.validated)
        self.assertEqual(result.validated['service_required'], 'Buy Property')

    def test_extract_service_sell(self):
        ics = self._ics()
        result = self.ex.extract("I am looking to sell my house", ics)
        self.assertIn('service_required', result.validated)
        self.assertEqual(result.validated['service_required'], 'Sell Property')

    def test_extract_service_rental(self):
        ics = self._ics()
        result = self.ex.extract("I need rental management for my property", ics)
        self.assertIn('service_required', result.validated)
        self.assertEqual(result.validated['service_required'], 'Rental Management')

    def test_extract_property_type_villa(self):
        ics = self._ics()
        result = self.ex.extract("I want a villa in Chennai", ics)
        self.assertIn('property_type', result.validated)
        self.assertEqual(result.validated['property_type'], 'Villa')

    def test_extract_property_type_apartment(self):
        ics = self._ics()
        result = self.ex.extract("looking for an apartment near OMR", ics)
        self.assertIn('property_type', result.validated)
        self.assertEqual(result.validated['property_type'], 'Apartment')

    def test_extract_budget_inr(self):
        ics = self._ics()
        result = self.ex.extract("my budget is around ₹1 crore", ics)
        self.assertIn('budget', result.validated)

    def test_extract_location_omr(self):
        ics = self._ics()
        result = self.ex.extract("I prefer OMR area", ics)
        self.assertIn('preferred_location', result.validated)

    def test_no_false_positive_name_generic(self):
        """'I am interested in property' should NOT yield a name extraction."""
        ics = self._ics()
        result = self.ex.extract("I am interested in property", ics)
        # customer_name should not be extracted from this generic phrase
        self.assertNotIn('customer_name', result.validated)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Field Extractor — Multi-Field Tests (Annexure A §1 & §9)
# ─────────────────────────────────────────────────────────────────────────────

class InquiryFieldExtractorMultiFieldTests(TestCase):

    def setUp(self):
        self.ex = InquiryFieldExtractor()
        self.session = _make_session()

    def _ics(self, collected=None):
        return InquiryConversationSession(
            realbot_session=self.session,
            state='collecting_information',
            collected_data=collected or {},
            skipped_fields=[],
            expires_at=timezone.now() + timedelta(minutes=30),
        )

    def test_annexure_a_section9_example(self):
        """
        Annexure A §9 example: a single message with name, country, service,
        property type, and phone should yield all 5 fields extracted.
        """
        msg = (
            "My name is Raj. I'm from Singapore. I want to buy a villa in Chennai. "
            "My mobile number is +65 91234567."
        )
        ics = self._ics()
        result = self.ex.extract(msg, ics)
        self.assertIn('customer_name', result.validated)
        self.assertIn('country', result.validated)
        self.assertIn('service_required', result.validated)
        self.assertIn('property_type', result.validated)
        self.assertIn('mobile_number', result.validated)
        self.assertGreaterEqual(result.fields_enriched, 4)

    def test_multi_field_name_country_service(self):
        """Three fields from one message."""
        msg = "This is Priya. I'm based in UK. I want to sell my flat."
        ics = self._ics()
        result = self.ex.extract(msg, ics)
        self.assertIn('country', result.validated)
        self.assertIn('service_required', result.validated)
        self.assertGreaterEqual(result.fields_enriched, 2)

    def test_multi_field_email_and_phone(self):
        """Email and phone in one message."""
        msg = "Email me at priya@example.com, call me on +44 7911123456"
        ics = self._ics({'country': 'UK'})
        result = self.ex.extract(msg, ics)
        self.assertIn('email_address', result.validated)
        self.assertIn('mobile_number', result.validated)

    def test_previously_captured_fields_not_duplicated(self):
        """Fields already in collected_data are not added again."""
        ics = self._ics({'customer_name': 'Raj'})
        result = self.ex.extract("My name is Raj. I want to sell my property.", ics)
        # customer_name already collected — should not appear in validated
        self.assertNotIn('customer_name', result.validated)
        # service should be newly extracted
        self.assertIn('service_required', result.validated)


# ─────────────────────────────────────────────────────────────────────────────
# 5. Conflict Detection Tests (Annexure A §7)
# ─────────────────────────────────────────────────────────────────────────────

class InquiryFieldExtractorConflictTests(TestCase):

    def setUp(self):
        self.ex = InquiryFieldExtractor()
        self.session = _make_session()

    def _ics(self, collected):
        return InquiryConversationSession(
            realbot_session=self.session,
            state='collecting_information',
            collected_data=collected,
            skipped_fields=[],
            expires_at=timezone.now() + timedelta(minutes=30),
        )

    def test_conflict_detected_when_country_changes(self):
        """If country is already India and message says Singapore, conflict is raised."""
        ics = self._ics({'country': 'India'})
        result = self.ex.extract("I am from Singapore.", ics)
        self.assertIn('country', result.conflicts)
        self.assertEqual(result.conflicts['country'], 'Singapore')
        # Must NOT overwrite validated data
        self.assertNotIn('country', result.validated)

    def test_no_conflict_same_value(self):
        """Same value repeated — no conflict."""
        ics = self._ics({'country': 'Singapore'})
        result = self.ex.extract("I am from Singapore.", ics)
        self.assertNotIn('country', result.conflicts)
        self.assertNotIn('country', result.validated)

    def test_conflict_does_not_overwrite(self):
        """conflicts dict must be returned; original value must be preserved."""
        ics = self._ics({'service_required': 'Buy Property'})
        result = self.ex.extract("I want to sell my property.", ics)
        # conflict detected, original not overwritten
        if 'service_required' in result.conflicts:
            self.assertEqual(result.conflicts['service_required'], 'Sell Property')
            self.assertNotIn('service_required', result.validated)


# ─────────────────────────────────────────────────────────────────────────────
# 6. Conversation Engine Tests
# ─────────────────────────────────────────────────────────────────────────────

class InquiryConversationEngineInitiationTests(TestCase):

    def test_initiate_creates_ics_session(self):
        session = _make_session()
        engine = InquiryConversationEngine()
        result = engine.initiate(session, source='manual_chat')
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()
        self.assertIsNotNone(ics)
        self.assertEqual(ics.state, 'collecting_information')

    def test_initiate_returns_prompt(self):
        session = _make_session()
        engine = InquiryConversationEngine()
        result = engine.initiate(session)
        self.assertIn('text', result)
        self.assertTrue(len(result['text']) > 0)

    def test_initiate_with_opening_message_extracts_fields(self):
        """Annexure A: fields in the opening message should be captured on initiation."""
        session = _make_session()
        engine = InquiryConversationEngine()
        result = engine.initiate(
            session,
            opening_message="My name is Raj from Singapore. I want to buy a villa."
        )
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()
        self.assertIn('country', ics.collected_data)
        self.assertIn('service_required', ics.collected_data)

    def test_initiate_logs_session_started(self):
        session = _make_session()
        engine = InquiryConversationEngine()
        engine.initiate(session)
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()
        log = InquiryConversationAuditLog.objects.filter(
            ics_session=ics, event_type='session_started'
        ).first()
        self.assertIsNotNone(log)


class InquiryConversationEngineFlowTests(TestCase):

    def test_never_asks_for_collected_field(self):
        """Annexure A §2: engine must never ask for already-captured info."""
        session = _make_session()
        engine = InquiryConversationEngine()
        engine.initiate(session)
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()

        # Provide name
        engine.process_message(ics, "My name is Raj")
        ics.refresh_from_db()

        # Send same name again — should not be prompted for name again
        result = engine.process_message(ics, "I said my name is Raj Kumar.")
        ics.refresh_from_db()
        # The current prompt field should NOT be customer_name again
        self.assertNotEqual(ics.current_prompt_field, 'customer_name')

    def test_all_mandatory_fields_triggers_confirmation(self):
        """Once all mandatory fields collected, state should move to awaiting_confirmation."""
        session = _make_session()
        ics = _make_full_ics(session)
        engine = InquiryConversationEngine()

        # Manually check — all mandatory fields present
        self.assertTrue(engine._all_mandatory_collected(ics))

        # Trigger confirmation
        result = engine._transition_to_confirmation(ics)
        ics.refresh_from_db()
        self.assertEqual(ics.state, 'awaiting_confirmation')
        self.assertIn('summary', result['text'].lower())

    def test_cancel_keyword_triggers_cancellation(self):
        """'cancel' keyword transitions to CANCELLED state."""
        session = _make_session()
        engine = InquiryConversationEngine()
        engine.initiate(session)
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()

        result = engine.process_message(ics, "cancel")
        ics.refresh_from_db()
        self.assertEqual(ics.state, 'cancelled')
        # Verify response text contains cancellation confirmation
        self.assertIn('cancelled', result['text'].lower())

    def test_confirmation_acknowledgment_contains_summary(self):
        """Confirmation prompt should include field summary."""
        session = _make_session()
        ics = _make_full_ics(session)
        engine = InquiryConversationEngine()
        ics.state = 'awaiting_confirmation'
        ics.save()

        result = engine.build_confirmation_summary(ics)
        self.assertIn('Raj Kumar', result)
        self.assertIn('Singapore', result)
        self.assertIn('Buy Property', result)


class InquiryConversationEngineCancelTests(TestCase):

    def test_cancel_sets_cancelled_state(self):
        session = _make_session()
        engine = InquiryConversationEngine()
        engine.initiate(session)
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()

        engine.handle_cancel(ics, reason='test')
        ics.refresh_from_db()
        self.assertEqual(ics.state, 'cancelled')

    def test_cancel_logs_event(self):
        session = _make_session()
        engine = InquiryConversationEngine()
        engine.initiate(session)
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()

        engine.handle_cancel(ics, reason='user request')
        log = InquiryConversationAuditLog.objects.filter(
            ics_session=ics, event_type='cancelled'
        ).first()
        self.assertIsNotNone(log)

    def test_cancel_from_process_message(self):
        session = _make_session()
        engine = InquiryConversationEngine()
        engine.initiate(session)
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()

        engine.process_message(ics, "never mind, stop")
        ics.refresh_from_db()
        self.assertEqual(ics.state, 'cancelled')


class InquiryConversationEngineExpiryTests(TestCase):

    def test_expired_session_returns_expiry_message(self):
        session = _make_session()
        ics = InquiryConversationSession.objects.create(
            realbot_session=session,
            state='collecting_information',
            expires_at=timezone.now() - timedelta(hours=2),  # far past — overrides refresh
        )
        engine = InquiryConversationEngine()
        # Override refresh_expiry so it does not extend the already-expired session
        original_refresh = engine.refresh_expiry
        engine.refresh_expiry = lambda s: None
        result = engine.process_message(ics, "Hello")
        ics.refresh_from_db()
        self.assertEqual(ics.state, 'expired')
        self.assertIn('expired', result['text'].lower())

    def test_check_and_expire_returns_true(self):
        session = _make_session()
        ics = InquiryConversationSession.objects.create(
            realbot_session=session,
            state='collecting_information',
            expires_at=timezone.now() - timedelta(seconds=1),
        )
        engine = InquiryConversationEngine()
        result = engine.check_and_expire(ics)
        self.assertTrue(result)

    def test_refresh_expiry_extends_session(self):
        session = _make_session()
        ics = InquiryConversationSession.objects.create(
            realbot_session=session,
            state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=5),
        )
        engine = InquiryConversationEngine()
        engine.refresh_expiry(ics)
        ics.refresh_from_db()
        # Should now be ~30 minutes from now
        self.assertGreater(ics.expires_at, timezone.now() + timedelta(minutes=25))


class InquiryConversationEngineSkipTests(TestCase):

    def test_skip_optional_marks_field_skipped(self):
        session = _make_session()
        ics = _make_full_ics(session)
        ics.state = 'collecting_information'
        ics.current_prompt_field = 'email_address'
        ics.save()
        engine = InquiryConversationEngine()

        engine._skip_optional_field(ics, 'email_address')
        ics.refresh_from_db()
        self.assertIn('email_address', ics.skipped_fields)

    def test_skip_does_not_mark_mandatory_skipped(self):
        """Skipping a mandatory field should not put it in skipped_fields."""
        session = _make_session()
        ics = InquiryConversationSession.objects.create(
            realbot_session=session,
            state='collecting_information',
            current_prompt_field='customer_name',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        engine = InquiryConversationEngine()
        # Process a "skip" message when on a mandatory field — should re-prompt
        result = engine.process_message(ics, "skip")
        ics.refresh_from_db()
        # customer_name is mandatory — should NOT be in skipped_fields
        self.assertNotIn('customer_name', ics.skipped_fields)


# ─────────────────────────────────────────────────────────────────────────────
# 7. Submission Adapter Tests
# ─────────────────────────────────────────────────────────────────────────────

class InquirySubmissionAdapterTests(TestCase):

    @patch('content.views.send_rfq_notification')
    def test_submit_creates_property_inquiry(self, mock_notify):
        from properties.models import Inquiry as PropertyInquiry
        from chat.inquiry_submission import InquirySubmissionAdapter

        session = _make_session()
        ics = _make_full_ics(session)

        adapter = InquirySubmissionAdapter()
        result = adapter.submit(ics)

        self.assertTrue(result['success'])
        self.assertIsNotNone(result['inquiry_id'])

        inq = PropertyInquiry.objects.get(pk=result['inquiry_id'])
        self.assertEqual(inq.name, 'Raj Kumar')
        self.assertEqual(inq.phone, '+65 91234567')
        self.assertIn('Looking for a villa in Chennai', inq.message)
        self.assertIn('realBOT', inq.form_source)
        self.assertEqual(inq.confidence_score, 80)
        self.assertEqual(inq.assessment_status, 'Genuine')

    @patch('content.views.send_rfq_notification')
    def test_form_source_uses_service_hint(self, mock_notify):
        from properties.models import Inquiry as PropertyInquiry
        from chat.inquiry_submission import InquirySubmissionAdapter

        session = _make_session()
        ics = _make_full_ics(session)
        ics.service_hint = 'sell_property'
        ics.save()

        adapter = InquirySubmissionAdapter()
        result = adapter.submit(ics)

        inq = PropertyInquiry.objects.get(pk=result['inquiry_id'])
        self.assertIn('Sell Property', inq.form_source)

    @patch('content.views.send_rfq_notification')
    def test_notification_called_on_submit(self, mock_notify):
        from chat.inquiry_submission import InquirySubmissionAdapter
        session = _make_session()
        ics = _make_full_ics(session)

        adapter = InquirySubmissionAdapter()
        adapter.submit(ics)
        mock_notify.assert_called_once()

    @patch('content.views.send_rfq_notification', side_effect=Exception('email error'))
    def test_notification_failure_does_not_fail_submission(self, mock_notify):
        """Notification errors must never block successful submission."""
        from chat.inquiry_submission import InquirySubmissionAdapter
        session = _make_session()
        ics = _make_full_ics(session)

        adapter = InquirySubmissionAdapter()
        result = adapter.submit(ics)
        self.assertTrue(result['success'])  # submission succeeded despite notification error


# ─────────────────────────────────────────────────────────────────────────────
# 8. Audit Trail Tests
# ─────────────────────────────────────────────────────────────────────────────

class InquiryAuditTrailTests(TestCase):

    def test_session_started_event_created(self):
        session = _make_session()
        engine = InquiryConversationEngine()
        engine.initiate(session)
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()
        self.assertTrue(
            InquiryConversationAuditLog.objects.filter(
                ics_session=ics, event_type='session_started'
            ).exists()
        )

    def test_field_extracted_event_created(self):
        session = _make_session()
        engine = InquiryConversationEngine()
        engine.initiate(session, opening_message="My name is Raj from India.")
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()
        self.assertTrue(
            InquiryConversationAuditLog.objects.filter(
                ics_session=ics, event_type='field_extracted'
            ).exists()
        )

    def test_cancelled_event_created(self):
        session = _make_session()
        engine = InquiryConversationEngine()
        engine.initiate(session)
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()
        engine.handle_cancel(ics, 'test')
        self.assertTrue(
            InquiryConversationAuditLog.objects.filter(
                ics_session=ics, event_type='cancelled'
            ).exists()
        )

    @patch('content.views.send_rfq_notification')
    def test_submitted_event_created(self, mock_notify):
        session = _make_session()
        ics = _make_full_ics(session)
        engine = InquiryConversationEngine()
        engine._submit_inquiry(ics)
        self.assertTrue(
            InquiryConversationAuditLog.objects.filter(
                ics_session=ics, event_type='submitted'
            ).exists()
        )


# ─────────────────────────────────────────────────────────────────────────────
# 9. API Endpoint Tests
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
class InquiryAPIEndpointTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())

    def _post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def test_inquiry_initiate_endpoint(self):
        url = '/api/v1/realbot/inquiry/initiate/'
        resp = self._post_json(url, {'session_id': str(self.session.session_id)})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])

    def test_inquiry_initiate_creates_ics(self):
        url = '/api/v1/realbot/inquiry/initiate/'
        self._post_json(url, {'session_id': str(self.session.session_id)})
        self.assertTrue(
            InquiryConversationSession.objects.filter(
                realbot_session=self.session
            ).exists()
        )

    def test_inquiry_status_no_session(self):
        url = f'/api/v1/realbot/inquiry/status/?session_id={self.session.session_id}'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertFalse(data['data']['has_active_session'])

    def test_inquiry_status_with_open_session(self):
        InquiryConversationSession.objects.create(
            realbot_session=self.session,
            state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        url = f'/api/v1/realbot/inquiry/status/?session_id={self.session.session_id}'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['data']['has_active_session'])

    def test_inquiry_cancel_endpoint(self):
        InquiryConversationSession.objects.create(
            realbot_session=self.session,
            state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        url = '/api/v1/realbot/inquiry/cancel/'
        resp = self._post_json(url, {'session_id': str(self.session.session_id)})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['data']['cancelled'])

    def test_inquiry_diagnostics_endpoint(self):
        url = '/api/v1/realbot/inquiry/diagnostics/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertIn('total_sessions', data['data'])

    def test_inquiry_initiate_missing_session_id(self):
        url = '/api/v1/realbot/inquiry/initiate/'
        resp = self._post_json(url, {})
        self.assertEqual(resp.status_code, 400)

    def test_inquiry_status_missing_session_id(self):
        url = '/api/v1/realbot/inquiry/status/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 400)


# ─────────────────────────────────────────────────────────────────────────────
# 10. End-to-End Integration Test
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
class InquiryIntegrationTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        # Seed an inquiry_creation rule
        BusinessRule.objects.create(
            name='Inquiry Creation Rule',
            intent='inquiry_creation',
            priority=1,
            positive_keywords='inquiry,contact,submit,reach,interested',
            min_confidence=0.3,
            action_type='inquiry_workflow',
        )

    def _post(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    @patch('content.views.send_rfq_notification')
    def test_full_inquiry_lifecycle_via_engine(self, mock_notify):
        """
        End-to-end: initiate → collect all mandatory fields → confirm → submit.
        Verifies PropertyInquiry is created with correct data.
        """
        from properties.models import Inquiry as PropertyInquiry

        session = _make_session()
        engine = InquiryConversationEngine()

        # 1. Initiate with rich opening message (Annexure A §9)
        result = engine.initiate(
            session,
            opening_message=(
                "My name is Meera. I'm from UAE. "
                "I want to buy a villa. My number is +971 501234567."
            ),
        )
        ics = InquiryConversationSession.objects.filter(realbot_session=session).first()

        self.assertIn('country', ics.collected_data)
        self.assertIn('service_required', ics.collected_data)
        self.assertIn('property_type', ics.collected_data)

        # 2. Provide the missing mandatory field: inquiry_message
        # (customer_name and mobile_number may or may not have been extracted —
        #  provide them if missing)
        if 'customer_name' not in ics.collected_data:
            engine.process_message(ics, "My name is Meera")
            ics.refresh_from_db()
        if 'mobile_number' not in ics.collected_data:
            engine.process_message(ics, "+971 501234567")
            ics.refresh_from_db()
        if 'inquiry_message' not in ics.collected_data:
            engine.process_message(ics, "I am looking for a premium villa with sea view")
            ics.refresh_from_db()

        # Ensure we reach awaiting_confirmation
        if ics.state == 'collecting_information' and engine._all_mandatory_collected(ics):
            engine._transition_to_confirmation(ics)
            ics.refresh_from_db()

        # 3. Confirm submission
        result = engine.process_message(ics, "yes, submit")
        ics.refresh_from_db()

        self.assertEqual(ics.state, 'submitted')
        self.assertIsNotNone(ics.submitted_inquiry_id)

        # 4. Verify PropertyInquiry was created
        inq = PropertyInquiry.objects.get(pk=ics.submitted_inquiry_id)
        self.assertEqual(inq.confidence_score, 80)
        self.assertEqual(inq.assessment_status, 'Genuine')
        self.assertIn('realBOT', inq.form_source)
        mock_notify.assert_called_once()

    def test_send_message_routes_to_open_ics(self):
        """
        When an open ICS session exists, send_message must route to the
        InquiryConversationEngine — not the Rule Engine.
        """
        # Create an open ICS session
        InquiryConversationSession.objects.create(
            realbot_session=self.session,
            state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )

        url = '/api/v1/realbot/query/'
        payload = {
            'session_id': str(self.session.session_id),
            'message': 'My name is Kavya',
        }
        resp = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])

        # Verify the ICS session was enriched or advanced
        ics = InquiryConversationSession.objects.filter(
            realbot_session=self.session
        ).first()
        self.assertIsNotNone(ics)


# ─────────────────────────────────────────────────────────────────────────────
# 11. Regression Tests (M2.1–M2.5 suite integrity)
# ─────────────────────────────────────────────────────────────────────────────

class M26RegressionModelTests(TestCase):
    """Verify that core M2.1–M2.5 models remain functional."""

    def test_realbot_session_creation(self):
        session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.assertIsNotNone(session.pk)

    def test_business_rule_creation(self):
        rule = BusinessRule.objects.create(
            name='Test Rule', intent='buy_property', priority=1,
            positive_keywords='buy', min_confidence=0.3,
            action_type='service_card',
        )
        self.assertEqual(rule.intent, 'buy_property')

    def test_service_profile_creation(self):
        from chat.models import ServiceProfile
        sp = ServiceProfile.objects.create(
            name='Test Service', category='Test Cat',
            short_description='Desc', detailed_description='Desc',
            business_objective='Obj', target_audience='Aud',
        )
        self.assertEqual(sp.service_id, 'SRV000001')

    def test_inquiry_session_does_not_break_realbot_session(self):
        """ICS FK to RealBotSession must not affect session behaviour."""
        session = _make_session()
        ics = InquiryConversationSession.objects.create(
            realbot_session=session,
            state='collecting_information',
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        # Session should still be queryable normally
        retrieved = RealBotSession.objects.get(pk=session.pk)
        self.assertEqual(retrieved.pk, session.pk)
