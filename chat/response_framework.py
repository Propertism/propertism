"""
chat/response_framework.py — M2.9 Rich Response Framework.
Implements the ResponseValidator, ResponseTemplateEngine, ResponseCompositionEngine,
ResponseBuilder, and Analytics/Diagnostics logging.
"""
import logging
import re
from typing import Dict, Any, List, Tuple, Optional
from chat.models import ResponseComponent, ResponseCompositionLog, RealBotSession

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Response Schema Validator & Template Engine
# ─────────────────────────────────────────────────────────────────────────────

class ResponseValidator:
    """Validates dynamic inputs against Response Component Data Schemas."""

    def validate(self, component: ResponseComponent, parameters: Dict[str, Any]) -> List[str]:
        errors = []
        
        # 1. Check status
        if component.status != 'active':
            errors.append(f"Response component '{component.name}' is currently inactive.")

        # 2. Check all schema fields exist in params
        schema_fields = component.data_schema or []
        for field in schema_fields:
            if field not in parameters:
                errors.append(f"Missing required data field '{field}' for component '{component.name}'.")
                
        return errors


class ResponseTemplateEngine:
    """Interpolates parameters into component template strings for text fallback rendering."""

    def resolve(self, template: str, parameters: Dict[str, Any]) -> str:
        if not template:
            return ""
        resolved = template
        # Find all {placeholders}
        placeholders = re.findall(r'\{([A-Za-z0-9_]+)\}', template)
        for ph in placeholders:
            val = parameters.get(ph, "")
            # Format lists cleanly
            if isinstance(val, list):
                val = ", ".join(str(item) for item in val)
            resolved = resolved.replace(f"{{{ph}}}", str(val))
        return resolved


# ─────────────────────────────────────────────────────────────────────────────
# 2. Composition Engine
# ─────────────────────────────────────────────────────────────────────────────

class ResponseCompositionEngine:
    """Composes, validates, groups, and orders response components by priority."""

    def __init__(self):
        self.validator = ResponseValidator()
        self.template_engine = ResponseTemplateEngine()

    def compose(
        self,
        requested_components: List[Dict[str, Any]],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Accepts a list of component composition requests, e.g.:
        [
            {'name': 'warning_card', 'parameters': {'warning_message': 'Check rates'}},
            {'name': 'service_card', 'parameters': {...}}
        ]
        """
        session = None
        if session_id:
            try:
                session = RealBotSession.objects.filter(session_id=session_id).first()
            except Exception:
                pass

        composed_elements = []
        validation_errors = []
        is_validated = True

        for req in requested_components:
            name = req.get('name')
            params = req.get('parameters', {})

            if not name:
                validation_errors.append("Component composition block is missing required 'name' key.")
                is_validated = False
                continue

            # Fetch component from registry
            comp = ResponseComponent.objects.filter(name=name).first()
            if not comp:
                validation_errors.append(f"Response component '{name}' not found in registry.")
                is_validated = False
                continue

            # Validate schema
            errors = self.validator.validate(comp, params)
            if errors:
                validation_errors.extend(errors)
                is_validated = False
                continue

            # Resolve template display
            resolved_text = self.template_engine.resolve(comp.display_template, params)

            composed_elements.append({
                'component_id': comp.component_id,
                'name': comp.name,
                'component_type': comp.component_type,
                'rendering_priority': comp.rendering_priority,
                'text_display': resolved_text,
                'data': params
            })

        # Sort elements by priority ascending (e.g. 1 at the top, 50 at the bottom)
        composed_elements.sort(key=lambda x: x['rendering_priority'])

        # Build final composed text markup
        text_blocks = [elem['text_display'] for elem in composed_elements if elem['text_display']]
        unified_text = "\n\n".join(text_blocks)

        # Log compilation to analytics DB log
        ResponseCompositionLog.objects.create(
            session=session,
            composition=requested_components,
            is_validated=is_validated,
            errors=validation_errors
        )

        return {
            'success': is_validated,
            'errors': validation_errors,
            'text': unified_text,
            'rich_components': [
                {
                    'component_id': elem['component_id'],
                    'name': elem['name'],
                    'component_type': elem['component_type'],
                    'data': elem['data']
                } for elem in composed_elements
            ]
        }


# ─────────────────────────────────────────────────────────────────────────────
# 3. Response Builder Wrapper
# ─────────────────────────────────────────────────────────────────────────────

class ResponseBuilder:
    """Assembles all rich response models and inputs for delivery (M2.9)."""

    def __init__(self):
        self.composition_engine = ResponseCompositionEngine()

    def build_composed_response(
        self,
        components_list: List[Dict[str, Any]],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Convenience assembly layer returning structured payload."""
        return self.composition_engine.compose(components_list, session_id=session_id)
