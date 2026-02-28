from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Property, PropertyType
from .serializers import PropertySerializer

def react_properties_app(request):
    """View to render React SPA embedded in CMS"""
    return render(request, 'properties/cms_app.html')

@api_view(['GET'])
def property_list_api(request):
    """API endpoint for property list with pagination"""
    paginator = PageNumberPagination()
    paginator.page_size = 10
    
    queryset = Property.objects.all().order_by('-created_at')
    
    # Filters
    location = request.GET.get('location')
    price_max = request.GET.get('price_max')
    price_type = request.GET.get('price_type')
    
    if location:
        queryset = queryset.filter(location__icontains=location)
    if price_max:
        queryset = queryset.filter(price__lte=price_max)
    if price_type:
        queryset = queryset.filter(price_type=price_type)
    
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = PropertySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def property_detail_api(request, pk):
    """API endpoint for property detail"""
    property_obj = get_object_or_404(Property, pk=pk)
    serializer = PropertySerializer(property_obj)
    return Response(serializer.data)

def property_list(request):
    properties = Property.objects.all()
    property_types = PropertyType.objects.all()
    
    # Filter by type
    property_type_id = request.GET.get('type')
    if property_type_id:
        properties = properties.filter(property_type_id=property_type_id)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    # Filter by location
    location = request.GET.get('location')
    if location:
        properties = properties.filter(location__icontains=location)
    
    # Filter by bedrooms
    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(properties, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'properties/list.html', {
        'properties': page_obj,
        'property_types': property_types,
    })

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/detail.html', {
        'property': property_obj,
    })
