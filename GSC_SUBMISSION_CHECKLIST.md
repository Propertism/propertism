# GOOGLE SEARCH CONSOLE (GSC) SUBMISSION CHECKLIST

## Phase 5 — Accelerated Indexing & Authority Building

**Document Date:** 2026-06-16  
**Status:** Ready for Execution  
**Target Property:** https://www.propertism.in

---

## PRE-SUBMISSION VERIFICATION (COMPLETE BEFORE GSC ACTIONS)

Execute these checks before attempting any GSC submissions.

### [ ] 1. GSC Property Verification

- [ ] Log into Google Search Console
- [ ] Verify "propertism.in" property exists
- [ ] Verify "www.propertism.in" property exists (if separate)
- [ ] Ensure property is NOT in review or pending state
- [ ] Check "Settings" → "Ownership verified"

**If not verified:** Verify property via DNS TXT record or HTML file upload before proceeding.

### [ ] 2. GSC Health Check

- [ ] Go to **Coverage** report
- [ ] Review for any **"Excluded"** items (should be minimal)
- [ ] Check **"Errors"** tab (should be 0 or very low)
- [ ] Check **"Valid with warnings"** (note count for baseline)
- [ ] Go to **"Core Web Vitals"** report (note current state)

### [ ] 3. Robots.txt Verification

- [ ] Go to **Settings** → **Crawlers and user-agents**
- [ ] Verify robots.txt is NOT blocking `/blog/` paths
- [ ] Verify robots.txt is NOT blocking `/sitemap.xml`
- [ ] Test: Navigate to https://www.propertism.in/robots.txt
- [ ] Confirm response is 200 OK
- [ ] Confirm contains: `Sitemap: https://www.propertism.in/sitemap.xml`

### [ ] 4. URL Accessibility Test

- [ ] Test homepage: https://www.propertism.in/ → Should load without errors
- [ ] Test blog article: https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/ → Should load
- [ ] Test service page: https://www.propertism.in/chennai/nri-property-management/ → Should load
- [ ] All URLs should return **200 OK** status

---

## TASK 1: SITEMAP SUBMISSION

### Step 1: Remove Previous Sitemaps (if any)

1. **Open GSC Dashboard** → Select "propertism.in" property
2. **Left menu** → Click **"Sitemaps"**
3. **Check existing sitemaps:**
   - If sitemaps exist with status "FAILED" or "ERROR"
   - [ ] Click the sitemap name
   - [ ] Click **"Remove"** button
   - [ ] Confirm removal
   - [ ] Wait for 1 minute

### Step 2: Submit Sitemap

1. **In Sitemaps page**, find the **"Add/Test sitemap"** box (top right)
2. **Enter sitemap URL:**
   ```
   sitemap.xml
   ```
   (GSC will auto-prepend the domain)

3. **Click "Submit"** button
4. **Expected response:** "Submitted" or "Sitemaps submitted successfully"

### Step 3: Monitor Sitemap Status

1. **Refresh Sitemaps page** (may take 1–5 minutes to appear)
2. **Look for:**
   - [ ] Sitemap URL: `https://www.propertism.in/sitemap.xml`
   - [ ] Status: `SUCCESS` or `PROCESSING`
   - [ ] URLs Read: Should show ~765
   - [ ] Submitted URLs: Should match

3. **If "ERROR" appears:**
   - Click on the error message
   - Read the error description
   - Common issues:
     - Robots.txt blocks sitemap (verify robots.txt)
     - Sitemap not returning XML (test directly in browser)
     - Network error (retry after 1 hour)

### Success Criteria

- [ ] Sitemap status shows **"SUCCESS"**
- [ ] URL count shows **~765 URLs**
- [ ] No errors or warnings on sitemap

---

## TASK 2: URL INDEXING REQUESTS

### Step 1: Homepage Indexing Request

1. **Open GSC** → Select "propertism.in"
2. **Top search bar** → Click the "URL Inspection" icon (magnifying glass)
3. **Paste URL:**
   ```
   https://www.propertism.in/
   ```
