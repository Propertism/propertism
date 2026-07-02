# Technical Performance Audit Report

## Metadata
* **Report ID**: RP-TECH-001
* **Report Name**: Technical Performance Audit
* **SCCB Reference**: SCCB-PROP-GROWTH-AUDIT-001 / 001A
* **Version**: 1.0.0
* **Generated Date**: 2026-06-30
* **Repository / Workspace**: Propertism/propertism
* **Audit Scope**: Performance, mobile optimizations, caching configurations, asset compression
* **Evidence Version**: Static assets config and collectstatic hooks
* **Classification**: Multi-Class [A] / [B] / [C] / [D]
* **Status**: FINAL
* **Prepared By**: Platform Integration Lead (Astra)

---

## 1. Executive Summary
This report audits page load speed, asset sizes, and mobile optimizations. The technical foundation is strong, featuring optimized WebP images and viewport normalizations. However, the site lacks CDN-level assets caching, which can increase load times for international users.

## 2. Evidence Used
* **WebP Image Assets**: Verifies WebP optimization of large hero files `[C - Historical Documentation]`.
* **EB Post-deployment Hooks**: `.platform/hooks/postdeploy/00_collectstatic_current.sh` manages static assets collections `[B - Repository Evidence]`.
* **CSS Normalization Styles**: `viewport-section-normalization.css` manages 100vh viewport sizes `[B - Repository Evidence]`.

## 3. Evidence Missing / Data Limitations
* **Lighthouse / Core Web Vitals Live Reports**: Live page speeds, LCP scores, and CLS metrics are missing.

---

## 4. Current Findings
* **Image Compression**: Transitioning major hero images to WebP achieved a 90% size reduction, improving load times `[C - Historical Documentation]`.
* **Mobile Viewport Optimization**: CSS adjustments prevent layout shifts and normalise viewports on mobile devices `[B - Repository Evidence]`.
* **Assets Delivery**: The server runs `collectstatic` on deployment. However, it lacks CDN caching configurations for static files, which can delay page loads for international NRI users `[D - Professional Recommendation]`.

---

## 5. Potential Bottlenecks
* **Potential Bottleneck**: International Latency.
  - **Evidence Available**: CloudFront caching is HTTP-only with no static cache TTL values defined in Django config `[B]`.
  - **Confidence**: Medium.
  - **Missing Evidence**: Live speed tests from international nodes.

---

## 6. Confidence Level & Business Impact
* **Overall Confidence Level**: High.
* **Business Impact Rating**: Medium.
* **Impact Rationale**: Slow loading speeds on international connections can cause users to bounce before reading the conversion landing pages.

---

## 7. Recommended Actions
* **Recommendation ID**: REC-TECH-001
  - **Description**: Define static files cache control settings in `settings_production.py`.
  - **Priority**: Medium.
  - **Expected Business Impact**: Improve international page speeds by enabling client-side caching.
  - **Estimated Effort**: Low (3 hours).
  - **Supporting Evidence**: `settings_production.py` `[B]`.
  - **Success Criteria**: GTmetrix confirms active cache-control headers on static files.

--- 8. Appendix: Static Deployment Configuration
* static folder: `static/css/`, `static/js/` `[B]`
* Hook: `00_collectstatic_current.sh` runs during EB deployment `[B]`.
