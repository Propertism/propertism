from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class CompanyInfo(models.Model):
    """Single instance model for company information"""
    INDIA_OFFICE_ADDRESS = "No. 30, 3rd Floor\nSSR Pankajam Towers\nArunachalam Road, Saligramam"
    US_OFFICE_ADDRESS = "46 Berkshire Pl"

    company_name = models.CharField(max_length=200, default="Propertism Realty Advisors LLP")
    tagline = models.TextField(default="We manage your property and resources when you are far from the nation.")
    about_mission = models.TextField(blank=True)
    about_description = models.TextField(blank=True)
    
    # Hero Section
    hero_eyebrow = models.CharField(max_length=100, blank=True, help_text="Small text above hero title")
    hero_eyebrow_color = models.CharField(max_length=7, default="#B89A4A", help_text="Hex color code (e.g., #B89A4A)")
    hero_title = models.CharField(max_length=300, default="NRI Property Management Services In India, Chennai")
    hero_title_color = models.CharField(max_length=7, default="#0F172A", help_text="Hex color code (e.g., #0F172A)")
    hero_description = models.TextField(default="We manage your property and resources when you are far from the nation")
    hero_description_color = models.CharField(max_length=7, default="#475569", help_text="Hex color code (e.g., #475569)")
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True, help_text="Hero background image")
    logo = models.ImageField(upload_to='company/', blank=True, null=True, help_text="Company logo used across the site")

    # Homepage section copy
    about_section_eyebrow = models.CharField(max_length=100, default="About")
    about_section_title = models.CharField(max_length=200, default="Property support for owners living abroad.")
    about_primary_cta_text = models.CharField(max_length=80, default="Meet Management")
    about_secondary_cta_text = models.CharField(max_length=80, default="Request a callback")
    proof_section_eyebrow = models.CharField(max_length=100, default="Why Owners Stay With Us")
    proof_section_title = models.CharField(
        max_length=220,
        default="Clear updates, reliable follow-through, and local execution.",
    )
    properties_section_title = models.CharField(max_length=200, default="Featured Properties for NRIs")
    properties_section_subtitle = models.TextField(
        default="Handpicked premium properties perfect for investment"
    )
    properties_section_cta_text = models.CharField(max_length=80, default="Request Property Shortlist")
    services_section_title = models.CharField(max_length=200, default="Services built for NRI ownership")
    services_section_description = models.TextField(
        default="Buy, rent, maintain, and monitor property with one coordinated team in Chennai."
    )
    services_card_cta_text = models.CharField(max_length=80, default="Discuss this service")
    management_section_eyebrow = models.CharField(max_length=100, default="Management")
    management_section_title = models.CharField(
        max_length=220,
        default="One team coordinating owners, tenants, vendors, and follow-through.",
    )
    management_section_description = models.TextField(
        default=(
            "Practical accountability on the ground matters more than generic advisory. "
            "The management team is structured around execution, reporting, and decision support for owners abroad."
        )
    )
    blog_section_eyebrow = models.CharField(max_length=100, default="Insights")
    blog_section_title = models.CharField(
        max_length=220,
        default="Useful updates for owners managing from abroad.",
    )
    blog_section_description = models.TextField(
        default="Short, practical support for reporting, rentals, maintenance, Chennai"
    )
    contact_section_eyebrow = models.CharField(max_length=100, default="Get in Touch")
    contact_section_title = models.CharField(max_length=200, default="Let's discuss your property needs")
    contact_section_description = models.TextField(
        default=(
            "Whether you're managing from abroad or looking to invest in Chennai, we're here to help. "
            "Share your requirements and we'll provide expert guidance."
        )
    )
    contact_primary_cta_text = models.CharField(max_length=80, default="Talk to Us")
    contact_form_submit_text = models.CharField(max_length=80, default="Send My Request")

    # Footer and chat copy
    footer_services_heading = models.CharField(max_length=120, default="Service Coverage")
    footer_newsletter_heading = models.CharField(max_length=120, default="Stay Updated")
    footer_newsletter_description = models.TextField(
        default="Subscribe for market insights, NRI ownership updates, and new property opportunities."
    )
    footer_newsletter_button_text = models.CharField(max_length=80, default="Subscribe")
    chat_window_title = models.CharField(max_length=120, default="Leave a message")
    chat_window_subtitle = models.CharField(max_length=160, default="We'll get back to you soon")
    chat_submit_text = models.CharField(max_length=40, default="Send")
    chat_sending_text = models.CharField(max_length=40, default="Sending...")
    chat_success_title = models.CharField(max_length=120, default="Message sent!")
    chat_success_message = models.TextField(
        default="Thanks for reaching out. We'll get back to you within 24 hours."
    )
    
    # India Office
    india_office_address = models.TextField(default=INDIA_OFFICE_ADDRESS)
    india_office_city = models.CharField(max_length=100, default="Chennai")
    india_office_state = models.CharField(max_length=100, default="Tamil Nadu")
    india_office_pincode = models.CharField(max_length=20, default="600093")
    india_phone_1 = models.CharField(max_length=20, default="+91 86670 20798")
    india_phone_2 = models.CharField(max_length=20, blank=True, default="+91 98412 01930")
    india_phone_3 = models.CharField(max_length=20, blank=True, default="+91 98418 44452")
    
    # US Office
    us_office_address = models.TextField(default=US_OFFICE_ADDRESS)
    us_office_city = models.CharField(max_length=100, default="Hackensack")
    us_office_state = models.CharField(max_length=100, default="NJ")
    us_office_zipcode = models.CharField(max_length=20, default="07601")
    us_phone = models.CharField(max_length=20, default="+1 518 409 3485")
    
    # Contact
    email = models.EmailField(default="info@propertism.in")
    
    # Social Media
    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/PropertismIndia")
    twitter_url = models.URLField(blank=True, default="https://x.com/PropertismIndia")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com/company/propertism")
    
    # Business Hours
    business_hours = models.CharField(max_length=200, default="Monday - Saturday: 9:00 AM - 6:00 PM IST")
    
    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"
    
    def __str__(self):
        return self.company_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and CompanyInfo.objects.exists():
            raise ValueError('Only one CompanyInfo instance is allowed')
        return super().save(*args, **kwargs)

    def get_active_hero_backgrounds(self):
        if not self.pk:
            return []
        try:
            return list(self.hero_backgrounds.filter(is_active=True).order_by("order", "id"))
        except Exception:
            return []

    def get_primary_hero_image(self):
        hero_backgrounds = self.get_active_hero_backgrounds()
        if hero_backgrounds:
            return hero_backgrounds[0].image
        return self.hero_image


