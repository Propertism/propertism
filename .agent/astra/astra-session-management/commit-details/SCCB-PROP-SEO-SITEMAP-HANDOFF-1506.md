# SCCB-PROP-SEO-SITEMAP-HANDOFF-1506
## Handoff Document — SEO Sitemap Fetch Fix & Footer V4 Optimization
**Date**: June 15, 2026  
**Session**: Astra — Platform Integration Lead  
**Status**: IN PROGRESS — Awaiting CloudFront invalidation propagation + GSC revalidation

---

## PART 1: SEO / INFRASTRUCTURE FIX

### Problem Statement
Google Search Console reported `"Couldn't fetch"` for `https://propertism.in/sitemap.xml`:
- Type: Unknown
- Discovered Pages: 0
- `https://propertism.in/sitemap.xml` → HTTP 404
- `https://propertism.in/robots.txt` → HTTP 404

### Investigation Summary

| Phase | Finding |
|---|---|
| Phase 1 | `propertism.in/*` returns 404, `www.propertism.in/*` returns 200 |
| Phase 2 | No redirect from apex to www |
| Phase 3 | Route53: Not used — DNS on GoDaddy |
| Phase 4 | AWS CLI was pointing to wrong account (Olivine `673981388490`) |
| Phase 5 | Correct account: Propertism `622370466597` (profile: `default`) |
| Phase 6 | CloudFront `E1GGPU208SQFFT` (`d1yv5od4i0bho.cloudfront.net`) — both `propertism.in` and `www.propertism.in` aliased ✅ |
| Phase 7 | OriginRequestPolicy `216adef6` → `allViewer` — Host header forwarded ✅ |
| Phase 8 | nginx: `proxy_set_header Host $host` — Host reaches Django ✅ |
| Phase 9 | Django `CanonicalDomainRedirectMiddleware` correctly configured ✅ |
| **Root Cause** | **CloudFront was caching stale 404 responses** — no invalidation had been run |

### Infrastructure Map

```
propertism.in  (GoDaddy DNS)
      ↓  CNAME
d1yv5od4i0bho.cloudfront.net  (CF: E1GGPU208SQFFT)
      ↓  allViewer OriginRequestPolicy
propertism-prod-2026.us-east-1.elasticbeanstalk.com  (EB: e-jcbmtpnpvx)
      ↓  nginx proxy_set_header Host $host
Gunicorn → Django
      ↓  CanonicalDomainRedirectMiddleware
301 → https://www.propertism.in/*
```

### Fix Applied

**CloudFront Cache Invalidation** — `/*` — Distribution `E1GGPU208SQFFT`:
```
Invalidation ID:  I2YOTS6CFBOV7QTIO9SIM8ML7P
Status:           InProgress (at time of session)
CreateTime:       2026-06-15T13:14:45.461Z
Paths:            /*
```

### Pending Validation (Next Session)

Run these checks after invalidation completes (~5–15 mins):

```powershell
# Should return 301 → https://www.propertism.in/sitemap.xml
Invoke-WebRequest -Uri "https://propertism.in/sitemap.xml" -MaximumRedirection 0 -UseBasicParsing

# Should return 301 → https://www.propertism.in/robots.txt
Invoke-WebRequest -Uri "https://propertism.in/robots.txt" -MaximumRedirection 0 -UseBasicParsing

# Should return 200
Invoke-WebRequest -Uri "https://www.propertism.in/sitemap.xml" -UseBasicParsing
```

### Google Search Console — Post Fix Action
1. Go to GSC → `propertism.in` Domain Property → Sitemaps
2. Remove the failed entry `https://propertism.in/sitemap.xml`
3. Submit: `https://www.propertism.in/sitemap.xml`
4. Monitor status — should change from `Couldn't fetch` → `Success` within 24–72 hrs

### Key Files (No changes made — infrastructure only)
- `.ebextensions/01_django.config` — `CANONICAL_HOST`, `CANONICAL_REDIRECT_HOSTS` ✅
- `content/middleware.py` — `CanonicalDomainRedirectMiddleware` ✅
- `content/sitemaps.py` — `BaseSitemap` uses `www.propertism.in` canonical host ✅
- `content/views.py` — `robots_txt` uses `www.propertism.in` ✅
- `.platform/nginx/nginx.conf` — `proxy_set_header Host $host` ✅

---

## PART 2: FOOTER V4 OPTIMIZATION

### Objective
Reduce footer height, implement 5-column layout, fix text colors and font consistency.

### Changes Made

#### 1. `uilayers/templates/base.html`
- Added `v4-footer.css` to `<head>` after `v4-contact.css`
- Removed inline `<link>` from footer component
- **Root cause of color/font fixes not reflecting**: CSS was loaded inline in component body, losing specificity battle against `propertism-premium.css`

