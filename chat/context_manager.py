"""
chat/context_manager.py — M2.10 Conversation Memory & Context Management.
Implements ContextValidator, ConversationContextManager, TopicManager, and ContextResolutionEngine.
"""
import logging
import time
from typing import Any, Dict, List, Optional, Union
from chat.models import ConversationContext, ContextUpdateLog, RealBotSession

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Context Validator
# ─────────────────────────────────────────────────────────────────────────────

class ContextValidator:
    """Validates variable types (str, int, float, bool, list, dict)."""

    SUPPORTED_TYPES = {
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        'list': list,
        'dict': dict
    }

    def validate_type(self, value: Any, expected_type_name: str) -> bool:
        if expected_type_name not in self.SUPPORTED_TYPES:
            return False
        
        expected_type = self.SUPPORTED_TYPES[expected_type_name]
        
        # Django JSONField loads float/int as numbers, lists as list, dicts as dict.
        # Boolean is handled properly by JSON parser as True/False.
        return isinstance(value, expected_type)


# ─────────────────────────────────────────────────────────────────────────────
# 2. Conversation Context Manager
# ─────────────────────────────────────────────────────────────────────────────

class ConversationContextManager:
    """Manages session-scoped conversation variables, lookup, and expiration policies."""

    def __init__(self):
        self.validator = ContextValidator()

    def get_or_create_context(self, session_id: Union[str, Any]) -> ConversationContext:
        """Locates or creates the OneToOne ConversationContext for a RealBotSession."""
        session = RealBotSession.objects.filter(session_id=session_id).first()
        if not session:
            # Fallback to create a session if session_id is a UUID/string
            try:
                session = RealBotSession.objects.create(session_id=session_id)
            except Exception:
                # If session_id is not valid UUID or doesn't exist, retrieve first or mock
                session = RealBotSession.objects.first()
                if not session:
                    import uuid
                    session = RealBotSession.objects.create(session_id=uuid.uuid4())

        context, created = ConversationContext.objects.get_or_create(session=session)
        if created:
            ContextUpdateLog.objects.create(
                context=context,
                action='created',
                transition_to='idle'
            )
        return context

    def update_variables(
        self,
        context: ConversationContext,
        variables_dict: Dict[str, Any],
        ttl_seconds: Optional[int] = None
    ) -> List[str]:
        """
        Updates typed variables with optional TTL expiration.
        variables_dict format: {'name': {'value': 'Vijay', 'type': 'str'}}
        Returns list of validation error strings if any fail.
        """
        errors = []
        valid_updates = {}

        # Pre-clean expired variables first
        self.expire_variables(context)

        for key, details in variables_dict.items():
            if not isinstance(details, dict) or 'value' not in details:
                errors.append(f"Invalid update payload format for key '{key}'. Must define 'value'.")
                continue

            val = details['value']
            val_type = details.get('type', 'str')

            # Validate type
            if not self.validator.validate_type(val, val_type):
                errors.append(f"Type validation failed for key '{key}'. Value '{val}' is not of type '{val_type}'.")
                continue

            # Calculate expiration timestamp
            expires_at = None
            if ttl_seconds is not None:
                expires_at = int(time.time()) + ttl_seconds
            elif 'ttl' in details:
                expires_at = int(time.time()) + int(details['ttl'])

            valid_updates[key] = {
                'value': val,
                'type': val_type,
                'expires_at': expires_at
            }

        if valid_updates:
            current_vars = context.variables or {}
            current_vars.update(valid_updates)
            context.variables = current_vars
            context.save()

            ContextUpdateLog.objects.create(
                context=context,
                action='updated',
                updated_variables=valid_updates
            )

        return errors

    def get_variable(self, context: ConversationContext, name: str) -> Any:
        """Retrieves a variable value, enforcing expiration check."""
        current_vars = context.variables or {}
        if name not in current_vars:
            return None

        details = current_vars[name]
        expires_at = details.get('expires_at')

        if expires_at and int(time.time()) > expires_at:
            # Expired! Remove variable
            del current_vars[name]
            context.variables = current_vars
            context.save()

            ContextUpdateLog.objects.create(
                context=context,
                action='expired',
                updated_variables={name: details}
            )
            return None

        return details.get('value')

    def expire_variables(self, context: ConversationContext) -> int:
        """Garbage collects all expired variables. Returns count of deleted variables."""
        current_vars = context.variables or {}
        now = int(time.time())
        expired_keys = []

        for key, details in list(current_vars.items()):
            exp = details.get('expires_at')
            if exp and now > exp:
                expired_keys.append(key)
                del current_vars[key]

        if expired_keys:
            context.variables = current_vars
            context.save()
            ContextUpdateLog.objects.create(
                context=context,
                action='expired',
                updated_variables={k: {} for k in expired_keys}
            )

        return len(expired_keys)

    def clear_context(self, context: ConversationContext):
        """Resets the context topic state, stack, and active variables."""
        context.current_topic = ""
        context.previous_topic = ""
        context.active_intent = ""
        context.active_service = ""
        context.active_inquiry_id = ""
        context.last_knowledge_topic = ""
        context.last_suggested_actions = []
        context.recent_inputs = []
        context.pending_questions = []
        context.outstanding_fields = []
        context.variables = {}
        context.conversation_state = "idle"
        context.navigation_state = {}
        context.save()

        ContextUpdateLog.objects.create(
            context=context,
            action='cleared'
        )


