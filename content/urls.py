from django.urls import path
from . import views
from .views_landing import landing_page, city_hub, nri_landing_page

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('management/', views.management, name='management'),
    path('management/<slug:slug>/', views.team_member_detail, name='team_member_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_post, name='blog_post'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('api/landing-lead/', views.landing_lead_api, name='landing_lead_api'),
    path('api/landing-lead/followup/', views.landing_lead_followup_api, name='landing_lead_followup_api'),
    
    # SEO Landing Pages
    # SEO Landing Pages (Primary NRI routing first to avoid pattern overlapping)
    path('<slug:nri_location_slug>/<slug:geo_slug>/', nri_landing_page, name='nri_landing_page'),
    path('<slug:city_slug>/<slug:intent_slug>/', landing_page, name='landing_page'),
    path('<slug:city_slug>/', city_hub, name='city_hub'),
]