#### 2. `uilayers/templates/components/_footer.html`
- Removed inline `<link rel="stylesheet" href="v4-footer.css">`
- Removed all inline styles from phone number links
- Removed inline styles from `.footer-office-city`
- Moved to `.footer-office-phones` CSS class

#### 3. `static/css/v4-footer.css` — Full Rewrite Summary

| Property | Before | After |
|---|---|---|
| Grid layout | `repeat(4, 1fr)` | `1.2fr 1fr 1.1fr 1.1fr 1.3fr` (5 cols) |
| Clock strip | Full-width row (span 4) | Column 5, 2×3 grid |
| Clock cell padding | `30px 20px` | `8px 6px` |
| Clock time font | `clamp(1.12rem, 1.7vw, 1.42rem)` | `0.8rem` |
| Clock label font | `0.65rem` | `0.5rem` |
| Clock date font | `0.7rem` | `0.48rem` |
| Footer padding | `var(--section-v-padding)` | `30px 0 20px 0` |
| Column gap | `60px` | `24px` |
| Content margin-bottom | `80px` | `24px` |
| Section h3 size | `1.25rem` | `0.85rem` |
| Section h3 margin | `30px` | `12px` |
| All body text | `0.95–1rem` | `0.85–0.9rem` |
| Tagline color | `#94A3B8` | `#FFFFFF` |
| Links color | `#94A3B8` | `#FFFFFF` |
| Address color | `var(--gray-900)` | `#FFFFFF` |
| Phone color | `#FFFFFF` | `var(--brand-gold)` |

### CSS Specificity Conflicts Resolved
The following files had conflicting rules overriding `v4-footer.css`:

| File | Conflicting Rule | Fix |
|---|---|---|
| `propertism-styles.css:4009` | `.world-clock-time { font-size: clamp(1.12rem...) }` | Scoped under `.site-footer` |
| `propertism-premium.css:2169` | `.footer-content { grid-template-columns: 1.8fr 1fr 1.2fr 1fr !important }` | Added `!important` to 5-col rule |
| `propertism-premium.css:2201` | `.footer-brand h3 { white-space: nowrap !important }` | Override with `white-space: normal` |
| `propertism-styles.css:3932` | `.world-clock-cell { min-height: 100px; background: gradient }` | Scoped override under `.site-footer` |

### Known Status
- Footer layout (5-column, 2×3 clocks) rendering correctly ✅
- Text colors reflecting (white body, gold phones/city) — pending hard refresh confirmation
- Clock font sizes reduced — pending confirmation after CSS load order fix

---

## PART 3: ABOUT SECTION OPTIMIZATION

### Changes Made — `static/css/v4-about.css`

- Card padding: `15px 40px` (top/bottom 15px)
- Gap between cards: `40px`
- Mission stack gap: `14px`, margin-bottom: `20px`
- Mission highlight padding: `14px 20px`, margin: `20px`
- Office info gap: `20px`, margin-bottom: `16px`
- Stats box padding: `14px`
- Divider margins: `16px 0`
- `margin-top: auto` on both `.about-cta-block` and `.operations-footer` — aligns CTAs at bottom

---

## AWS Account Reference

| Account | ID | CLI Profile | Purpose |
|---|---|---|---|
| Propertism | `622370466597` | `default` | All Propertism infrastructure |
| Olivine | `673981388490` | `vijim` | Olivine/ERP infrastructure |

**CloudFront Distribution (Propertism)**:
- ID: `E1GGPU208SQFFT`
- Domain: `d1yv5od4i0bho.cloudfront.net`
- Aliases: `propertism.in`, `www.propertism.in`
- Origin: `propertism-prod-2026.us-east-1.elasticbeanstalk.com`
- ACM Cert: `arn:aws:acm:us-east-1:622370466597:certificate/25654f35-6da6-41ae-a2fe-203356b31cb6`

**EB Environment (Propertism)**:
- Name: `propertism-prod-2026`
- ID: `e-jcbmtpnpvx`
- App: `propertism-2026`
- CNAME: `propertism-prod-2026.us-east-1.elasticbeanstalk.com`
- Health: Green ✅
- Last Deploy: `gh-139-c111de1b8f99a32ee86ffeea829d697cdecf981a`

---

## Next Session Priorities

1. **Validate** CloudFront invalidation completed → test `propertism.in/sitemap.xml` returns 301
2. **Resubmit** sitemap in Google Search Console under `www.propertism.in`
3. **Confirm** footer rendering — 5-column layout, compact clocks, white text
4. **Deploy** any pending footer CSS changes via `commit-push.bat` → CI/CD
5. **Monitor** GSC sitemap status change from `Couldn't fetch` → `Success`
