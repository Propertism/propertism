# Future Recommendations — SCCB-PROP-RBOT-AUDIT-001

## Based on Read-Only Audit of realBOT Production Connection Failures

**Date:** 2026-07-07

---

## 1. Production Configuration

### 1.1 Environment Variable
Set `REALBOT_INTEGRATION_ENABLED=True` in the production environment. This is the single most impactful fix — it will enable the backend session init and message endpoints to function correctly.

### 1.2 Configuration Audit
- Verify all `REALBOT_*` environment variables are correctly set in production
- Consider adding a startup validation script that checks required env vars
- Add structured logging to capture when `is_realbot_enabled()` returns False

---

## 2. Frontend Resilience (realbot-panel.js)

### 2.1 Graceful Demo Mode
Replace hardcoded error messages with a proper demo/offline mode:
- On session init failure, initialize a local demo session with the proper welcome message
- On query failure, use a `generateDemoResponse()` function that provides contextual responses
- Maintain the chips and suggestion UI even in offline mode

### 2.2 Health Check on Load
Add a health check call on page load to determine backend availability before showing any error messages. If the backend is unavailable, silently switch to demo mode.

### 2.3 User-Friendly Messages
Replace technical error messages with user-friendly alternatives:
- "realBOT is operating in offline advisory mode" instead of "Connection failed"
- "Please try again shortly" instead of "Check your internet connection"

---

## 3. Backend Improvements

### 3.1 Remove Hardcoded API Key
The `DEEPSEEK_API_KEY` default value in `realtor_project/settings.py` (`'AIzaSyBAOA3xvBpa3FQF4l27hVh7-_5mlTR3zB0'`) appears to be a Google API key, not a DeepSeek key. Remove this default or replace with an empty string.

### 3.2 Feature Flag Consolidation
Consider consolidating the dual-gate mechanism (settings + feature_flags.json) into a single source of truth to avoid confusion.

### 3.3 Add CORS Headers
If the realBOT widget is loaded from a different domain, ensure CORS headers are properly configured.

---

## 4. Monitoring & Observability

### 4.1 Add Production Logging
Add specific log messages when:
- `is_realbot_enabled()` returns False
- Session init fails due to integration being disabled
- Message processing fails due to invalid session

### 4.2 Health Check Dashboard
Create a simple health check dashboard that shows:
- realBOT integration status (enabled/disabled)
- Database connectivity
- Last successful session init
- Error rate

---

## 5. Long-Term Architecture

### 5.1 Configuration UI
Consider adding an admin UI to toggle realBOT features without requiring environment variable changes.

### 5.2 Progressive Enhancement
Implement a progressive enhancement approach:
1. Static welcome message (always works)
2. Local demo responses (when backend is unavailable)
3. Full AI-powered responses (when all systems are operational)

### 5.3 Error Recovery
Add automatic retry logic with exponential backoff for transient failures.

---

## Priority Matrix

| Priority | Recommendation | Effort | Impact |
|----------|---------------|--------|--------|
| P0 | Set `REALBOT_INTEGRATION_ENABLED=True` in production | 5 min | Critical |
| P1 | Frontend graceful demo mode | 2-3 hours | High |
| P2 | Remove hardcoded API key default | 10 min | Medium |
| P3 | Add production logging | 1 hour | Medium |
| P4 | Health check dashboard | 4 hours | Low |
| P5 | Configuration UI | 8 hours | Low |
