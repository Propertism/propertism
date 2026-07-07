"""
chat/insights_manager.py — M2.16 Analytics & Customer Insights Framework.
Provides business intelligence, dashboards, reports, and recommendations.
"""
import csv
import io
import json
import logging
from typing import Any, Dict, List, Optional
from django.db.models import Count, Avg, Q, Min, Max
from django.utils import timezone
from dateutil.parser import parse as parse_date
from chat.models import PlatformEvent, RealBotSession, KnowledgeArticle, KnowledgeDocument

logger = logging.getLogger(__name__)

class BusinessAnalyticsManager:
    """Central facade orchestrating customer journeys, inquiries, knowledge and conversion analytics."""

    def __init__(self, filters: Optional[Dict[str, Any]] = None):
        self.filters = filters or {}
        self.base_qs = PlatformEvent.objects.all()
        self._apply_filters()

    def _apply_filters(self):
        # 1. Configurable Date Ranges
        start_date = self.filters.get('start_date')
        end_date = self.filters.get('end_date')
        if start_date:
            try:
                dt_start = parse_date(start_date) if isinstance(start_date, str) else start_date
                if timezone.is_naive(dt_start):
                    dt_start = timezone.make_aware(dt_start)
                self.base_qs = self.base_qs.filter(created_at__gte=dt_start)
            except Exception as e:
                logger.warning(f"Invalid start_date filter '{start_date}': {e}")

        if end_date:
            try:
                dt_end = parse_date(end_date) if isinstance(end_date, str) else end_date
                if timezone.is_naive(dt_end):
                    dt_end = timezone.make_aware(dt_end)
                self.base_qs = self.base_qs.filter(created_at__lte=dt_end)
            except Exception as e:
                logger.warning(f"Invalid end_date filter '{end_date}': {e}")

        # 2. Country Filters
        country = self.filters.get('country')
        if country:
            # Match payload__country, payload__country_code or direct payload details
            self.base_qs = self.base_qs.filter(
                Q(payload__country__iexact=country) |
                Q(payload__country_code__iexact=country) |
                Q(payload__country_name__iexact=country)
            )

        # 3. Service Filters
        service = self.filters.get('service')
        if service:
            # Match payload__service_code, payload__service_name or payload__intent_name
            self.base_qs = self.base_qs.filter(
                Q(payload__service_code__iexact=service) |
                Q(payload__service_name__iexact=service) |
                Q(payload__service__iexact=service) |
                Q(payload__intent_name__iexact=service)
            )

    def get_executive_summary(self) -> Dict[str, Any]:
        """Provides high level summarized business metrics."""
        total_convs = self.base_qs.filter(event_type='conversation_start').count()
        unique_visitors = self.base_qs.values('session_id').distinct().count()

        inquiry_initiated = self.base_qs.filter(event_type='inquiry_initiated').count()
        inquiry_completed = self.base_qs.filter(event_type='inquiry_submitted').count()
        conversion_rate = (inquiry_completed / total_convs * 100.0) if total_convs > 0 else 0.0

        searches = self.base_qs.filter(event_type='knowledge_search').count()
        failed_searches = self.base_qs.filter(event_type='failed_search').count()
        knowledge_coverage = ((searches - failed_searches) / searches * 100.0) if searches > 0 else 0.0

        suggestions_displayed = self.base_qs.filter(event_type='suggestion_displayed').count()
        suggestions_clicked = self.base_qs.filter(event_type='suggestion_clicked').count()
        suggestions_ctr = (suggestions_clicked / suggestions_displayed * 100.0) if suggestions_displayed > 0 else 0.0

        return {
            'total_conversations': total_convs,
            'unique_visitors': unique_visitors,
            'inquiry_initiations': inquiry_initiated,
            'inquiry_completions': inquiry_completed,
            'inquiry_conversion_rate': round(conversion_rate, 2),
            'knowledge_coverage_rate': round(knowledge_coverage, 2),
            'suggestion_ctr': round(suggestions_ctr, 2),
        }

    def build_dashboard_data(self) -> Dict[str, Any]:
        """Assembles data for all 8 business dashboards."""
        return {
            'executive': self.get_executive_summary(),
            'customer_journey': CustomerJourneyAnalyzer(self.base_qs).analyze(),
            'inquiry': InquiryAnalyticsManager(self.base_qs).analyze(),
            'knowledge': KnowledgeAnalyticsManager(self.base_qs).analyze(),
            'service': ServiceAnalyticsManager(self.base_qs).analyze(),
            'conversation': ConversationOutcomeAnalyzer(self.base_qs).analyze(),
            'search': SearchAnalyticsManager(self.base_qs).analyze(),
            'conversion': ConversionAnalyticsManager(self.base_qs).analyze(),
        }


