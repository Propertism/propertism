"""
chat/indexer.py — M2.2 Website Knowledge Base + M2.3 Internal Knowledge Repository
WebsiteContentIndexer reads published Propertism Django model records and upserts
them as KnowledgeArticle records.
DocumentIndexer ingests internal Markdown documents from chat/knowledge_docs/.
"""
import logging
from dataclasses import dataclass, field
from typing import List

from django.utils import timezone

logger = logging.getLogger('chat')


@dataclass
class IndexResult:
    indexed: int = 0
    updated: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)

    def as_dict(self):
        return {
            "indexed": self.indexed,
            "updated": self.updated,
            "skipped": self.skipped,
            "errors": self.errors,
            "total_processed": self.indexed + self.updated + self.skipped,
        }


def _keywords_from(*text_fields):
    """Combine text fields and extract a clean keyword string."""
    combined = " ".join(str(t) for t in text_fields if t).lower()
    # Basic deduplication of words
    words = dict.fromkeys(combined.split())
    return " ".join(words)


def _upsert_article(source_ref, defaults):
    """
    Insert or update a KnowledgeArticle by source_ref.
    Returns ('created'|'updated'|'skipped', article).
    """
    from chat.models import KnowledgeArticle

    try:
        article, created = KnowledgeArticle.objects.get_or_create(
            source_ref=source_ref,
            defaults=defaults
        )
        if not created:
            # Check whether content has changed before updating
            changed = False
            for key, value in defaults.items():
                if key == 'indexed_at':
                    continue
                if getattr(article, key) != value:
                    changed = True
                    break
            if changed:
                for key, value in defaults.items():
                    setattr(article, key, value)
                article.save()
                return 'updated', article
            return 'skipped', article
        return 'created', article
    except Exception as exc:
        raise RuntimeError(f"Error upserting {source_ref}: {exc}") from exc


