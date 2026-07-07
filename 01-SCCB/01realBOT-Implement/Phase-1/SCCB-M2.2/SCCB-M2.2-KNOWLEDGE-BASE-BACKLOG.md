<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-06 20:18:00
Searchtag: REALBOT-KNOWLEDGE-BASE-PRODUCT-BACKLOG
-->

# realBOT Knowledge Base — Product Backlog

> These items were identified by Viji during M2.2 implementation review.
> They are non-blocking for M2.2 and have been deferred for implementation in appropriate future milestones.
> The one immediately implementable item (Knowledge ID) was implemented in M2.2 itself.

---

## Implemented Immediately

### ✅ KA-000 — Knowledge ID (implemented in M2.2)

**Status:** DONE

Every `KnowledgeArticle` now carries a stable, immutable `knowledge_id` in the format `KA000001`. Generated once on creation via a DB aggregate, never changes on re-index. Surfaced in search results and message metadata under `knowledge.knowledge_id`.

---

## Product Backlog — Deferred Items

---

### KB-001 — Knowledge Version

**Priority:** Medium
**Target Milestone:** M2.5+

**Description:**
Each `KnowledgeArticle` should carry an integer `knowledge_version` counter (default: `1`) that increments on every content update. This allows audit logs and conversation history to record `"answered from KA000042 v7"` rather than just the current state.

**Implementation Notes:**
- Add `knowledge_version = IntegerField(default=1)` to model.
- Increment in `_upsert_article()` on `status='updated'`.
- Include `knowledge_version` in `SearchMatch` and response metadata.
- Migration: simple `AddField`, zero downtime.

---

### KB-002 — Knowledge Slug

**Priority:** Medium
**Target Milestone:** M2.5+

**Description:**
Store a `knowledge_slug` (e.g., `nri-property-management`) alongside the URL. URLs can change; slugs are generally stable and provide a cleaner citation surface for search analytics and admin screens.

**Implementation Notes:**
- Add `knowledge_slug = SlugField(max_length=200, blank=True)` to model.
- Auto-derive from `page_title` if not provided (using `slugify()`).
- Indexers pass `knowledge_slug` explicitly from `Service.slug`, `BlogPost.slug`, `Property.slug` where available.
- Migration: simple `AddField`.

---

### KB-003 — Synonym Engine

**Priority:** High
**Target Milestone:** M2.4 (Rule Engine) or dedicated KB Enhancement milestone

**Description:**
A deterministic synonym mapping table that expands query terms before keyword scoring. Example: `villa → villa, independent house, house, home`. Strictly deterministic — no AI.

**Implementation Notes:**
- New model: `KnowledgeSynonymGroup(primary_term, synonyms_csv)`.
- `KnowledgeSearchEngine.search()` expands `query_terms` through synonym table before scoring.
- Admin-editable via Django admin with no code changes.
- Will dramatically improve recall for colloquial queries.

---

### KB-004 — Search Analytics Log

**Priority:** High
**Target Milestone:** Precursor to M2.13

**Description:**
Log every search event to a `KnowledgeSearchLog` table. This becomes the training corpus for M2.13 (Conversation Intelligence).

**Fields to log:**
- `query` — original user query
- `matched_knowledge_id` — KA ID of best match (or null)
- `relevance_score` — score of best match
- `result_rank` — number of results returned
- `no_match` — boolean flag
- `session_id` — links to `RealBotSession`
- `searched_at` — timestamp

**Implementation Notes:**
- New model `KnowledgeSearchLog`.
- Log in `KnowledgeSearchEngine.search()` after scoring, non-blocking (fire-and-forget).
- Admin dashboard aggregation: top queries, top no-match queries.

---

### KB-005 — Admin Weight Override

**Priority:** Low
**Target Milestone:** M2.5+ / Admin milestone

**Description:**
Allow admin users to pin articles, increase or decrease `search_weight` directly from Django admin without code changes.

**Implementation Notes:**
- `search_weight` field is already on the model.
- Expose as editable in `KnowledgeArticleAdmin` with `list_editable = ['search_weight']`.
- Add a `is_pinned = BooleanField(default=False)` field that forces `search_weight=10.0`.
- No code changes to search engine needed — weight is already used in scoring.

---

### KB-006 — Extended Knowledge Status

**Priority:** Low
**Target Milestone:** M2.5+

**Description:**
Extend `published_status` from `[published, draft, hidden]` to:

| Status | Description |
|--------|-------------|
| `published` | Active, searchable |
| `archived` | Retired content, read-only for history |
| `deprecated` | Will be removed; replaced by newer article |
| `internal` | Visible only to admin/staff queries |
| `hidden` | Excluded from all searches |
| `draft` | Not yet published |

**Implementation Notes:**
- Update `PUBLISHED_STATUS_CHOICES` on `KnowledgeArticle`.
- Update `KnowledgeSearchEngine` filter to include `internal` only for staff queries.
- Migration: no data loss, existing `published/draft/hidden` values remain valid.

---

### KB-007 — Multilingual Knowledge Groups

**Priority:** Medium
**Target Milestone:** M2.x (Multilingual) — aligned with content i18n rollout

**Description:**
Group multiple language variants of the same logical article under a single `KnowledgeGroup`. Currently `language` is stored per-article; this item promotes it to a relationship.

**Implementation Notes:**
- New model: `KnowledgeGroup(group_id, primary_title, created_at)`.
- `KnowledgeArticle` gets optional `ForeignKey(KnowledgeGroup)`.
- `KnowledgeSearchEngine` accepts `language` parameter and filters within the group.
- Existing `en` articles automatically form singleton groups on migration.

---

### KB-008 — Retrieval Confidence Score

**Priority:** High
**Target Milestone:** M2.10 (Clarifying Questions)

**Description:**
Return a normalized `confidence_score` (0–100%) alongside each `SearchMatch`. M2.10 can use this to decide whether to answer directly or ask a clarifying question.

**Threshold design (proposed):**
- ≥ 80% → Return answer directly.
- 55–79% → Return answer with a note ("Based on my best match…").
- < 55% → Ask a clarifying question instead.

**Implementation Notes:**
- Normalize raw relevance score relative to the theoretical maximum for the query.
- `confidence_score = min(100, int((score / max_possible_score) * 100))`.
- Add to `SearchMatch.confidence_score` and surface in `as_dict()`.
- No AI involved — purely deterministic math.

---

## Backlog Summary

| ID | Item | Priority | Target Milestone |
|----|------|----------|-----------------|
| KB-001 | Knowledge Version | Medium | M2.5+ |
| KB-002 | Knowledge Slug | Medium | M2.5+ |
| KB-003 | Synonym Engine | **High** | M2.4 |
| KB-004 | Search Analytics Log | **High** | Pre-M2.13 |
| KB-005 | Admin Weight Override | Low | M2.5+ Admin |
| KB-006 | Extended Knowledge Status | Low | M2.5+ |
| KB-007 | Multilingual Knowledge Groups | Medium | Multilingual milestone |
| KB-008 | Retrieval Confidence Score | **High** | M2.10 |
