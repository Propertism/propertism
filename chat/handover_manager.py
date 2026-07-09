"""
chat/handover_manager.py — M2.17 Human Handover & Conversation Closure Framework.

Provides the core business logic for:
  - Human handover request lifecycle management
  - Advisor queue management and assignment
  - Advisor conversation participation
  - Conversation closure flow
  - Transcript generation (HTML format)
  - Transcript email dispatch
  - Conversation archival
  - Full lifecycle orchestration
  - Handover analytics aggregation
  - Handover audit logging

Zero runtime AI dependency — all logic is deterministic and configuration-driven.
"""

import json
import logging
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db import transaction

from chat.constants import (
    STATE_BOT_ACTIVE, STATE_HANDOVER_REQUESTED, STATE_WAITING_FOR_AGENT,
    STATE_AGENT_CONNECTED, STATE_HUMAN_CONVERSATION, STATE_CHAT_END_REQUESTED,
    STATE_CHAT_CLOSED, STATE_ARCHIVED, MANDATORY_TRANSITIONS,
    ADVISOR_AVAILABLE, ADVISOR_BUSY, ADVISOR_OFFLINE,
    CLOSURE_CUSTOMER_INITIATED, CLOSURE_ADVISOR_INITIATED,
    CLOSURE_TIMEOUT, CLOSURE_SYSTEM,
    DEFAULT_TRANSCRIPT_EMAIL_RECIPIENTS, DEFAULT_EMAIL_ENABLED,
    DEFAULT_AGENT_HANDOVER_ENABLED, DEFAULT_TRANSCRIPT_SUBJECT_PREFIX,
    DEFAULT_EMAIL_RETRY_COUNT, DEFAULT_EMAIL_TIMEOUT,
    ERR_HANDOVER_FAILED, ERR_ADVISOR_UNAVAILABLE, ERR_HANDOVER_NOT_FOUND,
    ERR_HANDOVER_INVALID_STATE, ERR_ADVISOR_NOT_FOUND,
    ERR_ADVISOR_NOT_AUTHORIZED, ERR_CONVERSATION_CLOSED,
    ERR_TRANSCRIPT_FAILED, ERR_EMAIL_DISPATCH_FAILED, ERR_ARCHIVE_FAILED,
    ERR_HANDOVER_ALREADY_EXISTS,
)
from chat.models import (
    RealBotSession, RealBotMessage, AdvisorProfile, HandoverRequest,
    AdvisorMessage, ConversationArchive, TranscriptRecord, HandoverAnalytics,
    HandoverAuditLog,
)

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Human Handover Manager
# ══════════════════════════════════════════════════════════════════════════════

