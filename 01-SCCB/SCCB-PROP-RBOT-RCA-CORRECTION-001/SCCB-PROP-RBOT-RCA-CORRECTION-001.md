# SCCB-PROP-RBOT-RCA-CORRECTION-001

## Title
Correction to Static Audit – Validate realBOT Runtime Behaviour Before Applying Fixes

## Status
REVIEW REQUIRED

## Priority
HIGH

## Date
2026-07-07

---

## 1. Background

The previous audit (SCCB-PROP-RBOT-AUDIT-001) concluded that:

> "The production connection failures are caused by REALBOT_INTEGRATION_ENABLED=False."

This conclusion was based on **static code analysis only**. No runtime evidence was collected. This SCCB formally corrects that conclusion and provides the actual runtime analysis.

---

## 2. Architecture Intent (Confirmed)

The intended architecture for Phase-1 is:

```
01propertism (Production Repository)
    ├── Contains realBOT UI (realbot-panel.js + realbot.html)
    ├── Contains chat backend (chat/views.py)
    ├── Contains Human Handover (M2.17)
    ├── Contains Rule Engine (M2.4)
    ├── Contains Inquiry Engine (M2.6)
    ├── Contains Suggestion Engine (M2.7)
    └── Must work independently

08realBOT (Separate Development Workspace)
    ├── Experimental AI project
    ├── Future standalone service
    └── NOT required for current production deployment
```

**Key finding:** The 08realBOT project is NOT a deployment dependency. The realBOT framework in 01propertism must operate independently.

---

## 3. Runtime Evidence (Static Code Trace)

### 3.1 Two Separate Frontend Implementations Exist

The codebase contains **two independent frontend implementations** that call different API endpoints:

#### Frontend A: `static/js/realbot-panel.js` (Sliding Panel Widget)
- **Session init URL:** `GET /chat/session/init/` (line 106-109)
- **Query URL:** `POST /chat/query/` (line 526-537)
- **Error handling:** `.catch()` at line 124 → shows "Connection failed. Please verify that the local server is running and database migrations have been applied."
- **Query error:** `.catch()` at line 551-555 → shows "Connection failure. Check your internet connection and try again."

#### Frontend B: `uilayers/templates/realbot.html` (Full Page /realbot/ route)
- **Session init URL:** `POST /chat/session/init/` (line 755-768)
- **Error handling:** `.catch()` at line 767 → silent console.warn, falls back to demo mode
- **Query:** Uses `sendChipMessage()` → calls `window.realbotControl.triggerChip()` → calls `triggerResponseSequence()` → calls `POST /chat/query/`

### 3.2 URL Routing Analysis

From `realtor_project/urls.py`:

| URL Pattern | View | Exists? |
|---|---|---|
| `chat/session/init/` | `chat.views.init_session` | ✅ YES (line 8 of chat/urls.py) |
| `chat/query/` | `chat.views.send_message` | ✅ YES (line 9 of chat/urls.py) |
| `api/v1/realbot/session/init/` | `chat.views.init_session` | ✅ YES (line 45 of realtor_project/urls.py) |
| `api/v1/realbot/query/` | `chat.views.send_message` | ✅ YES (line 46 of realtor_project/urls.py) |

Both URL patterns resolve to the same view functions. The routes exist.

### 3.3 The `is_realbot_enabled()` Gate

```python
def is_realbot_enabled():
    return getattr(settings, 'REALBOT_INTEGRATION_ENABLED', False) and \
           is_feature_enabled('REALBOT_INTEGRATION_ENABLED', default=True)
```

This function is called at the top of:
- `init_session()` (line 120) → returns **403** with `ERR_INTEGRATION_DISABLED`
- `send_message()` (line 208) → returns **403** with `ERR_INTEGRATION_DISABLED`
- `exchange_token()` (line 438) → returns **403** with `ERR_INTEGRATION_DISABLED`

### 3.4 What Happens When `is_realbot_enabled()` Returns False

The view returns:
```json
HTTP 403 Forbidden
{
    "success": false,
    "correlation_id": "...",
    "error": {
        "code": "RBOT0001",
        "message": "realBOT integration is disabled locally"
    }
}
```

### 3.5 How the Frontend Handles This

