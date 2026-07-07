<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Viji (Product Owner & Final Decision Authority)
Reviewed By: Astra (Platform Integration Lead)
Created By: Viji
Created On: 2026-07-07 09:28:00
Searchtag: SCCB-PROP-RBOT-M2.6-CONVERSATIONAL-INQUIRY-CREATION-001
-->

# SCCB-PROP-RBOT-M2.6-CONVERSATIONAL-INQUIRY-CREATION-001

## Title
Conversational Inquiry Creation

## Module
realBOT → Customer Engagement

## Phase
M2.6

---

## Objective

Implement a conversational inquiry framework enabling realBOT to intelligently collect customer
information through guided conversations and create General Inquiry records using Propertism's
existing Inquiry Management module. The framework shall minimise customer effort, support
progressive information capture, validate collected data, and seamlessly transition customers
from conversation to business engagement.

---

## Scope

- Implement Conversation-driven Inquiry Framework.
- Integrate with the existing General Inquiry module.
- Reuse existing business validation rules.
- Prevent duplication of inquiry business logic.
- Support progressive information collection.
- Support interrupted conversation recovery.
- Support inquiry confirmation before submission.
- Support inquiry cancellation.
- Support inquiry editing before submission.
- Support optional and mandatory fields.
- Validate customer inputs.
- Support country-aware phone validation.
- Validate email format.
- Support multilingual-ready prompts.
- Maintain inquiry conversation state.
- Support session resume.
- Maintain inquiry audit trail.
- Record inquiry creation diagnostics.
- Support configurable conversation templates.
- Support future CRM integration without architectural changes.

---

## Inquiry Data Capture

### Mandatory
- Customer Name
- Mobile Number
- Country
- Service Required
- Inquiry Message

### Optional
- Email Address
- Preferred Contact Time
- Preferred Location
- Budget
- Property Type
- Timeline
- Additional Remarks

---

## Conversation Flow

Support:
- Inquiry initiation
- Guided information collection
- Missing information prompts
- Input validation
- Context-aware follow-up questions
- Information summary
- Customer confirmation
- Inquiry submission
- Submission acknowledgement
- Conversation completion

---

## Supported Inquiry Sources

- Manual chat request
- Service Profile CTA
- Rule Engine intent
- Quick Inquiry suggestion chips
- Future website entry points

---

## Architecture Considerations

- The Inquiry Framework shall orchestrate conversations but shall not implement business persistence logic.
- Existing General Inquiry services shall remain the single source of truth for inquiry creation.
- Conversation state shall be maintained independently from inquiry persistence.
- Each inquiry conversation shall have an immutable Inquiry Session ID.
- The framework shall support pausing and resuming incomplete inquiry sessions.
- Field definitions shall be configuration-driven to accommodate future business changes.
- Validation rules shall be reusable across chatbot, website forms, mobile applications, and future APIs.
- Conversation templates shall be separated from validation logic.
- Support future attachment uploads without redesign.
- Support future authenticated users by pre-populating known customer information.
- The framework shall expose extension points for future AI-assisted conversational guidance while preserving deterministic business validation.

---

## Conversation States

- Not Started
- Collecting Information
- Awaiting Conflict Resolution *(added per Annexure A)*
- Awaiting Validation
- Awaiting Confirmation
- Submitted
- Cancelled
- Expired

---

## Deliverables

- Inquiry Conversation Engine
- Inquiry State Manager
- Inquiry Session Manager
- Field Validation Framework
- Deterministic Field Extractor *(added per Annexure A)*
- Conversation Template Framework
- Inquiry Confirmation Handler
- Existing General Inquiry Integration
- Inquiry Diagnostics
- Inquiry Audit Trail
- Administrative Conversation Configuration Foundation

---

## Out of Scope

- CRM synchronisation
- Lead assignment
- Appointment scheduling
- File uploads
- AI-generated conversations
- Automated follow-up notifications
- WhatsApp conversations
- Workflow automation
- Sales pipeline management

---

## Acceptance Criteria

- ✓ Guided conversational inquiry operational.
- ✓ Existing General Inquiry reused without duplication.
- ✓ Mandatory fields validated.
- ✓ Optional fields supported.
- ✓ Country-aware phone validation operational.
- ✓ Email validation operational.
- ✓ Inquiry confirmation implemented.
- ✓ Conversation resume supported.
- ✓ Inquiry Session IDs generated.
- ✓ Audit trail maintained.
- ✓ Diagnostics available.
- ✓ No regression to M2.1 through M2.5.

