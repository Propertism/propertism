# Session: SEO Authority & Conversion Execution
**Date:** June 15, 2026 — 23:45 IST
**Session IDs:** SCCB-PROP-SEO-AUTHORITY-CONVERSION-PHASE3-1506 + SCCB-PROP-SEO-CONTENT-AUTHORITY-EXECUTION-1506 + SCCB-PROP-SEO-PHASE4-RANKING-EXECUTION-1506
**Type:** SEO Enhancement + CRO Optimization + Content Authority + Ranking Acceleration
**Priority:** P0/P1 – Critical

---

## Session Summary

Two back-to-back tickets executed in a single session. Phase 3 delivered the audit framework, quality hardening controls, GA4 analytics, and the NRI Knowledge Hub architecture. The Execution ticket built on those foundations by adding the Phase-A content seeder, a fast static audit command, and the monthly monitoring framework.

---

## Completed Tasks

### SCCB-PROP-SEO-AUTHORITY-CONVERSION-PHASE3-1506

#### ✅ 1. pSEO Quality Audit Framework
- **File created:** `content/pseo_quality.py`
  - Single-source configurable thresholds: `PSEO_MIN_WORD_COUNT = 500`, `PSEO_NOINDEX_WORD_COUNT = 200`
  - `classify_page()` function returning `INDEX` / `REVIEW` / `NOINDEX` with flags
  - Used by both the audit command and the `seo_meta` template tag

- **File created:** `content/management/commands/audit_pseo_quality.py`
  - Command: `python manage.py audit_pseo_quality`
  - Renders all pages via Django `RequestFactory` (requires DB)
  - Extracts: title, meta description, H1, canonical URL, word count, structured data, internal link count
  - Runs duplicate detection across all pages
  - Classifies every page as INDEX / REVIEW / NOINDEX
  - Writes `reports/pseo_quality_audit.csv`
  - Options: `--output`, `--city`, `--summary-only`

#### ✅ 2. Quality Hardening — Conditional noindex
- **File modified:** `uilayers/templates/seo/meta_tags.html`
  - Renders `<meta name="robots" content="noindex,follow">` when `noindex=True`
  - Falls back to `index, follow` for all other pages
  - Evidence-based: only thin pages affected, no blanket implementation

- **File modified:** `content/templatetags/seo_tags.py`
  - Imports `classify_page` from `content/pseo_quality.py`
  - Reads `_pseo_word_count` from template context
  - Passes `noindex=True` to `meta_tags.html` for pages below the noindex threshold

- **File modified:** `content/views_landing.py`
  - Injects `_pseo_word_count` into landing page context (approximated from `intro` + `seo_content` + `description` config fields)
  - Enables the noindex gate to fire correctly per page

#### ✅ 3. GA4 Conversion Analytics
- **File created:** `static/js/ga4-conversion.js`
  - Tracks 5 conversion events against GA4 Property `G-WZCH8BV34J`:
    - `whatsapp_click` — all WhatsApp links and floating button
    - `phone_call_click` — all `tel:` links
    - `contact_form_submit` — lead forms, contact forms, NRI assist forms
    - `resource_hub_click` — blog links, resource links, guide links
    - `newsletter_subscribe` — newsletter form submissions
  - Every event captures: `page_url`, `page_type`, `service_intent`, `city_context`, `event_timestamp`
  - Context read from body `data-*` attributes already set by `landing_page.html`

- **File modified:** `uilayers/templates/base.html`
  - Loads `ga4-conversion.js` globally for all page types

- **File modified:** `uilayers/templates/landing_page.html`
  - Loads `ga4-conversion.js` on landing pages

#### ✅ 4. NRI Knowledge Hub Architecture
- **File created:** `documents/NRI_KNOWLEDGE_HUB_ROADMAP.md`
  - 8 content clusters with pillar + spoke structure
  - Bidirectional internal linking rules (5 rules)
  - 4-phase publishing sequence (Phase A through D, 26 weeks)
  - Tier 1 / Tier 2 / Tier 3 keyword opportunity tables
  - 50–100 article roadmap anchored to core service landing pages
  - Production constraints and success metrics

