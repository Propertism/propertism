from django.urls import path
from . import views

urlpatterns = [
    path('', views.nri_assist, name='nri_assist'),
    path('log-cta/', views.log_cta, name='nri_assist_log_cta'),
]