---

## Dependencies

### Completed
- M2.1 – Integration Foundation
- M2.1.1 – Integration Hardening
- M2.2 – Website Knowledge Base
- M2.3 – Internal Knowledge Repository
- M2.4 – Rule Engine & Intent Routing
- M2.5 – Service Coverage Framework

---

## ANNEXURE A — Conversation Intelligence & Progressive Information Capture

### Purpose

This annexure enhances the Conversational Inquiry Framework by defining the mandatory
behaviour for intelligent information capture, progressive inquiry completion, and
conversational efficiency. These requirements are considered part of the M2.6 implementation
and shall be treated as mandatory.

### 1. Progressive Information Capture

- The Inquiry Conversation Engine shall continuously analyse every customer message throughout the conversation.
- Customer information voluntarily provided at any stage shall be immediately identified, validated and mapped to the corresponding Inquiry Session fields.
- The engine shall progressively enrich the Inquiry Session without requiring customers to answer questions in a predefined sequence.
- Multiple business fields provided within a single customer message shall be extracted during a single processing cycle.

### 2. Smart Conversation Behaviour

The conversation engine shall:
- Never ask for information already captured.
- Ask only for missing mandatory information required to create a valid General Inquiry.
- Request optional information only when it improves customer service and shall never block inquiry submission.
- Automatically adapt the conversation based on information already known.
- Maintain a natural conversational flow rather than a rigid form-based questionnaire.

### 3. Deterministic Field Extraction

Field extraction shall remain completely deterministic.

Extraction may utilise:
- Keyword dictionaries
- Configurable phrase patterns
- Regular expressions
- Business rules
- Validation rules

Artificial Intelligence or probabilistic inference shall not be used for field extraction within M2.6.

### 4. Supported Automatic Field Detection

The framework shall support automatic identification of, but not be limited to:
- Customer Name
- Country
- Mobile Number
- Email Address
- Service Required
- Property Type
- Budget
- Preferred Location
- Timeline
- Preferred Contact Method
- Inquiry Message
- Additional Remarks

### 5. Dynamic Inquiry Session

- The Inquiry Session shall function as a continuously evolving working model.
- Each successful extraction shall immediately update the Inquiry Session.
- The Inquiry Session shall always represent the latest validated state of the conversation.

### 6. Validation Behaviour

Every extracted value shall be validated before acceptance.

When validation fails:
- The customer shall be informed politely.
- Only the invalid field shall be requested again.
- Previously validated information shall never be requested again.

### 7. Conflict Resolution

If newly supplied information conflicts with previously validated values:
- The framework shall detect the conflict.
- The customer shall be asked to confirm the correct value.
- No conflicting value shall overwrite validated data without customer confirmation.

### 8. Missing Information Strategy

- The conversation engine shall determine the minimum remaining information required to create a valid General Inquiry.
- Only those missing mandatory fields shall be requested.

### 9. Conversation Efficiency

Example:

Customer: "My name is Raj. I'm from Singapore. I want to buy a villa in Chennai. My mobile number is +65 91234567."

The Inquiry Session shall automatically populate: Name, Country, Service Required, Property Type, Mobile Number.

The next prompt shall request only the remaining mandatory information (if any).

### 10. Future Extensibility

The Conversation Engine shall expose configurable extraction rules allowing future business fields
to be introduced without redesigning the framework. The architecture shall remain compatible with
future AI-assisted conversation enhancements while preserving deterministic validation and business rules.

### 11. Additional Acceptance Criteria (Annexure A)

- ✓ Information already supplied by the customer shall never be requested again.
- ✓ Multiple inquiry fields contained within a single customer message shall be correctly extracted.
- ✓ Inquiry Sessions shall be progressively enriched throughout the conversation.
- ✓ Only missing mandatory information shall be requested.
- ✓ Invalid values shall trigger field-level validation prompts.
- ✓ Conflicting information shall require customer confirmation before updating the Inquiry Session.
- ✓ The conversation shall remain natural and adaptive rather than sequential and form-driven.

---

## Success Criteria

realBOT shall seamlessly transition users from advisory conversations to qualified business inquiries
through a structured, deterministic, and user-friendly conversational workflow that integrates directly
with Propertism's existing General Inquiry infrastructure, maximising lead capture while maintaining
data quality, consistency, and future extensibility.
