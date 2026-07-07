"""
chat/knowledge_manager.py — M2.15 Knowledge Administration Framework.
Implements QualityValidator, VersionManager, PublishingFramework, ReindexFramework,
and KnowledgeAdministrationManager facade.
"""
import logging
from typing import Any, Dict, List, Optional, Tuple
from django.utils import timezone
from chat.models import (
    KnowledgeArticle, KnowledgeDocument, KnowledgeVersionHistory,
    KnowledgeLifecycleAuditLog, KNOWLEDGE_STATE_CHOICES
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Knowledge Quality Validation
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgeValidationFramework:
    """
    Assesses knowledge asset quality metrics before publication.
    Computes score and returns list of validation issues.
    """

    def validate_article(self, article: KnowledgeArticle) -> Tuple[float, List[str]]:
        return self.validate_content(
            title=article.page_title,
            main_content=article.main_content,
            summary=article.summary,
            keywords=article.keywords,
            tags=article.tags
        )

    def validate_document(self, doc: KnowledgeDocument) -> Tuple[float, List[str]]:
        return self.validate_content(
            title=doc.title,
            main_content=doc.title,  # Doc level content fallback
            summary=doc.tags,        # Doc level tags fallback
            keywords=doc.doc_slug,
            tags=doc.tags
        )

    def validate_content(
        self,
        title: str,
        main_content: str,
        summary: str,
        keywords: str,
        tags: str
    ) -> Tuple[float, List[str]]:
        """Runs quality rule checks and returns (score, issues)."""
        issues = []
        score = 100.0

        # Rule 1: Title Validation
        if not title or len(str(title).strip()) < 5:
            issues.append("Title is missing or too short (minimum 5 characters).")
            score -= 20.0

        # Rule 2: Content Completeness
        content_len = len(str(main_content or '').strip())
        if content_len < 20:
            issues.append("Main content is missing or too short (minimum 20 characters).")
            score -= 30.0

        # Rule 3: Summary Presence
        if not summary or len(str(summary).strip()) < 10:
            issues.append("Summary is missing or too short (minimum 10 characters).")
            score -= 15.0

        # Rule 4: Keywords and Tags Quantity
        keywords_list = [k.strip() for k in str(keywords or '').replace(',', ' ').split() if k.strip()]
        if len(keywords_list) < 2:
            issues.append("Asset should have at least 2 keywords.")
            score -= 15.0

        # Rule 5: Duplicate Keywords check
        if len(keywords_list) != len(set(keywords_list)):
            issues.append("Duplicate keywords detected.")
            score -= 10.0

        # Prevent negative score
        final_score = max(0.0, score)
        return final_score, issues


# ─────────────────────────────────────────────────────────────────────────────
# 2. Knowledge Version Manager
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgeVersionManager:
    """
    Manages creation of immutable historical content versions, diffing,
    and rolling back to older versions.
    """

    def create_version(
        self,
        article: Optional[KnowledgeArticle] = None,
        document: Optional[KnowledgeDocument] = None,
        user: str = 'admin'
    ) -> KnowledgeVersionHistory:
        """Saves current state as an immutable history version."""
        if article:
            version_num = article.version
            hist = KnowledgeVersionHistory.objects.create(
                article=article,
                version=version_num,
                title=article.page_title,
                summary=article.summary,
                main_content=article.main_content,
                keywords=article.keywords,
                tags=article.tags,
                search_weight=article.search_weight,
                created_by=user
            )
            # Log versioning event
            KnowledgeLifecycleAuditLog.objects.create(
                article_id=article.knowledge_id,
                action='versioned',
                performed_by=user,
                details={'version': version_num, 'history_id': hist.version_id}
            )
            return hist
        elif document:
            version_num = document.version
            hist = KnowledgeVersionHistory.objects.create(
                document=document,
                version=version_num,
                title=document.title,
                summary=document.tags,  # fallback summary
                main_content='',
                keywords=document.doc_slug,
                tags=document.tags,
                created_by=user
            )
            # Log versioning event
            KnowledgeLifecycleAuditLog.objects.create(
                doc_id=document.doc_id,
                action='versioned',
                performed_by=user,
                details={'version': version_num, 'history_id': hist.version_id}
            )
            return hist
        else:
            raise ValueError("Must specify either article or document to version.")

    def compare_versions(self, v1: KnowledgeVersionHistory, v2: KnowledgeVersionHistory) -> Dict[str, Any]:
        """Compares two historical versions and returns changed fields."""
        fields = ['title', 'summary', 'main_content', 'keywords', 'tags', 'search_weight']
        diff = {}
        for f in fields:
            val1 = getattr(v1, f, None)
            val2 = getattr(v2, f, None)
            if val1 != val2:
                diff[f] = {
                    'v1': val1,
                    'v2': val2
                }
        return diff

    def rollback(self, history: KnowledgeVersionHistory, user: str = 'admin') -> Tuple[bool, str]:
        """Restores a past historical version to the live asset."""
        if history.article:
            art = history.article
            # Create a version of the current state before rolling back (safeguard)
            self.create_version(article=art, user=user)

            # Revert fields
            art.page_title = history.title
            art.summary = history.summary
            art.main_content = history.main_content
            art.keywords = history.keywords
            art.tags = history.tags
            art.search_weight = history.search_weight
            art.version += 1
            art.modified_by = user
            art.save()

            # Log audit
            KnowledgeLifecycleAuditLog.objects.create(
                article_id=art.knowledge_id,
                action='rollback',
                performed_by=user,
                details={'rolled_back_to_version': history.version, 'history_id': history.version_id}
            )
            return True, f"Article {art.knowledge_id} successfully rolled back to version {history.version}."
        elif history.document:
            doc = history.document
            # Safeguard current version
            self.create_version(document=doc, user=user)

            # Revert fields
            doc.title = history.title
            doc.tags = history.tags
            doc.version += 1
            doc.modified_by = user
            doc.save()

            # Log audit
            KnowledgeLifecycleAuditLog.objects.create(
                doc_id=doc.doc_id,
                action='rollback',
                performed_by=user,
                details={'rolled_back_to_version': history.version, 'history_id': history.version_id}
            )
            return True, f"Document {doc.doc_id} successfully rolled back to version {history.version}."

        return False, "Invalid history target."


# ─────────────────────────────────────────────────────────────────────────────
# 3. Knowledge Publishing Framework
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgePublishingFramework:
    """
    Manages asset state transitions (Draft -> Review -> Approved -> Published -> Archived).
    Enforces quality checks and publication actions.
    """

    ALLOWED_TRANSITIONS = {
        'draft': ['review', 'archived'],
        'review': ['approved', 'draft', 'archived'],
        'approved': ['published', 'draft', 'archived'],
        'published': ['archived', 'deprecated'],
        'archived': ['draft'],
        'deprecated': ['archived']
    }

    def __init__(self):
        self.validator = KnowledgeValidationFramework()
        self.reindex_mgr = KnowledgeReindexFramework()

    def transition_state(self, asset: Any, new_status: str, user: str = 'admin') -> Tuple[bool, str]:
        """Transitions asset to new lifecycle status."""
        current_status = asset.status
        new_status = new_status.lower()

        # Validate status exists
        valid_statuses = [choice[0] for choice in KNOWLEDGE_STATE_CHOICES]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status '{new_status}'. Choices: {valid_statuses}")

        # Check transition validity (support administrative overrides if transitioning directly,
        # but enforce logical path from draft to published)
        if current_status == new_status:
            return True, f"Status is already {new_status}."

        # Quality Gate for Publishing
        if new_status == 'published':
            # Calculate and store quality score
            if isinstance(asset, KnowledgeArticle):
                score, issues = self.validator.validate_article(asset)
            else:
                score, issues = self.validator.validate_document(asset)

            asset.quality_score = score
            if score < 70.0:
                raise ValueError(f"Quality score ({score}) is below publication threshold (70.0). Issues: {issues}")

            asset.published_date = timezone.now()

        # Update status
        asset.status = new_status
        asset.modified_by = user
        asset.save()

        # Log audit
        details = {'from_status': current_status, 'to_status': new_status}
        if isinstance(asset, KnowledgeArticle):
            KnowledgeLifecycleAuditLog.objects.create(
                article_id=asset.knowledge_id,
                action='published' if new_status == 'published' else 'unpublished',
                performed_by=user,
                details=details
            )
        else:
            KnowledgeLifecycleAuditLog.objects.create(
                doc_id=asset.doc_id,
                action='published' if new_status == 'published' else 'unpublished',
                performed_by=user,
                details=details
            )

        # Trigger indexing on publish
        if new_status == 'published':
            self.reindex_mgr.trigger_reindex(source_type=asset.source_type)

        return True, f"Successfully transitioned to status '{new_status}'."


# ─────────────────────────────────────────────────────────────────────────────
# 4. Knowledge Re-index Framework
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgeReindexFramework:
    """
    Triggers content index runs for website pages or internal Markdown files.
    """

    def trigger_reindex(self, source_type: Optional[str] = None) -> Dict[str, Any]:
        """Runs the indexers and logs re-index statistics."""
        start_time = timezone.now()
        stats = {
            'indexed': 0,
            'updated': 0,
            'skipped': 0,
            'errors': []
        }

        try:
            # Reindex Website
            if not source_type or source_type == 'Website':
                from chat.indexer import WebsiteContentIndexer
                web_res = WebsiteContentIndexer().index_all()
                stats['indexed'] += web_res.indexed
                stats['updated'] += web_res.updated
                stats['skipped'] += web_res.skipped
                stats['errors'].extend(web_res.errors)

            # Reindex Documents
            if not source_type or source_type in ['Markdown', 'Policy', 'FAQ', 'Terms', 'FeeStructure']:
                from chat.indexer import DocumentIndexer
                doc_res = DocumentIndexer().index_all()
                stats['indexed'] += doc_res.indexed
                stats['updated'] += doc_res.updated
                stats['skipped'] += doc_res.skipped
                stats['errors'].extend(doc_res.errors)

            # Log reindex execution in lifecycle log
            duration = int((timezone.now() - start_time).total_seconds() * 1000)
            KnowledgeLifecycleAuditLog.objects.create(
                action='reindexed',
                performed_by='system',
                details={'source_type': source_type, 'duration_ms': duration, 'stats': stats}
            )

        except Exception as exc:
            logger.exception(f"Re-indexing failed: {exc}")
            stats['errors'].append(str(exc))

        return stats


# ─────────────────────────────────────────────────────────────────────────────
# 5. Central Knowledge Administration Manager
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgeAdministrationManager:
    """
    Facade class governing registrations, edits, cloning, analytics,
    and administrative functions for all knowledge assets.
    """

    def __init__(self):
        self.validator = KnowledgeValidationFramework()
        self.version_mgr = KnowledgeVersionManager()
        self.publishing = KnowledgePublishingFramework()
        self.reindex_mgr = KnowledgeReindexFramework()

    def register_article(self, data: Dict[str, Any], user: str = 'admin') -> KnowledgeArticle:
        """Registers a new knowledge article."""
        article = KnowledgeArticle.objects.create(
            page_title=data['page_title'],
            url=data.get('url', ''),
            category=data.get('category', 'General'),
            language=data.get('language', 'en'),
            keywords=data.get('keywords', ''),
            summary=data.get('summary', ''),
            main_content=data.get('main_content', ''),
            published_status=data.get('published_status', 'published'),
            search_weight=data.get('search_weight', 1.0),
            source_type=data.get('source_type', 'Website'),
            source_ref=data['source_ref'],
            status='draft',  # Newly registered assets start as draft
            modified_by=user
        )

        # Compute initial validation score
        score, _ = self.validator.validate_article(article)
        article.quality_score = score
        article.save()

        # Log version and audit
        self.version_mgr.create_version(article=article, user=user)
        KnowledgeLifecycleAuditLog.objects.create(
            article_id=article.knowledge_id,
            action='registered',
            performed_by=user,
            details={'title': article.page_title}
        )
        return article

    def edit_article(self, article: KnowledgeArticle, data: Dict[str, Any], user: str = 'admin') -> KnowledgeArticle:
        """Edits fields of an article, increments version, and saves history."""
        # Create history of the state BEFORE editing
        self.version_mgr.create_version(article=article, user=user)

        # Edit fields
        for field in ['page_title', 'url', 'category', 'language', 'keywords', 'summary', 'main_content', 'search_weight', 'source_type', 'tags']:
            if field in data:
                setattr(article, field, data[field])

        article.version += 1
        article.modified_by = user
        # Re-evaluate quality score
        score, _ = self.validator.validate_article(article)
        article.quality_score = score
        article.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            article_id=article.knowledge_id,
            action='edited',
            performed_by=user,
            details={'fields_updated': list(data.keys())}
        )
        return article

    def clone_article(self, article: KnowledgeArticle, user: str = 'admin') -> KnowledgeArticle:
        """Clones an existing article into a new Draft article."""
        cloned_ref = f"{article.source_ref}-clone-{timezone.now().strftime('%s')}"
        cloned = KnowledgeArticle.objects.create(
            page_title=f"Copy of {article.page_title}",
            url=article.url,
            category=article.category,
            language=article.language,
            keywords=article.keywords,
            summary=article.summary,
            main_content=article.main_content,
            search_weight=article.search_weight,
            source_type=article.source_type,
            source_ref=cloned_ref[:200],
            tags=article.tags,
            status='draft',
            modified_by=user
        )
        # Audit clone
        KnowledgeLifecycleAuditLog.objects.create(
            article_id=article.knowledge_id,
            action='cloned',
            performed_by=user,
            details={'cloned_to_id': cloned.knowledge_id}
        )
        return cloned

    def archive_article(self, article: KnowledgeArticle, user: str = 'admin') -> KnowledgeArticle:
        """Archives an article (sets status to 'archived')."""
        # Create history of the current state
        self.version_mgr.create_version(article=article, user=user)

        # Update status
        article.status = 'archived'
        article.version += 1
        article.modified_by = user
        article.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            article_id=article.knowledge_id,
            action='archived',
            performed_by=user,
            details={}
        )
        return article

    def deprecated_article(self, article: KnowledgeArticle, user: str = 'admin') -> KnowledgeArticle:
        """Marks an article as deprecated."""
        # Create history of the current state
        self.version_mgr.create_version(article=article, user=user)

        # Update status
        article.status = 'deprecated'
        article.version += 1
        article.modified_by = user
        article.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            article_id=article.knowledge_id,
            action='deprecated',
            performed_by=user,
            details={}
        )
        return article

    def add_tags_article(self, article: KnowledgeArticle, tags: str, user: str = 'admin') -> KnowledgeArticle:
        """Adds tags to an article (appends to existing tags, avoiding duplicates)."""
        # Create history of the current state
        self.version_mgr.create_version(article=article, user=user)

        # Combine existing and new tags
        existing_tags = set(t.strip() for t in article.tags.split(',') if t.strip())
        new_tags = set(t.strip() for t in tags.split(',') if t.strip())
        all_tags = sorted(list(existing_tags.union(new_tags)))
        article.tags = ', '.join(all_tags)

        article.version += 1
        article.modified_by = user
        article.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            article_id=article.knowledge_id,
            action='tags_added',
            performed_by=user,
            details={'added_tags': list(new_tags)}
        )
        return article

    def update_content_article(self, article: KnowledgeArticle, main_content: str = None, summary: str = None, user: str = 'admin') -> KnowledgeArticle:
        """Updates the main content and/or summary of an article."""
        # Create history of the current state
        self.version_mgr.create_version(article=article, user=user)

        # Update fields if provided
        if main_content is not None:
            article.main_content = main_content
        if summary is not None:
            article.summary = summary

        # Re-evaluate quality score
        score, _ = self.validator.validate_article(article)
        article.quality_score = score

        article.version += 1
        article.modified_by = user
        article.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            article_id=article.knowledge_id,
            action='content_updated',
            performed_by=user,
            details={'updated_fields': []}
        )
        return article

    # Document methods
    def register_document(self, data: Dict[str, Any], user: str = 'admin') -> KnowledgeDocument:
        """Registers a new knowledge document."""
        document = KnowledgeDocument.objects.create(
            title=data['title'],
            doc_slug=data.get('doc_slug', ''),
            file_path=data.get('file_path', ''),
            source_type=data.get('source_type', 'Website'),
            category=data.get('category', 'General'),
            language=data.get('language', 'en'),
            tags=data.get('tags', ''),
            published_status=data.get('published_status', 'published'),
            search_weight=data.get('search_weight', 1.0),
            section_count=data.get('section_count', 0),
            status='draft',  # Newly registered assets start as draft
            modified_by=user
        )

        # Compute initial validation score
        score, _ = self.validator.validate_document(document)
        document.quality_score = score
        document.save()

        # Log version and audit
        self.version_mgr.create_version(document=document, user=user)
        KnowledgeLifecycleAuditLog.objects.create(
            doc_id=document.doc_id,
            action='registered',
            performed_by=user,
            details={'title': document.title}
        )
        return document

    def edit_document(self, document: KnowledgeDocument, data: Dict[str, Any], user: str = 'admin') -> KnowledgeDocument:
        """Edits fields of a document, increments version, and saves history."""
        # Create history of the state BEFORE editing
        self.version_mgr.create_version(document=document, user=user)

        # Edit fields
        for field in ['title', 'doc_slug', 'file_path', 'source_type', 'category', 'language', 'tags', 'search_weight', 'section_count']:
            if field in data:
                setattr(document, field, data[field])

        document.version += 1
        document.modified_by = user
        # Re-evaluate quality score
        score, _ = self.validator.validate_document(document)
        document.quality_score = score
        document.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            doc_id=document.doc_id,
            action='edited',
            performed_by=user,
            details={'fields_updated': list(data.keys())}
        )
        return document

    def clone_document(self, document: KnowledgeDocument, user: str = 'admin') -> KnowledgeDocument:
        """Clones an existing document into a new Draft document."""
        cloned_ref = f"{document.doc_slug}-clone-{timezone.now().strftime('%s')}"
        cloned = KnowledgeDocument.objects.create(
            title=f"Copy of {document.title}",
            doc_slug=cloned_ref[:200],
            file_path=document.file_path,
            source_type=document.source_type,
            category=document.category,
            language=document.language,
            tags=document.tags,
            published_status=document.published_status,
            search_weight=document.search_weight,
            section_count=document.section_count,
            status='draft',
            modified_by=user
        )
        # Audit clone
        KnowledgeLifecycleAuditLog.objects.create(
            doc_id=document.doc_id,
            action='cloned',
            performed_by=user,
            details={'cloned_to_id': cloned.doc_id}
        )
        return cloned

    def archive_document(self, document: KnowledgeDocument, user: str = 'admin') -> KnowledgeDocument:
        """Archives a document (sets status to 'archived')."""
        # Create history of the current state
        self.version_mgr.create_version(document=document, user=user)

        # Update status
        document.status = 'archived'
        document.version += 1
        document.modified_by = user
        document.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            doc_id=document.doc_id,
            action='archived',
            performed_by=user,
            details={}
        )
        return document

    def deprecated_document(self, document: KnowledgeDocument, user: str = 'admin') -> KnowledgeDocument:
        """Marks a document as deprecated."""
        # Create history of the current state
        self.version_mgr.create_version(document=document, user=user)

        # Update status
        document.status = 'deprecated'
        document.version += 1
        document.modified_by = user
        document.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            doc_id=document.doc_id,
            action='deprecated',
            performed_by=user,
            details={}
        )
        return document

    def add_tags_document(self, document: KnowledgeDocument, tags: str, user: str = 'admin') -> KnowledgeDocument:
        """Adds tags to a document (appends to existing tags, avoiding duplicates)."""
        # Create history of the current state
        self.version_mgr.create_version(document=document, user=user)

        # Combine existing and new tags
        existing_tags = set(t.strip() for t in document.tags.split(',') if t.strip())
        new_tags = set(t.strip() for t in tags.split(',') if t.strip())
        all_tags = sorted(list(existing_tags.union(new_tags)))
        document.tags = ', '.join(all_tags)

        document.version += 1
        document.modified_by = user
        document.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            doc_id=document.doc_id,
            action='tags_added',
            performed_by=user,
            details={'added_tags': list(new_tags)}
        )
        return document

    def update_content_document(self, document: KnowledgeDocument, title: str = None, doc_slug: str = None, user: str = 'admin') -> KnowledgeDocument:
        """Updates the title and/or doc_slug of a document."""
        # Create history of the current state
        self.version_mgr.create_version(document=document, user=user)

        # Update fields if provided
        if title is not None:
            document.title = title
        if doc_slug is not None:
            document.doc_slug = doc_slug

        document.version += 1
        document.modified_by = user
        document.save()

        # Log audit
        KnowledgeLifecycleAuditLog.objects.create(
            doc_id=document.doc_id,
            action='content_updated',
            performed_by=user,
            details={'updated_fields': []}
        )
        return document