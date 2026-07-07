<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-06 19:58:00
Last Updated By: Antigravity
Last Updated On: 2026-07-06 19:58:00
Searchtag: SCCB-PROP-RBOT-M2.2-WEBSITE-KNOWLEDGE-BASE-001
-->

# SCCB-PROP-RBOT-M2.2-WEBSITE-KNOWLEDGE-BASE-001

## Title
Website Knowledge Base

## Module
realBOT → Knowledge Management

## Phase
M2.2

## Objective
Establish the Website Knowledge Base as the primary and authoritative source of information for realBOT by indexing all published Propertism website content. The bot shall answer user queries deterministically using only approved and published website content, ensuring accurate, consistent, and explainable responses without AI-generated or inferred information.

---

## Scope

- Discover and index all published website pages.
- Build the Website Knowledge Repository.
- Extract page title, URL, metadata and main content.
- Preserve page hierarchy and navigation relationships.
- Support multilingual content architecture.
- Index service pages.
- Index About, Contact and Footer pages.
- Index Resource Hub articles.
- Index FAQs.
- Index Useful Links.
- Index NRI content.
- Index Property service information.
- Ignore unpublished, draft or hidden pages.
- Maintain searchable content index.
- Support keyword-based deterministic retrieval.
- Rank responses using relevance scoring.
- Return source page references for every answer.
- Detect duplicate indexed pages.
- Re-index updated pages.
- Support manual and scheduled indexing.
- Maintain indexing statistics.
- Record indexing logs and diagnostics.

---

## Knowledge Sources

- Home
- About Us
- Services
- Property Pages
- Resource Hub
- FAQ
- Contact
- Footer Pages
- Useful Links
- NRI Services
- Published Landing Pages

---

## Out of Scope

- Terms & Conditions documents
- Fee Structure documents
- Markdown document ingestion
- AI/LLM responses
- Semantic search
- Vector databases
- Embeddings
- Inquiry creation
- Conversation intelligence
- Rule Engine
- External websites

---

## Deliverables

- Website Content Indexer
- Knowledge Repository
- Search Index
- Content Extraction Engine
- Re-index Framework
- Source Reference Framework
- Index Statistics
- Index Diagnostics
- Administrative Re-index Service

---

## Architectural Design Note
> Every indexed page shall be treated as a **"Knowledge Article"** with the following unified record structure:
>
> | Field | Description |
> |-------|-------------|
> | `knowledge_id` | Unique article identifier |
> | `page_title` | Title of the page |
> | `url` | Full canonical URL |
> | `category` | Service, FAQ, Blog, NRI, Contact, etc. |
> | `language` | Language code (e.g., `en`, `ta`) |
> | `keywords` | Extracted keyword list |
> | `summary` | Short descriptive summary |
> | `main_content` | Full extracted body content |
> | `last_modified` | Last modification timestamp |
> | `published_status` | Published / Draft / Hidden |
> | `search_weight` | Relevance scoring weight |
> | `source_type` | `Website` (M2.2), `Markdown`/`Policy` (M2.3+) |
>
> This abstraction ensures M2.3 (Internal Documents) reuses the exact same retrieval engine with only `source_type` differentiating record origins — making the knowledge architecture clean and extensible.

---

## Acceptance Criteria

- [ ] All published website pages successfully indexed.
- [ ] Hidden and unpublished content excluded.
- [ ] Deterministic keyword retrieval operational.
- [ ] Source page references returned with every response.
- [ ] Duplicate content detection operational.
- [ ] Incremental re-index supported.
- [ ] Index statistics available.
- [ ] Structured diagnostics available.
- [ ] Modular architecture ready for M2.3 knowledge expansion.
- [ ] No AI-generated responses.

---

## Dependencies

**Completed:**
- M2.1 &ndash; Integration Foundation
- M2.1.1 &ndash; Integration Foundation Hardening

---

## Success Criteria
realBOT shall possess a complete, searchable, deterministic knowledge repository built exclusively from published Propertism website content, establishing the authoritative knowledge source for customer interactions while providing a scalable foundation for future document repositories introduced in subsequent milestones.
