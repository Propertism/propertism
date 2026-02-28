from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from properties.models import Property, PropertyType
from properties.serializers import PropertySerializer

@api_view(['GET'])
def search_properties(request):
    """Search properties by location and price"""
    location = request.GET.get('location', '')
    price_max = request.GET.get('price_max')
    
    queryset = Property.objects.all()
    
    if location:
        queryset = queryset.filter(location__icontains=location)
    if price_max:
        queryset = queryset.filter(price__lte=price_max)
    
    serializer = PropertySerializer(queryset, many=True)
    return Response(serializer.data)

def search(request):
    """Web view for search"""
    query = request.GET.get('q', '')
    properties = Property.objects.all()
    
    if query:
        from django.db import models
        properties = properties.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(location__icontains=query)
        )
    
    property_types = PropertyType.objects.all()
    
    return render(request, 'search/results.html', {
        'properties': properties,
        'query': query,
        'property_types': property_types,
    })