class WebsiteContentIndexer:
    """
    Indexes all published Propertism website content into KnowledgeArticle records.
    Each sub-indexer is independent and idempotent.
    """

    def index_all(self) -> IndexResult:
        """Run all sub-indexers and return aggregated IndexResult."""
        result = IndexResult()
        sub_indexers = [
            self.index_company_info,
            self.index_services,
            self.index_blog_posts,
            self.index_team_members,
            self.index_properties,
        ]
        for sub in sub_indexers:
            try:
                sub_result = sub()
                result.indexed += sub_result.indexed
                result.updated += sub_result.updated
                result.skipped += sub_result.skipped
                result.errors.extend(sub_result.errors)
            except Exception as exc:
                error_msg = f"{sub.__name__} failed: {exc}"
                result.errors.append(error_msg)
                logger.error(error_msg)
        logger.info(
            f"realBOT Knowledge index complete — indexed: {result.indexed}, "
            f"updated: {result.updated}, skipped: {result.skipped}, errors: {len(result.errors)}"
        )
        return result

    def index_company_info(self) -> IndexResult:
        """Index CompanyInfo: About, Contact, Home sections."""
        result = IndexResult()
        try:
            from content.models import CompanyInfo
            company = CompanyInfo.objects.first()
            if not company:
                return result

            records = [
                {
                    "source_ref": "Website:company:about",
                    "page_title": f"About {company.company_name}",
                    "url": "/about/",
                    "category": "About",
                    "summary": company.about_description[:200] if company.about_description else company.tagline,
                    "main_content": "\n".join(filter(None, [
                        company.tagline,
                        company.about_mission,
                        company.about_description,
                    ])),
                    "keywords": _keywords_from(
                        company.company_name, company.tagline,
                        company.about_mission, company.about_description
                    ),
                    "search_weight": 1.5,
                },
                {
                    "source_ref": "Website:company:contact",
                    "page_title": "Contact Propertism",
                    "url": "/contact/",
                    "category": "Contact",
                    "summary": f"Contact us at {company.email} or call {company.india_phone_1}",
                    "main_content": "\n".join(filter(None, [
                        company.india_office_address,
                        f"Chennai, {company.india_office_state} {company.india_office_pincode}",
                        f"Phone: {company.india_phone_1}",
                        f"Email: {company.email}",
                        company.us_office_address,
                        f"{company.us_office_city}, {company.us_office_state} {company.us_office_zipcode}",
                        f"US Phone: {company.us_phone}",
                        f"Business Hours: {company.business_hours}",
                    ])),
                    "keywords": _keywords_from(
                        "contact", "phone", "email", "address", "office",
                        company.india_phone_1, company.email, company.business_hours
                    ),
                    "search_weight": 1.3,
                },
            ]
            for rec in records:
                source_ref = rec.pop("source_ref")
                rec.update({
                    "language": "en",
                    "published_status": "published",
                    "source_type": "Website",
                    "last_modified": timezone.now(),
                })
                status, _ = _upsert_article(source_ref, rec)
                if status == 'created':
                    result.indexed += 1
                elif status == 'updated':
                    result.updated += 1
                else:
                    result.skipped += 1
        except Exception as exc:
            result.errors.append(f"index_company_info: {exc}")
            logger.error(f"index_company_info error: {exc}")
        return result

    def index_services(self) -> IndexResult:
        """Index active Service records."""
        result = IndexResult()
        try:
            from content.models import Service
            services = Service.objects.filter(is_active=True)
            for service in services:
                source_ref = f"Website:service:{service.slug}"
                defaults = {
                    "page_title": service.title,
                    "url": f"/services/{service.slug}/",
                    "category": "Service",
                    "summary": service.short_description[:300],
                    "main_content": "\n".join(filter(None, [
                        service.short_description,
                        service.full_description,
                        service.features,
                    ])),
                    "keywords": _keywords_from(
                        service.title, service.short_description,
                        service.full_description, service.features
                    ),
                    "language": "en",
                    "published_status": "published",
                    "source_type": "Website",
                    "search_weight": 2.0,
                    "last_modified": timezone.now(),
                }
                status, _ = _upsert_article(source_ref, defaults)
                if status == 'created':
                    result.indexed += 1
                elif status == 'updated':
                    result.updated += 1
                else:
                    result.skipped += 1
        except Exception as exc:
            result.errors.append(f"index_services: {exc}")
            logger.error(f"index_services error: {exc}")
        return result

    def index_blog_posts(self) -> IndexResult:
        """Index published BlogPost records. Category 'nri' → KA category 'NRI', others → 'Blog'."""
        result = IndexResult()
        try:
            from content.models import BlogPost
            posts = BlogPost.objects.filter(is_published=True)
            for post in posts:
                ka_category = "NRI" if post.category == "nri" else "Blog"
                source_ref = f"Website:blog:{post.slug}"
                # Strip HTML tags from content for clean text storage
                from django.utils.html import strip_tags
                clean_content = strip_tags(post.content)[:3000]
                defaults = {
                    "page_title": post.title,
                    "url": f"/knowledge-hub/{post.slug}/",
                    "category": ka_category,
                    "summary": post.excerpt[:400],
                    "main_content": "\n".join(filter(None, [post.excerpt, clean_content])),
                    "keywords": _keywords_from(
                        post.title, post.excerpt, post.category
                    ),
                    "language": "en",
                    "published_status": "published",
                    "source_type": "Website",
                    "search_weight": 1.2,
                    "last_modified": post.updated_date,
                }
                status, _ = _upsert_article(source_ref, defaults)
                if status == 'created':
                    result.indexed += 1
                elif status == 'updated':
                    result.updated += 1
                else:
                    result.skipped += 1
        except Exception as exc:
            result.errors.append(f"index_blog_posts: {exc}")
            logger.error(f"index_blog_posts error: {exc}")
        return result

    def index_team_members(self) -> IndexResult:
        """Index active TeamMember records under the About category."""
        result = IndexResult()
        try:
            from content.models import TeamMember
            members = TeamMember.objects.filter(is_active=True)
            for member in members:
                slug = member.slug or member.name.lower().replace(" ", "-")
                source_ref = f"Website:team:{slug}"
                defaults = {
                    "page_title": f"{member.name} — {member.role}",
                    "url": "/about/",
                    "category": "About",
                    "summary": f"{member.role} at Propertism. {member.bio[:150]}",
                    "main_content": "\n".join(filter(None, [
                        member.bio,
                        member.expertise,
                        member.department,
                    ])),
                    "keywords": _keywords_from(
                        member.name, member.role, member.expertise, member.department
                    ),
                    "language": "en",
                    "published_status": "published",
                    "source_type": "Website",
                    "search_weight": 0.9,
                    "last_modified": timezone.now(),
                }
                status, _ = _upsert_article(source_ref, defaults)
                if status == 'created':
                    result.indexed += 1
                elif status == 'updated':
                    result.updated += 1
                else:
                    result.skipped += 1
        except Exception as exc:
            result.errors.append(f"index_team_members: {exc}")
            logger.error(f"index_team_members error: {exc}")
        return result

    def index_properties(self) -> IndexResult:
        """Index available Property records."""
        result = IndexResult()
        try:
            from properties.models import Property
            properties = Property.objects.filter(status="available").select_related("property_type")
            for prop in properties:
                source_ref = f"Website:property:{prop.slug}"
                prop_type_name = prop.property_type.name if prop.property_type else "Property"
                defaults = {
                    "page_title": prop.title,
                    "url": f"/properties/{prop.slug}/",
                    "category": "Property",
                    "summary": f"{prop_type_name} in {prop.location}. {prop.formatted_price}.",
                    "main_content": "\n".join(filter(None, [
                        prop.description,
                        f"Location: {prop.location}",
                        f"Type: {prop_type_name}",
                        f"Price: {prop.formatted_price}",
                        f"Status: {prop.status}",
                    ])),
                    "keywords": _keywords_from(
                        prop.title, prop.location, prop_type_name,
                        prop.price_type, "property"
                    ),
                    "language": "en",
                    "published_status": "published",
                    "source_type": "Website",
                    "search_weight": 1.8,
                    "last_modified": prop.updated_at,
                }
                status, _ = _upsert_article(source_ref, defaults)
                if status == 'created':
                    result.indexed += 1
                elif status == 'updated':
                    result.updated += 1
                else:
                    result.skipped += 1
        except Exception as exc:
            result.errors.append(f"index_properties: {exc}")
            logger.error(f"index_properties error: {exc}")
        return result