#### ✅ 5. SEO Blocker Assessment
- **File created:** `documents/SEO_BLOCKER_ASSESSMENT.md`
  - 12-section audit covering all 9 required areas
  - Ranked blocker table (10 items, Critical → Low)
  - Immediate action item list (6 items, ranked by impact)
  - GSC validation checklist
  - GA4 DebugView validation instructions
  - SEO-to-Lead measurement framework with funnel diagram

#### ✅ 6. Reports Directory
- **Directory created:** `reports/`
  - Output target for `pseo_quality_audit.csv` and `pseo_config_analysis.csv`

---

### SCCB-PROP-SEO-CONTENT-AUTHORITY-EXECUTION-1506

#### ✅ 7. Knowledge Hub Phase-A Content — 10 Articles Seeded
- **File created:** `content/management/commands/seed_knowledge_hub_phase_a.py`
  - Command: `python manage.py seed_knowledge_hub_phase_a`
  - Seeds to drafts by default; `--publish` flag to go live
  - Safe to re-run: skips existing slugs
  - All 10 articles are 1,800–2,500 words, E-E-A-T compliant, with H2/H3 structure, FAQ sections, and internal links to service pages

| # | Slug | Category | Words (approx) |
|---|------|----------|----------------|
| 1 | `nri-property-management-chennai-complete-guide` | nri | 2,100 |
| 2 | `how-nris-can-sell-property-in-india-from-abroad` | nri | 2,000 |
| 3 | `power-of-attorney-for-nris-complete-guide` | legal | 1,900 |
| 4 | `how-to-verify-property-documents-chennai` | legal | 1,800 |
| 5 | `patta-transfer-process-explained` | legal | 1,900 |
| 6 | `encumbrance-certificate-guide-for-nris` | legal | 1,850 |
| 7 | `property-tax-guide-chennai-nris` | legal | 1,800 |
| 8 | `capital-gains-tax-property-sale-nris` | legal | 2,000 |
| 9 | `tenant-management-guide-overseas-property-owners` | tenant | 2,100 |
| 10 | `nri-property-maintenance-checklist` | maintenance | 1,950 |

#### ✅ 8. Static pSEO Config Analyser
- **File created:** `content/management/commands/analyse_pseo_config.py`
  - Command: `python manage.py analyse_pseo_config`
  - No server or HTTP rendering required — reads `intent_mapping.py` directly
  - Analyses all city × intent × NRI location combinations
  - Detects duplicate titles, meta descriptions, H1s
  - Classifies pages as INDEX / REVIEW / NOINDEX
  - Writes `reports/pseo_config_analysis.csv`
  - Options: `--output`, `--summary-only`

#### ✅ 9. Monthly SEO Monitoring Framework
- **File created:** `documents/SEO_MONITORING_FRAMEWORK.md`
  - Weekly / monthly / quarterly cadence
  - Primary KPI tables: indexing health, organic traffic, conversions, content authority, pSEO quality
  - GSC keyword tracking list (Tier 1 / Tier 2 / Tier 3)
  - 4 GA4 custom report specifications
  - Monthly review checklist (12 items)
  - Escalation triggers
  - Baseline establishment instructions

---

## Files Modified This Session

| File | Change |
|------|--------|
| `content/pseo_quality.py` | **NEW** — quality thresholds and classify_page() |
| `content/management/commands/audit_pseo_quality.py` | **NEW** — full render-based audit command |
| `content/management/commands/analyse_pseo_config.py` | **NEW** — fast static config analyser |
| `content/management/commands/seed_knowledge_hub_phase_a.py` | **NEW** — Phase-A article seeder |
| `content/views_landing.py` | Modified — injects `_pseo_word_count` into context |
| `content/templatetags/seo_tags.py` | Modified — noindex logic via classify_page() |
| `uilayers/templates/seo/meta_tags.html` | Modified — conditional noindex/follow meta tag |
| `uilayers/templates/landing_page.html` | Modified — loads ga4-conversion.js |
| `uilayers/templates/base.html` | Modified — loads ga4-conversion.js globally |
| `static/js/ga4-conversion.js` | **NEW** — GA4 conversion event tracking |
| `documents/NRI_KNOWLEDGE_HUB_ROADMAP.md` | **NEW** — 8-cluster authority roadmap |
| `documents/SEO_BLOCKER_ASSESSMENT.md` | **NEW** — ranked blocker assessment |
| `documents/SEO_MONITORING_FRAMEWORK.md` | **NEW** — monthly monitoring framework |
| `reports/` | **NEW** — output directory for audit CSVs |

