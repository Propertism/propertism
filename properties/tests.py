import json
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from content.templatetags.seo_tags import property_schema

from .models import Property, PropertyType
from .serializers import PropertySerializer


class PropertyCurrencyFormattingTests(TestCase):
    def setUp(self):
        self.property_type = PropertyType.objects.create(name="Apartment", slug="apartment")

    def test_inr_price_uses_indian_grouping_and_words(self):
        property_obj = Property.objects.create(
            title="Anna Nagar Apartment",
            description="Premium apartment",
            price=Decimal("1500000.00"),
            currency="INR",
            location="Chennai",
            property_type=self.property_type,
        )

        self.assertEqual(property_obj.formatted_price_value, "15,00,000.00")
        self.assertEqual(property_obj.formatted_price, "₹15,00,000.00")
        self.assertEqual(property_obj.price_in_words, "Fifteen Lakh")
        self.assertEqual(property_obj.price_in_words_with_currency, "Fifteen Lakh Indian Rupees")

    def test_usd_price_uses_international_grouping_and_words(self):
        property_obj = Property.objects.create(
            title="Hackensack Rental",
            description="Managed rental",
            price=Decimal("1000000.00"),
            currency="USD",
            location="Hackensack",
            property_type=self.property_type,
        )

        self.assertEqual(property_obj.formatted_price_value, "1,000,000.00")
        self.assertEqual(property_obj.formatted_price, "$1,000,000.00")
        self.assertEqual(property_obj.price_in_words, "One Million")
        self.assertEqual(property_obj.price_in_words_with_currency, "One Million US Dollars")

    def test_serializer_exposes_currency_aware_price_fields(self):
        property_obj = Property.objects.create(
            title="Dollar Listing",
            description="USD listing",
            price=Decimal("250000.00"),
            currency="USD",
            location="Dallas",
            property_type=self.property_type,
        )

        serializer = PropertySerializer(property_obj)

        self.assertEqual(serializer.data["currency"], "USD")
        self.assertEqual(serializer.data["currency_symbol"], "$")
        self.assertEqual(serializer.data["formatted_price"], "$250,000.00")
        self.assertEqual(serializer.data["price_in_words_with_currency"], "Two Hundred Fifty Thousand US Dollars")

    def test_property_schema_uses_property_currency(self):
        property_obj = Property.objects.create(
            title="USD Villa",
            description="Villa",
            price=Decimal("1000000.00"),
            currency="USD",
            location="Dubai",
            property_type=self.property_type,
        )

        schema_context = property_schema(property_obj)
        schema = json.loads(schema_context["schema"])

        self.assertEqual(schema["offers"]["priceCurrency"], "USD")

    def test_property_detail_page_renders_currency_aware_price_copy(self):
        property_obj = Property.objects.create(
            title="Dallas Listing",
            description="Managed sale",
            price=Decimal("250000.00"),
            currency="USD",
            location="Dallas",
            property_type=self.property_type,
        )

        response = self.client.get(reverse("property_detail", args=[property_obj.pk]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "$250,000.00")
        self.assertContains(response, "Two Hundred Fifty Thousand US Dollars")
        self.assertContains(response, "Guide Price")
        self.assertContains(response, "Back to Properties")
        self.assertContains(response, "css/premium-styles.css")

    def test_homepage_featured_properties_render_formatted_price(self):
        property_obj = Property.objects.create(
            title="Anna Nagar Apartment",
            description="Premium apartment",
            price=Decimal("1500000.00"),
            currency="INR",
            location="Chennai",
            property_type=self.property_type,
        )

        response = self.client.get(reverse("home"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, property_obj.formatted_price)
        self.assertContains(response, property_obj.price_in_words_with_currency)
        self.assertContains(response, property_obj.title)

    def test_property_list_page_renders_available_properties(self):
        property_obj = Property.objects.create(
            title="ECR Villa",
            description="Sea-facing villa",
            price=Decimal("50000000.00"),
            currency="INR",
            location="ECR",
            property_type=self.property_type,
        )

        response = self.client.get(reverse("property_list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, property_obj.title)
        self.assertContains(response, property_obj.formatted_price)
        self.assertContains(response, property_obj.price_in_words_with_currency)
        self.assertContains(response, "Curated Properties")
        self.assertContains(response, "css/premium-styles.css")
