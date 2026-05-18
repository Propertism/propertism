import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.db.utils import OperationalError, ProgrammingError
from django.http import Http404, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from properties.models import Property
from properties.models import Inquiry as PropertyInquiry

from .models import (
    BlogPost,
    CoreValue,
    CustomerReviewSection,
    ExpertiseArea,
    HomepageCard,
    HomepageCardSection,
    LandingLead,
    Newsletter,
    Service,
    Statistic,
    TeamMember,
)
from .site_context import (
    get_active_core_values,
    get_active_expertise_areas,
    get_active_services,
    get_company_info,
    get_contact_property_choices,
    get_contact_service_choices,
    get_hero_title_segments,
    get_home_section_links,
)

logger = logging.getLogger(__name__)
RECOVERABLE_DB_ERRORS = (OperationalError, ProgrammingError)


def _safe_list(queryset, *, fallback=None, warning=None):
    try:
        if callable(queryset):
            queryset = queryset()
        return list(queryset)
    except RECOVERABLE_DB_ERRORS:
        if warning:
            logger.warning(warning, exc_info=True)
        return [] if fallback is None else fallback


def _safe_first(queryset, *, fallback=None, warning=None):
    try:
        if callable(queryset):
            queryset = queryset()
        return queryset.first()
    except RECOVERABLE_DB_ERRORS:
        if warning:
            logger.warning(warning, exc_info=True)
        return fallback


def health(request):
    """Lightweight endpoint for load balancer health checks.
    
    This endpoint bypasses Django's ALLOWED_HOSTS validation to ensure
    load balancer health checks always succeed regardless of Host header.
    """
    from django.http import HttpResponse
    return HttpResponse("OK", content_type="text/plain", status=200)


def redirect_default_language(request, path=""):
    """Redirect legacy /en/... URLs to the default-language root paths."""
    normalized_path = path.lstrip("/")
    target = f"/{normalized_path}" if normalized_path else "/"
    query_string = request.META.get("QUERY_STRING")
    if query_string:
        target = f"{target}?{query_string}"
    return HttpResponsePermanentRedirect(target)


def get_company_context():
    """Get company info for all pages."""
    return {"company": get_company_info()}


def redirect_to_home_section(request, section_name):
    return redirect(get_home_section_links()[section_name])


def home(request):
    """Homepage view."""
    context = get_company_context()
    company = context["company"]
    all_services = get_active_services()
    expertise_areas = get_active_expertise_areas(limit=4)
    customer_reviews = []
    customer_review_slides = []
    customer_review_section = None
    custom_card_sections = []
    hero_background_urls = []

    try:
        if getattr(company, "pk", None):
            hero_background_urls = company.get_active_hero_background_urls()
    except RECOVERABLE_DB_ERRORS:
        logger.warning("Homepage hero background tables are unavailable.", exc_info=True)
        hero_background_urls = []

    customer_review_section = _safe_first(
        lambda: CustomerReviewSection.objects.filter(is_active=True),
        warning="Homepage customer review section table is unavailable.",
    )
    if customer_review_section:
        customer_reviews = _safe_list(
            lambda: customer_review_section.reviews.filter(is_active=True),
            warning="Homepage customer review table is unavailable.",
        )
        customer_review_slides = [
            customer_reviews[index:index + 6]
            for index in range(0, len(customer_reviews), 6)
        ]
    custom_card_sections = _safe_list(
        lambda: HomepageCardSection.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "cards",
                queryset=HomepageCard.objects.filter(is_active=True),
                to_attr="active_cards",
            )
        ),
        warning="Homepage custom card section tables are unavailable.",
    )

    if not hero_background_urls:
        fallback_hero_url = company.get_primary_hero_image_url()
        if fallback_hero_url:
            hero_background_urls = [fallback_hero_url]

    context.update(
        {
            "stats": _safe_list(
                lambda: Statistic.objects.filter(is_active=True)[:4],
                warning="Homepage statistics table is unavailable.",
            ),
            "service_highlights": all_services[:4],
            "credibility_points": get_active_core_values(limit=4),
            "core_values": get_active_core_values(limit=3),
            "expertise_highlights": expertise_areas,
            "featured_properties": _safe_list(
                lambda: Property.objects.filter(status="available").prefetch_related("photos")[:6],
                warning="Homepage featured properties table is unavailable.",
            ),
            "team_highlights": _safe_list(
                lambda: TeamMember.objects.filter(is_active=True)[:3],
                warning="Homepage team member table is unavailable.",
            ),
            "recent_posts": _safe_list(
                lambda: BlogPost.objects.filter(is_published=True)[:3],
                warning="Homepage blog post table is unavailable.",
            ),
            "customer_review_section": customer_review_section,
            "customer_reviews": customer_reviews,
            "customer_review_slides": customer_review_slides,
            "custom_card_sections": custom_card_sections,
            "contact_property_choices": get_contact_property_choices(),
            "contact_service_choices": get_contact_service_choices(),
            "hero_background_urls": hero_background_urls,
            "hero_title_segments": get_hero_title_segments(company.hero_title),
            "breadcrumbs": [{"name": "Home", "url": None}],
        }
    )
    return render(request, "home-premium.html", context)


