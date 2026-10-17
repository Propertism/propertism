"""
SCCB-09 regression tests for API access control, CAPTCHA fail-closed
behaviour, and the legacy chat ContactMessage endpoint.

Validator field names (from templates + content/security/validators.py):
  - g-recaptcha-response
  - website_url_check
  - form_render_time
"""

import json
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from properties.models import ContactMessage, Inquiry, Property, PropertyType
from content.security.google_recaptcha import GoogleRecaptchaV2, RecaptchaResult
from content.security.spam_protection import SpamProtectionService
from content.security.validators import _get_ip, validate_rate_limit


User = get_user_model()


def _property():
    ptype = PropertyType.objects.create(name="Apartment", slug="apartment-sec")
    return Property.objects.create(
        title="Test Property",
        description="Test",
        price=Decimal("1000000"),
        currency="INR",
        location="Chennai",
        property_type=ptype,
        status="available",
    )


class InquiryAPIAuthenticationTests(APITestCase):
    """IsAdminUser allows any is_staff user, not only superusers."""

    def setUp(self):
        self.property = _property()
        self.inquiry = Inquiry.objects.create(
            property=self.property,
            name="John Doe",
            email="john@example.com",
            phone="+1234567890",
            message="Interested in property",
            form_source="Test",
        )
        self.superuser = User.objects.create_superuser(
            username="superuser",
            email="super@example.com",
            password="testpass123",
        )
        self.staff_user = User.objects.create_user(
            username="staffuser",
            email="staff@example.com",
            password="testpass123",
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="regularuser",
            email="user@example.com",
            password="testpass123",
            is_staff=False,
        )
        self.client = APIClient()
        self.url = reverse("inquiry_list_api")

    def test_unauthenticated_access_returns_401(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_access_returns_403(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_access_succeeds(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("items", response.data)
        self.assertGreater(response.data["total"], 0)

    def test_superuser_access_succeeds(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_session_authenticated_staff_succeeds(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method_not_allowed(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(self.url, {"name": "Test"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @override_settings(DEAL_ENGINE_INQUIRIES_KEY="test-deal-engine-key-value")
    def test_post_with_service_key_still_not_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION="DealEngine test-deal-engine-key-value")
        response = self.client.post(self.url, {"name": "Test"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_excludes_manage_inquiries(self):
        manage_inquiry = Inquiry.objects.create(
            property=self.property,
            name="Manager",
            email="manager@example.com",
            phone="+1234567890",
            message="Manage request",
            service_needed="manage",
            form_source="Test",
        )
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.url)
        inquiry_ids = [item["id"] for item in response.data["items"]]
        self.assertNotIn(manage_inquiry.id, inquiry_ids)

    def test_response_includes_pii_fields_for_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.url)
        first_item = response.data["items"][0]
        for field in ("id", "name", "email", "phone", "message"):
            self.assertIn(field, first_item)

    @override_settings(DEAL_ENGINE_INQUIRIES_KEY="test-deal-engine-key-value")
    def test_valid_service_key_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION="DealEngine test-deal-engine-key-value")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("items", response.data)

    @override_settings(DEAL_ENGINE_INQUIRIES_KEY="test-deal-engine-key-value")
    def test_invalid_service_key_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION="DealEngine wrong-key")
        response = self.client.get(self.url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    @override_settings(DEAL_ENGINE_INQUIRIES_KEY="test-deal-engine-key-value")
    def test_malformed_service_key_scheme_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer test-deal-engine-key-value")
        response = self.client.get(self.url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    @override_settings(DEAL_ENGINE_INQUIRIES_KEY="test-deal-engine-key-value")
    def test_missing_authorization_denied_when_key_configured(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(DEAL_ENGINE_INQUIRIES_KEY="")
    def test_empty_configured_key_does_not_open_anonymous_access(self):
        self.client.credentials(HTTP_AUTHORIZATION="DealEngine anything")
        response = self.client.get(self.url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    @override_settings(
        DEAL_ENGINE_INQUIRIES_KEY="active-key-value",
        DEAL_ENGINE_INQUIRIES_KEY_PREVIOUS="previous-key-value",
    )
    def test_previous_key_accepted_during_rotation(self):
        self.client.credentials(HTTP_AUTHORIZATION="DealEngine previous-key-value")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(
        DEAL_ENGINE_INQUIRIES_KEY="active-key-value",
        DEAL_ENGINE_INQUIRIES_KEY_PREVIOUS="",
    )
    def test_previous_key_rejected_when_not_configured(self):
        self.client.credentials(HTTP_AUTHORIZATION="DealEngine leftover-old-key")
        response = self.client.get(self.url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_service_key_not_leaked_in_error_body(self):
        self.client.credentials(HTTP_AUTHORIZATION="DealEngine secret-should-not-echo")
        response = self.client.get(self.url)
        body = str(response.data) if response.data is not None else ""
        self.assertNotIn("secret-should-not-echo", body)


class CAPTCHAFailClosedTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        self.property = _property()
        self.form_data = {
            "property_id": self.property.id,
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+1234567890",
            "message": "Interested in this property",
            "form_source": "Property Detail Page",
            "g-recaptcha-response": "fake-token",
            "website_url_check": "",
            "form_render_time": "1",
        }

    @override_settings(RECAPTCHA_SECRET_KEY="")
    def test_missing_secret_key_fails_verification(self):
        result = GoogleRecaptchaV2().verify(token="fake-token", remote_ip="127.0.0.1")
        self.assertFalse(result.success)
        self.assertIn("secret-key-missing", result.error_codes)

    @override_settings(RECAPTCHA_FAIL_OPEN=False, RECAPTCHA_SECRET_KEY="dummy")
    @patch("realtor_project.features.is_feature_enabled")
    @patch("content.security.google_recaptcha.GoogleRecaptchaV2.verify")
    def test_network_error_rejects_when_fail_closed(self, mock_verify, mock_flags):
        mock_flags.side_effect = lambda flag, default=False: True if flag == "CAPTCHA_ENABLE" else default
        mock_verify.return_value = RecaptchaResult(success=False, error_codes=["network-error"])
        self.client.post(reverse("create_inquiry"), self.form_data)
        self.assertEqual(Inquiry.objects.filter(email="test@example.com").count(), 0)

    @override_settings(RECAPTCHA_SECRET_KEY="dummy")
    @patch("realtor_project.features.is_feature_enabled")
    @patch("content.security.google_recaptcha.GoogleRecaptchaV2.verify")
    def test_invalid_token_rejects_submission(self, mock_verify, mock_flags):
        mock_flags.side_effect = lambda flag, default=False: True if flag == "CAPTCHA_ENABLE" else default
        mock_verify.return_value = RecaptchaResult(success=False, error_codes=["invalid-input-response"])
        self.client.post(reverse("create_inquiry"), self.form_data)
        self.assertEqual(Inquiry.objects.filter(email="test@example.com").count(), 0)

    @override_settings(DEBUG=False, TESTING=False)
    @patch("realtor_project.features.is_feature_enabled")
    def test_production_cannot_disable_captcha_via_flag(self, mock_flags):
        mock_flags.side_effect = lambda flag, default=False: False if flag == "CAPTCHA_ENABLE" else default
        factory = RequestFactory()
        request = factory.post("/inquiry/", self.form_data)
        result = SpamProtectionService(request).validate("Property Detail Page")
        self.assertFalse(result.passed)
        self.assertEqual(result.failure_reason, "captcha-disabled-in-production")

    @override_settings(RECAPTCHA_SECRET_KEY="dummy")
    @patch("realtor_project.features.is_feature_enabled")
    @patch("content.security.google_recaptcha.GoogleRecaptchaV2.verify")
    def test_legitimate_inquiry_succeeds(self, mock_verify, mock_flags):
        mock_flags.side_effect = lambda flag, default=False: True if flag == "CAPTCHA_ENABLE" else default
        mock_verify.return_value = RecaptchaResult(success=True, hostname="localhost")
        response = self.client.post(reverse("create_inquiry"), self.form_data)
        self.assertEqual(response.status_code, 302)
        inquiry = Inquiry.objects.filter(email="test@example.com").first()
        self.assertIsNotNone(inquiry)
        self.assertEqual(inquiry.name, "Test User")


class RequestControlFailClosedTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(TRUSTED_PROXY_IPS=[])
    def test_untrusted_forwarded_for_cannot_choose_rate_limit_identity(self):
        request = self.factory.post(
            "/contact/", {}, REMOTE_ADDR="198.51.100.10",
            HTTP_X_FORWARDED_FOR="203.0.113.99",
        )
        self.assertEqual(_get_ip(request), "198.51.100.10")

    @override_settings(TRUSTED_PROXY_IPS=["127.0.0.1"])
    def test_trusted_proxy_uses_valid_forwarded_client_identity(self):
        request = self.factory.post(
            "/contact/", {}, REMOTE_ADDR="127.0.0.1",
            HTTP_X_FORWARDED_FOR="203.0.113.99, 127.0.0.1",
        )
        self.assertEqual(_get_ip(request), "203.0.113.99")

    @patch("content.security.validators.cache.get", side_effect=Exception("cache down"))
    def test_form_rate_limit_fails_closed_when_cache_is_unavailable(self, mock_get):
        request = self.factory.post("/contact/", {}, REMOTE_ADDR="198.51.100.10")
        passed, reason = validate_rate_limit(request)
        self.assertFalse(passed)
        self.assertEqual(reason, "rate-limit-cache-unavailable")

    @patch("content.security.validators.cache.set", return_value=False)
    @patch("content.security.validators.cache.get", return_value=0)
    def test_form_rate_limit_fails_closed_when_cache_rejects_write(self, mock_get, mock_set):
        request = self.factory.post("/contact/", {}, REMOTE_ADDR="198.51.100.10")
        passed, reason = validate_rate_limit(request)
        self.assertFalse(passed)
        self.assertEqual(reason, "rate-limit-cache-unavailable")


class ChatEndpointSpamProtectionTests(TestCase):
    """Legacy /chat/submit/ writes ContactMessage, not Inquiry."""

    def setUp(self):
        self.url = reverse("chat:submit")
        self.form_data = {
            "name": "Test User",
            "email": "chat@example.com",
            "phone": "+1234567890",
            "message": "Test chat message",
            "g-recaptcha-response": "fake-token",
            "website_url_check": "",
            "form_render_time": "1",
        }

    @patch("content.security.spam_protection.SpamProtectionService.validate")
    def test_rejects_when_spam_detected(self, mock_validate):
        from content.security.spam_protection import SpamProtectionResult
        mock_validate.return_value = SpamProtectionResult(passed=False, error_message="Validation failed")
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(json.loads(response.content)["success"])

    @patch("content.security.spam_protection.SpamProtectionService.validate")
    def test_returns_429_on_rate_limit(self, mock_validate):
        from content.security.spam_protection import SpamProtectionResult
        mock_validate.return_value = SpamProtectionResult(
            passed=False, rate_limited=True, error_message="Too many requests"
        )
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 429)

    @patch("content.security.spam_protection.SpamProtectionService.validate")
    def test_legitimate_submission_creates_contact_message(self, mock_validate):
        from content.security.spam_protection import SpamProtectionResult
        mock_validate.return_value = SpamProtectionResult(passed=True)
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)["success"])
        self.assertEqual(ContactMessage.objects.filter(email="chat@example.com").count(), 1)
        self.assertEqual(Inquiry.objects.count(), 0)
