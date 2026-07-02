import calendar
import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth, ExtractYear, TruncDate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from content.site_context import get_company_info, get_home_section_links

from .models import Inquiry, InquiryReply, Property
from .serializers import PropertySerializer

logger = logging.getLogger(__name__)


def _parse_email_list(raw_value):
    emails = []
    invalid = []

    for item in (raw_value or "").replace(";", ",").split(","):
        email = item.strip()
        if not email:
            continue
        try:
            validate_email(email)
        except ValidationError:
            invalid.append(email)
            continue
        emails.append(email)

    return emails, invalid


@api_view(["GET"])
def property_list_api(request):
    """API endpoint for property list with pagination."""
    paginator = PageNumberPagination()
    paginator.page_size = 10

    queryset = Property.objects.all().order_by("-created_at")

    location = request.GET.get("location")
    price_max = request.GET.get("price_max")
    price_type = request.GET.get("price_type")

    if location:
        queryset = queryset.filter(location__icontains=location)
    if price_max:
        queryset = queryset.filter(price__lte=price_max)
    if price_type:
        queryset = queryset.filter(price_type=price_type)

    result_page = paginator.paginate_queryset(queryset, request)
    serializer = PropertySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def property_detail_api(request, pk):
    """API endpoint for property detail."""
    property_obj = get_object_or_404(Property, pk=pk)
    serializer = PropertySerializer(property_obj)
    return Response(serializer.data)


def property_list(request):
    queryset = Property.objects.filter(status="available").prefetch_related("photos").order_by("-created_at")
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    company = get_company_info()
    return render(
        request,
        "properties/list.html",
        {
            "properties": page_obj,
            "company": company,
        },
    )


