import uuid
import re
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


# ── Shared choice lists ───────────────────────────────────────────────────────

SOURCE_TYPE_CHOICES = [
    ('Website',      'Website'),
    ('Markdown',     'Markdown'),
    ('Policy',       'Policy'),
    ('FAQ',          'FAQ'),
    ('Terms',        'Terms & Conditions'),
    ('FeeStructure', 'Fee Structure'),
]

CATEGORY_CHOICES = [
    ('Service',  'Service'),
    ('FAQ',      'FAQ'),
    ('Blog',     'Blog'),
    ('NRI',      'NRI'),
    ('About',    'About'),
    ('Contact',  'Contact'),
    ('Property', 'Property'),
    ('General',  'General'),
]

PUBLISHED_STATUS_CHOICES = [
    ('published', 'Published'),
    ('draft',     'Draft'),
    ('hidden',    'Hidden'),
]

KNOWLEDGE_STATE_CHOICES = [
    ('draft',      'Draft'),
    ('review',     'Review'),
    ('approved',   'Approved'),
    ('published',  'Published'),
    ('archived',   'Archived'),
    ('deprecated', 'Deprecated'),
]

KNOWLEDGE_ACTION_CHOICES = [
    ('registered',  'Registered'),
    ('edited',      'Edited'),
    ('archived',    'Archived'),
    ('published',   'Published'),
    ('unpublished', 'Unpublished'),
    ('cloned',      'Cloned'),
    ('versioned',    'Versioned'),
    ('rollback',     'Rollback'),
    ('imported',     'Imported'),
    ('exported',     'Exported'),
    ('reindexed',    'Reindexed'),
    ('validated',    'Validated'),
]


