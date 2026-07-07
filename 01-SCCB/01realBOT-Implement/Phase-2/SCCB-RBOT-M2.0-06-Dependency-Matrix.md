<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Antigravity (Authorized Execution Agent)
Reviewed By: Mindra (Final Review Authority)
Product Approval: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-05 14:35:00
Last Updated By: Antigravity
Last Updated On: 2026-07-05 14:35:00
Searchtag: SCCB-RBOT-M2.0-06-Dependency-Matrix
-->

# SCCB-RBOT-M2.0 - Dependency Matrix
## Analysis of Software, Network, and Architectural Dependencies

---

## 1. Overview

The integration transition decouples direct, high-level dependencies on AI vendors from the Propertism client and redirects them through the realBOT platform. Below is the active mapping of dependencies.

---

## 2. Dependency Classification Matrix

| Dependency Type | Dependency Name | Current Hook / Reference | Target Hook / Integration Path | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Internal Python App** | `properties` | In `chat/views.py` to parse offline inquiries | Kept as context source for property specs | RETAIN |
| **Internal Python App** | `users` | In `chat/views.py` to identify authenticated users | Kept to exchange local user claims for realBOT JWTs | RETAIN |
| **Internal Python App** | `content` | Home URL routing and base layouts | Kept for widget embedding and static parameters | RETAIN |
| **External Platform** | `realBOT API` | None | Propertism backend proxies HTTP requests | NEW |
| **External script** | `realBOT Widget SDK` | Local `realbot-panel.js` file | Embedded CDN link loaded dynamically | NEW |
| **Third-Party Python** | `requests` | None (or used for simple APIs) | Relies on `requests` for backend HTTP proxy forwarding | NEW |
| **Third-Party Python** | `djangorestframework` | Configures API serializations | Used to secure proxy inputs | RETAIN |
| **Third-Party Python** | `django-allauth` | Google OAuth | Relies on existing JWT tokens for SSO handshakes | RETAIN |
| **AI Provider SDKs** | `DeepSeek SDK / HTTP API` | Direct HTTP posts in `chat/ai_service.py` | Removed (Managed entirely inside realBOT) | REMOVE |
| **Vector Indexing** | `pgvector / chunks` | None (Mock keywords checking) | Handled by realBOT Knowledge Base | REMOVE |

---

## 3. DeepSeek & AI Provider Dependency De-coupling

```
=== CURRENT HIGH COUPLING ===
Propertism Backend ───[DEEPSEEK_API_KEY]───▶ DeepSeek Completion API

=== TARGET DE-COUPLED STATE ===
Propertism Backend ───[REALBOT_API_KEY]───▶ realBOT Gateway ───[AI Credentials]───▶ DeepSeek API
```

*   **Zero LLM Direct References:** The Propertism codebase will contain no references to `api.deepseek.com`, OpenAI, Anthropic, or other foundation model endpoints.
*   **Vector Search & Chunking:** All databases, models, vector files (like pgvector tables), or embedding generators are handled within the realBOT platform.
*   **Prompt Formatting Logic:** System configurations and system prompt strings are decoupled from Python classes and stored within realBOT's Prompt database.

---
*Maintained by Antigravity | 2026-07-05 14:35:10 IST*
