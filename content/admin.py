# FIXED DUPLICATE REGISTRATION VERSION
from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    CompanyInfo, Statistic, Service, CoreValue, TeamMember,
    ExpertiseArea, BlogPost, Newsletter, ContactInquiry,
    CustomerReviewSection, CustomerReview, HomepageCardSection, HomepageCard,
    HeroBackgroundImage, LandingLead,
)


class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
        widgets = {
            'hero_eyebrow_color': forms.TextInput(attrs={'type': 'color'}),
            'hero_title_color': forms.TextInput(attrs={'type': 'color'}),
            'hero_description_color': forms.TextInput(attrs={'type': 'color'}),
        }


class HeroBackgroundImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        image_count = 0

        for form in self.forms:
            if not hasattr(form, "cleaned_data") or not form.cleaned_data:
                continue
            if form.cleaned_data.get("DELETE"):
                continue
            if form.cleaned_data.get("image") or getattr(form.instance, "pk", None):
                image_count += 1

        if image_count > 5:
            raise ValidationError("You can add up to 5 hero background images.")


class HeroBackgroundImageInline(admin.StackedInline):
    model = HeroBackgroundImage
    formset = HeroBackgroundImageInlineFormSet
    extra = 0
    max_num = 5
    fields = ("image", "image_preview", "order", "is_active")
    readonly_fields = ("image_preview",)
    ordering = ("order", "id")

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" alt="Hero background preview" style="max-height: 120px; max-width: 240px; object-fit: cover;" />',
                obj.image.url,
            )
        return "No image uploaded"

    image_preview.short_description = "Preview"


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    form = CompanyInfoForm
    readonly_fields = ('logo_preview', 'hero_image_preview')
    inlines = [HeroBackgroundImageInline]

    fieldsets = (
        ('Hero Section', {
            'fields': (
                'hero_eyebrow', 'hero_eyebrow_color',
                'hero_title', 'hero_title_color',
                'hero_description', 'hero_description_color',
                'hero_image', 'hero_image_preview'
            ),
            'description': 'Homepage hero content and fallback background image. Add up to 5 rotating hero backgrounds below.'
        }),
        ('Company Details', {
            'fields': ('company_name', 'logo', 'logo_preview', 'tagline', 'about_mission', 'about_description')
        }),
        ('Homepage Sections', {
            'fields': (
                'about_section_eyebrow', 'about_section_title',
                'about_primary_cta_text', 'about_secondary_cta_text',
                'proof_section_eyebrow', 'proof_section_title',
                'properties_section_title', 'properties_section_subtitle', 'properties_section_cta_text',
                'services_section_title', 'services_section_description', 'services_card_cta_text',
                'management_section_eyebrow', 'management_section_title', 'management_section_description',
                'blog_section_eyebrow', 'blog_section_title', 'blog_section_description',
                'contact_section_eyebrow', 'contact_section_title', 'contact_section_description',
                'contact_primary_cta_text', 'contact_form_submit_text',
            ),
            'description': 'Editable copy used across the homepage sections and major calls to action.'
        }),
        ('India Office', {
            'fields': ('india_office_address', 'india_office_city', 'india_office_state', 
                      'india_office_pincode', 'india_phone_1', 'india_phone_2', 'india_phone_3')
        }),
        ('US Office', {
            'fields': ('us_office_address', 'us_office_city', 'us_office_state', 
                      'us_office_zipcode', 'us_phone')
        }),
        ('Contact & Social', {
            'fields': (
                'email', 'business_hours',
                'facebook_url', 'twitter_url', 'linkedin_url', 
                'instagram_url', 'whatsapp_url', 'youtube_url'
            )
        }),
        ('Footer & Chat', {
            'fields': (
                'footer_services_heading',
                'footer_newsletter_heading', 'footer_newsletter_description', 'footer_newsletter_button_text',
                'chat_window_title', 'chat_window_subtitle',
                'chat_submit_text', 'chat_sending_text',
                'chat_success_title', 'chat_success_message',
            ),
            'description': 'Controls footer newsletter copy and the floating chat popup text.'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not CompanyInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False

    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html(
                '<img src="{}" alt="Current logo" style="max-height: 80px; max-width: 240px; object-fit: contain;" />',
                obj.logo.url,
            )
        return "No logo uploaded"

    logo_preview.short_description = 'Current logo'

    def hero_image_preview(self, obj):
        if obj and obj.hero_image:
            return format_html(
                '<img src="{}" alt="Current hero image" style="max-height: 160px; max-width: 320px; object-fit: cover;" />',
                obj.hero_image.url,
            )
        return "No hero image uploaded"

    hero_image_preview.short_description = 'Current hero image'


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('label', 'value')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'full_description')
        }),
        ('Media', {
            'fields': ('icon', 'image')
        }),
        ('Features', {
            'fields': ('features',),
            'description': 'Enter one feature per line'
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


class CustomerReviewInline(admin.StackedInline):
    model = CustomerReview
    extra = 0
    fields = (
        'customer_name', 'customer_location', 'service_label', 'quote',
        'rating', 'avatar_initials', 'order', 'is_active'
    )
    ordering = ('order',)


@admin.register(CustomerReviewSection)
class CustomerReviewSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    inlines = [CustomerReviewInline]
    fieldsets = (
        ('Section Content', {
            'fields': ('eyebrow', 'title', 'description')
        }),
        ('Badge', {
            'fields': ('badge_title', 'badge_text')
        }),
        ('Display', {
            'fields': ('is_active',)
        }),
    )

    def has_add_permission(self, request):
        return not CustomerReviewSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        review_section = CustomerReviewSection.objects.first()
        if review_section:
            change_url = reverse(
                'admin:content_customerreviewsection_change',
                args=[review_section.pk],
            )
            return HttpResponseRedirect(change_url)
        return super().changelist_view(request, extra_context=extra_context)


class HomepageCardInline(admin.StackedInline):
    model = HomepageCard
    extra = 0
    fields = ('eyebrow', 'title', 'description', 'footer', 'cta_text', 'cta_url', 'order', 'is_active')
    ordering = ('order',)


@admin.register(HomepageCardSection)
class HomepageCardSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [HomepageCardInline]
    fieldsets = (
        ('Section Content', {
            'fields': ('title', 'slug', 'eyebrow', 'description')
        }),
        ('Badge', {
            'fields': ('badge_title', 'badge_text')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'department', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'department')
    search_fields = ('name', 'role', 'bio')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'role', 'department', 'bio', 'photo')
        }),
        ('Expertise', {
            'fields': ('expertise',),
            'description': 'Enter comma-separated expertise areas'
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(ExpertiseArea)
class ExpertiseAreaAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published_date', 'is_published')
    list_filter = ('is_published', 'category', 'published_date')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Meta', {
            'fields': ('author', 'category')
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_date')
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_date', 'is_active')
    list_filter = ('is_active', 'subscribed_date')
    search_fields = ('email',)
    date_hierarchy = 'subscribed_date'
    readonly_fields = ('subscribed_date',)


# @admin.register(ContactInquiry)
# class ContactInquiryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'service', 'submitted_date', 'is_read')
#     list_filter = ('is_read', 'service', 'property_type', 'submitted_date')
#     search_fields = ('name', 'email', 'phone', 'message')
#     date_hierarchy = 'submitted_date'
#     readonly_fields = ('submitted_date',)
#     fieldsets = (
#         ('Contact Information', {
#             'fields': ('name', 'email', 'phone')
#         }),
#         ('Inquiry Details', {
#             'fields': ('service', 'property_type', 'message')
#         }),
#         ('Status', {
#             'fields': ('is_read', 'notes', 'submitted_date')
#         }),
#     )
#     
#     def get_readonly_fields(self, request, obj=None):
#         if obj:  # Editing existing object
#             return self.readonly_fields + ('name', 'email', 'phone', 'service', 'property_type', 'message')
#         return self.readonly_fields


@admin.register(LandingLead)
class LandingLeadAdmin(admin.ModelAdmin):
    list_display = ("phone", "intent_type", "property_city", "geo_origin", "lead_score", "lead_category_badge", "lead_stage", "created_at")
    list_filter = ("intent_type", "lead_stage", "geo_origin", "property_type", "created_at")
    search_fields = ("name", "email", "phone", "property_city", "geo_origin")
    readonly_fields = ("created_at",)
    ordering = ("-lead_score", "-created_at")
    fieldsets = (
        ("Contact", {
            "fields": ("name", "phone", "email")
        }),
        ("Lead Context", {
            "fields": ("property_city", "property_type", "intent_type", "geo_origin", "lead_stage", "lead_score", "lead_category")
        }),
        ("Qualification", {
            "fields": ("expected_price_range", "preferred_contact_time", "qualification_data", "created_at")
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (
                "name",
                "phone",
                "email",
                "property_city",
                "property_type",
                "intent_type",
                "geo_origin",
                "qualification_data",
                "lead_score",
                "lead_category",
            )
        return self.readonly_fields

    def lead_category_badge(self, obj):
        color = {
            "hot": "#b91c1c",
            "warm": "#b45309",
            "cold": "#475569",
        }.get(obj.lead_category, "#475569")
        return format_html(
            '<span style="font-weight: 700; color: {};">{}</span>',
            color,
            obj.lead_category.upper(),
        )

    lead_category_badge.short_description = "Lead Category"


# --- ADMIN UI CLEANUP ---
# Hide core Django models to keep the admin focused on content and properties
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

try:
    admin.site.unregister(Group)
    admin.site.unregister(User)
    admin.site.unregister(Site)
except admin.sites.NotRegistered:
    pass