4. **Wait for inspection** (30–60 seconds)
5. **Response should show:**
   - URL status: "Indexed" or "Not indexed"
   - If "Not indexed" or you see "Request indexing" button:
     - [ ] Click **"Request indexing"** button
     - [ ] Confirm **"Request sent"** notification appears
     - [ ] Screenshot for records
6. **If already indexed:**
   - No action needed (good sign)
   - Proceed to next URL

**URL:** https://www.propertism.in/

| Status | Action |
|---|---|
| Already indexed | Move to next URL |
| Not indexed + "Request indexing" button visible | Click button |
| Error/Cannot index | Log error, proceed to next |

---

### Step 2: Core Service Pages (2 URLs)

Repeat the URL Inspection process for each:

#### URL 1: NRI Property Management

**URL:**
```
https://www.propertism.in/chennai/nri-property-management/
```

- [ ] Paste in URL Inspection tool
- [ ] Wait for inspection
- [ ] Click "Request indexing" if available
- [ ] Confirm "Request sent"

#### URL 2: NRI Sell Property

**URL:**
```
https://www.propertism.in/chennai/nri-sell-property/
```

- [ ] Paste in URL Inspection tool
- [ ] Wait for inspection
- [ ] Click "Request indexing" if available
- [ ] Confirm "Request sent"

---

### Step 3: Knowledge Hub Articles (10 URLs)

Repeat the URL Inspection process for EACH article below:

#### Article 1
**URL:**
```
https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/
```
- [ ] Request indexing submitted

#### Article 2
**URL:**
```
https://www.propertism.in/blog/how-nris-can-sell-property-in-india-from-abroad/
```
- [ ] Request indexing submitted

#### Article 3
**URL:**
```
https://www.propertism.in/blog/power-of-attorney-for-nris-complete-guide/
```
- [ ] Request indexing submitted

#### Article 4
**URL:**
```
https://www.propertism.in/blog/how-to-verify-property-documents-chennai/
```
- [ ] Request indexing submitted

#### Article 5
**URL:**
```
https://www.propertism.in/blog/patta-transfer-process-explained/
```
- [ ] Request indexing submitted

#### Article 6
**URL:**
```
https://www.propertism.in/blog/encumbrance-certificate-guide-for-nris/
```
- [ ] Request indexing submitted

#### Article 7
**URL:**
```
https://www.propertism.in/blog/property-tax-guide-chennai-nris/
```
- [ ] Request indexing submitted

#### Article 8
**URL:**
```
https://www.propertism.in/blog/capital-gains-tax-property-sale-nris/
```
- [ ] Request indexing submitted

#### Article 9
**URL:**
```
https://www.propertism.in/blog/tenant-management-guide-overseas-property-owners/
```
- [ ] Request indexing submitted

#### Article 10
**URL:**
```
https://www.propertism.in/blog/nri-property-maintenance-checklist/
```
- [ ] Request indexing submitted

---

## TASK 3: POST-SUBMISSION MONITORING

### Immediate (Within 1 Hour)

- [ ] Refresh Sitemaps page
- [ ] Confirm sitemap status is not "ERROR"
- [ ] No new crawl errors in Coverage report

### Daily (Days 1–7)

1. **Monitor Coverage Report:**
   - [ ] Daily: Check "Indexed" count (should increase)
   - [ ] Daily: Check "Errors" count (should stay low)
   - [ ] Log daily index count (spreadsheet or notes)

2. **Monitor Core Web Vitals:**
   - [ ] Check if any new pages appear in CWV report
   - [ ] Note baseline metrics for Month-0 document

### Weekly (Weeks 1–4)

1. **Coverage Trending:**
   - [ ] Document indexed URL count each week
   - [ ] Compare week-over-week growth
   - [ ] Expected: 50% indexed by week 2, 80%+ by week 4

2. **URL Inspection Follow-up:**
   - [ ] For 2–3 Knowledge Hub articles
   - [ ] Use URL Inspection to verify they're now indexed
   - [ ] Screenshot for evidence

