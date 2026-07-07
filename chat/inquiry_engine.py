"""
chat/inquiry_engine.py — M2.6 Adaptive Conversation Engine & State Manager

Orchestrates the full inquiry conversation lifecycle:
  1. Initiates a new InquiryConversationSession.
  2. Processes every customer message through the Deterministic Field Extractor.
  3. Progressively enriches the session with extracted fields.
  4. Handles conflict resolution (Annexure A §7).
  5. Determines next missing mandatory field and prompts only for that.
  6. Transitions to confirmation when all mandatory fields are collected.
  7. On customer confirmation, delegates submission to InquirySubmissionAdapter.
  8. Records every event in the append-only audit log.

The engine NEVER persists PropertyInquiry records — that is delegated exclusively
to InquirySubmissionAdapter → properties.Inquiry.objects.create().
"""
import logging
from datetime import timedelta

from django.utils import timezone

from chat.models import InquiryConversationSession, InquiryConversationAuditLog
from chat.inquiry_fields import (
    INQUIRY_FIELD_CONFIG,
    MANDATORY_FIELDS_ORDER,
    OPTIONAL_FIELDS_ORDER,
    CANCEL_KEYWORDS,
    CONFIRM_KEYWORDS,
    SKIP_KEYWORDS,
)
from chat.inquiry_extractor import InquiryFieldExtractor
from chat.inquiry_validator import InquiryFieldValidator

logger = logging.getLogger(__name__)

SESSION_EXPIRY_MINUTES = 30

OPEN_STATES = frozenset([
    'collecting_information',
    'awaiting_conflict_resolution',
    'awaiting_confirmation',
])


# ── Response builder helpers ──────────────────────────────────────────────────

def _build_engine_response(text: str, chips: list = None, metadata: dict = None) -> dict:
    return {
        'text': text,
        'metadata': {
            'chips': chips or [],
            'inquiry': metadata or {},
        },
    }


def _ack_extracted(new_fields: dict) -> str:
    """Build a brief, natural acknowledgment for newly extracted fields."""
    if not new_fields:
        return ''
    parts = []
    label_map = {k: v['label'] for k, v in INQUIRY_FIELD_CONFIG.items()}
    for field_name, value in new_fields.items():
        label = label_map.get(field_name, field_name.replace('_', ' ').title())
        parts.append(f"**{label}**: {value}")
    joined = ', '.join(parts)
    return f"Got it — I've noted {joined}. "


# ── Audit helper ──────────────────────────────────────────────────────────────

def _log_event(ics_session, event_type: str, field_name: str = '',
               raw_input: str = '', extracted_value: str = '', notes: str = ''):
    try:
        InquiryConversationAuditLog.objects.create(
            ics_session=ics_session,
            event_type=event_type,
            field_name=field_name,
            raw_input=raw_input[:2000],
            extracted_value=extracted_value[:500],
            notes=notes[:500],
        )
    except Exception as exc:
        logger.warning(f'[InquiryEngine] Audit log write failed: {exc}')


# ── Main engine ───────────────────────────────────────────────────────────────

