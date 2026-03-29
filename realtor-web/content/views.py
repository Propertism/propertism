import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.db.utils import OperationalError, ProgrammingError
from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render

from properties.models import Property
from properties.models import Inquiry as PropertyInquiry

from .models import (
    BlogPost,
    ContactInquiry,
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
    get_hero_title_segments,
    get_home_section_links,
)

logger = logging.getLogger(__name__)


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

        customer_review_section = CustomerReviewSection.objects.filter(is_active=True).first()
        if customer_review_section:
            customer_reviews = list(customer_review_section.reviews.filter(is_active=True))
            customer_review_slides = [
                customer_reviews[index:index + 3]
                for index in range(0, len(customer_reviews), 3)
            ]
        custom_card_sections = HomepageCardSection.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "cards",
                queryset=HomepageCard.objects.filter(is_active=True),
                to_attr="active_cards",
            )
        )
    except (OperationalError, ProgrammingError):
        # Local dev can hit this before migrations are applied. The rest of the
        # homepage should still render while the new tables are missing.
        customer_review_section = None
        customer_reviews = []
        customer_review_slides = []
        custom_card_sections = []
        hero_background_urls = []

    if not hero_background_urls and company.hero_image:
        hero_background_urls = [company.hero_image.url]

    context.update(
        {
            "stats": Statistic.objects.filter(is_active=True)[:4],
            "service_highlights": all_services[:4],
            "credibility_points": get_active_core_values(limit=4),
            "expertise_highlights": expertise_areas,
            "featured_properties": Property.objects.filter(status="available")[:6],
            "team_highlights": TeamMember.objects.filter(is_active=True)[:3],
            "recent_posts": BlogPost.objects.filter(is_published=True)[:3],
            "customer_review_section": customer_review_section,
            "customer_reviews": customer_reviews,
            "customer_review_slides": customer_review_slides,
            "custom_card_sections": custom_card_sections,
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
        "services": Service.objects.filter(is_active=True),
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
        "stats": Statistic.objects.filter(is_active=True),
        "values": CoreValue.objects.filter(is_active=True),
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
        "team_members": TeamMember.objects.filter(is_active=True),
        "expertise_areas": ExpertiseArea.objects.filter(is_active=True),
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Management", "url": None}
        ],
    })
    return render(request, "management.html", context)


def team_member_detail(request, slug):
    """Team member profile detail page."""
    from django.shortcuts import get_object_or_404
    team_member = get_object_or_404(TeamMember, slug=slug, is_active=True)
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
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    context.update(
        {
            "post": post,
            "recent_posts": BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3],
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
