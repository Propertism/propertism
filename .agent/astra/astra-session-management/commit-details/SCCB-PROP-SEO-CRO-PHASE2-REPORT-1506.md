# SCCB-PROP-SEO-CRO-PHASE2 — Implementation Report
**Date**: June 15, 2026
**Prepared by**: Astra (Platform Integration Lead)
**System**: Propertism Realty Advisors LLP
**Environment**: Production (propertism-prod-2026 / AWS EB + CloudFront)

---

## EXECUTIVE SUMMARY

This report documents the implementation status of all 7 phases defined in `SCCB-PROP-SEO-CRO-PHASE2-IMPLEMENTATION-1506`. Phases 2, 3, and 5 have been fully implemented. Phases 1 and 6 are audit/validation phases requiring live production access or external tooling. Phases 4 and 7 require product decisions and external service integrations.

---

## PHASE 1 — SEO VALIDATION AUDIT

**Status**: ⚠️ PARTIAL — Infrastructure fixed, full audit pending post-deployment

### Completed Validation:
| Endpoint | Status |
|---|---|
| `https://www.propertism.in/sitemap.xml` | ✅ 200 OK |
| `https://www.propertism.in/robots.txt` | ✅ 200 OK |
| `https://propertism.in/sitemap.xml` | ⏳ 404 → 301 pending CF invalidation |
| `https://propertism.in/robots.txt` | ⏳ 404 → 301 pending CF invalidation |

### CloudFront Invalidations Executed:
- `I2YOTS6CFBOV7QTIO9SIM8ML7P` — Full `/*` invalidation (June 15, 13:14 UTC)
- `I6ATFOCDWDLBLHJ7YT6ZRAAFQU` — Targeted `/robots.txt`, `/sitemap.xml` (June 15, 16:42 UTC)

### Canonical URL Generation:
- `BaseSitemap` class hardcodes `www.propertism.in` as canonical host ✅
- All sitemap URLs correctly reference `https://www.propertism.in/...` ✅
- `robots.txt` references `https://www.propertism.in/sitemap.xml` ✅

### Remaining Audit Items (requires external tools):
- `site:propertism.in` index count — requires Google Search Console / manual check
- Duplicate title/meta description detection — requires Screaming Frog or GSC
- Core Web Vitals baseline — requires PageSpeed Insights / CrUX data
- Internal linking effectiveness — requires crawl tool

---

## PHASE 2 — DJANGO SITES FRAMEWORK CLEANUP

**Status**: ✅ COMPLETE (was already correct)

### Verified via shell:
```
ID: 1 | Domain: www.propertism.in | Name: Propertism
```

No migration needed. Django Sites framework correctly configured. Sitemap URLs are independent of this (using `BaseSitemap` hardcoded canonical host), so there is zero risk.

---

## PHASE 3 — PAGE SPEED & CORE WEB VITALS OPTIMIZATION

**Status**: ✅ COMPLETE

### WebP Conversion Results:
| Asset | Original | WebP | Reduction |
|---|---|---|---|
| `propertism-hero-bg.jpg` | 1,547 KB | 196 KB | **87.3%** |
| `hero-bg.jpg` | 1,547 KB | 196 KB | **87.3%** |
| `placeholder-property.jpg` | 20 KB | 5 KB | **76.5%** |

### Implementation Details:
- `static/images/propertism-hero-bg.webp` — generated at quality 82 ✅
- `static/images/hero-bg.webp` — generated at quality 82 ✅
- `static/images/placeholder-property.webp` — generated ✅
- `static/css/premium-styles.css` — both CSS background-image references updated to `.webp` ✅
- `uilayers/templates/socialaccount/login.html` — background updated to `.webp` ✅

### LCP / CLS Improvements:
- Hero `<img>` tags: `fetchpriority="high"` on first image, `loading="lazy"` on rotator images ✅
- Hero `<img>` tags: `width="1920" height="1080"` added (prevents CLS) ✅
- Property card images: `loading="lazy"` + `width="600" height="400"` ✅
- Blog featured image: `loading="lazy"` + `width="1200" height="480"` ✅
- `<link rel="preload">` for `propertism-hero-bg.webp` added to `base.html` ✅

### Estimated Impact:
- LCP improvement: ~1.5–2s reduction (hero image 1.5MB → 196KB)
- CLS: Near 0 (explicit width/height on all key images)
- Mobile Performance Score estimate: 75 → 85+

