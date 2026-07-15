# SCCB-PDE-M1-INQUIRY-CONSUMER-FOUNDATION-001

**Status**: ✅ COMPLETED
**Date**: July 14, 2026
**Session**: 77
**Focus**: Deal Engine Inquiries Module, Buyer Discovery Mode Switch & UI Refinement

---

## Overview

Implemented the Inquiries consumer module within the Propertism Deal Engine frontend, enabling staff to view inbound Sell inquiries from propertism.in. Refactored the Buyer Discovery panel to support a mode switch between AI-discovered leads and web inquiries, with unified grid-based selection and automatic buyer matching. Relocated the Serper API quota display to the sidebar for persistent visibility.

---

## Changes Made

### 1. Deal Engine — Inquiries View (`index.html`)

**New UI Section:**
- Added `<div class="view" id="inquiries-view">` with empty state and data table
- Empty state shows kicker ("INQUIRIES"), title ("No inquiries yet"), and description
- Data table columns: Name, Phone, Email, Property, Location, Received

**Sidebar Navigation:**
- Added `inquiries` nav item with `contact_mail` icon and subtitle "Inbound inquiries from propertism.in"
- Registered routing path `/propertism/deal-engine/inquiries`
- `switchModule('inquiries')` load integration

**API Integration:**
- Added `inquiriesList: () => GET(\`\${DEAL_ENGINE_API_PREFIX}/inquiries\`)` to API client
- Implemented `loadInquiries()` async function fetching Sell inquiries from the REST API
- Renders table body or shows connection-failed error state

**AppState:**
- Added `inquirySortOrder: 'desc'` to AppState
- Added `AppState.inquiriesList` for cached inquiry records

### 2. Buyer Discovery — Mode Switch (AI Discovered / Web Inquiries)

**Radio Toggle UI:**
- Replaced fixed lead selector filter group with inline radio buttons:
  - `AI Discovered` (default, checked)
  - `Web Inquiries`
- `onBuyerDiscoveryModeChange(mode)` toggles visibility of lead selector vs inquiry selector
- `getActiveBuyerDiscoveryMode()` reads the active radio value

**Lead & Inquiry Selectors:**
- `populateBuyerDiscoveryLeadSelector()` — populates from shortlist + direct leads APIs, caches in `AppState.allLeadsList`
- `populateBuyerDiscoveryInquirySelector()` — populates from `dealEngineAPI.inquiriesList()`, uses `inquiry:id` prefix
- `syncBuyerLeadSelectorValue()` — manages synchronized state between both selectors
- `onBuyerDiscoveryInquiryChange()` — selects inquiry, clears lead selector, sets `AppState.selectedLead`, triggers `runBuyerDiscoverySearch()`

**Grid Rendering:**
- `renderLeadGrid()` — renders a grid of lead cards with header showing count + sort toggle
- `renderInquiryGrid()` — renders a grid of inquiry cards with header showing count + sort toggle
- `renderLeadCard(lead, index)` — uniform key-value catalog card (Name, Location, Intent, Confidence, Source, Updated, Details)
- `renderInquiryCard(inquiry, index)` — uniform key-value catalog card (Name, Contact, Location, Intent, Date, Message)
- `toggleInquirySort()` — toggles between 'asc' (oldest first) and 'desc' (latest first) within AppState

**Lead Selection:**
- `selectLeadById(leadId)` — universal handler supporting both `inquiry:id` prefixed and regular IDs
- `selectInquiryFromGrid(inquiryId)` — delegates to `selectLeadById`
- `selectLeadFromGrid(leadId)` — delegates to `selectLeadById`
- `getBuyerCandidateById(normalizedId)` — unwraps inquiry prefix to locate cached inquiry records
- Unified lead resolution: shortlist lookup, direct lead lookup, inquiry record lookup

**Navigation Integration:**
- `switchToBuyerDiscovery()` populates both selectors and renders appropriate grid based on active mode
- `resetBuyerDiscoveryView()` clears selected lead state and renders empty state matching active mode
- `loadBuyerDiscovery()` populates both selectors and renders lead grid or inquiry grid

### 3. Buyer Discovery — Results Table Refactoring

**Table Layout:**
- Replaced card-based tree layout with responsive `<table>` with sticky header
- Columns: Checkbox, Business Name (with % Match badge + stars), Category, Area, Contact (phone/email), Status, Actions
- `toggleSelectAllBuyerRows(checked)` — batch checkbox toggling
- Contact info renders inline with SVG icons (Phone, Email) with structured layout

**Helper Functions:**
- `getBuyerCandidatePhone(buyer)` — extracts phone from buyer or meta
- `getBuyerCandidateEmail(buyer)` — extracts email from buyer or meta
- `getBuyerCandidateReviewsCount(buyer)` — extracts reviews count
- `getBuyerCandidateRating(buyer)` — extracts rating