def services(request):
    """Services page view."""
    context = get_company_context()
    context.update({
        "services": _safe_list(
            lambda: Service.objects.filter(is_active=True),
            warning="Services table is unavailable.",
        ),
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Services", "url": None}
        ],
    })
    return render(request, "services.html", context)


def about(request):
    """About page view."""
    context = get_company_context()
    context.update({
        "stats": _safe_list(
            lambda: Statistic.objects.filter(is_active=True),
            warning="About page statistics table is unavailable.",
        ),
        "values": _safe_list(
            lambda: CoreValue.objects.filter(is_active=True),
            warning="About page core values table is unavailable.",
        ),
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "About", "url": None}
        ],
    })
    return render(request, "about.html", context)


def management(request):
    """Management page view."""
    context = get_company_context()
    context.update({
        "team_members": _safe_list(
            lambda: TeamMember.objects.filter(is_active=True),
            warning="Management page team member table is unavailable.",
        ),
        "expertise_areas": _safe_list(
            lambda: ExpertiseArea.objects.filter(is_active=True),
            warning="Management page expertise area table is unavailable.",
        ),
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Management", "url": None}
        ],
    })
    return render(request, "management.html", context)


def team_member_detail(request, slug):
    """Team member profile detail page."""
    team_member = _safe_first(
        lambda: TeamMember.objects.filter(slug=slug, is_active=True),
        warning="Team member detail table is unavailable.",
    )
    if not team_member:
        raise Http404
    context = get_company_context()
    context.update({
        "team_member": team_member,
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Management", "url": "/management/"},
            {"name": team_member.name, "url": None}
        ],
    })
    return render(request, "team_member_detail.html", context)


def blog(request):
    """Blog listing page view."""
    return redirect_to_home_section(request, "blog")


def blog_post(request, slug):
    """Individual blog post view."""
    context = get_company_context()
    post = _safe_first(
        lambda: BlogPost.objects.filter(slug=slug, is_published=True),
        warning="Blog post table is unavailable.",
    )
    if not post:
        raise Http404
    context.update(
        {
            "post": post,
            "recent_posts": _safe_list(
                lambda: BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3],
                warning="Recent blog post table is unavailable.",
            ),
        }
    )
    return render(request, "blog_post.html", context)


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


def send_admin_notification(subject, message_lines, whatsapp_text):
    """Send email and WhatsApp notifications for new lead activity."""
    message = "\n".join(message_lines)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ADMIN_EMAILS,
            fail_silently=False,
        )
    except Exception as exc:
        logger.error("Email notification failed: %s", exc)

    send_whatsapp_notification(whatsapp_text)


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
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ADMIN_EMAILS,
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Email notification failed: {e}")

    # Trigger WhatsApp
    send_whatsapp_notification(f"🚀 *New Lead*: {inquiry.name}\nPhone: {inquiry.phone}\nMsg: {inquiry.message}")


