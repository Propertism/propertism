<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Viji (Product Owner & Final Decision Authority)
Reviewed By: Astra (Platform Owner-Propertism)
Created By: Antigravity
Created On: 2026-07-06 20:49:00
Last Updated By: Antigravity
Last Updated On: 2026-07-06 20:49:00
Searchtag: SCCB-M2.3-KNOWLEDGE-ENHANCEMENT-BACKLOG
-->

# M2.3 — Knowledge Repository Enhancement Backlog

> [!NOTE]
> These are non-blocking future enhancements recommended by the Product Owner during M2.3 sign-off. No item below is required for current functionality. They are candidates for M2.12 (Knowledge Administration) and M2.13 (Analytics & Insights).

---

## 1. Cross-Reference Graph

**Priority**: Medium  
**Target Milestone**: M2.12

Allow `KnowledgeArticle` records to reference one another.

**Example traversal**:
```
Terms
  └── Fee Structure
         └── Policies
```

realBOT can surface: *"This topic is also covered under..."* — deterministically, without AI.

**Implementation Note**: Add a `ManyToManyField` on `KnowledgeArticle` pointing to itself (`self`), with a `relationship_type` qualifier (`see_also`, `parent`, `child`).

---

## 2. Knowledge Collections

**Priority**: Medium  
**Target Milestone**: M2.12

Group documents into logical collections instead of relying solely on `source_type` or `category`.

**Example collections**:
- Legal Collection → Terms, Policies, Procedures
- Financial Collection → Fee Structure, NRI Remittance
- NRI Collection → NRI FAQs, NRI advisory docs

**Implementation Note**: New `KnowledgeCollection` model with a M2M relationship to `KnowledgeDocument`. No change to `KnowledgeArticle` retrieval.

---

## 3. Effective Dates

**Priority**: Medium  
**Target Milestone**: M2.12

Store temporal validity on `KnowledgeDocument`:

| Field | Type | Purpose |
|-------|------|---------|
| `effective_from` | `DateField` | Document validity start |
| `effective_to` | `DateField` (nullable) | Document validity end (null = currently active) |

**Use case**: Multiple fee structures can coexist. Retrieval engine filters to the currently active version. Historical versions remain queryable for audit.

---

## 4. Author Metadata

**Priority**: Low  
**Target Milestone**: M2.12 / M2.14

Store governance metadata on `KnowledgeDocument`:

| Field | Purpose |
|-------|---------|
| `owner` | Document owner (person / team) |
| `reviewer` | Last reviewed by |
| `approved_by` | Formal approver |
| `last_reviewed_at` | Review date |

Useful for compliance workflows and future document lifecycle management.

---

## 5. Section-Level Content Fingerprint

**Priority**: High  
**Target Milestone**: M2.12

Currently the entire document is hashed (SHA-256). Extend to hash each extracted `ParsedSection` individually.

**Benefit**: When only one section of a 30-section document changes, only that section's `KnowledgeArticle` is re-indexed. Currently all sections are re-indexed when any change is detected.

**Implementation Note**: Store `section_hash` on each `KnowledgeArticle` with `source_type != 'Website'`. Compare before upsert.

---

## 6. Knowledge Relationships

**Priority**: High  
**Target Milestone**: M2.12

Surface related articles deterministically alongside the primary answer.

**Example**:
```
Payment Terms
  → Related: Refund Policy
  → Related: Cancellation Policy
  → Related: GST
```

realBOT can suggest: *"You may also want to read..."* — deterministically.

**Implementation Note**: Extends item 1 (Cross-Reference Graph). Relationship types: `related`, `prerequisite`, `supersedes`, `clarifies`.

---

## 7. Knowledge Priority

**Priority**: Medium  
**Target Milestone**: M2.12

Extend `search_weight` into a structured `business_priority` field with four levels:

| Level | Value | Use Case |
|-------|-------|---------|
| `critical` | 4.0 | Always surfaces in top result |
| `high` | 2.5 | Primary authoritative source |
| `medium` | 1.5 | Standard content |
| `low` | 0.8 | Supplementary or archival |

Useful when two documents answer the same question but one is more authoritative than the other.

---

## 8. Knowledge Audit (Retrieval Analytics)

**Priority**: High  
**Target Milestone**: M2.13

Record retrieval metrics per `KnowledgeArticle`:

| Field | Purpose |
|-------|---------|
| `last_retrieved_at` | When was this article last served to a user |
| `retrieved_count` | Total retrieval count |
| `last_search_query` | The query that last matched this article |
| `average_rank` | Average rank position when retrieved |
| `no_match_count` | Times this was a candidate but scored 0 |

This becomes training data for M2.13 Analytics and eventual search optimization.

---

## Sign-Off Record

| Field | Detail |
|-------|--------|
| **Signed Off By** | Viji (Product Owner & Final Decision Authority) |
| **Sign-Off Date** | 2026-07-06 |
| **Overall Rating** | ⭐⭐⭐⭐⭐ (5/5) |
| **Milestone Status** | M2.1 ✅ · M2.1.1 ✅ · M2.2 ✅ · M2.3 ✅ |
| **Next Milestone** | M2.4 — Rule Engine & Intent Routing |

> *"The platform now has a robust, deterministic knowledge layer that supports both public website content and controlled internal documents through a single retrieval engine. This provides an excellent foundation for the next milestone, M2.4 – Rule Engine & Intent Routing, where the focus shifts from what the bot knows to how it decides what action to take."*
> — Viji, Product Owner
