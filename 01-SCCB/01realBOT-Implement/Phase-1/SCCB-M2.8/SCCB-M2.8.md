# SCCB-PROP-RBOT-M2.8-NAVIGATION-ACTION-SERVICES-001

## Title
Navigation & Action Services

## Module
realBOT → Navigation & External Actions

## Phase
M2.8

## Objective
Implement a unified Navigation and Action Services Framework enabling realBOT to execute deterministic business actions, website navigation, communication channels, government services, and external integrations through a centralized Action Registry. The framework shall provide customers with seamless transitions from conversations to business actions while maintaining security, traceability, extensibility, and a consistent user experience.

## Scope
* Implement Navigation Service Framework.
* Implement Action Registry.
* Implement Action Dispatcher.
* Support internal website navigation.
* Support external URL navigation.
* Support deep linking.
* Support contextual navigation.
* Support configurable action definitions.
* Support action validation.
* Support action confirmation where required.
* Support action diagnostics.
* Support action analytics.
* Support multilingual-ready action definitions.
* Support future mobile deep links.
* Support future application integrations.
* Support future authenticated actions.

## Supported Navigation Actions

### Internal
* Home
* About Us
* Services
* Property Listings
* Property Details
* Resource Hub
* FAQ
* Contact
* Terms & Conditions
* Privacy Policy
* Useful Links
* NRI Services

### Communication
* Call Office
* WhatsApp
* Email
* Contact Advisor
* Create Inquiry

### Location
* Open Google Maps
* Get Directions
* Navigate to Chennai Office

### Social
* LinkedIn
* Future Social Channels

### Government Services
* Patta / Chitta
* Encumbrance Search
* GCC Property Tax

### Business Actions
* Launch Inquiry
* Continue Inquiry
* Resume Inquiry
* Cancel Inquiry
* Contact Human Advisor

## Action Definition
Each Action shall define:
* Action ID (e.g. ACT000001)
* Action Name
* Action Category
* Action Type
* Display Name
* Description
* Target URL / Route
* Target Service
* Supported Parameters
* Confirmation Required
* Visibility Rules
* Security Level
* Status
* Version

## Architecture Considerations
* Every action shall be configuration-driven and registered within a centralized Action Registry.
* Every action shall have an immutable Action ID (e.g., ACT000001).
* The Rule Engine, Suggestion Engine, and Service Framework shall invoke actions exclusively through the Action Dispatcher.
* Navigation logic shall never be hardcoded inside conversation flows.
* Internal routes and external URLs shall be abstracted behind Action Definitions.
* Actions shall support parameterized execution (e.g., property ID, service ID, article ID, inquiry ID).
* The framework shall validate every action before execution.
* Security-sensitive actions shall support configurable confirmation workflows.
* Action Handlers shall follow a plug-in architecture allowing future integrations without modifying the Action Dispatcher.
* Future integrations (CRM, Calendar, Mobile Apps, Payment Gateways, Identity Providers, etc.) shall be introduced by registering new Action Handlers rather than changing existing architecture.
* The framework shall support future audit, authorization, localization, and personalization capabilities without redesign.

## Action Providers
* Internal Navigation Provider
* External URL Provider
* Contact Provider
* Communication Provider
* Government Service Provider
* Inquiry Provider
* Social Provider
* Map Provider

## Deliverables
* Action Registry
* Action Definition Repository
* Action Dispatcher
* Action Provider Framework
* Navigation Resolver
* Parameter Resolver
* Action Validation Framework
* Action Analytics
* Action Diagnostics
* Administrative Action Registry Foundation

## Out of Scope
* CRM integration
* Calendar booking
* Payment processing
* Authentication workflows
* AI-generated actions
* Mobile application implementation
* Push notifications
* Workflow automation

## Acceptance Criteria
* Action Registry operational.
* Immutable Action IDs generated.
* Internal navigation operational.
* External URL navigation operational.
* Communication actions operational.
* Government service navigation operational.
* Parameterized actions supported.
* Action validation operational.
* Confirmation workflows operational where required.
* Action providers operate independently.
* Rule Engine integration completed.
* Service Framework integration completed.
* Suggestion Framework integration completed.
* Diagnostics available.
* Analytics available.
* No regression to M2.1 through M2.7.
