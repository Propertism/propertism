# Fix Report — Propertism (01propertism)
# Current State as of 2026-05-21

---

## Session 2026-05-21 (Afternoon) — Open Items Clearance

**Date:** 2026-05-21
**Branch:** main
**Approved by Viji** — execution decisions

### Fix 1 — Company Logo 404 (Header)

**File:** `uilayers/templates/components/_header-english.html`
- Added `{% static '...' as logo_fallback_url %}` at top of file
- Dark logo `<img>` now uses conditional `src`: `company.logo.url` if set, else static fallback
- Added `onerror` handler so browser-side 404 also falls back to `propertism-logo.png`
- Handles both: empty logo field (no URL attempt), and missing file on EB (onerror recovery)

### Fix 2 — Blog 500 (Missing Template)

**Root cause:** `blog_post` view calls `render(request, "blog_post.html", context)` but template did not exist → `TemplateDoesNotExist` → 500.

**File created:** `uilayers/templates/blog_post.html`
- Extends `base.html`, dark navy/gold luxury aesthetic matching propertism.in design
- Hero area: category kicker, title (Cormorant Garamond), author, published date, optional featured image
- Two-column layout: article content (left) + sticky sidebar (right)
- Sidebar: related posts list + Contact Advisor CTA
- Mobile-first responsive (single column below 899px)
- SEO: custom `{% block meta_title %}` and `{% block seo_meta %}` with post title/excerpt

### Fix 3 — Property Slug URLs

**Files modified:**
- `properties/models.py` — added `slug = SlugField(max_length=255, unique=True, blank=True)`, `save()` override with uniqueness loop, `get_absolute_url()`
- `properties/migrations/0006_property_slug.py` — **SCCB-PROP-DEPLOY-01 rewrite** (see below)
- `properties/migrations/0007_property_slug_unique.py` — **new file** (see below)
- `properties/urls_web.py` — `<int:pk>/` → `property_detail_by_pk` (301 redirect); `<slug:slug>/` → canonical `property_detail`
- `properties/views.py` — `property_detail(request, slug)` uses `get_object_or_404(Property, slug=slug)`; new `property_detail_by_pk` issues permanent redirect; `create_inquiry` redirect updated to slug
- `content/sitemaps.py` — `PropertySitemap.location()` now returns `/properties/{obj.slug}/`

**Templates updated (5 files):**
- `uilayers/templates/properties/list.html`
- `uilayers/templates/components/_property-card.html`
- `uilayers/templates/home/sections/_properties.html`
- `uilayers/templates/components/_lp_listings.html`
- `uilayers/templates/inquiries/dashboard.html`

All `{% url 'property_detail' property.pk %}` → `{% url 'property_detail' property.slug %}`.
Hardcoded `/properties/{{ property.pk }}/` in `_lp_listings.html` also fixed to `{% url ... %}`.

**Migration result (local):** `properties.0006_property_slug... OK`, `properties.0007_property_slug_unique` pending prod deploy.

**Backward compatibility:** Old `/properties/<pk>/` URLs → 301 permanent redirect to `/properties/<slug>/`. External links and Google-indexed URLs will self-heal.

---

### SCCB-PROP-DEPLOY-01 — Deploy Failure + Migration Split

**Date:** 2026-05-21
**Approved by Viji/Manthraa — SCCB-PROP-DEPLOY-01**

**Root cause (original):** Migration `0006_property_slug` added a `SlugField` (which has `db_index=True` by default) via `AddField` AND made it `unique=True` via `AlterField` in the same migration. Both operations independently appended a `CREATE INDEX _like` (varchar_pattern_ops) to `deferred_sql`. Django's `__exit__` executes deferred SQL sequentially — first creation succeeded, second creation raised `DuplicateTable`. This fails on any database state including clean. The `RunSQL DROP INDEX IF EXISTS` patch (commit `6bac2f4`) was diagnosing a DB state problem (orphaned index) that was real but secondary; the double-queue was the actual blocker.

**Fix — split into two migrations:**

`0006_property_slug.py` (rewritten):
- `RunSQL("DROP INDEX IF EXISTS properties_property_slug_f3b16024_like;")` — one-shot cleanup for 2026-05-21 prod deploy drift, no-op on clean environments
- `AddField(slug, blank=True, null=True)` — column only, no populate, no unique

