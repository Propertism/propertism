from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('submit/', views.submit_chat_message, name='submit'),
    path('session/init/', views.init_session, name='init_session'),
    path('query/', views.send_message, name='send_message'),
    path('auth/exchange/', views.exchange_token, name='exchange_token'),
    path('health/', views.health_check, name='health_check'),
    path('health/live/', views.health_live, name='health_live'),
    path('health/ready/', views.health_ready, name='health_ready'),
    path('version/', views.version_service, name='version_service'),
    path('knowledge/index/', views.knowledge_index, name='knowledge_index'),
    path('knowledge/documents/', views.document_index, name='document_index'),
    path('rules/', views.rules_list, name='rules_list'),
    path('rules/diagnostics/', views.rules_diagnostics, name='rules_diagnostics'),
    path('rules/logs/', views.rules_logs, name='rules_logs'),
    path('services/', views.services_list, name='services_list'),
    path('services/diagnostics/', views.services_diagnostics, name='services_diagnostics'),
    # M2.6 — Inquiry Conversation Endpoints
    path('inquiry/initiate/', views.inquiry_initiate, name='inquiry_initiate'),
    path('inquiry/status/', views.inquiry_status, name='inquiry_status'),
    path('inquiry/cancel/', views.inquiry_cancel, name='inquiry_cancel'),
    path('inquiry/diagnostics/', views.inquiry_diagnostics, name='inquiry_diagnostics'),
    # M2.7 — Suggestion Interaction & Analytics Endpoints
    path('inquiry/suggestion/click/', views.inquiry_suggestion_click, name='inquiry_suggestion_click'),
    path('inquiry/suggestion/analytics/', views.inquiry_suggestion_analytics, name='inquiry_suggestion_analytics'),
    # M2.8 — Action Navigation & Analytics Endpoints
    path('inquiry/action/execute/', views.inquiry_action_execute, name='inquiry_action_execute'),
    path('inquiry/action/analytics/', views.inquiry_action_analytics, name='inquiry_action_analytics'),
    # M2.9 — Rich Response Components & Analytics Endpoints
    path('inquiry/response/components/', views.inquiry_response_components, name='inquiry_response_components'),
    path('inquiry/response/compose/', views.inquiry_response_compose, name='inquiry_response_compose'),
    path('inquiry/response/analytics/', views.inquiry_response_analytics, name='inquiry_response_analytics'),
    # M2.10 — Conversation Memory & Context Endpoints
    path('inquiry/context/get/', views.inquiry_context_get, name='inquiry_context_get'),
    path('inquiry/context/update/', views.inquiry_context_update, name='inquiry_context_update'),
    path('inquiry/context/switch-topic/', views.inquiry_context_switch_topic, name='inquiry_context_switch_topic'),
    path('inquiry/context/analytics/', views.inquiry_context_analytics, name='inquiry_context_analytics'),
    # M2.11 — Analytics, Diagnostics & Health Observability Endpoints
    path('inquiry/analytics/event/publish/', views.analytics_event_publish, name='analytics_event_publish'),
    path('inquiry/analytics/metrics/', views.analytics_metrics_get, name='analytics_metrics_get'),
    path('inquiry/analytics/health/', views.analytics_health_get, name='analytics_health_get'),
    path('inquiry/analytics/aggregate/', views.analytics_aggregate_trigger, name='analytics_aggregate_trigger'),
    # M2.12 — Administration & Configuration Endpoints
    path('inquiry/config/get/', views.config_get_view, name='config_get_view'),
    path('inquiry/config/update/', views.config_update_view, name='config_update_view'),
    path('inquiry/config/rollback/', views.config_rollback_view, name='config_rollback_view'),
    path('inquiry/config/audit/', views.config_audit_view, name='config_audit_view'),
    path('inquiry/config/import/', views.config_import_view, name='config_import_view'),
    path('inquiry/config/export/', views.config_export_view, name='config_export_view'),
    # M2.13 — Conversation Orchestration Endpoints
    path('inquiry/orchestrator/message/', views.orchestrator_message_view, name='orchestrator_message_view'),
    path('inquiry/orchestrator/status/', views.orchestrator_workflow_status_view, name='orchestrator_workflow_status_view'),
    path('inquiry/orchestrator/trace/', views.orchestrator_workflow_trace_view, name='orchestrator_workflow_trace_view'),
    path('inquiry/orchestrator/analytics/', views.orchestrator_workflow_analytics_view, name='orchestrator_workflow_analytics_view'),
    # M2.14 — Security, Authorization & Platform Governance Endpoints
    path('inquiry/security/events/', views.security_events_view, name='security_events_view'),
    path('inquiry/security/policies/', views.security_policies_view, name='security_policies_view'),
    path('inquiry/security/validate/', views.security_validate_view, name='security_validate_view'),
    path('inquiry/security/analytics/', views.security_analytics_view, name='security_analytics_view'),
    path('inquiry/security/governance/', views.security_governance_view, name='security_governance_view'),
    # M2.15 — Knowledge Administration Endpoints
    path('inquiry/knowledge/admin/list/', views.knowledge_admin_list_view, name='knowledge_admin_list_view'),
    path('inquiry/knowledge/admin/update/', views.knowledge_admin_update_view, name='knowledge_admin_update_view'),
    path('inquiry/knowledge/admin/publish/', views.knowledge_admin_publish_view, name='knowledge_admin_publish_view'),
    path('inquiry/knowledge/admin/rollback/', views.knowledge_admin_rollback_view, name='knowledge_admin_rollback_view'),
    path('inquiry/knowledge/admin/reindex/', views.knowledge_admin_reindex_view, name='knowledge_admin_reindex_view'),
    path('inquiry/knowledge/admin/analytics/', views.knowledge_admin_analytics_view, name='knowledge_admin_analytics_view'),
    # Website Conversational Knowledge Extraction Endpoints
    path('inquiry/knowledge/extraction/trigger/', views.knowledge_extraction_trigger_view, name='knowledge_extraction_trigger'),
    path('inquiry/knowledge/extraction/candidates/', views.knowledge_extraction_candidates_view, name='knowledge_extraction_candidates'),
    path('inquiry/knowledge/extraction/approve/', views.knowledge_extraction_approve_view, name='knowledge_extraction_approve'),
    path('inquiry/knowledge/extraction/reject/', views.knowledge_extraction_reject_view, name='knowledge_extraction_reject'),
    path('inquiry/knowledge/extraction/update/', views.knowledge_extraction_update_view, name='knowledge_extraction_update'),
    # M2.16 — Propertism Analytics & Customer Insights Endpoints
    path('inquiry/insights/dashboard/', views.insights_dashboard_view, name='insights_dashboard_view'),
    path('inquiry/insights/report/', views.insights_report_view, name='insights_report_view'),
    path('inquiry/insights/export/', views.insights_export_view, name='insights_export_view'),
    path('inquiry/insights/recommendations/', views.insights_recommendations_view, name='insights_recommendations_view'),
    # M2.17 — Human Handover & Conversation Closure Endpoints
    path('inquiry/handover/request/', views.handover_request, name='handover_request'),
    path('inquiry/handover/status/', views.handover_status, name='handover_status'),
    path('inquiry/handover/advisor/waiting/', views.advisor_waiting_list, name='advisor_waiting_list'),
    path('inquiry/handover/advisor/accept/', views.advisor_accept, name='advisor_accept'),
    path('inquiry/handover/advisor/message/', views.advisor_message, name='advisor_message'),
    path('inquiry/handover/advisor/close/', views.advisor_close, name='advisor_close'),
    path('inquiry/handover/customer/end/', views.customer_end_conversation, name='customer_end_conversation'),
    path('inquiry/handover/transcript/', views.conversation_transcript, name='conversation_transcript'),
    path('inquiry/handover/archives/', views.conversation_archive_list, name='conversation_archive_list'),
    path('inquiry/handover/diagnostics/', views.handover_diagnostics, name='handover_diagnostics'),
    path('inquiry/handover/analytics/', views.handover_analytics, name='handover_analytics'),
]
