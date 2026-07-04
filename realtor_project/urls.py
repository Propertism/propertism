from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.static import serve
from content import views as content_views
from content.sitemaps import StaticViewSitemap, PropertySitemap, BlogSitemap, LandingPageSitemap
from users import views as user_views
from uilayers import views as uilayers_views
from chat import views as chat_views

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'properties': PropertySitemap,
    'blog': BlogSitemap,
    'landing': LandingPageSitemap,
}

# Custom error handlers
handler404 = 'content.views.custom_404'
handler500 = 'content.views.custom_500'

# Main URL patterns (no language prefix)
urlpatterns = [
    path('health/', content_views.health, name='health'),
    path(
        'favicon.ico',
        RedirectView.as_view(url=f'{settings.STATIC_URL}images/propertism-logo-tm.png', permanent=True),
    ),
    path(f'{settings.ADMIN_URL}/send-otp/', content_views.send_otp_view, name='admin_send_otp'),
    path(f'{settings.ADMIN_URL}/verify-otp/', content_views.verify_otp_view, name='admin_verify_otp'),
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    # Google OAuth + allauth
    path('accounts/', include('allauth.urls')),
    # User dashboard (web)
    path('dashboard/', user_views.dashboard, name='dashboard'),
    # NRI Assist module
    path('nri-assist/', include('nri_assist.urls')),
    path('properties/', include('properties.urls_web')),
    path('chat/', include('chat.urls')),
    path('realbot/', chat_views.realbot_view, name='realbot'),
    path('api/', include('properties.urls')),
    path('api/', include('users.urls')),
    path('api/', include('search.urls')),
    path('api/v1/communications/', include('communications.urls')),
    # Auth routes (must precede catch-all slug routes in content.urls)
    path('login/', uilayers_views.user_login, name='login'),
    path('register/', uilayers_views.user_register, name='register'),
    path('logout/', uilayers_views.user_logout, name='logout'),
    # Legal Pages
    path('terms/', TemplateView.as_view(template_name='legal/terms.html'), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='legal/privacy.html'), name='privacy'),
    
    path('inquiries/', include('properties.urls_inquiries')),
    path('', include('content.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', content_views.robots_txt, name='robots'),
]

# Static and media files - serve in all environments (including production admin)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# SCCB: Serve media files for local storage (fixes 404 errors)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