class HumanHandoverManager:
    """
    Manages the lifecycle of a handover request from a customer.
    Handles creation, acceptance, rejection, and cancellation of handover requests.
    """

    @staticmethod
    def create_handover(session, customer_name='', customer_email='',
                        customer_phone='', reason=''):
        """
        Create a new handover request for a given session.
        Validates that no active handover already exists for the session.
        """
        # Check for existing active handover
        active_statuses = ['requested', 'accepted']
        existing = HandoverRequest.objects.filter(
            session=session, status__in=active_statuses
        ).first()
        if existing:
            return {
                'success': False,
                'error_code': ERR_HANDOVER_ALREADY_EXISTS,
                'error_message': 'An active handover request already exists for this session.',
                'handover_id': existing.handover_id,
            }

        handover = HandoverRequest.objects.create(
            session=session,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            reason=reason,
            status='requested',
        )

        # Audit log
        HandoverAuditLog.objects.create(
            session=session,
            handover=handover,
            action='handover_requested',
            performed_by=customer_name or 'customer',
            details={
                'handover_id': handover.handover_id,
                'reason': reason,
                'customer_email': customer_email,
            }
        )

        logger.info(
            'Handover created: %s for session %s',
            handover.handover_id, session.session_id
        )

        return {
            'success': True,
            'handover_id': handover.handover_id,
            'status': handover.status,
            'created_at': handover.created_at.isoformat(),
        }

    @staticmethod
    def get_handover_status(handover_id):
        """Get the current status of a handover request."""
        try:
            handover = HandoverRequest.objects.get(handover_id=handover_id)
        except HandoverRequest.DoesNotExist:
            return {
                'success': False,
                'error_code': ERR_HANDOVER_NOT_FOUND,
                'error_message': f'Handover request {handover_id} not found.',
            }

        data = {
            'handover_id': handover.handover_id,
            'status': handover.status,
            'customer_name': handover.customer_name,
            'reason': handover.reason,
            'created_at': handover.created_at.isoformat(),
            'updated_at': handover.updated_at.isoformat(),
        }
        if handover.assigned_advisor:
            data['assigned_advisor'] = handover.assigned_advisor.display_name
            data['assigned_at'] = handover.assigned_at.isoformat() if handover.assigned_at else None
        if handover.completed_at:
            data['completed_at'] = handover.completed_at.isoformat()

        return {'success': True, 'data': data}

    @staticmethod
    def cancel_handover(handover_id, performed_by='customer'):
        """Cancel a handover request."""
        try:
            handover = HandoverRequest.objects.get(handover_id=handover_id)
        except HandoverRequest.DoesNotExist:
            return {
                'success': False,
                'error_code': ERR_HANDOVER_NOT_FOUND,
                'error_message': f'Handover request {handover_id} not found.',
            }

        if handover.status not in ['requested', 'accepted']:
            return {
                'success': False,
                'error_code': ERR_HANDOVER_INVALID_STATE,
                'error_message': f'Cannot cancel handover in status: {handover.status}.',
            }

        handover.status = 'cancelled'
        handover.save()

        HandoverAuditLog.objects.create(
            session=handover.session,
            handover=handover,
            action='handover_cancelled',
            performed_by=performed_by,
            details={'previous_status': handover.status},
        )

        return {'success': True, 'handover_id': handover.handover_id, 'status': 'cancelled'}


# ══════════════════════════════════════════════════════════════════════════════
# 2. Advisor Queue Manager
# ══════════════════════════════════════════════════════════════════════════════

class AdvisorQueueManager:
    """
    Manages the advisor queue and assignment logic.
    Handles finding available advisors and assigning them to handover requests.
    """

    @staticmethod
    def get_available_advisors():
        """Return list of advisors currently available for assignment."""
        return AdvisorProfile.objects.filter(
            status=ADVISOR_AVAILABLE,
            is_active=True,
            active_chat_count__lt=models.F('max_concurrent_chats')
        ).order_by('active_chat_count', 'display_name')

    @staticmethod
    def assign_advisor(handover):
        """
        Assign the best available advisor to a handover request.
        Uses round-robin style: picks advisor with fewest active chats.
        """
        available = AdvisorQueueManager.get_available_advisors()
        if not available.exists():
            return {
                'success': False,
                'error_code': ERR_ADVISOR_UNAVAILABLE,
                'error_message': 'No advisors are currently available.',
            }

        advisor = available.first()
        handover.assigned_advisor = advisor
        handover.assigned_at = timezone.now()
        handover.status = 'accepted'
        handover.save()

        advisor.active_chat_count = models.F('active_chat_count') + 1
        if advisor.active_chat_count >= advisor.max_concurrent_chats:
            advisor.status = ADVISOR_BUSY
        advisor.save()

        HandoverAuditLog.objects.create(
            session=handover.session,
            handover=handover,
            action='advisor_assigned',
            performed_by='system',
            details={
                'advisor_id': advisor.advisor_id,
                'advisor_name': advisor.display_name,
            }
        )

        return {
            'success': True,
            'advisor_id': advisor.advisor_id,
            'advisor_name': advisor.display_name,
        }

    @staticmethod
    def get_waiting_handovers():
        """Get all handover requests waiting for advisor assignment."""
        return HandoverRequest.objects.filter(
            status='requested'
        ).select_related('session').order_by('created_at')

    @staticmethod
    def release_advisor(advisor):
        """Decrement active chat count and update status."""
        advisor.active_chat_count = models.F('active_chat_count') - 1
        if advisor.active_chat_count < 0:
            advisor.active_chat_count = 0
        if advisor.status == ADVISOR_BUSY and advisor.active_chat_count < advisor.max_concurrent_chats:
            advisor.status = ADVISOR_AVAILABLE
        advisor.save()


