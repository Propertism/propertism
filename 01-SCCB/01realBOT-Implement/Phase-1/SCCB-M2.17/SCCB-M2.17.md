<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Mindra
Created On: 2026-07-07
Searchtag: SCCB-PROP-RBOT-M2.17-HUMAN-HANDOVER-CONVERSATION-CLOSURE-001
-->

# SCCB-PROP-RBOT-M2.17-HUMAN-HANDOVER-CONVERSATION-CLOSURE-001

# Milestone

**M2.17 — Human Handover & Conversation Closure Framework**

---

# 1. Executive Summary

This milestone implements the final customer interaction lifecycle for the Propertism implementation of realBOT.

Until this milestone, conversations are completely handled by the deterministic Rule Engine.

M2.17 extends this lifecycle by introducing a controlled transition from automated assistance to a live Propertism advisor, followed by structured conversation closure, transcript generation, archival, analytics updates, and automatic email notifications.

This implementation shall continue to comply with the **Zero Runtime AI Dependency Architecture**.

No external AI services shall participate.

---

# 2. Objectives

Implement a complete end-to-end customer lifecycle comprising:

- Human advisor handover
- Advisor conversation continuation
- Customer or advisor initiated conversation closure
- Transcript generation
- Automatic email delivery
- Conversation archival
- Analytics updates
- Complete audit trail

---

# 3. Scope

This SCCB includes:

- Human handover
- Advisor workspace integration
- Conversation ownership transfer
- Live conversation continuation
- Conversation closure
- Transcript generation
- Email notifications
- Archive management
- Diagnostics
- Analytics

---

# 4. Architecture

```
Customer
      │
      ▼
realBOT
      │
      ▼
Conversation Engine
      │
      ▼
Human Handover Manager
      │
      ▼
Advisor Workspace
      │
      ▼
Conversation Closure
      │
      ▼
Transcript Generator
      │
      ▼
Archive Manager
      │
      ▼
Email Dispatcher
      │
      ▼
Analytics
```

---

# 5. Conversation State Machine

```
BOT_ACTIVE

↓

HANDOVER_REQUESTED

↓

WAITING_FOR_AGENT

↓

AGENT_CONNECTED

↓

HUMAN_CONVERSATION

↓

CHAT_END_REQUESTED

↓

CHAT_CLOSED

↓

ARCHIVED
```

No conversation shall skip any mandatory transition.

---

# 6. Human Handover Framework

## Customer Actions

Customer may initiate handover by:

- Talk to Advisor
- Contact Advisor
- Human Assistance
- Connect to Human Agent
- Request Callback
- Escalate Conversation

or any configured synonym.

---

## Bot Behaviour

realBOT shall reply:

> Thank you. I'm transferring this conversation to a Propertism advisor. Please wait while one of our advisors joins the conversation.

The conversation state shall change to

```
HANDOVER_REQUESTED
```

---

## Queue Management

The framework shall maintain:

Waiting Queue

↓

Available Advisors

↓

Accepted Conversation

↓

Active Conversation

↓

Completed Conversation

---

# 7. Advisor Workspace

The Propertism administration portal shall provide:

## Waiting Conversations

Display

- Conversation ID
- Customer Name
- Country
- Service
- Current Intent
- Waiting Duration

---

## Accept Conversation

Once accepted

- conversation ownership transfers
- bot responses stop
- advisor responses begin

---

## Advisor Capabilities

Advisor may

- read entire conversation
- continue existing conversation
- view customer details
- view inquiry
- view service selections
- view conversation context
- send messages
- attach notes
- close conversation

---

# 8. Bot Suspension

Once an advisor accepts:

realBOT shall

- stop generating responses
- preserve context
- preserve transcript
- preserve analytics

The advisor becomes the active responder.

---

# 9. Conversation Closure

Conversation may be closed by

Customer

or

Advisor

---

## Customer Flow

End Conversation

↓

Confirmation

```
End this conversation?

Yes

Cancel
```

If confirmed

Conversation closes.

---

## Advisor Flow

Advisor selects

Close Conversation

↓

Optional resolution notes

↓

Conversation archived

---

# 10. Conversation Transcript

Automatically generate transcript.

Include

## Session Information

- Conversation ID
- Session ID
- Started
- Ended
- Duration

---

## Customer Information

- Name
- Phone
- Email
- Country

---

## Business Information

- Service Selected
- Inquiry
- Active Intent
- Assigned Advisor

---

## Conversation

Every message

including

