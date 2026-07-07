"""
chat/service_builder.py — M2.5 Service Response Builder
Generates standardized, configuration-driven advisory responses by parsing user queries
for specific sub-topics and mapping them to ServiceProfile properties.
Also compiles suggestion chips, CTAs, contacts, and related service links.
"""
import re
from typing import Dict, Any, List, Optional
from chat.models import ServiceProfile

class ServiceResponseBuilder:
    """Parses queries and structures markdown & metadata responses from Service Profiles."""
    
    SUB_TOPICS = {
        'documents': ['document', 'documents', 'paperwork', 'inputs', 'required inputs', 'id proof', 'pan card', 'aadhaar'],
        'process': ['process', 'step', 'steps', 'workflow', 'stages', 'procedure', 'how does it work', 'how to'],
        'benefits': ['benefit', 'benefits', 'advantage', 'advantages', 'feature', 'features', 'why use', 'why propertism'],
        'eligibility': ['eligibility', 'eligible', 'criteria', 'qualify', 'who can', 'requirements'],
        'pricing': ['pricing', 'price', 'fee', 'fees', 'charge', 'charges', 'commission', 'cost', 'rate', 'rates'],
        'faqs': ['faq', 'faqs', 'question', 'questions', 'common query', 'ask'],
        'limitations': ['limitation', 'limitations', 'limit', 'limits', 'restriction', 'restrictions', 'exclusion', 'exclusions']
    }

    def build_response(self, service: ServiceProfile, query: str) -> Dict[str, Any]:
        """
        Builds dynamic advisory content based on parsed sub-topic.
        Returns:
            {
                'text': markdown_string,
                'metadata': dict
            }
        """
        query_lower = query.lower()
        matched_subtopic = self._detect_subtopic(query_lower)
        
        # Assemble Response Text
        header = f"### {service.name} — {service.category}\n\n"
        body = ""
        
        if matched_subtopic == 'documents':
            body = (
                f"Here are the required inputs and documents for our **{service.name}** service:\n\n"
                f"{self._format_list(service.required_inputs or 'Contact us for details.')}"
            )
        elif matched_subtopic == 'process':
            proc = service.advisory_content.get('process', '')
            body = (
                f"Here is the process workflow for **{service.name}**:\n\n"
                f"{self._format_process(proc)}"
            )
        elif matched_subtopic == 'benefits':
            ben = service.advisory_content.get('benefits', '')
            body = (
                f"Key benefits of choosing Propertism for **{service.name}**:\n\n"
                f"{self._format_list(ben)}"
            )
        elif matched_subtopic == 'eligibility':
            body = (
                f"Eligibility criteria for **{service.name}**:\n\n"
                f"{self._format_list(service.eligibility or 'Open to all platforms.')}"
            )
        elif matched_subtopic == 'pricing':
            prc = service.advisory_content.get('pricing', '')
            body = (
                f"Pricing reference and service fees for **{service.name}**:\n\n"
                f"{prc or 'Contact us for a direct quote.'}"
            )
        elif matched_subtopic == 'faqs':
            body = f"### Frequently Asked Questions for {service.name}:\n\n"
            if service.faqs:
                for idx, item in enumerate(service.faqs, 1):
                    body += f"**{idx}. {item['q']}**\n{item['a']}\n\n"
            else:
                body += "No FAQs defined for this service yet. Please ask an advisor."
        elif matched_subtopic == 'limitations':
            lim = service.advisory_content.get('limitations', '')
            body = (
                f"Please note the following service limitations / restrictions for **{service.name}**:\n\n"
                f"{lim or 'No specific limitations apply.'}"
            )
        else:
            # Default to full Overview / Introduction
            body = (
                f"{service.short_description}\n\n"
                f"**Overview:**\n"
                f"{service.detailed_description}\n\n"
                f"**Business Objective:**\n"
                f"{service.business_objective}\n\n"
                f"**Target Audience:**\n"
                f"{service.target_audience}"
            )

        full_markdown = header + body
        
        # Assemble Response Metadata
        metadata = self._assemble_metadata(service, matched_subtopic)
        
        return {
            'text': full_markdown.strip(),
            'metadata': metadata
        }

    def _detect_subtopic(self, query: str) -> Optional[str]:
        """Detects if query matches any specific sub-topic keywords."""
        for subtopic, keywords in self.SUB_TOPICS.items():
            for kw in keywords:
                # Basic boundary check for keyword/phrase in query
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, query):
                    return subtopic
        return None

    def _format_list(self, text: str) -> str:
        """Formats comma-separated or newline list items as markdown bullets."""
        if not text:
            return ""
        if '\n' in text:
            lines = [line.strip() for line in text.split('\n') if line.strip()]
        else:
            lines = [item.strip() for item in text.split(',') if item.strip()]
            
        formatted = ""
        for line in lines:
            if line.startswith('-') or line.startswith('*'):
                formatted += f"{line}\n"
            else:
                formatted += f"- {line}\n"
        return formatted

    def _format_process(self, process_text: str) -> str:
        """Formats standard '1. Step → 2. Step' process string as numbered lists."""
        if not process_text:
            return "Contact us for step-by-step guidance."
        if '→' in process_text:
            steps = [s.strip() for s in process_text.split('→') if s.strip()]
            formatted = ""
            for idx, step in enumerate(steps, 1):
                # Clean prefix numbers if any
                clean_step = re.sub(r'^\d+\.\s*', '', step)
                formatted += f"{idx}. {clean_step}\n"
            return formatted
        return process_text

    def _assemble_metadata(self, service: ServiceProfile, subtopic: Optional[str]) -> Dict[str, Any]:
        """Assembles chips, CTAs, navigation, escalation, and related services metadata."""
        metadata = {}
        
        # Suggestion Chips
        chips = []
        for cta in service.call_to_actions[:3]:
            chips.append(cta['label'])
            
        # Add basic navigational chips based on parsed subtopic
        subtopic_chips = {
            'overview': 'Process Steps',
            'process': 'Required Documents',
            'documents': 'Pricing & Fees',
            'eligibility': 'Required Documents',
            'pricing': 'FAQ'
        }
        if subtopic in subtopic_chips and subtopic_chips[subtopic] not in chips:
            chips.append(subtopic_chips[subtopic])
            
        chips.extend(['Contact Us', 'Inquiry Form'])
        metadata['chips'] = chips[:5]  # Cap at 5 chips for clean UI
        
        # Service Metadata
        metadata['service'] = {
            'service_id': service.service_id,
            'name': service.name,
            'category': service.category,
            'version': service.version,
            'display_priority': service.display_priority,
        }
        
        # Call-To-Actions
        metadata['call_to_actions'] = service.call_to_actions
        
        # Contact Channels & Escalation
        metadata['contact_channels'] = service.contact_channels
        metadata['escalation'] = service.escalation_rules
        
        # Navigation Link
        if service.navigation_links:
            metadata['navigation'] = {
                'url': service.navigation_links[0]['url'],
                'label': service.navigation_links[0]['label']
            }
            
        # Related Services Engine (fetches related service details dynamically)
        related_ids = service.related_services
        if related_ids:
            related_profiles = ServiceProfile.objects.filter(service_id__in=related_ids, status='active')
            metadata['related_services'] = [
                {
                    'service_id': rp.service_id,
                    'name': rp.name,
                    'short_description': rp.short_description
                }
                for rp in related_profiles
            ]
            
        return metadata
