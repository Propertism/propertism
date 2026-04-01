import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.db.utils import OperationalError, ProgrammingError
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render

from properties.models import Property
from properties.models import Inquiry as PropertyInquiry

from .models import (
    BlogPost,
    CoreValue,
    CustomerReviewSection,
    ExpertiseArea,
    HomepageCard,
    HomepageCardSection,
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
            hero_background_urls = [
                item.image.url
                for item in company.get_active_hero_backgrounds()
                if item.image
            ]
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
            customer_reviews[index:index + 3]
            for index in range(0, len(customer_reviews), 3)
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

    if not hero_background_urls and company.hero_image:
        hero_background_urls = [company.hero_image.url]

    context.update(
        {
            "stats": _safe_list(
                lambda: Statistic.objects.filter(is_active=True)[:4],
                warning="Homepage statistics table is unavailable.",
            ),
            "service_highlights": all_services[:4],
            "credibility_points": get_active_core_values(limit=4),
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


def send_rfq_notification(inquiry):
    """Send email notification when RFQ is submitted."""
    subject = f"New Quote Request from {inquiry.name}"
    
    # Build email body
    message_lines = [
        f"New Quote Request received:",
        f"",
        f"Name: {inquiry.name}",
        f"Email: {inquiry.email}",
        f"Phone: {inquiry.phone or 'Not provided'}",
        f"",
        f"Message:",
        f"{inquiry.message}",
        f"",
        f"Submitted: {inquiry.created_at.strftime('%B %d, %Y at %I:%M %p')}",
        f"",
        f"View in admin: https://propertism.in/admin/properties/inquiry/{inquiry.id}/change/",
    ]
    
    message = "\n".join(message_lines)
    
    # Send email
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )


def newsletter_subscribe(request):
    """Newsletter subscription handler."""
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            try:
                Newsletter.objects.get_or_create(email=email)
                messages.success(request, "Thank you for subscribing to our newsletter!")
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
