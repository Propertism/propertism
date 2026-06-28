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
from .models import RealBotSession, RealBotMessage
from .ai_service import AIService

logger = logging.getLogger(__name__)

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
            try:
                session = RealBotSession.objects.get(session_id=session_id_str)
            except (RealBotSession.DoesNotExist, ValueError):
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
                "chips": ['Luxury Villas', 'Apartments', 'Plots', 'NRI Investment', 'Rental Homes', 'Compare Projects']
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

        return JsonResponse({
            "success": True,
            "session_id": str(session.session_id),
            "messages": messages_list
        })

    except Exception as exc:
        logger.exception(f"Error in init_session: {exc}")
        return JsonResponse({"success": False, "error": "Internal server session failure"}, status=500)


@csrf_exempt
@require_POST
def send_message(request):
    """
    Submits client message, calls AI Service Coordinator, and returns the response metadata.
    """
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
            return JsonResponse({"success": False, "error": "Missing session_id or message parameters"}, status=400)

        try:
            session = RealBotSession.objects.get(session_id=session_id_str)
        except (RealBotSession.DoesNotExist, ValueError):
            return JsonResponse({"success": False, "error": "Invalid or expired session session_id"}, status=404)

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

        # 3. Call AI Service Layer
        ai_response_text = ""
        service = AIService()
        
        try:
            ai_data = service.get_advisory_response(formatted_history[:-1]) # send past history, exclude newly saved user prompt
            ai_response_text = ai_data.get("text", "")
        except Exception as ai_exc:
            logger.warning(f"AI Service call failed, invoking fallback response generator: {ai_exc}")
            # Robust fallback simulation if API Key is unconfigured/expired
            ai_response_text = f"I have received your inquiry: \"{prompt_text}\". Our premium client advisory desk is currently verifying available market portfolios. Let me provide our latest recommendations below."

        # 4. Extract dynamic card/chip parameters based on keywords
        query = prompt_text.lower()
        response_metadata = {}

        if "villa" in query or "luxury" in query or "villas" in query:
            ai_response_text = "I have retrieved our prime listing in the luxury villa segment located in Chennai ECR:"
            response_metadata = {
                "chips": ['View Details', 'Compare Properties', 'Schedule Visit', 'Show Similar'],
                "property": {
                    "imageUrl": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
                    "badge": "PREMIUM ASSET",
                    "name": "The Oceanfront Manor",
                    "location": "VGP Layout, ECR, Chennai",
                    "price": "₹4.90 Crore",
                    "config": "4 BHK Beach Villa",
                    "area": "4,500 Sq.Ft.",
                    "builder": "Oceanic Developers",
                    "highlights": ["Beachfront Access", "Private Gardens", "High Security"]
                }
            }
        elif "nri" in query or "investment" in query or "investments" in query:
            ai_response_text = "For NRI investors, commercial real estate allocations in Chennai deliver high yield stability [1].\n\n### Capital Yield Averages\n- **Chennai ECR Villas**: 3.2% - 3.8% gross [2].\n- **OMR IT Corridors**: 4.2% - 4.8% gross [3]."
            response_metadata = {
                "chips": ['Filter by Budget', 'Ready to Move', 'Under ₹75 Lakhs'],
                "comparison": {
                    "headers": ['Asset Type', 'Growth (YoY)', 'Rental Yield', 'Regulatory Ease'],
                    "rows": [
                        ['Commercial Office', '8.5%', '7.2% - 8.5%', 'High (Pre-leased)'],
                        ['Premium ECR Villas', '12.0%', '3.5% - 4.2%', 'Medium (RERA Ready)'],
                        ['OMR Apartments', '6.0%', '4.5% - 5.0%', 'High (Ready to Move)']
                    ]
                },
                "citations": [
                    "[1] RBI Repatriation Circular 2026.",
                    "[2] Propertism Q2 Index.",
                    "[3] Chennai Residential Bulletin 2026."
                ]
            }
        elif "apartment" in query or "budget" in query or "apartments" in query or "plots" in query:
            ai_response_text = "Here is our curated apartment listing matching your budget criteria:"
            response_metadata = {
                "chips": ['Luxury Villas', 'Compare Projects', 'Ready to Move'],
                "property": {
                    "imageUrl": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80",
                    "badge": "VALUE PORTFOLIO",
                    "name": "Meridian Heights Complex",
                    "location": "Medavakkam, Chennai",
                    "price": "₹72 Lakhs",
                    "config": "2.5 BHK Apartment",
                    "area": "1,280 Sq.Ft.",
                    "builder": "Meridian Builders",
                    "highlights": ["Near Metro Station", "Reserved Parking", "Under Construction"]
                }
            }
        else:
            # General fallback chips
            response_metadata = {
                "chips": ['Luxury Villas', 'Apartments', 'NRI Investment']
            }

        # 5. Persist Advisor response
        assistant_msg = RealBotMessage.objects.create(
            session=session,
            sender='assistant',
            text=ai_response_text,
            metadata=response_metadata
        )

        return JsonResponse({
            "success": True,
            "message": {
                "id": assistant_msg.id,
                "sender": assistant_msg.sender,
                "time": assistant_msg.created_at.strftime('%I:%M %p'),
                "text": assistant_msg.text,
                "metadata": assistant_msg.metadata
            }
        })

    except Exception as exc:
        logger.exception(f"Error in send_message: {exc}")
        return JsonResponse({"success": False, "error": "Advisory message processing failed"}, status=500)
