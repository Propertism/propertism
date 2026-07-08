"""
chat/rule_engine.py — M2.4 Rule Engine Core
Evaluates user queries against registered BusinessRule configurations deterministically
without using AI inference. Provides confidence scoring, priority routing,
conflict resolution, clarification checking, fallback management, and audit logging.
"""
import re
import time
from dataclasses import dataclass
from typing import List, Optional
from django.utils import timezone
from chat.models import BusinessRule, RuleExecutionLog

@dataclass
class IntentResult:
    intent: str
    rule_id: Optional[str]
    confidence: float
    action_type: str
    action_config: dict
    outcome: str  # resolved / clarification / fallback / unknown
    clarification_question: str = ""
    rules_evaluated: int = 0
    matched_rule: Optional[BusinessRule] = None

class RuleEvaluator:
    """Evaluates a single BusinessRule against a normalized user query."""
    
    def __init__(self, rule: BusinessRule):
        self.rule = rule
        self.positive_keywords = rule.get_positive_keyword_list()
        self.negative_keywords = rule.get_negative_keyword_list()
        self.phrase_patterns = rule.get_phrase_pattern_list()

    def evaluate(self, query: str, query_tokens: List[str]) -> float:
        """
        Calculates a confidence score between 0.0 and 1.0.
        Formula:
          score = (positive_hits * weight + phrase_hits * 3.0 - negative_hits * 2.0) / max(1, len(positive_keywords))
        """
        if not self.positive_keywords and not self.phrase_patterns:
            # Special case for catch-all fallback rule which has no keywords
            if self.rule.intent == 'unknown_intent':
                return 0.001
            return 0.0

        # 3. Negative Keyword exclusions
        negative_hits = sum(1 for kw in self.negative_keywords if kw in query_tokens)
        if negative_hits > 0:
            return 0.0

        # 2. Phrase pattern matches (substring matching on full normalized query)
        phrase_hits = sum(1 for phrase in self.phrase_patterns if phrase in query)
        if phrase_hits > 0:
            return 1.0

        # 1. Positive Keyword matches
        positive_hits = sum(1 for kw in self.positive_keywords if kw in query_tokens)
        if positive_hits <= 0:
            return 0.0

        # Normalize score based on query length and keyword list size to avoid long list penalties
        normalization_factor = min(len(query_tokens), len(self.positive_keywords)) if self.positive_keywords else 1
        confidence = (positive_hits * self.rule.keyword_weight) / normalization_factor
        return min(1.0, max(0.0, confidence))

