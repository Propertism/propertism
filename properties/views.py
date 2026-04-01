from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from content.site_context import get_company_info, get_home_section_links

from .models import Inquiry, Property
from .serializers import PropertySerializer


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


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    company = get_company_info()
    return render(
        request,
        "properties/detail.html",
        {
            "property": property_obj,
            "company": company,
        },
    )


def create_inquiry(request):
    if request.method != "POST":
        return redirect(get_home_section_links()["properties"])

    property_id = request.POST.get("property_id")
    property_obj = get_object_or_404(Property, pk=property_id)

    try:
        Inquiry.objects.create(
            property=property_obj,
            name=request.POST.get("name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            message=request.POST.get("message", "").strip(),
        )
        messages.success(request, "Thank you for your inquiry! We will get back to you soon.")
    except Exception:
        messages.error(
            request,
            "There was an error submitting your inquiry. Please try again or call us directly.",
        )

    return redirect("property_detail", pk=property_obj.pk)
