from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from content.site_context import get_company_info, get_home_section_links

from .models import Property
from .serializers import PropertySerializer


def react_properties_app(request):
    """View to render React SPA embedded in CMS."""
    return render(request, "properties/cms_app.html")


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
    """Legacy list route now points to the homepage properties section."""
    return redirect(get_home_section_links()["properties"])


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
