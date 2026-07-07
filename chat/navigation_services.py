"""
chat/navigation_services.py — M2.8 Navigation and Action Services Framework.
Implements the ParameterResolver, ActionValidator, Pluggable Action Providers,
ActionDispatcher, and Analytics/Diagnostics integrations.
"""
import logging
import re
from typing import Dict, Any, List, Optional
from django.utils import timezone
from abc import ABC, abstractmethod

from chat.models import ActionDefinition, ActionExecutionLog, RealBotSession

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Parameter Resolver & Validator
# ─────────────────────────────────────────────────────────────────────────────

class ParameterResolver:
    """Resolves and interpolates dynamic parameters inside Action Target URLs."""

    def resolve(self, url: str, parameters: Dict[str, Any]) -> str:
        if not url:
            return ""
        resolved_url = url
        # Find all placeholders like {param_name}
        placeholders = re.findall(r'\{([A-Za-z0-9_]+)\}', url)
        for ph in placeholders:
            val = parameters.get(ph, "")
            resolved_url = resolved_url.replace(f"{{{ph}}}", str(val))
        return resolved_url


class ActionValidator:
    """Validates Action Definitions before execution."""

    def validate(self, definition: ActionDefinition, parameters: Dict[str, Any]) -> List[str]:
        errors = []

        # 1. Check active status
        if definition.status != 'active':
            errors.append(f"Action '{definition.action_name}' is currently inactive.")

        # 2. Check all supported parameters are present
        req_params = definition.supported_parameters or []
        for param in req_params:
            if param not in parameters or parameters[param] in (None, ""):
                errors.append(f"Required parameter '{param}' is missing or empty.")

        # 3. Check internal navigation routes start with slash
        if definition.action_type == 'internal_nav' and definition.target_url:
            if not (definition.target_url.startswith('/') or definition.target_url.startswith('http')):
                errors.append(f"Internal route target URL '{definition.target_url}' must start with a forward slash ('/').")

        return errors


# ─────────────────────────────────────────────────────────────────────────────
# 2. Pluggable Action Providers
# ─────────────────────────────────────────────────────────────────────────────

