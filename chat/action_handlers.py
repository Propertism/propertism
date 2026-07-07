"""
chat/action_handlers.py — M2.4 Action Dispatcher and Pluggable Action Handlers
Executes the business action resolved by the Rule Engine. Integrated with the
Unified Knowledge Repository (M2.2 & M2.3) for knowledge response rendering.
"""
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from chat.rule_engine import IntentResult

logger = logging.getLogger(__name__)

@dataclass
class ActionResponse:
    text: str
    metadata: Dict[str, Any]

class BaseActionHandler(ABC):
    """Abstract base class for all pluggable action handlers."""
    
    @abstractmethod
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        pass

class GreetingHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        chips = intent_result.action_config.get('chips', ['Buy Property', 'Sell Property', 'NRI Services', 'Contact Us'])
        text = "Hello! Welcome to Propertism Realty Advisors. How may I assist you today?"
        return ActionResponse(
            text=text,
            metadata={'chips': chips}
        )

class FarewellHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        chips = intent_result.action_config.get('chips', ['Start New Query', 'Contact Us'])
        text = "Thank you for connecting with Propertism. Have a wonderful day!"
        return ActionResponse(
            text=text,
            metadata={'chips': chips}
        )

class ContactCardHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        config = intent_result.action_config
        text = config.get('message', "Here are our contact details. Please feel free to reach out to us.")
        return ActionResponse(
            text=text,
            metadata={
                'chips': config.get('chips', ['Call Now', 'Send WhatsApp']),
                'contact': {
                    'phone': config.get('phone', '+91 86670 20798'),
                    'email': config.get('email', 'info@propertism.in'),
                    'address': config.get('address', '')
                }
            }
        )

class GoogleMapsHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        config = intent_result.action_config
        text = f"You can navigate to our office using Google Maps:\n\n**Office Address:**\n{config.get('address', 'No. 30, 3rd Floor, SSR Pankajam Towers, Arunachalam Road, Saligramam, Chennai - 600093')}"
        return ActionResponse(
            text=text,
            metadata={
                'chips': config.get('chips', ['Open Maps', 'Get Directions']),
                'navigation': {
                    'url': config.get('maps_url', 'https://maps.google.com/?q=Propertism+Realty+Advisors+Chennai'),
                    'label': 'Open Google Maps'
                }
            }
        )

class ExternalLinkHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        config = intent_result.action_config
        text = f"Click below to visit the external link for {config.get('label', 'resource')}:"
        return ActionResponse(
            text=text,
            metadata={
                'chips': config.get('chips', ['Open Link']),
                'navigation': {
                    'url': config.get('url', 'https://www.linkedin.com/company/propertism'),
                    'label': config.get('label', 'Open External Link')
                }
            }
        )

class WhatsAppHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        config = intent_result.action_config
        phone = config.get('phone', '918667020798').replace('+', '').replace(' ', '')
        message = config.get('message', 'Hello')
        # URL encode message
        import urllib.parse
        encoded_msg = urllib.parse.quote(message)
        wa_url = f"https://wa.me/{phone}?text={encoded_msg}"
        text = "Opening WhatsApp to connect with our support desk..."
        return ActionResponse(
            text=text,
            metadata={
                'chips': config.get('chips', ['Open WhatsApp']),
                'action_trigger': {
                    'type': 'whatsapp',
                    'url': wa_url
                }
            }
        )

class PhoneCallHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        config = intent_result.action_config
        phone = config.get('phone', '+91 86670 20798')
        text = f"Connecting you to Propertism client desk at {phone}..."
        return ActionResponse(
            text=text,
            metadata={
                'chips': config.get('chips', ['Call Now']),
                'action_trigger': {
                    'type': 'phone',
                    'phone': phone
                }
            }
        )

