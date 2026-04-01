from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('inquiry/', views.create_inquiry, name='create_inquiry'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
]
