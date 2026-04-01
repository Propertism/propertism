from rest_framework import serializers
from .models import Property, PropertyType

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'price', 'price_type', 'area', 
                  'bedrooms', 'bathrooms', 'location', 'image', 'property_type', 
                  'status', 'created_at', 'updated_at']

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'
