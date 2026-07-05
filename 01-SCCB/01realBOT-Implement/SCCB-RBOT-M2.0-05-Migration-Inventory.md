<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Antigravity (Authorized Execution Agent)
Reviewed By: Mindra (Final Review Authority)
Product Approval: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-05 14:30:00
Last Updated By: Antigravity
Last Updated On: 2026-07-05 14:30:00
Searchtag: SCCB-RBOT-M2.0-05-Migration-Inventory
-->

# SCCB-RBOT-M2.0 - Migration Inventory
## Transition Guidelines and Migration Mappings

---

## 1. Migration Overview

To transform Propertism into a pure thin client, functional components must be moved from local application scopes to the centralized `realBOT` backend. Below is the technical plan for each layer.

---

## 2. Migration Matrix by Architectural Layer

### 2.1 Database Models
*   **Current State:** `RealBotSession` & `RealBotMessage` defined in `chat/models.py`.
*   **Target State:** Handled by `realbot.ConversationSession` and `realbot.ConversationMessage` on the realBOT platform.
*   **Migration Plan:**
    1.  Create a Django migration in the `chat` app that drops tables `chat_realbotsession` and `chat_realbotmessage`.
    2.  Write a script to clean up stale rows if necessary, avoiding references to missing models in subsequent deployments.

### 2.2 Backend Views & Business Logic
*   **Current State:** `init_session` & `send_message` query local databases and initiate direct completions with DeepSeek.
*   **Target State:** Relocated to realBOT API controllers.
*   **Migration Plan:**
    1.  Purge the business logic inside `chat/views.py`.
    2.  Implement proxy methods using the Python `requests` library to relay incoming JSON payloads to `REALBOT_BASE_URL/api/v1/conversations/init` and `/message` endpoints.
    3.  Attach appropriate JWT headers for verification.

### 2.3 AI Provider & Prompt Services
*   **Current State:** `ai_service.py` houses provider classes, prompts, and stubs.
*   **Target State:** Managed by realBOT's Prompt Engine and Pluggable Provider Registry.
*   **Migration Plan:**
    1.  Delete `chat/ai_service.py`.
    2.  Migrate the specialized corporate system prompts and E-E-A-T advisory logic into the realBOT Database under `PromptTemplate` configurations.

### 2.4 User Interface & Visual Templates
*   **Current State:** base.html includes raw templates for sliding panels, chat messages, and property listings.
*   **Target State:** Visual layouts are served by realBOT's Widget Engine.
*   **Migration Plan:**
    1.  Purge the `<script type="text/template" id="realbot-panel-template">` from `uilayers/templates/base.html`.
    2.  Remove `<link rel="stylesheet" href="{% static 'css/realbot-panel.css' %}">` from headers.
    3.  Add the embeddable Widget loader code:
        ```html
        <script src="{{ REALBOT_WIDGET_URL }}/sdk/widget.js" async defer></script>
        ```

### 2.5 JavaScript Controllers
*   **Current State:** `realbot-panel.js` manages panel animations, DOM insertion, and AJAX updates.
*   **Target State:** Managed by the official realBOT Widget SDK script.
*   **Migration Plan:**
    1.  Remove `static/js/realbot-panel.js`.
    2.  Initialize the official widget through a small inline bootstrap config:
        ```javascript
        window.addEventListener('realbot-ready', () => {
            window.realBOT.init({
                tenant: 'propertism',
                product: 'propertism.in',
                theme: { primary: '#0E2A47', accent: '#C89B2B' }
            });
        });
        ```

---

## 3. Configuration & Settings Migration

Settings must be cleaned up and aligned with integration gateway parameters:

### 3.1 Variables to Purge
*   `DEEPSEEK_API_KEY`
*   `DEEPSEEK_MODEL`
*   `DEEPSEEK_TEMPERATURE`
*   `DEEPSEEK_MAX_TOKENS`
*   `DEEPSEEK_TIMEOUT`

### 3.2 New Variables to Introduce
*   `REALBOT_BASE_URL`: Root URL of the deployed realBOT server.
*   `REALBOT_API_KEY`: Client token for server-to-server operations.
*   `REALBOT_TENANT`: Identification code (value: `'propertism'`).
*   `REALBOT_PRODUCT`: Domain classification (value: `'propertism.in'`).
*   `REALBOT_DOMAIN`: System namespace (value: `'real_estate'`).
*   `REALBOT_ENVIRONMENT`: Current environment tag (e.g., `'production'`).
*   `REALBOT_WIDGET_URL`: Script hosting directory.
*   `REALBOT_API_VERSION`: API path segment (value: `'v1'`).

---
*Maintained by Antigravity | 2026-07-05 14:30:45 IST*
