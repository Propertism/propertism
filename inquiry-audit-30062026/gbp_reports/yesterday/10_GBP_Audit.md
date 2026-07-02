# Google Business Profile Audit Report

## Metadata
* **Report ID**: RP-GBP-001
* **Report Name**: Google Business Profile Audit
* **SCCB Reference**: SCCB-PROP-GROWTH-AUDIT-001 / 001A
* **Version**: 1.0.0
* **Generated Date**: 2026-06-30
* **Repository / Workspace**: Propertism/propertism
* **Audit Scope**: GBP completeness, reviews, photos, local map rankings
* **Evidence Version**: Month-0 Local SEO configurations
* **Classification**: Multi-Class [A] / [B] / [C] / [D]
* **Status**: FINAL
* **Prepared By**: Platform Integration Lead (Astra)

---

## 1. Executive Summary
This report audits Propertism's local Google Business Profile listing. Google Business analytics data is currently unlinked and unavailable.

## 2. Evidence Used
* **Company Information Model**: The database contains standard address information for local registry requirements `[B - Repository Evidence]`.

## 3. Evidence Missing / Data Limitations
* **Google Business Profile Insights Dashboard**: GBP search views, user click actions, and map directions requests are missing.
* **Live Google Map Ranking Telemetry**: Map pack search position history is missing.

---

## 4. Current Findings
* **GBP Linkage**: The Google Business Profile is not integrated with the website's schema configs or analytics triggers `[B - Repository Evidence]`.
* **Reviews and Photos**: Review database logs list 4 customer reviews `[B]`, but these are stored locally and are not synced with a live Google Business Profile.

---

## 5. Potential Bottlenecks
* **Potential Bottleneck**: Map Visibility Gap.
  - **Evidence Available**: GBP schema hooks are absent from the landing template `[B]`.
  - **Confidence**: Medium.
  - **Missing Evidence**: GBP dashboard profile access.

---

## 6. Confidence Level & Business Impact
* **Overall Confidence Level**: High.
* **Business Impact Rating**: Medium.
* **Impact Rationale**: NRIs search for verified physical locations to confirm credibility. A missing or unlinked GBP listing increases trust friction.

---

## 7. Recommended Actions
* **Recommendation ID**: REC-GBP-001
  - **Description**: Add LocalBusiness schema referencing GBP address credentials in `base.html`.
  - **Priority**: Medium.
  - **Expected Business Impact**: Boost local maps indexation and trust signals.
  - **Estimated Effort**: Low (3 hours).
  - **Supporting Evidence**: Organization schema in `seo_tags.py` `[B]`.
  - **Success Criteria**: Rich results testing confirms correct LocalBusiness schema rendering.

---

## 8. Appendix: Local Company Details
* Registered Address: Chennai, India `[B]`
* Phone Support: +91 87786 51851 `[B]`