- sender
- timestamp
- message
- suggestion chips clicked
- actions executed

---

## Resolution

- Closed By
- Closure Reason
- Resolution Status

---

# 11. Transcript Format

Generate structured HTML email.

Sections

- Header
- Customer Details
- Conversation Summary
- Complete Transcript
- Inquiry Details
- Resolution
- Footer

Formatting shall follow Propertism branding.

---

# 12. Automatic Email Delivery

Upon successful conversation closure

Automatically email transcript.

Recipients shall NOT be hardcoded.

Recipients shall be read from

```
.env
```

Example

```
REALBOT_TRANSCRIPT_EMAIL_RECIPIENTS=
tamil@propertism.in,
propertism.tami@gmail.com
```

The framework shall support

- one recipient
- multiple recipients
- comma-separated recipients

---

# 13. Email Subject

Example

```
realBOT Conversation Transcript

Conversation ID:
RB-20260707-000145

Customer:
John David

Status:
Completed
```

---

# 14. Email Failure Handling

If email delivery fails

Conversation SHALL NOT fail.

Instead

- archive conversation
- log email failure
- retry according to notification policy
- notify administrator

---

# 15. Conversation Archive

Persist

- all messages
- advisor replies
- customer replies
- suggestion chips
- actions executed
- knowledge articles
- service selections
- inquiry details
- navigation history
- timestamps
- context snapshot

Archive shall be immutable.

---

# 16. Advisor Notifications

When new handover requested

Notify advisor.

Future notification providers may include

- Email
- WhatsApp
- Internal dashboard
- Push notifications

Provider abstraction shall be maintained.

---

# 17. Administration

Provide

## Active Conversations

## Waiting Conversations

## Completed Conversations

## Search Conversation

## View Transcript

## Download Transcript

## Resend Transcript

## Conversation Analytics

---

# 18. Analytics

Capture

- Human handovers
- Waiting time
- Acceptance time
- Conversation duration
- Closure duration
- Advisor workload
- Transcript generation
- Email delivery
- Customer completion

---

# 19. Audit Trail

Record

- handover requested
- advisor assigned
- advisor accepted
- advisor joined
- advisor replied
- conversation closed
- transcript generated
- transcript emailed
- archive completed

Audit entries shall be append-only.

---

# 20. Security

Only authenticated administrators may

- accept conversations
- reply as advisor
- close conversations
- view transcripts
- resend transcripts

Conversation history shall never be editable.

---

# 21. Configuration

Read from Configuration Manager and `.env`.

Examples

```
REALBOT_TRANSCRIPT_EMAIL_RECIPIENTS

REALBOT_EMAIL_ENABLED

REALBOT_AGENT_HANDOVER_ENABLED

REALBOT_TRANSCRIPT_SUBJECT_PREFIX

REALBOT_EMAIL_RETRY_COUNT

REALBOT_EMAIL_TIMEOUT

REALBOT_AGENT_IDLE_TIMEOUT
```

No values shall be hardcoded.

---

# 22. Diagnostics

Provide diagnostics for

- Active conversations
- Waiting queue
- Connected advisors
- Email delivery status
- Archive status
- Transcript generation
- Queue length
- Failed notifications

---

# 23. Deliverables

Implement

- HumanHandoverManager
- AdvisorConversationManager
- ConversationClosureManager
- TranscriptGenerator
- TranscriptEmailDispatcher
- ConversationArchiveManager
- AdvisorQueueManager
- ConversationLifecycleManager

Provide

- Django models
- REST APIs
- Django Admin
- Management Commands
- Unit Tests
- Integration Tests

---

# 24. Acceptance Criteria

- Human handover operational.
- Advisor queue operational.
- Advisor can accept conversations.
- Bot suspends after advisor acceptance.
- Advisor continues same conversation.
- Customer context preserved.
- Conversation closes successfully.
- Transcript generated automatically.
- Transcript archived automatically.
- Transcript emailed automatically.
- Email recipients loaded from `.env`.
- Email failures handled gracefully.
- Analytics updated.
- Audit logs generated.
- Zero conversation loss.
- Zero regression to M2.1–M2.16.

---

# 25. Success Criteria

The Human Handover & Conversation Closure Framework shall provide a seamless transition from deterministic realBOT assistance to live Propertism advisors while preserving the complete conversational context. Every conversation shall conclude with a professionally formatted transcript, secure archival, configurable email distribution, complete analytics, and immutable audit records, ensuring production-grade customer support without introducing any runtime AI dependency.
