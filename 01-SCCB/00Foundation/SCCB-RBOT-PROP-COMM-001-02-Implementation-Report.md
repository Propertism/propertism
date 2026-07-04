<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-07-04 11:00:00
Last Updated By: Astra
Last Updated On: 2026-07-04 11:00:00
Searchtag: SCCB-RBOT-PROP-COMM-001
-->

# Implementation Readiness & Touchpoint Inventory Report
## chat/ App Structural Audit & Integration Mapping

**Date:** July 04, 2026  
**Architect:** Astra (Integration Architect)  
**Status:** READINESS ANALYSIS (IMPLEMENTATION ON HOLD)  

---

## 1. Existing Chatbot Touchpoints & Inventory

An audit of the current Propertism repository has mapped all active areas touching the chatbot flow:

### A. Backend App (`chat/`)
- `chat/views.py`: Exposes `init_session` and `send_message` REST endpoints.
- `chat/models.py`: Defines database models `RealBotSession` (UUID based session tracking) and `RealBotMessage` (role/sender and metadata logs).
- `chat/ai_service.py`: Contains RAG stub interfaces, `DeepSeekProvider` (API request handler), and `AIService` orchestrator.
- `chat/urls.py`: Configures namespace routing for chat endpoints.

### B. Settings & Config Locations
- `realtor_project/settings.py` lines 544-550: Holds DeepSeek model parameters (`DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL`, `DEEPSEEK_TEMPERATURE`, `DEEPSEEK_MAX_TOKENS`, `DEEPSEEK_TIMEOUT`).

### C. Frontend UI
- `uilayers/templates/base.html` lines 337-425:
  - `featured-properties-data` script block serializing featured property listings.
  - `realbot-panel-template` container template holding the sliding message overlay.
  - `js/realbot-panel.js` loader and script controller.
- `static/js/realbot-panel.js`: Handles trigger FAB rendering, session init, markdown text processing, and AJAX query posting.
- `uilayers/templates/properties/detail.html`: Property detail view.

---

## 2. Deprecated Components Inventory

When the integration resumes, the following components will be deprecated and deleted:
1. `chat/ai_service.py` (Delete - completely clean out local prompt/LLM connections).
2. settings.py `DEEPSEEK_*` keys (Delete - replace with `REALBOT_*` URLs).
3. `chat/models.py` database writes (Overridden to disable writes, database schemas eventually dropped).

---

## 3. Implementation Assumptions

- **Host Environment:** `REALBOT_BASE_URL` will be provided as an environment variable in production.
- **REST Endpoints:** realBOT will host standard versioned `/api/v1/sessions/init/` and `/api/v1/chats/message/` routes.
- **Widget script:** Widget will render fully within an iframe or shadow DOM via `<script src="[derived_widget_url]"></script>` dynamically.

---

***
*Maintained by Astra | 2026-07-04 11:00 IST*