# ─────────────────────────────────────────────────────────────────────────────
# 1. Customer Journey Analyzer
# ─────────────────────────────────────────────────────────────────────────────

class CustomerJourneyAnalyzer:
    """Analyzes customer session lifecycle, unique visitors, durations, and drop-offs."""

    def __init__(self, qs):
        self.qs = qs

    def analyze(self) -> Dict[str, Any]:
        total_convs = self.qs.filter(event_type='conversation_start').count()
        sessions = self.qs.values('session_id').distinct()
        unique_visitors = sessions.count()

        # Returning visitors: count distinct session_ids that have > 1 conversation_start event
        session_convs = self.qs.filter(event_type='conversation_start').values('session_id').annotate(
            count=Count('event_id')
        ).filter(count__gt=1)
        returning_visitors = session_convs.count()

        # Conversation duration
        durations = self.qs.filter(event_type='session_closed').aggregate(avg=Avg('duration_ms'))['avg']
        avg_duration = (durations / 1000.0) if durations else 0.0

        # Session completion vs drop-off
        inquiry_initiated = self.qs.filter(event_type='inquiry_initiated').count()
        inquiry_completed = self.qs.filter(event_type='inquiry_submitted').count()
        completion_rate = (inquiry_completed / inquiry_initiated * 100.0) if inquiry_initiated > 0 else 0.0
        dropoff_rate = 100.0 - completion_rate if inquiry_initiated > 0 else 0.0

        # Funnel analysis per provider stage
        stages = ['welcome', 'rule', 'service', 'knowledge', 'inquiry', 'suggestion']
        dropoffs = {}
        for stage in stages:
            events = self.qs.filter(provider=stage).count()
            dropoffs[stage] = events

        return {
            'total_conversations': total_convs,
            'unique_visitors': unique_visitors,
            'returning_visitors': returning_visitors,
            'avg_conversation_duration_seconds': round(avg_duration, 2),
            'session_completion_rate': round(completion_rate, 2),
            'session_dropoff_rate': round(dropoff_rate, 2),
            'stage_dropoff_distribution': dropoffs,
        }


# ─────────────────────────────────────────────────────────────────────────────
# 2. Inquiry Analytics Manager
# ─────────────────────────────────────────────────────────────────────────────

class InquiryAnalyticsManager:
    """Monitors inquiry funnels, field completion drop-offs, and distributions."""

    def __init__(self, qs):
        self.qs = qs

    def analyze(self) -> Dict[str, Any]:
        initiated = self.qs.filter(event_type='inquiry_initiated').count()
        completed = self.qs.filter(event_type='inquiry_submitted').count()
        abandoned = max(0, initiated - completed)
        abandoned_rate = (abandoned / initiated * 100.0) if initiated > 0 else 0.0

        # Mandatory Field Completion
        field_completions = {}
        fields_recorded = self.qs.filter(event_type='inquiry_field_recorded')
        for f in fields_recorded:
            fname = f.payload.get('field_name')
            if fname:
                field_completions[fname] = field_completions.get(fname, 0) + 1

        # Country distribution
        countries = {}
        country_events = self.qs.filter(event_type='inquiry_initiated').values('payload__country').annotate(
            count=Count('event_id')
        )
        for c in country_events:
            cname = c.get('payload__country') or 'Unknown'
            countries[cname] = c['count']

        # Service distribution
        services = {}
        service_events = self.qs.filter(event_type='inquiry_initiated').values('payload__service_code').annotate(
            count=Count('event_id')
        )
        for s in service_events:
            sname = s.get('payload__service_code') or 'Unknown'
            services[sname] = s['count']

        return {
            'inquiry_initiated': initiated,
            'inquiry_completed': completed,
            'inquiry_abandoned': abandoned,
            'inquiry_abandoned_rate': round(abandoned_rate, 2),
            'mandatory_field_completion_counts': field_completions,
            'country_distribution': countries,
            'service_distribution': services,
        }


