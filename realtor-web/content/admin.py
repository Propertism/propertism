from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from .models import (
    CompanyInfo, Statistic, Service, CoreValue, TeamMember,
    ExpertiseArea, BlogPost, Newsletter, ContactInquiry
)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(TabbedTranslationAdmin):
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_eyebrow', 'hero_title', 'hero_description', 'hero_image'),
            'description': 'Homepage hero section content and background image'
        }),
        ('Company Details', {
            'fields': ('company_name', 'tagline', 'about_mission', 'about_description')
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
            'fields': ('email', 'facebook_url', 'twitter_url', 'linkedin_url', 'business_hours')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not CompanyInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('label', 'value')


@admin.register(Service)
class ServiceAdmin(TabbedTranslationAdmin):
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
class CoreValueAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(TeamMember)
class TeamMemberAdmin(TabbedTranslationAdmin):
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
class ExpertiseAreaAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(BlogPost)
class BlogPostAdmin(TabbedTranslationAdmin):
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
            'fields': ('is_published',)
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_date', 'is_active')
    list_filter = ('is_active', 'subscribed_date')
    search_fields = ('email',)
    date_hierarchy = 'subscribed_date'
    readonly_fields = ('subscribed_date',)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'submitted_date', 'is_read')
    list_filter = ('is_read', 'service', 'property_type', 'submitted_date')
    search_fields = ('name', 'email', 'phone', 'message')
    date_hierarchy = 'submitted_date'
    readonly_fields = ('submitted_date',)
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('service', 'property_type', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'notes', 'submitted_date')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ('name', 'email', 'phone', 'service', 'property_type', 'message')
        return self.readonly_fields

