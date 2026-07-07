"""
chat/search.py — M2.2 Website Knowledge Base + M2.3 Internal Knowledge Repository
KnowledgeSearchEngine: deterministic keyword-based retrieval over KnowledgeArticle.
Searches all source types (Website + Internal) by default via source_types=None.
No AI, embeddings, or semantic search. Responses always include source references.
"""
import logging
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger('chat')


@dataclass
class SearchMatch:
    article_id: int
    knowledge_id: str
    page_title: str
    url: str
    category: str
    summary: str
    relevance_score: float
    source_type: str
    source_ref: str
    keywords: str
    document_ref: str = ""  # M2.3: "Document Title → Section Heading" for internal docs


@dataclass
class SearchResult:
    matches: List[SearchMatch] = field(default_factory=list)
    query: str = ""
    total_found: int = 0
    source_references: List[str] = field(default_factory=list)

    def as_dict(self):
        return {
            "query": self.query,
            "total_found": self.total_found,
            "matches": [
                {
                    "id": m.article_id,
                    "knowledge_id": m.knowledge_id,
                    "title": m.page_title,
                    "url": m.url,
                    "category": m.category,
                    "summary": m.summary,
                    "relevance_score": round(m.relevance_score, 3),
                    "source_type": m.source_type,
                    "source_ref": m.source_ref,
                    "document_ref": m.document_ref,
                }
                for m in self.matches
            ],
            "source_references": self.source_references,
        }


def _score_article(article, query_terms: List[str]) -> float:
    """
    Compute a relevance score for a KnowledgeArticle against query terms.

    Scoring weights:
    - Title match:    3.0x per term occurrence
    - Keywords match: 2.0x per term occurrence
    - Summary match:  1.5x per term occurrence
    - Content match:  1.0x per term occurrence

    Final score is multiplied by the article's search_weight.
    """
    title = (article.page_title or "").lower()
    keywords = (article.keywords or "").lower()
    summary = (article.summary or "").lower()
    content = (article.main_content or "").lower()

    score = 0.0
    for term in query_terms:
        if not term:
            continue
        score += title.count(term) * 3.0
        score += keywords.count(term) * 2.0
        score += summary.count(term) * 1.5
        score += content.count(term) * 1.0

    return score * article.search_weight


def _build_document_ref(article) -> str:
    """
    Build a human-readable document reference for an internal document article.
    Format: "Document Title → Section Heading"
    For website articles (no dash separator in source_ref meaning), returns empty string.
    """
    source_ref = article.source_ref or ""
    parts = source_ref.split(':')
    # source_ref format: {source_type}:{doc_slug}:{section_slug}
    if len(parts) >= 3 and parts[2] not in ('', '__doc__'):
        # Extract section heading from page_title: "Doc Title — Section Heading"
        if ' \u2014 ' in article.page_title:
            doc_part, section_part = article.page_title.split(' \u2014 ', 1)
            return f"{doc_part} \u2192 {section_part}"
        return article.page_title
    return ""


# Internal source types — used to build document_ref and source citations
_INTERNAL_SOURCE_TYPES = {'Markdown', 'Policy', 'Terms', 'FeeStructure', 'FAQ'}
_WEBSITE_SOURCE_TYPE = 'Website'


class KnowledgeSearchEngine:
    """
    Deterministic keyword-based search over indexed KnowledgeArticle records.
    Searches all source types (Website + Internal) by default.
    Returns ranked results with source and document references.
    """

    def search(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None,
        source_types: Optional[List[str]] = None,
    ) -> SearchResult:
        """
        Search indexed knowledge articles across all source types.

        Args:
            query: Natural language or keyword query string.
            top_k: Maximum number of matches to return.
            category: Optional category filter (e.g., 'Service', 'General').
            source_types: Optional list of source types to restrict search.
                          None (default) = search all source types (Website + Internal).
        """
        from chat.models import KnowledgeArticle

        result = SearchResult(query=query)

        if not query or not query.strip():
            return result

        query_terms = [term.lower() for term in query.lower().split() if len(term) > 2]
        if not query_terms:
            query_terms = [query.lower().strip()]

        # Base queryset — only published articles across all sources
        qs = KnowledgeArticle.objects.filter(published_status='published', status='published')
        if source_types:
            qs = qs.filter(source_type__in=source_types)
        if category:
            qs = qs.filter(category=category)

        # Score all candidates
        scored = []
        for article in qs:
            score = _score_article(article, query_terms)
            if score > 0:
                scored.append((score, article))

        # Sort by score descending and take top_k
        scored.sort(key=lambda x: x[0], reverse=True)
        top_results = scored[:top_k]
        
        # Increment usage_count on returned matches
        for score, article in top_results:
            article.usage_count += 1
            article.save(update_fields=['usage_count'])

        result.total_found = len(scored)
        result.matches = [
            SearchMatch(
                article_id=article.pk,
                knowledge_id=article.knowledge_id,
                page_title=article.page_title,
                url=article.url,
                category=article.category,
                summary=article.summary,
                relevance_score=score,
                source_type=article.source_type,
                source_ref=article.source_ref,
                keywords=article.keywords,
                document_ref=_build_document_ref(article),
            )
            for score, article in top_results
        ]

        # Source references: URLs for website matches, document_ref for internal matches
        refs = []
        for m in result.matches:
            if m.url:
                refs.append(m.url)
            elif m.document_ref:
                refs.append(m.document_ref)
        result.source_references = refs

        logger.info(
            f"Knowledge search: query='{query}' → {result.total_found} candidates, "
            f"returning top {len(result.matches)}"
        )
        return result
