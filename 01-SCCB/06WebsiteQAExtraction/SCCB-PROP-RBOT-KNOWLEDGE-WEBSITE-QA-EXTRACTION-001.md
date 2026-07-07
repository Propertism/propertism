<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Mindra
Created On: 2026-07-07
Searchtag: SCCB-PROP-RBOT-KNOWLEDGE-WEBSITE-QA-EXTRACTION-001
-->

# SCCB-PROP-RBOT-KNOWLEDGE-WEBSITE-QA-EXTRACTION-001

## Title

Website Conversational Knowledge Extraction Framework

---

# Objective

Implement a deterministic Website Conversational Knowledge Extraction Framework that transforms published Propertism webpages into structured conversational knowledge assets suitable for rule-based customer interactions.

Instead of indexing raw webpage content alone, the framework shall automatically derive reusable Question-and-Answer knowledge records from website components.

---

# Business Motivation

The existing Website Knowledge Repository indexes webpage content.

However, many customer questions are entity-based rather than page-based.

Examples:

- Who is Tamilselvan?
- Who are your founders?
- Do you manage rental properties?
- Where is your office?
- What services do you offer?
- How can I contact Propertism?
- What is NRI Assist?
- Do you help NRIs?

These questions should be answerable directly without requiring AI inference.

---

# Scope

The extractor shall analyse every published webpage and generate conversational knowledge.

---

# Extraction Categories

## Company

Generate Q&A for:

- Company name
- About Propertism
- Vision
- Mission
- Why choose Propertism
- Years of experience
- Coverage locations

---

## Team Members

Generate:

- Who is <Person>?
- What is <Person>'s role?
- What does <Person> specialize in?
- Meet our advisors.
- Who can help me with NRI services?
- Who can help me sell property?

Each team member shall become an independent knowledge entity.

---

## Services

Generate:

- What services do you offer?
- Tell me about Rental Management.
- Tell me about Property Management.
- Tell me about Selling Property.
- Tell me about NRI Services.
- What is included?
- Who is eligible?

---

## Property Listings

Generate:

- Tell me about <Property>.
- Where is <Property>?
- What is the price?
- What configuration is available?
- Is it available?

---

## Testimonials

Generate:

- Customer testimonials
- Success stories
- Reviews

---

## FAQs

Generate one knowledge record for every FAQ.

---

## Resource Hub

Generate:

- Article summary
- Related questions
- Suggested follow-up questions

---

## Contact

Generate:

- Phone number
- Email
- Office location
- Working hours
- WhatsApp
- Google Maps

---

## Navigation

Generate:

- Where can I find...
- Take me to...
- Open...

---

## Government Links

Generate:

- Patta
- Chitta
- Encumbrance
- GCC Tax

---

# Knowledge Record Structure

Every extracted knowledge item shall contain:

- Knowledge ID
- Entity Type
- Entity Name
- Primary Question
- Alternative Questions
- Canonical Answer
- Keywords
- Synonyms
- Source URL
- Source Section
- Language
- Search Weight

---

# Synonym Generation

Generate deterministic synonyms.

Example:

Tamilselvan

↓

Mr Tamilselvan

↓

Tamil Selvan

↓

Advisor Tamilselvan

↓

Senior Consultant

↓

Relationship Manager

---

# Question Variants

Generate multiple deterministic question variants.

Example

Primary

Who is Tamilselvan?

Variants

Tell me about Tamilselvan.

Who is Mr Tamilselvan?

Can you introduce Tamilselvan?

What does Tamilselvan do?

Who handles NRI clients?

---

# Integration

Integrate with:

- M2.2 Website Knowledge Repository
- M2.4 Rule Engine
- M2.7 Suggestion Framework
- M2.15 Knowledge Administration
- M2.16 Analytics

No AI services shall be invoked.

---

# Administration

Knowledge Administrators shall be able to:

- View generated questions
- Edit generated answers
- Add aliases
- Add synonyms
- Approve publication
- Regenerate website Q&A
- Disable individual questions

---

# Acceptance Criteria

- Website components converted into conversational knowledge.
- Every Team Member searchable.
- Every Service searchable.
- Every FAQ searchable.
- Every Resource searchable.
- Every Contact method searchable.
- Synonyms generated deterministically.
- Question variants generated deterministically.
- Knowledge editable from M2.15.
- Searchable through existing Knowledge Engine.
- No runtime AI dependency.
- Zero regression to M2.1–M2.16.

---

# Success Criteria

The Website Conversational Knowledge Extraction Framework shall transform Propertism webpages into a structured conversational knowledge repository by generating deterministic question-and-answer records for every significant business entity, service, team member, contact point, resource, and website component. This ensures that realBOT can answer natural customer questions such as "Who is Tamilselvan?" or "Tell me about Rental Management" directly from curated website knowledge without relying on external AI services, thereby improving coverage, consistency, searchability, and customer experience while preserving the Zero Runtime AI Dependency architecture.
