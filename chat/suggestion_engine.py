"""
chat/suggestion_engine.py — M2.7 Suggestion Engine & Providers Framework

Aggregates suggestions from 9 context providers, ranks them, deduplicates,
applies visibility rules, logs analytics, and returns suggestion chips.
"""
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from chat.models import SuggestionDefinition, SuggestionInteractionLog, RealBotSession

logger = logging.getLogger(__name__)


# ── Context DTO ───────────────────────────────────────────────────────────────

@dataclass
class SuggestionContext:
    session:                Optional[RealBotSession] = None
    intent:                 str = 'unknown_intent'
    active_service_profile: Optional[str] = None          # service profile name
    conversation_state:     str = 'active'                # welcome, active, idle
    inquiry_state:          str = 'not_started'           # not_started, collecting_information, awaiting_confirmation, submitted, cancelled, expired
    current_page:           str = ''                      # page URL e.g. /nri-assist
    knowledge_resolved:     bool = False                  # True if last query resolved via knowledge doc
    custom_chips:           List[str] = field(default_factory=list) # Custom chips from matched rule/engine


# ── Provider Base (Plug-in architecture) ──────────────────────────────────────

class BaseSuggestionProvider:
    """Pluggable base class for suggestion providers."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        raise NotImplementedError("Suggestion providers must implement get_suggestions()")


# ── Provider Implementations ──────────────────────────────────────────────────

class WelcomeProvider(BaseSuggestionProvider):
    """Provides initial chips when user greets realBOT or conversation is new."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        if context.intent == 'greeting' or context.conversation_state == 'welcome':
            return list(SuggestionDefinition.objects.filter(category='Welcome', status='active'))
        return []


class RuleEngineProvider(BaseSuggestionProvider):
    """Provides suggestions mapped directly to the current intent."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        if not context.intent or context.intent == 'unknown_intent':
            return []
        
        # Match trigger condition e.g. {"intent": "buy_property"}
        results = []
        candidates = SuggestionDefinition.objects.filter(status='active')
        for item in candidates:
            cond = item.trigger_condition or {}
            if cond.get('intent') == context.intent:
                results.append(item)
        return results


class ServiceProvider(BaseSuggestionProvider):
    """Provides service-specific actions when a Service Profile is active."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        if not context.active_service_profile:
            return []
        results = []
        candidates = SuggestionDefinition.objects.filter(category='Service', status='active')
        for item in candidates:
            cond = item.trigger_condition or {}
            if cond.get('service_profile') == context.active_service_profile:
                results.append(item)
        return results


class KnowledgeProvider(BaseSuggestionProvider):
    """Provides follow-up documentation suggestions after a knowledge query."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        if context.knowledge_resolved:
            return list(SuggestionDefinition.objects.filter(category='Knowledge', status='active'))
        return []


class InquiryProvider(BaseSuggestionProvider):
    """Provides suggestions during active inquiry collection or confirmation."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        if context.inquiry_state == 'collecting_information':
            return list(SuggestionDefinition.objects.filter(category='Inquiry', status='active'))
        return []


class NavigationProvider(BaseSuggestionProvider):
    """Provides suggestions based on the active website page the customer is viewing."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        if not context.current_page:
            return []
        results = []
        candidates = SuggestionDefinition.objects.filter(category__in=['Navigation', 'Contact', 'Inquiry'], status='active')
        for item in candidates:
            cond = item.trigger_condition or {}
            if cond.get('page') == context.current_page:
                results.append(item)
        return results


class ContactProvider(BaseSuggestionProvider):
    """Provides quick contact/escalation options on fallback or explicit contact intents."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        if context.intent in ('contact_information', 'human_assistance', 'unknown_intent'):
            return list(SuggestionDefinition.objects.filter(category='Contact', status='active'))
        return []


