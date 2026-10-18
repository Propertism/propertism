<!-- AUDIT METADATA -->
<!-- Date: 2026-10-18 -->
<!-- Time: 19:50 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra 1 -->
<!-- Module: 03-propertism -->
<!-- Status: LEVEL 4 VERIFIED — READY FOR PRODUCTION DEPLOYMENT -->
<!-- Git Commit: HEAD (uncommitted) -->

# 📋 IMPLEMENTATION REPORT: SPAM QUARANTINE GATEWAY, PROPERTIES CAROUSEL & DUAL CTA

**Platform / Module**: `03-propertism`  
**Platform URL**: `https://www.propertism.in`  
**Product Owner**: Viji  
**Supervisor / Platform Owner**: Astra 1  
**Execution Date**: 18 October 2026 (Evening Session)  
**Governance Alignment**: Canonical 8-Stage Delivery Protocol (Stage 2: Internal Test & Declare ➔ Stage 3: Report to Viji)  

---

## 1. Executive Summary & Objective Alignment

Following Viji's strategic directives ("1,3 - proceed", "2 - i have deleted", "4 - Option C is my choice"):
1. **Task 1 — Midform / General Inquiry Spam Quarantine**:
   - Eliminated the leak vector where `Likely Spam` inquiries were saved into the primary `PropertyInquiry` / `Inquiry` table.
   - Guaranteed that flagged submissions are completely diverted into `content.models.SpamLog` with full forensic context (`name`, `email`, `phone`, `message`, `country`, `confidence_score`, `failure_reason`, and raw `payload`).
   - Guarded the reCAPTCHA confidence boost (`+10`) so that dangerous spam indicators (Cyrillic script, bot names, blacklisted domains, danger flags) are not masked into a "Review Recommended" score.
   - Preserved silent honeypot UX: Returning normal `messages.success` thank-you confirmation so malicious bots do not discover quarantine or mutate payloads.
2. **Task 2 — SpamLog Table Audit (30K rows)**:
   - Evaluated root cause: historical 31K entries were edge DDoS firewall rate-limit hits with null contact fields.
   - Viji verified and cleanly purged them via the newly deployed "Empty Spam Log" UI on production.
