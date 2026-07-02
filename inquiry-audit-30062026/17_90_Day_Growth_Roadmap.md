# 90-Day Growth Roadmap

## Metadata
* **Report ID**: RP-ROAD-001
* **Report Name**: 90-Day Growth Roadmap
* **SCCB Reference**: SCCB-PROP-GROWTH-AUDIT-001 / 001A
* **Version**: 1.0.0
* **Generated Date**: 2026-06-30
* **Repository / Workspace**: Propertism/propertism
* **Audit Scope**: Prioritization of growth wins, 30-60-90 Day tasks
* **Evidence Version**: Audit bottleneck priorities
* **Classification**: Multi-Class [A] / [B] / [C] / [D]
* **Status**: FINAL
* **Prepared By**: Platform Integration Lead (Astra)

---

## 1. Executive Summary
This report defines a structured 90-day roadmap. Recommendations are categorized by impact and effort, focusing on restoring lead delivery and boosting organic search presence.

## 2. Evidence Used
* **Growth Bottleneck Report**: Connects roadmap priorities to verified bottlenecks `[C - Historical Documentation]`.

## 3. Evidence Missing / Data Limitations
* **Live traffic trends**: The timeline lacks live traffic baseline metrics.

---

## 4. Current Findings

### Priority Matrix (Impact vs Effort)

```
       High | [High Impact, Low Effort]        | [High Impact, High Effort]
            | - Fix production email config    | - Relocate media assets to S3
            | - Verify GSC sitemaps            | - Build Tamil association links
            |                                  |
     I      |                                  |
     M      |                                  |
     P      |----------------------------------|----------------------------------
     A      | [Low Impact, Low Effort]         | [Low Impact, High Effort]
     C      | - Add Clarity script tag         | - Sync database with CRM pipeline
     T      | - Add cache-control settings     |
            |                                  |
        Low +----------------------------------+----------------------------------
                           Low                               High
                                       EFFORT
```

* **Quick Wins (High Impact, Low Effort)**: Fix production email config; verify GSC sitemap indexation.
* **High Impact (High Impact, High Effort)**: Move media assets to S3; build links with international Tamil associations.
* **Low Impact (Low Impact, Low Effort)**: Add Clarity tracking script; define cache-control settings in production.
* **Future Investment (Low Impact, High Effort)**: Sync local database leads with external CRM pipeline tools.

---

## 5. Potential Bottlenecks
* **Potential Bottleneck**: Resource Constraints.
  - **Evidence Available**: The roadmap depends on active developer time for deployment `[D]`.
  - **Confidence**: Medium.
  - **Missing Evidence**: Dev team availability details.

---

## 6. Confidence Level & Business Impact
* **Overall Confidence Level**: High.
* **Business Impact Rating**: Critical.
* **Impact Rationale**: The roadmap provides a clear prioritization framework for resolving blockers and launching growth campaigns.

---

## 7. Recommended Actions
* **Recommendation ID**: REC-ROAD-001
  - **Description**: Approve and schedule Phase 1 tasks (Days 1-30) to resolve critical lead delivery blockers.
  - **Priority**: Critical.
  - **Expected Business Impact**: Restore lead notification delivery.
  - **Estimated Effort**: Low (2-3 days).
  - **Supporting Evidence**: Growth bottlenecks register `[C]`.
  - **Success Criteria**: Email notifications are successfully sent to `info@propertism.in`.

---

## 8. Appendix: Timeline Summary
* **Days 1-30**: Deploy email settings patch; submit GSC index request.
* **Days 31-60**: Integrate Microsoft Clarity; configure media assets on AWS S3.
* **Days 61-90**: Launch outreach to Tamil associations; connect CRM endpoints.
