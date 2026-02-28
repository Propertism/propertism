from django.db import models
from django.utils.text import slugify


class CompanyInfo(models.Model):
    """Single instance model for company information"""
    company_name = models.CharField(max_length=200, default="Propertism Realty Advisors LLP")
    tagline = models.TextField(default="We manage your property and resources when you are far from the nation")
    about_mission = models.TextField(blank=True)
    about_description = models.TextField(blank=True)
    
    # Hero Section
    hero_eyebrow = models.CharField(max_length=100, blank=True, help_text="Small text above hero title")
    hero_title = models.CharField(max_length=300, default="NRI Property Management Services In India, Chennai")
    hero_description = models.TextField(default="We manage your property and resources when you are far from the nation")
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True, help_text="Hero background image")
    
    # India Office
    india_office_address = models.TextField()
    india_office_city = models.CharField(max_length=100, default="Chennai")
    india_office_state = models.CharField(max_length=100, default="Tamil Nadu")
    india_office_pincode = models.CharField(max_length=20, default="600093")
    india_phone_1 = models.CharField(max_length=20)
    india_phone_2 = models.CharField(max_length=20, blank=True)
    india_phone_3 = models.CharField(max_length=20, blank=True)
    
    # US Office
    us_office_address = models.TextField()
    us_office_city = models.CharField(max_length=100, default="Hackensack")
    us_office_state = models.CharField(max_length=100, default="NJ")
    us_office_zipcode = models.CharField(max_length=20, default="07601")
    us_phone = models.CharField(max_length=20)
    
    # Contact
    email = models.EmailField(default="info@propertism.com")
    
    # Social Media
    facebook_url = models.URLField(blank=True, default="https://facebook.com/propertism")
    twitter_url = models.URLField(blank=True, default="https://twitter.com/propertism")
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


class TeamMember(models.Model):
    """Management team members"""
    name = models.CharField(max_length=200)
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
    published_date = models.DateTimeField(auto_now_add=True)
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
    phone = models.CharField(max_length=20)
    
    SERVICE_CHOICES = [
        ('buy-sell', 'Real Estate Buy & Sell'),
        ('rental', 'Rental & Maintenance'),
        ('industrial', 'Industrial Land Services'),
        ('consultation', 'General Consultation'),
    ]
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    
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
