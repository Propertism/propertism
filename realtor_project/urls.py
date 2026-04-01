from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from content import views as content_views
from content.sitemaps import StaticViewSitemap, PropertySitemap, BlogSitemap

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'properties': PropertySitemap,
    'blog': BlogSitemap,
}

# Custom error handlers
handler404 = 'content.views.custom_404'
handler500 = 'content.views.custom_500'

# Main URL patterns (no language prefix)
urlpatterns = [
    path('health/', content_views.health, name='health'),
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('', include('content.urls')),
    path('properties/', include('properties.urls_web')),
    path('chat/', include('chat.urls')),
    path('api/', include('properties.urls')),
    path('api/', include('users.urls')),
    path('api/', include('search.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
]

# Static and media files for local development.
if settings.DEBUG or getattr(settings, "IS_LOCAL_DEVELOPMENT", False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
