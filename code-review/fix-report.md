# Fix Report — Propertism (01propertism)
# Current State as of 2026-05-08
**Branch:** main | **Author:** Astra (Claude Code Sonnet 4.6)

---

## SCCB-PROP-NRIASSIST-0805 — Google OAuth + NRI Assist Module

**Date:** 2026-05-08
**Approval:** Approved by Viji/Manthraa — SCCB-PROP-NRIASSIST-0805

---

### Part A — Google OAuth (django-allauth)

**File:** `requirements.txt`
Added `django-allauth==0.63.6`.

**File:** `realtor_project/settings.py`
- Added to INSTALLED_APPS: `allauth`, `allauth.account`, `allauth.socialaccount`, `allauth.socialaccount.providers.google`, `nri_assist.apps.NriAssistConfig`
- Added to MIDDLEWARE: `allauth.account.middleware.AccountMiddleware` (after AuthenticationMiddleware)
- Added AUTHENTICATION_BACKENDS (django + allauth)
- Added SOCIALACCOUNT_PROVIDERS with Google APP config reading from env vars
- Added LOGIN_REDIRECT_URL = '/dashboard/', LOGIN_URL, ACCOUNT_* settings
- ACCOUNT_EMAIL_VERIFICATION = 'none' (no verification email required for OAuth flow)

**File:** `realtor_project/urls.py`
- Added `path('accounts/', include('allauth.urls'))` for Google OAuth callback
- Added `path('dashboard/', user_views.dashboard, name='dashboard')` at root level
- Added `path('nri-assist/', include('nri_assist.urls'))`

**File:** `.env`
Added `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` as empty placeholders with instructions.
**Credentials not yet set** — Viji must obtain from Google Console and add to .env + EB properties.

**File:** `uilayers/templates/account/login.html`
Allauth login override. Prominent "Continue with Google" CTA (navy button with Google icon).
Email/password form hidden by default, shown via "sign in with email" toggle.
Extends base.html — full Propertism design system applied.

---

### Part B — Post-Login Dashboard

**File:** `uilayers/templates/users/dashboard.html`
Rewritten. Extends base.html. 4 quick action cards in 2×2 mobile / 4×1 desktop grid.
Cards: Post Property, Saved Properties, Contact Advisor, NRI Assist.
Design: dark navy + gold palette, Cormorant Garamond + Jost fonts.
No subscription/pricing language.

---

### Part C — NRI Assist Module

**New app:** `nri_assist/`

**Files created:**
- `nri_assist/__init__.py`
- `nri_assist/apps.py` — loads signals on ready()
- `nri_assist/models.py` — NRIService + NRIAssistEvent models
- `nri_assist/views.py` — nri_assist() view + log_cta() endpoint + _log_event() helper
- `nri_assist/urls.py` — `/nri-assist/` + `/nri-assist/log-cta/`
- `nri_assist/admin.py` — NRIServiceAdmin, NRIAssistEventAdmin
- `nri_assist/signals.py` — allauth user_logged_in signal → logs GOOGLE_LOGIN event
- `nri_assist/migrations/__init__.py`
- `nri_assist/migrations/0001_initial.py` — creates NRIService + NRIAssistEvent tables
- `nri_assist/management/commands/seed_nri_services.py` — seeds 19 services across 4 categories

**File:** `uilayers/templates/nri_assist/nri_assist.html`
4 service category cards (Property Care, Sale Assistance, Acquisition Assistance, Priority Coordination).
Services driven from NRIService model (DB). Falls back to "Services available on request" if empty.
"Request Assistance" CTA → /contact/. CTA click logged via /nri-assist/log-cta/.
Bottom strip: "Ready to talk?" → Contact an Advisor.

---

### Part D/E — Navigation

**File:** `uilayers/templates/components/_header-english.html`
Added "NRI Assist" link (`/nri-assist/`) to both desktop nav and mobile nav.

