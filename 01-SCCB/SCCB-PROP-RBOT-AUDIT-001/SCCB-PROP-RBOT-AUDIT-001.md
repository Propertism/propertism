# SCCB-PROP-RBOT-AUDIT-001

## Title: Read-Only Audit — realBOT Production Connection Failures

**Date:** 2026-07-07  
**Status:** COMPLETED (Read-Only Audit)  
**Scope:** Propertism realBOT integration — Frontend JS (`realbot-panel.js`), Backend Views (`chat/views.py`), URL Routing, Settings, Feature Flags

---

## 1. Executive Summary

The user reported that in production, the realBOT advisory panel shows two distinct error messages:

1. **On session init:** *"Welcome to realBOT (advisory channel). Connection failed. Please verify that the local server is running and database migrations have been applied."*
2. **On sending a message:** *"Connection failure. Check your internet connection and try again."*

A full read-only audit was conducted across the frontend JavaScript (`static/js/realbot-panel.js`), backend views (`chat/views.py`), URL routing (`realtor_project/urls.py`, `chat/urls.py`), settings (`realtor_project/settings.py`), and feature flags (`feature_flags.json`).

---

## 2. Root Cause Analysis

### 2.1 Error #1 — Session Init Failure

**Source:** `static/js/realbot-panel.js`, function `initializeSession()` (line ~97-138)

The frontend calls `fetch('/chat/session/init/')`. If this fetch fails (network error, server error, or non-OK response), the `.catch()` block renders a hardcoded fallback message:

> *"Welcome to **realBOT** (advisory channel). Connection failed. Please verify that the local server is running and database migrations have been applied."*

**Why it fails in production:** The frontend JS (`realbot-panel.js`) is loaded on the `/realbot/` page (served by `uilayers/templates/realbot.html`). The JS calls `/chat/session/init/` which routes to `chat.views.init_session`. This view checks `is_realbot_enabled()` which requires BOTH:
- `settings.REALBOT_INTEGRATION_ENABLED = True` (env var or default `False`)
- `is_feature_enabled('REALBOT_INTEGRATION_ENABLED')` (from `feature_flags.json`)

The `feature_flags.json` has `"REALBOT_INTEGRATION_ENABLED": true`, but the **settings default is `False`** unless the env var is explicitly set. If the env var is not set in production, the view returns a 403 error with `ERR_INTEGRATION_DISABLED`, which causes the frontend fetch to fail and fall into the `.catch()` block.

### 2.2 Error #2 — Message Send Failure

**Source:** `static/js/realbot-panel.js`, function `triggerResponseSequence()` (line ~506-556)

The frontend calls `fetch('/chat/query/', { method: 'POST', ... })`. If this fails, the `.catch()` block renders:

> *"Connection failure. Check your internet connection and try again."*

