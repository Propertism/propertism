from django.db import models
from django.utils import timezone


class ContactInquiry(models.Model):
    """Contact inquiry model for Request Quote form"""
    
    INQUIRY_TYPES = [
        ('buy_sell', 'Real Estate Buy & Sell'),
        ('rental', 'Rental & Maintenance'),
        ('industrial', 'Industrial Land Services'),
        ('general', 'General Inquiry'),
    ]
    
    # Contact Information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Inquiry Details
    inquiry_type = models.CharField(
        max_length=20, 
        choices=INQUIRY_TYPES,
        default='general'
    )
    property_type = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Admin notes")
    
    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_inquiry_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"


class NewsletterSubscriber(models.Model):
    """Newsletter subscription model"""
    
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
