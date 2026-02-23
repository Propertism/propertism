from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

# Non-i18n URLs (API endpoints)
urlpatterns = [
    path('api/', include('properties.urls')),
    path('api/', include('users.urls')),
    path('api/', include('search.urls')),
]

# i18n URLs (CMS and admin)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('cms/', include('cms.urls')),  # CMS must come before catch-all
    path('', include('content.urls')),
    path('properties/', TemplateView.as_view(template_name='properties/properties_spa.html'), name='properties-spa'),
)

# Static and media files (only in DEBUG mode) - MUST BE LAST
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