def property_detail_by_pk(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return redirect('property_detail', slug=property_obj.slug, permanent=True)


def property_detail(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)
    company = get_company_info()
    from realtor_project.features import is_feature_enabled
    return render(
        request,
        "properties/detail.html",
        {
            "property": property_obj,
            "company": company,
            "captcha_test_mode": is_feature_enabled("CAPTCHA_TEST_MODE", default=False),
        },
    )


def create_inquiry(request):
    if request.method != "POST":
        return redirect(get_home_section_links()["properties"])

    property_id = request.POST.get("property_id")
    property_obj = get_object_or_404(Property, pk=property_id)
    form_source = request.POST.get("form_source", "Unknown Form")
    
    from properties.utils.lead_validation import LeadValidator
    from content.views import send_rfq_notification
    from realtor_project.features import is_feature_enabled
    
    validator = LeadValidator(request, request.POST)
    assessment = validator.validate()
    
    # Check CAPTCHA
    captcha_answer = request.POST.get('captcha_answer')
    expected_answer = request.session.get('captcha_expected_answer')
    
    captcha_enabled = is_feature_enabled('CAPTCHA_ENABLE', default=True)
    
    if captcha_enabled and assessment['confidence_score'] < validator.config.get('CAPTCHA_THRESHOLD', 70):
        if not (expected_answer and captcha_answer and str(captcha_answer) == str(expected_answer)):
            if captcha_answer:
                messages.error(request, "Incorrect security answer. Please try again.")
            # Generate new CAPTCHA challenge
            import random
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            request.session['captcha_question'] = f"{num1} + {num2}"
            request.session['captcha_expected_answer'] = str(num1 + num2)
            
            return render(request, "properties/detail.html", {
                "property": property_obj,
                "company": get_company_info(),
                "show_captcha": True,
                "captcha_test_mode": is_feature_enabled("CAPTCHA_TEST_MODE", default=False),
                "prefilled_name": request.POST.get("name", ""),
                "prefilled_email": request.POST.get("email", ""),
                "prefilled_phone": request.POST.get("phone", ""),
                "prefilled_message": request.POST.get("message", ""),
            })
        else:
            # CAPTCHA Passed!
            assessment['confidence_score'] = max(assessment['confidence_score'], 75)
            assessment['assessment_status'] = "Genuine (Verified by CAPTCHA)"
            request.session.pop('captcha_expected_answer', None)
            request.session.pop('captcha_question', None)

    try:
        # Capture UTM parameters, Referrer, and Landing page for attribution
        utm_source = request.POST.get("utm_source", "").strip()
        utm_medium = request.POST.get("utm_medium", "").strip()
        utm_campaign = request.POST.get("utm_campaign", "").strip()
        utm_term = request.POST.get("utm_term", "").strip()
        utm_content = request.POST.get("utm_content", "").strip()
        referrer = request.POST.get("referrer", "").strip()
        landing_page = request.POST.get("landing_page", "").strip()

        msg_body = request.POST.get("message", "").strip()
        attribution_lines = []
        if utm_source: attribution_lines.append(f"UTM Source: {utm_source}")
        if utm_medium: attribution_lines.append(f"UTM Medium: {utm_medium}")
        if utm_campaign: attribution_lines.append(f"UTM Campaign: {utm_campaign}")
        if utm_term: attribution_lines.append(f"UTM Term: {utm_term}")
        if utm_content: attribution_lines.append(f"UTM Content: {utm_content}")
        if referrer: attribution_lines.append(f"Referrer: {referrer}")
        if landing_page: attribution_lines.append(f"Landing Page: {landing_page}")

        if attribution_lines:
            msg_body += "\n\n--- Traffic Attribution Parameters ---\n" + "\n".join(attribution_lines)

        inquiry = Inquiry.objects.create(
            property=property_obj,
            name=request.POST.get("name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            message=msg_body,
            form_source=form_source,
            confidence_score=assessment['confidence_score'],
            assessment_status=assessment['assessment_status'],
            validation_summary=assessment['validation_summary']
        )
        
        # Send notifications (emails to both ids, and WhatsApp notification)
        try:
            send_rfq_notification(inquiry, form_source=form_source)
        except Exception as email_exc:
            logger.exception("Failed to send notification for property inquiry %s", inquiry.email)
            # Don't fail the request if email fails

        messages.success(request, "Thank you for your inquiry! We will get back to you soon.")
    except Exception as exc:
        logger.exception("Error processing property inquiry: %s", exc)
        messages.error(
            request,
            "There was an error submitting your inquiry. Please try again or call us directly.",
        )

    return redirect("property_detail", slug=property_obj.slug)


# ── SCCB-19052026-1 Inquiries Dashboard ──────────────────────────────────────

def _is_staff_user(user):
    return user.is_active and user.is_staff


def _safe_inquiries_next(request):
    next_url = request.POST.get("next") or request.GET.get("next") or reverse("inquiries_dashboard")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return next_url
    return reverse("inquiries_dashboard")


def inquiry_staff_login(request):
    next_url = _safe_inquiries_next(request)

    if request.user.is_authenticated and request.user.is_staff:
        return redirect(next_url)

    error = ""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user and user.is_active and user.is_staff:
            login(request, user)
            return redirect(next_url)
        error = "Use an active staff account to open Inquiries."

    return render(request, "inquiries/login.html", {
        "next": next_url,
        "error": error,
    })


inquiries_staff_required = user_passes_test(_is_staff_user, login_url="inquiries_login")


@inquiries_staff_required
def inquiries_dashboard(request):
    status_filter = request.GET.get("status", "")
    date_filter = request.GET.get("date", "")
    q = request.GET.get("q", "").strip()

    # Listing queryset — all three filters apply
    qs = Inquiry.objects.select_related("property").order_by("-created_at")
    if status_filter in ("pending", "contacted", "closed"):
        qs = qs.filter(status=status_filter)
    if date_filter:
        try:
            from datetime import date as date_cls
            d_obj = date_cls.fromisoformat(date_filter)
            qs = qs.filter(created_at__date=d_obj)
        except ValueError:
            date_filter = ""
    if q:
        qs = qs.filter(
            Q(name__icontains=q) | Q(email__icontains=q) | Q(property__title__icontains=q)
        )

    # Stats — unfiltered totals (site-wide counts)
    all_qs = Inquiry.objects.all()
    stats = {
        "total": all_qs.count(),
        "pending": all_qs.filter(status="pending").count(),
        "contacted": all_qs.filter(status="contacted").count(),
        "closed": all_qs.filter(status="closed").count(),
    }

    # Tree query — one query, grouped by year/month/day, status filter respected
    tree_base = Inquiry.objects.all()
    if status_filter in ("pending", "contacted", "closed"):
        tree_base = tree_base.filter(status=status_filter)

    tree_rows = (
        tree_base
        .annotate(
            _year=ExtractYear("created_at"),
            _month=ExtractMonth("created_at"),
            _day=TruncDate("created_at"),
        )
        .values("_year", "_month", "_day")
        .annotate(count=Count("id"))
        .order_by("-_year", "-_month", "-_day")
    )

    today = timezone.now().date()
    tree_data = []
    cur_year = cur_month = None

    for row in tree_rows:
        y, m, d = row["_year"], row["_month"], row["_day"]
        cnt = row["count"]
        d_str = d.isoformat() if d else ""

        if cur_year is None or cur_year["year"] != y:
            cur_year = {"year": y, "months": [], "count": 0, "open": y == today.year}
            tree_data.append(cur_year)
            cur_month = None

        if cur_month is None or cur_month["month"] != m:
            cur_month = {
                "month": m,
                "name": calendar.month_name[m],
                "dates": [],
                "count": 0,
                "open": y == today.year and m == today.month,
            }
            cur_year["months"].append(cur_month)

        cur_month["dates"].append({
            "date_str": d_str,
            "display": (str(d.day) + " " + d.strftime("%b")) if d else "",
            "count": cnt,
            "active": d_str == date_filter,
        })
        cur_month["count"] += cnt
        cur_year["count"] += cnt

    return render(request, "inquiries/dashboard.html", {
        "inquiries": qs,
        "stats": stats,
        "active_filter": status_filter,
        "date_filter": date_filter,
        "q": q,
        "tree_data": tree_data,
        "today": today,
        "board_columns": [("pending", "Pending"), ("contacted", "Contacted"), ("closed", "Closed")],
    })


@inquiries_staff_required
@require_POST
def inquiry_status_update(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, pk=inquiry_id)
    try:
        data = json.loads(request.body)
        new_status = data.get("status")
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Invalid request"}, status=400)

    valid = [c[0] for c in Inquiry.STATUS_CHOICES]
    if new_status not in valid:
        return JsonResponse({"error": "Invalid status"}, status=400)

    inquiry.status = new_status
    inquiry.save(update_fields=["status", "updated_at"])
    return JsonResponse({"status": inquiry.status, "updated_at": inquiry.updated_at.isoformat()})


@inquiries_staff_required
@require_POST
def inquiry_delete(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, pk=inquiry_id)
    inquiry.delete()
    return JsonResponse({"ok": True})


@inquiries_staff_required
def inquiry_replies(request, inquiry_id):
    """Return all sent replies for a given inquiry as JSON."""
    inquiry = get_object_or_404(Inquiry, pk=inquiry_id)
    replies = (
        InquiryReply.objects
        .filter(inquiry=inquiry)
        .order_by("sent_at")
        .values("id", "to_email", "cc", "subject", "body", "sent_at", "sent_by__username")
    )
    data = [
        {
            "id": r["id"],
            "to_email": r["to_email"],
            "cc": r["cc"],
            "subject": r["subject"],
            "body": r["body"],
            "sent_at": r["sent_at"].strftime("%d %b %Y, %H:%M") if r["sent_at"] else "",
            "sent_by": r["sent_by__username"] or "system",
        }
        for r in replies
    ]
    return JsonResponse({"replies": data})


@inquiries_staff_required
@require_POST
def inquiry_send_reply(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Invalid request"}, status=400)

    inquiry_id = data.get("inquiry_id")
    to_email = (data.get("to") or "").strip()
    cc_raw = data.get("cc") or ""
    subject = (data.get("subject") or "").strip()
    body = (data.get("body") or "").strip()

    if not to_email or not subject or not body:
        return JsonResponse({"error": "Recipient, subject, and content are required."}, status=400)

    try:
        validate_email(to_email)
    except ValidationError:
        return JsonResponse({"error": "Enter a valid recipient email address."}, status=400)

    cc_list, invalid_cc = _parse_email_list(cc_raw)
    if invalid_cc:
        return JsonResponse(
            {"error": "Enter valid CC email addresses: " + ", ".join(invalid_cc)},
            status=400,
        )

    inquiry = None
    if inquiry_id:
        inquiry = get_object_or_404(Inquiry, pk=inquiry_id)
        if inquiry.email and inquiry.email.lower() != to_email.lower():
            return JsonResponse({"error": "Recipient does not match this inquiry."}, status=400)

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "") or getattr(settings, "ADMIN_EMAIL", "")
    if not from_email:
        logger.error("Inquiry reply email blocked because DEFAULT_FROM_EMAIL/ADMIN_EMAIL is not configured")
        return JsonResponse({"error": "Outbound email is not configured."}, status=500)

    reply_to = [getattr(settings, "ADMIN_EMAIL", from_email)] if getattr(settings, "ADMIN_EMAIL", "") else None

    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to_email],
            cc=cc_list,
            reply_to=reply_to,
        )
        email.send(fail_silently=False)
    except Exception:
        logger.exception("Inquiry reply email failed")
        return JsonResponse({"error": "Could not send email. Check SMTP configuration."}, status=500)

    # ── Persist the reply for audit trail ─────────────────────────────────────
    if inquiry:
        InquiryReply.objects.create(
            inquiry=inquiry,
            sent_by=request.user if request.user.is_authenticated else None,
            to_email=to_email,
            cc=", ".join(cc_list),
            subject=subject,
            body=body,
        )

    updated_at = None
    if inquiry and inquiry.status == "pending":
        inquiry.status = "contacted"
        inquiry.save(update_fields=["status", "updated_at"])
        updated_at = inquiry.updated_at.isoformat()

    return JsonResponse({
        "ok": True,
        "status": inquiry.status if inquiry else None,
        "updated_at": updated_at,
    })


@inquiries_staff_required
def inquiry_pending_count(request):
    count = Inquiry.objects.filter(status="pending").count()
    return JsonResponse({"count": count})