# ─────────────────────────────────────────────────────────────────────────────
# 3. Knowledge Analytics Manager
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgeAnalyticsManager:
    """Evaluates knowledge base article queries, failures, coverage, and quality score trends."""

    def __init__(self, qs):
        self.qs = qs

    def analyze(self) -> Dict[str, Any]:
        searches = self.qs.filter(event_type='knowledge_search').count()
        failed_searches = self.qs.filter(event_type='failed_search').count()
        coverage_rate = ((searches - failed_searches) / searches * 100.0) if searches > 0 else 0.0

        # Most viewed articles
        most_viewed = {}
        views = self.qs.filter(event_type='article_resolved').values('payload__article_title').annotate(
            count=Count('event_id')
        ).order_by('-count')[:5]
        for v in views:
            title = v['payload__article_title']
            if title:
                most_viewed[title] = v['count']

        # Least viewed articles (computed from total articles in DB minus views)
        all_articles = KnowledgeArticle.objects.values_list('page_title', flat=True)
        least_viewed = {}
        for title in all_articles[:5]:
            least_viewed[title] = most_viewed.get(title, 0)

        # Missing knowledge requests
        missing_requests = []
        failed_events = self.qs.filter(event_type='failed_search')[:5]
        for f in failed_events:
            query = f.payload.get('query')
            if query:
                missing_requests.append(query)

        # Knowledge Quality Trends (averages of quality scores recorded)
        qualities = self.qs.filter(event_type='quality_validated').aggregate(avg=Avg('payload__quality_score'))['avg']
        quality_avg = qualities if qualities else 0.0

        return {
            'knowledge_searches': searches,
            'failed_knowledge_searches': failed_searches,
            'knowledge_coverage_percentage': round(coverage_rate, 2),
            'most_viewed_articles': most_viewed,
            'least_viewed_articles': least_viewed,
            'missing_knowledge_requests': missing_requests,
            'knowledge_quality_average': round(quality_avg, 2),
        }


# ─────────────────────────────────────────────────────────────────────────────
# 4. Service Analytics Manager
# ─────────────────────────────────────────────────────────────────────────────

class ServiceAnalyticsManager:
    """Measures service profile trigger volume, conversion rates, and abandonment."""

    def __init__(self, qs):
        self.qs = qs

    def analyze(self) -> Dict[str, Any]:
        # Most requested service profiles
        services_requested = {}
        triggers = self.qs.filter(event_type='service_triggered').values('payload__service_code').annotate(
            count=Count('event_id')
        ).order_by('-count')
        for t in triggers:
            code = t['payload__service_code']
            if code:
                services_requested[code] = t['count']

        # Service Conversion and Abandonment
        conversions = {}
        abandonment = {}
        for code, count in services_requested.items():
            completed = self.qs.filter(
                event_type='inquiry_submitted',
                payload__service_code=code
            ).count()
            conversions[code] = round((completed / count * 100.0) if count > 0 else 0.0, 2)
            abandonment[code] = max(0, count - completed)

        # Popular entry pages (e.g. from session start URLs)
        entry_pages = {}
        entry_events = self.qs.filter(event_type='conversation_start').values('payload__referrer').annotate(
            count=Count('event_id')
        ).order_by('-count')[:5]
        for e in entry_events:
            ref = e['payload__referrer'] or '/'
            entry_pages[ref] = e['count']

        return {
            'services_requested': services_requested,
            'service_conversion_rates': conversions,
            'service_abandonment_counts': abandonment,
            'popular_entry_pages': entry_pages,
        }


# ─────────────────────────────────────────────────────────────────────────────
# 5. Conversation Outcome Analyzer
# ─────────────────────────────────────────────────────────────────────────────

class ConversationOutcomeAnalyzer:
    """Aggregates conversation ending flags and resolved statuses."""

    def __init__(self, qs):
        self.qs = qs

    def analyze(self) -> Dict[str, Any]:
        total = self.qs.filter(event_type='conversation_start').count()
        answered = self.qs.filter(event_type='response_composed').count()
        inquiries = self.qs.filter(event_type='inquiry_submitted').count()
        escalated = self.qs.filter(event_type='human_requested').count()
        navigated = self.qs.filter(event_type='action_executed').count()
        cancelled = self.qs.filter(event_type='inquiry_cancelled').count()

        return {
            'total_conversations': total,
            'successfully_answered': answered,
            'inquiry_generated': inquiries,
            'escalated_to_human': escalated,
            'navigation_assisted': navigated,
            'conversation_cancelled': cancelled,
        }


# ─────────────────────────────────────────────────────────────────────────────
# 6. Search Analytics Manager
# ─────────────────────────────────────────────────────────────────────────────

class SearchAnalyticsManager:
    """Tacks search query frequencies, zero-result searches, synonyms, and refinements."""

    def __init__(self, qs):
        self.qs = qs

    def analyze(self) -> Dict[str, Any]:
        # Top search terms
        terms = {}
        searches = self.qs.filter(event_type='knowledge_search').values('payload__query').annotate(
            count=Count('event_id')
        ).order_by('-count')[:10]
        for s in searches:
            q = s['payload__query']
            if q:
                terms[q] = s['count']

        # Zero result searches
        zero_results = {}
        failed = self.qs.filter(event_type='failed_search').values('payload__query').annotate(
            count=Count('event_id')
        ).order_by('-count')[:10]
        for f in failed:
            q = f['payload__query']
            if q:
                zero_results[q] = f['count']

        # Synonym Usage and Search Refinements (refinements = multiple searches in same session)
        synonyms = self.qs.filter(event_type='knowledge_search', payload__synonym_matched=True).count()

        refinement_sessions = self.qs.filter(event_type='knowledge_search').values('session_id').annotate(
            count=Count('event_id')
        ).filter(count__gt=1).count()

        return {
            'top_search_terms': terms,
            'zero_result_searches': zero_results,
            'synonym_usage_count': synonyms,
            'search_refinements_sessions': refinement_sessions,
        }


