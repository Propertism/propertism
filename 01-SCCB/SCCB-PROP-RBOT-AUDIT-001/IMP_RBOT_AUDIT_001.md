# Implementation Report — SCCB-PROP-RBOT-AUDIT-001

## Title: Read-Only Audit — realBOT Production Connection Failures

**Date:** 2026-07-07  
**Auditor:** Platform Integration Lead  
**Status:** COMPLETED (Read-Only Audit — No Code Changes)

---

## Summary

A comprehensive read-only audit was conducted to diagnose the realBOT production connection failures. The audit examined 11 files across the frontend, backend, routing, and configuration layers.

## Root Cause

The production connection failures are caused by the `REALBOT_INTEGRATION_ENABLED` setting defaulting to `False` in production. The `is_realbot_enabled()` function in `chat/views.py` (line 21-23) requires BOTH:
1. `settings.REALBOT_INTEGRATION_ENABLED = True` (defaults to `False` from env var)
2. `feature_flags.json` has `"REALBOT_INTEGRATION_ENABLED": true`

Since the environment variable is likely not set in production, the backend returns 403 errors, causing the frontend to display hardcoded error messages.

## Files Examined

| File | Lines | Purpose |
|------|-------|---------|
| `static/js/realbot-panel.js` | 636 | Frontend JS — session init & message handling |
| `chat/views.py` | 3228 | Backend views — session, message, health endpoints |
| `chat/urls.py` | 95 | Chat URL routing |
| `realtor_project/urls.py` | 129 | Project-level URL routing |
| `realtor_project/settings.py` | 717 | Django settings & feature flags |
| `feature_flags.json` | 7 | JSON feature flag configuration |
| `chat/constants.py` | 122 | Error codes & state constants |
| `chat/responses.py` | 21 | Standard API response builder |
| `chat/ai_service.py` | 165 | DeepSeek AI provider integration |
| `uilayers/templates/realbot.html` | 1360 | realBOT UI template |
| `.env.example` | 56 | Environment variable documentation |

## Key Findings

1. **Session Init Failure** — `initializeSession()` in `realbot-panel.js` calls `/chat/session/init/`. Backend returns 403 if `is_realbot_enabled()` is False. Frontend `.catch()` shows hardcoded "Connection failed" message.

2. **Message Send Failure** — `triggerResponseSequence()` calls `/chat/query/`. Without a valid session, backend returns 404. Frontend `.catch()` shows "Connection failure. Check your internet connection."

3. **URL Routing is Correct** — `/chat/session/init/` and `/chat/query/` resolve properly via `chat/urls.py`. No routing issues.

4. **DeepSeek API Key** — Hardcoded default `'AIzaSyBAOA3xvBpa3FQF4l27hVh7-_5mlTR3zB0'` in settings.py appears to be a Google API key, not a DeepSeek key. Not causing current errors since AI is disabled.

5. **Template Has Separate JS** — `realbot.html` has its own inline script with separate session init logic.

## Recommendations

### Immediate (Production Fix)
- Set `REALBOT_INTEGRATION_ENABLED=True` in production environment variables

### Frontend Resilience
- Update `realbot-panel.js` to provide graceful demo/fallback mode instead of error messages
- Add `generateDemoResponse()` function for offline query handling

### Configuration
- Remove hardcoded DeepSeek API key default from settings.py
- Add production logging for `is_realbot_enabled()` failures

## Conclusion

**No code changes were made.** This was a read-only audit. The fix requires either setting the production environment variable or updating the frontend to gracefully degrade to demo mode.
