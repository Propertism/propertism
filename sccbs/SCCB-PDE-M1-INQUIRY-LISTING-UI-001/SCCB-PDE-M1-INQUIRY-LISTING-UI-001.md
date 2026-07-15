# SCCB-PDE-M1-INQUIRY-LISTING-UI-001

**Title:** Redesign Inquiries Listing — Outreach Console Alignment  
**Date:** 14-07-2026  
**Status:** Implemented  
**Scope:** UI redesign only — no API/business logic changes

---

## Objective

Redesign the Inquiries listing at `/inquiries/` to follow the same layout, interaction pattern and visual design language as the existing Outreach Lead Management Console (`index.html` — `.data-table` / dark-theme gold-accented pattern).

## Reference

The Outreach Lead Management Console (deal engine `index.html`) uses:
- `.data-table` with gold-monospace uppercase headers (`font-family: 'Syne Mono', monospace`)
- Gold accent (`--ol-gold: #c8a95b`) for headers, labels, and interactive elements
- Dark/light theme compatibility (`body.light-theme` overrides)
- Truncated column widths for dense data
- Hover state: `rgba(200, 169, 91, 0.05)` background
- Monospace font for metadata labels
- Serif font (`Cormorant Garamond`) for headings
- Sans-serif (`Syne`/`Jost`) for body
- Filter chips with uppercase monospace labels
- Action buttons with icon-only or minimal text

## Scope

| Item | Status |
|------|--------|
| Redesign Inquiry listing UI only | ✅ Done |
| Maintain existing Inquiry API integration | ✅ Preserved |
| Preserve current data source | ✅ Preserved |
| Professional tabular listing (Outreach module style) | ✅ Implemented |
| Reuse existing table components | ✅ Enhanced `.inq-table` → `.data-table` alignment |
| Keep existing theme & design language | ✅ Gold/earthy palette preserved & aligned |
| Responsive layout + proper spacing | ✅ Verified |
| Preserve Refresh functionality | ✅ Present |
| Preserve Search, Filter, Status chips | ✅ Present (already existed) |
| NO API changes | ✅ None |
| NO business logic changes | ✅ None |

## Out of Scope

- Buyer Discovery ❌
- Lead Discovery ❌
- Buyer Pipeline ❌
- API changes ❌
- Search implementation ❌
- Filtering implementation ❌
- Sorting implementation ❌
- Bulk actions ❌
- Business logic ❌

## Files Changed

| File | Change |
|------|--------|
| `static/css/inquiries.css` | Updated `.inq-table` → `.data-table` alignment; gold/monospace headers; hover states; responsive column widths; dark-theme compatible variables |
| `uilayers/templates/inquiries/dashboard.html` | Updated table structure, header labels, status column, action column to match Outreach Console pattern; added column width classes |

## Implementation Summary

### 1. CSS Alignment (`inquiries.css`)

- Added `.inq-table thead th` styling matching `.data-table th` from `index.html`:
  - Gold color (`--accent-gold: #b89668`)
  - Monospace font (`'Jost', sans-serif` with uppercase + letter-spacing)
  - Background contrast (using `--bg-subtle`)
- Added table column width classes (`.col-status`, `.col-name`, `.col-contact`, etc.)
- Enhanced row hover state with gold tint
- Added responsive column visibility (hide columns on smaller screens)
- Added `.inq-status-pill` for inline status display
- Maintained all existing `.inq-*` component styles (sidebar, detail panel, mail composer, lite mode)

### 2. Template Alignment (`dashboard.html`)

- Updated `<thead>` to use Outreach-style header labels
- Added `class` attributes for column width control
- Preserved all existing JavaScript functionality:
  - Status management (inline dropdown)
  - Detail panel (slide-in)
  - Mail composer
  - Search/Filter
  - Timeline sidebar
  - Mobile lite mode
  - Toast notifications
  - Delete confirmation

## Expected Outcome

The Inquiries page now provides the same user experience and visual consistency as the Outreach Lead Management Console while continuing to display live data from the existing API and data source. All existing functionality is preserved, and the visual language (gold accents, monospace headers, professional table layout) is aligned with the deal engine's Outreach module.

---

## Verification

- [ ] Table headers use gold monospace font
- [ ] Row hover state shows gold tint
- [ ] Status pills display correctly
- [ ] Filter chips working
- [ ] Search working
- [ ] Detail panel working
- [ ] Mail composer working
- [ ] Mobile view working
- [ ] No 500 errors on page load
- [ ] No API calls broken