# ─────────────────────────────────────────────────────────────────────────────
# 7. Conversion Analytics Manager
# ─────────────────────────────────────────────────────────────────────────────

class ConversionAnalyticsManager:
    """Aggregates click through rates and conversion triggers across components."""

    def __init__(self, qs):
        self.qs = qs

    def analyze(self) -> Dict[str, Any]:
        # Suggestion click rate
        s_disp = self.qs.filter(event_type='suggestion_displayed').count()
        s_click = self.qs.filter(event_type='suggestion_clicked').count()
        s_ctr = (s_click / s_disp * 100.0) if s_disp > 0 else 0.0

        # Action (whatsapp/phone/maps) clicks
        action_clicks = {
            'whatsapp': self.qs.filter(event_type='action_executed', payload__action_name='whatsapp').count(),
            'phone_call': self.qs.filter(event_type='action_executed', payload__action_name='phone_call').count(),
            'google_maps': self.qs.filter(event_type='action_executed', payload__action_name='google_maps').count(),
            'linkedin': self.qs.filter(event_type='action_executed', payload__action_name='linkedin').count(),
            'government_service': self.qs.filter(event_type='action_executed', payload__action_name__icontains='gov').count(),
        }

        return {
            'suggestion_ctr': round(s_ctr, 2),
            'action_clicks': action_clicks,
        }


# ─────────────────────────────────────────────────────────────────────────────
# 8. Report Generator, Export Framework & Insight Engine
# ─────────────────────────────────────────────────────────────────────────────

class ReportGenerator:
    """Compiles tabular reports for download/export operations."""

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def generate_csv_report(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Metric Category', 'Metric Key', 'Metric Value'])

        # Flattens nested dictionary to tabular CSV format
        for category, metrics in self.data.items():
            if isinstance(metrics, dict):
                for key, val in metrics.items():
                    writer.writerow([category, key, json.dumps(val) if isinstance(val, (dict, list)) else val])
            else:
                writer.writerow(['general', category, metrics])

        return output.getvalue()


class InsightEngine:
    """Analyses metrics indicators and yields business insight recommendations."""

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def generate_recommendations(self) -> List[Dict[str, Any]]:
        recs = []

        # Rule 1: High Inquiry Abandonment
        inquiry = self.data.get('inquiry', {})
        initiated = inquiry.get('inquiry_initiated', 0)
        abandoned_rate = inquiry.get('inquiry_abandoned_rate', 0.0)
        if initiated > 5 and abandoned_rate > 40.0:
            recs.append({
                'id': 'REC001',
                'severity': 'high',
                'category': 'Inquiry Funnel',
                'observation': f"Inquiry abandonment rate is very high ({abandoned_rate}%).",
                'recommendation': "Reduce the number of mandatory fields in your inquiry creation steps to prevent friction.",
            })

        # Rule 2: Low Search Coverage
        knowledge = self.data.get('knowledge', {})
        searches = knowledge.get('knowledge_searches', 0)
        coverage = knowledge.get('knowledge_coverage_percentage', 100.0)
        if searches > 5 and coverage < 70.0:
            recs.append({
                'id': 'REC002',
                'severity': 'medium',
                'category': 'Knowledge Base',
                'observation': f"Search coverage is low ({coverage}%).",
                'recommendation': f"Analyze failed queries: {', '.join(knowledge.get('missing_knowledge_requests', []))}. Add matching articles.",
            })

        # Rule 3: Low Suggestion Click Through Rate
        conversion = self.data.get('conversion', {})
        ctr = conversion.get('suggestion_ctr', 100.0)
        if ctr < 15.0:
            recs.append({
                'id': 'REC003',
                'severity': 'low',
                'category': 'User Experience',
                'observation': f"Suggestion chips Click-Through Rate is low ({ctr}%).",
                'recommendation': "Reposition suggestion chips dynamically or review chip label relevance to match typical user goals.",
            })

        # Default fallback recommendation
        if not recs:
            recs.append({
                'id': 'REC000',
                'severity': 'low',
                'category': 'Operational',
                'observation': "All core metrics are performing within normal operational boundaries.",
                'recommendation': "Continue monitoring telemetry to establish seasonal baselines.",
            })

        return recs
