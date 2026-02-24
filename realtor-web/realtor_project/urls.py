from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Non-i18n URLs (API endpoints)
urlpatterns = [
    path('api/', include('properties.urls')),
    path('api/', include('users.urls')),
    path('api/', include('search.urls')),
]

# Static and media files (only in DEBUG mode) - BEFORE i18n patterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# i18n URLs (multi-language support)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('content.urls')),
    path('properties/', include('properties.urls_web')),
)
