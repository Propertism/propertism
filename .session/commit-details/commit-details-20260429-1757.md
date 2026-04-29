<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-04-29 17:57:00
Last Updated By: Astra
Last Updated On: 2026-04-29 17:57:00
Searchtag:COMMITDETAILS202604291757
-->

# Commit Manifest — 2026-04-29 17:57 IST

## Session Title
**Trust → Action Flow Optimization (SCCB-CONVERSION-BOOST-019)**

## Scope
- **Workspace**: `D:\viji\viji-olivine\03rolledout\01propertism`
- **Domain**: Propertism Frontend (UX Psychology / Conversion)
- **Sections**: About (credibility-proof-card) + Contact

---

## ⚠️ SCCB Point 6 — Copy Change NOT Applied (DB Field)

SCCB asked to change contact h2 text to *"Let's manage your Chennai property — stress-free."*

The contact section title is rendered via `{{ company.contact_section_title }}` — a database field, NOT hardcoded. It cannot be changed via HTML or CSS. To update this copy, Viji must update it through the Django admin panel.

---

## Files Modified

| File | Change |
|------|--------|
| `static/css/propertism-premium.css` | SCCB-019 CSS block appended (+138 lines) |
| `uilayers/templates/home/sections/_about.html` | `.why-owners-cta` micro CTA added after `.credibility-proof-card` |
| `uilayers/templates/home/sections/_contact.html` | `.contact-trust-points` bullets added inside `.contact-info-column` |

---

## CSS Changes

| Item | Implementation |
|---|---|
| Gold accent bar | `#about-section .credibility-proof-card::before` — 3px × 60px gold line, `margin-bottom: 20px` |
| `.btn-outline-light` | White ghost button for dark card; hover: `rgba(255,255,255,0.1)` bg + lift |
| `.why-owners-cta` | Separator border-top, `margin-top: 24px`, `padding-top: 20px` |
| Contact form shadow | `box-shadow: 0 16px 40px rgba(0,0,0,0.08)` |
| `.contact-form .btn-gold` | `width: 100%; padding: 16px 24px; font-size: 1rem; border-radius: 8px` |
| `.contact-form .btn-gold:hover` | `translateY(-2px)` + gold glow shadow |
| `.contact-trust-points` | Flex column, gap 10px, gold `✔` pseudo-element via `::before` |

## HTML Changes

### `_about.html` — Why Owners micro CTA
Added AFTER `.credibility-proof-card` closing tag, INSIDE `.credibility-grid`:
```html
<div class="why-owners-cta">
    <a href="#contact-section" class="btn-outline-light">Talk to Us</a>
</div>
```
⚠️ Note: `.why-owners-cta` sits inside `.credibility-grid` but OUTSIDE `.credibility-proof-card`. The CSS positions it inside the dark card via the grid column structure. Visually it appears at the bottom of the right column.

### `_contact.html` — Trust proof bullets
Added AFTER `.contact-map-link`, inside `.contact-info-column`:
```html
<ul class="contact-trust-points">
    <li>10+ years of NRI property expertise</li>
    <li>500+ properties managed across Chennai</li>
    <li>Dedicated on-ground team, always reachable</li>
</ul>
```
Gold `✔` checkmarks applied via CSS `::before` pseudo-element (no emoji in HTML).

---

## Conversion Flow Achieved

```
About (Context: light) 
→ Why Owners Card (Trust: dark — gold accent bar)
   → [Talk to Us] ghost CTA ─────────────────────┐
→ Management / Reviews (Proof: light)             │
→ Contact Section (Action: beige → white)  ◄──────┘
   ← trust bullets (10yr / 500+ / dedicated team)
   ← elevated form card with dominant gold CTA
```

---

## Validation Checklist
- [ ] Gold accent bar visible above proof card content
- [ ] "Talk to Us" ghost button visible on dark card bg
- [ ] Ghost button links to `#contact-section`
- [ ] Contact form button: full-width, gold, prominent
- [ ] Button hover: lift + gold shadow
- [ ] Trust bullets: `✔` in gold, dark text
- [ ] Trust bullets: 3 items visible in contact left column
- [ ] Copy change (DB field): update via Django Admin: *"Let's manage your Chennai property — stress-free."*

---

## Commit Message (Suggested)

```
feat: conversion flow optimization (SCCB-019)

About proof card: gold accent bar (::before 3px × 60px).
Add .why-owners-cta ghost CTA linking to #contact-section.
Add .btn-outline-light: white ghost button for dark card context.
Contact form: elevated shadow 0 16px 40px, full-width gold CTA.
CTA hover: translateY(-2px) + gold glow.
Add .contact-trust-points: 3 proof bullets with gold checkmarks.
Trust bullets: 10yr / 500+ properties / dedicated team.
Note: contact h2 copy is a DB field — update via Django Admin.
```

---

**Status**: ✅ COMPLETE  
**Files**: 3 (propertism-premium.css, _about.html, _contact.html)