`0007_property_slug_unique.py` (new):
- `RunPython(populate_slugs)` — verbatim from old 0006
- `AlterField(slug, blank=True, unique=True)` — matches model definition

**Why this works:** Each migration runs in its own transaction with its own `deferred_sql` list. 0006's `__exit__` creates the `_like` index once (from AddField). 0007's `AlterField` drops and recreates it as part of the db_index → unique transition — no double-queue.

**Rollback trigger per SCCB:** If 0006 passes but 0007 fails on unique constraint (slug collision in real data) → do not patch and retry. Report colliding slugs. Fix is in `populate_slugs` logic, separate SCCB.

### Fix 4 — GA4 Wired

**File:** `uilayers/templates/base.html`
- Added Google Analytics GA4 gtag.js snippet in `<head>` above font preconnects
- Measurement ID: `G-WZCH8BV34J`
- All pages now tracked on every page load — page views, sessions, users, traffic sources

**Code-Review Mirror:** `code-review/base.html` ✓

### Open Items (deferred)

1. **WhatsApp access token expired** — parked. Viji to generate permanent System User token in Meta Business Suite when ready.
2. **Blog 500 errors** — fixed (missing template created). Monitor live.
3. **fb:app_id** — optional. Create a Facebook App at developers.facebook.com → share App ID → 10-min code change. No functional loss without it.
4. **Company logo 404 on EB** — code fallback applied. Underlying fix: re-upload logo at `/admin/content/companyinfo/`.

### Code-Review Mirrors

- `code-review/_header-english.html` ✓
- `code-review/blog_post.html` ✓
- `code-review/models.py` ✓
- `code-review/0006_property_slug.py` ✓
- `code-review/urls_web.py` ✓
- `code-review/views.py` ✓
- `code-review/sitemaps.py` ✓

---

## Session 2026-05-21 — OG v5, Inquiry Delete, Admin Tightening

**Date:** 2026-05-21
**Branch:** main
**Approved by Viji** — execution decisions

### OG Image v5 — LinkedIn & WhatsApp
- `og-propertism-v5.png` (1200×630 Chennai skyline, Cinzel headline, proof pills) promoted as default OG image
- `seo_tags.py` updated — `og_image` now points to `/static/images/og-propertism-v5.png`
- Validated: Facebook Sharing Debugger (200, full card) + LinkedIn Post Inspector (full-bleed confirmed)
- Deployed to EB + pushed to GitHub — commit `a8ff3cd`

### Inquiry Delete — Staff Console + Django Admin
- New view: `inquiry_delete` in `properties/views.py` (`@inquiries_staff_required`, `@require_POST`)
- New URL: `/<id>/delete/` in `properties/urls_inquiries.py`
- Staff console: trash button in table Actions column, detail panel, and mobile lite row
- Confirm: uses `inq-confirm-overlay` (not browser native) — Delete button red `#DC2626`
- Django admin: `delete_inquiry_view` + URL in `properties/admin.py`, trash icon per row in changelist
- Commits: `e9ab0a2`, `5a776cf`

### Admin Changelist — Table Tightening + Search Fix
- `table-layout: fixed` with explicit column widths — horizontal scrollbar eliminated
- Reduced padding, font sizes, truncation with ellipsis on name/email/property
- Search icon: replaced `&#x1F50D;` emoji with 14px SVG lens — overlap with placeholder resolved
- Commits: `ad8a4f7`, `5d47110`

### Code-Review Mirrors
- `code-review/seo_tags.py` ✓
- `code-review/views.py` ✓
- `code-review/urls_inquiries.py` ✓
- `code-review/admin.py` ✓

---

## SCCB-002 - Inquiries Console UI Remediation (Desktop List View)

**Date:** 2026-05-19  
**Approval:** Approved by Viji - SCCB-002

### Target page
- /inquiries/ desktop list view only
- Not the Django admin inquiries changelist

### Files Modified
- uilayers/templates/inquiries/dashboard.html
  - Reworked the desktop list-view structure around SCCB-002 instead of the earlier mixed desktop/board chrome
  - Hid the dead board toggle from the reviewed surface
  - Rebuilt the listing header into a single panel header with title, scope text, result count, and updated timestamp
  - Replaced the row <select> status control with an inline status trigger + anchored action menu
  - Replaced input-like contact rendering with plain email/phone actions
  - Made row actions permanently visible with icon-only buttons and disabled states
  - Added loading shell markup, offline banner, improved empty states, and keyboard row hooks
  - Replaced the public-site inquiries header treatment with a console-specific wordmark and explicit Sign out button
