import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")

import django
django.setup()

from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from properties.models import Inquiry, Property
from content.views import contact
from properties.views import create_inquiry

# Mock spam validation by patching SpamProtectionService.validate to return a passed result
from unittest.mock import patch
from unittest.mock import MagicMock
mock_passed = MagicMock()
mock_passed.passed = True
mock_passed.rate_limited = False
mock_passed.error_message = None
mock_passed.confidence_boost = 0

# 1. Test General Inquiry submission (Homepage Consultation form)
print("Testing General Inquiry Form submission...")
factory = RequestFactory()
request = factory.post('/contact/', {
    'form_source': 'General Inquiry',
    'name': 'Test Lead Owner',
    'email': 'leadowner@example.com',
    'phone': '9876543210',
    'contact_country_code': '+91',
    'service': 'buy-sell',
    'property_type': 'plot',
    'locality': 'perungudi',
    'user_role': 'owner',
    'nri_status': 'Yes',
    'message': 'I want to sell my plot quickly.'
})
# Attach messages framework mock
session_mock = MagicMock()
session_mock.session_key = 'test-session'
setattr(request, 'session', session_mock)
messages_store = FallbackStorage(request)
setattr(request, '_messages', messages_store)

with patch('content.security.spam_protection.SpamProtectionService.validate', return_value=mock_passed):
    response = contact(request)

# Query the database for the created inquiry
inq = Inquiry.objects.filter(email='leadowner@example.com').first()
if inq:
    print(f"Successfully Created Inquiry ID: {inq.id}")
    print("Inquiry Message Field Content:")
    print("-" * 50)
    print(inq.message)
    print("-" * 50)
else:
    print("Failed to create general inquiry!")

# 2. Test Quick Inquiry submission (Property Detail Sidebar form)
print("\nTesting Quick Inquiry Form (Property Detail Sidebar) submission...")
prop = Property.objects.first()
if prop:
    request_sidebar = factory.post('/properties/inquire/', {
        'property_id': prop.id,
        'form_source': 'Property Detail Form',
        'name': 'Test Sidebar Lead',
        'email': 'sidebarlead@example.com',
        'phone': '9876543210',
        'user_role': 'buyer',
        'contact_preference': 'whatsapp',
        'nri_status': 'Yes',
        'message': 'Is this property still available?'
    })
    session_mock_sidebar = MagicMock()
    session_mock_sidebar.session_key = 'test-session'
    setattr(request_sidebar, 'session', session_mock_sidebar)
    setattr(request_sidebar, '_messages', FallbackStorage(request_sidebar))
    
    with patch('content.security.spam_protection.SpamProtectionService.validate', return_value=mock_passed):
        response_sidebar = create_inquiry(request_sidebar)
        
    inq_sidebar = Inquiry.objects.filter(email='sidebarlead@example.com').first()
    if inq_sidebar:
        print(f"Successfully Created Sidebar Inquiry ID: {inq_sidebar.id}")
        print("Inquiry Message Field Content:")
        print("-" * 50)
        print(inq_sidebar.message)
        print("-" * 50)
    else:
        print("Failed to create sidebar inquiry!")
else:
    print("No property found to test sidebar inquiry.")

# 3. Test Mid-page Quick Inquiry submission
print("\nTesting Homepage Mid-page Quick Inquiry submission...")
request_mid = factory.post('/contact/', {
    'form_source': 'Quick Inquiry',
    'name': 'Test Mid Lead',
    'email': 'midlead@example.com',
    'phone': '9876543210',
    'contact_country_code': '+91',
    'service': 'buy-sell',
    'property_type': 'plot',
    'locality': 'chromepet',
    'user_role': 'owner',
    'nri_status': 'Yes',
    'message': 'I want to sell my plot.'
})
session_mock_mid = MagicMock()
session_mock_mid.session_key = 'test-session'
setattr(request_mid, 'session', session_mock_mid)
setattr(request_mid, '_messages', FallbackStorage(request_mid))

with patch('content.security.spam_protection.SpamProtectionService.validate', return_value=mock_passed):
    response_mid = contact(request_mid)

inq_mid = Inquiry.objects.filter(email='midlead@example.com').first()
if inq_mid:
    print(f"Successfully Created Mid-page Inquiry ID: {inq_mid.id}")
    print("Inquiry Message Field Content:")
    print("-" * 50)
    print(inq_mid.message)
    print("-" * 50)
else:
    print("Failed to create mid-page inquiry!")
