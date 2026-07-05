<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Antigravity (Authorized Execution Agent)
Reviewed By: Mindra (Final Review Authority)
Product Approval: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-05 14:45:00
Last Updated By: Antigravity
Last Updated On: 2026-07-05 14:45:00
Searchtag: SCCB-RBOT-M2.0-08-Implementation-Roadmap
-->

# SCCB-RBOT-M2.0 - Proposed Implementation Roadmap
## Execution Milestones and Step-by-Step Integration Guide

---

## 1. Roadmap Framework

This proposed roadmap outlines the sequential phases of execution for the Propertism-realBOT integration. Each phase builds upon the previous one to ensure stable, thin-client architecture compliance and zero visual regressions.

```
┌──────────────────────────────────────┐
│  M2.0: Discovery & Planning          │  ◄── CURRENT STATUS
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│  M2.1: Configuration & Env Setup     │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│  M2.2: Auth Handshake & JWT Exchange │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│  M2.3 - M2.4: Widget SDK & Proxy API │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│  M2.5 - M2.6: Context Sync & Chat    │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│  M2.7 - M2.9: UI Styling & Fallback  │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│  M2.10 - M2.11: Testing & Rollout    │
└──────────────────┘
```

---

## 2. Phase Deliverables

### Milestone M2.1: Configuration & Environment Setup
*   **Action Items:**
    1.  Add configuration variables to `settings.py` (e.g., `REALBOT_BASE_URL`, `REALBOT_API_KEY`).
    2.  Implement the feature toggle settings `REALBOT_INTEGRATION_ENABLED`.
    3.  Load variable values securely from environment variables.

### Milestone M2.2: Authentication & Tenant Handshake
*   **Action Items:**
    1.  Develop secure JWT exchange logic (`/api/v1/auth/exchange/`) on Propertism's backend.
    2.  Secure server-to-server operations with API key authentication headers.

### Milestone M2.3: Widget SDK Integration
*   **Action Items:**
    1.  Purge local styling rules (`realbot-panel.css`) and inline template tags.
    2.  Embed the official realBOT Widget script loader to lazy-load the chat interface via iframe.

### Milestone M2.4: REST API Gateway & Proxy Service
*   **Action Items:**
    1.  Refactor `chat/views.py` to route all conversation requests to realBOT API gateway.
    2.  Implement error checking and timeout handling.

### Milestone M2.5: Property Context Provider
*   **Action Items:**
    1.  Build a serialized data extractor to capture property prices, layouts, and locations on listing pages.
    2.  Provide context injection endpoints to feed active listing variables to realBOT.

### Milestone M2.6: Conversation & Session Synchronization
*   **Action Items:**
    1.  Wire up session initialization, resumption, and restart commands.
    2.  Synchronize session details in browser sessionStorage cache.

### Milestone M2.7: Branding & Theme Alignment
*   **Action Items:**
    1.  Register theme properties (Navy `#0E2A47` and Gold `#C89B2B`) on realBOT branding configurations.
    2.  Ensure correct logo resources are loaded within the widget iframe.

### Milestone M2.8: Diagnostics & Telemetry
*   **Action Items:**
    1.  Deploy health checker routines on the client.
    2.  Monitor API response latency and log errors.

### Milestone M2.9: Error Fallback Framework
*   **Action Items:**
    1.  Build frontend circuit breakers that show warning toasts if endpoints fail.
    2.  Implement a graceful offline fallback UI when `REALBOT_INTEGRATION_ENABLED` is disabled.

### Milestone M2.10: Verification & Testing
*   **Action Items:**
    1.  Execute full integration verification test suites.
    2.  Verify authentication handshakes and token exchange.

### Milestone M2.11: Production Rollout
*   **Action Items:**
    1.  Toggle environment variables to enable the integration on production AWS servers.
    2.  Monitor logs and confirm healthy operational state.

---
*Maintained by Antigravity | 2026-07-05 14:45:10 IST*