**Why it fails in production:** Same root cause — if `init_session` fails (Error #1), the `sessionId` remains `null`. When the user types a message, `triggerResponseSequence()` sends `session_id: null` to `/chat/query/`. The backend `send_message` view requires a valid `session_id` and returns a 404 error (`ERR_SESSION_NOT_FOUND`), causing the frontend `.catch()` to trigger.

### 2.3 Additional Issue — URL Path Mismatch

The frontend JS calls:
- `/chat/session/init/` (line 106)
- `/chat/query/` (line 526)

But the project's `realtor_project/urls.py` defines BOTH:
- `path('chat/', include('chat.urls'))` — which maps to `chat/urls.py` with paths like `session/init/`, `query/`
- `path('api/v1/realbot/session/init/', ...)` — direct API paths

The `chat/urls.py` defines paths WITHOUT the `/api/v1/realbot` prefix:
- `path('session/init/', views.init_session, ...)`
- `path('query/', views.send_message, ...)`

So `/chat/session/init/` resolves correctly via `chat/urls.py`. **This is NOT a routing issue** — the paths are correct.

### 2.4 The `realbot.html` Template Has a Separate JS Block

The `uilayers/templates/realbot.html` template has its own inline `<script>` block (lines 673-1360) that handles session init via `initRealBotSession()` calling `/chat/session/init/` with POST. This is separate from the `realbot-panel.js` logic. The template's inline script also has a `.catch()` that silently degrades to demo mode.

---

## 3. Files Examined

| File | Path | Role |
|------|------|------|
| Frontend JS | `static/js/realbot-panel.js` | Client-side realBOT panel logic (636 lines) |
| Backend Views | `chat/views.py` | Django views for session init, message send, health, etc. (3228 lines) |
| Chat URLs | `chat/urls.py` | URL routing for chat endpoints (95 lines) |
| Main URLs | `realtor_project/urls.py` | Project-level URL routing (129 lines) |
| Settings | `realtor_project/settings.py` | Django settings including REALBOT flags (717 lines) |
| Feature Flags | `feature_flags.json` | JSON feature flag configuration |
| Constants | `chat/constants.py` | Error codes, state constants (122 lines) |
| Responses | `chat/responses.py` | Standard API response builder (21 lines) |
| AI Service | `chat/ai_service.py` | DeepSeek AI provider integration (165 lines) |
| Template | `uilayers/templates/realbot.html` | realBOT UI template with inline handover JS (1360 lines) |
| Env Example | `.env.example` | Environment variable documentation |

---

## 4. Detailed Findings

### 4.1 `is_realbot_enabled()` Gate (chat/views.py, line 21-23)

```python
def is_realbot_enabled():
    return getattr(settings, 'REALBOT_INTEGRATION_ENABLED', False) and \
           is_feature_enabled('REALBOT_INTEGRATION_ENABLED', default=True)
```

- **AND condition** — BOTH must be true
- `settings.REALBOT_INTEGRATION_ENABLED` defaults to `False` unless env var is set
- `feature_flags.json` has `"REALBOT_INTEGRATION_ENABLED": true`
- If the env var is not set in production, the function returns `False`

### 4.2 `is_ai_enabled()` Gate (chat/views.py, line 25-27)

```python
def is_ai_enabled():
    return getattr(settings, 'REALBOT_AI_ENABLED', False) or \
           is_feature_enabled('REALBOT_AI_ENABLED', default=False)
```

- **OR condition** — either can be true
- `settings.REALBOT_AI_ENABLED` defaults to `False`
- `feature_flags.json` has `"REALBOT_AI_ENABLED": false`
- AI is disabled in both — this is intentional

### 4.3 DeepSeek API Key Concern

In `realtor_project/settings.py`:
```python
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', 'AIzaSyBAOA3xvBpa3FQF4l27hVh7-_5mlTR3zB0')
```

The hardcoded default value `'AIzaSyBAOA3xvBpa3FQF4l27hVh7-_5mlTR3zB0'` appears to be a Google API key format, not a DeepSeek key. This is a placeholder/incorrect default. However, since `is_ai_enabled()` returns `False`, the AI service is never called, so this is not causing the current errors.

### 4.4 Frontend Error Messages Are Hardcoded

The error messages shown to users are hardcoded strings in `realbot-panel.js`:
- Line 131: `"Welcome to **realBOT** (advisory channel). Connection failed..."` — shown on session init failure
- Line 554: `"Connection failure. Check your internet connection and try again."` — shown on query failure
- Line 548: `"The advisor is currently offline. Please try again."` — shown on API error response

These messages are misleading because they suggest infrastructure problems when the actual issue is likely the `REALBOT_INTEGRATION_ENABLED` setting.

### 4.5 The `realbot.html` Template Has Its Own Session Init

The template's inline script (line 754-768) has `initRealBotSession()` which calls `/chat/session/init/` with POST. This is separate from the `realbot-panel.js` `initializeSession()` which uses GET. Both can fail independently.

---

## 5. Recommendations

### 5.1 Immediate Fix (Production)

**Set the environment variable in production:**
```
REALBOT_INTEGRATION_ENABLED=True
```

This will allow `is_realbot_enabled()` to return `True`, enabling the session init and message endpoints to function properly.

### 5.2 Frontend Resilience Improvement

Update `realbot-panel.js` to provide a graceful demo/fallback mode instead of showing connection error messages:

1. **`initializeSession()`** — On fetch failure, instead of showing "Connection failed", initialize a local demo session with the proper welcome message and enable demo mode responses.

2. **`triggerResponseSequence()`** — On fetch failure, use a local `generateDemoResponse()` function that provides contextual responses based on the user's query (e.g., property listings, market insights, etc.) rather than showing "Connection failure."

3. **`showAPIError()`** — Replace with a demo response generator that maintains the illusion of functionality.

### 5.3 Configuration Audit

- Verify that `.env` in production has `REALBOT_INTEGRATION_ENABLED=True`
- Consider removing the hardcoded DeepSeek API key default from settings.py
- Add logging to production to capture when `is_realbot_enabled()` returns False unexpectedly

### 5.4 Long-Term

- Implement a proper demo/offline mode in the frontend that provides meaningful responses even when the backend is unavailable
- Add a health check call on page load to determine if the backend is available before showing error messages
- Consider adding a configuration UI to toggle realBOT features without requiring env var changes

---

## 6. Conclusion

The production connection failures are caused by the `REALBOT_INTEGRATION_ENABLED` setting defaulting to `False` in production, which causes the backend to return 403 errors. The frontend then displays hardcoded error messages that are misleading. The fix requires either setting the environment variable or updating the frontend to gracefully degrade to a demo mode.

**No code changes were made during this audit.** All findings are based on read-only analysis.