3. **Indexation Pattern:**
   - [ ] Note which types of pages index first (service, blog, etc.)
   - [ ] Note indexation speed (hours vs. days)

---

## EXPECTED TIMELINE

| Timeframe | Expected Status |
|---|---|
| **Immediately after submission** | Sitemap shows "Processing" or "Success" |
| **Within 24 hours** | GSC begins crawling URLs from sitemap |
| **Days 1–3** | First indexed URLs appear in Coverage |
| **Week 1** | ~50–150 URLs indexed |
| **Week 2** | ~150–300 URLs indexed |
| **Week 4** | ~300–500 URLs indexed |
| **Week 8** | ~500–650 URLs indexed (80%+) |

---

## TROUBLESHOOTING

### Sitemap Submission Fails

**Error: "Submitted but not indexed"**

- **Action 1:** Verify robots.txt doesn't block `/sitemap.xml`
- **Action 2:** Test https://www.propertism.in/sitemap.xml in browser (should return XML)
- **Action 3:** Resubmit after 24 hours
- **Action 4:** Check GSC "Tools" → "Fetch as Google" to test crawlability

**Error: "Invalid sitemap format"**

- **Cause:** Sitemap XML is malformed
- **Action 1:** Test sitemap directly in browser
- **Action 2:** Validate using https://www.xml-sitemaps.com/validate-xml-sitemap.html
- **Action 3:** Contact tech support if validation fails

### URLs Not Indexing

**Issue: "URL cannot be indexed" message**

- **Check 1:** Verify URL returns 200 OK status (test in browser)
- **Check 2:** Verify URL is not blocked by robots.txt
- **Check 3:** Verify URL has no noindex tag
- **Check 4:** Check for redirect loops or chains
- **Action:** Fix blocking issue, then request indexing again

**Issue: "Indexing request sent but no indexation after 7 days"**

- **Common causes:**
  - New domain (less than 6 months old)
  - Low site authority/backlinks
  - Content quality concerns
  - Duplicate content
- **Action:** Proceed to Phase 5 Week 2+ backlink strategy

---

## COMPLETION CHECKLIST

### Submission Complete

- [ ] Sitemap submitted to GSC
- [ ] Sitemap status: SUCCESS or PROCESSING
- [ ] 13 URL indexing requests submitted (1 homepage + 2 service + 10 blog)
- [ ] All "Request indexing" buttons clicked
- [ ] No unresolved errors in GSC

### Monitoring Setup

- [ ] Bookmarked GSC Coverage report
- [ ] Set phone reminder to check daily for first week
- [ ] Created spreadsheet/notes for weekly tracking
- [ ] Identified team member responsible for monitoring

### Documentation

- [ ] Screenshots taken of sitemap submission
- [ ] Screenshots taken of indexing requests
- [ ] Baseline metrics recorded (initial Coverage state)
- [ ] Submitted to project documentation folder

---

## NEXT PHASE TASKS

After GSC submission is complete:

1. **Monitor Indexation (Weeks 1–4)**
   - Daily check of Coverage report
   - Weekly documentation of indexing growth

2. **Establish Month-0 Baseline (Week 1)**
   - Capture GSC metrics: Impressions, Clicks, Position
   - Capture GA4 metrics: Sessions, Events, Conversions
   - Create Month-0 baseline document

3. **Monitor Rankings (Weeks 2–4)**
   - Begin tracking keyword rankings for target terms
   - Focus on: "nri property management chennai", "nri sell property", etc.
   - Expected: Initial organic impressions within 2–3 weeks

4. **Begin Backlink Strategy (Week 4+)**
   - Identify high-authority NRI & property sites for outreach
   - Prepare Knowledge Hub articles for guest posting
   - Execute backlink acquisition plan

---

**Status:** Ready for Execution  
**Date:** 2026-06-16  
**Next Review:** After sitemap submission (within 24 hours)

---
