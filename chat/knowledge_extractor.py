import re
import json
import logging
import hashlib
from typing import List, Dict, Any, Tuple
from django.utils import timezone
from django.utils.html import strip_tags
from chat.models import KnowledgeArticle, ExtractedKnowledgeCandidate, KnowledgeLifecycleAuditLog

logger = logging.getLogger('chat')

def generate_synonyms(name: str, role: str = "") -> List[str]:
    """Generates a list of deterministic synonyms/aliases based on name and role."""
    synonyms = [name]
    clean_name = re.sub(r'^(mr\.|ms\.|mrs\.|dr\.|advisor|consultant)\s+', '', name, flags=re.IGNORECASE).strip()
    if clean_name != name:
        synonyms.append(clean_name)
    
    tokens = [t for t in clean_name.split() if len(t) > 2]
    for token in tokens:
        if token not in synonyms:
            synonyms.append(token)
            
    if f"Mr. {clean_name}" not in synonyms:
        synonyms.append(f"Mr. {clean_name}")
        
    if len(tokens) == 2:
        split_name = " ".join(tokens)
        if split_name not in synonyms:
            synonyms.append(split_name)
            
    # Deterministic synonym mapping based on SCCB example
    if clean_name.lower() == "tamilselvan":
        if "Tamil Selvan" not in synonyms:
            synonyms.append("Tamil Selvan")
            
    if role:
        if role not in synonyms:
            synonyms.append(role)
        role_tokens = role.split()
        if len(role_tokens) > 1:
            synonyms.append(f"Advisor {clean_name}")
            synonyms.append(f"Senior {role_tokens[-1]}")
            synonyms.append("Relationship Manager")
            
    return list(dict.fromkeys(synonyms))

def generate_question_variants(entity_type: str, entity_name: str, primary_question: str) -> List[str]:
    """Generates a list of deterministic question variants based on entity type and name."""
    variants = []
    name = entity_name
    
    if entity_type == 'Team':
        variants = [
            f"Tell me about {name}.",
            f"Who is Mr. {name}?",
            f"Can you introduce {name}?",
            f"What does {name} do?",
            f"Who handles NRI clients?",
            f"What is {name}'s role at Propertism?",
            f"What does {name} specialize in?"
        ]
    elif entity_type == 'Service':
        variants = [
            f"What is {name}?",
            f"Tell me about {name}.",
            f"Do you offer {name}?",
            f"How does {name} work?",
            f"What is included in {name}?",
            f"Who is eligible for {name}?"
        ]
    elif entity_type == 'Property':
        variants = [
            f"Tell me about {name}.",
            f"Where is {name}?",
            f"What is the price of {name}?",
            f"What configuration is available for {name}?",
            f"Is {name} available?"
        ]
    elif entity_type == 'Company':
        variants = [
            "Tell me about Propertism.",
            "What is Propertism Realty Advisors?",
            "Introduce Propertism.",
            "What is Propertism's mission statement?",
            "What is Propertism's vision statement?",
            "Why choose Propertism?",
            "Where does Propertism operate?"
        ]
    elif entity_type == 'Contact':
        variants = [
            "What is your contact number?",
            "What is your email address?",
            "Where is your office located?",
            "What are your working hours?",
            "Do you have WhatsApp?",
            "Show me your Google Maps location."
        ]
    elif entity_type == 'GovLink':
        variants = [
            f"What is the link for {name}?",
            f"How do I search for {name}?",
            f"Check {name} online.",
            f"Pay {name}."
        ]
    else:
        variants = [
            f"Tell me about {name}.",
            f"What is {name}?",
            f"Can you explain {name}?"
        ]
        
    unique_variants = []
    for v in variants:
        if v.strip() and v.strip() != primary_question and v.strip() not in unique_variants:
            unique_variants.append(v.strip())
    return unique_variants


