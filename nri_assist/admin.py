from django.contrib import admin
from .models import NRIService, NRIAssistEvent


@admin.register(NRIService)
class NRIServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'sort_order', 'created_at']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active', 'sort_order']
    search_fields = ['name', 'description']
    ordering = ['category', 'sort_order']


@admin.register(NRIAssistEvent)
class NRIAssistEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'user', 'service_category', 'ip_address', 'created_at']
    list_filter = ['event_type', 'service_category']
    readonly_fields = ['event_type', 'user', 'service_category', 'metadata', 'ip_address', 'created_at']
    date_hierarchy = 'created_at'
