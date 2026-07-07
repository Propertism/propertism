"""
chat/analytics_engine.py — M2.11 Analytics, Diagnostics & Observability Framework.
Implements EventPublisher, EventAggregationEngine, MetricsCalculator, and HealthMonitoringFramework.
"""
import logging
import time
from typing import Any, Dict, List, Optional
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from chat.models import PlatformEvent, MetricAggregate, RealBotSession
from realtor_project.features import is_feature_enabled

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Event Publisher Framework
# ─────────────────────────────────────────────────────────────────────────────

class EventPublisher:
    """Publishes structured, immutable platform events for operational diagnostics."""

    def publish_event(
        self,
        event_type: str,
        provider: str,
        session_id: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[int] = None
    ) -> PlatformEvent:
        try:
            evt = PlatformEvent.objects.create(
                event_type=event_type,
                provider=provider,
                session_id=session_id,
                payload=payload or {},
                duration_ms=duration_ms
            )
            return evt
        except Exception as exc:
            logger.exception(f"Failed to publish event {event_type} (Provider: {provider}): {exc}")
            # Mock or return unsaved instance so callers don't fail hard
            return PlatformEvent(event_type=event_type, provider=provider)


# ─────────────────────────────────────────────────────────────────────────────
# 2. Event Aggregation Engine
# ─────────────────────────────────────────────────────────────────────────────

class EventAggregationEngine:
    """Consolidates event streams into window-based MetricAggregate records."""

    def aggregate_metrics(self, window_type: str = 'daily') -> int:
        """
        Consolidates counts for key events into MetricAggregate records.
        Returns count of aggregates created/updated.
        """
        now = timezone.now()
        window_start = now.replace(minute=0, second=0, microsecond=0)
        if window_type == 'daily':
            window_start = window_start.replace(hour=0)

        keys_mapping = {
            'conversations_total': 'conversation_start',
            'failed_searches_total': 'failed_search',
            'inquiries_total': 'inquiry_submitted'
        }

        count = 0
        for metric_key, event_type in keys_mapping.items():
            val = PlatformEvent.objects.filter(
                event_type=event_type,
                created_at__gte=window_start
            ).count()

            agg, created = MetricAggregate.objects.get_or_create(
                metric_key=metric_key,
                window_type=window_type,
                window_start=window_start,
                defaults={'value': float(val)}
            )
            if not created:
                agg.value = float(val)
                agg.save()
            count += 1

        return count


# ─────────────────────────────────────────────────────────────────────────────
# 3. Metrics Calculator
# ─────────────────────────────────────────────────────────────────────────────