# ─────────────────────────────────────────────────────────────────────────────
# 3. Topic Switching & Restoration Engine
# ─────────────────────────────────────────────────────────────────────────────

class TopicManager:
    """Manages active topics and nested topic switches/restorations."""

    def switch_topic(self, context: ConversationContext, new_topic: str):
        """
        Switches the current conversation topic.
        Pushes the current topic onto the nested '_topic_stack' stack.
        """
        old_topic = context.current_topic or ""
        if old_topic == new_topic:
            return

        # Fetch/Create Stack
        vars_dict = context.variables or {}
        stack_details = vars_dict.get('_topic_stack', {'value': [], 'type': 'list'})
        stack = list(stack_details.get('value', []))

        # Push old topic to stack
        if old_topic:
            stack.append(old_topic)

        # Update context fields
        context.previous_topic = old_topic
        context.current_topic = new_topic

        # Update stack in variables
        vars_dict['_topic_stack'] = {
            'value': stack,
            'type': 'list',
            'expires_at': None
        }
        context.variables = vars_dict
        context.save()

        ContextUpdateLog.objects.create(
            context=context,
            action='topic_switch',
            transition_from=old_topic,
            transition_to=new_topic
        )

    def restore_previous_topic(self, context: ConversationContext) -> Optional[str]:
        """
        Pops the last topic from the '_topic_stack' topic stack.
        Restores it as the current active topic.
        """
        vars_dict = context.variables or {}
        stack_details = vars_dict.get('_topic_stack', {'value': [], 'type': 'list'})
        stack = list(stack_details.get('value', []))

        if not stack:
            # If stack is empty, fall back to previous_topic or clear current_topic
            restored_topic = context.previous_topic or ""
            context.previous_topic = ""
            context.current_topic = restored_topic
            context.save()
            
            ContextUpdateLog.objects.create(
                context=context,
                action='topic_restore',
                transition_from=context.current_topic,
                transition_to=restored_topic
            )
            return restored_topic if restored_topic else None

        restored_topic = stack.pop()

        # Update context fields
        context.previous_topic = context.current_topic
        context.current_topic = restored_topic

        # Update stack in variables
        vars_dict['_topic_stack'] = {
            'value': stack,
            'type': 'list',
            'expires_at': None
        }
        context.variables = vars_dict
        context.save()

        ContextUpdateLog.objects.create(
            context=context,
            action='topic_restore',
            transition_from=context.previous_topic,
            transition_to=restored_topic
        )
        return restored_topic


# ─────────────────────────────────────────────────────────────────────────────
# 4. Context Resolution Engine
# ─────────────────────────────────────────────────────────────────────────────

class ContextResolutionEngine:
    """Resolves intent, active service profiles, and inquiry session dependencies."""

    def resolve_conversation_context(self, context: ConversationContext) -> Dict[str, Any]:
        """Returns consolidated, resolved snapshot profile of the context."""
        # Pre-expire variables first
        mgr = ConversationContextManager()
        mgr.expire_variables(context)

        return {
            'context_id': context.context_id,
            'current_topic': context.current_topic,
            'previous_topic': context.previous_topic,
            'active_intent': context.active_intent,
            'active_service': context.active_service,
            'active_inquiry_id': context.active_inquiry_id,
            'last_knowledge_topic': context.last_knowledge_topic,
            'last_suggested_actions': context.last_suggested_actions,
            'recent_inputs': context.recent_inputs,
            'pending_questions': context.pending_questions,
            'outstanding_fields': context.outstanding_fields,
            'conversation_state': context.conversation_state,
            'navigation_state': context.navigation_state,
            # Return variables stripped of their metadata structure for clean business API consumption
            'variables': {
                key: details['value']
                for key, details in (context.variables or {}).items()
                if key != '_topic_stack'
            }
        }
