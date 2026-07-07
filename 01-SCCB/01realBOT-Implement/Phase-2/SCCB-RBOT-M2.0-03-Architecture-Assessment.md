<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Antigravity (Authorized Execution Agent)
Reviewed By: Mindra (Final Review Authority)
Product Approval: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-05 14:20:00
Last Updated By: Antigravity
Last Updated On: 2026-07-05 14:20:00
Searchtag: SCCB-RBOT-M2.0-03-Architecture-Assessment
-->

# SCCB-RBOT-M2.0 - Architecture Assessment Report
## Boundary Enforcement and Thin-Client Structural Audit

---

## 1. Context & Architectural Mandate

The primary architectural constraint for the realBOT integration is that **Propertism must remain a thin client**. The `realBOT` platform serves as a centralized, multi-tenant AI engine responsible for prompt execution, conversation persistence, and knowledge indexing. All logic, database models, credentials, and engines related to these systems belong exclusively to `realBOT`.

---

## 2. Boundary Verification Matrix

The target division of concerns is defined below:

| Feature Layer | Primary Owner | Propertism Stake / Responsibility | realBOT Stake / Responsibility | Boundary Status |
| :--- | :--- | :--- | :--- | :--- |
| **AI Provider Connections** | **realBOT** | None (No credentials or endpoints stored locally) | Configures provider APIs, keys, and endpoints | ❌ Current Violation |
| **Prompt Engineering** | **realBOT** | None (No system prompts or formatting instructions) | Formulates context-enriched system prompts | ❌ Current Violation |
| **Conversation Storage** | **realBOT** | None (No chat logs or session rows stored locally) | Persists sessions, logs messages, tracks feedback | ❌ Current Violation |
| **Knowledge Engine** | **realBOT** | Feeds web static assets/blog text as context | Indexes sources, chunks, runs vector/semantic RAG | ❌ Current Violation |
| **Authentication Gateway** | **Propertism** | Handles user log-in and generates tokens | Validates client tokens, issues scoped realBOT JWTs | ⬜ Pending |
| **Property Context** | **Propertism** | Serializes active property specs and search terms | Absorbs context metadata to guide answers | ⬜ Pending |
| **Widget Frame** | **Propertism** | Embeds iframe and triggers visibilities | Serves the layout and loads dynamic styling | ❌ Current Violation |
| **Branding Configuration** | **Propertism** | Configures colors and assets locally | Applies CSS variables to white-label the widget | ⬜ Pending |

---

## 3. Gap Analysis (Current vs. Target)

The discovery audit reveals a total mismatch between the current implementation and the mandated target boundaries:

```
=== CURRENT COUPLING ===
┌────────────────────────────────────────────────────────┐
│ Propertism Monolith                                    │
│  - chat.RealBotSession & chat.RealBotMessage Models     │
│  - chat.ai_service (Direct DeepSeek API integration)   │
│  - Hardcoded prompts, fallback blocks, & templates     │
└────────────────────────────────────────────────────────┘

=== TARGET THIN-CLIENT ===
┌───────────────────────┐            ┌───────────────────────┐
│ Propertism (Thin Client)│            │ realBOT Platform      │
│  - Auth Gateway       │── REST ───▶│  - AI Provider Engine │
│  - Context Serializer │◀── JWT ───│  - Prompt Templates   │
│  - Widget Iframe      │            │  - Conversation DB    │
└───────────────────────┘            └───────────────────────┘
```

### Deviations Identified:
1.  **AI Engine Duplication:** Propertism executes direct REST completions with DeepSeek inside `chat/ai_service.py` using local credentials.
2.  **Schema Overlap:** Propertism maintains its own tables (`RealBotSession`, `RealBotMessage`) inside its relational database.
3.  **Local Prompts:** The system prompt and formatting instructions are stored in Python classes on the Propertism backend.
4.  **Static UI Markup:** base.html has detailed inline HTML templates for rendering property cards, comparison tables, and text messages which are duplicate copies of what the realBOT widget provides.

---

## 4. Thin Client Validation Compliance Checklist

Before moving to the next integration milestones, the following validation checks must be satisfied by the design:

- [ ] **Zero Local Credentials:** All `DEEPSEEK_*` variables must be removed from Propertism settings.
- [ ] **No Conversation Tables:** The `chat.RealBotSession` and `chat.RealBotMessage` models must be deprecated and purged from Propertism's database.
- [ ] **Proxy Communication:** The Propertism backend must not write any LLM prompts; it must only proxy messages directly through REST connections to the realBOT API gateway.
- [ ] **Widget Embedding:** The user-facing chat panel must be rendered via an embeddable iframe served directly by realBOT.
- [ ] **API-Driven Styling:** The widget must pull style sheets and branding rules from realBOT configuration APIs, avoiding hardcoded classes inside Propertism.

---
*Maintained by Antigravity | 2026-07-05 14:20:10 IST*
