<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-04-29 17:19:00
Last Updated By: Astra
Last Updated On: 2026-04-29 17:19:00
Searchtag:COMMITDETAILS202604291719
-->

# Commit Manifest — 2026-04-29 17:19 IST

## Session Title
**Desktop Layout Expansion — Full Viewport Utilization (SCCB-PRM-DESKTOP-WIDTH-EXPANSION-014)**

## Scope
- **Workspace**: `D:\viji\viji-olivine\03rolledout\01propertism`
- **Domain**: Propertism Frontend (CSS / Layout)
- **Sections**: All sections except Hero (locked)

---

## Root Cause Analysis

### Primary Issue: `--prm-container: 1100px`
`propertism-premium.css` `:root` block set the container token to `1100px`. Since `.container` uses `max-width: var(--prm-container)`, every section was capped at a narrow 1100px centered column — creating large dead gutters on 1440px+ displays.

### Secondary Issue: Grid gaps too tight
All section grids had `gap: 20–24px` from `section-overrides.css`. On a 1440px canvas, 24px gaps on 3-col grids read as compressed.

---

## Fixes Applied

### Fix 1: Root Token — `propertism-premium.css`
```diff
-    --prm-container: 1100px;
+    --prm-container: 1440px;
```

### Fix 2: Container override block (appended to `propertism-premium.css`)
```css
.container {
    max-width: var(--prm-container) !important;
    width: 92% !important;
    padding: 0 !important;
    margin: 0 auto !important;
}

@media (min-width: 1600px) {
    .container { max-width: 1600px !important; }
}
```

### Fix 3: Section grid expansions (appended to `propertism-premium.css`)

All 3-column sections (Services `.insights-grid`, Management `.management-preview-grid`, Reviews `.cr-masonry-grid`, Properties `.property-grid-hybrid`, Insights `.journal-preview-grid`) upgraded to `gap: 32px`.

About section (`.credibility-grid`) upgraded to `gap: 48px` for editorial spacing.

Contact (`.contact-section-grid`) confirmed `1fr / 1.2fr` split with `gap: 80px`.

Footer bottom (`.footer-bottom`) set to `display: flex; justify-content: space-between`.

### Fix 4: Responsive breakpoints
- `1025px–1280px`: 3-col maintained, gaps tightened to 24px
- `769px–1024px`: Collapse to 2-col; About & Contact go 1-col
- `≤768px`: Existing mobile block in `propertism-premium.css` unchanged

---

## Files Modified

| File | Summary |
|------|---------|
| `static/css/propertism-premium.css` | (1) `--prm-container` token: 1100px → 1440px. (2) Full desktop expansion block appended (196 lines). |

## Files NOT Modified
- Hero section (`_hero.html`, hero CSS) — LOCKED per SCCB constraint
- `section-overrides.css` — not touched; higher-specificity rules in `propertism-premium.css` win
- All mobile breakpoints (`@media max-width: 768px`) — preserved

---

## Validation Checklist
- [ ] 1920px: No excessive margins left/right
- [ ] 1600px: Balanced card spread
- [ ] 1440px: No overlap / no crowding
- [ ] Mobile (≤768px): Unchanged behavior
- [ ] Tablet (769px–1024px): 2-col fallback intact

---

## Commit Message (Suggested)

```
feat: desktop layout expansion — full viewport utilization (SCCB-PRM-014)

Expanded --prm-container token from 1100px to 1440px.
Added 92% fluid width container with 1600px+ premium cap.
All 3-col section grids upgraded to gap: 32px.
About section gap: 48px for editorial feel.
Desktop breakpoints: 3-col at 1025–1280px, 2-col at 769–1024px.
Hero section untouched (locked).
Mobile breakpoints preserved.
```

---

**Session Status**: ✅ READY FOR COMMIT  
**Quality**: Surgical — Root token fix + targeted section grid expansion
