<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Mindra
Created On: 2026-07-07
Searchtag: SCCB-PROP-RBOT-ARCH-AI-INDEPENDENCE-001
-->

# SCCB-PROP-RBOT-ARCH-AI-INDEPENDENCE-001 — Zero Runtime AI Dependency Policy

## 1. Executive Summary

This SCCB establishes the architectural policy that the **Propertism implementation of realBOT shall operate as a fully deterministic, rule-based conversational system with zero runtime dependency on external Artificial Intelligence (LLM) providers.**

The objective is to ensure that all customer interactions remain deterministic, predictable, secure, privacy-preserving, highly available, and free from recurring API costs while leveraging the existing realBOT Core Platform and the Propertism knowledge ecosystem.

---

# 2. Background

The **realBOT Core Platform** has already been developed as a reusable conversational platform.

The current implementation scope is:

> **Integration of realBOT into Propertism.in**

This integration consumes:

- Website Knowledge Base
- Internal Knowledge Repository
- Rule Engine
- Service Profiles
- Inquiry Framework
- Navigation Services
- Suggestion Framework
- Rich Response Framework
- Conversation Context
- Business Analytics

Accordingly, customer conversations shall be resolved entirely through deterministic business logic without requiring external AI inference.

---

# 3. Architectural Decision

## Runtime Policy

The Propertism deployment shall execute customer conversations using only locally available components.

```
Customer
      │
      ▼
Propertism Website
      │
      ▼
realBOT
      │
 ┌───────────────┐
 │ Rule Engine   │
 │ Knowledge     │
 │ Services      │
 │ Inquiry       │
 │ Navigation    │
 │ Suggestions   │
 │ Context       │
 │ Responses     │
 └───────────────┘
      │
      ▼
Propertism Database
```

No external AI provider shall participate in runtime response generation.

---

# 4. Runtime Resolution Order

Every incoming message shall be processed using the following deterministic pipeline:

1. Conversation Context
2. Rule Engine
3. Website Knowledge
4. Internal Knowledge
5. Service Profiles
6. Inquiry Engine
7. Navigation Framework
8. Suggestion Framework
9. Rich Response Builder
10. Response Delivery

Only this pipeline shall determine customer responses.

---

# 5. Prohibited Runtime Dependencies

The production deployment shall **NOT** invoke external LLM providers during customer conversations, including but not limited to:

- OpenAI
- Anthropic Claude
- Google Gemini
- DeepSeek
- Grok
- Cohere
- Mistral
- Meta Llama APIs
- Azure OpenAI
- AWS Bedrock hosted models
- Any third-party hosted LLM inference service

This restriction applies to:

- Response generation
- Intent classification
- Knowledge retrieval
- Question answering
- Inquiry creation
- Customer guidance

---

# 6. Approved External Integrations

The following integrations remain permitted because they provide business functionality rather than conversational intelligence:

## Communication

- WhatsApp
- Telephone
- Email (SMTP)

## Maps & Navigation

- Google Maps

## Social Platforms

- LinkedIn

## Government Services

- Patta / Chitta
- Encumbrance Search
- GCC Property Tax
- Other approved public portals

## Security

- Google reCAPTCHA
- Cloudflare Turnstile (future)

## Infrastructure

- Database
- Redis
- Django
- Internal APIs

---

# 7. Benefits

This architecture provides:

- Deterministic responses
- Consistent customer experience
- Zero AI API costs
- No token consumption
- No rate limiting
- No vendor lock-in
- Improved customer privacy
- Faster response times
- Offline-ready architecture (excluding approved external business integrations)
- Simplified compliance and auditing

---

# 8. Future AI Extensibility

The architecture shall remain extensible.

Future AI capabilities may be introduced only through an optional provider abstraction layer.

Example:

```
Customer
      │
      ▼
Rule Engine
      │
Knowledge Engine
      │
Response Builder
      │
      ▼
Customer
```

Future optional flow:

```
Rule Engine
      │
No Deterministic Match
      │
      ▼
Optional AI Provider
      │
      ▼
Human Review / Future Enhancement
```

The AI provider shall remain:

- Optional
- Configuration-controlled
- Disabled by default
- Outside the deterministic execution path

---

# 9. Compliance Requirements

The implementation shall ensure:

- No runtime AI API keys are required.
- No AI SDKs are mandatory for production deployment.
- System startup shall succeed without AI provider configuration.
- All customer-facing functionality shall operate without external AI services.
- Existing business integrations shall remain unaffected.

---

# 10. Acceptance Criteria

- [ ] No runtime dependency on external LLM providers.
- [ ] All customer conversations resolved deterministically.
- [ ] Website knowledge fully supports customer queries.
- [ ] Internal document knowledge fully supports customer queries.
- [ ] Inquiry creation remains deterministic.
- [ ] Navigation and action services remain deterministic.
- [ ] Suggestion framework operates locally.
- [ ] Rich response generation operates locally.
- [ ] Production deployment requires no AI API credentials.
- [ ] Existing approved business integrations continue to function.
- [ ] Future AI providers remain optional and disabled by default.

---

# 11. Impact Assessment

This SCCB introduces **no breaking changes** to M2.1–M2.16.

Instead, it formalizes the architectural principle already followed throughout the Propertism integration and establishes **Zero Runtime AI Dependency** as the governing design policy for the Propertism deployment of realBOT.
