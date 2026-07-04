from django.contrib import admin
from communications.models import (
    CommunicationType,
    CommunicationBrand,
    CommunicationLanguage,
    CommunicationTemplate,
    CommunicationChannel,
    CommunicationConfiguration,
    CommunicationPreference,
    CommunicationRequest,
    CommunicationDelivery,
    CommunicationLog,
    CommunicationRetry,
)

@admin.register(CommunicationType)
class CommunicationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'description')
    search_fields = ('name', 'key')


@admin.register(CommunicationBrand)
class CommunicationBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_color', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('name',)


@admin.register(CommunicationLanguage)
class CommunicationLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


@admin.register(CommunicationTemplate)
class CommunicationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'communication_type', 'language', 'brand')
    list_filter = ('communication_type', 'language', 'brand')
    search_fields = ('name', 'subject_template')


@admin.register(CommunicationChannel)
class CommunicationChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'key')


@admin.register(CommunicationConfiguration)
class CommunicationConfigurationAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    search_fields = ('key', 'description')


@admin.register(CommunicationPreference)
class CommunicationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'channel', 'is_opted_in', 'updated_at')
    list_filter = ('channel', 'is_opted_in')
    search_fields = ('recipient',)


class CommunicationDeliveryInline(admin.TabularInline):
    model = CommunicationDelivery
    extra = 0
    readonly_fields = ('tracking_reference', 'channel', 'status', 'retry_count')


@admin.register(CommunicationRequest)
class CommunicationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'module', 'recipient', 'template', 'created_at')
    list_filter = ('module', 'created_at')
    search_fields = ('recipient', 'module')
    inlines = [CommunicationDeliveryInline]


class CommunicationLogInline(admin.TabularInline):
    model = CommunicationLog
    extra = 0
    readonly_fields = ('status', 'provider_response', 'created_at')


class CommunicationRetryInline(admin.TabularInline):
    model = CommunicationRetry
    extra = 0
    readonly_fields = ('scheduled_time', 'attempt_number', 'status')


@admin.register(CommunicationDelivery)
class CommunicationDeliveryAdmin(admin.ModelAdmin):
    list_display = ('tracking_reference', 'channel', 'status', 'retry_count', 'delivery_timestamp', 'updated_at')
    list_filter = ('channel', 'status', 'updated_at')
    search_fields = ('tracking_reference', 'request__recipient')
    inlines = [CommunicationLogInline, CommunicationRetryInline]


@admin.register(CommunicationLog)
class CommunicationLogAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('delivery__tracking_reference', 'status')


@admin.register(CommunicationRetry)
class CommunicationRetryAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'scheduled_time', 'attempt_number', 'status', 'created_at')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('delivery__tracking_reference', 'status')
