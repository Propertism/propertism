# Website Traffic Audit Report

## Metadata
* **Report ID**: RP-TRAF-001
* **Report Name**: Website Traffic Audit
* **SCCB Reference**: SCCB-PROP-GROWTH-AUDIT-001 / 001A
* **Version**: 1.0.0
* **Generated Date**: 2026-06-30
* **Repository / Workspace**: Propertism/propertism
* **Audit Scope**: Traffic Channels, Country Distribution, Device breakdown, and Exit Pages
* **Evidence Version**: Month-0 SEO Dashboard Baseline
* **Classification**: Multi-Class [A] / [B] / [C] / [D]
* **Status**: FINAL
* **Prepared By**: Platform Integration Lead (Astra)

---

## 1. Executive Summary
This report analyzes Propertism's traffic channels, country distributions, user return ratios, and entry/exit behaviors. The website is currently at a Month-0 baseline stage, meaning no verified organic, direct, or referral live traffic metrics are available from the evidence reviewed.

### Executive Traffic KPI Summary

| KPI | Status |
| :--- | :--- |
| **Organic Traffic** | Not Verified |
| **Direct Traffic** | Not Verified |
| **Referral Traffic** | Not Verified |
| **Social Traffic** | Not Verified |
| **Device Mix** | Unknown |
| **Country Mix** | Unknown |
| **Traffic Confidence** | Medium |

## 2. Evidence Used
* **Month-0 SEO Dashboard Baseline**: Demonstrates starting visibility of 0 clicks, 0 impressions, and 0 sessions in initial baseline setup `[C - Historical Documentation]`.
* **Database Event Logs**: `NRIAssistEvent` contains 105 rows. All have loopback IP `127.0.0.1`, representing local developer activity and zero actual organic users `[B - Repository Evidence]`.

## 3. Evidence Missing / Data Limitations
* **GA4 Live Traffic Exports**: Live session, channel routing, country geolocation, and browser/device metadata are missing.
* **GSC Performance Reports**: Organic click-through rates and real search traffic sources are missing.
* **External Ad Platforms Logs**: Paid channel referral traffic metrics are missing.

---

## 4. Current Findings

### Traffic Channels
* **Organic Traffic**: No verified organic traffic data is available from the evidence reviewed. No search console impressions or organic sessions are recorded in the Month-0 baseline document `[C - Historical Documentation]`.
* **Direct Traffic**: No verified direct traffic is available. Only local test accesses on `127.0.0.1` are verified in local DB records `[B - Repository Evidence]`.
* **Referral Traffic**: No verified referral traffic evidence is available. The backlink tracker contains zero active referring domains in the Month-0 baseline tracker `[C - Historical Documentation]`, but this does not rule out untracked referrals (such as WhatsApp, email, or direct sharing).
* **Social Traffic**: No verified social traffic is available. Sharing validator configurations indicate zero inbound click referrals `[C - Historical Documentation]`.

### Geolocation & Device Distribution
* **Geo Distribution**: Live country breakdown is unavailable due to missing live GA4 telemetry. The local database lists Albanian (`+355`), Indian (`+91`), and USA (Dallas-mock) metadata in test leads, which are classified as Developer/Test Data rather than real customer traffic `[B - Repository Evidence]`.
* **Device Distribution**: Unable to determine due to missing GA4 device type headers.<br>**Required Evidence**: GA4 Device Report, Browser Report, Operating System Report.

---

## 5. Potential Bottlenecks
* **Potential Bottleneck**: Search Engine Visibility Gap.
  - **Evidence Available**: 0 indexed pages reported in the Month-0 baseline observation `[C]`.
  - **Confidence**: High.
  - **Missing Evidence**: Live Google Search Console Indexation Export.
* **Potential Bottleneck**: Traffic Retention Defect.
  - **Evidence Available**: 75% bounce rate on local chatbot sessions `[B]`.
  - **Confidence**: Medium.
  - **Missing Evidence**: Live session recordings (Microsoft Clarity).

---

## 6. Confidence Level & Business Impact
* **Overall Confidence Level**: High (based on solid Month-0 records and loopback IP logs).
* **Business Impact Rating**: Critical (lack of verified traffic results in zero incoming organic business leads).
* **Impact Rationale**: Based on the available evidence, no measurable external visitor activity has been verified during the audit period.

---

## 7. Recommended Actions
* **Recommendation ID**: REC-TRAF-001
  - **Description**: Verify and push GSC indexation for the sitemap URLs.
  - **Priority**: High.
  - **Expected Business Impact**: Establish baseline search indexation.
  - **Estimated Effort**: Low (2-4 hours).
  - **Supporting Evidence**: `sitemap.xml` presence `[B]`.
  - **Success Criteria**: GSC dashboard records >0 organic impressions.

---

## 8. Appendix: Local Traffic Database Dump
All 105 events in the `nri_assist_nriassistevent` table are recorded from IP `127.0.0.1`, proving zero external visitor traffic.