---

## PHASE 4 — PREMIUM CRO ENHANCEMENTS

**Status**: ⏳ PENDING — Requires product decisions

### 4A — Timezone-Aware Consultation Scheduling
**Not implemented** — requires:
- Calendly account setup (or equivalent: Cal.com, TidyCal)
- Embed URL from Propertism's calendar
- Decision on which pages to surface CTAs

**Recommended next action**: Create a Calendly account at `calendly.com/propertism`, configure a "30-min NRI Property Consultation" event type, then provide the embed URL to implement.

### 4B — NRI Owner Dashboard Trust Visualizations
**Not implemented** — requires:
- Design decision on which mockup format (HTML component vs. static images)
- Content for each dashboard panel (inspection reports, maintenance tickets, etc.)

**Recommended next action**: Confirm whether this should be a static HTML showcase section or image-based mockups.

### 4C — Trust Signal Expansion
**Not implemented** — requires:
- Content approval for process visualization copy
- "How We Manage Your Property Remotely" section copy

**Recommended next action**: Provide approved copy/content for the trust section.

---

## PHASE 5 — STRUCTURED DATA EXPANSION

**Status**: ✅ COMPLETE

### Existing (already implemented before this session):
| Schema | Implementation |
|---|---|
| Organization / RealEstateAgent | `organization_schema` tag in `base.html` ✅ |
| Service Schema | `service_schema` tag in `landing_page.html` ✅ |
| FAQ Schema | `faq_schema` tag in `landing_page.html` (sell intent) ✅ |
| Breadcrumb Schema | `breadcrumb_schema` tag — partial ✅ |
| Property Schema | `property_schema` tag available ✅ |

### Added this session:
| Schema | Page | Status |
|---|---|---|
| Article Schema | `blog_post.html` | ✅ NEW |
| Breadcrumb Schema | `blog_post.html` | ✅ NEW |
| Breadcrumb Schema | `city_hub.html` | ✅ NEW |
| Breadcrumb Schema | `management.html` | ✅ NEW |
| Organization Schema | `management.html` | ✅ NEW |
| `breadcrumbs` context | `content/views.py` → `blog_post()` | ✅ NEW |

### LocalBusiness Schema:
Already embedded inside `Service` schema as a `provider` sub-object on landing pages. Standalone `LocalBusiness` schema could be added to `base.html` as an additional schema block — low priority since `RealEstateAgent` is a subtype of `LocalBusiness`.

### Validation:
- All schema tags use `json.dumps` for valid JSON-LD output ✅
- `article_schema` handles missing `published_date`, `updated_date`, `featured_image` gracefully ✅
- Django system check: **0 issues** ✅

---

## PHASE 6 — PROGRAMMATIC SEO QUALITY HARDENING

**Status**: ⏳ PENDING — Requires dedicated crawl session

### Scope:
- 420+ pSEO pages across city × intent × NRI location combinations
- Generated via `LandingPageSitemap` from `CITIES` × `get_all_intents()` × `NRI_LOCATIONS`

### What needs to be done:
1. Run Screaming Frog or custom Django management command to crawl all pSEO URLs
2. Extract H1, title, meta description for each
3. Flag duplicates and thin pages
4. Implement `noindex` for pages below quality threshold

### Recommended approach (code-ready):
A Django management command can be written to:
- Generate all pSEO URLs
- Render each page's H1, title, meta description
- Output a CSV for review

**Estimated effort**: 2–3 hours implementation + human review of output.

---

## PHASE 7 — CONVERSION TRACKING ENHANCEMENTS

**Status**: ⏳ PENDING — GA4 is installed, events need configuration

### Current State:
- GA4 (`G-WZCH8BV34J`) is installed in `base.html` ✅
- No custom event tracking implemented

### Events to implement:
| Event | Trigger | Method |
|---|---|---|
| `whatsapp_click` | WhatsApp CTA click | GA4 `gtag('event')` |
| `phone_call_click` | Phone number click | GA4 `gtag('event')` |
| `contact_form_submit` | Form POST success | Server-side or JS |
| `newsletter_subscribe` | Newsletter form POST | Server-side |
| `scroll_depth` | 25/50/75/100% scroll | GA4 scroll trigger |
| `resource_hub_click` | Resource link click | GA4 `gtag('event')` |
| `consultation_booking` | Calendly booking | Calendly webhook → GA4 |

