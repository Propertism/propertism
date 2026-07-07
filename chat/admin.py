from django.contrib import admin
from properties.models import ContactMessage

# Chat messages are now managed through ContactMessage in properties app
# No need to register here as it's already registered in properties/admin.py


# ── M2.6 Inquiry Conversation Admin ──────────────────────────────────────
# ... (existing content remains unchanged) ...

# ── M2.15 Knowledge Administration Admin ───────────────────────────────────────

from chat.models import KnowledgeVersionHistory, KnowledgeLifecycleAuditLog, KnowledgeArticle, KnowledgeDocument


@admin.register(KnowledgeVersionHistory)
class KnowledgeVersionHistoryAdmin(admin.ModelAdmin):
    """
    M2.15 — Admin panel for knowledge version histories.
    """
    list_display = ['version_id', 'version', 'title', 'created_by', 'created_at']
    list_filter = ['created_by', 'created_at']
    search_fields = ['version_id', 'title', 'created_by']
    readonly_fields = [
        'version_id', 'article', 'document', 'version', 'title', 'summary',
        'main_content', 'keywords', 'tags', 'search_weight', 'created_by', 'created_at'
    ]
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(KnowledgeLifecycleAuditLog)
class KnowledgeLifecycleAuditLogAdmin(admin.ModelAdmin):
    """
    M2.15 — Admin panel for knowledge lifecycle audit logs.
    """
    list_display = ['audit_id', 'action', 'performed_by', 'article_id', 'doc_id', 'created_at']
    list_filter = ['action', 'performed_by', 'created_at']
    search_fields = ['audit_id', 'action', 'performed_by', 'article_id', 'doc_id']
    readonly_fields = ['audit_id', 'article_id', 'doc_id', 'action', 'performed_by', 'details', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Knowledge Article and Document Admin
@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = ('knowledge_id', 'page_title', 'status', 'version', 'quality_score', 'usage_count', 'modified_by')
    list_filter = ('status', 'source_type', 'category', 'language')
    search_fields = ('knowledge_id', 'page_title', 'keywords', 'summary')
    readonly_fields = ('knowledge_id', 'indexed_at')
    ordering = ('-indexed_at',)


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_id', 'title', 'status', 'version', 'quality_score', 'usage_count', 'modified_by')
    list_filter = ('status', 'source_type', 'category', 'language')
    search_fields = ('doc_id', 'title', 'tags', 'doc_slug')
    readonly_fields = ('doc_id', 'indexed_at', 'created_at')
    ordering = ('-indexed_at',)


# ── M2.17 Human Handover & Conversation Closure Admin ─────────────────────────

from chat.models import (
    HandoverRequest, AdvisorProfile, AdvisorMessage,
    ConversationArchive, TranscriptRecord, HandoverAnalytics, HandoverAuditLog,
)


@admin.register(HandoverRequest)
class HandoverRequestAdmin(admin.ModelAdmin):
    """
    M2.17 — Admin panel for handover requests.
    """
    list_display = ['handover_id', 'session', 'customer_name', 'status', 'assigned_advisor', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['handover_id', 'customer_name', 'customer_email']
    readonly_fields = ['handover_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(AdvisorProfile)
class AdvisorProfileAdmin(admin.ModelAdmin):
    """
    M2.17 — Admin panel for advisor profiles.
    """
    list_display = ['advisor_id', 'display_name', 'status', 'is_active', 'active_chat_count', 'max_concurrent_chats']
    list_filter = ['status', 'is_active']
    search_fields = ['advisor_id', 'display_name', 'email']
    readonly_fields = ['advisor_id']
    ordering = ['display_name']


@admin.register(AdvisorMessage)
class AdvisorMessageAdmin(admin.ModelAdmin):
    """
    M2.17 — Admin panel for advisor messages.
    """
    list_display = ['message_id', 'sender_type', 'sender_name', 'handover', 'created_at']
    list_filter = ['sender_type', 'created_at']
    search_fields = ['message_id', 'sender_name', 'content']
    readonly_fields = ['message_id', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ConversationArchive)
class ConversationArchiveAdmin(admin.ModelAdmin):
    """
    M2.17 — Admin panel for conversation archives.
    """
    list_display = ['archive_id', 'handover', 'created_at']
    list_filter = ['created_at']
    search_fields = ['archive_id']
    readonly_fields = ['archive_id', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(TranscriptRecord)
class TranscriptRecordAdmin(admin.ModelAdmin):
    """
    M2.17 — Admin panel for transcript records.
    """
    list_display = ['transcript_id', 'archive', 'sender', 'message_type', 'sequence', 'created_at']
    list_filter = ['message_type', 'created_at']
    search_fields = ['transcript_id', 'sender', 'message']
    readonly_fields = ['transcript_id', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(HandoverAnalytics)
class HandoverAnalyticsAdmin(admin.ModelAdmin):
    """
    M2.17 — Admin panel for handover analytics snapshots.
    """
    list_display = ['analytics_id', 'handover', 'wait_duration_seconds', 'handover_duration_seconds', 'message_count', 'customer_satisfaction']
    list_filter = ['created_at']
    readonly_fields = ['analytics_id', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(HandoverAuditLog)
class HandoverAuditLogAdmin(admin.ModelAdmin):
    """
    M2.17 — Admin panel for handover audit logs.
    """
    list_display = ['audit_id', 'handover', 'action', 'performed_by', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['audit_id', 'action', 'performed_by']
    readonly_fields = ['audit_id', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