class WebsiteConversationalExtractor:
    """Extracts entities and constructs raw candidate records from Django databases."""

    def extract_all_entities(self) -> List[Dict[str, Any]]:
        candidates = []
        candidates.extend(self.extract_company_info())
        candidates.extend(self.extract_team_members())
        candidates.extend(self.extract_services())
        candidates.extend(self.extract_properties())
        candidates.extend(self.extract_testimonials())
        candidates.extend(self.extract_faqs())
        candidates.extend(self.extract_navigation())
        candidates.extend(self.extract_gov_links())
        return candidates

    def extract_company_info(self) -> List[Dict[str, Any]]:
        from content.models import CompanyInfo
        company = CompanyInfo.objects.first()
        if not company:
            return []
            
        name = company.company_name or "Propertism"
        tagline = company.tagline or "Premium Real Estate Advisory & Property Management"
        desc = company.about_description or tagline
        mission = company.about_mission or tagline
        
        return [
            {
                'entity_type': 'Company',
                'entity_name': name,
                'primary_question': f"Who is {name}?",
                'canonical_answer': f"{tagline}. {desc}",
                'keywords': f"{name.lower()} about profile introduction tagline advisors LLPs",
                'synonyms': f"{name}, Propertism Realty, Propertism Chennai",
                'source_url': '/about/',
                'source_section': 'About Us',
                'search_weight': 1.5
            },
            {
                'entity_type': 'Company',
                'entity_name': f"{name} Mission",
                'primary_question': f"What is the mission of {name}?",
                'canonical_answer': mission,
                'keywords': f"{name.lower()} mission statement goal focus values",
                'synonyms': f"mission statement, {name} goal, target",
                'source_url': '/about/',
                'source_section': 'Our Mission',
                'search_weight': 1.2
            }
        ]

    def extract_team_members(self) -> List[Dict[str, Any]]:
        from content.models import TeamMember
        members = TeamMember.objects.filter(is_active=True)
        results = []
        
        # Add general team query candidate
        if members.exists():
            advisors_list = ", ".join(m.name for m in members)
            results.append({
                'entity_type': 'Team',
                'entity_name': 'Our Team',
                'primary_question': "Meet our advisors.",
                'canonical_answer': f"Our advisory team includes key leaders and property specialists: {advisors_list}.",
                'keywords': "team advisors founders management staff list who handles Chennai advisory",
                'synonyms': "team, advisors, founders, staff list",
                'source_url': '/about/',
                'source_section': 'Management Advisory Team',
                'search_weight': 1.0
            })
            
        for member in members:
            syn_list = generate_synonyms(member.name, member.role)
            results.append({
                'entity_type': 'Team',
                'entity_name': member.name,
                'primary_question': f"Who is {member.name}?",
                'canonical_answer': f"{member.name} serves as {member.role} at Propertism. {member.bio}",
                'keywords': f"{member.name.lower()} {member.role.lower()} team advisor expertise bio specialization",
                'synonyms': ", ".join(syn_list),
                'source_url': '/about/',
                'source_section': member.role,
                'search_weight': 1.2
            })
            if member.expertise:
                results.append({
                    'entity_type': 'Team',
                    'entity_name': f"{member.name} Expertise",
                    'primary_question': f"What does {member.name} specialize in?",
                    'canonical_answer': f"{member.name} specializes in: {member.expertise}.",
                    'keywords': f"{member.name.lower()} expertise focus experience skill specialization",
                    'synonyms': f"{member.name} specialization, focus, skill",
                    'source_url': '/about/',
                    'source_section': f"{member.role} Expertise",
                    'search_weight': 1.1
                })
        return results

    def extract_services(self) -> List[Dict[str, Any]]:
        from content.models import Service
        services = Service.objects.filter(is_active=True)
        results = []
        for service in services:
            results.append({
                'entity_type': 'Service',
                'entity_name': service.title,
                'primary_question': f"Tell me about {service.title}.",
                'canonical_answer': f"{service.short_description} {service.full_description or ''}",
                'keywords': f"{service.title.lower()} service offering details custom features",
                'synonyms': f"{service.title}, propertism {service.title.lower()}",
                'source_url': f"/services/{service.slug or ''}/",
                'source_section': 'Service Description',
                'search_weight': 1.4
            })
            if service.features:
                results.append({
                    'entity_type': 'Service',
                    'entity_name': f"{service.title} Features",
                    'primary_question': f"What is included in {service.title}?",
                    'canonical_answer': service.features,
                    'keywords': f"{service.title.lower()} features inclusion details check package scope",
                    'synonyms': f"{service.title} inclusions, what's included",
                    'source_url': f"/services/{service.slug or ''}/",
                    'source_section': 'Service Features',
                    'search_weight': 1.2
                })
        return results

    def extract_properties(self) -> List[Dict[str, Any]]:
        from properties.models import Property
        props = Property.objects.filter(status="available").select_related("property_type")
        results = []
        for p in props:
            typename = p.property_type.name if p.property_type else "Property"
            results.append({
                'entity_type': 'Property',
                'entity_name': p.title,
                'primary_question': f"Tell me about {p.title}.",
                'canonical_answer': f"{p.title} is a {typename} in {p.location}. Price: {p.formatted_price}. {p.description or ''}",
                'keywords': f"{p.title.lower()} property rental listing realestate chennai price location {typename.lower()}",
                'synonyms': f"{p.title}, {p.location} property",
                'source_url': f"/properties/{p.slug}/",
                'source_section': 'Property Details',
                'search_weight': 1.0
            })
        return results

    def extract_testimonials(self) -> List[Dict[str, Any]]:
        from content.models import CustomerReview
        reviews = CustomerReview.objects.filter(is_active=True)
        if not reviews.exists():
            return []
            
        quotes_summary = "\n\n".join(f'"{r.quote}" — {r.customer_name} ({r.customer_location or "Chennai"})' for r in reviews[:5])
        return [{
            'entity_type': 'Testimonial',
            'entity_name': 'Customer Reviews',
            'primary_question': "What do your customers say?",
            'canonical_answer': f"Here are reviews from our clients:\n\n{quotes_summary}",
            'keywords': "reviews testimonials customer feedback success stories client opinions stars rating",
            'synonyms': "testimonials, customer reviews, success stories, reviews",
            'source_url': '/about/',
            'source_section': 'Customer Reviews',
            'search_weight': 1.0
        }]

    def extract_faqs(self) -> List[Dict[str, Any]]:
        from content.models import BlogPost
        posts = BlogPost.objects.filter(is_published=True)
        results = []
        for post in posts:
            faqs = post.faq_items
            for idx, item in enumerate(faqs):
                q = item['question']
                a = item['answer']
                results.append({
                    'entity_type': 'FAQ',
                    'entity_name': f"FAQ-{post.slug}-{idx}",
                    'primary_question': q,
                    'canonical_answer': a,
                    'keywords': f"faq question answer blog {post.title.lower()} {post.category}",
                    'synonyms': "frequently asked questions, FAQ",
                    'source_url': f"/knowledge-hub/{post.slug}/",
                    'source_section': 'Frequently Asked Questions',
                    'search_weight': 1.0
                })
        return results

    def extract_navigation(self) -> List[Dict[str, Any]]:
        routes = [
            ('Home', '/', 'Home Page'),
            ('About Us', '/about/', 'About Us Profile Page'),
            ('Services', '/services/', 'Our Services Portfolio Page'),
            ('Properties', '/properties/', 'Available Properties Listings Page'),
            ('Contact', '/contact/', 'Contact Information & Inquiries Page'),
        ]
        results = []
        for title, url, desc in routes:
            results.append({
                'entity_type': 'Navigation',
                'entity_name': title,
                'primary_question': f"Where can I find {title}?",
                'canonical_answer': f"You can find the {title} page online here: {url}",
                'keywords': f"navigation take me to open url link redirect navigate {title.lower()} page",
                'synonyms': f"{title} page, redirect {title.lower()}",
                'source_url': url,
                'source_section': 'Navigation Route',
                'search_weight': 1.0
            })
        return results

    def extract_gov_links(self) -> List[Dict[str, Any]]:
        links = [
            ('Patta Chitta', 'Tamil Nadu Land Records Portal', 'https://eservices.tn.gov.in/'),
            ('Encumbrance Certificate (EC)', 'TN Registration Department Portal (Inspector General of Registration)', 'https://tnreginet.gov.in/'),
            ('GCC Property Tax', 'Greater Chennai Corporation Property Tax Online Portal', 'https://chennaicorporation.gov.in/gcc/online-payment/property-tax/'),
        ]
        results = []
        for name, portal, url in links:
            results.append({
                'entity_type': 'GovLink',
                'entity_name': name,
                'primary_question': f"How do I search for {name}?",
                'canonical_answer': f"You can access the {name} online through the official {portal} at: {url}",
                'keywords': f"government links {name.lower()} official portal land records property tax TN chennai registration EC search online",
                'synonyms': f"{name} portal, official {name.lower()} link",
                'source_url': url,
                'source_section': 'Official Portal Link',
                'search_weight': 1.1
            })
        return results


