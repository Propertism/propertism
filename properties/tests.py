import json
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from content.templatetags.seo_tags import property_schema

from properties.models import Inquiry, Property, PropertyPhoto, PropertyType
from properties.serializers import PropertySerializer


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

        self.assertEqual(property_obj.formatted_price_value, "15,00,000")
        self.assertEqual(property_obj.formatted_price, "₹15,00,000")
        self.assertEqual(property_obj.price_in_words, "Fifteen Lakhs")
        self.assertEqual(property_obj.price_in_words_with_currency, "Fifteen Lakhs Indian Rupees")

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
        self.assertContains(response, "Back to Asset Portfolio")

    @override_settings(CLARITY_PROJECT_ID="test_clarity_id_123")
    def test_clarity_script_rendered_when_configured(self):
        property_obj = Property.objects.create(
            title="Clarity Test Property",
            description="Clarity verification",
            price=Decimal("150000.00"),
            currency="INR",
            location="Chennai",
            property_type=self.property_type,
        )
        response = self.client.get(reverse("property_detail", args=[property_obj.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_clarity_id_123")
        self.assertContains(response, "https://www.clarity.ms/tag/")

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

    def test_display_image_url_returns_photo_url_when_storage_check_fails(self):
        property_obj = Property.objects.create(
            title="Photo Listing",
            description="Has uploaded photo",
            price=Decimal("1500000.00"),
            currency="INR",
            location="Chennai",
            property_type=self.property_type,
        )
        photo = PropertyPhoto.objects.create(
            property=property_obj,
            image=SimpleUploadedFile("photo.jpg", b"filecontent", content_type="image/jpeg"),
            is_primary=True,
            sort_order=1,
        )

        with patch.object(photo.image.storage, "exists", return_value=False):
            self.assertEqual(property_obj.get_display_image_url(), photo.image.url)

    def test_display_image_url_normalizes_relative_property_image_path(self):
        property_obj = Property.objects.create(
            title="Relative Image Listing",
            description="Has relative image path",
            price=Decimal("1500000.00"),
            currency="INR",
            location="Chennai",
            property_type=self.property_type,
            image="properties/example.jpg",
        )

        self.assertEqual(property_obj.get_display_image_url(), "/media/properties/example.jpg")


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="team@propertism.in",
    ADMIN_EMAIL="info@propertism.in",
)
class InquiryReplyTests(TestCase):
    def setUp(self):
        self.staff_user = get_user_model().objects.create_user(
            username="inquiries-staff",
            password="testpass123",
            is_staff=True,
        )
        self.client.force_login(self.staff_user)
        self.inquiry = Inquiry.objects.create(
            name="Arun Kumar",
            email="lead@example.com",
            phone="9876543210",
            message="Please share more details.",
            status="pending",
        )

    def post_reply(self, payload):
        return self.client.post(
            reverse("inquiry_send_reply"),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_send_reply_sends_email_and_marks_inquiry_contacted(self):
        response = self.post_reply(
            {
                "inquiry_id": self.inquiry.pk,
                "to": self.inquiry.email,
                "cc": "ops@example.com, sales@example.com",
                "subject": "Re: Your inquiry",
                "body": "Happy to help with the next steps.",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.inquiry.refresh_from_db()
        self.assertEqual(self.inquiry.status, "contacted")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.inquiry.email])
        self.assertEqual(mail.outbox[0].cc, ["ops@example.com", "sales@example.com"])
        self.assertEqual(mail.outbox[0].reply_to, ["info@propertism.in"])

    def test_send_reply_rejects_invalid_cc_addresses(self):
        response = self.post_reply(
            {
                "inquiry_id": self.inquiry.pk,
                "to": self.inquiry.email,
                "cc": "ops@example.com, invalid-address",
                "subject": "Re: Your inquiry",
                "body": "Happy to help with the next steps.",
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Enter valid CC email addresses: invalid-address"},
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_send_reply_rejects_mismatched_recipient(self):
        response = self.post_reply(
            {
                "inquiry_id": self.inquiry.pk,
                "to": "someoneelse@example.com",
                "subject": "Re: Your inquiry",
                "body": "Happy to help with the next steps.",
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Recipient does not match this inquiry."},
        )
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(DEFAULT_FROM_EMAIL="", ADMIN_EMAIL="")
    def test_send_reply_requires_configured_sender(self):
        response = self.post_reply(
            {
                "inquiry_id": self.inquiry.pk,
                "to": self.inquiry.email,
                "subject": "Re: Your inquiry",
                "body": "Happy to help with the next steps.",
            }
        )

        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(
            response.content,
            {"error": "Outbound email is not configured."},
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_inquiry_replies_returns_sent_replies_json(self):
        from properties.models import InquiryReply
        InquiryReply.objects.create(
            inquiry=self.inquiry,
            sent_by=self.staff_user,
            to_email=self.inquiry.email,
            cc="ops@example.com",
            subject="Re: Your inquiry",
            body="Hello body text."
        )

        response = self.client.get(
            reverse("inquiry_replies", args=[self.inquiry.pk])
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("replies", data)
        self.assertEqual(len(data["replies"]), 1)
        self.assertEqual(data["replies"][0]["to_email"], self.inquiry.email)
        self.assertEqual(data["replies"][0]["cc"], "ops@example.com")
        self.assertEqual(data["replies"][0]["subject"], "Re: Your inquiry")
        self.assertEqual(data["replies"][0]["body"], "Hello body text.")
        self.assertEqual(data["replies"][0]["sent_by"], self.staff_user.username)

    def test_inquiry_replies_requires_staff(self):
        self.client.logout()
        response = self.client.get(
            reverse("inquiry_replies", args=[self.inquiry.pk])
        )
        self.assertEqual(response.status_code, 302)


class InquiryNotificationTests(TestCase):
    def setUp(self):
        self.property_type = PropertyType.objects.create(name="Villa", slug="villa")
        self.property_obj = Property.objects.create(
            title="Premium Beach Villa",
            description="Gorgeous villa on ECR",
            price=Decimal("45000000.00"),
            currency="INR",
            property_type=self.property_type,
            status="available",
        )

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
        EXTRA_NOTIFICATION_EMAIL="propertism.tamil@gmail.com",
    )
    @patch("content.views.send_whatsapp_notification")
    def test_create_inquiry_sends_email_and_whatsapp(self, mock_send_whatsapp):
        # Initial inquiry count
        self.assertEqual(Inquiry.objects.count(), 0)

        # Clear mail outbox
        mail.outbox = []

        # Make client POST to create_inquiry
        response = self.client.post(
            reverse("create_inquiry"),
            data={
                "property_id": self.property_obj.id,
                "name": "Viji Buyer",
                "email": "buyer@example.com",
                "phone": "+919876543210",
                "message": "Is this ECR villa open for visits?",
            },
        )

        # Inquiry should be created
        self.assertEqual(Inquiry.objects.count(), 1)
        inquiry = Inquiry.objects.first()
        self.assertEqual(inquiry.name, "Viji Buyer")
        self.assertEqual(inquiry.property, self.property_obj)

        # Response should redirect to property detail page
        self.assertRedirects(response, reverse("property_detail", kwargs={"slug": self.property_obj.slug}))

        # Email should be sent to both ADMIN_EMAIL and EXTRA_NOTIFICATION_EMAIL
        expected_recipients = set(["info@propertism.in", "propertism.tamil@gmail.com"])
        
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertEqual(set(sent_email.to), expected_recipients)
        self.assertIn("Viji Buyer", sent_email.subject)
        self.assertIn("Premium Beach Villa", sent_email.body)
        self.assertIn("ECR villa open for visits?", sent_email.body)

        # WhatsApp mock should be called with correct details
        mock_send_whatsapp.assert_called_once()
        whatsapp_call_args = mock_send_whatsapp.call_args[0][0]
        self.assertIn("Viji Buyer", whatsapp_call_args)
        self.assertIn("Premium Beach Villa", whatsapp_call_args)
        self.assertIn("+919876543210", whatsapp_call_args)