def send_landing_lead_notification(lead):
    """Send notifications for landing-page lead submissions."""
    qualification = lead.qualification_data or {}
    extras = []
    if qualification.get("selling_timeline"):
        extras.append(f"Selling timeline: {qualification['selling_timeline']}")
    if qualification.get("occupancy_status"):
        extras.append(f"Occupancy: {qualification['occupancy_status']}")
    if qualification.get("expected_rent"):
        extras.append(f"Expected rent: {qualification['expected_rent']}")
    if lead.expected_price_range:
        extras.append(f"Expected price range: {lead.expected_price_range}")
    if lead.preferred_contact_time:
        extras.append(f"Preferred contact time: {lead.preferred_contact_time}")

    message_lines = [
        "You have a new landing-page lead from Propertism:",
        "",
        f"Name: {lead.name or 'Not provided'}",
        f"Phone: {lead.phone}",
        f"Email: {lead.email or 'Not provided'}",
        f"Property city: {lead.property_city}",
        f"Property type: {lead.get_property_type_display() if lead.property_type else 'Not provided'}",
        f"Intent type: {lead.intent_type}",
        f"Geo origin: {lead.geo_origin or 'Domestic / not provided'}",
        f"Lead stage: {lead.lead_stage}",
        f"Lead score: {lead.lead_score}",
        f"Lead category: {lead.lead_category}",
    ]

    if extras:
        message_lines.extend(["", "Qualification:"])
        message_lines.extend(extras)

    message_lines.extend(
        [
            "",
            f"Submitted: {lead.created_at.strftime('%B %d, %Y at %I:%M %p')}",
            f"Admin View: https://propertism.in/admin/content/landinglead/{lead.id}/change/",
        ]
    )

    try:
        send_mail(
            subject=f"New Landing Lead: {lead.property_city} / {lead.intent_type}",
            message="\n".join(message_lines),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ADMIN_EMAILS,
            fail_silently=False,
        )
    except Exception as exc:
        logger.error("Landing lead email notification failed: %s", exc)

    whatsapp_lines = [
        "Landing Lead",
        f"Phone: {lead.phone}",
        f"City: {lead.property_city}",
        f"Intent: {lead.intent_type}",
    ]
    if lead.geo_origin:
        whatsapp_lines.append(f"Geo: {lead.geo_origin}")
    if extras:
        whatsapp_lines.extend(extras[:2])
    send_whatsapp_notification("\n".join(whatsapp_lines))


@require_POST
def landing_lead_api(request):
    """Store leads submitted from landing pages."""
    phone = (request.POST.get("phone") or "").strip()
    property_city = (request.POST.get("property_city") or "").strip()
    intent_type = (request.POST.get("intent_type") or "").strip()
    geo_origin = (request.POST.get("geo_origin") or "").strip()
    name = (request.POST.get("name") or "").strip()
    email = (request.POST.get("email") or "").strip()
    property_type = (request.POST.get("property_type") or "").strip()
    selling_timeline = (request.POST.get("selling_timeline") or "").strip()
    occupancy_status = (request.POST.get("occupancy_status") or "").strip()
    expected_rent = (request.POST.get("expected_rent") or "").strip()

    valid_intent_types = {choice[0] for choice in LandingLead.INTENT_TYPE_CHOICES}
    valid_property_types = {choice[0] for choice in LandingLead.PROPERTY_CHOICES}

    errors = {}
    if not phone:
        errors["phone"] = "Phone number is required."
    if not property_city:
        errors["property_city"] = "Property city is required."
    if intent_type not in valid_intent_types:
        errors["intent_type"] = "Intent type is invalid."
    if property_type and property_type not in valid_property_types:
        errors["property_type"] = "Property type is invalid."
    if intent_type == "sell" and not property_type:
        errors["property_type"] = "Property type is required."
    if intent_type == "sell" and not selling_timeline:
        errors["selling_timeline"] = "Selling timeline is required."
    if intent_type == "management" and not occupancy_status:
        errors["occupancy_status"] = "Please tell us whether the property is occupied or vacant."

    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=400)

    qualification_data = {}
    if selling_timeline:
        qualification_data["selling_timeline"] = selling_timeline
    if occupancy_status:
        qualification_data["occupancy_status"] = occupancy_status
    if expected_rent:
        qualification_data["expected_rent"] = expected_rent

    lead_stage = "qualified" if qualification_data else "initiated"

    lead = LandingLead.objects.create(
        name=name,
        phone=phone,
        email=email,
        property_city=property_city,
        property_type=property_type,
        intent_type=intent_type,
        geo_origin=geo_origin,
        lead_stage=lead_stage,
        qualification_data=qualification_data,
    )

    try:
        send_landing_lead_notification(lead)
    except Exception as exc:
        logger.error("Failed to send landing lead notification: %s", exc)

    return JsonResponse(
        {
            "ok": True,
            "message": "Thanks. We received your request and will get back to you shortly.",
            "lead_id": lead.id,
            "lead_stage": lead.lead_stage,
            "lead_score": lead.lead_score,
            "lead_category": lead.lead_category,
        },
        status=201,
    )