class HeroBackgroundImage(models.Model):
    """Hero background images that rotate on the homepage."""

    company = models.ForeignKey(
        CompanyInfo,
        on_delete=models.CASCADE,
        related_name="hero_backgrounds",
    )
    image = models.ImageField(upload_to="hero/")
    order = models.PositiveSmallIntegerField(default=0, help_text="Display order for the hero rotation.")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Hero Background Image"
        verbose_name_plural = "Hero Background Images"

    def __str__(self):
        return f"{self.company.company_name} hero background {self.order + 1}"

    def clean(self):
        super().clean()
        if not self.company_id:
            return

        existing_images = HeroBackgroundImage.objects.filter(company_id=self.company_id)
        if self.pk:
            existing_images = existing_images.exclude(pk=self.pk)
        if existing_images.count() >= 5:
            raise ValidationError("You can add a maximum of 5 hero background images.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Statistic(models.Model):
    """Company statistics displayed on homepage and about page"""
    label = models.CharField(max_length=100, help_text="e.g., Properties Managed")
    value = models.CharField(max_length=50, help_text="e.g., 500+")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"
    
    def __str__(self):
        return f"{self.value} {self.label}"


class Service(models.Model):
    """Services offered by the company"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(help_text="Brief description for cards")
    full_description = models.TextField(help_text="Detailed description for service page")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon identifier or emoji")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Features
    features = models.TextField(blank=True, help_text="One feature per line")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_features_list(self):
        """Return features as a list"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []


class CoreValue(models.Model):
    """Company core values"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="Icon identifier or symbol")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Core Value"
        verbose_name_plural = "Core Values"
    
    def __str__(self):
        return self.title


class CustomerReviewSection(models.Model):
    """Single review section displayed on the homepage."""
    eyebrow = models.CharField(max_length=100, default="Customer Reviews")
    title = models.CharField(max_length=200, default="What Our Customers Say")
    description = models.TextField(
        blank=True,
        default="Hear from customers who trust us for responsive, dependable service.",
    )
    badge_title = models.CharField(max_length=120, blank=True, default="Five Star Service")
    badge_text = models.CharField(max_length=200, blank=True, default="Quality Guaranteed")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Customer Review Section"
        verbose_name_plural = "Customer Review Section"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and CustomerReviewSection.objects.exists():
            raise ValueError("Only one CustomerReviewSection instance is allowed")
        return super().save(*args, **kwargs)


class CustomerReview(models.Model):
    """Individual customer review cards."""
    section = models.ForeignKey(
        CustomerReviewSection,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    service_label = models.CharField(max_length=120, blank=True)
    customer_name = models.CharField(max_length=120)
    customer_location = models.CharField(max_length=120, blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    avatar_initials = models.CharField(
        max_length=4,
        blank=True,
        help_text="Leave blank to generate initials automatically.",
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Customer Review"
        verbose_name_plural = "Customer Reviews"

    def __str__(self):
        return f"{self.customer_name} review"

    @property
    def display_initials(self):
        if self.avatar_initials:
            return self.avatar_initials.strip().upper()
        parts = [part[0].upper() for part in self.customer_name.split() if part][:2]
        return "".join(parts) or "C"

    @property
    def star_icons(self):
        rating = max(1, min(int(self.rating or 5), 5))
        return "★" * rating


class HomepageCardSection(models.Model):
    """Configurable homepage section rendered as cards."""
    slug = models.SlugField(unique=True, blank=True)
    eyebrow = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    badge_title = models.CharField(max_length=120, blank=True)
    badge_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Homepage Card Section"
        verbose_name_plural = "Homepage Card Sections"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class HomepageCard(models.Model):
    """Cards that belong to a configurable homepage section."""
    section = models.ForeignKey(
        HomepageCardSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    eyebrow = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    footer = models.CharField(max_length=160, blank=True)
    cta_text = models.CharField(max_length=80, blank=True)
    cta_url = models.CharField(max_length=300, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Homepage Card"
        verbose_name_plural = "Homepage Cards"

    def __str__(self):
        return f"{self.section.title} - {self.title}"


class TeamMember(models.Model):
    """Management team members"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="URL-friendly version of name")
    role = models.CharField(max_length=200, help_text="e.g., Managing Director")
    department = models.CharField(max_length=100, blank=True, help_text="e.g., Leadership & Strategy")
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Expertise
    expertise = models.TextField(blank=True, help_text="Comma-separated expertise areas")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return f"{self.name} - {self.role}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_expertise_list(self):
        """Return expertise as a list"""
        if self.expertise:
            return [e.strip() for e in self.expertise.split(',') if e.strip()]
        return []


class ExpertiseArea(models.Model):
    """Collective expertise areas"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Expertise Area"
        verbose_name_plural = "Expertise Areas"
    
    def __str__(self):
        return self.title


class BlogPost(models.Model):
    """Blog posts"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(help_text="Short summary for listing page")
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.CharField(max_length=100, default="Propertism Team")
    published_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    # Categories
    CATEGORY_CHOICES = [
        ('nri', 'NRI Property Management'),
        ('market', 'Chennai Real Estate Market'),
        ('legal', 'Legal & Compliance'),
        ('maintenance', 'Property Maintenance'),
        ('investment', 'Investment Strategies'),
        ('tenant', 'Tenant Management'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='nri')
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Newsletter(models.Model):
    """Newsletter subscriptions"""
    email = models.EmailField(unique=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_date']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
    
    def __str__(self):
        return self.email


class ContactInquiry(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    SERVICE_CHOICES = [
        ('buy-sell', 'Real Estate Buy & Sell'),
        ('rental', 'Rental & Maintenance'),
        ('industrial', 'Industrial Land Services'),
        ('consultation', 'General Consultation'),
    ]
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True)
    
    PROPERTY_CHOICES = [
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('plot', 'Plot'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial Land'),
    ]
    property_type = models.CharField(max_length=20, choices=PROPERTY_CHOICES, blank=True)
    
    message = models.TextField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Internal notes")
    
    class Meta:
        ordering = ['-submitted_date']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
    
    def __str__(self):
        return f"{self.name} - {self.service} ({self.submitted_date.strftime('%Y-%m-%d')})"


class LandingLead(models.Model):
    """Lead submissions captured directly from dynamic landing pages."""

    INTENT_TYPE_CHOICES = [
        ("sell", "Sell"),
        ("management", "Management"),
        ("rental", "Rental"),
        ("maintenance", "Maintenance"),
        ("informational", "Informational"),
        ("buy", "Buy"),
    ]

    PROPERTY_CHOICES = [
        ("apartment", "Apartment"),
        ("villa", "Villa"),
        ("plot", "Plot"),
        ("commercial", "Commercial"),
        ("industrial", "Industrial Land"),
    ]

    LEAD_STAGE_CHOICES = [
        ("initiated", "Initiated"),
        ("qualified", "Qualified"),
    ]

    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    property_city = models.CharField(max_length=120)
    property_type = models.CharField(max_length=20, choices=PROPERTY_CHOICES, blank=True)
    intent_type = models.CharField(max_length=20, choices=INTENT_TYPE_CHOICES)
    geo_origin = models.CharField(max_length=120, blank=True)
    lead_stage = models.CharField(max_length=20, choices=LEAD_STAGE_CHOICES, default="initiated")
    lead_score = models.IntegerField(default=0)
    lead_category = models.CharField(max_length=10, default="cold")
    qualification_data = models.JSONField(default=dict, blank=True)
    expected_price_range = models.CharField(max_length=120, blank=True)
    preferred_contact_time = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Landing Lead"
        verbose_name_plural = "Landing Leads"

    def __str__(self):
        return f"{self.phone} - {self.intent_type} ({self.created_at.strftime('%Y-%m-%d')})"

    def _compute_lead_score(self):
        score = 0
        intent_type = (self.intent_type or "").strip()
        if intent_type == "sell":
            score += 5
        if intent_type == "management":
            score += 2
        if self.geo_origin:
            score += 3

        qualification = self.qualification_data or {}
        selling_timeline = (qualification.get("selling_timeline") or "").strip()
        if selling_timeline in {"immediate", "30-days"}:
            score += 3
        return score

    @staticmethod
    def _lead_category_for(score):
        if score >= 8:
            return "hot"
        if score >= 4:
            return "warm"
        return "cold"

    def save(self, *args, **kwargs):
        self.lead_score = self._compute_lead_score()
        self.lead_category = self._lead_category_for(self.lead_score)
        return super().save(*args, **kwargs)
