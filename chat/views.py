import logging
import json
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from properties.models import ContactMessage
from .models import RealBotSession, RealBotMessage, KnowledgeArticle
from .ai_service import AIService
from realtor_project.features import is_feature_enabled
from chat.responses import standard_response
from chat.metrics import InfrastructureMetrics
from chat.validators import validate_realbot_configuration
from chat.constants import *

logger = logging.getLogger(__name__)

def is_realbot_enabled():
    """Helper to check settings and feature flags for integration status."""
    return getattr(settings, 'REALBOT_INTEGRATION_ENABLED', False) and is_feature_enabled('REALBOT_INTEGRATION_ENABLED', default=True)

def is_ai_enabled():
    """Helper to check settings and feature flags for AI status."""
    return getattr(settings, 'REALBOT_AI_ENABLED', False) or is_feature_enabled('REALBOT_AI_ENABLED', default=False)



# Legacy Lead Form Submission
@require_POST
@csrf_exempt
def submit_chat_message(request):
    """Handle chat message submission"""
    try:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        
        if not name or not email or not message:
            return JsonResponse({
                'success': False,
                'error': 'Please fill in all required fields'
            }, status=400)
        
        contact_msg = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject='',
            message=message,
            status='pending'
        )
        
        logger.info(f"Chat message received from {email}")
        
        try:
            send_chat_notification(contact_msg)
        except Exception as email_exc:
            logger.error(f"Failed to send chat notification: {email_exc}")
        
        return JsonResponse({
            'success': True,
            'message': 'Thanks! We\'ll get back to you soon.'
        })
        
    except Exception as exc:
        logger.exception(f"Error processing chat message: {exc}")
        return JsonResponse({
            'success': False,
            'error': 'Something went wrong. Please try again.'
        }, status=500)


def send_chat_notification(contact_msg):
    """Send email notification when chat message is received"""
    subject = f"New Chat Message from {contact_msg.name}"
    message_lines = [
        f"New chat message received:",
        f"",
        f"Name: {contact_msg.name}",
        f"Email: {contact_msg.email}",
        f"Phone: {contact_msg.phone or 'Not provided'}",
        f"",
        f"Message:",
        f"{contact_msg.message}",
        f"",
        f"Received: {contact_msg.created_at.strftime('%B %d, %Y at %I:%M %p')}",
        f"",
        f"View in admin: https://propertism.in/admin/properties/contactmessage/{contact_msg.id}/change/",
    ]
    message = "\n".join(message_lines)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )


def realbot_view(request):
    """Render the premium realBOT AI assistant view"""
    from content.views import home as content_home
    return content_home(request)


# ==============================================================================
# realBOT FUNCTIONAL REST API ENDPOINTS
# ==============================================================================

@csrf_exempt
@require_http_methods(["GET", "POST"])
def init_session(request):
    """
    Initializes a new realBOT consultation session or resumes an existing session.
    """
    if not is_realbot_enabled():
        InfrastructureMetrics.increment("failed_requests")
        return standard_response(
            success=False,
            error_code=ERR_INTEGRATION_DISABLED,
            error_message="realBOT integration is disabled locally",
            status=403
        )

    try:
        session_id_str = None
        if request.method == "POST":
            try:
                data = json.loads(request.body.decode('utf-8'))
                session_id_str = data.get('session_id')
            except Exception:
                session_id_str = request.POST.get('session_id')
        else:
            session_id_str = request.GET.get('session_id')

        session = None
        if session_id_str:
            from django.core.exceptions import ValidationError
            try:
                session = RealBotSession.objects.get(session_id=session_id_str)
            except (RealBotSession.DoesNotExist, ValueError, ValidationError):
                pass

        if not session:
            # Create a brand new session
            user = request.user if request.user.is_authenticated else None
            session = RealBotSession.objects.create(user=user)
            
            # Save the default welcome assistant message
            welcome_text = (
                "Welcome to **realBOT**, the premium advisory portal for **Propertism**.\n"
                "As your digital private wealth manager, I provide institutional-grade advisory on luxury real estate assets in Chennai and key markets.\n\n"
                "How may I assist you with your property portfolio today?"
            )
            welcome_metadata = {
                "chips": ['Luxury Villas', 'Apartments', 'Plots', 'NRI Investment', 'Talk to Advisor']
            }
            RealBotMessage.objects.create(
                session=session,
                sender='assistant',
                text=welcome_text,
                metadata=welcome_metadata
            )

        # Retrieve messages
        messages_query = session.messages.order_by('created_at')
        messages_list = []
        for msg in messages_query:
            messages_list.append({
                "id": msg.id,
                "sender": msg.sender,
                "time": msg.created_at.strftime('%I:%M %p'),
                "text": msg.text,
                "metadata": msg.metadata or {}
            })

        logger.info(f"Initialized realBOT session: {session.session_id}, conversation: {session.conversation_id}")
        return standard_response(
            success=True,
            data={
                "session_id": str(session.session_id),
                "conversation_id": str(session.conversation_id),
                "messages": messages_list
            }
        )

    except Exception as exc:
        logger.exception(f"Error in init_session: {exc}")
        InfrastructureMetrics.increment("failed_requests")
        return standard_response(
            success=False,
            error_code=ERR_DATABASE_ERROR,
            error_message="Internal server session failure",
            status=500
        )


