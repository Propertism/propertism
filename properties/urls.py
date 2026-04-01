from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('properties/', views.property_list_api, name='property_list_api'),
    path('properties/<int:pk>/', views.property_detail_api, name='property_detail_api'),
]