# ══════════════════════════════════════════════════════════════════════════════
# 3. Advisor Conversation Manager
# ══════════════════════════════════════════════════════════════════════════════

class AdvisorConversationManager:
    """
    Manages advisor participation in conversations.
    Handles sending messages as an advisor and retrieving conversation history.
    """

    @staticmethod
    def send_message(handover, advisor, message_text):
        """
        Send a message from an advisor in a handover conversation.
        Validates that the advisor is assigned to this handover.
        """
        if handover.assigned_advisor_id != advisor.pk:
            return {
                'success': False,
                'error_code': ERR_ADVISOR_NOT_AUTHORIZED,
                'error_message': 'This advisor is not assigned to this handover.',
            }

        if handover.status not in ['accepted']:
            return {
                'success': False,
                'error_code': ERR_HANDOVER_INVALID_STATE,
                'error_message': f'Cannot send message in handover status: {handover.status}.',
            }

        advisor_msg = AdvisorMessage.objects.create(
            session=handover.session,
            advisor=advisor,
            handover=handover,
            message_text=message_text,
        )

        HandoverAuditLog.objects.create(
            session=handover.session,
            handover=handover,
            action='advisor_message_sent',
            performed_by=advisor.display_name,
            details={
                'message_id': advisor_msg.message_id,
                'message_preview': message_text[:100],
            }
        )

        return {
            'success': True,
            'message_id': advisor_msg.message_id,
            'created_at': advisor_msg.created_at.isoformat(),
        }

    @staticmethod
    def get_conversation_history(session):
        """Get combined bot and advisor message history for a session."""
        bot_messages = RealBotMessage.objects.filter(session=session).order_by('created_at')
        advisor_messages = AdvisorMessage.objects.filter(session=session).order_by('created_at')

        history = []
        for msg in bot_messages:
            history.append({
                'type': 'bot' if msg.sender == 'assistant' else 'user',
                'sender': msg.sender,
                'text': msg.text,
                'metadata': msg.metadata,
                'created_at': msg.created_at.isoformat(),
            })
        for msg in advisor_messages:
            advisor_name = msg.advisor.display_name if msg.advisor else 'Advisor'
            history.append({
                'type': 'advisor',
                'sender': advisor_name,
                'text': msg.message_text,
                'created_at': msg.created_at.isoformat(),
            })

        history.sort(key=lambda x: x['created_at'])
        return history


# ══════════════════════════════════════════════════════════════════════════════
# 4. Conversation Closure Manager
# ══════════════════════════════════════════════════════════════════════════════