@require_POST
def landing_lead_followup_api(request):
    """Store optional post-submit lead details."""
    lead_id = (request.POST.get("lead_id") or "").strip()
    expected_price_range = (request.POST.get("expected_price_range") or "").strip()
    preferred_contact_time = (request.POST.get("preferred_contact_time") or "").strip()

    if not lead_id:
        return JsonResponse({"ok": False, "errors": {"lead_id": "Lead id is required."}}, status=400)

    try:
        lead = LandingLead.objects.get(pk=lead_id)
    except LandingLead.DoesNotExist:
        return JsonResponse({"ok": False, "errors": {"lead_id": "Lead not found."}}, status=404)

    if expected_price_range:
        lead.expected_price_range = expected_price_range
    if preferred_contact_time:
        lead.preferred_contact_time = preferred_contact_time
    lead.save()

    return JsonResponse(
        {
            "ok": True,
            "message": "Thanks. We saved your preferences.",
            "lead_id": lead.id,
            "lead_score": lead.lead_score,
            "lead_category": lead.lead_category,
        },
        status=200,
    )


def send_whatsapp_notification(text):
    """
    Sends a WhatsApp message via the Meta official Cloud API.
    Required ENV vars: WHATSAPP_PHONE_ID, WHATSAPP_ACCESS_TOKEN, WHATSAPP_ADMIN_PHONE
    """
    import requests
    
    phone_id = getattr(settings, 'WHATSAPP_PHONE_ID', None)
    token = getattr(settings, 'WHATSAPP_ACCESS_TOKEN', None)
    admin_phone = getattr(settings, 'WHATSAPP_ADMIN_PHONE', None)

    if not all([phone_id, token, admin_phone]):
        logger.info(f"NOTIFICATION TRIGGERED: [WhatsApp] -> {text} (API not configured)")
        return

    url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": admin_phone,
        "type": "text",
        "text": {"body": text}
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            logger.info("WhatsApp notification sent successfully.")
        else:
            logger.error(f"WhatsApp API Error {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Failed to send WhatsApp notification: {e}")


def newsletter_subscribe(request):
    """Newsletter subscription handler with Admin notification."""
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            try:
                sub, created = Newsletter.objects.get_or_create(email=email)
                if created:
                    messages.success(request, "Thank you for subscribing to our newsletter!")
                    # Notify admin via email
                    try:
                        send_mail(
                            subject="📩 New Newsletter Subscriber",
                            message=f"User {email} has subscribed to the newsletter.",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[settings.ADMIN_EMAIL],
                            fail_silently=False,
                        )
                    except Exception: pass
                    # Notify admin via WhatsApp
                    send_whatsapp_notification(f"📩 *Newsletter*: {email} has subscribed.")
                else:
                    messages.info(request, "You are already subscribed. Thank you!")
            except Exception:
                messages.error(request, "There was an error. Please try again.")
        else:
            messages.error(request, "Please provide a valid email address.")

    return redirect(request.META.get("HTTP_REFERER") or get_home_section_links()["blog"])


def custom_404(request, exception=None):
    """Custom 404 error handler."""
    return render(request, "404.html", status=404)


def custom_500(request):
    """Custom 500 error handler."""
    return render(request, "500.html", status=500)