3. **Task 3 — Properties Section Carousel Navigation (>3 items)**:
   - Added circular gold chevron controls (`‹` and `›`) to the section header when `featured_properties|length > 3`.
   - Built a 100% native inline SVG and Vanilla JS carousel track with scroll-snapping, showing 3 cards per row on desktop, 2 on tablet, and 1 on mobile.
   - Zero external CDNs or 3rd-party libraries (strictly compliant with Viji's 100% Native Code Law).
4. **Task 4 — "View All Properties" Dual CTA (Option C Architecture)**:
   - Replaced single dead-end button with high-converting **Dual CTA cluster**:
     - `[ View All Properties → ]`: Primary gold button routing to the catalog search page (`/properties/`).
     - `[ Request Off-Market Shortlist → ]`: Secondary gold outline button smoothly scrolling to the lead intake midform (`#contact-section`).

---

## 2. File-by-File Code & Architecture Changes

### A. `properties/utils/lead_validation.py`
- **Cyrillic Name Check (`_check_contact_info`)**:
  - Added explicit regex search `re.search(r'[\u0400-\u052F]', name)` before other name checks.
  - Penalizes `-80` points and appends a `type: 'danger'` flag to `validation_summary`.
  - Blocks Russian name injections (e.g. `Александр`, `Влад`) at intake.

### B. `content/views.py` (`contact()` view)
- **Guarded reCAPTCHA Confidence Boost**:
  - `has_spam_danger = any(v.get('type') == 'danger' for v in assessment.get('validation_summary', []))`
  - Suppresses the `+10` score boost when any danger flag is present, preventing spam bot scores from jumping from 35 to 45.
- **Comprehensive Spam Quarantine Gate**:
  - Added heuristic guard detecting:
    1. `assessment_status == 'Likely Spam'`
    2. Cyrillic script in combined name + message body
    3. Concatenated bot names (`RobertTharp`, etc.)
    4. Blacklisted affiliate domains (`wellorena.com`)
    5. Any `danger` type validation summary item
  - If triggered: Creates full forensic `SpamLog` record, logs warning, displays thank-you message to user, and redirects cleanly (handling `Quick Inquiry` midform vs general contact).

### C. `properties/views.py` (`create_inquiry()` view)
- **Symmetric Spam Quarantine Gate**:
  - Mirroring `content/views.py`, prevents any property detail page inquiry identified as spam from reaching `PropertyInquiry`.
  - Injects into `SpamLog` with matching `failure_reason = Likely Spam (...)`.

### D. `uilayers/templates/home/sections/_properties.html`
- **Prominent Dual Navigation Architecture**:
  - **Floating Side Chevrons**: Large 52px circular floating buttons (`.prop-floating-chevron`) positioned on the left and right edges directly vertically centered with the property cards. Impossible to miss; provides intuitive one-click sliding.
  - **Header Companion Controls & Live Counter**: `.properties-carousel-header-nav` placed to the right of the section title featuring an elegant gold counter pill (`1 / 9`) and paired circular arrow buttons.
- **Data & Spec Safeguards**:
  - Fixed duplicate location display: `{% if "Chennai" in property.location %}{{ property.location }}{% else %}{{ property.location }}, Chennai{% endif %}` cleanly prevents `Chennai, Chennai`.
  - Fixed blank specs display: Guarded BHK and area tags so `0 BHK` or `NONE SQ FT` never appear.
- **Scroll Snapping Carousel Track**:
  - Displaying 3 cards per row on desktop, 2 on tablet, and 1 on mobile with native CSS scroll-snapping.
- **Option C Dual CTA**:
  - `[ View All Properties → ]` $\rightarrow$ `{% url 'property_list' %}`
  - `[ Request Off-Market Shortlist → ]` $\rightarrow$ `{{ home_section_links.contact }}`

### H. Visual Refinements & Layout Optimization (Viji Directives)
1. **Header Pill & Counter Removal (User Directive 1)**:
   - Completely excised `.properties-carousel-header-nav` (the `2 / 9` pill and small header buttons) from `_properties.html` and `v4-properties.css`.
   - The UI is clean and uncluttered; navigation is handled exclusively via the floating side chevrons.
2. **Symmetrical Floating Chevrons on Card Edges (User Directive 2)**:
   - Diagnosed root cause of staggered right chevron: a legacy rule `#properties-section .property-grid-hybrid { gap: 1px !important; }` at line 438 of `v4-properties.css` was overriding the carousel's 24px gap to 1px, leaving 46px of dead space and allowing a 4th card to peek out.
   - Removed the legacy override and decoupled the carousel track from `.property-grid-hybrid` (`class="properties-carousel-track"`).
   - Enforced `width: 100% !important; max-width: 100% !important;` on `#propCarouselTrack`, guaranteeing that exactly 3 cards span 100% of the viewport width.
   - Positioned `.prop-floating-prev` at `left: -24px` (centered on Card 1's left border) and `.prop-floating-next` at `right: -24px` (centered on Card 3's right border), delivering 100% mathematical and visual symmetry.
3. **Properties Page Compact Header & Left Margin Normalization (User Directive 3)**:
   - Removed the giant dark box (`.properties-page-hero`) from `uilayers/templates/properties/list.html`.
   - Replaced it with a clean, open, compact 3-line header (`.properties-page-header`):
     - Line 1: `.properties-page-kicker` (Gold house SVG + uppercase `CURATED PROPERTIES`)
     - Line 2: `.properties-page-title` (Playfair Display serif title: `Premium opportunities for NRI ownership.`)
     - Line 3: `.properties-page-subtitle` (Muted gray subtitle: `Browse active listings selected for location strength, rental potential, and long-term ownership fit across Chennai.`)
   - Diagnosed tight left margin: Tailwind CSS runtime script injected a generic `.container` rule. Replaced `<div class="container">` with `<div class="properties-page-inner">`, enforcing `max-width: 1400px !important; margin: 0 auto !important; padding: 0 40px !important;`, perfectly aligning with the navbar and homepage layout.
   - Set top padding to `124px !important;` so the 3-line header sits cleanly 28px below the 92px fixed navbar.
4. **Single-Line Breathing Space Normalization (User Directive 4)**:
   - Reduced excessive vertical margins and padding to a unified single-line rhythm (~16-20px) across both pages:
     - `#properties-section`: `padding: 28px 0 32px !important;`
     - `.section-header`: `margin-bottom: 16px !important;`
     - `.properties-carousel-container`: `margin: 4px 0 16px !important;`
     - `.featured-properties-cta`: `margin-top: 16px !important;`
     - Card body: `padding: 20px !important;` with 4-8px spacing between location, title, price, and specs.

---

## 3. Deterministic Verification & Evidence Gate

### Local Test Suite Execution:
- **Command**: `.\.venv\Scripts\python.exe manage.py test properties.tests properties.test_security_fixes content.tests`
- **Result**: **93 passed, 0 failures, 0 errors** in 23.230s.

### Visual & Interactive Browser Verification:
- **Tool**: `browser_subagent` live probe at `http://127.0.0.1:8001/` and `http://127.0.0.1:8001/properties/`
- **Artifact Evidence Captured**:
  1. `homepage_properties_carousel_aligned.png`: Exact 3-card layout, zero peeking of Card 4, floating chevrons symmetrically overlapping the left edge of Card 1 and the right edge of Card 3.
  2. `homepage_properties_carousel_scrolled.png`: Smooth 1-step slide to Cards 2-4, maintaining exact edge-alignment under both chevrons.
  3. `properties_page_compact_clean.png`: Dark box completely eliminated; compact 3-line header visible below navbar with balanced 40px left and right margins matching the site container.

---

## 4. Adversarial Self-Critique & Failure Mode Analysis

| Component / Flow | Potential Failure Mode | Defense / Resolution Implemented |
|---|---|---|
| **Right Chevron Alignment** | Uneven card widths or narrow gap allow 4th card to peek, misaligning the right chevron. | Track decoupled from `.property-grid-hybrid`; legacy `gap: 1px` removed; exact `width: 100%` and `calc((100% - 48px) / 3)` enforced on desktop. |
| **Properties Page Container Override** | Tailwind runtime script (`cdn.tailwindcss.com`) overrides `.container` margin and width. | Changed wrapper to `.properties-page-inner` with explicit `max-width: 1400px !important; margin: 0 auto !important; padding: 0 40px !important;`. |
| **Navbar Overlap on `/properties/`** | Fixed 92px navbar covers header kicker. | Enforced `padding: 124px 0 48px !important;` on `.properties-page`, guaranteeing 28px clearance below navbar. |
| **Spam Quarantine Gate** | Bot receives error status and iteratively adjusts payload to evade filters. | Tarpit UX: Returns standard `messages.success` and identical UI redirect. The bot receives HTTP 302/200, believing submission succeeded. |
| **Confidence Score Distortion** | reCAPTCHA solve farm passes checkbox, adding `+10` boost and lifting a 35-score spam submission into "Review Recommended". | Guarded boost: If any `type == 'danger'` rule fired (Cyrillic, CamelCase, URL injection), boost is strictly skipped. |

---

## 5. Next Steps for Stage 4–6

1. **Stage 4 & 5 (PO Verification & Approval)**: Viji verifies implementation details and visual proof in chat.
2. **Stage 6 (Git Push under Propertism)**:
   - Ensure GitHub CLI user is `Propertism` (`gh auth switch --user Propertism`).
   - Stage and commit files with descriptive commit message.
   - Push to `origin main` to trigger GitHub Actions deployment pipeline to Lightsail.


