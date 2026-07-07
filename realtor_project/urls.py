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
    path('api/v1/realbot/session/init/', chat_views.init_session, name='api_init_session'),
    path('api/v1/realbot/query/', chat_views.send_message, name='api_send_message'),
    path('api/v1/realbot/auth/exchange/', chat_views.exchange_token, name='api_exchange_token'),
    path('api/v1/realbot/health/', chat_views.health_check, name='api_health_check'),
    path('api/v1/realbot/health/live/', chat_views.health_live, name='api_health_live'),
    path('api/v1/realbot/health/ready/', chat_views.health_ready, name='api_health_ready'),
    path('api/v1/realbot/version/', chat_views.version_service, name='api_version_service'),
    path('api/v1/realbot/knowledge/index/', chat_views.knowledge_index, name='api_knowledge_index'),
    path('api/v1/realbot/knowledge/documents/', chat_views.document_index, name='api_document_index'),
    path('api/v1/realbot/rules/', chat_views.rules_list, name='api_rules_list'),
    path('api/v1/realbot/rules/diagnostics/', chat_views.rules_diagnostics, name='api_rules_diagnostics'),
    path('api/v1/realbot/rules/logs/', chat_views.rules_logs, name='api_rules_logs'),
    path('api/v1/realbot/services/', chat_views.services_list, name='api_services_list'),
    path('api/v1/realbot/services/diagnostics/', chat_views.services_diagnostics, name='api_services_diagnostics'),
    # M2.6 — Inquiry Conversation Endpoints
    path('api/v1/realbot/inquiry/initiate/', chat_views.inquiry_initiate, name='api_inquiry_initiate'),
    path('api/v1/realbot/inquiry/status/', chat_views.inquiry_status, name='api_inquiry_status'),
    path('api/v1/realbot/inquiry/cancel/', chat_views.inquiry_cancel, name='api_inquiry_cancel'),
    path('api/v1/realbot/inquiry/diagnostics/', chat_views.inquiry_diagnostics, name='api_inquiry_diagnostics'),
    # M2.7 — Suggestion Interaction & Analytics Endpoints
    path('api/v1/realbot/inquiry/suggestion/click/', chat_views.inquiry_suggestion_click, name='api_inquiry_suggestion_click'),
    path('api/v1/realbot/inquiry/suggestion/analytics/', chat_views.inquiry_suggestion_analytics, name='api_inquiry_suggestion_analytics'),
    # M2.8 — Action Navigation & Analytics Endpoints
    path('api/v1/realbot/inquiry/action/execute/', chat_views.inquiry_action_execute, name='api_inquiry_action_execute'),
    path('api/v1/realbot/inquiry/action/analytics/', chat_views.inquiry_action_analytics, name='api_inquiry_action_analytics'),
    # M2.9 — Rich Response Components & Analytics Endpoints
    path('api/v1/realbot/inquiry/response/components/', chat_views.inquiry_response_components, name='api_inquiry_response_components'),
    path('api/v1/realbot/inquiry/response/compose/', chat_views.inquiry_response_compose, name='api_inquiry_response_compose'),
    path('api/v1/realbot/inquiry/response/analytics/', chat_views.inquiry_response_analytics, name='api_inquiry_response_analytics'),
    # M2.10 — Conversation Memory & Context Endpoints
    path('api/v1/realbot/inquiry/context/get/', chat_views.inquiry_context_get, name='api_inquiry_context_get'),
    path('api/v1/realbot/inquiry/context/update/', chat_views.inquiry_context_update, name='api_inquiry_context_update'),
    path('api/v1/realbot/inquiry/context/switch-topic/', chat_views.inquiry_context_switch_topic, name='api_inquiry_context_switch_topic'),
    path('api/v1/realbot/inquiry/context/analytics/', chat_views.inquiry_context_analytics, name='api_inquiry_context_analytics'),
    # M2.11 — Analytics, Diagnostics & Health Observability Endpoints
    path('api/v1/realbot/inquiry/analytics/event/publish/', chat_views.analytics_event_publish, name='api_analytics_event_publish'),
    path('api/v1/realbot/inquiry/analytics/metrics/', chat_views.analytics_metrics_get, name='api_analytics_metrics_get'),
    path('api/v1/realbot/inquiry/analytics/health/', chat_views.analytics_health_get, name='api_analytics_health_get'),
    path('api/v1/realbot/inquiry/analytics/aggregate/', chat_views.analytics_aggregate_trigger, name='api_analytics_aggregate_trigger'),
    # M2.12 — Administration & Configuration Endpoints
    path('api/v1/realbot/inquiry/config/get/', chat_views.config_get_view, name='api_config_get_view'),
    path('api/v1/realbot/inquiry/config/update/', chat_views.config_update_view, name='api_config_update_view'),
    path('api/v1/realbot/inquiry/config/rollback/', chat_views.config_rollback_view, name='api_config_rollback_view'),
    path('api/v1/realbot/inquiry/config/audit/', chat_views.config_audit_view, name='api_config_audit_view'),
    path('api/v1/realbot/inquiry/config/import/', chat_views.config_import_view, name='api_config_import_view'),
    path('api/v1/realbot/inquiry/config/export/', chat_views.config_export_view, name='api_config_export_view'),
    # M2.13 — Conversation Orchestration Endpoints
    path('api/v1/realbot/inquiry/orchestrator/message/', chat_views.orchestrator_message_view, name='api_orchestrator_message_view'),
    path('api/v1/realbot/inquiry/orchestrator/status/', chat_views.orchestrator_workflow_status_view, name='api_orchestrator_workflow_status_view'),
    path('api/v1/realbot/inquiry/orchestrator/trace/', chat_views.orchestrator_workflow_trace_view, name='api_orchestrator_workflow_trace_view'),
    path('api/v1/realbot/inquiry/orchestrator/analytics/', chat_views.orchestrator_workflow_analytics_view, name='api_orchestrator_workflow_analytics_view'),
    # M2.16 — Propertism Analytics & Customer Insights Endpoints
    path('api/v1/realbot/inquiry/insights/dashboard/', chat_views.insights_dashboard_view, name='api_insights_dashboard_view'),
    path('api/v1/realbot/inquiry/insights/report/', chat_views.insights_report_view, name='api_insights_report_view'),
    path('api/v1/realbot/inquiry/insights/export/', chat_views.insights_export_view, name='api_insights_export_view'),
    path('api/v1/realbot/inquiry/insights/recommendations/', chat_views.insights_recommendations_view, name='api_insights_recommendations_view'),
    path('realbot/', chat_views.realbot_view, name='realbot'),
    path('api/', include('properties.urls')),
    path('api/', include('users.urls')),
    path('api/', include('search.urls')),
    path('api/v1/communications/', include('communications.urls')),
    # Auth routes (must precede catch-all slug routes in content.urls)
    path('contact-test/', uilayers_views.contact, name='contact_test'),
    path('address-test/', uilayers_views.address_test, name='address_test'),
    path('login/', uilayers_views.user_login, name='login'),
    path('register/', uilayers_views.user_register, name='register'),
    path('logout/', uilayers_views.user_logout, name='logout'),
    # Legal Pages
    path('terms/', TemplateView.as_view(template_name='legal/terms.html'), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='legal/privacy.html'), name='privacy'),
    path('disclaimer/', TemplateView.as_view(template_name='legal/disclaimer.html'), name='disclaimer'),
    # Human-readable HTML sitemap (distinct from the XML sitemap for crawlers)
    path('sitemap-guide/', TemplateView.as_view(template_name='legal/sitemap_guide.html'), name='sitemap_guide'),
    
    path('inquiries/', include('properties.urls_inquiries')),
    path('', include('content.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', content_views.robots_txt, name='robots'),
]

# Static and media files - serve in all environments (including production admin)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# SCCB: Serve media files for local storage (fixes 404 errors)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
