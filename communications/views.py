from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from communications.models import (
    CommunicationTemplate,
    CommunicationChannel,
    CommunicationRequest,
    CommunicationDelivery,
    CommunicationLog,
    CommunicationRetry,
    CommunicationConfiguration,
    CommunicationType,
)
from communications.serializers import (
    CommunicationTemplateSerializer,
    CommunicationChannelSerializer,
    CommunicationRequestSerializer,
    CommunicationDeliverySerializer,
    CommunicationLogSerializer,
    CommunicationRetrySerializer,
    CommunicationConfigurationSerializer,
    SendAcknowledgementSerializer,
)
from communications.services import AcknowledgementService

class CommunicationTemplateViewSet(viewsets.ModelViewSet):
    queryset = CommunicationTemplate.objects.all().order_by('communication_type__key', 'language')
    serializer_class = CommunicationTemplateSerializer


class CommunicationChannelViewSet(viewsets.ModelViewSet):
    queryset = CommunicationChannel.objects.all().order_by('name')
    serializer_class = CommunicationChannelSerializer

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        channel = self.get_object()
        channel.is_active = not channel.is_active
        channel.save()
        return Response({'status': 'success', 'is_active': channel.is_active})


class CommunicationConfigurationViewSet(viewsets.ModelViewSet):
    queryset = CommunicationConfiguration.objects.all().order_by('key')
    serializer_class = CommunicationConfigurationSerializer


class SendAcknowledgementView(APIView):
    def post(self, request):
        serializer = SendAcknowledgementSerializer(data=request.data)
        if serializer.is_valid():
            req_data = serializer.validated_data
            result_request = AcknowledgementService.send(
                communication_type_key=req_data['communication_type_key'],
                recipient=req_data['recipient'],
                context=req_data['context'],
                channels=req_data['channels'],
                brand_name=req_data.get('brand_name'),
                language_code=req_data.get('language_code', 'en'),
                module=req_data.get('module', 'propertism')
            )
            if result_request:
                return Response(
                    {'status': 'success', 'request_id': str(result_request.id)},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'status': 'error', 'message': 'Failed to process communications request'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommunicationHistoryListView(generics.ListAPIView):
    queryset = CommunicationRequest.objects.all().order_by('-created_at')
    serializer_class = CommunicationRequestSerializer


class CommunicationDeliveryListView(generics.ListAPIView):
    queryset = CommunicationDelivery.objects.all().order_by('-updated_at')
    serializer_class = CommunicationDeliverySerializer


class CommunicationLogListView(generics.ListAPIView):
    queryset = CommunicationLog.objects.all().order_by('-created_at')
    serializer_class = CommunicationLogSerializer


class CommunicationRetryListView(generics.ListAPIView):
    queryset = CommunicationRetry.objects.all().order_by('-scheduled_time')
    serializer_class = CommunicationRetrySerializer


class CommunicationDashboardView(APIView):
    def get(self, request):
        total_requests = CommunicationRequest.objects.count()
        total_deliveries = CommunicationDelivery.objects.count()
        
        status_counts = dict(
            CommunicationDelivery.objects.values_list('status').annotate(total=Count('status'))
        )
        sent_count = status_counts.get('sent', 0)
        failed_count = status_counts.get('failed', 0)
        pending_count = status_counts.get('pending', 0)
        
        success_rate = 0.0
        if total_deliveries > 0:
            success_rate = round((sent_count / total_deliveries) * 100, 2)
            
        pending_retries = CommunicationRetry.objects.filter(status='pending').count()
        
        channel_counts = dict(
            CommunicationDelivery.objects.values_list('channel__key').annotate(total=Count('id'))
        )
        
        return Response({
            'total_requests': total_requests,
            'total_deliveries': total_deliveries,
            'sent': sent_count,
            'failed': failed_count,
            'pending': pending_count,
            'success_rate': success_rate,
            'pending_retries': pending_retries,
            'channel_breakdown': channel_counts,
        })
