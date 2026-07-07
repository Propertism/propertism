<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-06 20:52:00
Last Updated By: Antigravity
Last Updated On: 2026-07-06 20:52:00
Searchtag: SCCB-PROP-RBOT-M2.4-RULE-ENGINE-INTENT-ROUTING-001
-->

# SCCB-PROP-RBOT-M2.4-RULE-ENGINE-INTENT-ROUTING-001

## Title
Rule Engine & Intent Routing

## Module
realBOT → Conversation Intelligence

## Phase
M2.4

## Objective
Implement a deterministic Rule Engine and Intent Routing Framework that analyzes customer queries, classifies user intent, determines the appropriate business action, and orchestrates the correct response workflow. The Rule Engine shall operate entirely through predefined business rules without using AI inference, ensuring predictable, explainable, and auditable behaviour.

---

## Scope

- Build the Rule Engine framework.
- Implement deterministic intent classification.
- Support keyword and phrase matching.
- Support weighted rule evaluation.
- Support multiple rule conditions.
- Support positive and negative keyword matching.
- Support rule priorities.
- Support rule grouping.
- Support rule categories.
- Support rule enable/disable.
- Support rule versioning.
- Support default fallback rules.
- Support rule diagnostics.
- Maintain rule execution statistics.
- Maintain intent execution logs.
- Prevent conflicting rule execution.
- Execute only the highest ranked business rule.
- Support chained rule execution where explicitly configured.
- Return deterministic confidence scores.
- Integrate with the Unified Knowledge Repository (M2.2 & M2.3).
- Invoke business actions based on resolved intent.
- Support clarification requests for ambiguous queries.
- Support graceful fallback when no matching rule exists.

---

## Supported Intents

| # | Intent |
|---|--------|
| 1 | Greeting |
| 2 | Goodbye |
| 3 | General Information |
| 4 | About Propertism |
| 5 | Contact Information |
| 6 | Office Location |
| 7 | Business Hours |
| 8 | Buy Property |
| 9 | Sell Property |
| 10 | Rental Income Management |
| 11 | Land / Plot Services |
| 12 | Property Search |
| 13 | Property Viewing |
| 14 | NRI Assist |
| 15 | Resource Hub |
| 16 | Useful Links |
| 17 | FAQ |
| 18 | Terms & Conditions |
| 19 | Service Fee Structure |
| 20 | Patta / Chitta |
| 21 | Encumbrance Search |
| 22 | GCC Property Tax |
| 23 | WhatsApp |
| 24 | Phone Call |
| 25 | Google Maps |
| 26 | LinkedIn |
| 27 | Inquiry Creation |
| 28 | Human Assistance |
| 29 | Unknown Intent |

---

## Intent Actions

- Return Knowledge Response
- Return Service Card
- Return Navigation Card
- Return Contact Card
- Launch Inquiry Workflow
- Open Website Page
- Open External Link
- Open Google Maps
- Open WhatsApp
- Initiate Phone Call
- Suggest Related Services
- Request Clarification
- Return Fallback Response

---

## Architecture Considerations

- The Rule Engine shall remain independent of the Knowledge Repository.
- Intent resolution shall occur before response generation.
- Knowledge retrieval shall be invoked only after intent resolution when required.
- Every intent shall map to one or more business actions.
- Rules shall be configuration-driven rather than hardcoded wherever practical.
- Rules shall be uniquely identifiable using immutable Rule IDs (e.g., RBR000001).
- Every rule execution shall be fully traceable and auditable.
- Intent definitions shall be reusable across future AI-assisted implementations.
- The Rule Engine shall expose a clean orchestration layer so future LLM providers can delegate business-critical decisions back to deterministic rules.
- Rule evaluation shall be modular, allowing future addition of regex, synonym dictionaries, scoring models, and hybrid routing without redesigning the architecture.
- Business actions shall be implemented through pluggable Action Handlers, ensuring new actions can be introduced without modifying the Rule Engine core.

---

## Deliverables

- Rule Engine Framework
- Intent Classification Engine
- Rule Evaluation Engine
- Intent Router
- Action Dispatcher
- Rule Registry
- Rule Configuration Framework
- Rule ID Generator
- Rule Diagnostics
- Execution Logs
- Confidence Scoring Framework
- Clarification Framework
- Fallback Handler
- Administrative Rule Management Foundation

---

## Out of Scope

- AI-generated intent classification
- Machine Learning
- LLM providers
- Semantic search
- Vector databases
- Inquiry data capture implementation
- Property recommendation engine
- Conversation memory
- Analytics dashboards
- Voice interaction

---

## Acceptance Criteria

- [ ] Deterministic intent classification operational.
- [ ] All supported business intents correctly resolved.
- [ ] Highest priority rule selected deterministically.
- [ ] Rule conflicts detected and prevented.
- [ ] Action Dispatcher invokes correct business action.
- [ ] Confidence score returned for every resolved intent.
- [ ] Clarification workflow triggered for ambiguous requests.
- [ ] Unknown intents handled gracefully.
- [ ] Rule execution fully logged.
- [ ] Rule diagnostics available.
- [ ] Rule IDs generated and traceable.
- [ ] Unified Knowledge Repository integrated without coupling.
- [ ] Framework extensible for future AI-assisted routing.
- [ ] No regression to M2.1, M2.2 or M2.3.

---

## Dependencies

**Completed:**
- M2.1 – Integration Foundation
- M2.1.1 – Integration Hardening
- M2.2 – Website Knowledge Base
- M2.3 – Internal Knowledge Repository

---

## Success Criteria
realBOT shall possess a deterministic, auditable, and extensible Rule Engine capable of consistently classifying customer intent, routing conversations to the correct business workflow, and orchestrating knowledge retrieval or business actions through a unified routing architecture, forming the decision-making core for all subsequent conversational capabilities.