class ConversationClosureManager:
    """
    Handles the conversation closure flow.
    Manages end-request, closure, and cleanup of conversation state.
    """

    @staticmethod
    def request_closure(handover, requested_by='customer'):
        """Request closure of a handover conversation."""
        if handover.status not in ['accepted']:
            return {
                'success': False,
                'error_code': ERR_HANDOVER_INVALID_STATE,
                'error_message': f'Cannot close handover in status: {handover.status}.',
            }

        handover.status = 'completed'
        handover.completed_at = timezone.now()
        handover.save()

        # Release advisor
        if handover.assigned_advisor:
            AdvisorQueueManager.release_advisor(handover.assigned_advisor)

        HandoverAuditLog.objects.create(
            session=handover.session,
            handover=handover,
            action='conversation_closed',
            performed_by=requested_by,
            details={'closure_reason': CLOSURE_CUSTOMER_INITIATED},
        )

        return {
            'success': True,
            'handover_id': handover.handover_id,
            'completed_at': handover.completed_at.isoformat(),
        }

    @staticmethod
    def close_conversation(session, closure_reason=CLOSURE_SYSTEM, closed_by='system'):
        """
        Close a conversation session entirely.
        This is the final step before archival.
        """
        # Mark any active handovers as completed
        active_handovers = HandoverRequest.objects.filter(
            session=session, status__in=['requested', 'accepted']
        )
        for handover in active_handovers:
            handover.status = 'completed'
            handover.completed_at = timezone.now()
            handover.save()
            if handover.assigned_advisor:
                AdvisorQueueManager.release_advisor(handover.assigned_advisor)

        return {
            'success': True,
            'session_id': str(session.session_id),
            'closure_reason': closure_reason,
        }


# ══════════════════════════════════════════════════════════════════════════════
# 5. Transcript Generator
# ══════════════════════════════════════════════════════════════════════════════

