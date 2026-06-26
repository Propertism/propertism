import csv
import json

from django.contrib import admin
from django.core.paginator import Paginator
from django.db import models as db_models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import path
from django.utils import timezone

from .models import ContactMessage, Inquiry, InquiryReply, MaintenanceRequest, Property, PropertyPhoto, PropertyType, SupportTicket


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


class InquiryReplyInline(admin.TabularInline):
    model = InquiryReply
    extra = 0
    readonly_fields = ["sent_by", "to_email", "cc", "subject", "body", "sent_at"]
    can_delete = False
    show_change_link = False
    verbose_name = "Sent Reply"
    verbose_name_plural = "Sent Replies"


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    change_list_template = "admin/properties/inquiry/change_list.html"
    readonly_fields = ["created_at", "updated_at"]
    inlines = [InquiryReplyInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "set-status/",
                self.admin_site.admin_view(self.set_status_view),
                name="properties_inquiry_set_status",
            ),
            path(
                "export-csv/",
                self.admin_site.admin_view(self.export_csv_view),
                name="properties_inquiry_export_csv",
            ),
            path(
                "<int:inquiry_id>/delete/",
                self.admin_site.admin_view(self.delete_inquiry_view),
                name="properties_inquiry_delete",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        qs = Inquiry.objects.select_related("property")

        q = request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                db_models.Q(name__icontains=q)
                | db_models.Q(email__icontains=q)
                | db_models.Q(phone__icontains=q)
                | db_models.Q(message__icontains=q)
            )

        status_filter = request.GET.get("status", "")
        if status_filter and status_filter in dict(Inquiry.STATUS_CHOICES):
            qs = qs.filter(status=status_filter)

        year_filter = request.GET.get("year", "")
        month_filter = request.GET.get("month", "")
        if year_filter.isdigit():
            qs = qs.filter(created_at__year=int(year_filter))
            if month_filter.isdigit():
                qs = qs.filter(created_at__month=int(month_filter))

        sort = request.GET.get("sort", "desc")
        qs = qs.order_by("created_at" if sort == "asc" else "-created_at")
        paginator = Paginator(qs, 25)
        page_obj = paginator.get_page(request.GET.get("page", 1))

        all_qs = Inquiry.objects.all()

        # Build year chips from all data
        years = (
            all_qs.dates("created_at", "year", order="DESC")
        )
        months = []
        if year_filter.isdigit():
            months = all_qs.filter(created_at__year=int(year_filter)).dates(
                "created_at", "month", order="ASC"
            )

        context = {
            **self.admin_site.each_context(request),
            "title": "Inquiries",
            "opts": self.model._meta,
            "has_add_permission": self.has_add_permission(request),
            "inquiries": page_obj,
            "paginator": paginator,
            "page_obj": page_obj,
            "stats": {
                "total": all_qs.count(),
                "pending": all_qs.filter(status="pending").count(),
                "contacted": all_qs.filter(status="contacted").count(),
                "closed": all_qs.filter(status="closed").count(),
            },
            "status_choices": Inquiry.STATUS_CHOICES,
            "current_q": q,
            "current_status": status_filter,
            "current_year": year_filter,
            "current_month": month_filter,
            "current_sort": sort,
            "date_years": years,
            "date_months": months,
        }
        return render(request, self.change_list_template, context)

    def set_status_view(self, request):
        if request.method != "POST":
            return JsonResponse({"ok": False, "error": "POST required"}, status=405)
        try:
            data = json.loads(request.body)
            inquiry_id = int(data["id"])
            new_status = data["status"]
            if new_status not in dict(Inquiry.STATUS_CHOICES):
                return JsonResponse({"ok": False, "error": "Invalid status"}, status=400)
            Inquiry.objects.filter(pk=inquiry_id).update(
                status=new_status,
                updated_at=timezone.now(),
            )
            display = dict(Inquiry.STATUS_CHOICES)[new_status]
            return JsonResponse({"ok": True, "status": new_status, "display": display})
        except Exception as exc:
            return JsonResponse({"ok": False, "error": str(exc)}, status=400)

    def delete_inquiry_view(self, request, inquiry_id):
        if request.method != "POST":
            return JsonResponse({"ok": False, "error": "POST required"}, status=405)
        try:
            Inquiry.objects.filter(pk=inquiry_id).delete()
            return JsonResponse({"ok": True})
        except Exception as exc:
            return JsonResponse({"ok": False, "error": str(exc)}, status=400)

    def export_csv_view(self, request):
        qs = Inquiry.objects.select_related("property")
        q = request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                db_models.Q(name__icontains=q)
                | db_models.Q(email__icontains=q)
                | db_models.Q(phone__icontains=q)
            )
        status_filter = request.GET.get("status", "")
        if status_filter and status_filter in dict(Inquiry.STATUS_CHOICES):
            qs = qs.filter(status=status_filter)

        year_filter = request.GET.get("year", "")
        month_filter = request.GET.get("month", "")
        if year_filter.isdigit():
            qs = qs.filter(created_at__year=int(year_filter))
            if month_filter.isdigit():
                qs = qs.filter(created_at__month=int(month_filter))

        timestamp = timezone.now().strftime("%Y%m%d_%H%M")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="inquiries_{timestamp}.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Name", "Email", "Phone", "Property", "Message", "Status", "Submitted"])
        for inq in qs.order_by("-created_at"):
            writer.writerow([
                inq.id,
                inq.name,
                inq.email,
                inq.phone,
                inq.property.title if inq.property else "General",
                inq.message,
                dict(Inquiry.STATUS_CHOICES)[inq.status],
                inq.created_at.strftime("%Y-%m-%d %H:%M"),
            ])
        return response


@admin.register(InquiryReply)
class InquiryReplyAdmin(admin.ModelAdmin):
    list_display = ["inquiry", "to_email", "subject", "sent_by", "sent_at"]
    list_filter = ["sent_at", "sent_by"]
    search_fields = ["to_email", "subject", "body", "inquiry__name"]
    readonly_fields = ["inquiry", "sent_by", "to_email", "cc", "subject", "body", "sent_at"]
    date_hierarchy = "sent_at"

    def has_add_permission(self, request):
        return False  # Replies are created only programmatically

    def has_change_permission(self, request, obj=None):
        return False  # Read-only audit log


# @admin.register(MaintenanceRequest)
# class MaintenanceRequestAdmin(admin.ModelAdmin):
#     list_display = ["title", "property", "user", "priority", "status", "created_at"]
#     list_filter = ["priority", "status", "created_at"]
#     search_fields = ["title", "description", "property__title"]
#     date_hierarchy = "created_at"
#     readonly_fields = ["created_at", "updated_at"]


# @admin.register(SupportTicket)
# class SupportTicketAdmin(admin.ModelAdmin):
#     list_display = ["id", "subject", "user", "priority", "status", "created_at"]
#     list_filter = ["priority", "status", "created_at"]
#     search_fields = ["subject", "description", "user__username"]
#     date_hierarchy = "created_at"
#     readonly_fields = ["created_at", "updated_at"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "subject", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "email", "phone", "subject", "message"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at"]
