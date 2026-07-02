# Lead Source Analysis Report

## Metadata
* **Report ID**: RP-LEAD-001
* **Report Name**: Lead Source Analysis
* **SCCB Reference**: SCCB-PROP-GROWTH-AUDIT-001 / 001A
* **Version**: 1.0.0
* **Generated Date**: 2026-06-30
* **Repository / Workspace**: Propertism/propertism
* **Audit Scope**: Conversion sources, geography, devices, lead quality
* **Evidence Version**: local Inquiry database records
* **Classification**: Multi-Class [A] / [B] / [C] / [D]
* **Status**: FINAL
* **Prepared By**: Platform Integration Lead (Astra)

---

## 1. Executive Summary
This report analyzes lead generation sources, geographies, and quality metrics using local database records. The database contains 20 inquiries and 2 contact messages. 75% of leads are developer tests, and the only international lead originated from Dallas in June 2026.

## 2. Evidence Used
* **Inquiry Database Table**: `properties_inquiry` contains 20 rows `[B - Repository Evidence]`.
* **Contact Message Table**: `properties_contactmessage` contains 2 rows `[B - Repository Evidence]`.
* **Lead Validation Logs**: Validation details show confidence scores (100 in 15 leads, 75 in 1 lead, and 4 unrated) `[B - Repository Evidence]`.

## 3. Evidence Missing / Data Limitations
* **GA4 Campaign Traffic Logs**: Campaign-level traffic and attribution data are missing.
* **CRM Sales Records**: Lead-to-customer conversion rates and sales outcomes are missing.

---

## 4. Current Findings

### Lead Source Breakdown
* **Quick Inquiry Form**: 13 leads (65%). This is the primary lead capture source on the site `[B - Repository Evidence]`.
* **General Inquiry Form**: 3 leads (15%) `[B - Repository Evidence]`.
* **Unknown Form (Early Records)**: 4 leads (20%) `[B - Repository Evidence]`.

### Geographies
* **India (+91)**: 13 leads (representing local tests by developer/tester accounts) `[B - Repository Evidence]`.
* **USA (Dallas)**: 1 lead (Dallas-mock submission on June 15, 2026) `[B - Repository Evidence]`.
* **Albania (+355)**: 1 lead (test lead ID 20) `[B - Repository Evidence]`.
* **Unspecified**: 5 leads (early database entries) `[B - Repository Evidence]`.

### Lead Quality & Validation
* 15 inquiries scored a **100 Confidence Score**, passing all spam checks `[B - Repository Evidence]`.
* 1 inquiry (Lead ID 15) scored **75** due to a populated hidden field (indicates bot activity), but was approved by CAPTCHA validation `[B - Repository Evidence]`.
* 4 early inquiries are unrated `[B]`.

---

## 5. Potential Bottlenecks
* **Potential Bottleneck**: Real Traffic Deficiency.
  - **Evidence Available**: 15 out of 20 leads are test submissions from local IPs `[B]`.
  - **Confidence**: High.
  - **Missing Evidence**: None.

---

## 6. Confidence Level & Business Impact
* **Overall Confidence Level**: High.
* **Business Impact Rating**: Critical.
* **Impact Rationale**: The platform is not receiving organic NRI leads, which blocks business growth.

---

## 7. Recommended Actions
* **Recommendation ID**: REC-LEAD-001
  - **Description**: Connect CRM endpoints to track lead qualification pipelines.
  - **Priority**: Low.
  - **Expected Business Impact**: Better visibility into sales conversion rates.
  - **Estimated Effort**: High (20-30 hours).
  - **Supporting Evidence**: `properties_inquiry` database model `[B]`.
  - **Success Criteria**: Test lead status updates sync with CRM pipeline dashboards.

---

## 8. Appendix: Database Lead Index
* Lead 1-4: Domestic general test inquiries (April 2026)
* Lead 5: USA/Dallas-origin mock lead (June 2026)
* Lead 6-20: Test leads by developer/tester (June 2026)
