from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('auth/login/', views.login_api, name='login_api'),
    
    # Web views
    path('agents/', views.agent_list, name='agent_list'),
    path('agents/<int:pk>/', views.agent_detail, name='agent_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-inquiries/', views.my_inquiries, name='my_inquiries'),
    path('my-maintenance/', views.my_maintenance, name='my_maintenance'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('profile/', views.profile, name='profile'),
]
