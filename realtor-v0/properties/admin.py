from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from .models import PropertyType, Property, PropertyPhoto, Inquiry, MaintenanceRequest, SupportTicket, ContactMessage

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 1

@admin.register(Property)
class PropertyAdmin(TabbedTranslationAdmin):
    list_display = ['title', 'property_type', 'price', 'location', 'status', 'created_at']
    list_filter = ['status', 'property_type', 'created_at']
    search_fields = ['title', 'location', 'description']
    inlines = [PropertyPhotoInline]
    date_hierarchy = 'created_at'

@admin.register(PropertyPhoto)
class PropertyPhotoAdmin(admin.ModelAdmin):
    list_display = ['property', 'caption', 'is_primary', 'sort_order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['property__title', 'caption']

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'property', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'property__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'property', 'user', 'priority', 'status', 'created_at']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['title', 'description', 'property__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'user', 'priority', 'status', 'created_at']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['subject', 'description', 'user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
