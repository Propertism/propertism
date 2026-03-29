from django.contrib import admin
from properties.models import ContactMessage

# Chat messages are now managed through ContactMessage in properties app
# No need to register here as it's already registered in properties/admin.py