class KnowledgeReconciliationEngine:
    """Reconciles extracted candidates against existing KnowledgeArticles to prevent overwriting manual edits."""

    def reconcile_all(self, candidates_data: List[Dict[str, Any]]) -> Tuple[List[ExtractedKnowledgeCandidate], Dict[str, Any]]:
        existing_articles = list(KnowledgeArticle.objects.all())
        
        seen_entity_questions = set()
        
        stats = {
            'total_website_entities_analysed': len(candidates_data),
            'existing_kb_matches': 0,
            'new_conversational_qa_generated': 0,
            'duplicate_candidates': 0,
            'knowledge_gaps_detected': 0,
            'manual_review_items': 0,
            'publication_recommendations': 'Review all draft candidates and approve them.'
        }
        
        ExtractedKnowledgeCandidate.objects.filter(status='draft').delete()
        
        candidate_objs = []
        for index, data in enumerate(candidates_data):
            unique_key = (data['entity_type'], data['primary_question'].lower())
            is_internal_dup = unique_key in seen_entity_questions
            seen_entity_questions.add(unique_key)
            
            candidate = ExtractedKnowledgeCandidate(
                entity_type=data['entity_type'],
                entity_name=data['entity_name'],
                primary_question=data['primary_question'],
                alternative_questions=json.dumps(generate_question_variants(data['entity_type'], data['entity_name'], data['primary_question'])),
                canonical_answer=data['canonical_answer'],
                keywords=data['keywords'],
                synonyms=data['synonyms'],
                source_url=data['source_url'],
                source_section=data['source_section'],
                search_weight=data['search_weight'],
                status='draft',
            )
            
            if is_internal_dup:
                candidate.classification = 'duplicate'
                stats['duplicate_candidates'] += 1
            else:
                self._match_and_classify(candidate, existing_articles, stats)
                
            candidate.save()
            candidate_objs.append(candidate)
            
        stats['new_conversational_qa_generated'] = stats['total_website_entities_analysed'] - stats['existing_kb_matches'] - stats['duplicate_candidates']
        
        return candidate_objs, stats

    def _match_and_classify(self, candidate: ExtractedKnowledgeCandidate, existing_articles: List[KnowledgeArticle], stats: Dict[str, Any]) -> None:
        matched = None
        for art in existing_articles:
            if art.page_title.lower().strip() == candidate.primary_question.lower().strip():
                matched = art
                break
                
        if not matched:
            entity_slug = candidate.entity_name.lower().replace(' ', '-')
            for art in existing_articles:
                if f"Conversational:{candidate.entity_type}:{entity_slug}" in art.source_ref:
                    matched = art
                    break
                    
        if matched:
            candidate.matched_article = matched
            stats['existing_kb_matches'] += 1
            
            is_manually_curated = matched.modified_by not in ['admin', 'system']
            
            content_changed = (
                matched.summary.strip() != candidate.canonical_answer.strip() or
                matched.page_title.strip() != candidate.primary_question.strip() or
                matched.keywords.strip() != candidate.keywords.strip()
            )
            
            if content_changed:
                if is_manually_curated:
                    candidate.classification = 'review_required'
                    stats['manual_review_items'] += 1
                else:
                    candidate.classification = 'existing_update'
            else:
                candidate.classification = 'existing_no_action'
        else:
            candidate.classification = 'new_candidate'
            stats['knowledge_gaps_detected'] += 1
