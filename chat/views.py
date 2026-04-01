import logging
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from properties.models import ContactMessage

logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt  # We'll handle CSRF in the frontend
def submit_chat_message(request):
    """Handle chat message submission"""
    try:
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validate required fields
        if not name or not email or not message:
            return JsonResponse({
                'success': False,
                'error': 'Please fill in all required fields'
            }, status=400)
        
        # Save to database using ContactMessage model
        contact_msg = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject='',  # Chat messages don't have subject
            message=message,
            status='pending'
        )
        
        logger.info(f"Chat message received from {email}")
        
        # Send email notification
        try:
            send_chat_notification(contact_msg)
        except Exception as email_exc:
            logger.error(f"Failed to send chat notification: {email_exc}")
            # Don't fail the request if email fails
        
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