**Recommended next action**: Implement WhatsApp click tracking first (highest conversion signal) — 30-line JS addition.

---

## DELIVERABLES STATUS

| # | Deliverable | Status |
|---|---|---|
| 1 | SEO validation report | ✅ Partial (infrastructure fixed, audit pending) |
| 2 | Core Web Vitals optimization report | ✅ Complete (87% image reduction) |
| 3 | CRO enhancement implementation | ⏳ Pending product decisions |
| 4 | Structured data validation report | ✅ Complete |
| 5 | Programmatic SEO quality audit findings | ⏳ Pending dedicated crawl session |
| 6 | Analytics implementation summary | ⏳ Pending GA4 event configuration |
| 7 | Ranked blockers for Top-10 rankings | ✅ See below |

---

## RANKED BLOCKERS — TOP-10 NRI PROPERTY KEYWORDS

### Critical (Fix Now):
1. **`propertism.in` apex 404** — CloudFront invalidation in progress. GSC can't index apex domain. Priority: P0.
2. **GSC sitemap not submitted for `www`** — Must resubmit `https://www.propertism.in/sitemap.xml` in GSC after invalidation confirms.
3. **No consultation scheduling CTA** — Passive WhatsApp inquiry has high friction for international users in different timezones.

### High (Fix This Week):
4. **Core Web Vitals — LCP** — Hero image was 1.5MB. Now 196KB (WebP). Deploy and measure impact.
5. **Article schema missing from blog** — Fixed this session. Blogs now eligible for Google rich results.
6. **Breadcrumb schema gaps** — Fixed this session on management, city hub, blog pages.

### Medium (Fix This Month):
7. **pSEO thin pages** — 420+ pages, unknown quality distribution. Some may have near-duplicate content. Needs audit.
8. **GA4 event tracking** — No WhatsApp click signals going to Google. Can't optimize what you can't measure.
9. **NRI trust visualizations missing** — Competitors with dashboard mockups convert better on management intent pages.

### Lower Priority:
10. **LocalBusiness schema standalone** — Currently embedded inside Service schema. Standalone version would improve local pack eligibility.
11. **FAQ schema on management/about pages** — Currently only on sell-intent landing pages.
12. **Image alt text quality on pSEO pages** — May have empty or generic alt text.

---

## FILES MODIFIED THIS SESSION

| File | Change |
|---|---|
| `content/templatetags/seo_tags.py` | Added `article_schema` tag |
| `content/views.py` | Added `breadcrumbs` to `blog_post()` view |
| `uilayers/templates/blog_post.html` | Added Article + Breadcrumb schema, `loading="lazy"`, dimensions |
| `uilayers/templates/management.html` | Added structured_data block with Organization + Breadcrumb schema |
| `uilayers/templates/city_hub.html` | Added Breadcrumb schema |
| `uilayers/templates/home/sections/_hero.html` | `fetchpriority`, `loading="lazy"`, width/height on hero images |
| `uilayers/templates/home/sections/_properties.html` | `loading="lazy"` + dimensions + WebP placeholder |
| `uilayers/templates/base.html` | Added `<link rel="preload">` for hero WebP |
| `static/css/premium-styles.css` | Updated hero background references to `.webp` |
| `uilayers/templates/socialaccount/login.html` | Updated background to `.webp` |
| `static/images/propertism-hero-bg.webp` | NEW — 87% smaller than JPEG |
| `static/images/hero-bg.webp` | NEW — 87% smaller than JPEG |
| `static/images/placeholder-property.webp` | NEW — 76% smaller than JPEG |

---

## NEXT ACTIONS (PRIORITY ORDER)

1. **Run `commit-push.bat`** — Deploy all changes to production via CI/CD
2. **Wait 10 mins** — Confirm `propertism.in/robots.txt` returns 301 → `www.propertism.in`
3. **GSC** — Resubmit `https://www.propertism.in/sitemap.xml` under Domain Property `propertism.in`
4. **PageSpeed Insights** — Run `https://www.propertism.in/` after deploy to measure LCP improvement
5. **Calendly** — Set up consultation calendar (Phase 4A)
6. **GA4 Events** — Implement WhatsApp click tracking (Phase 7, highest ROI)
7. **pSEO Audit** — Write management command for quality scan (Phase 6)

---
*Report prepared by Astra | June 15, 2026 | CODEX-SESSION-1506-B*
