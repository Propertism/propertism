from django.db import models


class NRIService(models.Model):
    PROPERTY_CARE = 'PROPERTY_CARE'
    SALE = 'SALE'
    ACQUISITION = 'ACQUISITION'
    PRIORITY = 'PRIORITY'

    CATEGORY_CHOICES = [
        (PROPERTY_CARE, 'Property Care'),
        (SALE, 'Sale Assistance'),
        (ACQUISITION, 'Acquisition Assistance'),
        (PRIORITY, 'Priority Coordination'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, db_index=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['category', 'sort_order', 'name']
        verbose_name = 'NRI Service'
        verbose_name_plural = 'NRI Services'

    def __str__(self):
        return f"{self.get_category_display()} — {self.name}"


class NRIAssistEvent(models.Model):
    PAGE_VISIT = 'PAGE_VISIT'
    CTA_CLICK = 'CTA_CLICK'
    ADVISOR_REQUEST = 'ADVISOR_REQUEST'
    GOOGLE_LOGIN = 'GOOGLE_LOGIN'

    EVENT_CHOICES = [
        (PAGE_VISIT, 'NRI Assist Page Visit'),
        (CTA_CLICK, 'Service CTA Click'),
        (ADVISOR_REQUEST, 'Advisor Request Submitted'),
        (GOOGLE_LOGIN, 'Google Login Conversion'),
    ]

    event_type = models.CharField(max_length=30, choices=EVENT_CHOICES, db_index=True)
    user = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='nri_events'
    )
    service_category = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'NRI Assist Event'
        verbose_name_plural = 'NRI Assist Events'

    def __str__(self):
        return f"{self.event_type} — {self.created_at:%Y-%m-%d %H:%M}"
