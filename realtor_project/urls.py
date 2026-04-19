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
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('properties/', include('properties.urls_web')),
    path('chat/', include('chat.urls')),
    path('api/', include('properties.urls')),
    path('api/', include('users.urls')),
    path('api/', include('search.urls')),
    path('', include('content.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
]

# Static and media files - serve in all environments (including production admin)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files when using local storage (SCCB: always serve if MEDIA_ROOT is set)
# This fixes 404 errors for locally uploaded images in production
if getattr(settings, 'MEDIA_ROOT', None):
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