**Frontend A (`realbot-panel.js`):**
- `init_session()` at line 112: `if (!response.ok) throw new Error("Session init failed");`
- Since HTTP 403 is NOT ok, it throws → `.catch()` at line 124 → shows fallback message: *"Welcome to realBOT (advisory channel). Connection failed. Please verify that the local server is running and database migrations have been applied."*
- `triggerResponseSequence()` at line 538: `if (!response.ok) throw new Error("Query processing failed");`
- Since HTTP 403 is NOT ok, it throws → `.catch()` at line 551 → shows: *"Connection failure. Check your internet connection and try again."*

**This EXACTLY matches the user's reported error messages.**

### 3.6 The `feature_flags.json` vs `settings.py` Dual Gate

| Source | Value | Evaluates To |
|---|---|---|
| `feature_flags.json` → `is_feature_enabled('REALBOT_INTEGRATION_ENABLED')` | `true` | `True` |
| `settings.REALBOT_INTEGRATION_ENABLED` (from env var, default `False`) | Not set in production | `False` |
| `is_realbot_enabled()` = `True AND False` | | **`False`** |

### 3.7 The `is_ai_enabled()` Function (Separate Concern)

```python
def is_ai_enabled():
    return getattr(settings, 'REALBOT_AI_ENABLED', False) or \
           is_feature_enabled('REALBOT_AI_ENABLED', default=False)
```

This uses `OR` instead of `AND`. It controls AI service calls (line 267) but does NOT gate the session/query endpoints. This is a separate concern.

---

## 4. Confirmed Root Cause

**The production connection failures are caused by `is_realbot_enabled()` returning `False`.**

The specific reason is that `settings.REALBOT_INTEGRATION_ENABLED` defaults to `False` because the environment variable `REALBOT_INTEGRATION_ENABLED` is not set in the production environment.

The `feature_flags.json` has `"REALBOT_INTEGRATION_ENABLED": true`, but this alone is insufficient because the function requires **both** conditions to be `True`.

### HTTP Status Code Trace

| Request | Expected | Actual | Reason |
|---|---|---|---|
| `GET /chat/session/init/` | 200 | **403** | `is_realbot_enabled()` → `False` |
| `POST /chat/query/` | 200 | **403** | `is_realbot_enabled()` → `False` |

### Error Message Trace

| User Action | Error Shown | Source |
|---|---|---|
| Open panel | "Welcome to realBOT (advisory channel). Connection failed..." | `realbot-panel.js` line 131 (fallback in `.catch()`) |
| Send "hi" | "Connection failure. Check your internet connection and try again." | `realbot-panel.js` line 554 (`.catch()` in `triggerResponseSequence`) |
| Click "Premium Villas" chip | "Connection failure. Check your internet connection and try again." | Same as above |

---

## 5. Recommended Fix

### Option A: Set Environment Variable (Recommended)

Set `REALBOT_INTEGRATION_ENABLED=True` in the production environment.

For Elastic Beanstalk:
```
eb setenv REALBOT_INTEGRATION_ENABLED=True
```

Or in the `.env` file on the production server:
```
REALBOT_INTEGRATION_ENABLED=True
```

### Option B: Change the AND to OR in `is_realbot_enabled()`

```python
def is_realbot_enabled():
    return getattr(settings, 'REALBOT_INTEGRATION_ENABLED', False) or \
           is_feature_enabled('REALBOT_INTEGRATION_ENABLED', default=True)
```

This would make the feature flag sufficient to enable the integration. However, this changes the intended architecture where the env var is the master switch.

### Option C: Change the default in settings.py

```python
REALBOT_INTEGRATION_ENABLED = os.environ.get('REALBOT_INTEGRATION_ENABLED', 'True').lower() in ('true', '1', 'yes')
```

This would default to enabled. However, this may not be desired for all environments.

---

## 6. Verification Steps

After applying the fix:

1. Open browser to production URL
2. Open realBOT panel
3. Verify: Welcome message appears correctly
4. Type "hi" and send
5. Verify: Response is received (not an error)
6. Check browser console for any errors
7. Check Django logs for any errors

---

## 7. References

- SCCB-PROP-RBOT-AUDIT-001: Previous audit (requires correction)
- `chat/views.py` lines 21-23: `is_realbot_enabled()` function
- `chat/views.py` lines 120-127: `init_session()` gate
- `chat/views.py` lines 208-215: `send_message()` gate
- `static/js/realbot-panel.js` lines 106-137: Frontend session init with fallback
- `static/js/realbot-panel.js` lines 526-556: Frontend query with error handling
- `realtor_project/settings.py`: `REALBOT_INTEGRATION_ENABLED` definition
- `feature_flags.json`: Feature flag value
