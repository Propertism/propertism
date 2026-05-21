from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


_ONES = {
    0: "Zero",
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Eleven",
    12: "Twelve",
    13: "Thirteen",
    14: "Fourteen",
    15: "Fifteen",
    16: "Sixteen",
    17: "Seventeen",
    18: "Eighteen",
    19: "Nineteen",
}

_TENS = {
    20: "Twenty",
    30: "Thirty",
    40: "Forty",
    50: "Fifty",
    60: "Sixty",
    70: "Seventy",
    80: "Eighty",
    90: "Ninety",
}

_INDIAN_SCALES = (
    (10**7, "Crore"),
    (10**5, "Lakh"),
    (10**3, "Thousand"),
)

_INTERNATIONAL_SCALES = (
    (10**9, "Billion"),
    (10**6, "Million"),
    (10**3, "Thousand"),
)


def _format_indian_number(value, show_decimals=False):
    integer_part = str(int(value))
    
    if len(integer_part) <= 3:
        formatted_integer = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        chunks = []
        while remaining:
            chunks.append(remaining[-2:])
            remaining = remaining[:-2]
        formatted_integer = ",".join(reversed(chunks)) + f",{last_three}"
    
    if show_decimals:
        fractional_part = f"{value:.2f}".split(".")[1]
        return f"{formatted_integer}.{fractional_part}"
    
    return formatted_integer


def _number_to_words(number, scales):
    number = int(number)

    if number == 0:
        return "Zero"
    if number < 20:
        return _ONES[number]
    if number < 100:
        tens_value = (number // 10) * 10
        remainder = number % 10
        if remainder:
            return f"{_TENS[tens_value]} {_number_to_words(remainder, scales)}"
        return _TENS[tens_value]
    if number < 1000:
        remainder = number % 100
        if remainder:
            return f"{_ONES[number // 100]} Hundred {_number_to_words(remainder, scales)}"
        return f"{_ONES[number // 100]} Hundred"

    for scale_value, scale_name in scales:
        if number >= scale_value:
            major_value, remainder = divmod(number, scale_value)
            major_words = _number_to_words(major_value, scales)
            
            # Simple pluralization for Indian scales
            display_scale = scale_name
            if major_value > 1 and scale_name in ["Lakh", "Crore"]:
                display_scale = f"{scale_name}s"
                
            if remainder:
                return f"{major_words} {display_scale} {_number_to_words(remainder, scales)}"
            return f"{major_words} {display_scale}"

    return str(number)


class PropertyType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Property Types"


class Property(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("pending", "Pending"),
        ("construction", "Under Construction"),
    ]

    PRICE_TYPE_CHOICES = [
        ("sale", "For Sale"),
        ("rent", "For Rent"),
    ]

    CURRENCY_CHOICES = [
        ("INR", "Indian Rupee"),
        ("USD", "US Dollar"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="INR")
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES, default="sale")
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    location = models.CharField(max_length=255)
    image = models.URLField(max_length=500, blank=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.title) or 'property'
            slug = base
            qs = Property.objects.exclude(pk=self.pk) if self.pk else Property.objects.all()
            counter = 1
            while qs.filter(slug=slug).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('property_detail', kwargs={'slug': self.slug})

    def _normalize_image_reference(self, value):
        if not value:
            return ""

        image_value = str(value).strip()
        if not image_value:
            return ""

        if image_value.startswith(("http://", "https://", "//", "/")):
            return image_value

        normalized_value = image_value.lstrip("/")
        if normalized_value.startswith("media/"):
            return f"/{normalized_value}"

        media_url = (settings.MEDIA_URL or "/media/").rstrip("/")
        return f"{media_url}/{normalized_value}"

    def get_display_image_url(self):
        """Return the best available photo URL and let template onerror handle final fallback."""
        photos = self.photos.all()
        if hasattr(photos, "order_by"):
            photos = photos.order_by("-is_primary", "sort_order", "id")

        for photo in photos:
            if not photo.image:
                continue
            try:
                return photo.image.url
            except Exception:
                continue

        return self._normalize_image_reference(self.image)

    @property
    def currency_symbol(self):
        return "₹" if self.currency == "INR" else "$"

    @property
    def currency_unit_label(self):
        return "Indian Rupees" if self.currency == "INR" else "US Dollars"

    @property
    def currency_minor_unit_label(self):
        return "Paise" if self.currency == "INR" else "Cents"

    @property
    def formatted_price_value(self):
        normalized_price = Decimal(self.price).quantize(Decimal("0.01"))
        if self.currency == "INR":
            # Indian format typically hides decimals if they are zero for clean display
            show_decimals = (normalized_price % 1) != 0
            return _format_indian_number(normalized_price, show_decimals=show_decimals)
        return f"{normalized_price:,.2f}"

    @property
    def formatted_price(self):
        return f"{self.currency_symbol}{self.formatted_price_value}"

    @property
    def price_in_words(self):
        normalized_price = Decimal(self.price).quantize(Decimal("0.01"))
        whole_value = int(normalized_price)
        fractional_value = int((normalized_price - whole_value) * 100)
        scales = _INDIAN_SCALES if self.currency == "INR" else _INTERNATIONAL_SCALES

        words = _number_to_words(whole_value, scales)
        if fractional_value:
            fractional_words = _number_to_words(fractional_value, _INTERNATIONAL_SCALES)
            return f"{words} and {fractional_words} {self.currency_minor_unit_label}"
        return words

    @property
    def price_in_words_standard(self):
        """Standard format: Rupees X Lakhs Only"""
        if self.currency == "INR":
            return f"Rupees {self.price_in_words} Only"
        return f"{self.price_in_words} {self.currency_unit_label} Only"

    @property
    def price_in_words_with_currency(self):
        return f"{self.price_in_words} {self.currency_unit_label}"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ["-created_at"]


class PropertyPhoto(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="properties/")
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.title} - Photo {self.id}"

    class Meta:
        verbose_name_plural = "Property Photos"
        ordering = ["sort_order"]


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("contacted", "Contacted"),
        ("closed", "Closed"),
    ]

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inquiry from {self.name} - {self.property.title if self.property else 'General'}"

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"], name="inquiry_created_idx"),
            models.Index(fields=["status", "created_at"], name="inquiry_status_created_idx"),
        ]


class MaintenanceRequest(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.property.title if self.property else 'General'}"

    class Meta:
        verbose_name_plural = "Maintenance Requests"
        ordering = ["-created_at"]


class SupportTicket(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"

    class Meta:
        verbose_name_plural = "Support Tickets"
        ordering = ["-created_at"]


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("read", "Read"),
        ("replied", "Replied"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.subject:
            return f"Message from {self.name} - {self.subject}"
        return f"Message from {self.name}"

    class Meta:
        verbose_name_plural = "Contact Messages"
        ordering = ["-created_at"]
