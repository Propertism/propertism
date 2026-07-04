from django.urls import path, include
from rest_framework.routers import DefaultRouter
from communications.views import (
    CommunicationTemplateViewSet,
    CommunicationChannelViewSet,
    CommunicationConfigurationViewSet,
    SendAcknowledgementView,
    CommunicationHistoryListView,
    CommunicationDeliveryListView,
    CommunicationLogListView,
    CommunicationRetryListView,
    CommunicationDashboardView,
)

router = DefaultRouter()
router.register(r'templates', CommunicationTemplateViewSet, basename='templates')
router.register(r'channels', CommunicationChannelViewSet, basename='channels')
router.register(r'configuration', CommunicationConfigurationViewSet, basename='configuration')

urlpatterns = [
    path('', include(router.urls)),
    path('send/', SendAcknowledgementView.as_view(), name='communication_send'),
    path('history/', CommunicationHistoryListView.as_view(), name='communication_history'),
    path('deliveries/', CommunicationDeliveryListView.as_view(), name='communication_deliveries'),
    path('logs/', CommunicationLogListView.as_view(), name='communication_logs'),
    path('retries/', CommunicationRetryListView.as_view(), name='communication_retries'),
    path('dashboard/', CommunicationDashboardView.as_view(), name='communication_dashboard'),
]