- static/css/inquiries.css
  - Rewrote the desktop inquiries console styling to match SCCB-002
  - Compact stat row: reduced tile height, smaller numerals, consistent alignment
  - Search field: corrected icon placement and input left padding
  - Sidebar tree: Timeline label, clearer indentation, right-aligned counts, active-row treatment
  - Table: denser row rhythm, full-row hover/focus state, proper ACTIONS column styling
  - Status control: dot + text trigger, lightweight dropdown, no decorative filled pill
  - Added loading shimmer rows, offline banner, bottom-right toast, and refined sign-out styling

### SCCB-002 items addressed in this pass
- #1 Exit button/sign-out treatment
- #2 Stats chips reduced to compact stat row
- #3 Search icon overlap bug
- #4 Removed emoji from the reviewed desktop list surface
- #5 Inline status editing via anchored dropdown
- #6 Actions column always visible with header
- #7 Status visual weight reduced to dot + text
- #8 Tighter row density and row hover/focus states
- #9 Removed input-field style contact rendering from table rows
- #10 Sidebar hierarchy tightened and relabelled to Timeline
- #11 Listing/table header structure unified
- #12 Spacing/alignment pass across header, stats, chips, and rows
- #13 Dead board toggle hidden from the reviewed page
- #14 Added data freshness timestamp
- #15 Added visible loading shell and offline/error surfaces
- #16 Added keyboard support for /, Enter, Esc, ArrowUp, ArrowDown
- #17 Added clearer empty-state copy and treatment

### Verification
- python manage.py check - passed
- Browser verification against /inquiries/ is still pending in my session because the automation tab was redirected to /admin/login/?next=/inquiries/ when unauthenticated

### Code-Review Mirrors
- code-review/dashboard.html - synced
- code-review/inquiries.css - synced

### Follow-up: Header Branding Adjustment
- Restored the Propertism logo in the `/inquiries/` header instead of text-only branding
- Reduced the adjacent `Propertism · Inquiries` label size to sit closer to the home-page header standard
- Kept the existing home-page logo image behavior and appended the inquiries label beside it

### Follow-up: Move Page Context To Header
- Moved `Inquiries / All inquiries / Showing N of M / Updated ...` into the fixed header area beside the logo
- Removed the duplicated body-level listing header so the page context appears only once
- Kept the `Updated ...` stamp bound to the same `inqUpdatedStamp` JS refresh point

### Follow-up: Remove Header Brand Text
- Removed the extra `Propertism · Inquiries` text beside the logo
- Left the page context summary as the only header text in that area

### Follow-up: Header Controls + Flat Surface Cleanup
- Moved Refresh into the top-right header tools beside Sign out and removed the lower action-bar refresh control
- Switched both header controls to icon-only treatment with no text label or boxed background
- Corrected the search icon/input spacing so the lens no longer collides with the placeholder text
- Flattened rectangular UI surfaces across the inquiries console by removing rounded corners from the search field, stat chips, table shell, dropdown panels, action buttons, detail cards, dialog, toast, and mobile utility buttons

### Follow-up: Move Page Context Beside Metrics
- Moved `Inquiries / All inquiries / Showing N of M / Updated ...` out of the logo/header area and into the action bar immediately beside the metric chips
- Converted the context block from JS-injected header content to server-rendered action-bar markup
- Kept `inqUpdatedStamp` unchanged so refresh/status updates still update the visible freshness label

### Follow-up: Branded Staff Gate For Inquiries
- Replaced Django admin login fallback with `/inquiries/login/` for the Inquiries console
- Added `inquiry_staff_login` using Django `authenticate()`/`login()` while still requiring `is_staff`
- Added a Propertism staff login page and Ctrl+I modal for non-staff/anonymous visitors
- Kept the staff-only FAB + pending badge for already authenticated staff users
- Verified anonymous `/inquiries/` now redirects to `/inquiries/login/?next=/inquiries/`, not `/admin/login/`

### Follow-up: Remove Duplicate Chip Counts
- Removed numeric counts from the status filter chips (`All`, `Pending`, `Contacted`, `Closed`)
- Kept the metric chips as the single source for totals (`Total`, `Pending`, `Contact`, `This Wk`)