**Status Management:**
- Status dropdown: Pending, Scanned, Rejected, Discovered, Qualified
- `updateBuyerCandidateStatus(index, newStatus)` — updates in-place with toast notification

**Buyer Details Modal:**
- Added `<div id="buyer-details-modal">` overlay with close-on-backdrop-click
- `showBuyerCandidateDetails(index)` — populates modal with full buyer info (title, match score, location, phone, email, profile link, business insights)
- `closeBuyerDetailsModal()` — hides modal

**Signal Pills & Empty State:**
- `getBuyerMatchEmptyState(mode)` — returns empty state HTML based on active discovery mode
- `syncBuyerSignalPillState()` — maintained
- `renderBuyerDiscoveryResults()` — renders table HTML or empty state

### 4. Serper Quota Sidebar Indicator

**Sidebar Widget:**
- Added `#sidebar-serper-quota-container` in sidebar footer section
- Shows Serper API remaining/limit with gold icon and color styling
- Includes settings button to open `showCdKeysModal()`
- Hidden when sidebar is collapsed via CSS rule

**Quota Updates:**
- `cdUpdateSerperQuota(data.serper_quota)` — updates sidebar indicator
- Color-coded: gold for normal, red (#ef4444) when remaining < 10
- Removed old quota bar from community-discovery header

---

## Files Modified

| File | Change |
|------|--------|
| `index.html` | Added inquiries view, sidebar nav, mode switch, grid renderers, table refactoring, quota sidebar, buyer details modal |
| `.claude/settings.json` | Added `"model": "opus"` |
| `.claude/settings.local.json` | Added `Skill(update-config)` permissions |
| `lead_discovery_debug.json` | Updated run data |
| `lead_discovery_timing.json` | Updated timing data |

---

## Key Functions Added

| Function | Purpose |
|----------|---------|
| `loadInquiries()` | Fetches and renders Sell inquiries table from Deal Engine API |
| `onBuyerDiscoveryModeChange(mode)` | Toggles between AI Discovered and Web Inquiries modes |
| `getActiveBuyerDiscoveryMode()` | Returns active radio mode value |
| `populateBuyerDiscoveryInquirySelector()` | Populates inquiry dropdown from API |
| `onBuyerDiscoveryInquiryChange()` | Handles inquiry selection and auto-matching |
| `selectLeadById(leadId)` | Universal lead/inquiry selection handler |
| `selectInquiryFromGrid(inquiryId)` | Inquiry grid click handler |
| `selectLeadFromGrid(leadId)` | Lead grid click handler |
| `renderLeadGrid()` | Renders lead card grid with sort |
| `renderInquiryGrid()` | Renders inquiry card grid with sort |
| `renderLeadCard(lead, index)` | Individual lead card renderer |
| `renderInquiryCard(inquiry, index)` | Individual inquiry card renderer |
| `toggleInquirySort()` | Toggles date sort order |
| `toggleSelectAllBuyerRows(checked)` | Batch checkbox toggle |
| `updateBuyerCandidateStatus(index, status)` | Status update with toast |
| `showBuyerCandidateDetails(index)` | Buyer details modal populator |
| `closeBuyerDetailsModal()` | Modal close |
| `getBuyerCandidatePhone(buyer)` | Phone extraction helper |
| `getBuyerCandidateEmail(buyer)` | Email extraction helper |
| `getBuyerCandidateReviewsCount(buyer)` | Reviews count helper |
| `getBuyerCandidateRating(buyer)` | Rating extraction helper |

---

## Verification

- ✅ Inquiries view renders empty state when no data
- ✅ Inquiries view renders table when data exists
- ✅ Error state handles API failures gracefully
- ✅ Mode switch toggles between AI Discovered and Web Inquiries
- ✅ Inquiry selector populates from Deal Engine API
- ✅ Inquiry selection triggers auto buyer discovery search
- ✅ Lead grid renders with sort controls
- ✅ Inquiry grid renders with sort controls
- ✅ Buyer results render as responsive table
- ✅ Buyer details modal shows full info
- ✅ Serper quota indicator displays in sidebar
- ✅ Sidebar collapse hides quota indicator

---

## Future Recommendations

1. **Paginate inquiries list** — Add server-side pagination for large inquiry volumes
2. **Inquiry detail panel** — Implement a side panel or inline detail view for selected inquiries
3. **Bulk actions** — Add multi-select actions (batch status update, batch match) to inquiry and lead grids
4. **Inquiry search/filter** — Add search bar and status filter to the inquiries view
5. **Export inquiries** — Add CSV export for inquiries table
