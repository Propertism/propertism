# SCCB-PROP-RBOT-M2.7-QUICK-INQUIRY-SUGGESTION-FRAMEWORK-001

## Title
Quick Inquiry & Intelligent Suggestion Framework

## Module
realBOT → Customer Engagement

## Phase
M2.7

## Objective
Implement a configurable Quick Inquiry and Intelligent Suggestion Framework that enables realBOT to proactively guide customers through contextual suggestion chips, quick actions, service shortcuts, and conversation recommendations. The framework shall reduce customer effort, accelerate conversation flow, improve inquiry conversion, and maintain a consistent conversational experience throughout the Propertism platform.

## Scope
* Implement the Quick Inquiry Framework.
* Implement Intelligent Suggestion Engine.
* Support context-aware suggestion chips.
* Support dynamic quick actions.
* Support conversation shortcuts.
* Support service-specific suggestion sets.
* Support page-specific suggestion sets.
* Support inquiry-stage suggestions.
* Support conversation-state suggestions.
* Support Rule Engine integration.
* Support Service Profile integration.
* Support Knowledge Repository integration.
* Support configurable suggestion priorities.
* Support suggestion grouping.
* Support suggestion visibility rules.
* Support multilingual-ready suggestion definitions.
* Support future personalization.
* Support future recommendation engines.
* Maintain suggestion analytics.
* Maintain suggestion diagnostics.

## Suggestion Categories
* Welcome Suggestions
* Service Suggestions
* Property Suggestions
* Inquiry Suggestions
* Knowledge Suggestions
* Resource Hub Suggestions
* Government Service Suggestions
* Contact Suggestions
* Navigation Suggestions
* Follow-up Suggestions
* Conversation Recovery Suggestions
* Completion Suggestions

## Quick Inquiry Suggestions
Support predefined customer journeys for:
* Buy Property
* Sell Property
* Rental Income Management
* Land / Plot Services
* Property Search
* Property Viewing
* NRI Assist
* Patta / Chitta
* Encumbrance Search
* GCC Property Tax
* General Advisory
* Contact Advisor

## Suggestion Behaviour
The framework shall support:
* Initial welcome suggestions.
* Context-aware suggestions based on active intent.
* Suggestions based on active Service Profile.
* Suggestions based on conversation progress.
* Suggestions after successful knowledge responses.
* Suggestions after inquiry completion.
* Suggestions after conversation inactivity.
* Suggestions after clarification requests.
* Suggestions during incomplete inquiry sessions.
* Suggestions after business action completion.

## Suggestion Definition
Each suggestion shall define:
* Suggestion ID (e.g. SUG000001)
* Display Text
* Category
* Parent Context
* Trigger Condition
* Business Intent
* Target Action
* Display Priority
* Icon
* Display Order
* Visibility Rules
* Status
* Version

## Architecture Considerations
* Suggestion definitions shall be configuration-driven and independent of business logic.
* Every suggestion shall have an immutable Suggestion ID (e.g., SUG000001).
* Suggestion rendering shall remain independent of the Rule Engine.
* The Rule Engine shall request suggestions from the Suggestion Engine based on resolved intent and conversation state.
* Suggestion generation shall combine multiple contexts including:
  - Current Intent
  - Active Service Profile
  - Conversation State
  - Inquiry Session State
  - Current Website Page
  - Knowledge Response Context
* Multiple suggestion providers shall contribute recommendations, which shall be merged, ranked and de-duplicated before presentation.
* Suggestion Providers shall follow a plug-in architecture, enabling future providers without modifying the Suggestion Engine.
* The framework shall support future user-profile personalization while maintaining deterministic behaviour during Phase 1.
* Suggestions shall never interrupt mandatory business workflows or validation sequences.
* The engine shall expose extension points for future AI-assisted recommendations without changing the underlying framework.

## Suggestion Providers
* Welcome Provider
* Rule Engine Provider
* Service Provider
* Knowledge Provider
* Inquiry Provider
* Navigation Provider
* Contact Provider
* Conversation Recovery Provider
* Completion Provider

## Deliverables
* Suggestion Engine
* Suggestion Registry
* Suggestion Provider Framework
* Suggestion Ranking Engine
* Suggestion Deduplication Engine
* Quick Inquiry Registry
* Suggestion Context Resolver
* Suggestion Diagnostics
* Suggestion Analytics
* Administrative Suggestion Registry Foundation

## Out of Scope
* AI-generated suggestions
* Personalized recommendations
* Behavioural learning
* Marketing campaigns
* CRM recommendations
* Push notifications
* Email recommendations
* WhatsApp recommendations
* Predictive analytics

## Acceptance Criteria
* Suggestion Engine operational.
* Immutable Suggestion IDs generated.
* Context-aware suggestions operational.
* Dynamic suggestion chips displayed.
* Quick Inquiry journeys operational.
* Rule Engine integration completed.
* Service Profile integration completed.
* Knowledge Repository integration completed.
* Inquiry conversation integration completed.
* Suggestion providers contribute independently.
* Suggestion ranking and de-duplication operational.
* Diagnostics available.
* Analytics available.
* No regression to M2.1 through M2.6.
