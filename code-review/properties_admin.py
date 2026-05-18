import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from .models import ContactMessage, Inquiry, MaintenanceRequest, Property, PropertyPhoto, PropertyType, SupportTicket


def export_inquiries_csv(modeladmin, request, queryset):
    timestamp = timezone.now().strftime("%Y%m%d_%H%M")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="inquiries_{timestamp}.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Name", "Email", "Phone", "Property", "Message", "Status", "Submitted"])

    for inquiry in queryset.select_related("property"):
        writer.writerow([
            inquiry.id,
            inquiry.name,
            inquiry.email,
            inquiry.phone,
            inquiry.property.title if inquiry.property else "General",
            inquiry.message,
            inquiry.get_status_display(),
            inquiry.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    return response

export_inquiries_csv.short_description = "Export selected inquiries to CSV"


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["title", "property_type", "formatted_price", "currency", "location", "status", "created_at"]
    list_filter = ["currency", "status", "property_type", "created_at"]
    search_fields = ["title", "location", "description"]
    inlines = [PropertyPhotoInline]
    date_hierarchy = "created_at"

    @admin.display(description="Price")
    def formatted_price(self, obj):
        return obj.formatted_price


@admin.register(PropertyPhoto)
class PropertyPhotoAdmin(admin.ModelAdmin):
    list_display = ["property", "caption", "is_primary", "sort_order", "created_at"]
    list_filter = ["is_primary", "created_at"]
    search_fields = ["property__title", "caption"]


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "property", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "email", "phone", "property__title"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]
    actions = [export_inquiries_csv]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "subject", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "email", "phone", "subject", "message"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at"]
