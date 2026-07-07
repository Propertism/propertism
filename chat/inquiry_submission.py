"""
chat/inquiry_submission.py — M2.6 Inquiry Submission Adapter

Thin bridge between the realBOT conversation layer and the existing
properties.Inquiry model. This module:
  - Maps InquiryConversationSession.collected_data → PropertyInquiry fields.
  - Calls PropertyInquiry.objects.create() — the single source of truth.
  - Calls send_rfq_notification() — reuses existing notification pipeline.
  - DOES NOT re-implement any validation, spam detection, or notification logic.
  - DOES NOT call LeadValidator — fields are pre-validated by the conversation engine.
"""
import logging

from django.utils import timezone

logger = logging.getLogger(__name__)

# Confidence score for realBOT-submitted inquiries.
# Fields have been validated deterministically — assign Genuine baseline.
REALBOT_CONFIDENCE_SCORE = 80
REALBOT_ASSESSMENT_STATUS = 'Genuine'


class InquirySubmissionAdapter:
    """
    Assembles and creates a PropertyInquiry from a completed
    InquiryConversationSession. Returns a result dict with
    {'success': bool, 'inquiry_id': int|None, 'error': str}.
    """

    def submit(self, ics_session) -> dict:
        """
        Main submission entry point.
        ics_session must be in 'awaiting_confirmation' state with all
        mandatory fields present in collected_data.
        """
        try:
            from properties.models import Inquiry as PropertyInquiry
            from content.views import send_rfq_notification

            data = ics_session.collected_data or {}

            # ── Field mapping ─────────────────────────────────────────────────
            customer_name = data.get('customer_name', '').strip()
            mobile_number = data.get('mobile_number', '').strip()
            email_address = data.get('email_address', '').strip()
            service_required = data.get('service_required', '').strip()
            inquiry_message = data.get('inquiry_message', '').strip()

            # Optional fields
            country = data.get('country', '').strip()
            preferred_location = data.get('preferred_location', '').strip()
            property_type = data.get('property_type', '').strip()
            budget = data.get('budget', '').strip()
            timeline = data.get('timeline', '').strip()
            preferred_contact_time = data.get('preferred_contact_time', '').strip()
            additional_remarks = data.get('additional_remarks', '').strip()

            # ── Build message body ────────────────────────────────────────────
            message_parts = [inquiry_message]

            details = []
            if service_required:
                details.append(f"Service Required: {service_required}")
            if country:
                details.append(f"Country: {country}")
            if preferred_location:
                details.append(f"Preferred Location: {preferred_location}")
            if property_type:
                details.append(f"Property Type: {property_type}")
            if budget:
                details.append(f"Budget: {budget}")
            if timeline:
                details.append(f"Timeline: {timeline}")
            if preferred_contact_time:
                details.append(f"Preferred Contact Time: {preferred_contact_time}")
            if additional_remarks:
                details.append(f"Additional Remarks: {additional_remarks}")

            if details:
                message_parts.append('\n--- Additional Details ---\n' + '\n'.join(details))

            message_parts.append(
                f'\n--- Submitted via realBOT ---\n'
                f'ICS Session: {ics_session.ics_id}\n'
                f'Source: {ics_session.get_source_display()}'
            )

            full_message = '\n'.join(message_parts)

            # ── form_source label (resolved per plan: "realBOT — {service_hint}") ─
            service_hint = ics_session.service_hint or service_required or ''
            if service_hint:
                sh_lower = service_hint.strip().lower()
                if sh_lower in ('inquiry_creation', 'inquiry-creation'):
                    friendly_hint = 'General Inquiry'
                else:
                    friendly_hint = service_hint.replace('_', ' ').replace('-', ' ').strip().title()
                form_source = f'realBOT — {friendly_hint}'
            else:
                form_source = 'realBOT Chat'

            # ── Create PropertyInquiry ─────────────────────────────────────────
            inquiry = PropertyInquiry.objects.create(
                name=customer_name,
                phone=mobile_number,
                email=email_address,          # may be empty string for optional
                message=full_message,
                property=None,                # chat inquiries are not property-specific
                status='pending',
                form_source=form_source,
                confidence_score=REALBOT_CONFIDENCE_SCORE,
                assessment_status=REALBOT_ASSESSMENT_STATUS,
                validation_summary=[],        # pre-validated by engine
            )

            logger.info(
                f'[InquirySubmissionAdapter] Created PropertyInquiry #{inquiry.pk} '
                f'from ICS session {ics_session.ics_id}'
            )

            # ── Trigger existing notification pipeline ────────────────────────
            try:
                send_rfq_notification(inquiry, form_source=form_source)
            except Exception as notif_exc:
                # Notification failure must never block submission success
                logger.exception(
                    f'[InquirySubmissionAdapter] Notification failed for inquiry '
                    f'#{inquiry.pk}: {notif_exc}'
                )

            return {
                'success': True,
                'inquiry_id': inquiry.pk,
                'error': '',
            }

        except Exception as exc:
            logger.exception(
                f'[InquirySubmissionAdapter] Submission failed for ICS '
                f'{getattr(ics_session, "ics_id", "?")}: {exc}'
            )
            return {
                'success': False,
                'inquiry_id': None,
                'error': str(exc),
            }
