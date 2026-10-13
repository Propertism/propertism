"""
chat/inquiry_submission.py — M2.6 Inquiry Submission Adapter

Thin bridge between the realBOT conversation layer and the existing
properties.Inquiry model. This module:
  - Maps InquiryConversationSession.collected_data → PropertyInquiry fields.
  - Calls PropertyInquiry.objects.create() — the single source of truth.
  - Calls send_rfq_notification() — reuses existing notification pipeline.
  - Maps fields, then assesses via LeadValidator when available.
  - Never hardcodes assessment_status='Genuine' or confidence_score=80.
  - Does not call SpamProtectionService (HTML-form CAPTCHA/honeypot/timing).
"""
import logging

from django.utils import timezone

logger = logging.getLogger(__name__)

# Assessment is produced by LeadValidator. Never hardcode Genuine/80.


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
            from properties.country_utils import resolve_country_from_intake
            c_code, c_name = resolve_country_from_intake(
                message=full_message,
                phone=mobile_number
            )

            confidence_score = None
            assessment_status = 'Pending Validation'
            validation_summary = []
            try:
                from properties.utils.lead_validation import LeadValidator

                class _AdapterRequest:
                    META = {}
                    session = type("S", (), {"session_key": "realbot"})()

                assessment = LeadValidator(
                    request=_AdapterRequest(),
                    data={
                        'name': customer_name,
                        'phone': mobile_number,
                        'email': email_address,
                        'message': full_message,
                        'country_code': c_code,
                    },
                ).validate()
                confidence_score = assessment.get('confidence_score')
                assessment_status = assessment.get('assessment_status') or 'Pending Validation'
                validation_summary = assessment.get('validation_summary') or []
            except Exception as assess_exc:
                logger.info(
                    '[InquirySubmissionAdapter] LeadValidator unavailable; pending validation. %s',
                    assess_exc,
                )

            inquiry = PropertyInquiry.objects.create(
                name=customer_name,
                phone=mobile_number,
                email=email_address,          # may be empty string for optional
                message=full_message,
                property=None,                # chat inquiries are not property-specific
                status='pending',
                form_source=form_source,
                country_code=c_code,
                country_name=c_name,
                confidence_score=confidence_score,
                assessment_status=assessment_status,
                validation_summary=validation_summary,
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
