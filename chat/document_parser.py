"""
chat/document_parser.py — M2.3 Internal Knowledge Repository
Modular document parsing framework. Phase 1 supports Markdown (.md).
New format parsers (HTML, PDF, DOCX) implement BaseDocumentParser without
touching indexer or retrieval logic.
"""
import hashlib
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

logger = logging.getLogger('chat')


# ── Data classes ──────────────────────────────────────────────────────────────

@dataclass
class ParsedSection:
    """Represents a single extracted section from a document."""
    heading: str           # Section heading text (empty string for document intro)
    body: str              # Section body text
    level: int             # Heading level (0=intro, 1=#, 2=##, 3=###)
    section_slug: str      # URL-safe slug derived from heading
    keywords: str          # Extracted keyword string for search index


@dataclass
class ParsedDocument:
    """Represents a fully parsed document with all its sections."""
    title: str
    doc_slug: str
    intro_summary: str     # Text before the first heading (document-level summary)
    sections: List[ParsedSection] = field(default_factory=list)
    content_hash: str = ""

    @property
    def total_sections(self) -> int:
        return len(self.sections)


# ── Base parser ABC ───────────────────────────────────────────────────────────

class BaseDocumentParser(ABC):
    """
    Abstract base for all document format parsers.
    Implement parse() to support a new format.
    """

    @abstractmethod
    def parse(self, file_path: Path) -> ParsedDocument:
        """Parse file at file_path and return a ParsedDocument."""
        ...

    @staticmethod
    def compute_hash(file_path: Path) -> str:
        """Compute SHA-256 of a file's content for change detection."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert heading text to a URL-safe slug."""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_]+', '-', text)
        text = re.sub(r'-+', '-', text).strip('-')
        return text[:100] or 'section'

    @staticmethod
    def _extract_keywords(heading: str, body: str) -> str:
        """Extract meaningful keyword terms from heading and body."""
        combined = f"{heading} {body}".lower()
        # Remove punctuation
        combined = re.sub(r'[^\w\s]', ' ', combined)
        words = combined.split()
        # Deduplicate while preserving order; filter very short tokens
        seen = {}
        keywords = []
        for word in words:
            if len(word) > 2 and word not in seen:
                seen[word] = True
                keywords.append(word)
        return ' '.join(keywords[:80])  # cap at 80 unique terms


# ── Markdown Parser ───────────────────────────────────────────────────────────

class MarkdownSectionParser(BaseDocumentParser):
    """
    Parses a Markdown (.md) file into a ParsedDocument.
    Splitting strategy:
    - The first H1 (#) is the document title.
    - Text before the first H2 (##) is the document intro/summary.
    - Each H2 (##) and H3 (###) heading creates an independent ParsedSection.
    - H3 sections nested under H2 inherit the H2 context in their keywords.
    """

    def parse(self, file_path: Path) -> ParsedDocument:
        content = file_path.read_text(encoding='utf-8')
        content_hash = self.compute_hash(file_path)

        lines = content.splitlines()
        title = ""
        doc_slug = self._slugify(file_path.stem)

        # Extract title from first H1
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('# ') and not stripped.startswith('## '):
                title = stripped.lstrip('# ').strip()
                break
        if not title:
            title = file_path.stem.replace('-', ' ').title()

        sections: List[ParsedSection] = []
        intro_lines: List[str] = []
        current_heading = ""
        current_level = 0
        current_body_lines: List[str] = []
        in_body = False

        def flush_section():
            nonlocal current_heading, current_level, current_body_lines, in_body
            if current_heading or current_body_lines:
                body = '\n'.join(current_body_lines).strip()
                slug = self._slugify(current_heading) if current_heading else '__intro__'
                keywords = self._extract_keywords(current_heading, body)
                sections.append(ParsedSection(
                    heading=current_heading,
                    body=body,
                    level=current_level,
                    section_slug=slug,
                    keywords=keywords,
                ))
            current_heading = ""
            current_level = 0
            current_body_lines = []
            in_body = False

        for line in lines:
            stripped = line.strip()

            # Skip H1 title line
            if stripped.startswith('# ') and not stripped.startswith('## '):
                continue

            # H2 heading
            if stripped.startswith('## '):
                if in_body or current_heading:
                    flush_section()
                else:
                    # Capture intro (pre-first-H2 body)
                    intro_lines = list(current_body_lines)
                    current_body_lines = []
                current_heading = stripped.lstrip('# ').strip()
                current_level = 2
                in_body = True
                continue

            # H3 heading — treated as a sub-section
            if stripped.startswith('### '):
                if in_body and current_heading:
                    flush_section()
                current_heading = stripped.lstrip('# ').strip()
                current_level = 3
                in_body = True
                continue

            # Body text
            if in_body:
                current_body_lines.append(line)
            else:
                # Pre-first-heading intro lines
                if stripped and not stripped.startswith('# '):
                    current_body_lines.append(line)

        # Flush last section
        if in_body or current_body_lines:
            if not in_body:
                intro_lines = list(current_body_lines)
            else:
                flush_section()

        intro_summary = '\n'.join(intro_lines).strip()[:500]

        logger.info(
            f"MarkdownSectionParser: '{file_path.name}' → "
            f"{len(sections)} sections, hash={content_hash[:12]}…"
        )
        return ParsedDocument(
            title=title,
            doc_slug=doc_slug,
            intro_summary=intro_summary,
            sections=sections,
            content_hash=content_hash,
        )


# ── Parser registry ───────────────────────────────────────────────────────────

_PARSER_REGISTRY = {
    '.md': MarkdownSectionParser,
}


def get_parser_for(file_path: Path) -> BaseDocumentParser:
    """
    Return the appropriate parser for the given file extension.
    Raises ValueError for unsupported formats.
    """
    suffix = file_path.suffix.lower()
    parser_cls = _PARSER_REGISTRY.get(suffix)
    if not parser_cls:
        raise ValueError(
            f"No parser registered for '{suffix}'. "
            f"Supported formats: {list(_PARSER_REGISTRY.keys())}"
        )
    return parser_cls()
