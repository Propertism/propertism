<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-04-29 17:49:00
Last Updated By: Astra
Last Updated On: 2026-04-29 17:49:00
Searchtag:COMMITDETAILS202604291749
-->

# Commit Manifest — 2026-04-29 17:49 IST

## Session Title
**About Section Density Fix + Contact Section Balance (SCCB-PRM-BALANCE-ABOUT-CONTACT-018)**

## Scope
- **Workspace**: `D:\viji\viji-olivine\03rolledout\01propertism`
- **Domain**: Propertism Frontend (Visual Balance / Layout Harmony)
- **Sections**: About + Contact only

---

## Class Resolution Table

All SCCB alias names resolved to actual HTML classes — no phantom selectors written:

| SCCB Alias | Real HTML Class |
|---|---|
| `.about-text` | `#about-section .credibility-story-card` |
| `.about-text p` | `#about-section .credibility-copy` |
| `.about-text .cta-group` | `#about-section .credibility-actions` |
| `.why-owners-card` | `#about-section .credibility-proof-card` |
| `.about-grid` | `#about-section .credibility-grid` |
| `.get-in-touch` | `#contact-section, .nri-contact-section` |
| `.get-in-touch-grid` | `.contact-section-grid` |
| `.contact-info h2` | `#contact-section .section-intro-center h2` *(h2 is ABOVE the grid, in .section-intro-center)* |
| `.contact-info p` | `.contact-info-column p` |
| `.contact-form` | `.contact-form` ✅ exact match |

---

## Fixes Applied

### ABOUT SECTION

| Fix | Implementation |
|---|---|
| Left column density | `.credibility-story-card { max-width: 520px }` |
| Body text line-height | `.credibility-copy { line-height: 1.65; max-width: 520px }` |
| CTA anchoring | `.credibility-actions { margin-top: 20px; align-items: center; gap: 16px }` |
| Right card soften | `.credibility-proof-card { box-shadow: 0 10px 30px rgba(0,0,0,0.08) }` |
| Grid vertical balance | `.credibility-grid { align-items: center; gap: 56px }` |

### CONTACT SECTION

| Fix | Implementation |
|---|---|
| Gradient bg | `linear-gradient(to bottom, var(--prm-beige) 0%, var(--prm-beige) 70%, #FFFFFF 100%)` |
| Grid rebalance | `grid-template-columns: 1.1fr 1fr; gap: 56px` (left column wins weight) |
| Section intro: left-align | `.section-intro-center { text-align: left; margin-bottom: 40px }` |
| h2 width + dark color | `max-width: 420px; color: #111111 !important` (overrides inline `style="color:white"`) |
| Description p | `max-width: 420px; line-height: 1.6` |
| Form width control | `.contact-form { max-width: 520px; border-radius: 14px }` |
| Form card elevation | `box-shadow: 0 12px 32px rgba(0,0,0,0.06); border: 1px solid rgba(0,0,0,0.04)` |
| Contact padding | `72px 0 80px` (asymmetric — extra bottom for gradient softening) |

### Responsive Safeguards
- `≤1024px`: Contact grid collapses to 1-col; section intro re-centered
- `≤768px`: About grid restores stretch alignment; left column full-width

---

## Files Modified

| File | Summary |
|------|---------|
| `static/css/propertism-premium.css` | SCCB-018 block appended (+181 lines) |

## Files NOT Modified
- HTML templates — no structural changes
- Global grid system — untouched
- Typography system — untouched
- Footer — untouched

---

## Validation Checklist
- [ ] About: left/right columns feel balanced in height and visual weight
- [ ] About: CTA buttons vertically centered and not floating
- [ ] About: right card softer (less shadow dominance)
- [ ] Contact: gradient visible — beige fading into white at bottom
- [ ] Contact: h2 left-aligned, dark, max 420px wide
- [ ] Contact: form capped at 520px width
- [ ] Contact: form card elevated (white on beige, subtle shadow)
- [ ] Tablet (≤1024px): contact intro re-centered, grid stacked
- [ ] Mobile (≤768px): about grid stretches, left column full width

---

## Full Session Commit Summary (6 SCCBs)

| SCCB | Title |
|---|---|
| Hero Fix (06:50) | Rotation CSS + duplicate script |
| **014** | Desktop width expansion, 1440px container |
| **015** | Edge anchoring + contact light theme |
| **016** | Typography system + bg rhythm + section padding |
| **017** | Footer full light theme recolor |
| **018** | About density + contact balance ← TODAY'S FINAL |

---

## Commit Message (Suggested)

```
feat: about density fix + contact balance (SCCB-PRM-018)

About: constrain left column max-width 520px, tighten line-height 1.65.
CTA: margin-top 20px, align-items center (anchored, not floating).
Right card: softer shadow (0 10px 30px 0.08). Grid: align-items center, gap 56px.
Contact: beige→white gradient bg (70/30 split), no hard block.
Grid: 1.1fr/1fr (info column weighted). Section intro: left-aligned.
h2: max-width 420px, color #111111 overriding inline white style.
Form: max-width 520px, border-radius 14px, elevated white card.
Responsive: contact 1-col + re-centered intro at ≤1024px.
```

---

**Session Status**: ✅ ALL 6 SCCBs COMPLETE  
**Quality**: Precise — All SCCB aliases resolved to actual HTML classes before writing
