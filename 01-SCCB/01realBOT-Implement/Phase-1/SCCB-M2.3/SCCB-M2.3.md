<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-06 20:22:00
Last Updated By: Antigravity
Last Updated On: 2026-07-06 20:22:00
Searchtag: SCCB-PROP-RBOT-M2.3-INTERNAL-KNOWLEDGE-REPOSITORY-001
-->

# SCCB-PROP-RBOT-M2.3-INTERNAL-KNOWLEDGE-REPOSITORY-001

## Title
Internal Knowledge Repository

## Module
realBOT → Knowledge Management

## Phase
M2.3

## Objective
Extend the realBOT Knowledge Repository to incorporate controlled internal business documents as authoritative knowledge sources. The repository shall ingest, index, version, and retrieve approved internal documents such as Terms & Conditions, Service Fee Structure, Policies, Procedures, FAQs, and future business documentation while maintaining deterministic, explainable, and source-referenced responses.

---

## Scope

- Extend the existing Knowledge Repository introduced in M2.2.
- Reuse the existing KnowledgeArticle architecture without schema redesign.
- Support ingestion of approved Markdown documents.
- Design the ingestion framework to be extensible for future HTML, PDF and DOCX support.
- Index document title, headings, sections and content.
- Preserve document hierarchy and section relationships.
- Generate immutable Knowledge IDs for every document section.
- Maintain document version history.
- Support document metadata.
- Support document categorization.
- Support document tagging.
- Support document language.
- Maintain document publication status.
- Support document activation and deactivation.
- Detect duplicate document ingestion.
- Detect modified documents and perform incremental re-indexing.
- Maintain document source references.
- Record indexing diagnostics.
- Maintain repository statistics.
- Support deterministic keyword retrieval across Website and Internal Knowledge sources.
- Merge retrieval results while preserving source priority.
- Return document name and section reference with every response.
- Ensure only approved and published documents are searchable.

---

## Knowledge Sources

- Terms & Conditions
- Service Fee Structure
- Company Policies
- Operating Procedures
- Frequently Asked Questions
- Advisory Documents
- Customer Information Documents
- Future Markdown Knowledge Documents

---

## Supported Formats (Phase 1)

- Markdown (.md)

## Future Ready Formats

- HTML
- PDF
- DOCX
- TXT
- JSON Knowledge Packs

---

## Architecture Considerations

- Continue using the unified KnowledgeArticle model introduced in M2.2.
- Every ingested document section shall become an independent Knowledge Article.
- Introduce immutable Knowledge IDs (e.g., KA000001).
- Maintain Source Type values such as:
  - Website
  - Markdown
  - Policy
  - Terms
  - FeeStructure
  - FAQ
- Preserve parent-child relationships between documents and sections.
- Store document metadata separately from searchable content.
- Retrieval shall always operate against the unified Knowledge Repository abstraction rather than individual source types.
- Support weighted retrieval while prioritizing exact section matches.
- The ingestion pipeline shall be modular, enabling new document parsers without modifying retrieval logic.

---

## Deliverables

- Internal Document Ingestion Engine
- Markdown Parser
- Knowledge Document Indexer
- Section Extraction Engine
- Document Version Manager
- Knowledge ID Generator
- Repository Statistics
- Index Diagnostics
- Incremental Re-index Framework
- Unified Retrieval Integration
- Administrative Re-index Service

---

## Out of Scope

- AI-generated answers
- LLM providers
- Semantic search
- Embeddings
- Vector databases
- Inquiry creation
- Conversation intelligence
- Rule engine enhancements
- External document repositories
- OCR processing

---

## Acceptance Criteria

- [ ] Markdown documents successfully ingested.
- [ ] Every document section indexed as a Knowledge Article.
- [ ] Immutable Knowledge IDs generated.
- [ ] Document versioning operational.
- [ ] Duplicate detection operational.
- [ ] Incremental re-index operational.
- [ ] Website and Internal Knowledge searched through a unified retrieval engine.
- [ ] Responses include document and section references.
- [ ] Repository statistics available.
- [ ] Structured diagnostics available.
- [ ] No regression to M2.2 Website Knowledge Base.
- [ ] Architecture remains extensible for future document formats.

---

## Dependencies

**Completed:**
- M2.1 – Integration Foundation
- M2.2 – Website Knowledge Base

---

## Success Criteria
realBOT shall possess a unified enterprise Knowledge Repository capable of serving deterministic, explainable responses from both published website content and approved internal business documents through a single retrieval framework, establishing the complete knowledge foundation for Phase 1 rollout without introducing AI-generated responses.
