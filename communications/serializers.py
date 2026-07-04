from rest_framework import serializers
from communications.models import (
    CommunicationType,
    CommunicationBrand,
    CommunicationLanguage,
    CommunicationTemplate,
    CommunicationChannel,
    CommunicationRequest,
    CommunicationDelivery,
    CommunicationLog,
    CommunicationRetry,
    CommunicationConfiguration,
)

class CommunicationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationType
        fields = '__all__'


class CommunicationBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationBrand
        fields = '__all__'


class CommunicationLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationLanguage
        fields = '__all__'


class CommunicationTemplateSerializer(serializers.ModelSerializer):
    language_code = serializers.CharField(source='language.code', read_only=True)
    communication_type_key = serializers.CharField(source='communication_type.key', read_only=True)
    class Meta:
        model = CommunicationTemplate
        fields = '__all__'


class CommunicationChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationChannel
        fields = '__all__'


class CommunicationConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationConfiguration
        fields = '__all__'


class CommunicationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationRequest
        fields = '__all__'


class CommunicationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationLog
        fields = '__all__'


class CommunicationRetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationRetry
        fields = '__all__'


class CommunicationDeliverySerializer(serializers.ModelSerializer):
    logs = CommunicationLogSerializer(many=True, read_only=True)
    retries = CommunicationRetrySerializer(many=True, read_only=True)
    recipient = serializers.CharField(source='request.recipient', read_only=True)
    module = serializers.CharField(source='request.module', read_only=True)
    class Meta:
        model = CommunicationDelivery
        fields = '__all__'


class SendAcknowledgementSerializer(serializers.Serializer):
    communication_type_key = serializers.CharField(max_length=100)
    recipient = serializers.CharField(max_length=255)
    context = serializers.JSONField(default=dict)
    channels = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=None
    )
    brand_name = serializers.CharField(max_length=100, required=False, default=None)
    language_code = serializers.CharField(max_length=10, required=False, default='en')
    module = serializers.CharField(max_length=100, required=False, default='propertism')