**File:** `uilayers/templates/components/_footer.html`
Added "NRI Assist" to footer services list and footer bottom links.

---

### Part F — Analytics

**Model:** `NRIAssistEvent` in `nri_assist/models.py`
Tracks: PAGE_VISIT, CTA_CLICK, ADVISOR_REQUEST, GOOGLE_LOGIN
Fields: event_type, user (FK nullable), service_category, metadata (JSON), ip_address, created_at
Admin: read-only view in Django admin with date_hierarchy.

**Signal:** `nri_assist/signals.py`
Listens to allauth `user_logged_in`. Creates GOOGLE_LOGIN event when social provider is Google.

---

### Part G — Future-Ready Architecture

NRIService model supports extension:
- `metadata` (JSONField) — extensible per-service data
- `icon` (CharField) — future icon mapping
- `sort_order` — manual ordering
- `is_active` — toggle services without deleting

App structure ready for: advisor assignment, ticket management, document vault, WhatsApp integration, NRI CRM.

---

### Part H — Environment Variables

Added to `.env`:
- `GOOGLE_CLIENT_ID` — placeholder (must be set)
- `GOOGLE_CLIENT_SECRET` — placeholder (must be set)

**Post-deploy steps for Viji:**
1. `pip install -r requirements.txt` (installs django-allauth==0.63.6)
2. `python manage.py migrate` (creates nri_assist + allauth tables)
3. `python manage.py seed_nri_services` (seeds 19 services)
4. Obtain GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET from Google Console
5. Add to .env (local) and EB environment properties (production)
6. In Django admin → Sites: set domain to `www.propertism.in`
7. No Social Application entry needed in admin (credentials come from SOCIALACCOUNT_PROVIDERS APP config via env vars)

---

## Code-Review Mirrors

- `requirements.txt` ✓
- `realtor_project/settings.py` ✓
- `realtor_project/urls.py` ✓
- `.env` ✓
- `uilayers/templates/account/login.html` ✓
- `uilayers/templates/users/dashboard.html` ✓
- `uilayers/templates/nri_assist/nri_assist.html` ✓
- `uilayers/templates/components/_header-english.html` ✓
- `uilayers/templates/components/_footer.html` ✓
- `nri_assist/` (full app) ✓

---

## Session 2026-05-15 — Google OAuth UX Fixes

**Date:** 2026-05-15
**Branch:** main
**Approved by Viji** — execution decisions

### Fix 1 — Direct Google OAuth from Auth Drawer

**File:** `realtor_project/settings.py`
Added `SOCIALACCOUNT_LOGIN_ON_GET = True`.

**Root cause:** allauth, by default, does not initiate OAuth on a GET request (CSRF safety measure). Clicking "Continue with Google" in the auth drawer navigated to `/accounts/google/login/` via GET, which allauth silently redirected to the login page. User had to click Google again from there.

**Fix:** `SOCIALACCOUNT_LOGIN_ON_GET = True` tells allauth to honour GET-initiated OAuth. Drawer button now goes directly to Google's account chooser — no intermediate stop.

---

### Fix 2 — "Sign Up Closed" on New User Google OAuth Callback

**File:** `users/adapters.py`
Added `is_open_for_signup` override to `AdminOnlySocialAccountAdapter`.

**Root cause:** `PropertismAccountAdapter.is_open_for_signup` returns `False` to block email/password signup (correct behaviour per SCCB-SEC-PRT-1510). However, allauth's `DefaultSocialAccountAdapter.is_open_for_signup` chains to the account adapter, so new Google OAuth users were also blocked — hitting the allauth "Sign Up Closed" page on callback.

**Fix:** Override `is_open_for_signup(request, sociallogin)` on `AdminOnlySocialAccountAdapter` to return `True`. Google registration stays open; email/password signup stays closed.

---

### Code-Review Mirrors (2026-05-15)

- `realtor_project/settings.py` ✓
- `users/adapters.py` ✓