---

## Pending Tasks

### 🔴 Critical — Do Before Next Deploy

1. **Seed and publish Knowledge Hub articles**
   ```powershell
   # Seed as drafts first
   .\scripts\django.cmd seed_knowledge_hub_phase_a

   # Review each article in Django admin → /admin/content/blogpost/
   # Then publish with:
   .\scripts\django.cmd seed_knowledge_hub_phase_a --publish
   ```

2. ~~**Run baseline pSEO audit and record results**~~ ✅ **DONE** — June 15, 2026 23:45 IST
   - 765 pages analysed. Results recorded in Baseline Metrics table above.

3. **Submit sitemap to Google Search Console**
   - URL to submit: `https://www.propertism.in/sitemap.xml`
   - Remove any previously failed sitemap entries first
   - Request indexing for: homepage, `/chennai/nri-property-management/`, `/chennai/nri-sell-property/`

4. **Validate GA4 DebugView**
   - Open any landing page in browser
   - Open GA4 → DebugView (Property `G-WZCH8BV34J`)
   - Click the floating WhatsApp button
   - Confirm `whatsapp_click` event fires with `service_intent`, `city_context`, `page_url` parameters

### 🟠 High — Within 1 Week

5. ~~**Add `service_schema` to informational landing pages**~~ ✅ **DONE** — June 15, 2026 23:45 IST
   - `landing_page.html` now fires `service_schema` for both `category == "service"` and `intent_type == "informational"`

6. **Review NRI geo × Bangalore/Hyderabad thin pages**
   - Run `analyse_pseo_config` and filter CSV for `is_nri_geo=yes` + `recommendation=NOINDEX`
   - Decision: either add city-specific content or accept noindex for these combinations

7. ~~**Add internal links from property detail pages to city service pages**~~ ✅ **DONE** — June 15, 2026 23:45 IST
   - "Related NRI Services in Chennai" section added to `properties/detail.html` with 5 internal links

8. ~~**E-E-A-T signals on blog posts**~~ ✅ **DONE** — June 15, 2026 23:45 IST
   - Author box with `schema.org/Person` microdata added to `blog_post.html`
   - Content switched to `|safe` filter so seeded HTML renders correctly
   - FAQ schema block added to `blog_post.html` structured data block

9. ~~**Robots.txt sitemap directive verification**~~ ✅ **DONE** — June 15, 2026 23:45 IST
   - Hardcoded `Sitemap: https://www.propertism.in/sitemap.xml` in `robots.txt` (was dynamic/unreliable)

### 🟡 Medium — Within 2 Weeks

10. **CSS consolidation for Core Web Vitals**
    - `base.html` loads 20+ separate CSS files synchronously
    - Bundle into 3 groups: critical (above-fold), layout, components
    - Or switch to `CompressedManifestStaticFilesStorage` with WhiteNoise (already commented out in settings)

11. **Page-level caching for landing pages**
    - `landing_page` and `city_hub` views are fully deterministic
    - Add `@cache_page(3600)` decorator or set `Cache-Control` headers via CloudFront behaviour
    - Will improve TTFB and reduce RDS load at scale

12. **Knowledge Hub Phase-B content — start planning**
    - Cluster 3 Pillar: NRI Property Legal Guide
    - Cluster 4 Pillar: NRI Property Tax and Capital Gains
    - Target: 4 spokes from these clusters
    - Reference: `documents/NRI_KNOWLEDGE_HUB_ROADMAP.md` Phase B

13. **Lazy-load property card images**
    - Add `loading="lazy"` to all `<img>` tags in property listing cards
    - Already present on `blog_post.html` featured image — extend to property templates

### 🟢 Low — Backlog

14. **GSC Performance baseline recording**
    - After sitemap submission settles (allow 1 week)
    - Pull 28-day GSC Performance report
    - Record impressions, clicks, average position as Month 0 baseline
    - Store in this file under "Baseline Metrics"

15. **Newsletter form selector confirmation**
    - `newsletter_subscribe` event tracked by `ga4-conversion.js`
    - Verify footer form has `data-form="newsletter"` or `id="newsletter-form"` attribute

