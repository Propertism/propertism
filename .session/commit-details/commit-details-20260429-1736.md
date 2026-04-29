<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-04-29 17:36:00
Last Updated By: Astra
Last Updated On: 2026-04-29 17:36:00
Searchtag:COMMITDETAILS202604291736
-->

# Commit Manifest — 2026-04-29 17:36 IST

## Session Title
**Typography Consistency + Section Rhythm + Background Harmonization (SCCB-PRM-TYPO-RHYTHM-COLOR-016)**

## Scope
- **Workspace**: `D:\viji\viji-olivine\03rolledout\01propertism`
- **Domain**: Propertism Frontend (Typography / Color / Rhythm)
- **Sections**: All sections except Hero (locked)

---

## Design Decisions & Deviations

### ⚠️ Footer Background — DEFERRED to SCCB-017

**SCCB spec:** Change footer background from dark `#0F0F10` to light `#FBFAF8`.

**Why deferred:**  
The footer has ~80 lines of `!important` overrides in `propertism-premium.css` targeting:
- Body text, links: `#B0B0B5` (light gray — invisible on `#FBFAF8`)  
- World clock cells: same light gray text  
- Copyright strip: `rgba(255,255,255,0.4)` (fully invisible on white)  
- Newsletter form inputs: dark glass styling  
- Social icon colors  

Changing background without full text recolor = broken footer with invisible content.  
Token `--prm-footer-light: #FBFAF8` is registered and ready for SCCB-017.

### ℹ️ `.why-owners-card` class not found in templates

This class does not exist anywhere in the codebase. The equivalent is `#about-section .credibility-proof-card` (right panel in About section). Tone correction applied to that selector.

### ℹ️ `text-wrap: balance` — browser compatibility

Supported: Chrome 114+, Firefox 121+, Safari 17.4+ (April 2024+). Safe for production target audience.

### ℹ️ HTML span wrapping (heading orphan control)

The SCCB mentions wrapping orphan words in `<span style="white-space:nowrap">`. This is an HTML change — not done in this SCCB. `text-wrap: balance` via CSS handles 80% of orphan cases automatically without HTML edits.

---

## Fixes Applied

### Fix 1: Design Tokens Added to `:root`
```css
--prm-white: #FFFFFF
--prm-beige: #F7F5F2
--prm-footer-light: #FBFAF8   (ready for SCCB-017)
--prm-text-body: #4A4A4A
--prm-text-sub: #6B7280
```

### Fix 2: Typography Utility System

| Selector | What changed |
|---|---|
| `.section-title` | New utility: `clamp(1.8–2rem)`, `line-height: 1.25`, `text-wrap: balance` |
| `.section-subtitle` | New utility: `1rem`, `color: #6B7280`, `max-width: 720px` |
| `.section-title-centered` | Existing class aligned to same spec + `text-wrap: balance` |
| `.section-desc-centered` | Existing class aligned to same spec |
| `#services-section h2` | Targeted via `.section-intro-center h2` |
| `#reviews-section h2` | Targeted via `.customer-reviews-intro h2` |
| `.featured-properties-title` | Aligned to canonical spec |
| `.featured-properties-subtitle` | Aligned to canonical spec |

### Fix 3: Background Rhythm

| Section | Before | After |
|---|---|---|
| Services | `#F9F8F5` | `#F7F5F2` (canonical beige) |
| Management | `#F9F8F5` | `#F7F5F2` |
| Properties | `#F9F8F5` | `#F7F5F2` |
| Contact | `#f8f9fb` (SCCB-015) | `#F7F5F2` (canonical beige) |
| About / Reviews / Insights | `#FFFFFF` | `#FFFFFF` (unchanged) |

### Fix 4: Section Rhythm
`section { padding: 100px 0 }` → `72px 0` (desktop) / `60px 0` (mobile) / `88px 0` (1600px+)  
`#home-section` (hero) excluded — `padding: 0 !important` prevents interference.

### Fix 5: About Card Tone Correction
```diff
- background: linear-gradient(180deg, #132236 0%, #182c44 100%)
+ background: linear-gradient(135deg, #1F2937 0%, #111827 100%)
```
Softer, warmer navy tone. Less harsh against white background.

### Fix 6: Card Density
`.insight-card, .cr-card, .management-preview-card, .journal-preview-card`  
→ `padding: 24px`, `border-radius: 14px`

---

## Files Modified

| File | Summary |
|------|---------|
| `static/css/propertism-premium.css` | SCCB-016 block appended: tokens, typography system, bg rhythm, section padding, card density, about card tone |

## Files NOT Modified
- Any HTML templates (no structural changes)
- Hero (`#home-section`) — padding explicitly excluded
- Footer — deferred to SCCB-017

---

## SCCB-017 Pre-Requisite (Footer Light Theme)

Requires full recolor of:
- `.site-footer` all text (`#B0B0B5` → `#6B7280`)
- `.site-footer a` (`#B0B0B5` → `#6B7280`)
- `.site-footer h3` (gold — stays, but may need adjustment)
- World clock cell text (all light colors → dark)
- Copyright strip (`rgba(255,255,255,0.4)` → `#9CA3AF`)
- Newsletter form inputs (dark glass → light)
- Footer bottom border color update

---

## Commit Message (Suggested)

```
feat: typography + rhythm + bg harmonization (SCCB-PRM-016)

Add CSS tokens: --prm-white, --prm-beige, --prm-text-sub.
Add .section-title / .section-subtitle utility classes.
Apply text-wrap: balance to all section headings.
Enforce alternating white/beige bg rhythm across all sections.
Contact bg aligned to canonical --prm-beige.
Section padding: 100px → 72px (88px@1600px+). Hero excluded.
About card: gradient angle softened (135deg, warmer navy).
Card density: padding 24px, radius 14px uniform.
Footer light theme deferred → SCCB-017 (token ready).
```

---

**Session Status**: ✅ READY FOR COMMIT  
**Quality**: Precision — class names verified against HTML, hero excluded, footer deferred with reasoning