### Follow-up: Align Status LOV
- Updated the metric row to use the same inquiry status values as Django admin: `Pending`, `Contacted`, `Closed`
- Replaced `This Wk` with `Closed` and renamed `Contact` to `Contacted`

### Follow-up: Premium Mail Composer
- Added an inline reply composer below the inquiries list for leads with an email address
- Email links and email action buttons now populate the composer instead of launching a bare `mailto:` immediately
- Composer pre-fills recipient, subject, and a Propertism Advisory response draft using the selected lead/property context
- Added actions to open the draft in the local mail client, copy the complete draft, or clear the composer
- Kept the visual treatment premium, quiet, and text-only with no emojis

### Follow-up: Full Compose Surface
- Reworked the composer to match a modern mail composition surface: `Recipient`, `CC`, `Subject`, `Content`, `Attachments`
- Added recipient chip with initial, remove control, attachment tool row, Save Draft, Schedule, and Send actions
- Save Draft stores the current draft in local browser storage; Schedule/attachment controls are staged with clear future-integration messaging
- Send continues to launch the local mail client via `mailto:` until SMTP-backed sending is approved

### Follow-up: SMTP Send + Focused Composer Mode
- Composer is hidden by default and opens as the primary Zone C workspace only when an email action is clicked
- Added `/inquiries/send-reply/` staff-only POST endpoint using Django `EmailMessage`, `DEFAULT_FROM_EMAIL`, and configured SMTP settings
- Send now posts to Django and sends from the configured Propertism email instead of opening a local `mailto:` draft
- Successful send marks a pending inquiry as `Contacted` and syncs the row/status UI
- Verified endpoint with Django locmem email backend: one outbound message created with To and CC

### Follow-up: Composer Send JSON/CSRF Hardening
- Added a template-rendered CSRF token inside the composer form because CSRF cookies are HTTP-only in settings
- Updated `getCsrf()` to prefer the hidden form token before falling back to the cookie
- Hardened the Send fetch handler to parse response text safely and show a clear session/server error instead of `Unexpected token '<'`

---

## SCCB-19052026/A2 — Inquiries Lite (Mobile Surface)

**Date:** 2026-05-19
**Approval:** Approved by Viji — SCCB-19052026/A2

### Files Modified
- `static/css/inquiries.css`
  - Replaced old mobile `@media (max-width:899px)` block: now hides `.inq-actionbar` + `.inq-body`, shows `.inq-lite`, sets `height:auto` + `overflow-y:auto` on `.main-content`
  - Added full `.inq-lite-*` component system (chip bar, rows, expand, action buttons, empty state, SOP note)
- `uilayers/templates/inquiries/dashboard.html`
  - Inserted `.inq-lite` section (filter chips, row list, SOP note) between `/inq-body` and confirm dialog
  - Inline redirect script: first mobile visit with no params → `?status=pending`
  - New `<script>` block: `liteToggleExpand`, `liteDone`, `confirmStatusChange` override, `cancelStatusChange` override
  - Reuses existing `postStatus`, `openWhatsApp`, confirm overlay, undo toast

### Mobile Lite features (< 900px)
- CSS-first split: desktop workspace hidden, lite view shown
- Default filter: Pending (auto-redirect on first visit)
- Chips: Pending / All
- Row: status dot + name + property/time + email + expand-on-tap for message
- Action buttons (44px): WhatsApp (via openWhatsApp JS), Call (tel:), Done/Close
  - Phone null → WA + Call disabled at 40% opacity
  - Pending → Done → contacted (optimistic + undo toast + row fades)
  - Contacted → Close → confirm dialog → closed
- SOP note: "For full inquiry management, open on desktop."
- Empty states: "All clear. No pending inquiries." / "No inquiries yet."

---

## SCCB-19052026-1/A1 — Nav Suppression on Inquiries Console

**Date:** 2026-05-19
**Approval:** Approved by Viji — nav suppression directive

### Files Modified
- `static/css/inquiries.css` — added `body.inq-app` scoped rules to hide `.main-nav`, `.mobile-menu-toggle`, `.mobile-nav`, `.mobile-menu-backdrop`, `#typoToggle`, `.nav-profile-trigger-name`, `.nav-profile-chevron`; added `.inq-exit-btn` style (gold-border, light text, dark nav background)
- `uilayers/templates/inquiries/dashboard.html` — added inline script that injects `<a class="inq-exit-btn" href="/">← Exit</a>` into `.header-v4-tools` before the profile wrapper

