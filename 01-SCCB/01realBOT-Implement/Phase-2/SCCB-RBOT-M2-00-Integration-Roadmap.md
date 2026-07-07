<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-07-04 18:20:00
Last Updated By: Antigravity
Last Updated On: 2026-07-06 19:30:00
Searchtag: SCCB-RBOT-M2-ROADMAP
-->

# realBOT &rarr; Propertism Integration Roadmap (M2)

## M2.0 &ndash; Discovery & Integration Foundation
- Define integration boundaries
- Application ownership
- Integration contracts
- Environment strategy

## M2.1 &ndash; Configuration & Environment
- API endpoints
- Environment variables
- AI provider configuration
- Feature flags
- Security configuration

## M2.2 &ndash; Authentication & Tenant Handshake
- JWT authentication
- User identity
- Session initialization
- Tenant validation
- Secure API handshake

## M2.3 &ndash; Widget SDK Integration
- Floating realBOT launcher
- Embedded chat panel
- Open/Close APIs
- Event hooks
- Responsive behavior

## M2.4 &ndash; REST Gateway
- Chat endpoint
- Conversation endpoint
- Health endpoint
- Configuration endpoint
- Provider abstraction

## M2.5 &ndash; Property Context Integration
realBOT receives context such as:
- Current property
- City
- Locality
- Project
- Property type
- Listing ID
- User language
- Page context

This allows responses to be context-aware.

## M2.6 &ndash; Conversation & Session Management
- Conversation IDs
- Session persistence
- Conversation history
- Multi-turn chat
- Timeout handling
- Resume previous conversations

## M2.7 &ndash; Branding & Theme
- Propertism branding
- realBOT identity
- Theme synchronization
- Typography
- Icons
- Colors
- Responsive UI

## M2.8 &ndash; Health & Diagnostics
- Connectivity checks
- Provider health
- AI availability
- Response latency
- Logging
- Monitoring

## M2.9 &ndash; Error Handling & Fallback
- Retry policy
- Timeout handling
- Friendly error messages
- Provider fallback framework
- Offline handling

## M2.10 &ndash; Testing
- Unit tests
- Integration tests
- API validation
- UI validation
- Cross-browser testing
- Mobile responsiveness

## M2.11 &ndash; Production Readiness
- Security review
- Performance optimization
- Deployment checklist
- Monitoring
- Documentation
- Rollout verification

---

## Phase 1 Foundation (already defined)
The initial realBOT foundation included:
- Chat widget
- Chat page/UI
- Backend REST APIs
- AI Service Layer
- DeepSeek Provider integration
- Provider abstraction pattern
- Session management
- Conversation management
- Configuration framework
- Error handling
- Logging
- RAG-ready architecture

---

## Core Architectural Principle

```
Propertism
      │
      ▼
realBOT Widget
      │
      ▼
realBOT REST API
      │
      ▼
AI Service Layer
      │
      ▼
DeepSeek Provider
      │
      ▼
DeepSeek API
```

All AI requests flow through the AI Service Layer. Controllers never call the AI provider directly, allowing future providers (such as OpenAI, Claude, Gemini, or local LLMs) to be added without changing the application architecture.

One important constraint we also established is that realBOT remains a separate application/repository, with Propertism integrating it through defined interfaces. Development is performed locally only, with no Git push or deployment until your approval after local verification.