class TranscriptGenerator:
    """
    Generates HTML transcripts of conversations.
    Produces a formatted HTML document suitable for email or download.
    """

    @staticmethod
    def generate_html_transcript(session, handover=None):
        """
        Generate an HTML transcript of the full conversation.
        Includes bot messages, user messages, and advisor messages.
        """
        history = AdvisorConversationManager.get_conversation_history(session)

        # Build transcript content
        transcript_lines = []
        transcript_lines.append(f'<h1>realBOT Conversation Transcript</h1>')
        transcript_lines.append(f'<p>Session ID: {session.session_id}</p>')
        transcript_lines.append(f'<p>Date: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}</p>')
        if handover:
            transcript_lines.append(f'<p>Handover ID: {handover.handover_id}</p>')
        transcript_lines.append('<hr>')

        for entry in history:
            msg_type = entry['type']
            sender = entry['sender']
            text = entry['text']
            timestamp = entry.get('created_at', '')

            css_class = 'bot-message' if msg_type == 'bot' else (
                'user-message' if msg_type == 'user' else 'advisor-message'
            )
            label = 'realBOT' if msg_type == 'bot' else (
                'Customer' if msg_type == 'user' else f'Advisor ({sender})'
            )

            transcript_lines.append(
                f'<div class="{css_class}">'
                f'<strong>{label}</strong> '
                f'<span class="timestamp">({timestamp})</span><br>'
                f'{text}'
                f'</div>'
            )

        html_content = '\n'.join(transcript_lines)
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>realBOT Conversation Transcript</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; padding: 20px; }}
        h1 {{ color: #1a56db; }}
        .bot-message {{ background: #f0f7ff; padding: 10px; margin: 8px 0; border-radius: 8px; }}
        .user-message {{ background: #f3f4f6; padding: 10px; margin: 8px 0; border-radius: 8px; }}
        .advisor-message {{ background: #ecfdf5; padding: 10px; margin: 8px 0; border-radius: 8px; }}
        .timestamp {{ color: #6b7280; font-size: 0.85em; }}
        hr {{ border: 1px solid #e5e7eb; margin: 20px 0; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""

        return full_html

    @staticmethod
    def generate_and_store(session, handover=None):
        """
        Generate transcript and store it as a TranscriptRecord.
        Returns the transcript record.
        """
        html_content = TranscriptGenerator.generate_html_transcript(session, handover)

        # Retrieve existing archive or create one using the manager to populate all details
        archive = ConversationArchive.objects.filter(session=session).first()
        if not archive:
            archive_result = ConversationArchiveManager.archive_conversation(
                session, closure_reason=CLOSURE_SYSTEM, closed_by='system'
            )
            archive = ConversationArchive.objects.get(archive_id=archive_result['archive_id'])

        transcript = TranscriptRecord.objects.create(
            archive=archive,
            format='html',
            content=html_content,
        )

        HandoverAuditLog.objects.create(
            session=session,
            handover=handover,
            action='transcript_generated',
            performed_by='system',
            details={
                'transcript_id': transcript.transcript_id,
                'archive_id': archive.archive_id,
            }
        )

        return transcript


# ══════════════════════════════════════════════════════════════════════════════
# 6. Transcript Email Dispatcher
# ══════════════════════════════════════════════════════════════════════════════

class TranscriptEmailDispatcher:
    """
    Dispatches conversation transcripts via email.
    Handles sending, retry logic, and delivery status tracking.
    """

    @staticmethod
    def send_transcript_email(transcript, recipients=None):
        """
        Send a transcript via email.
        Uses configured email backend (SMTP in production, console in development).
        """
        if not DEFAULT_EMAIL_ENABLED:
            return {
                'success': False,
                'error_message': 'Email dispatch is disabled.',
            }

        if not recipients:
            if hasattr(settings, 'ADMIN_EMAILS') and settings.ADMIN_EMAILS:
                recipient_list = settings.ADMIN_EMAILS
            else:
                recipient_list = [r.strip() for r in DEFAULT_TRANSCRIPT_EMAIL_RECIPIENTS.split(',') if r.strip()]
        else:
            recipient_list = [r.strip() for r in recipients.split(',') if r.strip()]
        if not recipient_list:
            return {
                'success': False,
                'error_code': ERR_EMAIL_DISPATCH_FAILED,
                'error_message': 'No email recipients specified.',
            }

        subject = f'{DEFAULT_TRANSCRIPT_SUBJECT_PREFIX} - {transcript.archive.session.session_id}'

        try:
            email = EmailMessage(
                subject=subject,
                body=transcript.content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipient_list,
            )
            email.content_subtype = 'html'
            email.send(fail_silently=False)

            transcript.email_sent = True
            transcript.email_sent_at = timezone.now()
            transcript.email_recipients = recipients
            transcript.email_status = 'sent'
            transcript.save()

            HandoverAuditLog.objects.create(
                session=transcript.archive.session,
                handover=transcript.archive.handover,
                action='email_dispatched',
                performed_by='system',
                details={
                    'transcript_id': transcript.transcript_id,
                    'recipients': recipients,
                }
            )

            return {
                'success': True,
                'transcript_id': transcript.transcript_id,
                'recipients': recipient_list,
            }

        except Exception as e:
            transcript.email_retry_count = models.F('email_retry_count') + 1
            transcript.email_status = f'failed: {str(e)}'
            transcript.save()

            logger.error('Email dispatch failed for transcript %s: %s',
                         transcript.transcript_id, str(e))

            return {
                'success': False,
                'error_code': ERR_EMAIL_DISPATCH_FAILED,
                'error_message': f'Email dispatch failed: {str(e)}',
            }

    @staticmethod
    def retry_failed_emails():
        """Retry sending emails for transcripts that failed."""
        failed = TranscriptRecord.objects.filter(
            email_sent=False,
            email_retry_count__lt=DEFAULT_EMAIL_RETRY_COUNT,
        )
        results = []
        for transcript in failed:
            result = TranscriptEmailDispatcher.send_transcript_email(transcript)
            results.append(result)
        return results


# ══════════════════════════════════════════════════════════════════════════════
# 7. Conversation Archive Manager
# ══════════════════════════════════════════════════════════════════════════════

class ConversationArchiveManager:
    """
    Manages the archival of completed conversations.
    Creates immutable archives with full conversation data.
    """

    @staticmethod
    def archive_conversation(session, closure_reason=CLOSURE_SYSTEM, closed_by='system'):
        """
        Archive a completed conversation.
        Gathers all messages and creates or updates the archive record.
        """
        # Gather conversation data
        history = AdvisorConversationManager.get_conversation_history(session)
        handover = HandoverRequest.objects.filter(session=session).first()

        bot_messages = RealBotMessage.objects.filter(session=session).order_by('created_at')
        advisor_messages = AdvisorMessage.objects.filter(session=session).order_by('created_at')

        bot_transcript = []
        for msg in bot_messages:
            bot_transcript.append({
                'sender': msg.sender,
                'text': msg.text,
                'metadata': msg.metadata,
                'created_at': msg.created_at.isoformat(),
            })

        advisor_transcript = []
        for msg in advisor_messages:
            advisor_name = msg.advisor.display_name if msg.advisor else 'Advisor'
            advisor_transcript.append({
                'sender': advisor_name,
                'text': msg.message_text,
                'created_at': msg.created_at.isoformat(),
            })

        start_time = session.created_at
        end_time = timezone.now()
        duration_seconds = int((end_time - start_time).total_seconds())

        conversation_data = {
            'session_id': str(session.session_id),
            'conversation_id': str(session.conversation_id),
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat() if session.updated_at else None,
            'message_count': len(history),
            'messages': history,
            'handover_id': handover.handover_id if handover else None,
            'archived_at': end_time.isoformat(),
        }

        # Check if already exists
        archive = ConversationArchive.objects.filter(session=session).first()
        if archive:
            archive.handover = handover
            archive.bot_transcript = bot_transcript
            archive.advisor_transcript = advisor_transcript
            archive.full_transcript = history
            archive.conversation_data = conversation_data
            archive.start_time = start_time
            archive.end_time = end_time
            archive.duration_seconds = duration_seconds
            archive.closure_reason = closure_reason
            archive.closed_by = closed_by
            archive.save()
        else:
            archive = ConversationArchive.objects.create(
                session=session,
                handover=handover,
                bot_transcript=bot_transcript,
                advisor_transcript=advisor_transcript,
                full_transcript=history,
                conversation_data=conversation_data,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration_seconds,
                closure_reason=closure_reason,
                closed_by=closed_by,
            )

        HandoverAuditLog.objects.create(
            session=session,
            handover=handover,
            action='conversation_archived',
            performed_by=closed_by,
            details={
                'archive_id': archive.archive_id,
                'message_count': len(history),
            }
        )

        return {
            'success': True,
            'archive_id': archive.archive_id,
            'message_count': len(history),
        }

    @staticmethod
    def get_archive(archive_id):
        """Retrieve a conversation archive by ID."""
        try:
            archive = ConversationArchive.objects.get(archive_id=archive_id)
        except ConversationArchive.DoesNotExist:
            return {
                'success': False,
                'error_code': ERR_ARCHIVE_FAILED,
                'error_message': f'Archive {archive_id} not found.',
            }

        return {
            'success': True,
            'data': {
                'archive_id': archive.archive_id,
                'session_id': str(archive.session.session_id) if archive.session else None,
                'closure_reason': archive.closure_reason,
                'closed_by': archive.closed_by,
                'message_count': len(archive.conversation_data.get('messages', [])),
                'archived_at': archive.created_at.isoformat(),
                'start_time': archive.start_time.isoformat() if archive.start_time else None,
                'end_time': archive.end_time.isoformat() if archive.end_time else None,
                'duration_seconds': archive.duration_seconds,
            }
        }

    @staticmethod
    def list_archives(limit=50):
        """List recent conversation archives."""
        archives = ConversationArchive.objects.all()[:limit]
        results = []
        for archive in archives:
            results.append({
                'archive_id': archive.archive_id,
                'session_id': str(archive.session.session_id) if archive.session else None,
                'closure_reason': archive.closure_reason,
                'message_count': len(archive.conversation_data.get('messages', [])),
                'archived_at': archive.archived_at.isoformat(),
            })
        return results


# ══════════════════════════════════════════════════════════════════════════════
# 8. Conversation Lifecycle Manager (Orchestrator)
# ══════════════════════════════════════════════════════════════════════════════

class ConversationLifecycleManager:
    """
    Orchestrates the full conversation lifecycle from bot active through
    handover, human conversation, closure, transcript generation,
    email dispatch, and archival.
    """

    def __init__(self):
        self.handover_mgr = HumanHandoverManager()
        self.advisor_queue = AdvisorQueueManager()
        self.conversation_mgr = AdvisorConversationManager()
        self.closure_mgr = ConversationClosureManager()
        self.transcript_gen = TranscriptGenerator()
        self.email_dispatcher = TranscriptEmailDispatcher()
        self.archive_mgr = ConversationArchiveManager()

    def request_handover(self, session, customer_name='', customer_email='',
                         customer_phone='', reason=''):
        """
        Full handover flow: create request, assign advisor.
        """
        # Step 1: Create handover request
        result = self.handover_mgr.create_handover(
            session, customer_name, customer_email, customer_phone, reason
        )
        if not result['success']:
            return result

        # Step 2: Get the handover
        handover = HandoverRequest.objects.get(handover_id=result['handover_id'])

        # Step 3: Send Admin notifications (routed via AcknowledgementService)
        from django.conf import settings
        from communications.services import AcknowledgementService
        
        domain = getattr(settings, 'SITE_URL', 'https://propertism.in').rstrip('/')
        chat_link = f"{domain}/realbot/?session_id={session.session_id}"
        
        subject = f"⚠️ Human Advisor Request from {customer_name or 'Customer'}"
        whatsapp_text = (
            f"⚠️ *Human Advisor Request*\n"
            f"Customer: {customer_name or 'Anonymous'}\n"
            f"Phone: {customer_phone or 'Not provided'}\n"
            f"Email: {customer_email or 'Not provided'}\n"
            f"Reason: {reason or 'Not provided'}\n\n"
            f"Link to continue: {chat_link}"
        )
        
        # Email to admin
        admin_emails = getattr(settings, 'ADMIN_EMAILS', [settings.ADMIN_EMAIL])
        for admin_email in admin_emails:
            try:
                AcknowledgementService.send(
                    communication_type_key='admin_lead_alert',
                    recipient=admin_email,
                    context={
                        'subject': subject,
                        'body': whatsapp_text,
                    },
                    channels=['email'],
                    module='realbot_handover'
                )
            except Exception as exc:
                logger.exception("Failed to send admin handover email to %s", admin_email)
                
        # WhatsApp to admin
        try:
            admin_phone = getattr(settings, 'WHATSAPP_ADMIN_PHONE', '918667020798')
            AcknowledgementService.send(
                communication_type_key='admin_lead_alert',
                recipient=admin_phone,
                context={
                    'subject': 'Admin Handover WhatsApp Alert',
                    'body': whatsapp_text
                },
                channels=['whatsapp'],
                module='realbot_handover'
            )
        except Exception as exc:
            logger.exception("Failed to send admin handover WhatsApp alert")

        # Step 4: Assign advisor
        assign_result = self.advisor_queue.assign_advisor(handover)
        if not assign_result['success']:
            # Handover is created but no advisor available — stays in 'requested' state
            return {
                'success': True,
                'handover_id': handover.handover_id,
                'status': 'requested',
                'advisor_assigned': False,
                'message': 'Handover requested. No advisor currently available.',
            }

        return {
            'success': True,
            'handover_id': handover.handover_id,
            'status': 'accepted',
            'advisor_assigned': True,
            'advisor_name': assign_result['advisor_name'],
        }

    def complete_lifecycle(self, session, closure_reason=CLOSURE_CUSTOMER_INITIATED,
                          closed_by='customer', send_email=True, email_recipients=None):
        """
        Complete the full conversation lifecycle:
        1. Close conversation
        2. Generate transcript
        3. Send email (optional)
        4. Archive conversation
        """
        results = {}

        # Step 1: Close conversation
        close_result = self.closure_mgr.close_conversation(session, closure_reason, closed_by)
        results['closure'] = close_result
        if not close_result['success']:
            return results

        # Step 2: Generate transcript
        handover = HandoverRequest.objects.filter(session=session).first()
        transcript = self.transcript_gen.generate_and_store(session, handover)
        results['transcript'] = {
            'success': True,
            'transcript_id': transcript.transcript_id,
        }

        # Step 3: Send email (if enabled)
        if send_email:
            email_result = self.email_dispatcher.send_transcript_email(
                transcript, recipients=email_recipients
            )
            results['email'] = email_result

        # Step 4: Archive conversation
        archive_result = self.archive_mgr.archive_conversation(
            session, closure_reason, closed_by
        )
        results['archive'] = archive_result

        return results


# ══════════════════════════════════════════════════════════════════════════════
# 9. Handover Analytics Aggregator
# ══════════════════════════════════════════════════════════════════════════════

class HandoverAnalyticsAggregator:
    """
    Aggregates handover analytics data for reporting.
    Computes metrics from handover records and stores snapshots.
    """

    @staticmethod
    def compute_period_analytics(start_date, end_date):
        """
        Compute handover analytics for a given date range.
        """
        handovers = HandoverRequest.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
        )

        total = handovers.count()
        completed = handovers.filter(status='completed').count()
        rejected = handovers.filter(status='rejected').count()
        cancelled = handovers.filter(status='cancelled').count()

        # Compute average wait time
        completed_handovers = handovers.filter(
            status='completed', assigned_at__isnull=False, completed_at__isnull=False
        )
        total_wait = 0
        wait_count = 0
        total_duration = 0
        duration_count = 0
        for h in completed_handovers:
            if h.assigned_at and h.created_at:
                wait_seconds = (h.assigned_at - h.created_at).total_seconds()
                total_wait += wait_seconds
                wait_count += 1
            if h.completed_at and h.assigned_at:
                duration_seconds = (h.completed_at - h.assigned_at).total_seconds()
                total_duration += duration_seconds
                duration_count += 1

        avg_wait = total_wait / wait_count if wait_count > 0 else 0.0
        avg_duration = total_duration / duration_count if duration_count > 0 else 0.0

        # Advisor messages count
        sessions = RealBotSession.objects.filter(handover_requests__in=handovers)
        total_advisor_msgs = AdvisorMessage.objects.filter(
            session__in=sessions
        ).count()

        # Transcripts and emails
        archives = ConversationArchive.objects.filter(
            session__in=sessions
        )
        transcripts = TranscriptRecord.objects.filter(archive__in=archives)
        total_transcripts = transcripts.count()
        total_emails = transcripts.filter(email_sent=True).count()

        # Store analytics record
        analytics, created = HandoverAnalytics.objects.update_or_create(
            period_start=start_date,
            period_end=end_date,
            defaults={
                'total_handovers': total,
                'completed_handovers': completed,
                'rejected_handovers': rejected,
                'cancelled_handovers': cancelled,
                'avg_wait_time_seconds': avg_wait,
                'avg_conversation_duration_seconds': avg_duration,
                'total_advisor_messages': total_advisor_msgs,
                'transcripts_generated': total_transcripts,
                'emails_sent': total_emails,
            }
        )

        return {
            'success': True,
            'analytics_id': analytics.analytics_id,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
            },
            'metrics': {
                'total_handovers': total,
                'completed_handovers': completed,
                'rejected_handovers': rejected,
                'cancelled_handovers': cancelled,
                'avg_wait_time_seconds': round(avg_wait, 2),
                'avg_conversation_duration_seconds': round(avg_duration, 2),
                'total_advisor_messages': total_advisor_msgs,
                'transcripts_generated': total_transcripts,
                'emails_sent': total_emails,
            }
        }


# Import models for type hints in querysets
from django.db import models as django_models
import django.db.models
