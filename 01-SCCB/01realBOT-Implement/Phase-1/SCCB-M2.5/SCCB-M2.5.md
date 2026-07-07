<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-06 21:18:00
Last Updated By: Antigravity
Last Updated On: 2026-07-06 21:18:00
Searchtag: SCCB-PROP-RBOT-M2.5-SERVICE-COVERAGE-FRAMEWORK-001
-->

# SCCB-PROP-RBOT-M2.5-SERVICE-COVERAGE-FRAMEWORK-001

## Title
Service Coverage Framework

## Module
realBOT → Business Services

## Phase
M2.5

## Objective
Implement the Service Coverage Framework to enable realBOT to provide structured, service-specific advisory experiences across all Propertism business offerings. Each supported service shall expose a standardized conversation model, business information, customer guidance, eligibility criteria, call-to-actions, and escalation pathways while remaining fully integrated with the Rule Engine and Unified Knowledge Repository.

---

## Scope

- Implement the Service Framework.
- Standardize all service definitions.
- Introduce reusable Service Profiles.
- Support structured service metadata.
- Configure service-specific conversation flows.
- Support contextual guidance for each service.
- Support eligibility information where applicable.
- Support required customer information.
- Support recommended next actions.
- Support service-specific CTAs.
- Support related service recommendations.
- Support service escalation paths.
- Support service contact channels.
- Support multilingual-ready service definitions.
- Maintain service statistics.
- Maintain service diagnostics.
- Integrate with Rule Engine.
- Integrate with Knowledge Repository.
- Integrate with Navigation Services.
- Support future AI-assisted advisory without architectural changes.

---

## Service Coverage

- Buy Property
- Sell Property
- Rental Income Management
- Land / Plot Services
- Property Search
- Property Viewing
- NRI Assist
- Resource Hub
- Useful Links
- Patta / Chitta Extract
- Encumbrance Search
- GCC Property Tax
- General Advisory
- Contact Advisory

---

## Service Profile Structure

Every service shall define:
- Service ID
- Service Name
- Service Category
- Short Description
- Detailed Description
- Business Objective
- Target Audience
- Eligibility
- Required Inputs
- Advisory Content
- FAQs
- Knowledge References
- Related Services
- Call-to-Actions
- Contact Channels
- Escalation Rules
- Navigation Links
- Display Priority
- Status
- Version

---

## Conversation Capabilities

Support:
- Service Introduction
- Service Overview
- Benefits
- Process Explanation
- Required Documents
- Frequently Asked Questions
- Service Limitations
- Pricing Reference
- Related Knowledge
- Contact Advisor
- Create Inquiry
- Continue Conversation
- End Conversation

---

## Architecture Considerations

- Services shall be represented as configuration-driven Service Profiles rather than hardcoded logic.
- Every Service Profile shall have an immutable Service ID (e.g., SRV000001).
- Service definitions shall remain independent of the Rule Engine.
- The Rule Engine shall resolve intent and delegate execution to the appropriate Service Profile.
- Service responses shall reuse the Unified Knowledge Repository wherever applicable.
- Service metadata shall be reusable by future web pages, APIs, mobile applications and AI providers.
- Support hierarchical service grouping to accommodate future expansion.
- Allow service-specific suggestion chips, quick actions and CTA definitions.
- Service Profiles shall support future addition of pricing models, SLA definitions, eligibility rules, and workflow orchestration without requiring schema redesign.
- The framework shall separate business knowledge from presentation, enabling multiple UI experiences to consume the same Service Profile.

---

## Deliverables

- Service Framework
- Service Profile Registry
- Service ID Generator
- Service Response Builder
- Service Conversation Templates
- Service CTA Framework
- Service Navigation Framework
- Related Service Engine
- Service Diagnostics
- Service Statistics
- Administrative Service Registry Foundation

---

## Out of Scope

- Inquiry data persistence
- CRM integration
- Property recommendation engine
- AI-generated advisory
- Workflow automation
- Lead assignment
- Appointment scheduling
- Analytics dashboards
- Voice interactions

---

## Acceptance Criteria

- [ ] All supported Propertism services represented as Service Profiles.
- [ ] Immutable Service IDs generated.
- [ ] Standardized advisory responses available.
- [ ] Service-specific CTAs operational.
- [ ] Related service recommendations available.
- [ ] Rule Engine successfully delegates to Service Profiles.
- [ ] Knowledge Repository integrated.
- [ ] Navigation services integrated.
- [ ] Configuration-driven architecture implemented.
- [ ] Diagnostics and statistics available.
- [ ] No regression to M2.1 through M2.4.

---

## Dependencies

**Completed:**
- M2.1 – Integration Foundation
- M2.1.1 – Integration Hardening
- M2.2 – Website Knowledge Base
- M2.3 – Internal Knowledge Repository
- M2.4 – Rule Engine & Intent Routing

---

## Success Criteria
realBOT shall provide a comprehensive, consistent, and extensible advisory experience across every Propertism business service through standardized Service Profiles, enabling deterministic conversations, seamless navigation, reusable business definitions, and future AI augmentation without architectural modifications.
