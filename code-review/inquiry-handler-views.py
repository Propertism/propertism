# Extracted from: content/views.py
# Lines: 280–364
# Purpose: Inquiry form POST handler + email notification chain

def contact(request):
    """Homepage quote form handler."""
    if request.method == "POST":
        try:
            inquiry = PropertyInquiry.objects.create(
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone", ""),
                message=request.POST.get("message"),
                property=None,  # Quote form doesn't link to specific property
                status='pending'
            )
            logger.info("Quote inquiry received from %s", inquiry.email)

            # Send email notification to admin
            try:
                send_rfq_notification(inquiry)
            except Exception as email_exc:
                logger.error("Failed to send email notification: %s", email_exc)
                # Don't fail the request if email fails

            messages.success(request, "Thank you for your inquiry! We will get back to you soon.")
            return redirect(get_home_section_links()["contact"])
        except Exception as exc:
            logger.exception("Error processing contact form: %s", exc)
            messages.error(
                request,
                "There was an error submitting your inquiry. Please try again or call us directly.",
            )
            return redirect(get_home_section_links()["contact"])

    return redirect_to_home_section(request, "contact")


def send_rfq_notification(inquiry):
    """Send email and whatsapp notification when RFQ is submitted."""
    subject = f"🚀 New Propertism Lead: {inquiry.name}"

    # Build email body
    message_lines = [
        f"You have a new inquiry from the website:",
        f"",
        f"Name: {inquiry.name}",
        f"Email: {inquiry.email}",
        f"Phone: {inquiry.phone or 'Not provided'}",
        f"Message: {inquiry.message}",
        f"",
        f"Submitted: {inquiry.created_at.strftime('%B %d, %Y at %I:%M %p')}",
        f"Admin View: https://propertism.in/admin/properties/inquiry/{inquiry.id}/change/",
    ]

    message = "\n".join(message_lines)

    # Send email to info@propertism.in
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],  # RISK: not defined in settings_production.py
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Email notification failed: {e}")

    # Trigger WhatsApp
    send_whatsapp_notification(f"🚀 *New Lead*: {inquiry.name}\nPhone: {inquiry.phone}\nMsg: {inquiry.message}")
