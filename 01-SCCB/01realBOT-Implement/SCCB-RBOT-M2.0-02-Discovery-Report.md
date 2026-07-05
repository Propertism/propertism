<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Antigravity (Authorized Execution Agent)
Reviewed By: Mindra (Final Review Authority)
Product Approval: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-05 14:15:00
Last Updated By: Antigravity
Last Updated On: 2026-07-05 14:15:00
Searchtag: SCCB-RBOT-M2.0-02-Discovery-Report
-->

# SCCB-RBOT-M2.0 - Discovery Report
## Analysis of the Existing Propertism Chatbot Implementation

---

## 1. Directory Structure

The current chatbot logic in the Propertism repository resides primarily in the `chat` application, with matching static assets and template layers in `uilayers` and `static`.

```
01propertism/
├── chat/
│   ├── admin.py            # Registers RealBotSession and RealBotMessage in Django Admin
│   ├── ai_service.py       # Holds provider ABC, DeepSeekProvider, and AIService
│   ├── apps.py             # App registry config ('chat')
│   ├── models.py           # Database models for sessions and messages
│   ├── urls.py             # Chat-related url endpoints
│   └── views.py            # Controllers for session initialization and chat queries
├── static/
│   ├── css/
│   │   └── realbot-panel.css # Visual styling rules for sliding panel, chips, property card elements
│   └── js/
│   │   └── realbot-panel.js  # Floating panel UI logic, session management, markup renderers
├── uilayers/
│   └── templates/
│       ├── base.html       # Embeds the floating panel lazy-loading script template
│       └── realbot.html    # Standalone simulated chat advisory console
└── realtor_project/
    └── settings.py         # Declares DEEPSEEK_* settings
```

---

## 2. Models Analysis (`chat/models.py`)

The application defines two database models for storing conversations:

### A. `RealBotSession`
*   **Purpose:** Tracks unique user session UUIDs.
*   **Schema:**
    *   `session_id`: `models.UUIDField` (Primary Key, defaults to `uuid.uuid4`).
    *   `user`: `models.ForeignKey(User)` (Optional, nullable link to authenticated users).
    *   `created_at`: `models.DateTimeField(auto_now_add=True)`.
    *   `updated_at`: `models.DateTimeField(auto_now=True)`.

### B. `RealBotMessage`
*   **Purpose:** Stores message history.
*   **Schema:**
    *   `session`: `models.ForeignKey(RealBotSession)` (Cascade delete).
    *   `sender`: `models.CharField` (Choices: `user` = "Client Consultant", `assistant` = "realBOT Advisor").
    *   `text`: `models.TextField` (Message content).
    *   `metadata`: `models.JSONField` (Optional; stores chips, property cards, comparisons, or citations).
    *   `created_at`: `models.DateTimeField(auto_now_add=True)`.

---

## 3. Core AI Integration (`chat/ai_service.py`)

The service layer implements provider abstractions and a concrete client for DeepSeek:

*   **Abstract Interfaces:**
    *   `AIProvider(ABC)`: Declares `generate_response(messages, system_prompt)`.
    *   `KnowledgeProvider`, `ContextBuilder`, `CitationProvider`, `RetrievalLayer` (Stub interfaces reserved for future RAG extensions).
*   **`DeepSeekProvider(AIProvider)`:**
    *   Initiates direct requests to the endpoint `https://api.deepseek.com/chat/completions`.
    *   Loads API keys and settings from Django `settings.DEEPSEEK_*`.
    *   Performs validation on requests, handling timeouts (15s), connection failures, and HTTP status issues (e.g., 401 Unauthorized, 429 Rate Limit, 500 Server Failures).
*   **`AIService`:**
    *   Orchestration class mapping prompts and default parameters.
    *   Configures a system prompt defining realBOT's formal persona (professional, no emojis, markdown formatting).

---

## 4. API Endpoints & Views (`chat/views.py` & `chat/urls.py`)

Three main endpoints are defined:

1.  **`chat/submit/` (`submit_chat_message`):**
    *   Used by legacy forms. Takes name, email, phone, and message POST parameters, saves them to a `ContactMessage` model in the `properties` app, and emails the administrators.
2.  **`chat/session/init/` (`init_session`):**
    *   GET/POST endpoint. Checks for an active `session_id`. Resumes session if valid, otherwise spins up a new `RealBotSession` and seeds an initial welcome message containing suggested chips.
3.  **`chat/query/` (`send_message`):**
    *   POST endpoint. Validates session, logs the user's message, compiles thread history, calls `AIService` to contact the DeepSeek completion API, and logs the response.
    *   **Heuristic Mock Interceptor:** Inspects incoming message text to append visual metadata blocks:
        *   Keywords `"villa"`, `"luxury"`: Injects an exclusive ECR Beach Villa property card.
        *   Keywords `"nri"`, `"investment"`: Injects capital yield comparison tables and RBI citation lists.
        *   Keywords `"apartment"`, `"budget"`: Injects a value-tier apartment property card.
        *   Others: Renders generic fallback suggestion chips.

---

## 5. UI and JavaScript controller (`static/js/realbot-panel.js`)

*   **FAB Trigger Logic:** Automatically injects a circular Navy & Gold floating action button (FAB) with animated ripple rings.
*   **Teaser Mode Guard:** Currently intercepts the FAB click to show a "Coming Soon" toast message instead of launching the interface, keeping the chatbot inactive on the live site.
*   **Sliding Panel DOM:** Lazy-loads panel HTML markup from the `<script type="text/template" id="realbot-panel-template">` block inside `base.html` to avoid heavy initial page loads.
*   **Conversational Renderer:** Translates basic markdown formatting, parses headings, styles property listing cards (image, tags, price, details, list highlights), constructs visual tabular structures, and displays citations.
*   **Suggested Chips Control:** Allows clicking inline chip options, which immediately dispatches queries through the conversation controller.

---

## 6. Configured settings variables (`realtor_project/settings.py`)

Variables initialized from the environment:
*   `DEEPSEEK_API_KEY`: API authentication key.
*   `DEEPSEEK_MODEL`: Completion model (default: `deepseek-chat`).
*   `DEEPSEEK_TEMPERATURE`: Creativity parameter (default: `0.2`).
*   `DEEPSEEK_MAX_TOKENS`: Max tokens cutoff (default: `2000`).
*   `DEEPSEEK_TIMEOUT`: Network timeout limit (default: `15`).

---
*Maintained by Antigravity | 2026-07-05 14:15:50 IST*
