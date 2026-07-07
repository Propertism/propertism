<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-06 19:30:00
Last Updated By: Antigravity
Last Updated On: 2026-07-06 19:30:00
Searchtag: SCCB-PROP-RBOT-M2-PHASE-1
-->

# SCCB-PROP-RBOT-M2 &ndash; realBOT Integration with Propertism (Phase 1)

## Objective
Integrate realBOT into Propertism as a production-ready, rule-based digital advisory assistant capable of answering Propertism-specific queries, guiding customers through services, creating enquiries, and seamlessly connecting visitors to business channels.

---

## Roadmap Milestones & Details

### M2.1 &ndash; Integration Foundation
- Embed realBOT into Propertism.
- Initialize bot with page context.
- Session lifecycle.
- Configuration framework.
- Feature toggles.
- Health monitoring.

### M2.2 &ndash; Knowledge Base (Website Content)
*   **Primary knowledge source:** All published Propertism content.
*   **Examples:**
    - Services
    - Home page
    - About
    - Resource Hub
    - FAQ
    - Blogs
    - NRI pages
    - Property pages
    - Contact information
    - Footer pages
*   *Note:* The bot should answer only from published content. No generative responses.

### M2.3 &ndash; Internal Knowledge Documents
*   **Additional controlled knowledge:**
    - Terms & Conditions
    - Service Fee Structure
    - Future policy documents
    - Company guidelines
*   **Supported formats:** Markdown, HTML, Plain text.
*   *Note:* These become searchable knowledge sources.

### M2.4 &ndash; Rule Engine
*   **Intent-based routing examples:**
    - Property enquiry
    - Rental enquiry
    - NRI assistance
    - Legal services
    - Plot services
    - Buying
    - Selling
    - Investment
    - Contact
    - Navigation
    - Maps
    - Useful links
*   *Note:* The rule engine determines the response.

### M2.5 &ndash; Service Coverage
Implement dedicated advisory modules for:
- Buy Property
- Sell Property
- Rental Income Management
- Land / Plot Services
- Property Discovery
- NRI Advisory
- Resource Hub
- Useful Links
- Patta / Chitta
- Encumbrance Search
- GCC Property Tax
*   *Note:* Each module returns deterministic responses with CTAs.

### M2.6 &ndash; Inquiry Creation
- Enable conversational enquiry creation.
- **Capture parameters:** Name, Mobile, Email, Country, Requirement, Service required, Property preference, Remarks.
- Validate input.
- Create General Inquiry automatically.
- Store using existing Inquiry module.
- *Note:* No duplicate business logic.

### M2.7 &ndash; Quick Inquiry Integration
- Leverage existing Quick Inquiry definitions.
- **Suggested chips:** Luxury Villas, Apartments, Plots, Rental, Investment, NRI, Buying, Selling, Schedule Visit, Talk to Advisor.

### M2.8 &ndash; Navigation Actions
*   **Support actionable commands:**
    - Open Contact
    - Open Resource Hub
    - Open FAQ
    - View Property
    - View Services
    - Useful Links
    - Open WhatsApp
    - Call Office
    - Open LinkedIn
    - Open Google Maps
    - Navigate to Chennai Office

### M2.9 &ndash; Rich Response Cards
*   **Supported elements:**
    - Property cards
    - Service cards
    - CTA cards
    - Link cards
    - Contact cards
    - Office card
    - Advisor card

### M2.10 &ndash; Conversation Management
*   **Maintain state parameters:**
    - Conversation ID
    - Session
    - History
    - Context
    - Multi-turn conversations
    - Greeting, Goodbye, Fallback handler

### M2.11 &ndash; Search Framework
*   **Search targets:** Website pages, Knowledge documents, Services, Resource Hub, Useful links, Internal documents.
*   *Note:* Return ranked deterministic matches.

### M2.12 &ndash; Admin Knowledge Management
Allow administrators to manage:
- Website indexing
- Knowledge documents
- Terms & Fee documents
- Response templates
- Rule definitions
- Suggestion chips

### M2.13 &ndash; Analytics
*   **Capture telemetry indicators:**
    - Most asked questions
    - Unknown questions
    - Conversation count
    - Inquiry conversion
    - Popular services
    - Session duration
    - Knowledge misses

### M2.14 &ndash; Testing
Verify:
- Knowledge validation
- Intent routing
- Inquiry generation
- Navigation actions
- Rule engine triggers
- Conversation flow
- Regression & UI testing

---

## Deferred to Phase 2
The following should remain intentionally out of scope for this rollout:
- DeepSeek integration
- GPT integration
- LLM providers
- RAG / vector database
- Embeddings
- Semantic search
- AI-generated responses
- Agentic workflows
- Multi-model routing
- Autonomous reasoning

---

## Why this revision?
This aligns perfectly with your current rollout objective. Phase 1 is about making realBOT the definitive digital advisor for Propertism, using trusted content and deterministic logic. Every response is explainable, consistent, and under your control.

The architecture we originally designed&mdash;with provider abstraction, AI service layers, and future LLM integration&mdash;remains valuable, but it becomes Phase 2. When you're ready, the rule engine and knowledge framework can evolve into a hybrid model where deterministic rules handle business-critical workflows while AI augments broader advisory capabilities. This staged approach minimizes risk while delivering immediate business value.
