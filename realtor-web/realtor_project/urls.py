from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
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

# Non-i18n URLs (API endpoints, sitemap, robots)
urlpatterns = [
    path('api/', include('properties.urls')),
    path('api/', include('users.urls')),
    path('api/', include('search.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
]

# Static and media files (only in DEBUG mode) - BEFORE i18n patterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# i18n URLs (multi-language support)
urlpatterns += i18n_patterns(
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('', include('content.urls')),
    path('properties/', include('properties.urls_web')),
)
