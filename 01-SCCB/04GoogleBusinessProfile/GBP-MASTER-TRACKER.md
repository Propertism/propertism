# Google Business Profile — Master Tracker
**Project:** Propertism Realty Advisors
**Profile:** Google Business Profile — Saligramam, Chennai
**Maintained by:** Propertism Admin / Antigravity

---

## Task Status Dashboard

| # | Task | Status | Owner |
|---|---|---|---|
| 1 | Claim your credit | ✅ Completed — Campaign created; no spend committed | Viji |
| 2 | Turn more views into customers | ✅ Completed | Viji |
| 3 | Share your Google QR | ✅ Completed — QR generated & PDF saved | Viji |
| 4 | Add update | ✅ Completed — New post published | Viji |
| 5 | Set up booking | ⏭️ Deferred — Current contact forms are sufficient | Product Decision |
| 6 | Get more reviews | ✅ Completed — Review link & QR generated | Viji |
| 7 | Add a map to your website | ✅ Completed — Homepage contact section integrated via SCCB | Antigravity |
| 8 | Add address autocomplete | ⏸️ Parked — Waiting for Google Maps Platform API enablement on `propertism-platform-maps-browser` | Propertism Admin |
| 9 | Add amenity map to your website | ⏸️ Parked — Phase 2 Feature (Property Details page, not homepage) | Product Decision |
| 10 | Create an offer | ✅ Completed | Viji |
| 11 | Get custom email | ⏭️ Skipped — Already using GoDaddy Business Email | Product Decision |
| 12 | Add directions to your website | ✅ Completed — Directions link embedded in contact section | Viji / Antigravity |
| 13 | Add your phone number | ⏳ Awaiting Google Approval | Viji |
| 14 | Get noticed by more customers (Add new photos) | ⏳ Awaiting photos from owner | Viji |

---

## Task 3 — Share Your Google QR

**Status:** ✅ Completed

### Assets
| Asset | Location |
|---|---|
| QR Code Image | `D:\viji\viji-olivine\03rolledout\01propertism\media\company\propertism-QRcode.png` |
| Review Link | https://g.page/r/CWE4qx3eFcR-EBE/review |

### Follow-up — Propertism-Branded Review Card

> Rather than using Google's default PDF everywhere, a branded Propertism Review Card should be created.

**Card Specification:**

| Element | Detail |
|---|---|
| Format | A5 or A6 — printable |
| Logo | Propertism logo (top) |
| Headline | "Review us on Google" |
| QR Code | `propertism-QRcode.png` |
| Message | Short thank-you message |
| Brand Colors | Matching Propertism palette (Gold `#B89A4A`, Deep Navy) |
| Layout | Clean, premium, print-ready |

**Rationale:** This will look significantly more professional than the default Google template and be fully consistent with the Propertism brand identity.

**Owner:** Antigravity (design) + Viji (approval)
**Priority:** Low — to be created when other tasks are stable

---

## Task 4 — Add Update (Google Posts Strategy)

**Status:** ✅ Initial post published

### Google Posts — Structured Rotation Strategy

Rather than posting randomly, all Google Posts should rotate across these content categories:

| # | Category | Frequency |
|---|---|---|
| 1 | Property Management | Monthly |
| 2 | NRI Services | Monthly |
| 3 | Success Stories | As available |
| 4 | Property Tips | Fortnightly |
| 5 | Company Updates | As needed |
| 6 | Customer Testimonials | As available |
| 7 | New Services | As launched |
| 8 | Festival Greetings | Seasonal |
| 9 | Market Insights | Monthly |
| 10 | Offers & Free Consultation | Quarterly |

### First Recommended Post — Brand Introduction

| Field | Value |
|---|---|
| **Headline** | Trusted Property Management in Chennai |
| **Content** | Looking for reliable property management in Chennai? Propertism Realty Advisors provides end-to-end services for NRIs and property owners, including tenant management, rent collection, maintenance coordination, resale assistance, and complete property care. Contact us today for a free consultation. |
| **Call-to-Action** | Learn More |
| **Button Link** | https://www.propertism.in/ |
| **Photo** | Hero banner or premium property management visual from brand assets |

---

## Task 6 — Get More Reviews

**Status:** ✅ Completed

### Assets

| Asset | Value |
|---|---|
| **Review Link** | https://g.page/r/CWE4qx3eFcR-EBE/review |
| **QR Code** | `D:\viji\viji-olivine\03rolledout\01propertism\media\company\propertism-QRcode.png` |

### Sharing Plan
- Share QR code on WhatsApp with clients post-service
- Include review link in email signature
- Add to Propertism-branded Review Card (see Task 3 follow-up)
- Print and display at office

---

## Task 7 — Add a Map to Your Website

**Status:** ✅ Completed via SCCB — SCCB-PROP-M2.X-MAPS-01

### Implementation — Phase 1 (Current — Completed)