class InquiryConversationEngine:
    """
    Adaptive, progressive conversation engine for M2.6.
    Instantiate per-request — stateless internally; all state lives in DB.
    """

    def __init__(self):
        self._extractor = InquiryFieldExtractor()
        self._validator = InquiryFieldValidator()

    # ── Initiation ─────────────────────────────────────────────────────────────

    def initiate(self, realbot_session, source: str = 'manual_chat',
                 service_hint: str = '', opening_message: str = '') -> dict:
        """
        Create a new InquiryConversationSession.
        If opening_message is supplied, run the extractor immediately
        so fields mentioned in the first message are captured at once.
        """
        ics = InquiryConversationSession.objects.create(
            realbot_session=realbot_session,
            state='collecting_information',
            source=source,
            service_hint=service_hint,
            expires_at=timezone.now() + timedelta(minutes=SESSION_EXPIRY_MINUTES),
        )
        _log_event(ics, 'session_started', notes=f'source={source} hint={service_hint}')

        # If an opening message was provided, run extraction immediately
        extraction_ack = ''
        if opening_message:
            extraction_result = self._extractor.extract(opening_message, ics)
            extraction_ack = self._apply_extraction(ics, extraction_result, opening_message)

        # Check if all mandatory fields are already satisfied
        if self._all_mandatory_collected(ics):
            return self._transition_to_confirmation(ics, prefix=extraction_ack)

        prompt_response = self.get_next_prompt(ics, ack_prefix=extraction_ack)
        return prompt_response

    # ── Primary message processor ──────────────────────────────────────────────

    def process_message(self, ics_session: InquiryConversationSession,
                        raw_message: str) -> dict:
        """
        Main entry point for every customer message while an ICS is open.

        Processing order:
          1. Refresh session expiry.
          2. Check for expiry.
          3. Log message_received.
          4. Detect cancel intent.
          5. Branch by current state.
        """
        self.refresh_expiry(ics_session)

        if self.check_and_expire(ics_session):
            return _build_engine_response(
                "Your inquiry session has expired due to inactivity. "
                "Type **Start Inquiry** whenever you're ready to begin again.",
                chips=['Start Inquiry', 'Contact Us'],
                metadata={'ics_state': 'expired'},
            )

        _log_event(ics_session, 'message_received', raw_input=raw_message)

        # Cancel detection (any state)
        if self._detect_cancel_intent(raw_message):
            return self.handle_cancel(ics_session, reason='Customer requested cancellation')

        state = ics_session.state

        if state == 'awaiting_conflict_resolution':
            return self._handle_conflict_response(ics_session, raw_message)

        if state == 'awaiting_confirmation':
            return self._handle_confirmation_response(ics_session, raw_message)

        # Default: collecting_information
        return self._process_collection(ics_session, raw_message)

    # ── Collection state ───────────────────────────────────────────────────────

    def _process_collection(self, ics_session: InquiryConversationSession,
                            raw_message: str) -> dict:
        """
        Run the extractor, apply validated fields, handle conflicts,
        then prompt for the next missing mandatory field.
        """
        # Handle optional field skip
        if self._detect_skip_intent(raw_message):
            current_field = ics_session.current_prompt_field
            if current_field:
                field_config = INQUIRY_FIELD_CONFIG.get(current_field, {})
                if not field_config.get('mandatory', True):
                    return self._skip_optional_field(ics_session, current_field)

        # Run the deterministic extractor
        extraction_result = self._extractor.extract(raw_message, ics_session)

        # Check for direct field input (user answering current prompt directly)
        # If the extractor didn't capture the currently prompted field, try direct validation
        current_field = ics_session.current_prompt_field
        if current_field and current_field not in extraction_result.validated:
            direct_result = self._try_direct_field_input(
                ics_session, current_field, raw_message, extraction_result
            )
            if direct_result is not None:
                return direct_result

        # Apply extraction results
        ack = self._apply_extraction(ics_session, extraction_result, raw_message)

        # Handle conflicts before continuing
        if extraction_result.conflicts:
            return self._initiate_conflict_resolution(ics_session, extraction_result.conflicts, ack)

        # Check if all mandatory fields now satisfied
        if self._all_mandatory_collected(ics_session):
            return self._transition_to_confirmation(ics_session, prefix=ack)

        return self.get_next_prompt(ics_session, ack_prefix=ack)

    def _try_direct_field_input(self, ics_session, current_field: str,
                                 raw_message: str, extraction_result) -> dict | None:
        """
        When the user is answering the currently prompted field directly
        (e.g. they just typed their name in response to "What is your name?"),
        attempt to validate the raw message as a direct value for that field.
        """
        field_config = INQUIRY_FIELD_CONFIG.get(current_field)
        if not field_config:
            return None

        context = {'country': ics_session.collected_data.get('country', '')}
        value = raw_message.strip()

        if current_field == 'mobile_number':
            passed, error_msg = self._validator.validate_phone(value, context['country'])
        else:
            method = getattr(self._validator, f'validate_{current_field}',
                             self._validator.validate_free_text)
            passed, error_msg = method(value)

        if passed:
            # Accept the direct input
            existing = ics_session.collected_data.get(current_field)
            if existing and existing.lower() != value.lower():
                # Conflict with already-validated value
                ics_session.conflict_field = current_field
                ics_session.conflict_new_value = value
                ics_session.state = 'awaiting_conflict_resolution'
                ics_session.save()
                _log_event(ics_session, 'conflict_detected', field_name=current_field,
                           raw_input=raw_message, extracted_value=value)
                return _build_engine_response(
                    f"I already have your **{field_config['label']}** as **{existing}**. "
                    f"You've now provided **{value}**. Which one is correct?",
                    chips=[existing, value, 'Keep original'],
                    metadata={'ics_state': 'awaiting_conflict_resolution',
                              'conflict_field': current_field},
                )
            else:
                data = dict(ics_session.collected_data)
                data[current_field] = value
                ics_session.collected_data = data
                ics_session.save()
                _log_event(ics_session, 'validation_passed', field_name=current_field,
                           raw_input=raw_message, extracted_value=value)
                if self._all_mandatory_collected(ics_session):
                    return self._transition_to_confirmation(ics_session)
                return self.get_next_prompt(ics_session)
        elif error_msg:
            # Direct input failed validation — re-prompt with the error
            _log_event(ics_session, 'validation_error', field_name=current_field,
                       raw_input=raw_message, notes=error_msg)
            prompt = INQUIRY_FIELD_CONFIG[current_field]['prompt']
            chips = INQUIRY_FIELD_CONFIG[current_field].get('chips', [])
            return _build_engine_response(
                f"{error_msg}\n\n{prompt}",
                chips=chips,
                metadata={'ics_state': 'collecting_information',
                          'current_field': current_field},
            )
        return None

    # ── Extraction application ─────────────────────────────────────────────────

    def _apply_extraction(self, ics_session: InquiryConversationSession,
                          extraction_result, raw_message: str) -> str:
        """Write validated new fields to the session; log each. Return ack string."""
        if not extraction_result.validated:
            return ''

        data = dict(ics_session.collected_data)
        newly_added = {}

        for field_name, clean_value in extraction_result.validated.items():
            if field_name not in data:
                data[field_name] = clean_value
                newly_added[field_name] = clean_value
                _log_event(ics_session, 'field_extracted',
                           field_name=field_name,
                           raw_input=raw_message,
                           extracted_value=clean_value)
                _log_event(ics_session, 'validation_passed',
                           field_name=field_name,
                           extracted_value=clean_value)

        if newly_added:
            ics_session.collected_data = data
            ics_session.save()

        return _ack_extracted(newly_added)

    # ── Conflict resolution ────────────────────────────────────────────────────

    def _initiate_conflict_resolution(self, ics_session: InquiryConversationSession,
                                      conflicts: dict, ack_prefix: str = '') -> dict:
        """Transition to AWAITING_CONFLICT_RESOLUTION for the first conflict found."""
        field_name, new_value = next(iter(conflicts.items()))
        existing_value = ics_session.collected_data.get(field_name, '')
        field_label = INQUIRY_FIELD_CONFIG.get(field_name, {}).get('label', field_name)

        ics_session.conflict_field = field_name
        ics_session.conflict_new_value = new_value
        ics_session.state = 'awaiting_conflict_resolution'
        ics_session.save()

        _log_event(ics_session, 'conflict_detected', field_name=field_name,
                   extracted_value=new_value,
                   notes=f'existing={existing_value}')

        text = (
            f"{ack_prefix}"
            f"I noticed you mentioned **{new_value}** for **{field_label}**, "
            f"but I already have **{existing_value}** on record. "
            f"Which one should I use?"
        )
        return _build_engine_response(
            text,
            chips=[existing_value, new_value, 'Keep original'],
            metadata={'ics_state': 'awaiting_conflict_resolution',
                      'conflict_field': field_name},
        )

    def _handle_conflict_response(self, ics_session: InquiryConversationSession,
                                   raw_message: str) -> dict:
        """
        Customer is responding to a conflict resolution question.
        Detect whether they want to keep the original or use the new value.
        """
        field_name = ics_session.conflict_field
        new_value = ics_session.conflict_new_value
        existing_value = ics_session.collected_data.get(field_name, '')
        field_label = INQUIRY_FIELD_CONFIG.get(field_name, {}).get('label', field_name)

        msg_lower = raw_message.lower().strip()

        # Check if they typed the new or existing value directly
        chose_new = (
            msg_lower == new_value.lower()
            or 'new' in msg_lower
            or 'use' in msg_lower
            or new_value.lower() in msg_lower
        )
        chose_keep = (
            msg_lower == existing_value.lower()
            or 'keep' in msg_lower
            or 'original' in msg_lower
            or 'first' in msg_lower
            or existing_value.lower() in msg_lower
        )

        if chose_new and not chose_keep:
            # Update to new value
            data = dict(ics_session.collected_data)
            data[field_name] = new_value
            ics_session.collected_data = data
            ics_session.conflict_field = ''
            ics_session.conflict_new_value = ''
            ics_session.state = 'collecting_information'
            ics_session.save()
            _log_event(ics_session, 'conflict_resolved', field_name=field_name,
                       extracted_value=new_value, notes='customer chose new value')
            resolved_msg = f"Updated — using **{new_value}** for **{field_label}**. "
        else:
            # Keep original (default if unclear)
            ics_session.conflict_field = ''
            ics_session.conflict_new_value = ''
            ics_session.state = 'collecting_information'
            ics_session.save()
            _log_event(ics_session, 'conflict_resolved', field_name=field_name,
                       extracted_value=existing_value, notes='customer kept original')
            resolved_msg = f"Understood — keeping **{existing_value}** for **{field_label}**. "

        if self._all_mandatory_collected(ics_session):
            return self._transition_to_confirmation(ics_session, prefix=resolved_msg)

        return self.get_next_prompt(ics_session, ack_prefix=resolved_msg)

    # ── Confirmation ───────────────────────────────────────────────────────────

    def _transition_to_confirmation(self, ics_session: InquiryConversationSession,
                                     prefix: str = '') -> dict:
        """Transition to AWAITING_CONFIRMATION and present summary."""
        ics_session.state = 'awaiting_confirmation'
        ics_session.current_prompt_field = ''
        ics_session.save()

        summary = self.build_confirmation_summary(ics_session)
        _log_event(ics_session, 'confirmation_prompted', notes='All mandatory fields collected')

        text = (
            f"{prefix}"
            f"Here's a summary of your inquiry:\n\n"
            f"{summary}\n\n"
            f"Shall I submit this inquiry to our team? "
            f"Type **Yes** to confirm or **Edit** to make changes."
        )
        return _build_engine_response(
            text,
            chips=['Yes, Submit', 'Edit Details', 'Cancel'],
            metadata={'ics_state': 'awaiting_confirmation'},
        )

    def _handle_confirmation_response(self, ics_session: InquiryConversationSession,
                                       raw_message: str) -> dict:
        """
        Customer is responding to the confirmation summary.
        Detect confirm vs edit vs cancel.
        """
        msg_lower = raw_message.lower().strip()

        if self._detect_confirm_intent(raw_message):
            return self._submit_inquiry(ics_session)

        if 'edit' in msg_lower or 'change' in msg_lower or 'update' in msg_lower or 'wrong' in msg_lower:
            ics_session.state = 'collecting_information'
            ics_session.save()
            return _build_engine_response(
                "No problem! What would you like to change? "
                "You can tell me the updated information directly.",
                chips=['Change Name', 'Change Phone', 'Change Service', 'Cancel'],
                metadata={'ics_state': 'collecting_information'},
            )

        # Ambiguous — re-prompt
        summary = self.build_confirmation_summary(ics_session)
        return _build_engine_response(
            f"I'm sorry, I didn't quite catch that.\n\n{summary}\n\n"
            "Would you like to **submit** this inquiry or make any **edits**?",
            chips=['Yes, Submit', 'Edit Details', 'Cancel'],
            metadata={'ics_state': 'awaiting_confirmation'},
        )

    # ── Submission ─────────────────────────────────────────────────────────────

    def _submit_inquiry(self, ics_session: InquiryConversationSession) -> dict:
        """Delegate to InquirySubmissionAdapter and update session state."""
        from chat.inquiry_submission import InquirySubmissionAdapter
        adapter = InquirySubmissionAdapter()
        result = adapter.submit(ics_session)

        if result['success']:
            ics_session.state = 'submitted'
            ics_session.submitted_inquiry_id = result['inquiry_id']
            ics_session.submitted_at = timezone.now()
            ics_session.save()
            _log_event(ics_session, 'submitted',
                       notes=f"inquiry_id={result['inquiry_id']}")
            _log_event(ics_session, 'confirmed')

            name = ics_session.collected_data.get('customer_name', 'there')
            return _build_engine_response(
                f"Thank you, **{name}**! ✅ Your inquiry has been submitted successfully.\n\n"
                f"Our team will review your requirements and contact you shortly. "
                f"You can also reach us directly at **+91 86670 20798** or "
                f"**info@propertism.in** if you prefer.\n\n"
                f"Is there anything else I can help you with?",
                chips=['Contact Us', 'Our Services', 'New Inquiry'],
                metadata={
                    'ics_state': 'submitted',
                    'inquiry_submitted': True,
                    'inquiry_id': result['inquiry_id'],
                },
            )
        else:
            logger.error(f'[InquiryEngine] Submission failed for {ics_session.ics_id}: {result.get("error")}')
            return _build_engine_response(
                "I'm sorry, something went wrong while submitting your inquiry. "
                "Please try again or contact us directly at **+91 86670 20798**.",
                chips=['Try Again', 'Contact Us'],
                metadata={'ics_state': 'awaiting_confirmation', 'submission_error': True},
            )

    # ── Cancellation ───────────────────────────────────────────────────────────

    def handle_cancel(self, ics_session: InquiryConversationSession,
                      reason: str = '') -> dict:
        """Transition to CANCELLED state. No inquiry is created."""
        ics_session.state = 'cancelled'
        ics_session.cancelled_reason = reason[:200]
        ics_session.save()
        _log_event(ics_session, 'cancelled', notes=reason)

        return _build_engine_response(
            "No problem — I've cancelled your inquiry session. "
            "Feel free to come back whenever you're ready.\n\n"
            "Is there anything else I can assist you with?",
            chips=['Our Services', 'Contact Us', 'Start Inquiry'],
            metadata={'ics_state': 'cancelled'},
        )

    # ── Optional field skip ────────────────────────────────────────────────────

    def _skip_optional_field(self, ics_session: InquiryConversationSession,
                              field_name: str) -> dict:
        """Mark the current optional field as skipped and advance."""
        skipped = list(ics_session.skipped_fields)
        if field_name not in skipped:
            skipped.append(field_name)
        ics_session.skipped_fields = skipped
        ics_session.save()
        _log_event(ics_session, 'field_skipped', field_name=field_name)
        return self.get_next_prompt(ics_session)

    # ── Next prompt resolver ───────────────────────────────────────────────────

    def get_next_prompt(self, ics_session: InquiryConversationSession,
                        ack_prefix: str = '') -> dict:
        """
        Determine the next field to prompt.
        Priority: mandatory fields in order, then optional (if user chose "Add Details").
        Never re-prompts a field already in collected_data or skipped_fields.
        """
        collected = ics_session.collected_data
        skipped = set(ics_session.skipped_fields)

        # Find first missing mandatory field
        for field_name in MANDATORY_FIELDS_ORDER:
            if field_name not in collected:
                return self._prompt_field(ics_session, field_name, ack_prefix)

        # All mandatory collected — should not reach here normally
        return self._transition_to_confirmation(ics_session, prefix=ack_prefix)

    def _prompt_field(self, ics_session: InquiryConversationSession,
                      field_name: str, ack_prefix: str = '') -> dict:
        """Build and return a prompt response for the given field."""
        config = INQUIRY_FIELD_CONFIG[field_name]
        ics_session.current_prompt_field = field_name
        ics_session.save()
        _log_event(ics_session, 'field_prompted', field_name=field_name)

        prompt_text = config['prompt']
        chips = config.get('chips', [])

        return _build_engine_response(
            f"{ack_prefix}{prompt_text}",
            chips=chips,
            metadata={
                'ics_state': 'collecting_information',
                'current_field': field_name,
            },
        )

    # ── Summary builder ────────────────────────────────────────────────────────

    def build_confirmation_summary(self, ics_session: InquiryConversationSession) -> str:
        """Return a formatted markdown summary of all collected fields."""
        data = ics_session.collected_data
        lines = []

        all_fields = MANDATORY_FIELDS_ORDER + OPTIONAL_FIELDS_ORDER
        for field_name in all_fields:
            value = data.get(field_name)
            if value:
                label = INQUIRY_FIELD_CONFIG[field_name]['label']
                lines.append(f"**{label}:** {value}")

        return '\n'.join(lines) if lines else '*(No details collected)*'

    # ── State utilities ────────────────────────────────────────────────────────

    def _all_mandatory_collected(self, ics_session: InquiryConversationSession) -> bool:
        collected = ics_session.collected_data
        return all(f in collected for f in MANDATORY_FIELDS_ORDER)

    def refresh_expiry(self, ics_session: InquiryConversationSession) -> None:
        ics_session.expires_at = timezone.now() + timedelta(minutes=SESSION_EXPIRY_MINUTES)
        ics_session.save(update_fields=['expires_at'])

    def check_and_expire(self, ics_session: InquiryConversationSession) -> bool:
        if ics_session.state in OPEN_STATES and timezone.now() > ics_session.expires_at:
            ics_session.state = 'expired'
            ics_session.save()
            _log_event(ics_session, 'expired')
            return True
        return False

    # ── Intent detection helpers ───────────────────────────────────────────────

    def _detect_cancel_intent(self, message: str) -> bool:
        msg_lower = message.lower().strip()
        return any(kw in msg_lower for kw in CANCEL_KEYWORDS)

    def _detect_confirm_intent(self, message: str) -> bool:
        msg_lower = message.lower().strip()
        return any(kw in msg_lower for kw in CONFIRM_KEYWORDS)

    def _detect_skip_intent(self, message: str) -> bool:
        msg_lower = message.lower().strip()
        return any(kw in msg_lower for kw in SKIP_KEYWORDS)