class RuleEngine:
    """Deterministic intent classification engine."""
    
    def evaluate(self, query: str, session_id=None) -> IntentResult:
        start_time = time.time()
        
        # Check if the query is an exact match for an active suggestion display text (case-insensitive)
        from chat.models import SuggestionDefinition, BusinessRule
        
        HARDCODED_CHIPS = {
            'talk to advisor': 'human_assistance',
            'contact advisor': 'human_assistance',
            'ask for advisor': 'human_assistance',
            'talk to support': 'human_assistance',
            'contact us': 'contact_information',
            'luxury villas': 'buy_property',
            'apartments': 'buy_property',
            'plots': 'land_plot',
            'nri investment': 'nri_assist',
        }
        
        display_text_clean = query.strip().lower()
        matched_intent = HARDCODED_CHIPS.get(display_text_clean)
        
        rule = None
        if matched_intent:
            rule = BusinessRule.objects.filter(intent=matched_intent, is_enabled=True).first()
        else:
            suggestion = SuggestionDefinition.objects.filter(display_text__iexact=query.strip(), status='active').first()
            if suggestion and suggestion.business_intent:
                rule = BusinessRule.objects.filter(intent=suggestion.business_intent, is_enabled=True).first()
                
        if rule:
            execution_time_ms = int((time.time() - start_time) * 1000)
            log_entry = RuleExecutionLog.objects.create(
                session_id=session_id,
                query=query,
                matched_rule=rule,
                resolved_intent=rule.intent,
                confidence_score=1.0,
                rules_evaluated=1,
                outcome='resolved',
                execution_time_ms=execution_time_ms
            )
            return IntentResult(
                intent=rule.intent,
                rule_id=rule.rule_id,
                confidence=1.0,
                action_type=rule.action_type,
                action_config=rule.action_config,
                outcome='resolved',
                clarification_question='',
                rules_evaluated=1,
                matched_rule=rule
            )
        
        # Normalize query
        normalized_query = query.strip().lower()
        # Clean punctuation for keyword matching but keep spaces for phrase matching
        clean_query = re.sub(r'[^\w\s\-\u0900-\u097F]', ' ', normalized_query)
        query_tokens = [t.strip() for t in clean_query.split() if t.strip()]
        
        # Get all enabled rules ordered by priority (1 is highest)
        rules = list(BusinessRule.objects.filter(is_enabled=True).order_by('priority'))
        rules_evaluated = len(rules)
        
        candidates = []
        unknown_rule = None
        
        for rule in rules:
            if rule.intent == 'unknown_intent':
                unknown_rule = rule
                continue
                
            evaluator = RuleEvaluator(rule)
            confidence = evaluator.evaluate(normalized_query, query_tokens)
            
            if confidence >= rule.min_confidence:
                candidates.append({
                    'rule': rule,
                    'confidence': confidence
                })
                
        # Sort candidates by confidence (descending) and then priority (ascending)
        candidates.sort(key=lambda x: (-x['confidence'], x['rule'].priority))
        
        outcome = 'resolved'
        winner = None
        confidence = 0.0
        intent = 'unknown_intent'
        action_type = 'fallback_response'
        action_config = {}
        clarification_q = ""
        
        # Clarification Threshold logic (if top 2 candidates are very close in confidence)
        if len(candidates) >= 2:
            first = candidates[0]
            second = candidates[1]
            # If the difference is within 0.15 and they map to different intents
            if (first['confidence'] - second['confidence']) <= 0.15 and first['rule'].intent != second['rule'].intent:
                outcome = 'clarification'
                # Merge options or use the clarification question of the highest scoring rule
                winner = first['rule']
                intent = 'unknown_intent'  # Routing is ambiguous
                action_type = 'clarification'
                action_config = {
                    'options': [first['rule'].intent, second['rule'].intent],
                    'candidates': [
                        {'intent': first['rule'].intent, 'rule_id': first['rule'].rule_id, 'confidence': first['confidence']},
                        {'intent': second['rule'].intent, 'rule_id': second['rule'].rule_id, 'confidence': second['confidence']}
                    ]
                }
                confidence = first['confidence']
                clarification_q = (
                    first['rule'].clarification_question or 
                    f"Did you mean {first['rule'].name} or {second['rule'].name}?"
                )
                
        if outcome == 'resolved':
            if candidates:
                best = candidates[0]
                winner = best['rule']
                confidence = best['confidence']
                intent = winner.intent
                action_type = winner.action_type
                action_config = winner.action_config
            else:
                # No rule matched above their thresholds -> fall back to Unknown
                outcome = 'fallback'
                winner = unknown_rule
                confidence = 0.0
                intent = 'unknown_intent'
                action_type = unknown_rule.action_type if unknown_rule else 'fallback_response'
                action_config = unknown_rule.action_config if unknown_rule else {}
                
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Persist audit execution log
        log_entry = RuleExecutionLog.objects.create(
            session_id=session_id,
            query=query,
            matched_rule=winner,
            resolved_intent=intent,
            confidence_score=confidence,
            rules_evaluated=rules_evaluated,
            outcome=outcome,
            execution_time_ms=execution_time_ms
        )
        
        return IntentResult(
            intent=intent,
            rule_id=winner.rule_id if winner else None,
            confidence=confidence,
            action_type=action_type,
            action_config=action_config,
            outcome=outcome,
            clarification_question=clarification_q,
            rules_evaluated=rules_evaluated,
            matched_rule=winner
        )