class BaseActionProvider(ABC):
    """Abstract Base Class for all pluggable action providers (M2.8)."""

    @abstractmethod
    def build_response(self, definition: ActionDefinition, resolved_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        pass


class InternalNavigationProvider(BaseActionProvider):
    def build_response(self, definition: ActionDefinition, resolved_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'navigation',
            'destination': 'internal',
            'url': resolved_url,
            'label': definition.display_name,
            'message': f"Opening page: {definition.display_name}...",
            'chips': ['Go Back', 'Contact Us'],
        }


class ExternalURLProvider(BaseActionProvider):
    def build_response(self, definition: ActionDefinition, resolved_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'navigation',
            'destination': 'external',
            'url': resolved_url,
            'label': definition.display_name,
            'message': f"Redirecting you to external portal: {definition.display_name}...",
            'chips': ['Go Back', 'Cancel Redirect'],
        }


class ContactProvider(BaseActionProvider):
    def build_response(self, definition: ActionDefinition, resolved_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'contact',
            'phone': params.get('phone', '+91 86670 20798'),
            'email': params.get('email', 'info@propertism.in'),
            'message': definition.description or "Here are our contact coordinates.",
            'chips': ['Call Now', 'WhatsApp Us', 'Send Email'],
        }


class CommunicationProvider(BaseActionProvider):
    def build_response(self, definition: ActionDefinition, resolved_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        # Formulate direct tel/mailto/wa deep links
        action_trigger_type = 'link'
        if definition.action_type == 'phone_call':
            action_trigger_type = 'phone'
        elif definition.action_type == 'whatsapp':
            action_trigger_type = 'whatsapp'
        elif definition.action_type == 'email':
            action_trigger_type = 'email'

        return {
            'type': 'communication',
            'action_type': definition.action_type,
            'url': resolved_url,
            'action_trigger': {
                'type': action_trigger_type,
                'url': resolved_url
            },
            'message': f"Launching {definition.display_name} connection sequence...",
            'chips': ['Proceed', 'Go Back']
        }


class GovernmentServiceProvider(BaseActionProvider):
    def build_response(self, definition: ActionDefinition, resolved_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'gov_service',
            'service_name': definition.display_name,
            'url': resolved_url,
            'message': f"Connecting you to Tamil Nadu Government Service: {definition.display_name}...",
            'chips': ['Proceed to Portal', 'Cancel']
        }


class InquiryProvider(BaseActionProvider):
    def build_response(self, definition: ActionDefinition, resolved_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'inquiry_action',
            'action': definition.target_service or 'inquiry_creation',
            'message': f"Redirecting to {definition.display_name} flow...",
            'chips': ['Start Inquiry', 'Go Back']
        }


class SocialProvider(BaseActionProvider):
    def build_response(self, definition: ActionDefinition, resolved_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'social',
            'platform': definition.display_name,
            'url': resolved_url,
            'message': f"Opening official Propertism {definition.display_name} profile...",
            'chips': ['Follow Us', 'Go Back']
        }


class MapProvider(BaseActionProvider):
    def build_response(self, definition: ActionDefinition, resolved_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'map_location',
            'destination': definition.display_name,
            'url': resolved_url,
            'message': f"Locating Propertism office: {definition.display_name}...",
            'chips': ['Get Directions', 'Open Map']
        }


# ─────────────────────────────────────────────────────────────────────────────
# 3. Action Dispatcher Core
# ─────────────────────────────────────────────────────────────────────────────

class ActionDispatcher:
    """Dispatches, validates, logs, and processes unified actions (M2.8)."""

    def __init__(self):
        self.resolver = ParameterResolver()
        self.validator = ActionValidator()
        self.providers: Dict[str, BaseActionProvider] = {
            'Internal':           InternalNavigationProvider(),
            'External':           ExternalURLProvider(),
            'Communication':       CommunicationProvider(),
            'Location':            MapProvider(),
            'Social':             SocialProvider(),
            'GovernmentServices': GovernmentServiceProvider(),
            'BusinessActions':    InquiryProvider(),
        }

    def dispatch_action(
        self,
        action_identifier: str,
        session_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        bypass_confirm: bool = False
    ) -> Dict[str, Any]:
        """
        Main execution entry point.
        action_identifier can be Action ID (ACT000001) or unique Action Name (nav_home).
        """
        parameters = parameters or {}
        session = None
        if session_id:
            try:
                session = RealBotSession.objects.filter(session_id=session_id).first()
            except Exception:
                pass

        # 1. Lookup the action definition
        lookup_field = 'action_id' if action_identifier.startswith('ACT') else 'action_name'
        definition = ActionDefinition.objects.filter(**{lookup_field: action_identifier}).first()

        if not definition:
            return {
                'success': False,
                'error': f"Action '{action_identifier}' not found in registry.",
                'requires_confirmation': False,
            }

        # 2. Validate action parameters and status
        validation_errors = self.validator.validate(definition, parameters)
        if validation_errors:
            # Log validation failure
            ActionExecutionLog.objects.create(
                session=session,
                action_id=definition.action_id,
                action_name=definition.action_name,
                parameters=parameters,
                is_validated=False,
                requires_confirmation=False,
                is_confirmed=False
            )
            return {
                'success': False,
                'error': "Validation failed: " + "; ".join(validation_errors),
                'requires_confirmation': False,
            }

        # 3. Resolve parameters inside URL
        resolved_url = self.resolver.resolve(definition.target_url, parameters)

        # 4. Check confirmation workflow
        if definition.confirmation_required and not bypass_confirm:
            # Log pending confirmation state
            ActionExecutionLog.objects.create(
                session=session,
                action_id=definition.action_id,
                action_name=definition.action_name,
                parameters=parameters,
                is_validated=True,
                requires_confirmation=True,
                is_confirmed=False
            )
            return {
                'success': True,
                'action_id': definition.action_id,
                'action_name': definition.action_name,
                'requires_confirmation': True,
                'confirmation_prompt': f"Are you sure you want to execute '{definition.display_name}'?",
                'text': f"To proceed with {definition.display_name}, please confirm below.",
                'metadata': {
                    'chips': ['Yes, Proceed', 'Cancel'],
                    'action_confirm': {
                        'action_id': definition.action_id,
                        'parameters': parameters
                    }
                }
            }

        # 5. Process execution using pluggable provider
        provider = self.providers.get(definition.category)
        if not provider:
            # Fallback to internal navigation
            provider = self.providers['Internal']

        payload = provider.build_response(definition, resolved_url, parameters)

        # Log successful execution
        ActionExecutionLog.objects.create(
            session=session,
            action_id=definition.action_id,
            action_name=definition.action_name,
            parameters=parameters,
            is_validated=True,
            requires_confirmation=definition.confirmation_required,
            is_confirmed=True
        )

        return {
            'success': True,
            'action_id': definition.action_id,
            'action_name': definition.action_name,
            'requires_confirmation': False,
            'payload': payload
        }