INTENT_TO_SERVICE_MAP = {
    'buy_property': 'Buy Property',
    'sell_property': 'Sell Property',
    'rental_income': 'Rental Income Management',
    'land_plot': 'Land / Plot Services',
    'property_search': 'Property Search',
    'property_viewing': 'Property Viewing',
    'nri_assist': 'NRI Assist',
    'resource_hub': 'Resource Hub',
    'useful_links': 'Useful Links',
    'patta_chitta': 'Patta / Chitta Extract',
    'encumbrance_search': 'Encumbrance Search',
    'gcc_property_tax': 'GCC Property Tax',
    'general_information': 'General Advisory',
    'contact_information': 'Contact Advisory',
    'human_assistance': 'Contact Advisory'
}

def get_service_profile_response(intent_result: IntentResult, query: str) -> Optional[ActionResponse]:
    """Helper to fetch from ServiceProfile database and return via ServiceResponseBuilder."""
    try:
        from chat.models import ServiceProfile
        from chat.service_builder import ServiceResponseBuilder

        service_name = INTENT_TO_SERVICE_MAP.get(intent_result.intent)
        if service_name:
            profile = ServiceProfile.objects.filter(name=service_name, status='active').first()
            if profile:
                builder = ServiceResponseBuilder()
                res = builder.build_response(profile, query)
                return ActionResponse(text=res['text'], metadata=res['metadata'])
    except Exception as exc:
        logger.warning(f"Failed to fetch ServiceProfile response: {exc}")
    return None

class ServiceCardHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        res = get_service_profile_response(intent_result, query)
        if res:
            return res

        config = intent_result.action_config
        text = config.get('description', '')
        return ActionResponse(
            text=text,
            metadata={
                'chips': config.get('chips', []),
                'service': {
                    'name': config.get('service', 'Service'),
                    'url': config.get('url', '#'),
                }
            }
        )

class NavigationCardHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        res = get_service_profile_response(intent_result, query)
        if res:
            return res

        config = intent_result.action_config
        text = config.get('description', f"Visit our {config.get('label', 'page')} below:")
        return ActionResponse(
            text=text,
            metadata={
                'chips': config.get('chips', []),
                'navigation': {
                    'url': config.get('url', '#'),
                    'label': config.get('label', 'Open Page'),
                }
            }
        )

class InquiryWorkflowHandler(BaseActionHandler):
    """
    M2.6 — Launches a new InquiryConversationSession via the Conversation Engine.
    The triggering query is passed to the engine so any field data already
    present in the message (name, country, service etc.) is captured immediately.
    """
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        from chat.inquiry_engine import InquiryConversationEngine
        config = intent_result.action_config
        service_hint = config.get('service_hint', intent_result.intent)

        try:
            # session_id is injected into intent_result at dispatch time (see views.py)
            session_id = getattr(intent_result, '_realbot_session', None)

            if session_id is None:
                # Fallback: return a friendly prompt asking user to continue
                return ActionResponse(
                    text=(
                        "I'd be happy to help you create an inquiry with Propertism! "
                        "Please tell me your name, country, and what you're looking for "
                        "and I'll get the details noted for our team."
                    ),
                    metadata={
                        'chips': ['Buy Property', 'Sell Property', 'Rental Management', 'NRI Assist'],
                        'inquiry': {'status': 'triggered', 'action': 'inquiry_creation'},
                    },
                )

            engine = InquiryConversationEngine()
            result = engine.initiate(
                realbot_session=session_id,
                source='rule_engine',
                service_hint=service_hint,
                opening_message=query,
            )
            return ActionResponse(
                text=result['text'],
                metadata=result['metadata'],
            )
        except Exception as exc:
            logger.exception(f'[InquiryWorkflowHandler] Failed to initiate inquiry: {exc}')
            return ActionResponse(
                text=(
                    "I'd be happy to help you submit an inquiry. "
                    "Please share your name, contact number, and what you're looking for."
                ),
                metadata={
                    'chips': config.get('chips', ['Submit Inquiry', 'Contact Us']),
                    'inquiry': {'status': 'error', 'action': 'inquiry_creation'},
                },
            )


class RelatedServicesHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        config = intent_result.action_config
        text = "I couldn't find a direct answer. You might be interested in these services:"
        return ActionResponse(
            text=text,
            metadata={
                'chips': config.get('chips', ['Buy Property', 'Rental Management', 'NRI Assist'])
            }
        )

class ClarificationHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        q = intent_result.clarification_question or "I found multiple matching topics. Could you please clarify what you're looking for?"
        config = intent_result.action_config
        # Clean intent names for human display in chips
        candidates = config.get('candidates', [])
        chips = []
        for cand in candidates:
            label = cand['intent'].replace('_', ' ').title()
            chips.append(label)
        chips.append('Other Query')
        return ActionResponse(
            text=q,
            metadata={
                'chips': chips,
                'clarification': {
                    'candidates': candidates
                }
            }
        )

class FallbackHandler(BaseActionHandler):
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        config = intent_result.action_config
        text = "I'm sorry, I couldn't understand your query. Could you please rephrase it, or select one of the options below?"
        return ActionResponse(
            text=text,
            metadata={
                'chips': config.get('chips', ['Buy Property', 'Sell Property', 'NRI Assist', 'Contact Us'])
            }
        )

class KnowledgeResponseHandler(BaseActionHandler):
    """
    Bridges Rule Engine and Unified Knowledge Repository.
    Executes KnowledgeSearchEngine search using rule action_config parameters.
    """
    def handle(self, intent_result: IntentResult, query: str) -> ActionResponse:
        from chat.search import KnowledgeSearchEngine
        
        config = intent_result.action_config
        source_types = config.get('source_types', None)
        top_k = config.get('top_k', 3)
        category = config.get('category', None)
        
        search_result = None
        try:
            engine = KnowledgeSearchEngine()
            # If a specific category filter is defined in the rule
            search_result = engine.search(query, top_k=top_k, source_types=source_types)
        except Exception as search_exc:
            logger.warning(f"Knowledge response handler search failed: {search_exc}")
            
        if search_result and search_result.total_found > 0:
            best = search_result.matches[0]
            text = best.summary or best.main_content or ""
            
            metadata = {
                "chips": ['Learn More', 'Contact Us', 'Request Consultation'],
                "knowledge": {
                    "knowledge_id": best.knowledge_id,
                    "source": best.page_title,
                    "url": best.url,
                    "category": best.category,
                    "source_type": best.source_type,
                    "document_ref": best.document_ref,
                    "relevance": round(best.relevance_score, 2),
                },
                "source_references": search_result.source_references[:3],
            }
            return ActionResponse(text=text, metadata=metadata)
        else:
            # Fallback to general unknown text
            text = config.get('fallback_text', "I've searched our knowledge base but couldn't find a direct match. Let me connect you with an advisor.")
            return ActionResponse(
                text=text,
                metadata={'chips': ['Talk to Advisor', 'Contact Us']}
            )

class ActionDispatcher:
    """Dispatches resolved intent results to the appropriate ActionHandler."""
    
    def __init__(self):
        self._handlers: Dict[str, BaseActionHandler] = {
            'greeting_response':  GreetingHandler(),
            'farewell_response':  FarewellHandler(),
            'contact_card':       ContactCardHandler(),
            'google_maps':        GoogleMapsHandler(),
            'external_link':      ExternalLinkHandler(),
            'whatsapp':           WhatsAppHandler(),
            'phone_call':         PhoneCallHandler(),
            'service_card':       ServiceCardHandler(),
            'navigation_card':    NavigationCardHandler(),
            'inquiry_workflow':   InquiryWorkflowHandler(),
            'related_services':   RelatedServicesHandler(),
            'clarification':      ClarificationHandler(),
            'fallback_response':  FallbackHandler(),
            'knowledge_response': KnowledgeResponseHandler(),
        }
        
    def dispatch(self, intent_result: IntentResult, query: str) -> ActionResponse:
        action_type = intent_result.action_type
        handler = self._handlers.get(action_type, self._handlers['fallback_response'])
        
        try:
            return handler.handle(intent_result, query)
        except Exception as exc:
            logger.exception(f"Error handling action '{action_type}': {exc}")
            # Dynamic fallback
            return ActionResponse(
                text="An internal action execution error occurred. How can I help you?",
                metadata={'chips': ['Restart', 'Contact Us']}
            )