class RealBotSession(models.Model):
    """Tracks an active realBOT chat session."""
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='realbot_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"realBOT Session {self.session_id} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class RealBotMessage(models.Model):
    """Persists messages for multi-turn conversational history."""
    SENDER_CHOICES = (
        ('user', 'Client Consultant'),
        ('assistant', 'realBOT Advisor'),
    )
    session = models.ForeignKey(RealBotSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=15, choices=SENDER_CHOICES)
    text = models.TextField()
    metadata = models.JSONField(null=True, blank=True, help_text="Stores chips, property cards, comparison tables, or citations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.upper()}: {self.text[:40]}"


class KnowledgeArticle(models.Model):
    """
    Unified knowledge record for all realBOT knowledge sources.
    source_type='Website' for M2.2 website content.
    source_type='Terms'|'Policy'|'FeeStructure'|'Markdown'|'FAQ' for M2.3 internal documents.

    knowledge_id is a stable, immutable human-readable identifier (KA000001).
    Generated once on creation; never changes even if the article is re-indexed.
    """

    # ── Stable permanent identifier ───────────────────────────────────────────
    knowledge_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable identifier e.g. KA000001. Auto-generated on creation.",
    )

    # ── Content fields ────────────────────────────────────────────────────────
    page_title = models.CharField(max_length=500)
    url = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='General')
    language = models.CharField(max_length=10, default='en')
    keywords = models.TextField(blank=True, help_text="Space or comma-separated keyword terms")
    summary = models.TextField(blank=True)
    main_content = models.TextField(blank=True)
    published_status = models.CharField(max_length=20, choices=PUBLISHED_STATUS_CHOICES, default='published')
    search_weight = models.FloatField(default=1.0, help_text="Multiplier applied during relevance scoring")
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPE_CHOICES, default='Website')
    source_ref = models.CharField(max_length=200, unique=True, help_text="e.g., Website:service:property-management")
    indexed_at = models.DateTimeField(auto_now=True)

    # ── M2.15 Lifecycle Administration Fields ──────────────────────────────────
    tags = models.TextField(blank=True, help_text="Comma-separated tags for filtering")
    version = models.PositiveIntegerField(default=1, help_text="Increments on modification")
    status = models.CharField(max_length=20, choices=KNOWLEDGE_STATE_CHOICES, default='published')
    published_date = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.CharField(max_length=100, default='admin')
    usage_count = models.PositiveIntegerField(default=0)
    quality_score = models.FloatField(default=100.0)

    class Meta:
        ordering = ['-search_weight', 'page_title']
        verbose_name = "Knowledge Article"
        verbose_name_plural = "Knowledge Articles"
        indexes = [
            models.Index(fields=['source_type', 'category']),
            models.Index(fields=['published_status']),
        ]

    def save(self, *args, **kwargs):
        """Auto-generate knowledge_id on first save. Immutable thereafter."""
        if not self.knowledge_id:
            self.knowledge_id = self._generate_knowledge_id()
        self.last_modified = timezone.now()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_knowledge_id(cls):
        """
        Generate next sequential KA ID in format KA000001.
        Uses DB aggregate; safe under concurrent writes.
        """
        from django.db.models import Max
        last = cls.objects.filter(
            knowledge_id__regex=r'^KA\d{6}$'
        ).aggregate(max_id=Max('knowledge_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"KA{seq:06d}"

    def __str__(self):
        return f"[{self.knowledge_id}] [{self.source_type}:{self.category}] {self.page_title}"


class KnowledgeDocument(models.Model):
    """
    M2.3 — Tracks a single internal business document file.
    Each document's sections are indexed as KnowledgeArticle records via:
        source_ref = '{source_type}:{doc_slug}:{section_slug}'

    doc_id is stable and immutable (DOC000001).
    version increments on every content change detected via SHA-256 content_hash.
    """

    # ── Stable permanent identifier ───────────────────────────────────────────
    doc_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable document identifier e.g. DOC000001.",
    )

    # ── Document metadata ─────────────────────────────────────────────────────
    title = models.CharField(max_length=300)
    doc_slug = models.SlugField(
        max_length=200, unique=True,
        help_text="URL-safe document identifier e.g. terms-and-conditions",
    )
    file_path = models.CharField(
        max_length=500,
        help_text="Filename relative to chat/knowledge_docs/ e.g. terms-and-conditions.md",
    )
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPE_CHOICES, default='Markdown')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='General')
    language = models.CharField(max_length=10, default='en')
    tags = models.TextField(blank=True, help_text="Comma-separated tags for filtering")
    version = models.PositiveIntegerField(
        default=1,
        help_text="Increments each time file content changes",
    )
    content_hash = models.CharField(
        max_length=64, blank=True,
        help_text="SHA-256 of file content for change detection",
    )
    published_status = models.CharField(
        max_length=20, choices=PUBLISHED_STATUS_CHOICES, default='published',
    )
    section_count = models.IntegerField(
        default=0,
        help_text="Number of KnowledgeArticle sections currently indexed",
    )
    indexed_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ── M2.15 Lifecycle Administration Fields ──────────────────────────────────
    summary = models.TextField(blank=True)
    keywords = models.TextField(blank=True, help_text="Space or comma-separated keyword terms")
    search_weight = models.FloatField(default=1.0, help_text="Multiplier applied during relevance scoring")
    status = models.CharField(max_length=20, choices=KNOWLEDGE_STATE_CHOICES, default='published')
    published_date = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.CharField(max_length=100, default='admin')
    usage_count = models.PositiveIntegerField(default=0)
    quality_score = models.FloatField(default=100.0)

    class Meta:
        ordering = ['source_type', 'title']
        verbose_name = "Knowledge Document"
        verbose_name_plural = "Knowledge Documents"

    def save(self, *args, **kwargs):
        """Auto-generate doc_id on first save. Immutable thereafter."""
        if not self.doc_id:
            self.doc_id = self._generate_doc_id()
        self.last_modified = timezone.now()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_doc_id(cls):
        """Generate next sequential DOC ID in format DOC000001."""
        from django.db.models import Max
        last = cls.objects.filter(
            doc_id__regex=r'^DOC\d{6}$'
        ).aggregate(max_id=Max('doc_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"DOC{seq:06d}"

    def is_changed(self, new_hash: str) -> bool:
        """Returns True if document content has changed since last index."""
        return self.content_hash != new_hash

    def __str__(self):
        return f"[{self.doc_id}] {self.title} v{self.version} ({self.source_type})"


class ExtractedKnowledgeCandidate(models.Model):
    """
    SCCB-PROP-RBOT-KNOWLEDGE-WEBSITE-QA-EXTRACTION-001
    Tracks structured conversational Q&A records generated from website components.
    Candidates must be reviewed and approved by administrators before publication.
    """
    candidate_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, sequential identifier e.g. KC000001.",
    )
    entity_type = models.CharField(max_length=50)
    entity_name = models.CharField(max_length=200)
    primary_question = models.CharField(max_length=500)
    alternative_questions = models.TextField(blank=True, help_text="Comma/newline separated or JSON list of alternative questions")
    canonical_answer = models.TextField()
    keywords = models.TextField(blank=True)
    synonyms = models.TextField(blank=True)
    source_url = models.CharField(max_length=1000, blank=True)
    source_section = models.CharField(max_length=200, blank=True)
    search_weight = models.FloatField(default=1.0)
    language = models.CharField(max_length=10, default='en')
    
    CLASSIFICATION_CHOICES = [
        ('existing_no_action', 'Existing Knowledge (No Action)'),
        ('existing_update', 'Existing Knowledge (Update Recommended)'),
        ('new_candidate', 'New Knowledge Candidate'),
        ('duplicate', 'Duplicate Candidate'),
        ('review_required', 'Administrator Review Required'),
    ]
    classification = models.CharField(
        max_length=30, choices=CLASSIFICATION_CHOICES, default='new_candidate'
    )
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='draft'
    )
    
    matched_article = models.ForeignKey(
        'KnowledgeArticle', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='candidates'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'candidate_id']
        verbose_name = "Extracted Knowledge Candidate"
        verbose_name_plural = "Extracted Knowledge Candidates"

    def save(self, *args, **kwargs):
        if not self.candidate_id:
            self.candidate_id = self._generate_candidate_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_candidate_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            candidate_id__regex=r'^KC\d{6}$'
        ).aggregate(max_id=Max('candidate_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"KC{seq:06d}"

    def __str__(self):
        return f"[{self.candidate_id}] [{self.entity_type}] {self.primary_question}"


# -- M2.4 Rule Engine & Intent Routing -----------------------------------------

INTENT_CHOICES = [
    ('greeting',            'Greeting'),
    ('goodbye',             'Goodbye'),
    ('general_information', 'General Information'),
    ('about_propertism',    'About Propertism'),
    ('contact_information', 'Contact Information'),
    ('office_location',     'Office Location'),
    ('business_hours',      'Business Hours'),
    ('buy_property',        'Buy Property'),
    ('sell_property',       'Sell Property'),
    ('rental_income',       'Rental Income Management'),
    ('land_plot',           'Land / Plot Services'),
    ('property_search',     'Property Search'),
    ('property_viewing',    'Property Viewing'),
    ('nri_assist',          'NRI Assist'),
    ('resource_hub',        'Resource Hub'),
    ('useful_links',        'Useful Links'),
    ('faq',                 'FAQ'),
    ('terms_conditions',    'Terms and Conditions'),
    ('fee_structure',       'Service Fee Structure'),
    ('patta_chitta',        'Patta / Chitta'),
    ('encumbrance_search',  'Encumbrance Search'),
    ('gcc_property_tax',    'GCC Property Tax'),
    ('whatsapp',            'WhatsApp'),
    ('phone_call',          'Phone Call'),
    ('google_maps',         'Google Maps'),
    ('linkedin',            'LinkedIn'),
    ('inquiry_creation',    'Inquiry Creation'),
    ('human_assistance',    'Human Assistance'),
    ('unknown_intent',      'Unknown Intent'),
]

RULE_CATEGORY_CHOICES = [
    ('conversation', 'Conversation'),
    ('general',      'General'),
    ('contact',      'Contact'),
    ('property',     'Property'),
    ('nri',          'NRI'),
    ('resources',    'Resources'),
    ('faq',          'FAQ'),
    ('legal',        'Legal'),
    ('financial',    'Financial'),
    ('action',       'Action'),
    ('inquiry',      'Inquiry'),
    ('escalation',   'Escalation'),
    ('fallback',     'Fallback'),
    ('unknown',       'Unknown'),
]

ACTION_TYPE_CHOICES = [
    ('knowledge_response', 'Return Knowledge Response'),
    ('service_card',       'Return Service Card'),
    ('navigation_card',    'Return Navigation Card'),
    ('contact_card',       'Return Contact Card'),
    ('inquiry_workflow',   'Launch Inquiry Workflow'),
    ('external_link',      'Open External Link'),
    ('google_maps',        'Open Google Maps'),
    ('whatsapp',           'Open WhatsApp'),
    ('phone_call',         'Initiate Phone Call'),
    ('related_services',   'Suggest Related Services'),
    ('clarification',      'Request Clarification'),
    ('fallback_response',  'Return Fallback Response'),
    ('greeting_response',  'Return Greeting Response'),
    ('farewell_response',  'Return Farewell Response'),
]

OUTCOME_CHOICES = [
    ('resolved',      'Resolved'),
    ('clarification', 'Clarification'),
    ('fallback',      'Fallback'),
    ('unknown',       'Unknown'),
]


class BusinessRule(models.Model):
    # M2.4: Deterministic business rule for intent classification.
    # rule_id is stable and immutable (RBR000001).
    # Rules are configuration-driven; loaded via seed_rules management command.
    rule_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable immutable identifier e.g. RBR000001.",
    )
    name = models.CharField(max_length=200)
    intent = models.CharField(max_length=50, choices=INTENT_CHOICES, db_index=True)
    category = models.CharField(max_length=30, choices=RULE_CATEGORY_CHOICES, default='general')
    priority = models.PositiveIntegerField(
        default=50,
        help_text="Lower = higher priority. 1=highest, 99=catch-all fallback.",
    )
    positive_keywords = models.TextField(blank=True,
        help_text="Comma-separated keywords that raise confidence when matched.")
    negative_keywords = models.TextField(blank=True,
        help_text="Comma-separated keywords that lower confidence when matched.")
    phrase_patterns = models.TextField(blank=True,
        help_text="Comma-separated exact multi-word phrases (weighted 3x over keywords).")
    keyword_weight = models.FloatField(default=1.0)
    min_confidence = models.FloatField(default=0.4)
    action_type = models.CharField(max_length=30, choices=ACTION_TYPE_CHOICES)
    action_config = models.JSONField(default=dict)
    is_enabled = models.BooleanField(default=True)
    version = models.PositiveIntegerField(default=1)
    allow_chain = models.BooleanField(default=False)
    clarification_question = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', 'name']
        verbose_name = "Business Rule"
        verbose_name_plural = "Business Rules"
        indexes = [
            models.Index(fields=['intent']),
            models.Index(fields=['is_enabled', 'priority']),
        ]

    def save(self, *args, **kwargs):
        if not self.rule_id:
            self.rule_id = self._generate_rule_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_rule_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            rule_id__regex=r'^RBR\d{6}$'
        ).aggregate(max_id=Max('rule_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"RBR{seq:06d}"

    def get_positive_keyword_list(self):
        return [k.strip().lower() for k in self.positive_keywords.split(',') if k.strip()]

    def get_negative_keyword_list(self):
        return [k.strip().lower() for k in self.negative_keywords.split(',') if k.strip()]

    def get_phrase_pattern_list(self):
        return [p.strip().lower() for p in self.phrase_patterns.split(',') if p.strip()]

    def __str__(self):
        status = "ON" if self.is_enabled else "OFF"
        return f"[{self.rule_id}] [{status}] [{self.intent}] {self.name} (P{self.priority})"


class RuleExecutionLog(models.Model):
    # M2.4: Audit log for every rule engine evaluation.
    # log_id is stable and immutable (REL000001).
    log_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable log identifier e.g. REL000001.",
    )
    session_id = models.UUIDField(null=True, blank=True, db_index=True)
    query = models.TextField()
    matched_rule = models.ForeignKey(
        BusinessRule, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='execution_logs',
    )
    resolved_intent = models.CharField(max_length=50, choices=INTENT_CHOICES,
                                       default='unknown_intent')
    confidence_score = models.FloatField(default=0.0)
    rules_evaluated = models.IntegerField(default=0)
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES, default='unknown')
    execution_time_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Rule Execution Log"
        verbose_name_plural = "Rule Execution Logs"

    def save(self, *args, **kwargs):
        if not self.log_id:
            self.log_id = self._generate_log_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_log_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            log_id__regex=r'^REL\d{6}$'
        ).aggregate(max_id=Max('log_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"REL{seq:06d}"

    def __str__(self):
        return (
            f"[{self.log_id}] [{self.outcome.upper()}] "
            f"intent={self.resolved_intent} confidence={self.confidence_score:.2f}"
        )


# ── M2.5 Service Coverage Framework ──────────────────────────────────────────

class ServiceProfile(models.Model):
    """
    M2.5 — Standardized, configuration-driven service profile.
    Every service gets an immutable sequential Service ID (e.g. SRV000001).
    """
    service_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable service identifier e.g. SRV000001."
    )
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    short_description = models.TextField()
    detailed_description = models.TextField()
    business_objective = models.TextField()
    target_audience = models.TextField()
    eligibility = models.TextField(blank=True, help_text="Eligibility rules / criteria")
    required_inputs = models.TextField(blank=True, help_text="Required documents / inputs")
    advisory_content = models.JSONField(
        default=dict,
        help_text="Advisory details including overview, benefits, process, pricing, and limitations."
    )
    faqs = models.JSONField(default=list, help_text="List of inline FAQs")
    knowledge_references = models.CharField(
        max_length=255, blank=True,
        help_text="Search terms to query Unified Knowledge Repository for this service"
    )
    related_services = models.JSONField(default=list, help_text="List of related Service IDs")
    call_to_actions = models.JSONField(default=list, help_text="Call-to-action actions / suggestions")
    contact_channels = models.JSONField(default=list, help_text="Allowed contact channels for this service")
    escalation_rules = models.JSONField(default=dict, help_text="Escalation pathways")
    navigation_links = models.JSONField(default=list, help_text="Key web page navigation URLs")
    display_priority = models.PositiveIntegerField(default=50)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_priority', 'name']
        verbose_name = "Service Profile"
        verbose_name_plural = "Service Profiles"

    def save(self, *args, **kwargs):
        if not self.service_id:
            self.service_id = self._generate_service_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_service_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            service_id__regex=r'^SRV\d{6}$'
        ).aggregate(max_id=Max('service_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"SRV{seq:06d}"

    def __str__(self):
        return f"[{self.service_id}] {self.name} (v{self.version})"


# ── M2.6 Conversational Inquiry Creation ─────────────────────────────────────

INQUIRY_STATE_CHOICES = [
    ('not_started',                   'Not Started'),
    ('collecting_information',        'Collecting Information'),
    ('awaiting_conflict_resolution',  'Awaiting Conflict Resolution'),
    ('awaiting_confirmation',         'Awaiting Confirmation'),
    ('submitted',                     'Submitted'),
    ('cancelled',                     'Cancelled'),
    ('expired',                       'Expired'),
]

INQUIRY_SOURCE_CHOICES = [
    ('manual_chat',          'Manual Chat Request'),
    ('service_profile_cta',  'Service Profile CTA'),
    ('rule_engine',          'Rule Engine Intent'),
    ('suggestion_chip',      'Suggestion Chip'),
    ('website_entry_point',  'Website Entry Point'),
]

AUDIT_EVENT_CHOICES = [
    ('session_started',        'Session Started'),
    ('message_received',       'Message Received'),
    ('field_extracted',        'Field Extracted from Message'),
    ('field_prompted',         'Field Prompted'),
    ('validation_error',       'Validation Error'),
    ('validation_passed',      'Validation Passed'),
    ('field_skipped',          'Field Skipped'),
    ('conflict_detected',      'Conflict Detected'),
    ('conflict_resolved',      'Conflict Resolved'),
    ('confirmation_prompted',  'Confirmation Prompted'),
    ('confirmed',              'Customer Confirmed'),
    ('submitted',              'Inquiry Submitted'),
    ('cancelled',              'Session Cancelled'),
    ('expired',                'Session Expired'),
    ('resumed',                'Session Resumed'),
]


class InquiryConversationSession(models.Model):
    """
    M2.6 — Tracks the full lifecycle of a realBOT-guided inquiry conversation.
    """
    ics_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable identifier e.g. ICS000001.",
    )
    realbot_session = models.ForeignKey(
        RealBotSession, on_delete=models.CASCADE, related_name='inquiry_sessions',
    )
    state = models.CharField(
        max_length=40, choices=INQUIRY_STATE_CHOICES,
        default='collecting_information', db_index=True,
    )
    source = models.CharField(
        max_length=30, choices=INQUIRY_SOURCE_CHOICES, default='manual_chat',
    )
    service_hint = models.CharField(
        max_length=100, blank=True,
        help_text="Service intent from triggering context e.g. 'sell_property'.",
    )
    collected_data = models.JSONField(default=dict)
    skipped_fields = models.JSONField(default=list)
    conflict_field = models.CharField(max_length=50, blank=True)
    conflict_new_value = models.CharField(max_length=500, blank=True)
    current_prompt_field = models.CharField(max_length=50, blank=True)
    submitted_inquiry_id = models.IntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    cancelled_reason = models.CharField(max_length=200, blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Inquiry Conversation Session'
        verbose_name_plural = 'Inquiry Conversation Sessions'
        indexes = [
            models.Index(fields=['state']),
            models.Index(fields=['realbot_session', 'state']),
        ]

    def save(self, *args, **kwargs):
        if not self.ics_id:
            self.ics_id = self._generate_ics_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_ics_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            ics_id__regex=r'^ICS\d{6}$'
        ).aggregate(max_id=Max('ics_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f'ICS{seq:06d}'

    def fields_collected_count(self):
        return len(self.collected_data)

    def __str__(self):
        return f'[{self.ics_id}] [{self.state}] {self.source}'


class InquiryConversationAuditLog(models.Model):
    """
    M2.6 — Immutable, append-only audit trail for every inquiry conversation event.
    """
    log_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable log identifier e.g. ICL000001.",
    )
    ics_session = models.ForeignKey(
        InquiryConversationSession, on_delete=models.CASCADE, related_name='audit_logs',
    )
    event_type = models.CharField(max_length=30, choices=AUDIT_EVENT_CHOICES)
    field_name = models.CharField(max_length=50, blank=True)
    raw_input = models.TextField(blank=True)
    extracted_value = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Inquiry Audit Log'
        verbose_name_plural = 'Inquiry Audit Logs'

    def save(self, *args, **kwargs):
        if not self.log_id:
            self.log_id = self._generate_log_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_log_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            log_id__regex=r'^ICL\d{6}$'
        ).aggregate(max_id=Max('log_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f'ICL{seq:06d}'

    def __str__(self):
        return f'[{self.log_id}] [{self.event_type}] {self.field_name or "-"}'


# ── M2.7 Quick Inquiry & Suggestion Framework ───────────────────────────────

SUGGESTION_CATEGORY_CHOICES = [
    ('Welcome',             'Welcome Suggestions'),
    ('Service',             'Service Suggestions'),
    ('Property',            'Property Suggestions'),
    ('Inquiry',             'Inquiry Suggestions'),
    ('Knowledge',            'Knowledge Suggestions'),
    ('ResourceHub',         'Resource Hub Suggestions'),
    ('GovernmentService',   'Government Service Suggestions'),
    ('Contact',             'Contact Suggestions'),
    ('Navigation',          'Navigation Suggestions'),
    ('Follow-up',           'Follow-up Suggestions'),
    ('Recovery',            'Conversation Recovery Suggestions'),
    ('Completion',          'Completion Suggestions'),
]

SUGGESTION_STATUS_CHOICES = [
    ('active',   'Active'),
    ('inactive', 'Inactive'),
]

INTERACTION_TYPE_CHOICES = [
    ('rendered', 'Rendered to Client'),
    ('clicked',  'Clicked by Client'),
]


class SuggestionDefinition(models.Model):
    """
    M2.7 — Configuration-driven Suggestion Registry.
    Each suggestion has an immutable sequential Suggestion ID (SUG000001).
    """
    suggestion_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable identifier e.g. SUG000001."
    )
    display_text = models.CharField(
        max_length=150,
        help_text="The label text displayed on the suggestion chip."
    )
    category = models.CharField(
        max_length=50, choices=SUGGESTION_CATEGORY_CHOICES, default='Welcome'
    )
    parent_context = models.CharField(
        max_length=100, blank=True,
        help_text="Associates the suggestion with an intent, service ID or other context."
    )
    trigger_condition = models.JSONField(
        default=dict, blank=True,
        help_text="JSON structure defining matching context e.g. {'intent': 'buy_property'}."
    )
    business_intent = models.CharField(
        max_length=50, choices=INTENT_CHOICES, blank=True,
        help_text="The intent triggered when this suggestion is clicked."
    )
    target_action = models.CharField(
        max_length=250, blank=True,
        help_text="Target URL or action description triggered on click."
    )
    display_priority = models.PositiveIntegerField(
        default=50,
        help_text="Lower values = higher priority. 1=highest, 99=lowest."
    )
    icon = models.CharField(
        max_length=50, blank=True,
        help_text="Icon reference name e.g., 'home', 'phone', 'file-text'."
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Defines display order within the same priority level."
    )
    visibility_rules = models.JSONField(
        default=dict, blank=True,
        help_text="Visibility constraints such as allowed pages list."
    )
    status = models.CharField(
        max_length=20, choices=SUGGESTION_STATUS_CHOICES, default='active'
    )
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_priority', 'display_order', 'display_text']
        verbose_name = "Suggestion Definition"
        verbose_name_plural = "Suggestion Definitions"
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['display_priority', 'status']),
        ]

    def save(self, *args, **kwargs):
        if not self.suggestion_id:
            self.suggestion_id = self._generate_suggestion_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_suggestion_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            suggestion_id__regex=r'^SUG\d{6}$'
        ).aggregate(max_id=Max('suggestion_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"SUG{seq:06d}"

    def __str__(self):
        return f"[{self.suggestion_id}] [{self.category}] {self.display_text}"


class SuggestionInteractionLog(models.Model):
    """
    M2.7 — Captures suggestion display and click analytics for analytics/diagnostics.
    Each log entry has a unique immutable ID SGL000001.
    """
    log_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable log identifier e.g. SGL000001."
    )
    session = models.ForeignKey(
        RealBotSession, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='suggestion_logs'
    )
    suggestion_id = models.CharField(
        max_length=20,
        help_text="The ID of the suggestion definition."
    )
    display_text = models.CharField(max_length=150)
    category = models.CharField(max_length=50)
    interaction_type = models.CharField(
        max_length=30, choices=INTERACTION_TYPE_CHOICES, default='rendered'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Suggestion Interaction Log"
        verbose_name_plural = "Suggestion Interaction Logs"
        indexes = [
            models.Index(fields=['suggestion_id', 'interaction_type']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.log_id:
            self.log_id = self._generate_log_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_log_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            log_id__regex=r'^SGL\d{6}$'
        ).aggregate(max_id=Max('log_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"SGL{seq:06d}"

    def __str__(self):
        return f"[{self.log_id}] [{self.interaction_type.upper()}] {self.display_text} ({self.suggestion_id})"


# ── M2.8 Quick Navigation & Action Models ────────────────────────────────────

class ActionDefinition(models.Model):
    """
    M2.8 — Administrative Action Registry Foundation.
    Represents configuration-driven actions mapping internal & external navigation.
    """
    action_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    action_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)  # Internal, Communication, Location, Social, GovernmentServices, BusinessActions
    action_type = models.CharField(max_length=50)  # internal_nav, external_nav, phone_call, whatsapp, inquiry_workflow
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    target_url = models.CharField(max_length=500, blank=True, default='')
    target_service = models.CharField(max_length=100, blank=True, default='')
    supported_parameters = models.JSONField(default=list, blank=True)
    confirmation_required = models.BooleanField(default=False)
    visibility_rules = models.JSONField(default=dict, blank=True)
    security_level = models.CharField(max_length=20, default='public')
    status = models.CharField(max_length=20, default='active')
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.action_id:
            self.action_id = self._generate_action_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_action_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            action_id__regex=r'^ACT\d{6}$'
        ).aggregate(max_id=Max('action_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"ACT{seq:06d}"

    def __str__(self):
        return f"[{self.action_id}] {self.display_name} ({self.category})"


class ActionExecutionLog(models.Model):
    """
    M2.8 — Action Diagnostics & Analytics logs. Read-only / append-only.
    """
    log_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    session = models.ForeignKey(RealBotSession, on_delete=models.SET_NULL, null=True, blank=True)
    action_id = models.CharField(max_length=20)
    action_name = models.CharField(max_length=100)
    parameters = models.JSONField(default=dict, blank=True)
    is_validated = models.BooleanField(default=True)
    requires_confirmation = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.log_id:
            self.log_id = self._generate_log_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_log_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            log_id__regex=r'^ACL\d{6}$'
        ).aggregate(max_id=Max('log_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"ACL{seq:06d}"

    def __str__(self):
        return f"[{self.log_id}] Executed {self.action_name} ({self.action_id})"


# ── M2.9 Rich Response Models ────────────────────────────────────────────────

class ResponseComponent(models.Model):
    """
    M2.9 — Response Component Registry.
    Represents structured, configuration-driven rich response templates.
    """
    component_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    component_type = models.CharField(max_length=50)  # text, card, list, chips, alert
    display_template = models.TextField(blank=True, default='')
    content_model = models.JSONField(default=dict, blank=True)
    data_schema = models.JSONField(default=list, blank=True)  # List of expected parameter names
    rendering_priority = models.IntegerField(default=10)
    visibility_rules = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default='active')
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.component_id:
            self.component_id = self._generate_component_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_component_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            component_id__regex=r'^RSP\d{6}$'
        ).aggregate(max_id=Max('component_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"RSP{seq:06d}"

    def __str__(self):
        return f"[{self.component_id}] {self.name} ({self.component_type})"


class ResponseCompositionLog(models.Model):
    """
    M2.9 — Response Analytics & Diagnostics Log. Read-only/append-only.
    """
    log_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    session = models.ForeignKey(RealBotSession, on_delete=models.SET_NULL, null=True, blank=True)
    composition = models.JSONField(default=list, blank=True)
    is_validated = models.BooleanField(default=True)
    errors = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.log_id:
            self.log_id = self._generate_log_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_log_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            log_id__regex=r'^RSL\d{6}$'
        ).aggregate(max_id=Max('log_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"RSL{seq:06d}"

    def __str__(self):
        return f"[{self.log_id}] Composed Response (Validated: {self.is_validated})"


# ── M2.10 Conversation Context & Memory Models ────────────────────────────────

class ConversationContext(models.Model):
    """
    M2.10 — Conversation Memory & Session Context Repository.
    Maintains session-scoped customer profile, intent tracking, active topic details.
    """
    context_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    session = models.OneToOneField(RealBotSession, on_delete=models.CASCADE, related_name='context')
    current_topic = models.CharField(max_length=100, default='', blank=True)
    previous_topic = models.CharField(max_length=100, default='', blank=True)
    active_intent = models.CharField(max_length=100, default='', blank=True)
    active_service = models.CharField(max_length=100, default='', blank=True)
    active_inquiry_id = models.CharField(max_length=50, default='', blank=True)
    last_knowledge_topic = models.CharField(max_length=200, default='', blank=True)
    last_suggested_actions = models.JSONField(default=list, blank=True)
    recent_inputs = models.JSONField(default=list, blank=True)
    pending_questions = models.JSONField(default=list, blank=True)
    outstanding_fields = models.JSONField(default=list, blank=True)
    variables = models.JSONField(default=dict, blank=True)  # Typed KV storage with expiration policies
    conversation_state = models.CharField(max_length=50, default='idle')
    navigation_state = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.context_id:
            self.context_id = self._generate_context_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_context_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            context_id__regex=r'^CTX\d{6}$'
        ).aggregate(max_id=Max('context_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"CTX{seq:06d}"

    def __str__(self):
        return f"[{self.context_id}] Context for Session {self.session.session_id} (Topic: {self.current_topic or 'None'})"


class ContextUpdateLog(models.Model):
    """
    M2.10 — Context Transitions and Analytics Logs. Append-only.
    """
    log_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    context = models.ForeignKey(ConversationContext, on_delete=models.CASCADE, related_name='update_logs')
    action = models.CharField(max_length=50)  # created, updated, topic_switch, cleared
    transition_from = models.CharField(max_length=100, default='', blank=True)
    transition_to = models.CharField(max_length=100, default='', blank=True)
    updated_variables = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.log_id:
            self.log_id = self._generate_log_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_log_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            log_id__regex=r'^CTL\d{6}$'
        ).aggregate(max_id=Max('log_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"CTL{seq:06d}"

    def __str__(self):
        return f"[{self.log_id}] Action: {self.action} (Transition: {self.transition_from or '-'} -> {self.transition_to or '-'})"


# ── M2.11 Analytics & Observability Models ────────────────────────────────────

class PlatformEvent(models.Model):
    """
    M2.11 — Platform Event Registry.
    Stores immutable, write-once operational logs and latency checks.
    """
    event_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    event_type = models.CharField(max_length=100)
    session_id = models.CharField(max_length=50, blank=True, null=True)
    provider = models.CharField(max_length=50)  # conversation, knowledge, service, inquiry, suggestion, etc.
    payload = models.JSONField(default=dict, blank=True)
    duration_ms = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.event_id:
            self.event_id = self._generate_event_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_event_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            event_id__regex=r'^EVT\d{6}$'
        ).aggregate(max_id=Max('event_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"EVT{seq:06d}"

    def __str__(self):
        return f"[{self.event_id}] Type: {self.event_type} (Provider: {self.provider})"


class MetricAggregate(models.Model):
    """
    M2.11 — Analytics Metrics Aggregation Window Cache table.
    """
    aggregate_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    metric_key = models.CharField(max_length=100)
    window_type = models.CharField(max_length=20)  # hourly, daily, weekly, monthly
    window_start = models.DateTimeField()
    value = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.aggregate_id:
            self.aggregate_id = self._generate_aggregate_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_aggregate_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            aggregate_id__regex=r'^AGG\d{6}$'
        ).aggregate(max_id=Max('aggregate_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"AGG{seq:06d}"

    def __str__(self):
        return f"[{self.aggregate_id}] {self.metric_key} ({self.window_type}): {self.value}"


# ── M2.12 Platform Administration & Configuration Models ──────────────────────

class ConfigurationItem(models.Model):
    """
    M2.12 — Central Configuration Registry.
    Manages runtime settings dynamically, governing bot behavior and modules.
    """
    config_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    key = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)  # Platform, Business, Conversation, Knowledge, Service, etc.
    config_type = models.CharField(max_length=20)  # string, integer, float, boolean, json
    value = models.TextField()
    default_value = models.TextField(blank=True, default='')
    validation_rules = models.JSONField(default=dict, blank=True)
    visibility_level = models.CharField(max_length=20, default='admin')
    editable = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    version = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default='active')
    last_modified_by = models.CharField(max_length=100, blank=True, default='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.config_id:
            self.config_id = self._generate_config_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_config_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            config_id__regex=r'^CFG\d{6}$'
        ).aggregate(max_id=Max('config_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"CFG{seq:06d}"

    def __str__(self):
        return f"[{self.config_id}] {self.key} = {self.value[:30]}"


class ConfigurationAuditLog(models.Model):
    """
    M2.12 — Configuration Change Audit Logs. Append-only/Read-only.
    """
    audit_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    config_item = models.ForeignKey(ConfigurationItem, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=50)  # created, updated, published, rollback, disabled
    previous_value = models.TextField(blank=True, default='')
    new_value = models.TextField()
    version = models.IntegerField()
    modified_by = models.CharField(max_length=100, default='admin')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.audit_id:
            self.audit_id = self._generate_audit_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_audit_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            audit_id__regex=r'^CFL\d{6}$'
        ).aggregate(max_id=Max('audit_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"CFL{seq:06d}"

    def __str__(self):
        return f"[{self.audit_id}] Config: {self.config_item.key} (V{self.version}) Action: {self.action}"


# ── M2.13 Conversation Orchestration & Workflow Engine Models ─────────────────

class OrchestrationWorkflow(models.Model):
    """
    M2.13 — Orchestration Workflow record.
    Tracks state transitions of incoming customer messages through the execution pipeline.
    """
    workflow_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    session_id = models.CharField(max_length=50)
    state = models.CharField(max_length=30, default='Initialized')
    current_stage = models.CharField(max_length=50, blank=True, default='')
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.workflow_id:
            self.workflow_id = self._generate_workflow_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_workflow_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            workflow_id__regex=r'^WF\d{6}$'
        ).aggregate(max_id=Max('workflow_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"WF{seq:06d}"

    def __str__(self):
        return f"[{self.workflow_id}] Session: {self.session_id} (State: {self.state})"


class WorkflowExecutionStep(models.Model):
    """
    M2.13 — Stage tracing logs for execution steps. Append-only.
    """
    step_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    workflow = models.ForeignKey(OrchestrationWorkflow, on_delete=models.CASCADE, related_name='steps')
    stage = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='success')  # success, warning, failed, skipped
    duration_ms = models.IntegerField(default=0)
    logs = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.step_id:
            self.step_id = self._generate_step_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_step_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            step_id__regex=r'^WFS\d{6}$'
        ).aggregate(max_id=Max('step_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"WFS{seq:06d}"

    def __str__(self):
        return f"[{self.step_id}] Workflow: {self.workflow.workflow_id} Stage: {self.stage} ({self.status})"


# ── M2.14 Security, Authorization & Platform Governance Models ────────────────

SECURITY_EVENT_TYPE_CHOICES = [
    ('session_started', 'Session Started'),
    ('session_terminated', 'Session Terminated'),
    ('invalid_request', 'Invalid Request'),
    ('authorization_failure', 'Authorization Failure'),
    ('policy_violation', 'Policy Violation'),
    ('rate_limit_triggered', 'Rate Limit Triggered'),
    ('abuse_detected', 'Abuse Detected'),
    ('configuration_access', 'Configuration Access'),
    ('administrative_change', 'Administrative Change'),
    ('security_exception', 'Security Exception'),
]

SECURITY_SEVERITY_CHOICES = [
    ('info', 'Info'),
    ('warning', 'Warning'),
    ('critical', 'Critical'),
]

SECURITY_DOMAIN_CHOICES = [
    ('session', 'Session Security'),
    ('request', 'Request Validation'),
    ('input', 'Input Validation'),
    ('output', 'Output Validation'),
    ('configuration', 'Configuration Security'),
    ('workflow', 'Workflow Security'),
    ('action', 'Action Authorization'),
    ('navigation', 'Navigation Security'),
    ('inquiry', 'Inquiry Protection'),
    ('analytics', 'Analytics Protection'),
    ('admin', 'Administrative Security'),
    ('api', 'API Security'),
]

SECURITY_POLICY_TYPE_CHOICES = [
    ('limit', 'Limit'),
    ('threshold', 'Threshold'),
    ('rule', 'Rule'),
    ('validation', 'Validation'),
]


class SecurityEvent(models.Model):
    """
    M2.14 — Immutable, append-only security audit event log.
    Every security-relevant occurrence receives a permanent, sequential SEC###### identifier.
    """
    event_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    event_type = models.CharField(max_length=30, choices=SECURITY_EVENT_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SECURITY_SEVERITY_CHOICES, default='info')
    source_ip = models.CharField(max_length=50, blank=True, default='')
    session_id = models.CharField(max_length=50, blank=True, default='')
    request_path = models.CharField(max_length=500, blank=True, default='')
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.event_id:
            self.event_id = self._generate_event_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_event_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            event_id__regex=r'^SEC\d{6}$'
        ).aggregate(max_id=Max('event_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"SEC{seq:06d}"

    def __str__(self):
        return f"[{self.event_id}] {self.event_type} ({self.severity})"


class SecurityPolicy(models.Model):
    """
    M2.14 — Configuration-driven security policies.
    Defines limits, thresholds, rules, and validation constraints
    consumed by the Security Manager and Policy Engine.
    """
    policy_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    policy_key = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=20, choices=SECURITY_DOMAIN_CHOICES)
    policy_type = models.CharField(max_length=20, choices=SECURITY_POLICY_TYPE_CHOICES)
    value = models.TextField()
    default_value = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.policy_id:
            self.policy_id = self._generate_policy_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_policy_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            policy_id__regex=r'^SPL\d{6}$'
        ).aggregate(max_id=Max('policy_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"SPL{seq:06d}"

    def __str__(self):
        return f"[{self.policy_id}] {self.policy_key} ({self.domain})"


# ── M2.15 Knowledge Version & Lifecycle Audit Models ──────────────────────────

class KnowledgeVersionHistory(models.Model):
    """
    M2.15 — Immutable, historical record of a KnowledgeArticle or KnowledgeDocument content version.
    Identified sequentially by KVH######.
    """
    version_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    article = models.ForeignKey(KnowledgeArticle, on_delete=models.CASCADE, null=True, blank=True, related_name='version_history')
    document = models.ForeignKey(KnowledgeDocument, on_delete=models.CASCADE, null=True, blank=True, related_name='version_history')
    version = models.PositiveIntegerField()
    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True)
    main_content = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    tags = models.TextField(blank=True)
    search_weight = models.FloatField(default=1.0)
    created_by = models.CharField(max_length=100, default='admin')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version', '-created_at']
        verbose_name = "Knowledge Version History"
        verbose_name_plural = "Knowledge Version Histories"

    def save(self, *args, **kwargs):
        if not self.version_id:
            self.version_id = self._generate_version_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_version_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            version_id__regex=r'^KVH\d{6}$'
        ).aggregate(max_id=Max('version_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"KVH{seq:06d}"

    def __str__(self):
        target = f"Article {self.article.knowledge_id}" if self.article else f"Document {self.document.doc_id}"
        return f"[{self.version_id}] {target} (v{self.version})"


class KnowledgeLifecycleAuditLog(models.Model):
    """
    M2.15 — Append-only log of all knowledge asset lifecycle actions.
    Identified sequentially by KLA######.
    """
    audit_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    article_id = models.CharField(max_length=20, blank=True, default='')
    doc_id = models.CharField(max_length=20, blank=True, default='')
    action = models.CharField(max_length=30, choices=KNOWLEDGE_ACTION_CHOICES)
    performed_by = models.CharField(max_length=100, default='admin')
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Knowledge Lifecycle Audit Log"
        verbose_name_plural = "Knowledge Lifecycle Audit Logs"

    def save(self, *args, **kwargs):
        if not self.audit_id:
            self.audit_id = self._generate_audit_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_audit_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            audit_id__regex=r'^KLA\d{6}$'
        ).aggregate(max_id=Max('audit_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"KLA{seq:06d}"

    def __str__(self):
        target = self.article_id or self.doc_id or "unknown"
        return f"[{self.audit_id}] Target: {target} Action: {self.action}"


# ══════════════════════════════════════════════════════════════════════════════
# M2.17 — Human Handover & Conversation Closure Models
# ══════════════════════════════════════════════════════════════════════════════

ADVISOR_STATUS_CHOICES = [
    ('available', 'Available'),
    ('busy', 'Busy'),
    ('offline', 'Offline'),
]

ADVISOR_AVAILABLE = 'available'

CLOSURE_REASON_CHOICES = [
    ('handover_completed', 'Handover Completed'),
    ('customer_disconnected', 'Customer Disconnected'),
    ('advisor_closed', 'Advisor Closed'),
    ('system', 'System Closure'),
    ('timeout', 'Session Timeout'),
]

CLOSURE_SYSTEM = 'system'


class AdvisorProfile(models.Model):
    """
    M2.17 — Registry of Propertism advisors available for human handover.
    Each advisor has a display name, email, and availability status.
    """
    advisor_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable advisor identifier e.g. ADV000001.",
    )
    display_name = models.CharField(max_length=200, help_text="Advisor display name shown to customers")
    email = models.EmailField(help_text="Advisor email for notifications")
    phone = models.CharField(max_length=30, blank=True, help_text="Optional contact number")
    status = models.CharField(
        max_length=20, choices=ADVISOR_STATUS_CHOICES, default=ADVISOR_AVAILABLE,
        help_text="Current availability status"
    )
    max_concurrent_chats = models.PositiveIntegerField(default=3, help_text="Maximum simultaneous conversations")
    active_chat_count = models.PositiveIntegerField(default=0, help_text="Current active conversation count")
    is_active = models.BooleanField(default=True, help_text="Whether this advisor is active in the system")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_name']
        verbose_name = "Advisor Profile"
        verbose_name_plural = "Advisor Profiles"

    def save(self, *args, **kwargs):
        if not self.advisor_id:
            self.advisor_id = self._generate_advisor_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_advisor_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            advisor_id__regex=r'^ADV\d{6}$'
        ).aggregate(max_id=Max('advisor_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"ADV{seq:06d}"

    def __str__(self):
        return f"[{self.advisor_id}] {self.display_name} ({self.status})"


class HandoverRequest(models.Model):
    """
    M2.17 — Tracks a customer's request to transition from bot to human advisor.
    Follows the state machine: REQUESTED -> ACCEPTED -> COMPLETED / REJECTED / CANCELLED.
    """
    REQUEST_STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    handover_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable handover identifier e.g. HOV000001.",
    )
    session = models.ForeignKey(
        RealBotSession, on_delete=models.CASCADE, related_name='handover_requests',
        help_text="The realBOT session requesting handover"
    )
    customer_name = models.CharField(max_length=200, blank=True, help_text="Customer display name")
    customer_email = models.EmailField(blank=True, help_text="Customer email for transcript delivery")
    customer_phone = models.CharField(max_length=30, blank=True, help_text="Customer contact number")
    reason = models.TextField(blank=True, help_text="Reason provided by customer for requesting handover")
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='requested')
    assigned_advisor = models.ForeignKey(
        AdvisorProfile, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='handover_assignments'
    )
    assigned_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Internal notes about the handover")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Handover Request"
        verbose_name_plural = "Handover Requests"

    def save(self, *args, **kwargs):
        if not self.handover_id:
            self.handover_id = self._generate_handover_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_handover_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            handover_id__regex=r'^HOV\d{6}$'
        ).aggregate(max_id=Max('handover_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"HOV{seq:06d}"

    def __str__(self):
        return f"[{self.handover_id}] Session: {self.session.session_id} (Status: {self.status})"


class AdvisorMessage(models.Model):
    """
    M2.17 — Stores messages exchanged between advisor and customer during a handover.
    Each message has a unique immutable ID ADM######.
    """
    SENDER_TYPE_CHOICES = [
        ('advisor', 'Advisor'),
        ('customer', 'Customer'),
        ('system', 'System'),
    ]

    message_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable message identifier e.g. ADM000001.",
    )
    handover = models.ForeignKey(
        HandoverRequest, on_delete=models.CASCADE, related_name='messages',
        help_text="The handover request this message belongs to"
    )
    sender_type = models.CharField(
        max_length=20, choices=SENDER_TYPE_CHOICES,
        help_text="Who sent this message"
    )
    sender_name = models.CharField(
        max_length=200, blank=True,
        help_text="Display name of the sender"
    )
    content = models.TextField(help_text="Message content")
    is_read = models.BooleanField(default=False, help_text="Whether the message has been read")
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "Advisor Message"
        verbose_name_plural = "Advisor Messages"

    def save(self, *args, **kwargs):
        if not self.message_id:
            self.message_id = self._generate_message_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_message_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            message_id__regex=r'^ADM\d{6}$'
        ).aggregate(max_id=Max('message_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"ADM{seq:06d}"

    def __str__(self):
        return f"[{self.message_id}] {self.sender_type}: {self.content[:50]}"


class ConversationArchive(models.Model):
    """
    M2.17 — Stores the complete conversation transcript when a handover is completed.
    Immutable once created. Identified by ARC######.
    """
    archive_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable archive identifier e.g. ARC000001.",
    )
    session = models.ForeignKey(
        'RealBotSession', on_delete=models.SET_NULL, null=True, blank=True, related_name='archives',
        help_text="The realBOT session this archive belongs to"
    )
    handover = models.OneToOneField(
        HandoverRequest, on_delete=models.CASCADE, related_name='archive',
        null=True, blank=True,
        help_text="The handover request this archive belongs to"
    )
    bot_transcript = models.JSONField(
        default=list, blank=True,
        help_text="List of bot conversation messages before handover"
    )
    advisor_transcript = models.JSONField(
        default=list, blank=True,
        help_text="List of advisor conversation messages during handover"
    )
    full_transcript = models.JSONField(
        default=list, blank=True,
        help_text="Combined full transcript of the entire conversation"
    )
    conversation_data = models.JSONField(
        default=dict, blank=True,
        help_text="Full conversation structured data"
    )
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    closure_reason = models.CharField(max_length=50, blank=True)
    closed_by = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(
        default=dict, blank=True,
        help_text="Additional metadata about the conversation"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Conversation Archive"
        verbose_name_plural = "Conversation Archives"

    def save(self, *args, **kwargs):
        if not self.archive_id:
            self.archive_id = self._generate_archive_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_archive_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            archive_id__regex=r'^ARC\d{6}$'
        ).aggregate(max_id=Max('archive_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"ARC{seq:06d}"

    def __str__(self):
        return f"[{self.archive_id}] Handover: {self.handover.handover_id if self.handover else 'None'}"


class TranscriptRecord(models.Model):
    """
    M2.17 — Individual transcript entry for a handover conversation.
    Each entry has a unique immutable ID TRN######.
    """
    transcript_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable transcript identifier e.g. TRN000001.",
    )
    archive = models.ForeignKey(
        ConversationArchive, on_delete=models.CASCADE, related_name='transcript_entries',
        help_text="The archive this transcript entry belongs to"
    )
    sender = models.CharField(max_length=100, help_text="Who sent the message")
    message = models.TextField(help_text="The message content")
    message_type = models.CharField(
        max_length=30, default='text',
        help_text="Type of message: text, system, handover_notice, etc."
    )
    sequence = models.PositiveIntegerField(
        default=0,
        help_text="Sequence number for ordering transcript entries"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sequence', 'created_at']
        verbose_name = "Transcript Record"
        verbose_name_plural = "Transcript Records"

    def save(self, *args, **kwargs):
        if not self.transcript_id:
            self.transcript_id = self._generate_transcript_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_transcript_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            transcript_id__regex=r'^TRN\d{6}$'
        ).aggregate(max_id=Max('transcript_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"TRN{seq:06d}"

    def __str__(self):
        return f"[{self.transcript_id}] {self.sender}: {self.message[:50]}"


class HandoverAnalytics(models.Model):
    """
    M2.17 — Aggregated analytics for handover performance monitoring.
    Each record has a unique immutable ID HAN######.
    """
    analytics_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable analytics identifier e.g. HAN000001.",
    )
    handover = models.OneToOneField(
        HandoverRequest, on_delete=models.CASCADE, related_name='analytics',
        help_text="The handover request these analytics belong to"
    )
    wait_duration_seconds = models.IntegerField(
        default=0,
        help_text="Time customer waited before being assigned to an advisor"
    )
    handover_duration_seconds = models.IntegerField(
        default=0,
        help_text="Total duration of the handover conversation"
    )
    message_count = models.IntegerField(
        default=0,
        help_text="Total number of messages exchanged during handover"
    )
    customer_satisfaction = models.IntegerField(
        null=True, blank=True,
        help_text="Customer satisfaction rating (1-5)"
    )
    resolution_status = models.CharField(
        max_length=50, blank=True,
        help_text="Whether the handover resolved the customer's issue"
    )
    notes = models.TextField(blank=True, help_text="Additional analytics notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Handover Analytics"
        verbose_name_plural = "Handover Analytics"

    def save(self, *args, **kwargs):
        if not self.analytics_id:
            self.analytics_id = self._generate_analytics_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_analytics_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            analytics_id__regex=r'^HAN\d{6}$'
        ).aggregate(max_id=Max('analytics_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"HAN{seq:06d}"

    def __str__(self):
        return f"[{self.analytics_id}] Handover: {self.handover.handover_id} (Duration: {self.handover_duration_seconds}s)"


class HandoverAuditLog(models.Model):
    """
    M2.17 — Immutable, append-only audit trail for all handover lifecycle events.
    Each entry has a unique immutable ID HAL######.
    """
    AUDIT_ACTION_CHOICES = [
        ('handover_requested', 'Handover Requested'),
        ('handover_accepted', 'Handover Accepted'),
        ('handover_rejected', 'Handover Rejected'),
        ('handover_cancelled', 'Handover Cancelled'),
        ('handover_completed', 'Handover Completed'),
        ('advisor_assigned', 'Advisor Assigned'),
        ('advisor_unavailable', 'Advisor Unavailable'),
        ('message_sent', 'Message Sent'),
        ('transcript_archived', 'Transcript Archived'),
        ('customer_disconnected', 'Customer Disconnected'),
        ('session_closed', 'Session Closed'),
        ('error', 'Error Occurred'),
    ]

    audit_id = models.CharField(
        max_length=20, unique=True, blank=True, db_index=True,
        help_text="Stable, immutable audit identifier e.g. HAL000001.",
    )
    handover = models.ForeignKey(
        HandoverRequest, on_delete=models.CASCADE, related_name='audit_logs',
        help_text="The handover request this audit entry belongs to"
    )
    action = models.CharField(
        max_length=30, choices=AUDIT_ACTION_CHOICES,
        help_text="The audit action performed"
    )
    performed_by = models.CharField(
        max_length=100, blank=True,
        help_text="Who performed the action (system, advisor name, customer)"
    )
    details = models.JSONField(
        default=dict, blank=True,
        help_text="Additional details about the audit event"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Handover Audit Log"
        verbose_name_plural = "Handover Audit Logs"

    def save(self, *args, **kwargs):
        if not self.audit_id:
            self.audit_id = self._generate_audit_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_audit_id(cls):
        from django.db.models import Max
        last = cls.objects.filter(
            audit_id__regex=r'^HAL\d{6}$'
        ).aggregate(max_id=Max('audit_id'))['max_id']
        if last:
            seq = int(re.search(r'\d+', last).group()) + 1
        else:
            seq = 1
        return f"HAL{seq:06d}"

    def __str__(self):
        return f"[{self.audit_id}] Handover: {self.handover.handover_id} Action: {self.action}"