# ── M2.3 Document Indexer ─────────────────────────────────────────────────────

class DocumentIndexer:
    """
    M2.3 — Ingests internal business documents from chat/knowledge_docs/.
    Each document section becomes an independent KnowledgeArticle.
    Document-level metadata is tracked in KnowledgeDocument.

    Adding a new document:
    1. Drop the .md file into chat/knowledge_docs/.
    2. Add an entry to manifest.json.
    3. Call index_all_documents() or POST /api/v1/realbot/knowledge/index/.
    No code changes required.
    """

    KNOWLEDGE_DOCS_DIR = None  # Resolved at runtime

    def _get_docs_dir(self):
        from pathlib import Path
        if self.KNOWLEDGE_DOCS_DIR is not None:
            return self.KNOWLEDGE_DOCS_DIR
        return Path(__file__).parent / 'knowledge_docs'

    def _split_master_knowledge_base(self):
        """Splits the consolidated propertism-knowledge-base.md into individual markdown files."""
        from pathlib import Path
        import re

        docs_dir = self._get_docs_dir()
        master_file = docs_dir / 'propertism-knowledge-base.md'
        
        if not master_file.exists():
            return

        try:
            with open(master_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split content by "# FILE: <filename>"
            chunks = re.split(r'^# FILE:\s*([a-zA-Z0-9_\-\.]+)\s*\n', content, flags=re.MULTILINE)
            
            for i in range(1, len(chunks), 2):
                filename = chunks[i].strip()
                file_content = chunks[i+1].strip() + '\n'
                target_path = docs_dir / filename
                with open(target_path, 'w', encoding='utf-8') as tf:
                    tf.write(file_content)
        except Exception as exc:
            logger.error(f"DocumentIndexer: failed to split master knowledge base: {exc}")

    def index_all_documents(self) -> 'IndexResult':
        """
        Scan knowledge_docs/ via manifest.json, detect changed files,
        and re-index modified or new documents.
        """
        import json
        from pathlib import Path

        # Automatically rebuild individual markdown files from consolidated master knowledge base
        self._split_master_knowledge_base()

        result = IndexResult()
        docs_dir = self._get_docs_dir()
        manifest_path = docs_dir / 'manifest.json'

        if not manifest_path.exists():
            result.errors.append(f"manifest.json not found at {manifest_path}")
            logger.error(f"DocumentIndexer: manifest.json not found at {manifest_path}")
            return result

        try:
            with open(manifest_path, encoding='utf-8') as f:
                manifest = json.load(f)
        except Exception as exc:
            result.errors.append(f"manifest.json parse error: {exc}")
            logger.error(f"DocumentIndexer: manifest parse error: {exc}")
            return result

        for entry in manifest.get('documents', []):
            file_name = entry.get('file', '')
            source_type = entry.get('source_type', 'Markdown')
            category = entry.get('category', 'General')
            file_path = docs_dir / file_name

            if not file_path.exists():
                result.errors.append(f"File not found: {file_name}")
                logger.warning(f"DocumentIndexer: file not found: {file_path}")
                continue

            try:
                doc_result = self.index_document(
                    file_path=file_path,
                    source_type=source_type,
                    category=category,
                    title=entry.get('title', ''),
                    doc_slug=entry.get('doc_slug', ''),
                    language=entry.get('language', 'en'),
                    tags=entry.get('tags', ''),
                )
                result.indexed += doc_result.indexed
                result.updated += doc_result.updated
                result.skipped += doc_result.skipped
                result.errors.extend(doc_result.errors)
            except Exception as exc:
                result.errors.append(f"Error indexing {file_name}: {exc}")
                logger.error(f"DocumentIndexer: error indexing {file_name}: {exc}")

        logger.info(
            f"DocumentIndexer complete → indexed: {result.indexed}, "
            f"updated: {result.updated}, skipped: {result.skipped}, "
            f"errors: {len(result.errors)}"
        )
        return result

    def index_document(
        self,
        file_path,
        source_type: str,
        category: str,
        title: str = '',
        doc_slug: str = '',
        language: str = 'en',
        tags: str = '',
    ) -> 'IndexResult':
        """
        Parse one document file and upsert its KnowledgeDocument record
        and all section KnowledgeArticle records.
        Skips the file if content hash is unchanged.
        Increments version on change.
        """
        from pathlib import Path
        from chat.document_parser import get_parser_for
        from chat.models import KnowledgeDocument

        file_path = Path(file_path)
        result = IndexResult()

        try:
            parser = get_parser_for(file_path)
            new_hash = parser.compute_hash(file_path)

            # Upsert KnowledgeDocument record
            doc, created = KnowledgeDocument.objects.get_or_create(
                doc_slug=doc_slug or self._slugify(file_path.stem),
                defaults={
                    'title': title or file_path.stem.replace('-', ' ').title(),
                    'file_path': file_path.name,
                    'source_type': source_type,
                    'category': category,
                    'language': language,
                    'tags': tags,
                    'content_hash': new_hash,
                    'published_status': 'published',
                }
            )

            if not created:
                if not doc.is_changed(new_hash):
                    # Nothing changed — skip entirely
                    from chat.models import KnowledgeArticle
                    existing_count = KnowledgeArticle.objects.filter(
                        source_ref__startswith=f"{source_type}:{doc.doc_slug}:"
                    ).count()
                    result.skipped += existing_count
                    logger.info(
                        f"DocumentIndexer: '{file_path.name}' unchanged — skipping "
                        f"({existing_count} sections)"
                    )
                    return result

                # Content changed — increment version
                doc.version += 1
                doc.content_hash = new_hash

            # Parse document
            parsed = parser.parse(file_path)

            # Upsert section articles
            section_result = self._upsert_section_articles(doc, parsed, source_type, category, language)
            result.indexed += section_result.indexed
            result.updated += section_result.updated
            result.skipped += section_result.skipped
            result.errors.extend(section_result.errors)

            # Update doc section count and save
            doc.section_count = len(parsed.sections)
            doc.save()

        except Exception as exc:
            result.errors.append(f"index_document({file_path.name}): {exc}")
            logger.error(f"DocumentIndexer: error in index_document: {exc}", exc_info=True)

        return result

    def _upsert_section_articles(
        self,
        doc,
        parsed,
        source_type: str,
        category: str,
        language: str,
    ) -> 'IndexResult':
        """Upsert one KnowledgeArticle per parsed section."""
        from django.utils import timezone

        result = IndexResult()

        # Document-level intro article (the __doc__ section)
        intro_ref = f"{source_type}:{doc.doc_slug}:__doc__"
        intro_defaults = {
            'page_title': parsed.title,
            'url': '',
            'category': category,
            'language': language,
            'keywords': ' '.join([parsed.title.lower(), doc.doc_slug.replace('-', ' '), doc.tags]),
            'summary': parsed.intro_summary[:500] if parsed.intro_summary else parsed.title,
            'main_content': parsed.intro_summary,
            'published_status': 'published',
            'source_type': source_type,
            'search_weight': 2.5,  # Document-level entry gets higher base weight
            'last_modified': timezone.now(),
        }
        intro_status, _ = _upsert_article(intro_ref, intro_defaults)
        if intro_status == 'created':
            result.indexed += 1
        elif intro_status == 'updated':
            result.updated += 1
        else:
            result.skipped += 1

        # Section articles
        for section in parsed.sections:
            source_ref = f"{source_type}:{doc.doc_slug}:{section.section_slug}"
            page_title = f"{parsed.title} — {section.heading}" if section.heading else parsed.title
            defaults = {
                'page_title': page_title,
                'url': '',
                'category': category,
                'language': language,
                'keywords': section.keywords,
                'summary': section.body[:300] if section.body else section.heading,
                'main_content': section.body,
                'published_status': 'published',
                'source_type': source_type,
                'search_weight': 2.0 if section.level == 2 else 1.7,
                'last_modified': timezone.now(),
            }
            status, _ = _upsert_article(source_ref, defaults)
            if status == 'created':
                result.indexed += 1
            elif status == 'updated':
                result.updated += 1
            else:
                result.skipped += 1

        return result

    @staticmethod
    def _slugify(text: str) -> str:
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_]+', '-', text)
        return re.sub(r'-+', '-', text).strip('-')[:100] or 'document'