@csrf_exempt
@require_POST
def send_message(request):
    """
    Submits client message, calls AI Service Coordinator, and returns the response metadata.
    """
    if not is_realbot_enabled():
        InfrastructureMetrics.increment("failed_requests")
        return standard_response(
            success=False,
            error_code=ERR_INTEGRATION_DISABLED,
            error_message="realBOT integration is disabled locally",
            status=403
        )

    try:
        # Load request payload
        session_id_str = None
        prompt_text = ""

        try:
            data = json.loads(request.body.decode('utf-8'))
            session_id_str = data.get('session_id')
            prompt_text = data.get('message', '').strip()
        except Exception:
            session_id_str = request.POST.get('session_id')
            prompt_text = request.POST.get('message', '').strip()

        if not session_id_str or not prompt_text:
            InfrastructureMetrics.increment("failed_requests")
            return standard_response(
                success=False,
                error_code=ERR_INVALID_PARAMETERS,
                error_message="Missing session_id or message parameters",
                status=400
            )

        try:
            from django.core.exceptions import ValidationError
            session = RealBotSession.objects.get(session_id=session_id_str)
        except (RealBotSession.DoesNotExist, ValueError, ValidationError):
            InfrastructureMetrics.increment("failed_requests")
            return standard_response(
                success=False,
                error_code=ERR_SESSION_NOT_FOUND,
                error_message="Invalid or expired session session_id",
                status=404
            )

        # 1. Save user prompt
        RealBotMessage.objects.create(
            session=session,
            sender='user',
            text=prompt_text
        )

        # 2. Compile dialog thread history
        db_messages = session.messages.order_by('created_at')
        formatted_history = []
        for msg in db_messages:
            role = "user" if msg.sender == "user" else "assistant"
            formatted_history.append({"role": role, "content": msg.text})

        # 3. Call AI Service Layer (as optional fallback/prose generator)
        ai_response_text = ""
        if is_ai_enabled():
            try:
                service = AIService()
                ai_data = service.get_advisory_response(formatted_history[:-1])
                ai_response_text = ai_data.get("text", "")
            except Exception as ai_exc:
                logger.warning(f"AI Service call failed: {ai_exc}")

        # ── M2.6 & M2.7: Inquiry session & suggestion intercept ──────────────
        from chat.models import InquiryConversationSession
        from chat.inquiry_engine import InquiryConversationEngine, OPEN_STATES
        from chat.suggestion_engine import SuggestionEngine, SuggestionContext

        current_page = ''
        try:
            req_data = json.loads(request.body.decode('utf-8'))
            current_page = req_data.get('current_page', '')
        except Exception:
            current_page = request.POST.get('current_page', '')

        open_ics = InquiryConversationSession.objects.filter(
            realbot_session=session,
            state__in=OPEN_STATES,
        ).order_by('-created_at').first()

        if open_ics:
            inq_engine = InquiryConversationEngine()
            inq_engine.refresh_expiry(open_ics)
            inq_result = inq_engine.process_message(open_ics, prompt_text)
            response_text = inq_result['text']
            response_metadata = inq_result['metadata']
            # Annotate with inquiry context
            response_metadata.setdefault('realbot', {})['intent'] = 'inquiry_creation'

            # M2.7: Context-aware suggestions during active/submitted/cancelled inquiry
            sug_engine = SuggestionEngine()
            sug_ctx = SuggestionContext(
                session=session,
                intent='inquiry_creation',
                inquiry_state=open_ics.state,
                current_page=current_page,
                custom_chips=response_metadata.get('chips', []),
            )
            suggestions = sug_engine.get_suggestions(sug_ctx)
            response_metadata['suggestions'] = suggestions

            # Only update chips if not actively in mandatory collection question
            if open_ics.state in ('awaiting_confirmation', 'submitted', 'cancelled', 'expired'):
                response_metadata['chips'] = [s['display_text'] for s in suggestions]

            assistant_msg = RealBotMessage.objects.create(
                session=session,
                sender='assistant',
                text=response_text,
                metadata=response_metadata,
            )
            logger.info(
                f"realBOT M2.6/M2.7 inquiry & suggestion engine processed message for ICS {open_ics.ics_id}"
            )
            return standard_response(
                success=True,
                data={
                    "message": {
                        "id": assistant_msg.id,
                        "sender": assistant_msg.sender,
                        "time": assistant_msg.created_at.strftime('%I:%M %p'),
                        "text": assistant_msg.text,
                        "metadata": assistant_msg.metadata,
                    }
                },
            )
        # ─────────────────────────────────────────────────────────────────────

        # 4. Rule Engine → Intent Resolution
        from chat.rule_engine import RuleEngine
        from chat.action_handlers import ActionDispatcher

        engine = RuleEngine()
        intent_result = engine.evaluate(prompt_text, session_id=session.session_id)

        # Inject realbot_session object so InquiryWorkflowHandler can create ICS
        intent_result._realbot_session = session

        # 5. Action Dispatch
        dispatcher = ActionDispatcher()
        action_response = dispatcher.dispatch(intent_result, query=prompt_text)

        response_text = action_response.text
        response_metadata = action_response.metadata or {}

        # If action handler did not produce text but AI did, use AI text
        if not response_text and ai_response_text:
            response_text = ai_response_text

        # ── M2.7 Suggestion Engine Integration for Standard Routing ─────────
        # Determine active service profile
        active_service = None
        from chat.models import ServiceProfile
        services = ServiceProfile.objects.filter(status='active').order_by('display_priority')
        for sp in services:
            if intent_result.intent in sp.name.lower().replace(' ', '_'):
                active_service = sp.name
                break

        # Check knowledge article resolution status
        knowledge_resolved = (intent_result.action_type == 'knowledge_response')

        sug_engine = SuggestionEngine()
        sug_ctx = SuggestionContext(
            session=session,
            intent=intent_result.intent,
            active_service_profile=active_service,
            inquiry_state='not_started',
            current_page=current_page,
            knowledge_resolved=knowledge_resolved,
            custom_chips=response_metadata.get('chips', []),
        )
        suggestions = sug_engine.get_suggestions(sug_ctx)
        response_metadata['suggestions'] = suggestions
        response_metadata['chips'] = [s['display_text'] for s in suggestions]
        # ─────────────────────────────────────────────────────────────────────

        # Append rule execution context to metadata
        if 'realbot' not in response_metadata:
            response_metadata['realbot'] = {}
        response_metadata['realbot'].update({
            'intent': intent_result.intent,
            'rule_id': intent_result.rule_id,
            'confidence': round(intent_result.confidence, 2),
            'outcome': intent_result.outcome,
        })

        # 6. Persist Advisor response
        assistant_msg = RealBotMessage.objects.create(
            session=session,
            sender='assistant',
            text=response_text,
            metadata=response_metadata
        )

        logger.info(f"realBOT message processed for session {session.session_id} using intent {intent_result.intent}")
        return standard_response(
            success=True,
            data={
                "message": {
                    "id": assistant_msg.id,
                    "sender": assistant_msg.sender,
                    "time": assistant_msg.created_at.strftime('%I:%M %p'),
                    "text": assistant_msg.text,
                    "metadata": assistant_msg.metadata
                }
            }
        )

    except Exception as exc:
        logger.exception(f"Error in send_message: {exc}")
        InfrastructureMetrics.increment("failed_requests")
        return standard_response(
            success=False,
            error_code=ERR_MESSAGE_PROCESSING_FAILED,
            error_message="Advisory message processing failed",
            status=500
        )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def exchange_token(request):
    """
    Exchanges the Propertism authenticated user session/credentials for a realBOT widget session.
    """
    if not is_realbot_enabled():
        InfrastructureMetrics.increment("failed_requests")
        return standard_response(
            success=False,
            error_code=ERR_INTEGRATION_DISABLED,
            error_message="realBOT integration is disabled locally",
            status=403
        )

    is_authenticated = request.user.is_authenticated
    user_identifier = request.user.email if is_authenticated else "anonymous_user"
    auth_method = "jwt" if is_authenticated else "anonymous"

    import requests
    import uuid

    instance_id = request.session.get('realbot_instance_id')
    if not instance_id:
        instance_id = str(uuid.uuid4())
        request.session['realbot_instance_id'] = instance_id

    realbot_session_token = None
    realbot_error = None

    try:
        instance_url = f"{settings.REALBOT_BASE_URL}/api/v1/widget/instances/"
        instance_payload = {
            "config_code": "propertism_default",
            "instance_id": instance_id,
            "client_url": request.build_absolute_uri('/')
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        if settings.REALBOT_API_KEY:
            headers["Authorization"] = f"ApiKey {settings.REALBOT_API_KEY}"

        instance_response = requests.post(instance_url, json=instance_payload, headers=headers, timeout=5)
        
        if instance_response.status_code in (200, 201):
            session_url = f"{settings.REALBOT_BASE_URL}/api/v1/widget/instances/{instance_id}/session/"
            session_payload = {
                "user_identifier": user_identifier,
                "auth_method": auth_method,
                "metadata": {
                    "username": request.user.username if is_authenticated else "Guest",
                    "full_name": request.user.get_full_name() if is_authenticated else "Guest Visitor",
                }
            }
            session_response = requests.post(session_url, json=session_payload, headers=headers, timeout=5)
            if session_response.status_code in (200, 201):
                session_data = session_response.json()
                if "data" in session_data:
                    realbot_session_token = session_data["data"].get("session_token")
                else:
                    realbot_session_token = session_data.get("session_token")
            else:
                realbot_error = f"Session creation failed: {session_response.status_code} - {session_response.text}"
        else:
            realbot_error = f"Instance registration failed: {instance_response.status_code} - {instance_response.text}"
            
    except requests.exceptions.RequestException as exc:
        realbot_error = f"Connection to realBOT server failed: {str(exc)}"
        logger.warning(f"realBOT handshake connection error: {exc}")

    if not realbot_session_token:
        realbot_session_token = f"mock_session_{uuid.uuid4().hex}"
        logger.info(f"Handshake generated mock session token due to error: {realbot_error}")

    return standard_response(
        success=True,
        data={
            "enabled": True,
            "session_token": realbot_session_token,
            "user": {
                "email": user_identifier,
                "username": request.user.username if is_authenticated else "Guest",
                "is_authenticated": is_authenticated
            },
            "config": {
                "tenant": settings.REALBOT_TENANT,
                "product": settings.REALBOT_PRODUCT,
                "domain": settings.REALBOT_DOMAIN,
                "widget_url": settings.REALBOT_WIDGET_URL,
                "sdk_url": f"{settings.REALBOT_WIDGET_URL}/api/v1/widget/sdk/download/"
            },
            "handshake_status": "mocked_fallback" if realbot_error else "established",
            "handshake_error": realbot_error
        }
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def health_check(request):
    """
    Checks the status of the realBOT integration components (Backward-compatible).
    """
    InfrastructureMetrics.increment("health_requests")
    # 1. Database check
    db_status = "healthy"
    try:
        from django.db import connection
        connection.ensure_connection()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        
    # 2. Integration Enabled check
    integration_enabled = is_realbot_enabled()
    
    # 3. Connection handshake status
    handshake_status = "ready" if integration_enabled else "disabled"

    logger.info(f"realBOT health check requested. status: operational, db: {db_status}")
    return standard_response(
        success=True,
        data={
            "status": "operational" if db_status == "healthy" else "degraded",
            "database": db_status,
            "integration_enabled": integration_enabled,
            "handshake": handshake_status,
            "environment": getattr(settings, 'REALBOT_ENVIRONMENT', 'development')
        }
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def health_live(request):
    """
    Liveness probe: verifies that the application server is up.
    """
    InfrastructureMetrics.increment("health_requests")
    logger.info("realBOT liveness check: operational")
    return standard_response(
        success=True,
        data={
            "status": "alive"
        }
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def health_ready(request):
    """
    Readiness probe: validates database connection and mandatory configurations.
    Returns structured validation details and metrics diagnostics.
    """
    InfrastructureMetrics.increment("health_requests")
    
    # 1. Check Database connection
    db_status = "healthy"
    try:
        from django.db import connection
        connection.ensure_connection()
    except Exception as exc:
        db_status = f"unhealthy: {str(exc)}"
        InfrastructureMetrics.increment("failed_requests")
        
    # 2. Check Configuration
    config_valid, config_issues, config_report = validate_realbot_configuration()
    if not config_valid:
        InfrastructureMetrics.increment("configuration_errors")
        
    status = "ready"
    if db_status != "healthy" or (not config_valid and config_report["integration_enabled"]):
        status = "degraded"
        
    logger.info(f"realBOT readiness check. status: {status}, db: {db_status}")
    return standard_response(
        success=True,
        data={
            "status": status,
            "database": db_status,
            "configuration": "valid" if config_valid else "invalid",
            "diagnostics": {
                "issues": config_issues,
                "report": config_report,
            },
            "metrics": InfrastructureMetrics.get_all()
        }
    )


@csrf_exempt
@require_http_methods(["GET"])
def version_service(request):
    """
    Version endpoint: returns API metadata, feature flags, environments and timestamps.
    """
    is_valid, issues, report = validate_realbot_configuration()
    
    logger.info("realBOT version endpoint requested")
    return standard_response(
        success=True,
        data={
            "api_version": getattr(settings, "REALBOT_API_VERSION", "v1"),
            "build_version": "2.1.1-stable",
            "application_version": "1.0.0-propertism",
            "environment": getattr(settings, "REALBOT_ENVIRONMENT", "development"),
            "feature_flag_status": is_realbot_enabled(),
            "deployment_timestamp": "2026-07-06 19:55:00 UTC",
            "config_status": "valid" if is_valid else "invalid"
        }
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def knowledge_index(request):
    """
    M2.2 — Knowledge Index Management.
    GET: Returns current index statistics (article count by category/source_type).
    POST: Triggers a full re-index of all published website content.
    """
    if request.method == "GET":
        # Return index statistics
        try:
            from django.db.models import Count
            total = KnowledgeArticle.objects.count()
            by_category = list(
                KnowledgeArticle.objects.values('category')
                .annotate(count=Count('id'))
                .order_by('category')
            )
            by_source_type = list(
                KnowledgeArticle.objects.values('source_type')
                .annotate(count=Count('id'))
                .order_by('source_type')
            )
            last_article = KnowledgeArticle.objects.order_by('-indexed_at').first()
            last_indexed = last_article.indexed_at.isoformat() if last_article else None

            logger.info(f"Knowledge index stats requested: {total} articles")
            return standard_response(
                success=True,
                data={
                    "total_articles": total,
                    "by_category": by_category,
                    "by_source_type": by_source_type,
                    "last_indexed": last_indexed,
                }
            )
        except Exception as exc:
            logger.exception(f"Error retrieving knowledge index stats: {exc}")
            return standard_response(
                success=False,
                error_code=ERR_DATABASE_ERROR,
                error_message="Failed to retrieve index statistics",
                status=500
            )

    elif request.method == "POST":
        # Trigger full re-index: Website (M2.2) + Internal Documents (M2.3)
        try:
            from chat.indexer import WebsiteContentIndexer, DocumentIndexer

            website_result = WebsiteContentIndexer().index_all()
            doc_result = DocumentIndexer().index_all_documents()

            combined = {
                "indexed": website_result.indexed + doc_result.indexed,
                "updated": website_result.updated + doc_result.updated,
                "skipped": website_result.skipped + doc_result.skipped,
                "errors": website_result.errors + doc_result.errors,
                "total_processed": (
                    website_result.indexed + website_result.updated + website_result.skipped +
                    doc_result.indexed + doc_result.updated + doc_result.skipped
                ),
                "website": website_result.as_dict(),
                "documents": doc_result.as_dict(),
            }
            logger.info(f"Unified re-index complete: {combined}")
            return standard_response(
                success=True,
                data={
                    "index_result": combined,
                    "message": "Knowledge base re-indexed successfully (Website + Internal Documents)",
                }
            )
        except Exception as exc:
            logger.exception(f"Error during unified knowledge re-index: {exc}")
            return standard_response(
                success=False,
                error_code=ERR_DATABASE_ERROR,
                error_message="Knowledge re-index operation failed",
                status=500
            )


@csrf_exempt
@require_http_methods(["GET"])
def document_index(request):
    """
    M2.3 — Knowledge Document List.
    GET: Returns list of all indexed KnowledgeDocument records.
    Supports ?source_type=Terms filter.
    """
    try:
        from chat.models import KnowledgeDocument
        qs = KnowledgeDocument.objects.all()

        source_type_filter = request.GET.get('source_type', '').strip()
        if source_type_filter:
            qs = qs.filter(source_type=source_type_filter)

        documents = list(qs.values(
            'doc_id', 'title', 'doc_slug', 'file_path',
            'source_type', 'category', 'language', 'tags',
            'version', 'published_status', 'section_count',
            'indexed_at', 'created_at',
        ))
        # Serialize datetimes
        for doc in documents:
            if doc.get('indexed_at'):
                doc['indexed_at'] = doc['indexed_at'].isoformat()
            if doc.get('created_at'):
                doc['created_at'] = doc['created_at'].isoformat()

        logger.info(f"Knowledge document list requested: {len(documents)} documents")
        return standard_response(
            success=True,
            data={
                "total_documents": len(documents),
                "documents": documents,
            }
        )
    except Exception as exc:
        logger.exception(f"Error retrieving knowledge document list: {exc}")
        return standard_response(
            success=False,
            error_code=ERR_DATABASE_ERROR,
            error_message="Failed to retrieve document list",
            status=500
        )

@csrf_exempt
@require_http_methods(["GET"])
def rules_list(request):
    """
    M2.4 — GET /api/v1/realbot/rules/
    Lists all rules in the database.
    """
    try:
        from chat.models import BusinessRule
        qs = BusinessRule.objects.all().order_by('priority', 'name')
        
        # Simple search filter
        search = request.GET.get('search', '').strip()
        if search:
            from django.db.models import Q
            qs = qs.filter(Q(name__icontains=search) | Q(intent__icontains=search))
            
        rules = list(qs.values(
            'rule_id', 'name', 'intent', 'category', 'priority',
            'is_enabled', 'version', 'action_type'
        ))
        
        return standard_response(
            success=True,
            data={
                "total_rules": len(rules),
                "rules": rules
            }
        )
    except Exception as exc:
        logger.exception(f"Error listing rules: {exc}")
        return standard_response(
            success=False,
            error_code=ERR_DATABASE_ERROR,
            error_message="Failed to retrieve rules list",
            status=500
        )

@csrf_exempt
@require_http_methods(["GET"])
def rules_diagnostics(request):
    """
    M2.4 — GET /api/v1/realbot/rules/diagnostics/
    Returns diagnostics statistics for all rules.
    """
    try:
        from django.db.models import Count
        from chat.models import BusinessRule, RuleExecutionLog
        
        total = BusinessRule.objects.count()
        enabled = BusinessRule.objects.filter(is_enabled=True).count()
        disabled = BusinessRule.objects.filter(is_enabled=False).count()
        
        by_category = list(
            BusinessRule.objects.values('category')
            .annotate(count=Count('id'))
            .order_by('category')
        )
        
        by_intent = list(
            BusinessRule.objects.values('intent')
            .annotate(count=Count('id'))
            .order_by('intent')
        )
        
        # Execution logs aggregates
        total_executions = RuleExecutionLog.objects.count()
        by_outcome = list(
            RuleExecutionLog.objects.values('outcome')
            .annotate(count=Count('id'))
            .order_by('outcome')
        )
        
        return standard_response(
            success=True,
            data={
                "rules": {
                    "total": total,
                    "enabled": enabled,
                    "disabled": disabled,
                    "by_category": by_category,
                    "by_intent": by_intent
                },
                "executions": {
                    "total": total_executions,
                    "by_outcome": by_outcome
                }
            }
        )
    except Exception as exc:
        logger.exception(f"Error retrieving rules diagnostics: {exc}")
        return standard_response(
            success=False,
            error_code=ERR_DATABASE_ERROR,
            error_message="Failed to retrieve rules diagnostics",
            status=500
        )

@csrf_exempt
@require_http_methods(["GET"])
def rules_logs(request):
    """
    M2.4 — GET /api/v1/realbot/rules/logs/
    Returns the last 50 rule execution log entries.
    """
    try:
        from chat.models import RuleExecutionLog
        qs = RuleExecutionLog.objects.all().order_by('-created_at')[:50]
        
        logs = []
        for log in qs:
            logs.append({
                'log_id': log.log_id,
                'session_id': str(log.session_id) if log.session_id else None,
                'query': log.query,
                'rule_id': log.matched_rule.rule_id if log.matched_rule else None,
                'rule_name': log.matched_rule.name if log.matched_rule else None,
                'resolved_intent': log.resolved_intent,
                'confidence_score': round(log.confidence_score, 2),
                'rules_evaluated': log.rules_evaluated,
                'outcome': log.outcome,
                'execution_time_ms': log.execution_time_ms,
                'created_at': log.created_at.isoformat()
            })
            
        return standard_response(
            success=True,
            data={
                "total_logged": len(logs),
                "logs": logs
            }
        )
    except Exception as exc:
        logger.exception(f"Error listing rule logs: {exc}")
        return standard_response(
            success=False,
            error_code=ERR_DATABASE_ERROR,
            error_message="Failed to retrieve rule logs",
            status=500
        )

@csrf_exempt
@require_http_methods(["GET"])
def services_list(request):
    """
    M2.5 — GET /api/v1/realbot/services/
    Lists all active Service Profiles in the database.
    """
    try:
        from chat.models import ServiceProfile
        qs = ServiceProfile.objects.filter(status='active').order_by('display_priority', 'name')
        
        category_filter = request.GET.get('category', '').strip()
        if category_filter:
            qs = qs.filter(category=category_filter)
            
        services = list(qs.values(
            'service_id', 'name', 'category', 'short_description', 
            'display_priority', 'version', 'created_at'
        ))
        
        for srv in services:
            if srv.get('created_at'):
                srv['created_at'] = srv['created_at'].isoformat()
                
        return standard_response(
            success=True,
            data={
                "total_services": len(services),
                "services": services
            }
        )
    except Exception as exc:
        logger.exception(f"Error listing services: {exc}")
        return standard_response(
            success=False,
            error_code=ERR_DATABASE_ERROR,
            error_message="Failed to retrieve services list",
            status=500
        )

@csrf_exempt
@require_http_methods(["GET"])
def services_diagnostics(request):
    """
    M2.5 — GET /api/v1/realbot/services/diagnostics/
    Returns diagnostics statistics for all Service Profiles.
    """
    try:
        from django.db.models import Count
        from chat.models import ServiceProfile
        
        total = ServiceProfile.objects.count()
        active = ServiceProfile.objects.filter(status='active').count()
        inactive = ServiceProfile.objects.filter(status='inactive').count()
        
        by_category = list(
            ServiceProfile.objects.values('category')
            .annotate(count=Count('id'))
            .order_by('category')
        )
        
        return standard_response(
            success=True,
            data={
                "total": total,
                "active": active,
                "inactive": inactive,
                "by_category": by_category
            }
        )
    except Exception as exc:
        logger.exception(f"Error retrieving services diagnostics: {exc}")
        return standard_response(
            success=False,
            error_code=ERR_DATABASE_ERROR,
            error_message="Failed to retrieve services diagnostics",
            status=500
        )


# ==============================================================================
# M2.6 — Inquiry Conversation Endpoints
# ==============================================================================

@csrf_exempt
@require_POST
def inquiry_initiate(request):
    """
    M2.6 — POST /api/v1/realbot/inquiry/initiate/
    Explicitly creates a new InquiryConversationSession for a realbot session.
    Accepts: session_id, source (optional), service_hint (optional), message (optional).
    """
    if not is_realbot_enabled():
        return standard_response(success=False, error_code=ERR_INTEGRATION_DISABLED,
                                 error_message="realBOT integration is disabled", status=403)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    session_id_str = data.get('session_id')
    source = data.get('source', 'manual_chat')
    service_hint = data.get('service_hint', '')
    opening_message = data.get('message', '')

    if not session_id_str:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing session_id", status=400)
    try:
        session = RealBotSession.objects.get(session_id=session_id_str)
    except (RealBotSession.DoesNotExist, ValueError):
        return standard_response(success=False, error_code=ERR_SESSION_NOT_FOUND,
                                 error_message="Invalid session_id", status=404)

    try:
        from chat.inquiry_engine import InquiryConversationEngine
        engine = InquiryConversationEngine()
        result = engine.initiate(
            realbot_session=session,
            source=source,
            service_hint=service_hint,
            opening_message=opening_message,
        )
        return standard_response(success=True, data=result)
    except Exception as exc:
        logger.exception(f"Error in inquiry_initiate: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Failed to initiate inquiry session", status=500)


@csrf_exempt
@require_http_methods(["GET"])
def inquiry_status(request):
    """
    M2.6 — GET /api/v1/realbot/inquiry/status/?session_id=...
    Returns the current state and collected data for the active ICS session.
    """
    if not is_realbot_enabled():
        return standard_response(success=False, error_code=ERR_INTEGRATION_DISABLED,
                                 error_message="realBOT integration is disabled", status=403)

    session_id_str = request.GET.get('session_id')
    if not session_id_str:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing session_id", status=400)

    try:
        from chat.models import InquiryConversationSession, INQUIRY_STATE_CHOICES
        from chat.inquiry_engine import OPEN_STATES
        ics = InquiryConversationSession.objects.filter(
            realbot_session__session_id=session_id_str
        ).order_by('-created_at').first()

        if not ics:
            return standard_response(success=True, data={'has_active_session': False})

        return standard_response(success=True, data={
            'has_active_session': ics.state in OPEN_STATES,
            'ics_id': ics.ics_id,
            'state': ics.state,
            'source': ics.source,
            'service_hint': ics.service_hint,
            'fields_collected': list(ics.collected_data.keys()),
            'mandatory_missing': [
                f for f in ['customer_name', 'country', 'mobile_number',
                            'service_required', 'inquiry_message']
                if f not in ics.collected_data
            ],
            'submitted_inquiry_id': ics.submitted_inquiry_id,
            'created_at': ics.created_at.isoformat(),
        })
    except Exception as exc:
        logger.exception(f"Error in inquiry_status: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve inquiry status", status=500)


@csrf_exempt
@require_POST
def inquiry_cancel(request):
    """
    M2.6 — POST /api/v1/realbot/inquiry/cancel/
    Cancels the active ICS session for a realbot session.
    Accepts: session_id, reason (optional).
    """
    if not is_realbot_enabled():
        return standard_response(success=False, error_code=ERR_INTEGRATION_DISABLED,
                                 error_message="realBOT integration is disabled", status=403)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    session_id_str = data.get('session_id')
    reason = data.get('reason', 'API cancellation')

    if not session_id_str:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing session_id", status=400)

    try:
        from chat.models import InquiryConversationSession
        from chat.inquiry_engine import InquiryConversationEngine, OPEN_STATES
        ics = InquiryConversationSession.objects.filter(
            realbot_session__session_id=session_id_str,
            state__in=OPEN_STATES,
        ).order_by('-created_at').first()

        if not ics:
            return standard_response(success=True, data={'cancelled': False,
                                                          'message': 'No active inquiry session found.'})

        engine = InquiryConversationEngine()
        result = engine.handle_cancel(ics, reason=reason)
        return standard_response(success=True, data={'cancelled': True, 'ics_id': ics.ics_id,
                                                      'response': result})
    except Exception as exc:
        logger.exception(f"Error in inquiry_cancel: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to cancel inquiry session", status=500)


@csrf_exempt
@require_http_methods(["GET"])
def inquiry_diagnostics(request):
    """
    M2.6 — GET /api/v1/realbot/inquiry/diagnostics/
    Admin endpoint: session counts by state and source.
    """
    try:
        from django.db.models import Count
        from chat.models import InquiryConversationSession

        total = InquiryConversationSession.objects.count()
        by_state = list(
            InquiryConversationSession.objects.values('state')
            .annotate(count=Count('id'))
            .order_by('state')
        )
        by_source = list(
            InquiryConversationSession.objects.values('source')
            .annotate(count=Count('id'))
            .order_by('source')
        )
        submitted = InquiryConversationSession.objects.filter(state='submitted').count()

        return standard_response(success=True, data={
            'total_sessions': total,
            'submitted': submitted,
            'by_state': by_state,
            'by_source': by_source,
        })
    except Exception as exc:
        logger.exception(f"Error in inquiry_diagnostics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve inquiry diagnostics", status=500)


# ==============================================================================
# M2.7 — Suggestion Interaction & Analytics Endpoints
# ==============================================================================

@csrf_exempt
@require_POST
def inquiry_suggestion_click(request):
    """
    M2.7 — POST /api/v1/realbot/inquiry/suggestion/click/
    Logs a click event for a suggestion chip.
    Accepts: session_id, suggestion_id, display_text, category.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    session_id_str = data.get('session_id')
    suggestion_id = data.get('suggestion_id', '')
    display_text = data.get('display_text', '')
    category = data.get('category', '')

    if not suggestion_id or not display_text:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing suggestion_id or display_text", status=400)

    session = None
    if session_id_str:
        try:
            session = RealBotSession.objects.get(session_id=session_id_str)
        except (RealBotSession.DoesNotExist, ValueError):
            pass

    try:
        from chat.models import SuggestionInteractionLog
        SuggestionInteractionLog.objects.create(
            session=session,
            suggestion_id=suggestion_id,
            display_text=display_text,
            category=category,
            interaction_type='clicked'
        )
        return standard_response(success=True, data={'status': 'logged'})
    except Exception as exc:
        logger.exception(f"Error logging suggestion click: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to log suggestion click", status=500)


@csrf_exempt
@require_http_methods(["GET"])
def inquiry_suggestion_analytics(request):
    """
    M2.7 — GET /api/v1/realbot/inquiry/suggestion/analytics/
    Returns display and click-through metrics for all suggestion chips.
    """
    try:
        from django.db.models import Count, Q
        from chat.models import SuggestionInteractionLog

        # Total counts
        totals = SuggestionInteractionLog.objects.aggregate(
            impressions=Count('id', filter=Q(interaction_type='rendered')),
            clicks=Count('id', filter=Q(interaction_type='clicked'))
        )
        impressions = totals.get('impressions') or 0
        clicks = totals.get('clicks') or 0
        ctr = (clicks / impressions) * 100 if impressions > 0 else 0.0

        # Breakdown by Category
        by_category = []
        cat_stats = SuggestionInteractionLog.objects.values('category').annotate(
            rendered=Count('id', filter=Q(interaction_type='rendered')),
            clicked=Count('id', filter=Q(interaction_type='clicked'))
        ).order_by('-clicked')
        for stat in cat_stats:
            cat_ctr = (stat['clicked'] / stat['rendered']) * 100 if stat['rendered'] > 0 else 0.0
            by_category.append({
                'category': stat['category'],
                'impressions': stat['rendered'],
                'clicks': stat['clicked'],
                'ctr': round(cat_ctr, 2)
            })

        # Breakdown by individual chip
        by_chip = []
        chip_stats = SuggestionInteractionLog.objects.values('suggestion_id', 'display_text').annotate(
            rendered=Count('id', filter=Q(interaction_type='rendered')),
            clicked=Count('id', filter=Q(interaction_type='clicked'))
        ).order_by('-clicked')[:30] # Top 30 performing
        for stat in chip_stats:
            chip_ctr = (stat['clicked'] / stat['rendered']) * 100 if stat['rendered'] > 0 else 0.0
            by_chip.append({
                'suggestion_id': stat['suggestion_id'],
                'display_text': stat['display_text'],
                'impressions': stat['rendered'],
                'clicks': stat['clicked'],
                'ctr': round(chip_ctr, 2)
            })

        return standard_response(success=True, data={
            'overall': {
                'impressions': impressions,
                'clicks': clicks,
                'ctr': round(ctr, 2)
            },
            'by_category': by_category,
            'by_chip': by_chip
        })
    except Exception as exc:
        logger.exception(f"Error retrieving suggestion analytics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve suggestion analytics", status=500)


# ── M2.8 Action Execution & Analytics REST Endpoints ────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def inquiry_action_execute(request):
    """
    POST /api/v1/realbot/action/execute/
    Executes a registered action definition with dynamic parameters.
    """
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload", status=400)

    action_id = data.get('action_id') or data.get('action_name')
    session_id = data.get('session_id')
    parameters = data.get('parameters', {})
    confirm = data.get('confirm', False)

    if not action_id:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required field: action_id or action_name", status=400)

    try:
        from chat.navigation_services import ActionDispatcher
        dispatcher = ActionDispatcher()
        res = dispatcher.dispatch_action(
            action_identifier=action_id,
            session_id=session_id,
            parameters=parameters,
            bypass_confirm=confirm
        )
        if not res['success']:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message=res['error'], status=400)
        return standard_response(success=True, data=res)
    except Exception as exc:
        logger.exception(f"Error executing action: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Action execution failed internally", status=500)


@require_http_methods(["GET"])
def inquiry_action_analytics(request):
    """
    GET /api/v1/realbot/action/analytics/
    Retrieves diagnostics and metrics for dispatched actions.
    """
    try:
        from django.db.models import Count, Q
        from chat.models import ActionExecutionLog

        total_runs = ActionExecutionLog.objects.count()
        valid_runs = ActionExecutionLog.objects.filter(is_validated=True).count()
        invalid_runs = ActionExecutionLog.objects.filter(is_validated=False).count()
        confirmed_runs = ActionExecutionLog.objects.filter(is_confirmed=True).count()
        pending_confirm = ActionExecutionLog.objects.filter(requires_confirmation=True, is_confirmed=False).count()

        # Breakdown by Action ID
        by_action = []
        action_stats = ActionExecutionLog.objects.values('action_id', 'action_name').annotate(
            total=Count('log_id'),
            validated=Count('log_id', filter=Q(is_validated=True)),
            confirmed=Count('log_id', filter=Q(is_confirmed=True))
        ).order_by('-total')[:30]

        for stat in action_stats:
            by_action.append({
                'action_id': stat['action_id'],
                'action_name': stat['action_name'],
                'total_executions': stat['total'],
                'validated': stat['validated'],
                'confirmed': stat['confirmed']
            })

        return standard_response(success=True, data={
            'overall': {
                'total_executions': total_runs,
                'validated_executions': valid_runs,
                'invalid_executions': invalid_runs,
                'confirmed_executions': confirmed_runs,
                'pending_confirmation': pending_confirm,
            },
            'by_action': by_action
        })
    except Exception as exc:
        logger.exception(f"Error retrieving action analytics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve action analytics", status=500)


# ── M2.9 Rich Response REST Endpoints ────────────────────────────────────────

@require_http_methods(["GET"])
def inquiry_response_components(request):
    """
    GET /api/v1/realbot/response/components/
    Lists all active response components from the registry.
    """
    try:
        from chat.models import ResponseComponent
        comps = ResponseComponent.objects.filter(status='active').order_by('rendering_priority')
        data = [{
            'component_id': c.component_id,
            'name': c.name,
            'component_type': c.component_type,
            'display_template': c.display_template,
            'data_schema': c.data_schema,
            'rendering_priority': c.rendering_priority,
            'version': c.version
        } for c in comps]
        return standard_response(success=True, data=data)
    except Exception as exc:
        logger.exception(f"Error retrieving response components: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve response components", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def inquiry_response_compose(request):
    """
    POST /api/v1/realbot/response/compose/
    Assembles multiple response components into a unified structured response payload.
    """
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload", status=400)

    components_list = data.get('components')
    session_id = data.get('session_id')

    if components_list is None or not isinstance(components_list, list):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing or invalid field: components (must be list)", status=400)

    try:
        from chat.response_framework import ResponseBuilder
        builder = ResponseBuilder()
        res = builder.build_composed_response(components_list, session_id=session_id)
        if not res['success']:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message="Composition validation failed",
                                     data={'errors': res['errors']}, status=400)
        return standard_response(success=True, data=res)
    except Exception as exc:
        logger.exception(f"Error composing rich response: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Response composition failed internally", status=500)


@require_http_methods(["GET"])
def inquiry_response_analytics(request):
    """
    GET /api/v1/realbot/response/analytics/
    Retrieves diagnostics and execution stats for composed rich responses.
    """
    try:
        from chat.models import ResponseCompositionLog

        total_compositions = ResponseCompositionLog.objects.count()
        valid_compositions = ResponseCompositionLog.objects.filter(is_validated=True).count()
        invalid_compositions = ResponseCompositionLog.objects.filter(is_validated=False).count()

        success_rate = (valid_compositions / total_compositions) * 100 if total_compositions > 0 else 0.0

        return standard_response(success=True, data={
            'overall': {
                'total_compositions': total_compositions,
                'valid_compositions': valid_compositions,
                'invalid_compositions': invalid_compositions,
                'success_rate_percentage': round(success_rate, 2)
            }
        })
    except Exception as exc:
        logger.exception(f"Error retrieving response composition analytics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve response analytics", status=500)


# ── M2.10 Conversation Context REST Endpoints ───────────────────────────────

@require_http_methods(["GET"])
def inquiry_context_get(request):
    """
    GET /api/v1/realbot/context/get/
    Retrieves the resolved context snapshot for a session_id.
    """
    session_id = request.GET.get('session_id')
    if not session_id:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing query parameter: session_id", status=400)

    try:
        from chat.context_manager import ConversationContextManager, ContextResolutionEngine
        mgr = ConversationContextManager()
        engine = ContextResolutionEngine()
        context = mgr.get_or_create_context(session_id)
        snapshot = engine.resolve_conversation_context(context)
        return standard_response(success=True, data=snapshot)
    except Exception as exc:
        logger.exception(f"Error retrieving conversation context: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve conversation context", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def inquiry_context_update(request):
    """
    POST /api/v1/realbot/context/update/
    Updates intents, service mappings, state, and conversation variables.
    """
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload", status=400)

    session_id = data.get('session_id')
    if not session_id:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required field: session_id", status=400)

    try:
        from chat.context_manager import ConversationContextManager, ContextResolutionEngine
        mgr = ConversationContextManager()
        engine = ContextResolutionEngine()
        context = mgr.get_or_create_context(session_id)

        # Update root metadata fields if present
        if 'intent' in data:
            context.active_intent = data['intent']
        if 'service' in data:
            context.active_service = data['service']
        if 'inquiry_id' in data:
            context.active_inquiry_id = data['inquiry_id']
        if 'state' in data:
            context.conversation_state = data['state']
        if 'last_knowledge_topic' in data:
            context.last_knowledge_topic = data['last_knowledge_topic']

        context.save()

        # Update variables if present
        variables = data.get('variables', {})
        if variables:
            errors = mgr.update_variables(context, variables)
            if errors:
                return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                         error_message="Variable validation failed",
                                         data={'errors': errors}, status=400)

        snapshot = engine.resolve_conversation_context(context)
        return standard_response(success=True, data=snapshot)
    except Exception as exc:
        logger.exception(f"Error updating conversation context: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Failed to update context internally", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def inquiry_context_switch_topic(request):
    """
    POST /api/v1/realbot/context/switch-topic/
    Performs topic switching and stack restorations.
    """
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload", status=400)

    session_id = data.get('session_id')
    new_topic = data.get('new_topic')
    restore = data.get('restore', False)

    if not session_id:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required field: session_id", status=400)

    try:
        from chat.context_manager import ConversationContextManager, TopicManager, ContextResolutionEngine
        mgr = ConversationContextManager()
        topic_mgr = TopicManager()
        engine = ContextResolutionEngine()
        context = mgr.get_or_create_context(session_id)

        if restore:
            topic_mgr.restore_previous_topic(context)
        elif new_topic:
            topic_mgr.switch_topic(context, new_topic)
        else:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message="Must specify new_topic or restore=True", status=400)

        snapshot = engine.resolve_conversation_context(context)
        return standard_response(success=True, data=snapshot)
    except Exception as exc:
        logger.exception(f"Error switching conversation topic: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Failed to switch topic internally", status=500)


@require_http_methods(["GET"])
def inquiry_context_analytics(request):
    """
    GET /api/v1/realbot/context/analytics/
    Retrieves diagnostics and logs for conversation context activity.
    """
    try:
        from chat.models import ConversationContext, ContextUpdateLog
        from django.db.models import Count

        total_contexts = ConversationContext.objects.count()
        total_switches = ContextUpdateLog.objects.filter(action='topic_switch').count()
        total_restores = ContextUpdateLog.objects.filter(action='topic_restore').count()

        intent_stats = ConversationContext.objects.exclude(active_intent='').values('active_intent').annotate(
            total=Count('context_id')
        ).order_by('-total')

        intents_breakdown = {item['active_intent']: item['total'] for item in intent_stats}

        return standard_response(success=True, data={
            'overall': {
                'total_contexts': total_contexts,
                'total_topic_switches': total_switches,
                'total_topic_restorations': total_restores,
            },
            'intents_breakdown': intents_breakdown
        })
    except Exception as exc:
        logger.exception(f"Error retrieving context analytics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve context analytics", status=500)


# ── M2.11 Analytics, Diagnostics & Observability REST Endpoints ───────────────

@csrf_exempt
@require_http_methods(["POST"])
def analytics_event_publish(request):
    """
    POST /api/v1/realbot/analytics/event/publish/
    Publishes an operational event to the platform event log.
    """
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload", status=400)

    event_type = data.get('event_type')
    provider = data.get('provider')
    session_id = data.get('session_id')
    payload = data.get('payload', {})
    duration_ms = data.get('duration_ms')

    if not event_type or not provider:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required field: event_type or provider", status=400)

    try:
        from chat.analytics_engine import EventPublisher
        pub = EventPublisher()
        evt = pub.publish_event(
            event_type=event_type,
            provider=provider,
            session_id=session_id,
            payload=payload,
            duration_ms=duration_ms
        )
        return standard_response(success=True, data={
            'event_id': evt.event_id,
            'event_type': evt.event_type,
            'provider': evt.provider,
            'created_at': evt.created_at.isoformat() if evt.created_at else None
        })
    except Exception as exc:
        logger.exception(f"Error publishing analytics event: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Event publication failed internally", status=500)


@require_http_methods(["GET"])
def analytics_metrics_get(request):
    """
    GET /api/v1/realbot/analytics/metrics/
    Retrieves aggregated operational metrics for the platform.
    """
    try:
        from chat.analytics_engine import MetricsCalculator
        calc = MetricsCalculator()
        metrics = calc.compute_all_metrics()
        return standard_response(success=True, data=metrics)
    except Exception as exc:
        logger.exception(f"Error computing analytics metrics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to compute operational metrics", status=500)


@require_http_methods(["GET"])
def analytics_health_get(request):
    """
    GET /api/v1/realbot/analytics/health/
    Retrieves live platform liveness health monitoring and diagnostics parameters.
    """
    try:
        from chat.analytics_engine import HealthMonitoringFramework
        health = HealthMonitoringFramework()
        res = health.check_health()
        status_code = 200 if res['status'] == 'healthy' else 500
        return standard_response(success=(res['status'] == 'healthy'), data=res, status=status_code)
    except Exception as exc:
        logger.exception(f"Error checking platform health: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve health checks", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def analytics_aggregate_trigger(request):
    """
    POST /api/v1/realbot/analytics/aggregate/
    Triggers consolidating aggregated counts caches.
    """
    try:
        data = json.loads(request.body) if request.body else {}
    except (ValueError, TypeError):
        data = {}

    window_type = data.get('window_type', 'daily')

    try:
        from chat.analytics_engine import EventAggregationEngine
        engine = EventAggregationEngine()
        processed = engine.aggregate_metrics(window_type=window_type)
        return standard_response(success=True, data={
            'processed_aggregates': processed,
            'window_type': window_type
        })
    except Exception as exc:
        logger.exception(f"Error running aggregation: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Aggregation process failed", status=500)


# ── M2.12 Administration & Configuration REST Endpoints ───────────────────────

@require_http_methods(["GET"])
def config_get_view(request):
    """
    GET /api/v1/realbot/config/get/
    Fetches a setting value.
    """
    key = request.GET.get('key')
    if not key:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required parameter: key", status=400)

    try:
        from chat.config_manager import ConfigurationManager
        val = ConfigurationManager.get_setting(key)
        return standard_response(success=True, data={'key': key, 'value': val})
    except Exception as exc:
        logger.exception(f"Error fetching configuration key '{key}': {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve configuration item", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def config_update_view(request):
    """
    POST /api/v1/realbot/config/update/
    Updates setting value.
    """
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload", status=400)

    key = data.get('key')
    value = data.get('value')
    modified_by = data.get('modified_by', 'admin')

    if not key or value is None:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required field: key or value", status=400)

    try:
        from chat.config_manager import ConfigurationManager
        item = ConfigurationManager.update_setting(key=key, value_str=str(value), modified_by=modified_by)
        return standard_response(success=True, data={
            'key': item.key,
            'value': item.value,
            'version': item.version,
            'status': item.status
        })
    except ValueError as val_err:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message=str(val_err), status=400)
    except Exception as exc:
        logger.exception(f"Error updating configuration: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Configuration update failed", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def config_rollback_view(request):
    """
    POST /api/v1/realbot/config/rollback/
    Rollbacks a setting to target version state.
    """
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload", status=400)

    key = data.get('key')
    version = data.get('version')
    modified_by = data.get('modified_by', 'admin')

    if not key or not version:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required field: key or version", status=400)

    try:
        from chat.config_manager import ConfigurationManager
        item = ConfigurationManager.rollback_setting(key=key, target_version=int(version), modified_by=modified_by)
        return standard_response(success=True, data={
            'key': item.key,
            'value': item.value,
            'version': item.version,
            'status': item.status
        })
    except ValueError as val_err:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message=str(val_err), status=400)
    except Exception as exc:
        logger.exception(f"Error rolling back configuration: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Configuration rollback failed", status=500)


@require_http_methods(["GET"])
def config_audit_view(request):
    """
    GET /api/v1/realbot/config/audit/
    Retrieves audit trails list for key.
    """
    key = request.GET.get('key')
    if not key:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required parameter: key", status=400)

    try:
        from chat.models import ConfigurationAuditLog
        logs = ConfigurationAuditLog.objects.filter(config_item__key=key).order_by('-created_at')
        audit_list = []
        for log in logs:
            audit_list.append({
                'audit_id': log.audit_id,
                'action': log.action,
                'previous_value': log.previous_value,
                'new_value': log.new_value,
                'version': log.version,
                'modified_by': log.modified_by,
                'created_at': log.created_at.isoformat()
            })
        return standard_response(success=True, data={'key': key, 'history': audit_list})
    except Exception as exc:
        logger.exception(f"Error fetching config audit trail: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve config audit history", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def config_import_view(request):
    """
    POST /api/v1/realbot/config/import/
    Imports config JSON records list.
    """
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload", status=400)

    configs_list = data if isinstance(data, list) else data.get('configurations', [])
    modified_by = data.get('modified_by', 'admin') if isinstance(data, dict) else 'admin'

    try:
        from chat.config_manager import ConfigurationManager
        imported_count = ConfigurationManager.import_configurations(configs_list, modified_by=modified_by)
        return standard_response(success=True, data={'imported_count': imported_count})
    except Exception as exc:
        logger.exception(f"Error importing configuration: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Configuration import failed", status=500)


@require_http_methods(["GET"])
def config_export_view(request):
    """
    GET /api/v1/realbot/config/export/
    Exports config JSON records list.
    """
    try:
        from chat.config_manager import ConfigurationManager
        exported = ConfigurationManager.export_configurations()
        return standard_response(success=True, data={'configurations': exported})
    except Exception as exc:
        logger.exception(f"Error exporting configurations: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to export configuration", status=500)


# ── M2.13 Conversation Orchestration REST Endpoints ───────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def orchestrator_message_view(request):
    """
    POST /api/v1/realbot/orchestrator/message/
    Single message processing pipeline gateway.
    """
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload", status=400)

    session_id = data.get('session_id')
    message_text = data.get('message_text')
    page_path = data.get('page_path', '/home/')
    category = data.get('category', 'General')

    if not session_id or not message_text:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required field: session_id or message_text", status=400)

    try:
        from chat.orchestrator import ConversationOrchestrator
        orch = ConversationOrchestrator()
        res = orch.process_message(
            session_id=session_id,
            message_text=message_text,
            page_path=page_path,
            category=category
        )
        return standard_response(success=True, data=res)
    except Exception as exc:
        logger.exception(f"Error in orchestrating message: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Orchestrator process failed internally", status=500)


@require_http_methods(["GET"])
def orchestrator_workflow_status_view(request):
    """
    GET /api/v1/realbot/orchestrator/workflow/status/
    Retrieves execution state parameters of a workflow ID.
    """
    workflow_id = request.GET.get('workflow_id')
    if not workflow_id:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required parameter: workflow_id", status=400)

    try:
        from chat.models import OrchestrationWorkflow
        wf = OrchestrationWorkflow.objects.get(workflow_id=workflow_id)
        return standard_response(success=True, data={
            'workflow_id': wf.workflow_id,
            'session_id': wf.session_id,
            'state': wf.state,
            'current_stage': wf.current_stage,
            'payload': wf.payload,
            'created_at': wf.created_at.isoformat()
        })
    except OrchestrationWorkflow.DoesNotExist:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message=f"Workflow '{workflow_id}' not found.", status=404)
    except Exception as exc:
        logger.exception(f"Error checking workflow status: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve workflow details", status=500)


@require_http_methods(["GET"])
def orchestrator_workflow_trace_view(request):
    """
    GET /api/v1/realbot/orchestrator/workflow/trace/
    Retrieves timing trace values list for stages.
    """
    workflow_id = request.GET.get('workflow_id')
    if not workflow_id:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Missing required parameter: workflow_id", status=400)

    try:
        from chat.models import WorkflowExecutionStep
        steps = WorkflowExecutionStep.objects.filter(workflow__workflow_id=workflow_id).order_by('created_at')
        trace_list = []
        for step in steps:
            trace_list.append({
                'step_id': step.step_id,
                'stage': step.stage,
                'status': step.status,
                'duration_ms': step.duration_ms,
                'logs': step.logs,
                'created_at': step.created_at.isoformat()
            })
        return standard_response(success=True, data={'workflow_id': workflow_id, 'trace': trace_list})
    except Exception as exc:
        logger.exception(f"Error fetching workflow trace: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to retrieve workflow step trace", status=500)


@require_http_methods(["GET"])
def orchestrator_workflow_analytics_view(request):
    """
    GET /api/v1/realbot/orchestrator/workflow/analytics/
    Retrieves orchestration execution performance averages.
    """
    try:
        from django.db.models import Avg
        from chat.models import OrchestrationWorkflow, WorkflowExecutionStep
        total_runs = OrchestrationWorkflow.objects.count()
        failed_runs = OrchestrationWorkflow.objects.filter(state='Failed').count()

        stage_averages = WorkflowExecutionStep.objects.values('stage').annotate(
            avg_duration=Avg('duration_ms')
        ).order_by('stage')

        stats = {item['stage']: round(item['avg_duration'], 2) for item in stage_averages}

        return standard_response(success=True, data={
            'total_executions': total_runs,
            'failed_executions': failed_runs,
            'success_rate_percentage': round(((total_runs - failed_runs) / total_runs * 100.0) if total_runs > 0 else 100.0, 2),
            'stage_average_durations_ms': stats
        })
    except Exception as exc:
        logger.exception(f"Error retrieving orchestrator analytics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to compute orchestrator performance analytics", status=500)


# ── M2.14 Security REST API Endpoints ──────────────────────────────────────────

@require_http_methods(["GET"])
def security_events_view(request):
    """
    GET /api/v1/realbot/inquiry/security/events/
    Lists security audit events with optional event_type and severity filters.
    """
    try:
        from chat.models import SecurityEvent
        event_type = request.GET.get('event_type')
        severity = request.GET.get('severity')
        
        events = SecurityEvent.objects.all()
        if event_type:
            events = events.filter(event_type=event_type)
        if severity:
            events = events.filter(severity=severity)
            
        data_list = []
        for e in events[:100]:  # Limit to 100 events
            data_list.append({
                'event_id': e.event_id,
                'event_type': e.event_type,
                'severity': e.severity,
                'source_ip': e.source_ip,
                'session_id': e.session_id,
                'request_path': e.request_path,
                'details': e.details,
                'created_at': e.created_at.isoformat()
            })
        return standard_response(success=True, data={'events': data_list})
    except Exception as exc:
        logger.exception(f"Error listing security events: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to list security audit events", status=500)


@require_http_methods(["GET"])
def security_policies_view(request):
    """
    GET /api/v1/realbot/inquiry/security/policies/
    Lists active security policies.
    """
    try:
        from chat.models import SecurityPolicy
        policies = SecurityPolicy.objects.filter(is_active=True)
        data_list = []
        for p in policies:
            data_list.append({
                'policy_id': p.policy_id,
                'policy_key': p.policy_key,
                'domain': p.domain,
                'policy_type': p.policy_type,
                'value': p.value,
                'default_value': p.default_value
            })
        return standard_response(success=True, data={'policies': data_list})
    except Exception as exc:
        logger.exception(f"Error listing security policies: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to list security policies", status=500)


@require_POST
@csrf_exempt
def security_validate_view(request):
    """
    POST /api/v1/realbot/inquiry/security/validate/
    Validates a request payload against security rules.
    """
    try:
        from chat.security_manager import SecurityManager
        payload = json.loads(request.body.decode('utf-8'))
        
        manager = SecurityManager()
        result = manager.validate_request(payload)
        
        return standard_response(success=True, data=result)
    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload.", status=400)
    except Exception as exc:
        logger.exception(f"Error in ad-hoc security validation: {exc}")
        return standard_response(success=False, error_code=ERR_MESSAGE_PROCESSING_FAILED,
                                 error_message="Security validation failed execution.", status=500)


@require_http_methods(["GET"])
def security_analytics_view(request):
    """
    GET /api/v1/realbot/inquiry/security/analytics/
    Computes security event statistics.
    """
    try:
        from chat.models import SecurityEvent
        from django.db.models import Count
        
        total_events = SecurityEvent.objects.count()
        by_type = SecurityEvent.objects.values('event_type').annotate(count=Count('event_id'))
        by_severity = SecurityEvent.objects.values('severity').annotate(count=Count('event_id'))
        
        type_stats = {item['event_type']: item['count'] for item in by_type}
        severity_stats = {item['severity']: item['count'] for item in by_severity}
        
        return standard_response(success=True, data={
            'total_security_events': total_events,
            'event_type_distribution': type_stats,
            'severity_distribution': severity_stats
        })
    except Exception as exc:
        logger.exception(f"Error computing security analytics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to compute security analytics", status=500)


@require_http_methods(["GET"])
def security_governance_view(request):
    """
    GET /api/v1/realbot/inquiry/security/governance/
    Returns governance reporting summary.
    """
    try:
        from chat.models import SecurityEvent, SecurityPolicy
        
        active_policies_count = SecurityPolicy.objects.filter(is_active=True).count()
        critical_violations_count = SecurityEvent.objects.filter(severity='critical').count()
        warning_violations_count = SecurityEvent.objects.filter(severity='warning').count()
        
        # Summary description
        compliance_status = "Compliant"
        if critical_violations_count > 0:
            compliance_status = "Action Required (Critical Violations Found)"
        elif warning_violations_count > 5:
            compliance_status = "Review Recommended (Excessive Warnings Found)"
            
        return standard_response(success=True, data={
            'compliance_status': compliance_status,
            'active_security_policies': active_policies_count,
            'critical_security_violations': critical_violations_count,
            'warning_security_violations': warning_violations_count
        })
    except Exception as exc:
        logger.exception(f"Error creating governance report: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to compile security governance report", status=500)


# ── M2.15 Knowledge Administration REST API Endpoints ─────────────────────────

@require_http_methods(["GET"])
def knowledge_admin_list_view(request):
    """
    GET /api/v1/realbot/inquiry/knowledge/admin/list/
    Lists knowledge articles and documents in catalog.
    """
    try:
        from chat.models import KnowledgeArticle, KnowledgeDocument
        
        status = request.GET.get('status')
        source_type = request.GET.get('source_type')
        
        articles = KnowledgeArticle.objects.all()
        docs = KnowledgeDocument.objects.all()
        
        if status:
            articles = articles.filter(status=status)
            docs = docs.filter(status=status)
        if source_type:
            articles = articles.filter(source_type=source_type)
            docs = docs.filter(source_type=source_type)
            
        articles_data = []
        for a in articles[:100]:
            articles_data.append({
                'knowledge_id': a.knowledge_id,
                'page_title': a.page_title,
                'source_type': a.source_type,
                'category': a.category,
                'status': a.status,
                'version': a.version,
                'quality_score': a.quality_score,
                'usage_count': a.usage_count,
                'last_modified': a.last_modified.isoformat() if a.last_modified else None
            })
            
        docs_data = []
        for d in docs[:100]:
            docs_data.append({
                'doc_id': d.doc_id,
                'title': d.title,
                'doc_slug': d.doc_slug,
                'source_type': d.source_type,
                'category': d.category,
                'status': d.status,
                'version': d.version,
                'quality_score': d.quality_score,
                'usage_count': d.usage_count,
                'indexed_at': d.indexed_at.isoformat() if d.indexed_at else None
            })
            
        return standard_response(success=True, data={
            'articles': articles_data,
            'documents': docs_data
        })
    except Exception as exc:
        logger.exception(f"Error listing knowledge items: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to list knowledge items", status=500)


@require_POST
@csrf_exempt
def knowledge_admin_update_view(request):
    """
    POST /api/v1/realbot/inquiry/knowledge/admin/update/
    Creates or updates a knowledge article.
    """
    try:
        from chat.models import KnowledgeArticle
        from chat.knowledge_manager import KnowledgeAdministrationManager
        
        payload = json.loads(request.body.decode('utf-8'))
        knowledge_id = payload.get('knowledge_id')
        user = payload.get('user', 'admin')
        
        mgr = KnowledgeAdministrationManager()
        
        if knowledge_id:
            try:
                article = KnowledgeArticle.objects.get(knowledge_id=knowledge_id)
                updated = mgr.edit_article(article, payload, user=user)
                return standard_response(success=True, data={
                    'knowledge_id': updated.knowledge_id,
                    'version': updated.version,
                    'quality_score': updated.quality_score,
                    'status': updated.status
                })
            except KnowledgeArticle.DoesNotExist:
                return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                         error_message=f"Article {knowledge_id} not found.", status=404)
        else:
            # Registration requires page_title and source_ref
            if 'page_title' not in payload or 'source_ref' not in payload:
                return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                         error_message="page_title and source_ref are required to register.", status=400)
            
            created = mgr.register_article(payload, user=user)
            return standard_response(success=True, data={
                'knowledge_id': created.knowledge_id,
                'version': created.version,
                'quality_score': created.quality_score,
                'status': created.status
            })
            
    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload.", status=400)
    except Exception as exc:
        logger.exception(f"Error registering/updating article: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message=f"Failed to update knowledge: {str(exc)}", status=500)


@require_POST
@csrf_exempt
def knowledge_admin_publish_view(request):
    """
    POST /api/v1/realbot/inquiry/knowledge/admin/publish/
    Transitions the lifecycle status of a knowledge article or document.
    """
    try:
        from chat.models import KnowledgeArticle, KnowledgeDocument
        from chat.knowledge_manager import KnowledgePublishingFramework
        
        payload = json.loads(request.body.decode('utf-8'))
        knowledge_id = payload.get('knowledge_id')
        doc_id = payload.get('doc_id')
        new_status = payload.get('status')
        user = payload.get('user', 'admin')
        
        if not new_status:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message="Missing parameter: status", status=400)
            
        pub_mgr = KnowledgePublishingFramework()
        
        if knowledge_id:
            try:
                article = KnowledgeArticle.objects.get(knowledge_id=knowledge_id)
                success, msg = pub_mgr.transition_state(article, new_status, user=user)
                return standard_response(success=success, data={'message': msg, 'quality_score': article.quality_score})
            except KnowledgeArticle.DoesNotExist:
                return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                         error_message=f"Article {knowledge_id} not found.", status=404)
        elif doc_id:
            try:
                doc = KnowledgeDocument.objects.get(doc_id=doc_id)
                success, msg = pub_mgr.transition_state(doc, new_status, user=user)
                return standard_response(success=success, data={'message': msg, 'quality_score': doc.quality_score})
            except KnowledgeDocument.DoesNotExist:
                return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                         error_message=f"Document {doc_id} not found.", status=404)
        else:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message="Either knowledge_id or doc_id is required.", status=400)
            
    except ValueError as val_err:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message=str(val_err), status=400)
    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload.", status=400)
    except Exception as exc:
        logger.exception(f"Error publishing knowledge item: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to publish knowledge item.", status=500)


@require_POST
@csrf_exempt
def knowledge_admin_rollback_view(request):
    """
    POST /api/v1/realbot/inquiry/knowledge/admin/rollback/
    Reverts an article or document to a previous version history entry.
    """
    try:
        from chat.models import KnowledgeVersionHistory
        from chat.knowledge_manager import KnowledgeVersionManager
        
        payload = json.loads(request.body.decode('utf-8'))
        version_id = payload.get('version_id')
        user = payload.get('user', 'admin')
        
        if not version_id:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message="Missing parameter: version_id", status=400)
            
        try:
            hist = KnowledgeVersionHistory.objects.get(version_id=version_id)
            v_mgr = KnowledgeVersionManager()
            success, msg = v_mgr.rollback(hist, user=user)
            return standard_response(success=success, data={'message': msg})
        except KnowledgeVersionHistory.DoesNotExist:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message=f"Version history {version_id} not found.", status=404)
            
    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload.", status=400)
    except Exception as exc:
        logger.exception(f"Error rolling back version: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to rollback knowledge version.", status=500)


@require_POST
@csrf_exempt
def knowledge_admin_reindex_view(request):
    """
    POST /api/v1/realbot/inquiry/knowledge/admin/reindex/
    Triggers indexing run.
    """
    try:
        from chat.knowledge_manager import KnowledgeReindexFramework
        payload = json.loads(request.body.decode('utf-8')) if request.body else {}
        source_type = payload.get('source_type')
        
        reindex_mgr = KnowledgeReindexFramework()
        stats = reindex_mgr.trigger_reindex(source_type=source_type)
        
        return standard_response(success=True, data={'indexing_statistics': stats})
    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload.", status=400)
    except Exception as exc:
        logger.exception(f"Error during manual reindexing run: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Re-indexing run failed.", status=500)


@require_http_methods(["GET"])
def knowledge_admin_analytics_view(request):
    """
    GET /api/v1/realbot/inquiry/knowledge/admin/analytics/
    Returns quality and usage analytics aggregates.
    """
    try:
        from chat.models import KnowledgeArticle, KnowledgeDocument, KnowledgeLifecycleAuditLog
        from django.db.models import Avg, Sum, Count
        
        articles_count = KnowledgeArticle.objects.count()
        avg_quality = KnowledgeArticle.objects.aggregate(avg=Avg('quality_score'))['avg'] or 100.0
        total_usage = KnowledgeArticle.objects.aggregate(total=Sum('usage_count'))['total'] or 0
        
        by_status = KnowledgeArticle.objects.values('status').annotate(count=Count('knowledge_id'))
        status_dist = {item['status']: item['count'] for item in by_status}
        
        recent_audits = KnowledgeLifecycleAuditLog.objects.all()[:10]
        audits_data = []
        for audit in recent_audits:
            audits_data.append({
                'audit_id': audit.audit_id,
                'action': audit.action,
                'performed_by': audit.performed_by,
                'target': audit.article_id or audit.doc_id,
                'created_at': audit.created_at.isoformat()
            })
            
        return standard_response(success=True, data={
            'total_knowledge_articles': articles_count,
            'average_quality_score': round(avg_quality, 2),
            'total_usage_hits': total_usage,
            'status_distribution': status_dist,
            'recent_audit_trail': audits_data
        })
    except Exception as exc:
        logger.exception(f"Error collecting knowledge analytics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to compute knowledge metrics.", status=500)


# ── M2.16 Analytics & Customer Insights Views ─────────────────────────────────

@csrf_exempt
@require_http_methods(["GET"])
def insights_dashboard_view(request):
    """
    GET /api/v1/realbot/inquiry/insights/dashboard/
    Resolves metrics for the 8 dashboards with configurable filters.
    """
    try:
        filters = {
            'start_date': request.GET.get('start_date'),
            'end_date': request.GET.get('end_date'),
            'service': request.GET.get('service'),
            'country': request.GET.get('country')
        }
        from chat.insights_manager import BusinessAnalyticsManager
        mgr = BusinessAnalyticsManager(filters=filters)
        data = mgr.build_dashboard_data()
        return standard_response(success=True, data=data)
    except Exception as exc:
        logger.exception(f"Error building dashboard metrics: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to build dashboard metrics.", status=500)


@csrf_exempt
@require_http_methods(["GET"])
def insights_report_view(request):
    """
    GET /api/v1/realbot/inquiry/insights/report/
    Compiles operational telemetry report.
    """
    try:
        filters = {
            'start_date': request.GET.get('start_date'),
            'end_date': request.GET.get('end_date'),
            'service': request.GET.get('service'),
            'country': request.GET.get('country')
        }
        from chat.insights_manager import BusinessAnalyticsManager
        from django.utils import timezone
        mgr = BusinessAnalyticsManager(filters=filters)
        data = mgr.build_dashboard_data()
        return standard_response(success=True, data={
            'report_generated_at': timezone.now().isoformat(),
            'filters_applied': filters,
            'summary': data.get('executive'),
            'details': data
        })
    except Exception as exc:
        logger.exception(f"Error generating reports: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to generate reports.", status=500)


@csrf_exempt
@require_http_methods(["GET"])
def insights_export_view(request):
    """
    GET /api/v1/realbot/inquiry/insights/export/
    Generates downloadable CSV metrics.
    """
    try:
        filters = {
            'start_date': request.GET.get('start_date'),
            'end_date': request.GET.get('end_date'),
            'service': request.GET.get('service'),
            'country': request.GET.get('country')
        }
        from chat.insights_manager import BusinessAnalyticsManager, ReportGenerator
        from django.http import HttpResponse
        
        mgr = BusinessAnalyticsManager(filters=filters)
        data = mgr.build_dashboard_data()
        
        gen = ReportGenerator(data)
        csv_content = gen.generate_csv_report()
        
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="realbot_insights_report.csv"'
        return response
    except Exception as exc:
        logger.exception(f"Error exporting metrics report: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to export metrics report.", status=500)


@csrf_exempt
@require_http_methods(["GET"])
def insights_recommendations_view(request):
    """
    GET /api/v1/realbot/inquiry/insights/recommendations/
    Yields dynamic business insight recommendations.
    """
    try:
        filters = {
            'start_date': request.GET.get('start_date'),
            'end_date': request.GET.get('end_date'),
            'service': request.GET.get('service'),
            'country': request.GET.get('country')
        }
        from chat.insights_manager import BusinessAnalyticsManager, InsightEngine
        mgr = BusinessAnalyticsManager(filters=filters)
        data = mgr.build_dashboard_data()
        
        engine = InsightEngine(data)
        recs = engine.generate_recommendations()
        return standard_response(success=True, data={'recommendations': recs})
    except Exception as exc:
        logger.exception(f"Error building insight recommendations: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to build insight recommendations.", status=500)


# ── Website Conversational Knowledge Extraction Framework Endpoints ──────────

@require_POST
@csrf_exempt
def knowledge_extraction_trigger_view(request):
    """
    POST /api/v1/realbot/inquiry/knowledge/extraction/trigger/
    Triggers extraction and reconciliation engine.
    """
    try:
        from chat.knowledge_extractor import WebsiteConversationalExtractor, KnowledgeReconciliationEngine
        
        extractor = WebsiteConversationalExtractor()
        reconciler = KnowledgeReconciliationEngine()
        
        raw_candidates = extractor.extract_all_entities()
        candidates, report = reconciler.reconcile_all(raw_candidates)
        
        return standard_response(success=True, data={
            'reconciliation_report': report,
            'candidates_count': len(candidates)
        })
    except Exception as exc:
        logger.exception(f"Error triggering conversational knowledge extraction: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message=f"Extraction failed: {str(exc)}", status=500)


@require_http_methods(["GET"])
def knowledge_extraction_candidates_view(request):
    """
    GET /api/v1/realbot/inquiry/knowledge/extraction/candidates/
    Lists generated candidates with status and classification filters.
    """
    try:
        from chat.models import ExtractedKnowledgeCandidate
        
        classification = request.GET.get('classification')
        status = request.GET.get('status')
        entity_type = request.GET.get('entity_type')
        
        qs = ExtractedKnowledgeCandidate.objects.all()
        if classification:
            qs = qs.filter(classification=classification)
        if status:
            qs = qs.filter(status=status)
        if entity_type:
            qs = qs.filter(entity_type=entity_type)
            
        data_list = []
        for c in qs[:200]:
            try:
                alts = json.loads(c.alternative_questions)
            except Exception:
                alts = []
            data_list.append({
                'candidate_id': c.candidate_id,
                'entity_type': c.entity_type,
                'entity_name': c.entity_name,
                'primary_question': c.primary_question,
                'alternative_questions': alts,
                'canonical_answer': c.canonical_answer,
                'keywords': c.keywords,
                'synonyms': c.synonyms,
                'source_url': c.source_url,
                'source_section': c.source_section,
                'search_weight': c.search_weight,
                'language': c.language,
                'classification': c.classification,
                'status': c.status,
                'matched_article_id': c.matched_article.knowledge_id if c.matched_article else None,
                'created_at': c.created_at.isoformat()
            })
            
        return standard_response(success=True, data={'candidates': data_list})
    except Exception as exc:
        logger.exception(f"Error listing conversational candidates: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message="Failed to list candidates", status=500)


@require_POST
@csrf_exempt
def knowledge_extraction_approve_view(request):
    """
    POST /api/v1/realbot/inquiry/knowledge/extraction/approve/
    Approves candidate IDs, migrating them to KnowledgeArticle.
    """
    try:
        from django.utils import timezone
        from chat.models import ExtractedKnowledgeCandidate, KnowledgeArticle, KnowledgeLifecycleAuditLog
        from chat.knowledge_manager import KnowledgeVersionManager
        
        payload = json.loads(request.body.decode('utf-8'))
        candidate_ids = payload.get('candidate_ids', [])
        user = payload.get('user', 'admin')
        
        if not candidate_ids:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message="Missing parameter: candidate_ids", status=400)
                                     
        candidates = ExtractedKnowledgeCandidate.objects.filter(candidate_id__in=candidate_ids, status='draft')
        approved_count = 0
        
        version_mgr = KnowledgeVersionManager()
        
        for c in candidates:
            entity_slug = c.entity_name.lower().replace(' ', '-')
            source_ref = f"Conversational:{c.entity_type}:{entity_slug}:{c.candidate_id}"
            
            keywords_combined = f"{c.keywords} {c.synonyms} {c.primary_question}"
            try:
                alts = json.loads(c.alternative_questions)
            except Exception:
                alts = []
            main_content = "\n".join([c.canonical_answer] + alts)
            
            defaults = {
                'page_title': c.primary_question,
                'url': c.source_url,
                'category': 'General',
                'language': c.language,
                'keywords': keywords_combined,
                'summary': c.canonical_answer,
                'main_content': main_content,
                'published_status': 'published',
                'search_weight': c.search_weight,
                'source_type': 'Website',
                'status': 'published',
                'modified_by': user,
                'last_modified': timezone.now()
            }
            
            if c.matched_article:
                article = c.matched_article
                version_mgr.create_version(article=article, user=user)
                
                article.page_title = defaults['page_title']
                article.url = defaults['url']
                article.keywords = defaults['keywords']
                article.summary = defaults['summary']
                article.main_content = defaults['main_content']
                article.search_weight = defaults['search_weight']
                article.modified_by = user
                article.version += 1
                article.last_modified = timezone.now()
                article.save()
                
                KnowledgeLifecycleAuditLog.objects.create(
                    article_id=article.knowledge_id,
                    action='edited',
                    performed_by=user,
                    details={'source': 'conversational_extraction', 'candidate_id': c.candidate_id}
                )
            else:
                article = KnowledgeArticle.objects.create(
                    source_ref=source_ref,
                    **defaults
                )
                
                KnowledgeLifecycleAuditLog.objects.create(
                    article_id=article.knowledge_id,
                    action='registered',
                    performed_by=user,
                    details={'source': 'conversational_extraction', 'candidate_id': c.candidate_id}
                )
                
            c.status = 'approved'
            c.matched_article = article
            c.save()
            approved_count += 1
            
        return standard_response(success=True, data={
            'approved_count': approved_count,
            'message': f"Successfully approved and published {approved_count} candidates."
        })
    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload.", status=400)
    except Exception as exc:
        logger.exception(f"Error during candidate approval: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message=f"Approval run failed: {str(exc)}", status=500)


@require_POST
@csrf_exempt
def knowledge_extraction_reject_view(request):
    """
    POST /api/v1/realbot/inquiry/knowledge/extraction/reject/
    Rejects candidate IDs.
    """
    try:
        from django.utils import timezone
        from chat.models import ExtractedKnowledgeCandidate
        payload = json.loads(request.body.decode('utf-8'))
        candidate_ids = payload.get('candidate_ids', [])
        
        if not candidate_ids:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message="Missing parameter: candidate_ids", status=400)
                                     
        rejected_count = ExtractedKnowledgeCandidate.objects.filter(
            candidate_id__in=candidate_ids, status='draft'
        ).update(status='rejected', updated_at=timezone.now())
        
        return standard_response(success=True, data={
            'rejected_count': rejected_count,
            'message': f"Successfully rejected {rejected_count} candidates."
        })
    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload.", status=400)
    except Exception as exc:
        logger.exception(f"Error during candidate rejection: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message=f"Rejection run failed: {str(exc)}", status=500)


@require_POST
@csrf_exempt
def knowledge_extraction_update_view(request):
    """
    POST /api/v1/realbot/inquiry/knowledge/extraction/update/
    Updates fields of a draft candidate.
    """
    try:
        from chat.models import ExtractedKnowledgeCandidate
        payload = json.loads(request.body.decode('utf-8'))
        candidate_id = payload.get('candidate_id')
        
        if not candidate_id:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message="Missing parameter: candidate_id", status=400)
                                     
        try:
            c = ExtractedKnowledgeCandidate.objects.get(candidate_id=candidate_id, status='draft')
            if 'primary_question' in payload:
                c.primary_question = payload['primary_question']
            if 'canonical_answer' in payload:
                c.canonical_answer = payload['canonical_answer']
            if 'keywords' in payload:
                c.keywords = payload['keywords']
            if 'synonyms' in payload:
                c.synonyms = payload['synonyms']
            if 'search_weight' in payload:
                c.search_weight = float(payload['search_weight'])
            if 'alternative_questions' in payload:
                c.alternative_questions = json.dumps(payload['alternative_questions'])
                
            c.save()
            return standard_response(success=True, data={'candidate_id': c.candidate_id, 'message': "Candidate updated successfully."})
        except ExtractedKnowledgeCandidate.DoesNotExist:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message=f"Draft candidate {candidate_id} not found.", status=404)
    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message="Invalid JSON payload.", status=400)
    except Exception as exc:
        logger.exception(f"Error during candidate update: {exc}")
        return standard_response(success=False, error_code=ERR_DATABASE_ERROR,
                                 error_message=f"Update failed: {str(exc)}", status=500)


# ══════════════════════════════════════════════════════════════════════════════
# M2.17 — Human Handover & Conversation Closure Views
# ══════════════════════════════════════════════════════════════════════════════

from chat.handover_manager import (
    HumanHandoverManager, AdvisorQueueManager, AdvisorConversationManager,
    ConversationClosureManager, TranscriptGenerator, TranscriptEmailDispatcher,
    ConversationArchiveManager, ConversationLifecycleManager, HandoverAnalyticsAggregator,
)
from chat.models import HandoverRequest, AdvisorProfile, ConversationArchive


@require_POST
@csrf_exempt
def handover_request(request):
    """
    POST /inquiry/handover/request/
    Customer requests handover to a human advisor.
    Body: { session_id, customer_name?, customer_email?, customer_phone?, reason? }
    """
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        if not session_id:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message='session_id is required.', status=400)

        try:
            session = RealBotSession.objects.get(pk=session_id)
        except RealBotSession.DoesNotExist:
            return standard_response(success=False, error_code=ERR_SESSION_NOT_FOUND,
                                     error_message='Session not found.', status=404)

        lifecycle = ConversationLifecycleManager()
        result = lifecycle.request_handover(
            session=session,
            customer_name=data.get('customer_name', ''),
            customer_email=data.get('customer_email', ''),
            customer_phone=data.get('customer_phone', ''),
            reason=data.get('reason', ''),
        )
        return standard_response(success=result['success'], data=result)

    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message='Invalid JSON payload.', status=400)
    except Exception as exc:
        logger.exception(f'Handover request error: {exc}')
        return standard_response(success=False, error_code=ERR_HANDOVER_FAILED,
                                 error_message=str(exc), status=500)


@require_http_methods(['GET'])
def handover_status(request):
    """
    GET /inquiry/handover/status/?handover_id=HOV000001
    Check the status of a handover request.
    """
    handover_id = request.GET.get('handover_id')
    if not handover_id:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message='handover_id is required.', status=400)

    mgr = HumanHandoverManager()
    result = mgr.get_handover_status(handover_id)
    return standard_response(success=result['success'], data=result.get('data'), error_code=result.get('error_code'),
                             error_message=result.get('error_message'), status=404 if not result['success'] else 200)


@require_http_methods(['GET'])
def advisor_waiting_list(request):
    """
    GET /inquiry/handover/advisor/waiting/
    List all handover requests waiting for advisor assignment.
    """
    waiting = AdvisorQueueManager.get_waiting_handovers()
    results = []
    for h in waiting:
        results.append({
            'handover_id': h.handover_id,
            'session_id': str(h.session.session_id),
            'customer_name': h.customer_name,
            'reason': h.reason,
            'created_at': h.created_at.isoformat(),
        })
    return standard_response(success=True, data={'waiting_count': len(results), 'handovers': results})


@require_POST
@csrf_exempt
def advisor_accept(request):
    """
    POST /inquiry/handover/advisor/accept/
    Advisor accepts a handover request.
    Body: { handover_id, advisor_id }
    """
    try:
        data = json.loads(request.body)
        handover_id = data.get('handover_id')
        advisor_id = data.get('advisor_id')

        if not handover_id or not advisor_id:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message='handover_id and advisor_id are required.', status=400)

        try:
            handover = HandoverRequest.objects.get(handover_id=handover_id)
        except HandoverRequest.DoesNotExist:
            return standard_response(success=False, error_code=ERR_HANDOVER_NOT_FOUND,
                                     error_message='Handover not found.', status=404)

        try:
            advisor = AdvisorProfile.objects.get(advisor_id=advisor_id, is_active=True)
        except AdvisorProfile.DoesNotExist:
            return standard_response(success=False, error_code=ERR_ADVISOR_NOT_FOUND,
                                     error_message='Advisor not found.', status=404)

        # Assign this specific advisor
        handover.assigned_advisor = advisor
        handover.assigned_at = timezone.now()
        handover.status = 'accepted'
        handover.save()

        advisor.active_chat_count += 1
        if advisor.active_chat_count >= advisor.max_concurrent_chats:
            advisor.status = ADVISOR_BUSY
        advisor.save()

        from chat.models import HandoverAuditLog
        HandoverAuditLog.objects.create(
            session=handover.session, handover=handover,
            action='advisor_assigned', performed_by=advisor.display_name,
            details={'advisor_id': advisor.advisor_id},
        )

        return standard_response(success=True, data={
            'handover_id': handover.handover_id,
            'advisor_id': advisor.advisor_id,
            'advisor_name': advisor.display_name,
            'status': 'accepted',
        })

    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message='Invalid JSON payload.', status=400)
    except Exception as exc:
        logger.exception(f'Advisor accept error: {exc}')
        return standard_response(success=False, error_code=ERR_HANDOVER_FAILED,
                                 error_message=str(exc), status=500)


@require_POST
@csrf_exempt
def advisor_message(request):
    """
    POST /inquiry/handover/advisor/message/
    Advisor sends a message in a handover conversation.
    Body: { handover_id, advisor_id, message }
    """
    try:
        data = json.loads(request.body)
        handover_id = data.get('handover_id')
        advisor_id = data.get('advisor_id')
        message_text = data.get('message', '')

        if not handover_id or not advisor_id or not message_text:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message='handover_id, advisor_id, and message are required.', status=400)

        try:
            handover = HandoverRequest.objects.get(handover_id=handover_id)
        except HandoverRequest.DoesNotExist:
            return standard_response(success=False, error_code=ERR_HANDOVER_NOT_FOUND,
                                     error_message='Handover not found.', status=404)

        try:
            advisor = AdvisorProfile.objects.get(advisor_id=advisor_id, is_active=True)
        except AdvisorProfile.DoesNotExist:
            return standard_response(success=False, error_code=ERR_ADVISOR_NOT_FOUND,
                                     error_message='Advisor not found.', status=404)

        mgr = AdvisorConversationManager()
        result = mgr.send_message(handover, advisor, message_text)
        return standard_response(success=result['success'], data=result,
                                 error_code=result.get('error_code'),
                                 error_message=result.get('error_message'),
                                 status=403 if not result['success'] else 200)

    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message='Invalid JSON payload.', status=400)
    except Exception as exc:
        logger.exception(f'Advisor message error: {exc}')
        return standard_response(success=False, error_code=ERR_HANDOVER_FAILED,
                                 error_message=str(exc), status=500)


@require_POST
@csrf_exempt
def advisor_close(request):
    """
    POST /inquiry/handover/advisor/close/
    Advisor closes a handover conversation.
    Body: { handover_id, advisor_id }
    """
    try:
        data = json.loads(request.body)
        handover_id = data.get('handover_id')
        advisor_id = data.get('advisor_id')

        if not handover_id or not advisor_id:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message='handover_id and advisor_id are required.', status=400)

        try:
            handover = HandoverRequest.objects.get(handover_id=handover_id)
        except HandoverRequest.DoesNotExist:
            return standard_response(success=False, error_code=ERR_HANDOVER_NOT_FOUND,
                                     error_message='Handover not found.', status=404)

        if handover.assigned_advisor and handover.assigned_advisor.advisor_id != advisor_id:
            return standard_response(success=False, error_code=ERR_ADVISOR_NOT_AUTHORIZED,
                                     error_message='This advisor is not assigned to this handover.', status=403)

        mgr = ConversationClosureManager()
        result = mgr.request_closure(handover, requested_by=advisor_id)
        return standard_response(success=result['success'], data=result,
                                 error_code=result.get('error_code'),
                                 error_message=result.get('error_message'),
                                 status=400 if not result['success'] else 200)

    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message='Invalid JSON payload.', status=400)
    except Exception as exc:
        logger.exception(f'Advisor close error: {exc}')
        return standard_response(success=False, error_code=ERR_HANDOVER_FAILED,
                                 error_message=str(exc), status=500)


@require_POST
@csrf_exempt
def customer_end_conversation(request):
    """
    POST /inquiry/handover/customer/end/
    Customer ends the conversation.
    Body: { session_id, send_email?, email_recipients? }
    """
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        if not session_id:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message='session_id is required.', status=400)

        try:
            session = RealBotSession.objects.get(pk=session_id)
        except RealBotSession.DoesNotExist:
            return standard_response(success=False, error_code=ERR_SESSION_NOT_FOUND,
                                     error_message='Session not found.', status=404)

        lifecycle = ConversationLifecycleManager()
        result = lifecycle.complete_lifecycle(
            session=session,
            closure_reason=CLOSURE_CUSTOMER_INITIATED,
            closed_by='customer',
            send_email=data.get('send_email', True),
            email_recipients=data.get('email_recipients'),
        )
        return standard_response(success=True, data=result)

    except json.JSONDecodeError:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message='Invalid JSON payload.', status=400)
    except Exception as exc:
        logger.exception(f'Customer end conversation error: {exc}')
        return standard_response(success=False, error_code=ERR_HANDOVER_FAILED,
                                 error_message=str(exc), status=500)


@require_http_methods(['GET'])
def conversation_transcript(request):
    """
    GET /inquiry/handover/transcript/?session_id=<uuid>
    Get the transcript for a conversation.
    """
    session_id = request.GET.get('session_id')
    if not session_id:
        return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                 error_message='session_id is required.', status=400)

    try:
        session = RealBotSession.objects.get(pk=session_id)
    except RealBotSession.DoesNotExist:
        return standard_response(success=False, error_code=ERR_SESSION_NOT_FOUND,
                                 error_message='Session not found.', status=404)

    transcript = TranscriptGenerator.generate_html_transcript(session)
    return standard_response(success=True, data={'transcript': transcript})


@require_http_methods(['GET'])
def conversation_archive_list(request):
    """
    GET /inquiry/handover/archives/?limit=50
    List conversation archives.
    """
    limit = int(request.GET.get('limit', 50))
    archives = ConversationArchiveManager.list_archives(limit=limit)
    return standard_response(success=True, data={'archives': archives, 'count': len(archives)})


@require_http_methods(['GET'])
def handover_diagnostics(request):
    """
    GET /inquiry/handover/diagnostics/
    Diagnostics endpoint for handover system health.
    """
    from chat.models import HandoverAuditLog

    total_handovers = HandoverRequest.objects.count()
    pending = HandoverRequest.objects.filter(status='requested').count()
    active = HandoverRequest.objects.filter(status='accepted').count()
    completed = HandoverRequest.objects.filter(status='completed').count()
    total_advisors = AdvisorProfile.objects.filter(is_active=True).count()
    available_advisors = AdvisorProfile.objects.filter(status=ADVISOR_AVAILABLE, is_active=True).count()
    total_archives = ConversationArchive.objects.count()
    total_audit_logs = HandoverAuditLog.objects.count()

    return standard_response(success=True, data={
        'handovers': {
            'total': total_handovers,
            'pending': pending,
            'active': active,
            'completed': completed,
        },
        'advisors': {
            'total': total_advisors,
            'available': available_advisors,
        },
        'archives': total_archives,
        'audit_logs': total_audit_logs,
    })


@require_http_methods(['GET'])
def handover_analytics(request):
    """
    GET /inquiry/handover/analytics/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
    Get handover analytics for a date range.
    """
    from datetime import datetime, timedelta

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return standard_response(success=False, error_code=ERR_INVALID_PARAMETERS,
                                     error_message='Invalid date format. Use YYYY-MM-DD.', status=400)
    else:
        # Default to last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

    aggregator = HandoverAnalyticsAggregator()
    result = aggregator.compute_period_analytics(start_date, end_date)
    return standard_response(success=result['success'], data=result)








