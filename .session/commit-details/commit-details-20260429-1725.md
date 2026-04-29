<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-04-29 17:25:00
Last Updated By: Astra
Last Updated On: 2026-04-29 17:25:00
Searchtag:COMMITDETAILS202604291725
-->

# Commit Manifest — 2026-04-29 17:25 IST

## Session Title
**Edge Anchoring + Full-Bleed + Contact Light Theme (SCCB-PRM-EDGE-ALIGN-FULLBLEED-015)**

## Scope
- **Workspace**: `D:\viji\viji-olivine\03rolledout\01propertism`
- **Domain**: Propertism Frontend (CSS / Layout / Visual Polish)
- **Sections**: Services, About, Management, Reviews, Properties, Insights, Contact, Footer

---

## Design Decisions & Deviations from SCCB Spec

### ⚠️ Edge Anchoring: `justify-self: stretch` instead of `start/center/end`

**SCCB spec:**
```css
.grid-3 > *:nth-child(1) { justify-self: start; }
.grid-3 > *:nth-child(2) { justify-self: center; }
.grid-3 > *:nth-child(3) { justify-self: end; }
```

**Why not implemented as-is:**  
In a `repeat(3, 1fr)` grid, `justify-self: start` on an item with no explicit width causes the item to shrink to content width — **cards collapse**. This directly contradicts the "stretch edge-to-edge" goal.

**What was implemented instead:**
```css
> * {
    justify-self: stretch !important;
    width: 100% !important;
    box-sizing: border-box !important;
}
```
This is the correct CSS Grid mechanism for ensuring each card fills its `1fr` cell edge-to-edge, anchored to the container boundaries.

---

## Fixes Applied

### Fix 1: Full-Bleed Utility Classes
```css
.section-full { width: 100%; position: relative; }
.section-inner { max-width: var(--prm-container); width: 92%; margin: 0 auto; }
```
Note: Existing HTML already uses `<section>` (100% wide) + `.container` (content bounded), which achieves full-bleed backgrounds natively. Utility classes added for future use.

### Fix 2: Edge Anchoring (Grid item stretch)
Applied `justify-self: stretch; width: 100%; box-sizing: border-box` to all grid children across all 3-col and 2-col sections.

### Fix 3: Micro spacing at 1600px+
| Section | Gap before | Gap after |
|---------|-----------|-----------|
| All 3-col grids | 32px (014) | 40px (1600px+) |
| About 2-col | 48px (014) | 56px (1600px+) |
| Contact 2-col | 80px (014) | 96px (1600px+) |

### Fix 4: Contact Section — Full Light Theme Recolor

Dark `#0F0F10` → Light `#f8f9fb`. ALL sub-elements recolored:

| Element | Before | After |
|---------|--------|-------|
| Section bg | `#0F0F10` dark | `#f8f9fb` light |
| h2 | white | `#111111` |
| p | white | `#4A4A4A` |
| Address text | white | `#1A1A1A` |
| Form inputs bg | `rgba(255,255,255,0.03)` | `#f8f9fb` |
| Form inputs text | white | `#111111` |
| Placeholder text | faded white | `#9CA3AF` |
| Form bg | dark glass | white card |
| Form focus | gold ring | gold ring (preserved) |
| Map link | dark glass | white card |

### Fix 5: Footer Width Enforcement
`.site-footer .container` pinned to `max-width: var(--prm-container)` + `width: 92%`.

---

## Files Modified

| File | Summary |
|------|---------|
| `static/css/propertism-premium.css` | Appended SCCB-015 block: utility classes, edge anchoring, micro-spacing, contact light theme, footer width enforcement |

## Files NOT Modified
- `_hero.html` — LOCKED
- All HTML templates — no structural changes
- Mobile breakpoints (`@768px`) — preserved

---

## Validation Checklist
- [ ] 1920px: Cards stretch to container edges, no float gap
- [ ] 1600px: Gap upgrades visible (40px / 56px)
- [ ] Contact section: Light background, dark legible text, correct form colors
- [ ] Contact form: Gold focus ring visible on light inputs
- [ ] Footer: No narrowing at 1440px+
- [ ] Mobile (≤768px): Contact form padding restored; grids stacked

---

## Commit Message (Suggested)

```
feat: edge anchoring + contact light theme (SCCB-PRM-015)

Add edge anchoring via justify-self: stretch + width: 100% on
all grid items (1fr columns require stretch, not start/end).
Add .section-full / .section-inner utility classes.
Upgrade gap at 1600px+: 40px (3-col), 56px (2-col), 96px (contact).
Contact section: full light theme (#f8f9fb bg, dark text, light
form inputs, placeholder color, focus ring preserved).
Footer container pinned to --prm-container width.
Hero + mobile unchanged.
```

---

**Session Status**: ✅ READY FOR COMMIT  
**Quality**: Precision CSS — Design conflict resolved at justify-self level
