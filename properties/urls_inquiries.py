from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.inquiry_staff_login, name="inquiries_login"),
    path("", views.inquiries_dashboard, name="inquiries_dashboard"),
    path("send-reply/", views.inquiry_send_reply, name="inquiry_send_reply"),
    path("<int:inquiry_id>/status/", views.inquiry_status_update, name="inquiry_status_update"),
    path("<int:inquiry_id>/delete/", views.inquiry_delete, name="inquiry_delete"),
    path("pending-count/", views.inquiry_pending_count, name="inquiry_pending_count"),
]
