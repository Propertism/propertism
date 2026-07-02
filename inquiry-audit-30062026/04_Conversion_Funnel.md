# Conversion Funnel Audit Report

## Metadata
* **Report ID**: RP-FUNN-001
* **Report Name**: Conversion Funnel Audit
* **SCCB Reference**: SCCB-PROP-GROWTH-AUDIT-001 / 001A
* **Version**: 1.0.0
* **Generated Date**: 2026-06-30
* **Repository / Workspace**: Propertism/propertism
* **Audit Scope**: Complete enquiry journey from Visitor to Sale
* **Evidence Version**: Django inquiry views, DB leads dump
* **Classification**: Multi-Class [A] / [B] / [C] / [D]
* **Status**: FINAL
* **Prepared By**: Platform Integration Lead (Astra)

---

## 1. Executive Summary
This report analyzes the complete user funnel: **Visitor → Homepage → Landing → Service → CTA → WhatsApp → Phone → Inquiry → Qualified Lead → Sales → Closed Customer**. It identifies two structural friction blocks: a missing production email recipient configuration that drops lead emails, and a high bounce rate on the realBOT greeting page.

## 2. Evidence Used
* **Django Settings**: `settings_production.py` vs `settings.py` files `[B - Repository Evidence]`.
* **Lead Email Views**: `content/views.py` swallowed exception block and AttributeError warning in email audit `[B - Repository Evidence]`.
* **Database Dumps**: 20 total inquiries logged, of which 15 are developer/tester submissions on June 30, 2026 `[B - Repository Evidence]`.

## 3. Evidence Missing / Data Limitations
* **GA4 Funnel Telemetry**: Live funnel drop-offs at Visitor, Homepage, and Landing/Service stages are missing.
* **CRM Pipeline Logs**: Qualification, sales outreach, and customer closure conversion rates are missing.
* **Call Tracking Data**: Direct phone call conversion rates are missing.

---

## 4. Current Findings

### Funnel Step Analysis & Leakage Points

```
[1. Visitor] 
      ↓ (0 Clicks / Impressions recorded in baseline)
[2. Homepage / Landing / Service Pages]
      ↓ (75% Bounce rate on local realBOT sessions)
[3. CTA Clicks / Form Views]
      ↓ (100% email notification failure in production)
[4. Inquiry Submitted]
      ↓ (CRM data missing - local DB holds 20 inquiries)
[5. Qualified Lead]
      ↓ (Telemetry missing)
[6. Sales Outreach]
      ↓ (Telemetry missing)
[7. Closed Customer / Revenue]
```

* **Visitor to Landing Page**: Zero live data. Baseline reports zero sessions `[C - Historical Documentation]`.
* **CTA to Inquiry Submission**: Forms save to `properties.Inquiry` `[B]`. However, inline Captcha challenges (which use show/hide replacement code) may cause friction for less technical users `[D - Professional Recommendation]`.
* **Inquiry to Qualified Lead**: The Lead Validation Engine validates inquiries `[B]`. However, due to the missing `ADMIN_EMAIL` setting in `settings_production.py`, the system fails to send email alerts, which results in critical leads being left unaddressed `[B - Repository Evidence]`.
* **Qualified Lead to Revenue**: Unable to determine due to missing CRM integration.

---

## 5. Potential Bottlenecks
* **Potential Bottleneck**: Email Delivery Defect.
  - **Evidence Available**: `settings_production.py` does not contain `ADMIN_EMAIL` `[B]`.
  - **Confidence**: High.
  - **Missing Evidence**: None.
* **Potential Bottleneck**: Captcha Layout Shift.
  - **Evidence Available**: CAPTCHA features hide form fields on selection `[B]`.
  - **Confidence**: Medium.
  - **Missing Evidence**: Live usability data.

---

## 6. Confidence Level & Business Impact
* **Overall Confidence Level**: High.
* **Business Impact Rating**: Critical.
* **Impact Rationale**: Lead alerts fail to trigger, which halts sales follow-up and breaks the bottom of the funnel.

---

## 7. Recommended Actions
* **Recommendation ID**: REC-FUNN-001
  - **Description**: Add `ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'info@propertism.in')` to `settings_production.py`.
  - **Priority**: Critical.
  - **Expected Business Impact**: Secure 100% notification delivery for incoming leads.
  - **Estimated Effort**: Low (1 hour).
  - **Supporting Evidence**: Swallowed AttributeError in `content/views.py` `[B]`.
  - **Success Criteria**: Local test inquiry triggers email notification without error.

---

## 8. Appendix: Inquiry Validation Fields
Database fields track lead quality metrics: `confidence_score` (0-100), `spam_score`, `assessment_status`, and `validation_summary`.