| Item | Status |
|---|---|
| Responsive embedded Google Map on Contact page | ✅ Live |
| Responsive embedded Google Map on Homepage Contact section | ✅ Live |
| `loading="lazy"` on the iframe | ✅ Applied |
| Footer — external Google Maps link only (performance) | ✅ Preserved |
| Google Maps links upgraded to canonical Business Profile URL | ✅ Centralized in `settings.py` |
| Gold Map Border & Visual Alignment | ✅ 2px subtle gold border (`rgba(184, 154, 74, 0.35)`), flat corners, unified section header styling, optimized padding |

### Implementation — Phase 2 (Planned — Post-realBOT Integration)

Once realBOT is integrated, the following will be added:

- **"Get Directions" button** on the Contact page
- **realBOT location query support:**
  - "Where is your office?"
  - "Navigate to your office."
  - "How do I reach Propertism?"
  - All resolved using the canonical Google Business Profile link

### Canonical Source of Truth Architecture

The single canonical location reference must flow through:

```
settings.py (GOOGLE_BUSINESS_PROFILE_MAP_URL)
        │
        ├── Website Contact Page (embedded map iframe)
        ├── Website Footer (external link)
        ├── Homepage (external link)
        ├── Schema.org LocalBusiness (hasMap)
        ├── Google Business Profile
        ├── realBOT conversation engine
        └── Future ERP integrations
```

### Governance Decision — SCCB Reference

**SCCB-PROP-M2.X-GOOGLE-MAPS-INTEGRATION-001**
**Title:** Canonical Google Business Profile Maps Integration

**Scope:**
1. Embed responsive Google Map on Contact page only
2. Replace generic address query URLs with canonical Google Business Profile / Place ID URL
3. Centralize the map URL in `settings.py` so every page, schema, and future module references the same value
4. Preserve homepage and footer performance by keeping external links rather than embedded maps

---

## Task 8 — Add Address Autocomplete

**Status:** ⏸️ Parked

### Block Reason
Waiting for:
1. Google Maps Platform APIs enabled on `propertism-platform` project
2. Restricted API key `propertism-platform-maps-browser` created and provided

### GCP Project Details (Created)

| Field | Value |
|---|---|
| Project Name | Propertism Platform |
| Project ID | `propertism-platform` |
| Project Number | `809664944773` |
| Organization | `propertism-tamil-org` |
| Billing Account | To be linked |

### APIs to Enable on `propertism-platform`
- [ ] Maps JavaScript API
- [ ] Places API
- [ ] Maps Embed API

### Key Specification
| Field | Value |
|---|---|
| Key Name | `propertism-platform-maps-browser` |
| Type | Browser (HTTP Referrer restricted) |
| Referrers | `https://*.propertism.in/*`, `http://localhost:8001/*`, `http://127.0.0.1:8001/*` |
| API Restrictions | Maps JavaScript API, Places API, Maps Embed API |

### Code Ready
The address autocomplete framework is **fully implemented** and waiting only for the key:
- `static/js/address-autocomplete.js` — Framework JS ✅
- `templates/includes/_address_fields.html` — Reusable component ✅
- `templates/address_test.html` — Validation page at `/address-test/` ✅
- `settings.py` — `GOOGLE_MAPS_API_KEY` placeholder ✅
- `content/context_processors.py` — Key injected globally ✅

**To unpark:** Provide the new restricted API key → Antigravity rotates it in `settings.py` and `.env`.

---

## Task 9 — Add Amenity Map to Your Website

**Status:** ⏸️ Parked — Phase 2 Feature

**Reason:**
Neighborhood Discovery is valuable when browsing **individual properties**, not on the corporate marketing homepage. It will be implemented as part of the future **Property Search & Property Details** experience.

**Phase 2 Scope (When Property Details pages are built):**
- Map showing nearby amenities (schools, hospitals, metro, hospitals, parks) per property listing
- Implemented on Property Details page, not on homepage or Contact page
- Requires Places Nearby Search API (server-side, via `propertism-platform` service account)
- Scope includes: search radius configuration, category filters, distance display

**Owner:** Product Decision → Viji / Mindra (Phase 2)

---

## Task 12 — Add Directions to Your Website

**Status:** ⏳ Pending

**Planned Implementation:**
- "Get Directions" button on Contact page (Phase 2)
- Links to canonical Google Business Profile directions URL
- realBOT integration (Phase 2)

**Owner:** Viji / Antigravity

---

## Related SCCB Items

| SCCB ID | Title | Status |
|---|---|---|
| SCCB-PROP-M2.X-MAPS-01 | Google Business Profile Map — Contact Section | ✅ Complete |
| SCCB-PROP-M2.X-ADDRESS-AUTOCOMPLETE-FRAMEWORK-001 | Google Places Address Autocomplete Framework | ⏸️ Parked |
| SCCB-PROP-M2.X-GOOGLE-MAPS-INTEGRATION-001 | Canonical Google Business Profile Maps Integration | 📋 Governance Decision Recorded |

---

*Last updated: 2026-07-05 by Antigravity (Platform Integration Lead)*
