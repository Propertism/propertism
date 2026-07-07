<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Antigravity (Authorized Execution Agent)
Reviewed By: Mindra (Final Review Authority)
Product Approval: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-05 14:25:00
Last Updated By: Antigravity
Last Updated On: 2026-07-05 14:25:00
Searchtag: SCCB-RBOT-M2.0-04-Integration-Inventory
-->

# SCCB-RBOT-M2.0 - Integration Inventory
## Component Classification, Rationales, and Touchpoint Mappings

---

## 1. Classification Definitions

To guarantee a clean transition to the thin-client architecture, every file, function, and setting in the current chatbot app is classified into one of the following categories:
*   **RETAIN:** Kept in Propertism with zero or minor functional modifications.
*   **REPLACE:** Swapped out for realBOT-native alternatives or scripts.
*   **DEPRECATE:** Marked for structured replacement (kept temporarily during transition, then removed).
*   **REMOVE:** Completely deleted from the Propertism codebase.
*   **REDIRECT/PROXY:** Pointed directly to realBOT endpoints.

---

## 2. Component Inventory Matrix

| Component Path | Current Responsibility | Classification | Target / Action | Justification |
| :--- | :--- | :--- | :--- | :--- |
| `chat/models.py` | Defines `RealBotSession` & `RealBotMessage` | **DEPRECATE** | Purge database rows, delete code files in Phase 2 | Relocates schema structures to the `realBOT` database to remove database duplicates. |
| `chat/ai_service.py` | DeepSeek API integration, system prompts, stub interfaces | **REMOVE** | Delete file | The provider connections and system prompts are now managed globally inside the realBOT workspace. |
| `chat/views.py` `init_session` | Local session creation and history database query | **REPLACE** & **PROXY** | Re-engineer as a proxy to realBOT `/api/v1/conversations/init/` | Moves session logic to realBOT while retaining the local `/chat/session/init/` routing hook for proxying. |
| `chat/views.py` `send_message` | Logs messages, runs keyword checks, executes AI completions | **REPLACE** & **PROXY** | Re-engineer as a proxy to realBOT `/api/v1/conversations/message/` | Moves prompt compiling, mock rules, and API connection to realBOT; backend becomes a thin client request forwarder. |
| `chat/views.py` `submit_chat_message` | Processes offline lead forms into local `ContactMessage` | **RETAIN** | Keep functionality | Collects offline contacts; does not interact with the conversational AI system. |
| `chat/urls.py` | Maps endpoints `/chat/session/init/`, `/chat/query/`, etc. | **RETAIN** | Keep same routes, map views to proxy controllers | Prevents breaking current client-side scripts during the integration transition. |
| `static/js/realbot-panel.js` | Controls chat panel rendering and handles AJAX queries | **REPLACE** | Replace with realBOT script loader and iframe messenger | Replaced by the official realBOT Widget SDK script. |
| `static/css/realbot-panel.css` | visual styles for chat panel layouts | **REMOVE** | Delete stylesheet | Layout styling is served dynamically by the widget's internal iframe templates. |
| `uilayers/templates/base.html` | Embeds styles and includes panel `<script>` template | **REPLACE** | Replace with realBOT widget container code block | Visual layout elements are rendered inside the realBOT iframe. |
| `uilayers/templates/realbot.html` | Simulated desktop dashboard / mockup view | **RETAIN** | Keep as demo console page | Useful workspace sandbox to test realBOT widget components in real-time. |
| `realtor_project/settings.py` `DEEPSEEK_*` vars | Local completion credentials | **REMOVE** | Purge settings variables | Replaced by clean gateway settings `REALBOT_BASE_URL` and `REALBOT_API_KEY`. |

---
*Maintained by Antigravity | 2026-07-05 14:25:20 IST*