16. **Structured data for NRI geo service pages**
    - NRI geo landing pages currently get `organization_schema` + `breadcrumb_schema` only
    - Add `service_schema` for NRI geo pages where `config.category == "service"`

17. **Review NRI geo × Bangalore/Hyderabad thin pages**
    - Filter `reports/pseo_config_analysis.csv` for `is_nri_geo=yes` + `recommendation=REVIEW`
    - Decision: add city-specific intro content or consolidate to Chennai canonical pages

---

## Baseline Metrics (Record After First Run)

> Fill these in after running the commands and checking GSC/GA4.

| Metric | Value | Date Recorded |
|--------|-------|---------------|
| Total pSEO pages (config analysis) | 765 | June 15, 2026 — 23:45 IST |
| INDEX candidates | 48 | June 15, 2026 — 23:45 IST |
| REVIEW candidates | 717 | June 15, 2026 — 23:45 IST |
| NOINDEX candidates | 0 | June 15, 2026 — 23:45 IST |
| Duplicate titles | 0 | June 15, 2026 — 23:45 IST |
| Duplicate meta descriptions | 0 | June 15, 2026 — 23:45 IST |
| Duplicate H1s | 210 | June 15, 2026 — 23:45 IST |
| GSC total indexed pages | — | pending GSC access |
| GSC organic impressions (28d) | — | pending GSC access |
| GSC organic clicks (28d) | — | pending GSC access |
| GSC average position (28d) | — | pending GSC access |
| GA4 organic sessions (28d) | — | pending GA4 access |
| GA4 whatsapp_click events (28d) | — | pending GA4 access |
| GA4 contact_form_submit events (28d) | — | pending GA4 access |

---

## Quick Command Reference

```powershell
# Fast pSEO quality check (no server needed)
.\scripts\django.cmd analyse_pseo_config
.\scripts\django.cmd analyse_pseo_config --summary-only

# Full render-based audit (requires DB, slower)
.\scripts\django.cmd audit_pseo_quality --summary-only
.\scripts\django.cmd audit_pseo_quality --city chennai

# Seed Knowledge Hub Phase-A articles
.\scripts\django.cmd seed_knowledge_hub_phase_a           # drafts
.\scripts\django.cmd seed_knowledge_hub_phase_a --publish  # live

# Standard checks
.\scripts\django.cmd check
.\scripts\django.cmd migrate
.\scripts\django.cmd runserver
```

---

## Next Session Start Checklist

1. `git status` — confirm all session files are committed
2. `.\scripts\django.cmd check` — confirm 0 errors
3. Smoke test: `https://www.propertism.in/chennai/nri-property-management/`
4. Check GA4 DebugView — confirm `whatsapp_click` fires on landing page
5. Check GSC sitemap status — confirm `sitemap.xml` submitted and processing
6. Run `.\scripts\django.cmd analyse_pseo_config --summary-only` — record baseline counts
7. Review seeded articles in admin (`/admin/content/blogpost/`) — publish if content approved
8. Continue with Pending Task #5 (informational page service_schema)

---

## Key Documents Created This Session

| Document | Path | Purpose |
|----------|------|---------|
| NRI Knowledge Hub Roadmap | `documents/NRI_KNOWLEDGE_HUB_ROADMAP.md` | 8-cluster content architecture, linking rules, publishing sequence, keyword opportunities |
| SEO Blocker Assessment | `documents/SEO_BLOCKER_ASSESSMENT.md` | Ranked blockers (Critical → Low), GSC/GA4 validation, measurement framework |
| SEO Monitoring Framework | `documents/SEO_MONITORING_FRAMEWORK.md` | Monthly KPI tracking, GA4 report specs, GSC keyword list, escalation triggers |

---

## Session Metadata

**Last Updated By:** Amazon Q (IDE)
**Last Updated On:** June 15, 2026 — 23:45 IST
**Preceding Session:** Session 33 — Tamil Nadu Resources Hub, Premium UI Refinement, Footer Wrapping
**All syntax checks:** ✅ PASSED (py_compile verified on all new Python files)
**Baseline Run:** June 15, 2026 — 23:45 IST (`analyse_pseo_config --summary-only` executed locally)
