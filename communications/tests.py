import time
from django.test import TransactionTestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from communications.models import (
    CommunicationBrand,
    CommunicationLanguage,
    CommunicationTemplate,
    CommunicationChannel,
    CommunicationRequest,
    CommunicationDelivery,
    CommunicationLog,
    CommunicationRetry,
    CommunicationType,
)
from communications.services import AcknowledgementService

@override_settings(COMMUNICATIONS_ASYNC=False)
class CommunicationsModelTests(TransactionTestCase):
    def setUp(self):
        # Setup defaults if not already seeded
        self.brand, _ = CommunicationBrand.objects.get_or_create(
            name="Test Brand",
            defaults={"is_default": True, "primary_color": "#123456"}
        )
        self.lang, _ = CommunicationLanguage.objects.get_or_create(
            code="en",
            defaults={"name": "English", "is_active": True}
        )
        self.comm_type, _ = CommunicationType.objects.get_or_create(
            key="test_type",
            defaults={"name": "Test Type", "description": "Test Type Desc"}
        )
        self.template, _ = CommunicationTemplate.objects.get_or_create(
            communication_type=self.comm_type,
            language=self.lang,
            defaults={
                "name": "Test Template",
                "subject_template": "Hello {{ name }}",
                "body_template": "Welcome, {{ name }}. Message: {{ message }}",
                "brand": self.brand
            }
        )
        self.channel, _ = CommunicationChannel.objects.get_or_create(
            key="email",
            defaults={"name": "Email", "is_active": True}
        )

    def test_acknowledgement_send_and_asynchronous_dispatch(self):
        # Mock providers to verify dispatch
        with patch('communications.providers.SMTPProvider.send') as mock_smtp_send:
            mock_smtp_send.return_value = "Mocked SMTP Success"
            
            # Send acknowledgement
            request = AcknowledgementService.send(
                communication_type_key="test_type",
                recipient="test@example.com",
                context={"name": "John Doe", "message": "Unit Test Message"},
                channels=["email"],
                module="test_module"
            )
            
            # Assert audit request is stored in database
            self.assertIsNotNone(request)
            self.assertEqual(request.module, "test_module")
            self.assertEqual(request.recipient, "test@example.com")
            
            # Wait briefly for background thread to run
            time.sleep(0.5)
            
            # Verify SMTP was called with resolved templates
            mock_smtp_send.assert_called_once_with(
                recipient="test@example.com",
                subject="Hello John Doe",
                body="Welcome, John Doe. Message: Unit Test Message",
                html_body=""
            )
            
            # Verify delivery record state
            delivery = CommunicationDelivery.objects.filter(request=request).first()
            self.assertIsNotNone(delivery)
            self.assertEqual(delivery.status, "sent")
            self.assertEqual(delivery.retry_count, 0)
            
            # Verify log entry was recorded
            log = CommunicationLog.objects.filter(delivery=delivery).first()
            self.assertIsNotNone(log)
            self.assertEqual(log.status, "sent")
            self.assertEqual(log.provider_response, "Mocked SMTP Success")


@override_settings(COMMUNICATIONS_ASYNC=False)
class CommunicationsAPITests(APITestCase):
    def setUp(self):
        self.brand, _ = CommunicationBrand.objects.get_or_create(
            name="Test Brand",
            defaults={"is_default": True}
        )
        self.lang, _ = CommunicationLanguage.objects.get_or_create(
            code="en",
            defaults={"name": "English", "is_active": True}
        )
        self.comm_type, _ = CommunicationType.objects.get_or_create(
            key="test_type",
            defaults={"name": "Test Type"}
        )

    def test_dashboard_endpoint(self):
        url = reverse('communication_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_requests', response.data)
        self.assertIn('success_rate', response.data)

    def test_send_api_endpoint(self):
        url = reverse('communication_send')
        data = {
            "communication_type_key": "test_type",
            "recipient": "test_api@example.com",
            "context": {"name": "API User"},
            "channels": ["email"],
            "module": "api_test"
        }
        with patch('communications.providers.SMTPProvider.send') as mock_smtp_send:
            mock_smtp_send.return_value = "API SMTP Success"
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['status'], 'success')
            self.assertIn('request_id', response.data)
