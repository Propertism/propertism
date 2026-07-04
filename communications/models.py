import uuid
from django.db import models

class CommunicationType(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=100, unique=True, help_text="Unique key identifier, e.g. welcome, inquiry_received")
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} ({self.key})"


class CommunicationBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    email_header = models.TextField(blank=True, help_text="HTML/Text Header wrapper")
    email_footer = models.TextField(blank=True, help_text="HTML/Text Footer wrapper")
    primary_color = models.CharField(max_length=7, default="#0056b3", help_text="HEX color code")
    social_links = models.JSONField(default=dict, blank=True)
    contact_info = models.JSONField(default=dict, blank=True)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            # Enforce single default brand
            CommunicationBrand.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Default)" if self.is_default else self.name


class CommunicationLanguage(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text="e.g. en, ta, hi")
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class CommunicationTemplate(models.Model):
    name = models.CharField(max_length=100)
    communication_type = models.ForeignKey(CommunicationType, on_delete=models.CASCADE, related_name='templates')
    subject_template = models.CharField(max_length=255)
    body_template = models.TextField(help_text="Plain text body with variable support")
    html_body_template = models.TextField(blank=True, help_text="HTML body with variable support")
    brand = models.ForeignKey(CommunicationBrand, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.ForeignKey(CommunicationLanguage, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('communication_type', 'language')

    def __str__(self):
        return f"{self.name} - {self.language.code}"


class CommunicationChannel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=50, unique=True, help_text="e.g. email, whatsapp, sms")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CommunicationConfiguration(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.key


class CommunicationPreference(models.Model):
    recipient = models.CharField(max_length=255, help_text="Email address or phone number")
    channel = models.ForeignKey(CommunicationChannel, on_delete=models.CASCADE)
    is_opted_in = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('recipient', 'channel')

    def __str__(self):
        status = "Opted In" if self.is_opted_in else "Opted Out"
        return f"{self.recipient} - {self.channel.name} ({status})"


class CommunicationRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.CharField(max_length=100, help_text="Initiator, e.g. propertism_contact, realbot_chat")
    recipient = models.CharField(max_length=255)
    template = models.ForeignKey(CommunicationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    context_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} for {self.recipient} via {self.module}"


class CommunicationDelivery(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )
    request = models.ForeignKey(CommunicationRequest, on_delete=models.CASCADE, related_name='deliveries')
    channel = models.ForeignKey(CommunicationChannel, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_reference = models.CharField(max_length=100, unique=True)
    delivery_timestamp = models.DateTimeField(null=True, blank=True)
    retry_count = models.IntegerField(default=0)
    last_error = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery {self.tracking_reference} ({self.channel.name}) - {self.status}"


class CommunicationLog(models.Model):
    delivery = models.ForeignKey(CommunicationDelivery, on_delete=models.CASCADE, related_name='logs')
    status = models.CharField(max_length=50)
    provider_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.delivery.tracking_reference} - {self.status}"


class CommunicationRetry(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    delivery = models.ForeignKey(CommunicationDelivery, on_delete=models.CASCADE, related_name='retries')
    scheduled_time = models.DateTimeField()
    attempt_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Retry {self.attempt_number} for {self.delivery.tracking_reference} ({self.status})"
