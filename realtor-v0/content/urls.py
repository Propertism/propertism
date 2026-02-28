from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('management/', views.management, name='management'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_post, name='blog_post'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
