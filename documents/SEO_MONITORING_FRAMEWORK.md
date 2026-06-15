# Monthly SEO Monitoring Framework
**Propertism Realty Advisors | SCCB-PROP-SEO-CONTENT-AUTHORITY-EXECUTION-1506**

---

## 1. Monitoring Cadence

| Frequency | Activity |
|-----------|----------|
| Weekly | GSC coverage errors, manual index request status, GA4 conversion event spot-check |
| Monthly | Full KPI review against baselines, content gap assessment, pSEO quality re-run |
| Quarterly | Full SEO blocker reassessment, content cluster progress review, competitor gap analysis |

---

## 2. Primary KPI Tracking

### 2.1 Indexing Health

| Metric | Source | Baseline (Set at first measurement) | Target (Month 3) |
|--------|--------|--------------------------------------|------------------|
| Total indexed pages | GSC → Coverage | TBD | +20% vs baseline |
| Sitemap submitted pages | GSC → Sitemaps | TBD | 100% submitted |
| Pages with coverage errors | GSC → Coverage | TBD | 0 critical errors |
| Pages excluded (noindex) | GSC → Coverage | TBD | Only justified exclusions |

### 2.2 Organic Traffic

| Metric | Source | Baseline | Target (Month 3) |
|--------|--------|----------|------------------|
| Organic sessions | GA4 → Acquisition | TBD | +30% vs baseline |
| Organic impressions | GSC → Performance | TBD | +50% vs baseline |
| Average keyword position (NRI terms) | GSC → Performance | TBD | Top 20 for Tier 1 keywords |
| Organic clicks | GSC → Performance | TBD | +40% vs baseline |
| Click-through rate | GSC → Performance | TBD | >2.5% average |

### 2.3 Conversion Metrics (GA4)

| Event | Monthly Count | Source |
|-------|--------------|--------|
| whatsapp_click | TBD | GA4 Events |
| phone_call_click | TBD | GA4 Events |
| contact_form_submit | TBD | GA4 Events |
| resource_hub_click | TBD | GA4 Events |
| newsletter_subscribe | TBD | GA4 Events |

**Conversion rate targets:**
- Landing page → WhatsApp: >1.5%
- Landing page → Contact form: >0.8%
- Blog post → Service page click: >3%

### 2.4 Content Authority

| Metric | Source | Monthly Target |
|--------|--------|---------------|
| Knowledge hub articles published | CMS | 2–4 per month |
| Blog posts indexed | GSC | 100% of published |
| Average position for hub articles | GSC | Improving month-on-month |
| Organic sessions from blog URLs | GA4 | +10% month-on-month |

### 2.5 pSEO Quality

| Metric | Source | Target |
|--------|--------|--------|
| INDEX candidate pages | `analyse_pseo_config` CSV | >85% of total |
| REVIEW candidate pages | `analyse_pseo_config` CSV | <12% of total |
| NOINDEX candidate pages | `analyse_pseo_config` CSV | <3% of total |
| Duplicate titles | `analyse_pseo_config` CSV | 0 exact duplicates |

---

## 3. GSC Keyword Tracking List

Track these specific queries monthly in GSC Performance report:

**Tier 1 — Primary NRI Service Keywords**
- nri property management chennai
- sell property in india from abroad
- nri property management india
- property management for nri india
- nri sell property india

**Tier 2 — Legal / Documentation Keywords**
- power of attorney for nri property india
- patta transfer for nri tamil nadu
- encumbrance certificate chennai
- capital gains tax nri property india
- property tax chennai online

**Tier 3 — NRI Geo-Origin Keywords**
- manage property india from dubai
- sell property india from singapore
- nri property management from usa
- property management india from london

---

## 4. GA4 Custom Report Specifications

### Report 1: SEO → Conversion Funnel
- Dimensions: `page_type`, `service_intent`, `city_context`
- Metrics: Sessions, Event count (whatsapp_click), Event count (contact_form_submit)
- Filter: Medium = organic

### Report 2: Landing Page Performance
- Dimensions: `page_path`, `service_intent`
- Metrics: Sessions, Engagement rate, Conversions
- Filter: Page path contains `/chennai/` OR `/nri-`

### Report 3: Knowledge Hub Engagement
- Dimensions: `page_path`
- Metrics: Sessions, Average engagement time, resource_hub_click events
- Filter: Page path contains `/blog/`

### Report 4: NRI Geo-Origin Page Performance
- Dimensions: `page_path`, `city_context`
- Metrics: Sessions, Bounce rate, whatsapp_click
- Filter: page_type = landing, nri_origin present

---

## 5. Monthly Review Checklist

```
□ Pull GSC Performance report — record impressions, clicks, avg position
□ Check GSC Coverage — resolve any new errors
□ Check GA4 conversion events — verify all 5 events are firing
□ Run: python manage.py analyse_pseo_config --summary-only
□ Review REVIEW/NOINDEX counts — investigate any increases
□ Check knowledge hub publish count — confirm 2+ articles published
□ Verify sitemap last-updated timestamp in GSC
□ Check top 10 GSC queries by impressions — flag new keyword opportunities
□ Review any 404 errors in GSC — fix or redirect
□ Update baseline table above with current month actuals
```

---

## 6. Escalation Triggers

These conditions warrant immediate investigation outside the monthly cycle:

| Trigger | Action |
|---------|--------|
| Indexed pages drop >10% week-on-week | Check robots.txt, noindex tags, GSC manual actions |
| Organic sessions drop >20% week-on-week | Check GSC for crawl errors, algorithm update notes |
| GA4 conversion events drop to 0 | Verify ga4-conversion.js is loaded, check gtag config |
| GSC manual action notification | Address within 48 hours |
| Sitemap errors >5 URLs | Fix and resubmit within 24 hours |

---

## 7. Baseline Establishment Instructions

Run the following immediately after deployment and record outputs as the baseline:

1. `python manage.py analyse_pseo_config --summary-only` → record INDEX/REVIEW/NOINDEX counts
2. GSC Performance → last 28 days → record total impressions, clicks, average position
3. GA4 → last 28 days → record session count, conversion event counts
4. GSC Coverage → record total valid indexed pages

Store baselines in `.session-tracker/SESSION_TRACKER.md` under a dated entry.