### Result
On `/inquiries/*`: all public nav links hidden; only the profile avatar/initial (click to sign out) and an Exit button remain visible in the header.

---

## SCCB-19052026-1 Phase 2 — Board View + Drag-and-Drop + Swipe

**Date:** 2026-05-19
**Approval:** Approved by Viji — SCCB-19052026-1 Phase 2

### Files Modified
- `properties/views.py` — added `board_columns` to context
- `uilayers/templates/inquiries/dashboard.html` — added view toggle to Zone A, wrapped list in `#inqListView`, added `#inqBoardView` with three columns (Pending/Contacted/Closed) and draggable cards, added all Phase 2 JS (setView, drag-and-drop, board column counts, mobile swipe-right)
- `static/css/inquiries.css` — added view toggle styles, board column and card styles, drag visual feedback, mobile swipe row transition

### Phase 2 features
- View toggle (☰ List / ▦ Board) in Zone A — desktop only
- localStorage persistence: `propertism.inquiries.view`
- Board: three columns, cards draggable with HTML5 DnD API
- Drop → status POST + optimistic move + undo toast
- Closed drop → confirmation dialog (same as table)
- Mobile swipe-right on list row → Mark Contacted (pending rows only)
- Board hidden on mobile (< 900px)

---

## SCCB-19052026-1/A1 — Inquiries Dashboard Amendment (Workspace Shell + Light Theme)

**Date:** 2026-05-19
**Approval:** Approved by Viji/Manthraa — SCCB-19052026-1/A1

### Files Modified
- `properties/views.py` — inquiries_dashboard fully rewritten: tree query (one GROUP BY query), date/q/status filters, tree_data nested dict built from TruncDate/ExtractYear/ExtractMonth
- `properties/models.py` — added Meta.indexes: `inquiry_created_idx` + `inquiry_status_created_idx` (composite)
- `uilayers/templates/base.html` — FAB guard updated: `{% if not request.path|slice:":11" == "/inquiries/" %}`, inline FAB CSS added so it works without loading inquiries.css on public pages

### Files Created
- `uilayers/templates/inquiries/base_app.html` — standalone workspace shell (does NOT extend public base.html); fonts, inquiries.css, top bar (Propertism · Inquiries wordmark + user + sign-out)
- `static/css/inquiries.css` — complete rewrite: light theme tokens (--bg-canvas, --ink-primary, --accent-gold, --status-*-bg/ink), three-zone layout (CSS flex), Zone A/B/C, status as soft pill (not dark-navy bordered), mobile sidebar drawer
- `uilayers/templates/inquiries/dashboard.html` — complete rewrite: extends base_app.html, Zone A (filter chips + search + refresh), Zone B (tree: year > month > date, server-rendered, collapse/expand JS), Zone C (stats + listing + detail panel sliding within Zone C)

### Migration
- `properties/migrations/0005_inquiry_indexes.py` — two non-breaking indexes

