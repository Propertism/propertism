# FUTURE_RECOMMENDATIONS.md

## SCCB-PROP-RBOT-RCA-CORRECTION-001

### Date
2026-07-07

---

## 1. Improve Error Messages in Frontend

**Current:** The frontend shows generic "Connection failure. Check your internet connection" for ALL HTTP errors (403, 404, 500, etc.).

**Recommendation:** Parse the actual error response from the backend and display it to the user. For example, if the backend returns `{"error": {"code": "RBOT0001", "message": "realBOT integration is disabled locally"}}`, the frontend should show this specific message instead of a generic one.

**File:** `static/js/realbot-panel.js` lines 538-555

## 2. Unify the Two Frontend Implementations

**Current:** There are two separate frontend implementations:
- `static/js/realbot-panel.js` (sliding panel widget on main site)
- `uilayers/templates/realbot.html` (full-page /realbot/ route)

These have different code paths, different error handling, and different API call patterns.

**Recommendation:** Consolidate into a single frontend module that both implementations can use.

## 3. Add Health Check Before Session Init

**Current:** The frontend calls `/chat/session/init/` directly without first checking if the backend is operational.

**Recommendation:** Call `/chat/health/` first. If it returns `integration_enabled: false`, show a meaningful message to the user explaining that the feature is currently disabled.

## 4. Resolve the Dual-Gate Architecture

**Current:** `is_realbot_enabled()` requires BOTH `settings.REALBOT_INTEGRATION_ENABLED` AND `feature_flags.json` to be `True`. This creates confusion about which is the authoritative source.

**Recommendation:** Choose one authoritative source:
- If env var is the master switch, remove the feature flag check from `is_realbot_enabled()`
- If feature flag is the master switch, remove the env var check from `is_realbot_enabled()`
- Document the chosen architecture clearly

## 5. Add Logging for Integration Gate

**Current:** When `is_realbot_enabled()` returns `False`, there is no log message explaining WHY.

**Recommendation:** Add debug logging:
```python
def is_realbot_enabled():
    settings_enabled = getattr(settings, 'REALBOT_INTEGRATION_ENABLED', False)
    feature_enabled = is_feature_enabled('REALBOT_INTEGRATION_ENABLED', default=True)
    logger.debug(f"realBOT gate: settings={settings_enabled}, feature_flag={feature_enabled}")
    return settings_enabled and feature_enabled
```