class ConversationRecoveryProvider(BaseSuggestionProvider):
    """Provides fallback options on unknown/unresolved intent."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        if context.intent == 'unknown_intent':
            return list(SuggestionDefinition.objects.filter(category='Recovery', status='active'))
        return []


class CompletionProvider(BaseSuggestionProvider):
    """Provides post-submission journeys after inquiry creation."""
    def get_suggestions(self, context: SuggestionContext) -> List[SuggestionDefinition]:
        if context.inquiry_state == 'submitted':
            return list(SuggestionDefinition.objects.filter(category='Completion', status='active'))
        return []


# ── Ranking & Deduplication Engines ───────────────────────────────────────────

class SuggestionRankingEngine:
    """Sorts suggestions by priority (lower number = higher) then order."""
    def rank(self, items: List[SuggestionDefinition]) -> List[SuggestionDefinition]:
        # display_priority (asc), display_order (asc), display_text (alphabetical)
        return sorted(
            items,
            key=lambda x: (x.display_priority, x.display_order, x.display_text.lower())
        )


class SuggestionDeduplicationEngine:
    """Filters duplicate display_text items, preserving the higher ranked ones."""
    def deduplicate(self, items: List[SuggestionDefinition]) -> List[SuggestionDefinition]:
        seen = set()
        deduped = []
        for item in items:
            key = item.display_text.strip().lower()
            if key not in seen:
                seen.add(key)
                deduped.append(item)
        return deduped


# ── Suggestion Engine Coordinator ─────────────────────────────────────────────

class SuggestionEngine:
    """
    Main Suggestion Coordinator.
    Loads and runs plug-in providers, ranks results, deduplicates,
    logs display interactions, and returns chip structures.
    """
    def __init__(self):
        self.providers = [
            WelcomeProvider(),
            RuleEngineProvider(),
            ServiceProvider(),
            KnowledgeProvider(),
            InquiryProvider(),
            NavigationProvider(),
            ContactProvider(),
            ConversationRecoveryProvider(),
            CompletionProvider(),
        ]
        self.ranking_engine = SuggestionRankingEngine()
        self.dedup_engine = SuggestionDeduplicationEngine()

    def get_suggestions(self, context: SuggestionContext, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Gathers suggestions, merges, ranks, deduplicates, and limits count.
        Returns a list of suggestion dicts suitable for client chips.
        """
        all_sugs = []
        for provider in self.providers:
            try:
                all_sugs.extend(provider.get_suggestions(context))
            except Exception as e:
                logger.error(f"[SuggestionEngine] Provider {provider.__class__.__name__} failed: {e}")

        # Rank
        ranked = self.ranking_engine.rank(all_sugs)

        # Deduplicate
        deduped = self.dedup_engine.deduplicate(ranked)

        # Apply visibility rules (e.g., checking page URL)
        visible = []
        for item in deduped:
            rules = item.visibility_rules or {}
            allowed_pages = rules.get('allowed_pages', [])
            if allowed_pages and context.current_page not in allowed_pages:
                continue
            visible.append(item)

        # Truncate to limit
        final_sugs = visible[:limit]

        # Log rendered events to Interaction Log for analytics (M2.7)
        if context.session:
            self._log_renders(context.session, final_sugs)

        # Convert to serialized chip dictionaries
        # Merge custom chips from matched rule if any
        serialized = []
        existing_texts = set()

        # 1. Prepend custom rule chips first (highest priority)
        for chip_text in context.custom_chips:
            if chip_text.lower() not in existing_texts:
                serialized.append({
                    'suggestion_id': 'SUG_RULE_CHIP',
                    'display_text':  chip_text,
                    'category':      'RuleChip',
                    'intent':        'inquiry_creation' if 'inquiry' in chip_text.lower() else 'general_information',
                    'action':        'inquiry_creation' if 'inquiry' in chip_text.lower() else '',
                    'icon':          'circle',
                })
                existing_texts.add(chip_text.lower())

        # 2. Append DB suggestions next
        for item in final_sugs:
            if item.display_text.strip().lower() not in existing_texts:
                serialized.append({
                    'suggestion_id': item.suggestion_id,
                    'display_text':  item.display_text,
                    'category':      item.category,
                    'intent':        item.business_intent,
                    'action':        item.target_action,
                    'icon':          item.icon,
                })
                existing_texts.add(item.display_text.strip().lower())

        return serialized[:limit]

    def _log_renders(self, session, suggestions: List[SuggestionDefinition]):
        """Logs 'rendered' event in append-only log."""
        try:
            for item in suggestions:
                SuggestionInteractionLog.objects.create(
                    session=session,
                    suggestion_id=item.suggestion_id,
                    display_text=item.display_text,
                    category=item.category,
                    interaction_type='rendered'
                )
        except Exception as exc:
            logger.warning(f"[SuggestionEngine] Failed to log rendered suggestions: {exc}")