### Key behaviour
- Public propertism.in: dark navy + gold unchanged
- /inquiries/* routes: standalone light workspace, no public chrome
- URL state: ?status=pending&date=2026-03-18&q=john — fully shareable
- Ctrl+I on inquiries page: focuses search input (not navigation)
- FAB: hidden on /inquiries/* (guard in base.html)

---

## SCCB-19052026-1 — Inquiries Dashboard (Phase 1)

**Date:** 2026-05-19
**Approval:** Approved by Viji/Manthraa — SCCB-19052026-1

### Files Modified
- `realtor_project/settings.py` — SESSION_COOKIE_AGE → 8h, added SESSION_EXPIRE_AT_BROWSER_CLOSE + SESSION_SAVE_EVERY_REQUEST globally
- `properties/views.py` — added `inquiries_dashboard`, `inquiry_status_update`, `inquiry_pending_count` views + imports
- `realtor_project/urls.py` — added `path('inquiries/', include('properties.urls_inquiries'))`
- `uilayers/templates/base.html` — added staff-only FAB (fixed bottom-right, gold envelope, pending badge) + Ctrl+I shortcut + 60s badge polling

### Files Created
- `properties/urls_inquiries.py` — 3 URL patterns: GET /inquiries/, POST /inquiries/<id>/status/, GET /inquiries/pending-count/
- `static/css/inquiries.css` — full dashboard styles (dark navy, gold, Cormorant/Jost)
- `uilayers/templates/inquiries/dashboard.html` — full Phase 1 dashboard template with stats strip, list table, detail slide-out, status workflow, quick actions, undo toast

### Auth: @staff_member_required on all 3 views. FAB + Ctrl+I guarded by {% if user.is_staff %}.
### Schema: ZERO migrations. Existing Inquiry model, no changes.

---
# Previous State as of 2026-05-08
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

---

## Session 2026-05-18 — Enterprise Inquiry Admin + SMTP + Dual-Email + WhatsApp

**Date:** 2026-05-18
**Branch:** main
**Approved by Viji** — execution decisions

### SCCB-DE-027 — EB Settings & SMTP Audit

Confirmed EB uses `realtor_project.settings` (not `settings_production.py`) via `.ebextensions/01_django.config`.
SMTP vars were absent from EB env — Viji added `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `ADMIN_EMAIL` to EB console this session.

### Email Routing — Dual Inbox

**File:** `realtor_project/settings.py`
Added `ADMIN_EMAILS = list({ADMIN_EMAIL, _extra_recipients})` — deduped set of `info@propertism.in` + `propertism.tamil@gmail.com`.
Gmail SMTP configured; reads credentials from EB env vars.

**File:** `content/views.py`
Updated `send_admin_notification()`, `send_rfq_notification()`, `send_landing_lead_notification()` — all use `recipient_list=settings.ADMIN_EMAILS`.

### WhatsApp Confirmed

`send_rfq_notification()` already calls `send_whatsapp_notification()`. EB vars `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_ADMIN_PHONE`, `WHATSAPP_PHONE_ID` confirmed present. No code change needed.

### Enterprise Inquiry Admin

**File:** `properties/admin.py`
Full `InquiryAdmin` rewrite:
- `changelist_view()` — custom queryset with search (Q objects), status filter, year/month filter, sort asc/desc, pagination (25/page)
- `set_status_view()` — AJAX POST endpoint; updates DB, returns `{ok, status, display}` JSON
- `export_csv_view()` — streams CSV honouring all active filters
- `get_urls()` — registers `set-status/` and `export-csv/` admin URLs

**File:** `uilayers/templates/admin/properties/inquiry/change_list.html` (new)
Enterprise custom admin template:
- Header bar: title + Total/Pending/Contacted/Closed inline chips + search input + Export CSV + Add Inquiry
- Year/Month filter chips from `all_qs.dates()`
- Table: # / Name / Email / Phone / Property / Message / Status badge / Submitted (sort toggle ▲▼) / Update Status dropdown
- AJAX status update via fetch POST + toast notification
- Pagination controls
- Mobile: `.hide-mobile` columns collapse at 900px

### UI Fixes

- Double title removed: `{% block content_title %}{% endblock %}`
- Column headers: dark navy text on `#F1F5F9` light gray (not white-on-navy)
- Phone as separate column
- Single-row layout: `white-space: nowrap` on all `td`
- Submitted: `d M Y, H:i` single line format
- Sort toggle on Submitted `<th>`; `current_sort` passed in context
- Stats cards moved from separate grid row into header bar inline chips
- Search moved from separate toolbar into header bar; toolbar row removed

### Code-Review Mirrors (2026-05-18)

- `properties/admin.py` ✓
- `inquiry_change_list.html` ✓

---

## Session 2026-05-18 (Evening) — EB Recovery, WhatsApp, UI, Flags, SEO Audit

**Date:** 2026-05-18
**Branch:** main
**Approved by Viji** — execution decisions

### Fix 1 — EB Deployment Restored (Health Red → Green)

**Root cause A:** `collectstatic --clear` in `Procfile` ran as `webapp` user on root-owned static files → `PermissionError` killed gunicorn before it started.
**Fix:** Removed collectstatic from `Procfile`. Now runs only in container_commands (root) and postdeploy hook.

**Root cause B:** Corrupt `tflw` entry in `/opt/elasticbeanstalk/deployment/env` line 19 caused all 4 postdeploy hooks to fail under `set -euo pipefail`.
**Fix:** Added `|| true` to env file sourcing line in all 4 hooks.

**Files:** `Procfile`, `.platform/hooks/postdeploy/00_collectstatic_current.sh`, `01_fix_db_permissions.sh`, `02_bootstrap_if_db_looks_empty.sh`, `03_repair_stale_customer_reviews.sh`

---

### Fix 2 — WhatsApp API Version + Logging

**File:** `content/views.py`
Bumped Meta Cloud API `v17.0` → `v21.0` (v17.0 deprecated, ~2-year lifecycle).

**File:** `realtor_project/settings.py`
Added `content` logger to Django LOGGING config — WhatsApp errors from `send_whatsapp_notification` now surface in EB `web.stdout.log`.

**Root cause confirmed from live logs:** Error code `190` (OAuthException) — expired access token.
**Pending (no code change):** Viji to generate permanent System User token in Meta Business Suite → update `WHATSAPP_ACCESS_TOKEN` EB env var.

---

### Fix 3 — Contact Section Icon Cleanup

**File:** `uilayers/templates/home/sections/_contact.html`
Removed Facebook, Instagram, YouTube, Twitter/X icon blocks.

**File:** `static/css/v4-contact.css`
Removed `border-radius`, `background`, `border` from `.hf-icon-link` — circle backgrounds gone.
Remaining icons: Maps, Phone, WhatsApp, LinkedIn.

---

### Fix 4 — World Clock Flag Icons

**Investigation finding:** `_world_clock_widget.html` is never included in any page template — it is unused dead code. All flag attempts targeting it had no visible effect.

**Actual widget:** Hardcoded `world-clock-strip` inside `_footer.html` (lines 84–134).

**Fix:** Added `<img src="cdn.jsdelivr.net/.../XX.svg">` tags to 4 timezone label spans in `_footer.html`.
**CSS:** Added `.world-clock-flag` (18×13px, border-radius, box-shadow) to `v4-footer.css`.
**CSS:** Updated `.world-clock-label` to `display: flex; align-items: center; gap: 5px` for inline flag alignment.

**Files:** `uilayers/templates/components/_footer.html`, `static/css/v4-footer.css`

---

### Audit — SEO Tags

All implemented and confirmed live:
- `seo_meta` tag (title, description, keywords, OG, Twitter Card, canonical) — on every page via `base.html`
- `organization_schema` (RealEstateAgent JSON-LD) — every page
- `property_schema` (Residence JSON-LD)
- `service_schema` (Service JSON-LD on landing pages)
- `faq_schema` (FAQPage JSON-LD)
- `breadcrumb_schema` (BreadcrumbList JSON-LD)
- `sitemap.xml` live at `propertism.in/sitemap.xml` (StaticViewSitemap, PropertySitemap, BlogSitemap, LandingPageSitemap)

**Gap found:** Property URLs use `/properties/<pk>/` (not slug). SEO-weak. Model has `slug` field. Fix deferred to next session.

---

### Audit — GA4

No Google Analytics tracking code in `base.html`. Zero data being collected.
**Pending:** Viji to create GA4 property → share Measurement ID → Astra adds gtag snippet.

---

### Open Items Carried Forward

1. WhatsApp: Update `WHATSAPP_ACCESS_TOKEN` in EB (expired token, code 190)
2. Google Search Console: Add TXT record in GoDaddy DNS → verify
3. GA4: Viji shares Measurement ID → Astra adds to `base.html`
4. Property slug URLs: `/properties/<pk>/` → `/properties/<slug>/`
5. Blog 500 errors: `/blog/NRI-Property-Sale-in-India/` — not investigated
6. Company logo 404: `propertism-logo-official_A7SQorH.png` missing from EB
7. `_world_clock_widget.html`: Unused template with dead code — archive or wire-up decision needed

### Code-Review Mirrors (2026-05-18 Evening)

- `Procfile` ✓
- `00_collectstatic_current.sh` ✓
- `01_fix_db_permissions.sh` ✓
- `02_bootstrap_if_db_looks_empty.sh` ✓
- `03_repair_stale_customer_reviews.sh` ✓
- `content/views.py` ✓
- `realtor_project/settings.py` ✓
- `static/css/propertism-styles.css` ✓
- `static/css/v4-contact.css` ✓
- `static/css/v4-footer.css` ✓
- `static/js/world-clock-widget.js` ✓
- `uilayers/templates/components/_footer.html` ✓
- `uilayers/templates/components/_world_clock_widget.html` ✓
- `uilayers/templates/home/sections/_contact.html` ✓
