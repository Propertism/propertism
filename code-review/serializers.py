from rest_framework import serializers

from .models import Inquiry, Property, PropertyType


class PropertySerializer(serializers.ModelSerializer):
    currency_symbol = serializers.ReadOnlyField()
    formatted_price = serializers.ReadOnlyField()
    price_in_words = serializers.ReadOnlyField()
    price_in_words_with_currency = serializers.ReadOnlyField()

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "description",
            "price",
            "currency",
            "currency_symbol",
            "formatted_price",
            "price_in_words",
            "price_in_words_with_currency",
            "price_type",
            "area",
            "bedrooms",
            "bathrooms",
            "location",
            "image",
            "property_type",
            "status",
            "created_at",
            "updated_at",
        ]


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = "__all__"


class InquirySerializer(serializers.ModelSerializer):
    property_title = serializers.SerializerMethodField()
    property_location = serializers.SerializerMethodField()

    class Meta:
        model = Inquiry
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "message",
            "status",
            "property",
            "property_title",
            "property_location",
            "created_at",
            "updated_at",
        ]

    def get_property_title(self, obj):
        return obj.property.title if obj.property else None

    def get_property_location(self, obj):
        return obj.property.location if obj.property else None