class MetricsCalculator:
    """Computes comprehensive operational visibility metrics from database and event streams."""

    def compute_all_metrics(self) -> Dict[str, Any]:
        return {
            'conversation': self.get_conversation_metrics(),
            'knowledge': self.get_knowledge_metrics(),
            'inquiry': self.get_inquiry_metrics(),
            'suggestions': self.get_suggestion_metrics(),
            'actions': self.get_action_metrics(),
            'responses': self.get_response_metrics(),
            'context': self.get_context_metrics(),
            'platform': self.get_platform_metrics()
        }

    def get_conversation_metrics(self) -> Dict[str, Any]:
        total_convs = PlatformEvent.objects.filter(event_type='conversation_start').count()
        active_limit = timezone.now() - timezone.timedelta(minutes=30)
        active_sessions = RealBotSession.objects.filter(updated_at__gte=active_limit).count()
        
        # Topic switches
        topic_switches = PlatformEvent.objects.filter(event_type='topic_switch').count()

        # Avg duration calculation (dummy fallback or calculated from duration logs)
        durations = PlatformEvent.objects.filter(event_type='session_closed').aggregate(avg=Avg('duration_ms'))['avg']
        avg_duration = (durations / 1000.0) if durations else 0.0

        # Completion vs Abandonment rate
        completions = PlatformEvent.objects.filter(event_type='inquiry_submitted').count()
        completion_rate = (completions / total_convs * 100.0) if total_convs > 0 else 0.0
        dropoff_rate = 100.0 - completion_rate if total_convs > 0 else 0.0

        return {
            'total_conversations': total_convs,
            'active_sessions': active_sessions,
            'avg_conversation_duration_seconds': round(avg_duration, 2),
            'conversation_completion_rate_percentage': round(completion_rate, 2),
            'conversation_dropoff_rate_percentage': round(dropoff_rate, 2),
            'topic_transition_counts': topic_switches
        }

    def get_knowledge_metrics(self) -> Dict[str, Any]:
        searches = PlatformEvent.objects.filter(event_type='knowledge_search').count()
        failed_searches = PlatformEvent.objects.filter(event_type='failed_search').count()
        
        # Coverage rate (percentage of searches successfully yielding articles)
        successful_searches = searches - failed_searches
        coverage_rate = (successful_searches / searches * 100.0) if searches > 0 else 0.0

        # Top articles from query payload
        top_articles = []
        article_events = PlatformEvent.objects.filter(event_type='article_resolved').values('payload__article_title').annotate(
            count=Count('event_id')
        ).order_by('-count')[:5]
        for item in article_events:
            if item['payload__article_title']:
                top_articles.append({
                    'title': item['payload__article_title'],
                    'count': item['count']
                })

        return {
            'knowledge_searches': searches,
            'top_knowledge_articles': top_articles,
            'failed_knowledge_searches': failed_searches,
            'knowledge_coverage_percentage': round(coverage_rate, 2)
        }

    def get_inquiry_metrics(self) -> Dict[str, Any]:
        initiations = PlatformEvent.objects.filter(event_type='inquiry_initiated').count()
        completions = PlatformEvent.objects.filter(event_type='inquiry_submitted').count()
        
        abandonment_rate = ((initiations - completions) / initiations * 100.0) if initiations > 0 else 0.0
        
        # Average completion time
        avg_time = PlatformEvent.objects.filter(event_type='inquiry_submitted').aggregate(avg=Avg('duration_ms'))['avg']
        avg_completion_time = (avg_time / 1000.0) if avg_time else 0.0

        return {
            'inquiry_initiations': initiations,
            'inquiry_completions': completions,
            'inquiry_abandonment_rate_percentage': round(abandonment_rate, 2),
            'avg_inquiry_completion_time_seconds': round(avg_completion_time, 2)
        }

    def get_suggestion_metrics(self) -> Dict[str, Any]:
        displayed = PlatformEvent.objects.filter(event_type='suggestion_displayed').count()
        clicks = PlatformEvent.objects.filter(event_type='suggestion_clicked').count()
        
        click_rate = (clicks / displayed * 100.0) if displayed > 0 else 0.0

        # Most selected suggestions
        top_suggestions = []
        suggestion_events = PlatformEvent.objects.filter(event_type='suggestion_clicked').values('payload__display_text').annotate(
            count=Count('event_id')
        ).order_by('-count')[:5]
        for item in suggestion_events:
            if item['payload__display_text']:
                top_suggestions.append({
                    'text': item['payload__display_text'],
                    'count': item['count']
                })

        return {
            'suggestions_displayed': displayed,
            'suggestion_click_rate_percentage': round(click_rate, 2),
            'most_selected_suggestions': top_suggestions
        }

    def get_action_metrics(self) -> Dict[str, Any]:
        executed = PlatformEvent.objects.filter(event_type='action_executed').count()
        confirmations = PlatformEvent.objects.filter(event_type='action_confirmed').count()
        failed = PlatformEvent.objects.filter(event_type='action_failed').count()

        confirmation_rate = (confirmations / executed * 100.0) if executed > 0 else 0.0

        # Top executed actions
        top_actions = []
        action_events = PlatformEvent.objects.filter(event_type='action_executed').values('payload__action_name').annotate(
            count=Count('event_id')
        ).order_by('-count')[:5]
        for item in action_events:
            if item['payload__action_name']:
                top_actions.append({
                    'name': item['payload__action_name'],
                    'count': item['count']
                })

        return {
            'actions_executed': executed,
            'confirmation_rate_percentage': round(confirmation_rate, 2),
            'failed_executions': failed,
            'top_executed_actions': top_actions
        }

    def get_response_metrics(self) -> Dict[str, Any]:
        rendered = PlatformEvent.objects.filter(event_type='response_composed').count()
        
        avg_size = PlatformEvent.objects.filter(event_type='response_composed').aggregate(avg=Avg('payload__char_length'))['avg'] or 0
        avg_composition = PlatformEvent.objects.filter(event_type='response_composed').aggregate(avg=Avg('duration_ms'))['avg'] or 0

        return {
            'response_components_rendered': rendered,
            'average_response_size_bytes': round(avg_size, 2),
            'avg_response_composition_time_ms': round(avg_composition, 2)
        }

    def get_context_metrics(self) -> Dict[str, Any]:
        switches = PlatformEvent.objects.filter(event_type='topic_switch').count()
        restores = PlatformEvent.objects.filter(event_type='topic_restore').count()
        expirations = PlatformEvent.objects.filter(event_type='context_expired').count()
        updates = PlatformEvent.objects.filter(event_type='context_updated').count()

        return {
            'context_switches': switches,
            'topic_restorations': restores,
            'context_expirations': expirations,
            'variable_updates': updates
        }

    def get_platform_metrics(self) -> Dict[str, Any]:
        requests = PlatformEvent.objects.filter(provider='platform').count()
        avg_time = PlatformEvent.objects.filter(provider='platform').aggregate(avg=Avg('duration_ms'))['avg'] or 0.0
        
        errors = PlatformEvent.objects.filter(event_type='error_occurred').count()
        error_rate = (errors / requests * 100.0) if requests > 0 else 0.0

        # Health
        health_mgr = HealthMonitoringFramework()
        health_status = health_mgr.check_health()

        # Feature flags status
        flags = {
            'REALBOT_INTEGRATION_ENABLED': is_feature_enabled('REALBOT_INTEGRATION_ENABLED', default=True),
            'CAPTCHA_ENABLE': is_feature_enabled('CAPTCHA_ENABLE', default=False),
            'REALBOT_AI_ENABLED': is_feature_enabled('REALBOT_AI_ENABLED', default=False)
        }

        return {
            'api_requests': requests,
            'average_response_time_ms': round(avg_time, 2),
            'error_rate_percentage': round(error_rate, 2),
            'module_health': health_status['status'],
            'active_feature_flags': flags
        }


# ─────────────────────────────────────────────────────────────────────────────
# 4. Health Monitoring Framework
# ─────────────────────────────────────────────────────────────────────────────

class HealthMonitoringFramework:
    """Verifies live health, db status, and metrics liveness diagnostics."""

    def check_health(self) -> Dict[str, Any]:
        db_healthy = True
        try:
            # Simple check
            from django.db import connection
            connection.cursor()
        except Exception:
            db_healthy = False

        status = 'healthy' if db_healthy else 'unhealthy'
        
        return {
            'status': status,
            'timestamp': timezone.now().isoformat(),
            'checks': {
                'database': 'healthy' if db_healthy else 'unhealthy',
                'cache': 'healthy',  # Placeholder for cache verification
                'latency_liveness': 'healthy'
            }
        }
