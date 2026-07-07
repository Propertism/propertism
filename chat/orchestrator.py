"""
chat/orchestrator.py — M2.13 Conversation Orchestration & Workflow Engine.
Coordinates subsystems: security validation, session check, context resolution, rule engine,
                       knowledge search, services, inquiry flow, suggestions, actions,
                       response composition, output validation, response delivery, and analytics.
"""
import time
import logging
from typing import Any, Dict, List, Optional
from django.utils import timezone
from chat.models import OrchestrationWorkflow, WorkflowExecutionStep, RealBotSession, RealBotMessage
from chat.config_manager import ConfigurationManager
from chat.context_manager import ConversationContextManager
from chat.inquiry_engine import InquiryConversationEngine
from chat.analytics_engine import EventPublisher
from chat.security_manager import SecurityManager

logger = logging.getLogger(__name__)


class ConversationOrchestrator:
    """Central Orchestrator and single entry point gateway for all customer conversation messages."""

    def __init__(self):
        self.publisher = EventPublisher()
        self.security = SecurityManager()

    def process_message(
        self,
        session_id: str,
        message_text: str,
        page_path: str = '/home/',
        category: str = 'General'
    ) -> Dict[str, Any]:
        """
        Coordinates the 13-stage conversation execution pipeline.
        Isolates module failures, tracks execution times, and stores workflow step traces.
        """
        # Create immutable workflow trace record
        workflow = OrchestrationWorkflow.objects.create(
            session_id=session_id,
            state='Processing',
            payload={
                'message_text': message_text,
                'page_path': page_path,
                'category': category
            }
        )

        pipeline_stages = [
            ('Security Validation', self._stage_security_validation),
            ('Session Validation', self._stage_session_validation),
            ('Context Resolution', self._stage_context_resolution),
            ('Rule Engine', self._stage_rule_engine),
            ('Knowledge Resolution', self._stage_knowledge_resolution),
            ('Service Resolution', self._stage_service_resolution),
            ('Inquiry Processing', self._stage_inquiry_processing),
            ('Suggestion Generation', self._stage_suggestion_generation),
            ('Navigation Resolution', self._stage_navigation_resolution),
            ('Action Resolution', self._stage_action_resolution),
            ('Response Composition', self._stage_response_composition),
            ('Output Validation', self._stage_output_validation),
            ('Response Delivery', self._stage_response_delivery),
            ('Analytics Publishing', self._stage_analytics_publishing),
            ('Workflow Completion', self._stage_workflow_completion)
        ]

        workflow.payload['stages_executed'] = []
        workflow.save()

        # Shared execution context across stages
        exec_ctx = {
            'workflow': workflow,
            'session_id': session_id,
            'message_text': message_text,
            'page_path': page_path,
            'category': category,
            'session_obj': None,
            'context_obj': None,
            'intent': None,
            'reply_text': '',
            'cards': [],
            'suggestions': [],
            'actions': [],
            'error_occurred': False
        }

        # Central Execution Loop
        for stage_name, stage_fn in pipeline_stages:
            workflow.current_stage = stage_name
            workflow.save()

            start_time = time.perf_counter()
            status = 'success'
            logs = ''

            try:
                stage_fn(exec_ctx)
                logs = f"Successfully executed stage: {stage_name}"
            except Exception as exc:
                logger.exception(f"Error in orchestration stage '{stage_name}': {exc}")
                status = 'failed'
                logs = f"Exception occurred: {str(exc)}"
                exec_ctx['error_occurred'] = True
                
                # Check for critical session check failures
                if stage_name == 'Session Validation':
                    # Session missing, we must abort the loop
                    exec_ctx['reply_text'] = "Error: Invalid session reference."
                    WorkflowExecutionStep.objects.create(
                        workflow=workflow,
                        stage=stage_name,
                        status='failed',
                        duration_ms=int((time.perf_counter() - start_time) * 1000),
                        logs=logs
                    )
                    break

            duration_ms = int((time.perf_counter() - start_time) * 1000)
            WorkflowExecutionStep.objects.create(
                workflow=workflow,
                stage=stage_name,
                status=status,
                duration_ms=duration_ms,
                logs=logs
            )

            workflow.payload['stages_executed'].append({
                'stage': stage_name,
                'status': status,
                'duration_ms': duration_ms
            })
            workflow.save()

        # Update final state
        if exec_ctx['error_occurred'] and not exec_ctx['reply_text']:
            workflow.state = 'Failed'
            exec_ctx['reply_text'] = "We are experiencing technical difficulties. Please try again shortly."
        else:
            workflow.state = 'Completed'
        
        workflow.payload['final_reply'] = exec_ctx['reply_text']
        workflow.payload['suggestions'] = exec_ctx['suggestions']
        workflow.save()

        return {
            'workflow_id': workflow.workflow_id,
            'state': workflow.state,
            'reply_text': exec_ctx['reply_text'],
            'suggestions': exec_ctx['suggestions'],
            'cards': exec_ctx['cards']
        }

    # ─────────────────────────────────────────────────────────────────────────
    # Pipeline Stage Implementations
    # ─────────────────────────────────────────────────────────────────────────

    def _stage_security_validation(self, ctx: Dict[str, Any]) -> None:
        """M2.14 — Pre-orchestration security validation stage."""
        result = self.security.validate_request({
            'session_id': ctx['session_id'],
            'message_text': ctx['message_text'],
            'source_ip': ctx.get('source_ip', ''),
            'request_path': ctx.get('page_path', '')
        })
        # Apply sanitized message
        ctx['message_text'] = result.get('sanitized_message', ctx['message_text'])
        ctx['security_result'] = result
        if not result['is_valid']:
            logger.warning(f"Security validation failed: {result['violations']}")

    def _stage_session_validation(self, ctx: Dict[str, Any]) -> None:
        try:
            session = RealBotSession.objects.get(session_id=ctx['session_id'])
            ctx['session_obj'] = session
        except Exception:
            raise ValueError(f"Session {ctx['session_id']} not found in registry database.")

    def _stage_context_resolution(self, ctx: Dict[str, Any]) -> None:
        # Retrieve or initialize context
        context_mgr = ConversationContextManager()
        ctx['context_obj'] = context_mgr.get_or_create_context(ctx['session_id'])

    def _stage_rule_engine(self, ctx: Dict[str, Any]) -> None:
        # Execute routing rule checks
        from chat.rule_engine import RuleEngine
        engine = RuleEngine()
        res = engine.evaluate(ctx['message_text'])
        ctx['intent'] = res.intent
        
        if ctx['context_obj']:
            ctx['context_obj'].active_intent = res.intent
            ctx['context_obj'].save()

    def _stage_knowledge_resolution(self, ctx: Dict[str, Any]) -> None:
        # Query internal documents matches
        from chat.search import KnowledgeSearchEngine
        search_engine = KnowledgeSearchEngine()
        results = search_engine.search(ctx['message_text'])
        if results.matches:
            ctx['reply_text'] = results.matches[0].summary
            ctx['cards'].append({
                'type': 'knowledge_card',
                'title': results.matches[0].page_title,
                'content': results.matches[0].summary
            })

    def _stage_service_resolution(self, ctx: Dict[str, Any]) -> None:
        # Check service coverage databases
        from chat.models import ServiceProfile
        profile = ServiceProfile.objects.filter(name__icontains=ctx['message_text']).first()
        if profile:
            ctx['reply_text'] = profile.short_description
            ctx['cards'].append({
                'type': 'service_card',
                'service_name': profile.name,
                'description': profile.short_description
            })

    def _stage_inquiry_processing(self, ctx: Dict[str, Any]) -> None:
        # Feed message into progressive inquiry flow engine
        from chat.models import InquiryConversationSession
        ics_session = InquiryConversationSession.objects.filter(
            realbot_session=ctx['session_obj'],
            state__in=['collecting_information', 'awaiting_conflict_resolution', 'awaiting_confirmation']
        ).first()

        if ics_session:
            engine = InquiryConversationEngine()
            res = engine.process_message(ics_session, ctx['message_text'])
            if res.get('text'):
                ctx['reply_text'] = res['text']
                # If there are any chips in metadata, extract them
                metadata = res.get('metadata', {})
                chips = metadata.get('chips', [])
                for c in chips:
                    ctx['suggestions'].append({
                        'display_text': c,
                        'intent': 'inquiry_creation'
                    })

    def _stage_suggestion_generation(self, ctx: Dict[str, Any]) -> None:
        # Load suggestions matching categories
        from chat.suggestion_engine import SuggestionEngine, SuggestionContext
        engine = SuggestionEngine()
        sug_ctx = SuggestionContext(
            session=ctx['session_obj'],
            intent=ctx['intent'] or 'unknown_intent',
            current_page=ctx['page_path']
        )
        chips = engine.get_suggestions(sug_ctx)
        
        # Avoid duplicate chips
        existing_texts = {c['display_text'].lower() for c in ctx['suggestions']}
        for chip in chips:
            if chip['display_text'].lower() not in existing_texts:
                ctx['suggestions'].append({
                    'display_text': chip['display_text'],
                    'intent': chip['intent']
                })
                existing_texts.add(chip['display_text'].lower())

    def _stage_navigation_resolution(self, ctx: Dict[str, Any]) -> None:
        # Perform navigational checks if matching deep links
        pass

    def _stage_action_resolution(self, ctx: Dict[str, Any]) -> None:
        # Validate predefined action codes
        pass

    def _stage_response_composition(self, ctx: Dict[str, Any]) -> None:
        # Final fallback composition if modules left reply blank
        if not ctx['reply_text']:
            ctx['reply_text'] = "Hello, how can I assist you with Tamil Nadu property consulting today?"

    def _stage_output_validation(self, ctx: Dict[str, Any]) -> None:
        """M2.14 — Post-composition output validation stage."""
        result = self.security.validate_output({
            'reply_text': ctx['reply_text'],
            'cards': ctx['cards'],
            'suggestions': ctx['suggestions']
        })
        ctx['output_validation'] = result
        if not result['is_safe']:
            logger.warning(f"Output validation issues: {result['issues']}")
            # Scrub the reply to a safe fallback to prevent internal data exposure
            ctx['reply_text'] = "I'm here to help with Tamil Nadu property consulting. How can I assist you?"

    def _stage_response_delivery(self, ctx: Dict[str, Any]) -> None:
        # Persist reply log to RealBotMessage table
        if ctx['session_obj']:
            # Save user message
            RealBotMessage.objects.create(
                session=ctx['session_obj'],
                sender='user',
                text=ctx['message_text']
            )
            # Save bot message
            RealBotMessage.objects.create(
                session=ctx['session_obj'],
                sender='assistant',
                text=ctx['reply_text']
            )

    def _stage_analytics_publishing(self, ctx: Dict[str, Any]) -> None:
        # Dispatch metric trace events
        self.publisher.publish_event(
            event_type='message_orchestrated',
            provider='platform',
            session_id=ctx['session_id'],
            payload={
                'workflow_id': ctx['workflow'].workflow_id,
                'intent': ctx['intent'],
                'error_occurred': ctx['error_occurred']
            }
        )

    def _stage_workflow_completion(self, ctx: Dict[str, Any]) -> None:
        # Mark workflow complete
        pass
