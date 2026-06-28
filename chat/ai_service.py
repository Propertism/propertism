import logging
import requests
import json
from abc import ABC, abstractmethod
from django.conf import settings

logger = logging.getLogger(__name__)

# ==============================================================================
# RAG EXTENSION LAYER STUBS (PHASE 1 - INTERFACES ONLY)
# ==============================================================================

class KnowledgeProvider(ABC):
    """Interface for database knowledge retrieval."""
    @abstractmethod
    def fetch_knowledge(self, query):
        pass

class ContextBuilder(ABC):
    """Interface for compiling prompt context."""
    @abstractmethod
    def build_context(self, history, retrieved_knowledge):
        pass

class CitationProvider(ABC):
    """Interface for mapping references and citations."""
    @abstractmethod
    def get_citations(self, response_text):
        pass

class RetrievalLayer(ABC):
    """Interface for vector store/semantic search retrieval."""
    @abstractmethod
    def retrieve(self, query):
        pass


# ==============================================================================
# AI PROVIDER ABSTRACT BASE CLASS & DEEPSEEK PROVIDER
# ==============================================================================

class AIProvider(ABC):
    """
    Abstract AI Provider interface to support hot-swapping AI engines.
    """
    @abstractmethod
    def generate_response(self, messages, system_prompt=None):
        """
        messages: List of dicts, e.g. [{'role': 'user', 'content': '...'}, ...]
        """
        pass


class DeepSeekProvider(AIProvider):
    """
    DeepSeek Chat API provider utilizing direct HTTP request completion calls.
    """
    def __init__(self):
        self.api_key = getattr(settings, 'DEEPSEEK_API_KEY', '')
        self.model = getattr(settings, 'DEEPSEEK_MODEL', 'deepseek-chat')
        self.temperature = getattr(settings, 'DEEPSEEK_TEMPERATURE', 0.2)
        self.max_tokens = getattr(settings, 'DEEPSEEK_MAX_TOKENS', 2000)
        self.timeout = getattr(settings, 'DEEPSEEK_TIMEOUT', 15)
        self.endpoint = "https://api.deepseek.com/chat/completions"

    def generate_response(self, messages, system_prompt=None):
        if not self.api_key or self.api_key == 'your-api-key-here':
            logger.error("DeepSeek API Key is not configured or is a placeholder.")
            raise ValueError("DeepSeek API Key is missing or invalid. Please configure DEEPSEEK_API_KEY in your settings.")

        # Prepare payload
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        
        # Append message thread
        formatted_messages.extend(messages)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        try:
            logger.info(f"Calling DeepSeek API completions endpoint using model: {self.model}")
            response = requests.post(
                self.endpoint,
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout
            )
            
            # Handle standard API response status codes
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content']
                usage = data.get('usage', {})
                logger.info(f"DeepSeek response received successfully. Tokens used: {usage}")
                return {
                    "text": content,
                    "tokens_used": usage.get('total_tokens', 0)
                }
            elif response.status_code == 401:
                logger.error("DeepSeek API Authorization failed (401).")
                raise PermissionError("DeepSeek API key is invalid or unauthorized. Please verify your credentials.")
            elif response.status_code == 429:
                logger.warning("DeepSeek API rate limits hit (429).")
                raise ConnectionRefusedError("DeepSeek rate limits exceeded. Please retry after a brief delay.")
            elif response.status_code >= 500:
                logger.error(f"DeepSeek server side failure: HTTP {response.status_code}")
                raise IOError("DeepSeek remote service is currently unavailable. Please try again later.")
            else:
                logger.error(f"DeepSeek request returned unexpected status: {response.status_code} - {response.text}")
                raise ValueError(f"Provider API returned status {response.status_code}.")

        except requests.exceptions.Timeout:
            logger.error("DeepSeek API call timed out.")
            raise TimeoutError("Connection to AI advisor timed out. Please try sending your query again.")
        except requests.exceptions.ConnectionError:
            logger.error("Network connection error to DeepSeek host.")
            raise ConnectionError("Unable to establish a connection to the advisor. Please check your internet connectivity.")
        except Exception as exc:
            if not isinstance(exc, (ValueError, TimeoutError, ConnectionError, PermissionError, ConnectionRefusedError, IOError)):
                logger.exception(f"Unexpected error in DeepSeek response processing: {exc}")
                raise RuntimeError(f"An unexpected advisor error occurred: {str(exc)}")
            raise exc


# ==============================================================================
# CORE AI SERVICE LAYER COORDINATOR
# ==============================================================================

class AIService:
    """
    Orchestration layer managing selected providers, exception logs,
    and fallback prompts.
    """
    def __init__(self, provider: AIProvider = None):
        self.provider = provider or DeepSeekProvider()

    def get_advisory_response(self, conversation_history, system_prompt=None):
        """
        conversation_history: List of dicts in role-content schema:
          [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
        """
        if not system_prompt:
            system_prompt = (
                "You are realBOT, the premium AI Property Advisor for Propertism.\n"
                "Provide professional, institutional-grade real estate advisory for Chennai and key markets.\n"
                "Maintain a formal, enterprise tone. Do not use emojis, speech bubbles, or playful language.\n"
                "Format answers using clean Markdown. When listing details, present them clearly."
            )

        try:
            return self.provider.generate_response(conversation_history, system_prompt)
        except Exception as e:
            logger.error(f"AI Service Layer failure: {str(e)}")
            raise e
