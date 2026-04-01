"""
SCCB-46 Task 10: Unit Tests
Basic unit tests for models and views
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from properties.models import Property
from content.models import CompanyInfo, ContactInquiry, Newsletter, BlogPost
from django.urls import reverse

class PropertyModelTest(TestCase):
    """Test Property model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_property_creation(self):
        """Test creating a property"""
        property = Property.objects.create(
            title='Test Property',
            slug='test-property',
            description='Test description',
            property_type='residential',
            listing_type='sale',
            price=1000000,
            bedrooms=3,
            bathrooms=2,
            area=1500,
            status='available',
            created_by=self.user
        )
        self.assertEqual(property.title, 'Test Property')
        self.assertEqual(property.slug, 'test-property')
        self.assertEqual(property.status, 'available')
    
    def test_property_str(self):
        """Test property string representation"""
        property = Property.objects.create(
            title='Test Property',
            slug='test-property',
            description='Test',
            property_type='residential',
            listing_type='sale',
            price=1000000,
            created_by=self.user
        )
        self.assertEqual(str(property), 'Test Property')

class ContactInquiryModelTest(TestCase):
    """Test ContactInquiry model"""
    
    def test_contact_inquiry_creation(self):
        """Test creating a contact inquiry"""
        inquiry = ContactInquiry.objects.create(
            name='Test User',
            email='test@example.com',
            phone='+1234567890',
            service='buy',
            message='Test message'
        )
        self.assertEqual(inquiry.name, 'Test User')
        self.assertEqual(inquiry.email, 'test@example.com')
        self.assertFalse(inquiry.is_contacted)

class NewsletterModelTest(TestCase):
    """Test Newsletter model"""
    
    def test_newsletter_subscription(self):
        """Test newsletter subscription"""
        subscription = Newsletter.objects.create(email='newsletter@example.com')
        self.assertEqual(subscription.email, 'newsletter@example.com')
        self.assertTrue(subscription.is_active)

class ViewsTest(TestCase):
    """Test views"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
    
    def test_services_page(self):
        """Test services page loads"""
        response = self.client.get('/en/services/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_page(self):
        """Test about page loads"""
        response = self.client.get('/en/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_contact_page(self):
        """Test contact page loads"""
        response = self.client.get('/en/contact/')
        self.assertEqual(response.status_code, 200)
    
    def test_404_page(self):
        """Test 404 page"""
        response = self.client.get('/en/nonexistent-page/')
        self.assertEqual(response.status_code, 404)

class FormSubmissionTest(TestCase):
    """Test form submissions"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_contact_form_submission(self):
        """Test contact form submission"""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'service': 'buy',
            'message': 'Test message'
        }
        response = self.client.post('/en/contact/', data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(ContactInquiry.objects.count(), 1)
    
    def test_newsletter_subscription(self):
        """Test newsletter subscription"""
        data = {'email': 'newsletter@example.com'}
        response = self.client.post('/en/newsletter/subscribe/', data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Newsletter.objects.filter(email='newsletter@example.com').exists())

# Run tests with: python manage.py test
