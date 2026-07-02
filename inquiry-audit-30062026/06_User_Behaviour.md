# User Behaviour Analysis

## Metadata
* **Report ID**: RP-BEH-001
* **Report Name**: User Behaviour Analysis
* **SCCB Reference**: SCCB-PROP-GROWTH-AUDIT-001 / 001A
* **Version**: 1.0.0
* **Generated Date**: 2026-06-30
* **Repository / Workspace**: Propertism/propertism
* **Audit Scope**: Scroll depth, dead clicks, navigation, bounce metrics
* **Evidence Version**: NRIAssistEvent dataset
* **Classification**: Multi-Class [A] / [B] / [C] / [D]
* **Status**: FINAL
* **Prepared By**: Platform Integration Lead (Astra)

---

## 1. Executive Summary
This report analyzes user behavior patterns, navigation paths, and page exit behaviors. The database records 105 total events, showing that 93% of actions are basic page visits, and only 2.8% involve interactive CTA clicks.

## 2. Evidence Used
* **NRIAssistEvent Logs**: Breakdown of 105 local events: `PAGE_VISIT` (98), `GOOGLE_LOGIN` (4), `CTA_CLICK` (3) `[B - Repository Evidence]`.
* **Chat Message Logs**: 4 realBOT sessions showing 75% bounce rate at chatbot initiation `[B - Repository Evidence]`.

## 3. Evidence Missing / Data Limitations
* **Microsoft Clarity Export**: Heatmaps, scroll-depth distributions, rage clicks, and user session recordings are missing.
* **GA4 Engagement Metrics**: Bounce rates and exit percentage statistics by page type are missing.

---

## 4. Current Findings

### User Action Patterns
* **Visits vs Interactions**: Out of 105 events, 98 are simple page loads. Interaction rate stands at a low 5.7% (4 logins, 3 clicks) `[B - Repository Evidence]`.
* **realBOT Interaction**: 3 out of 4 sessions ended immediately after the bot's greeting. Only Session 4 shows multi-turn queries, with the user entering "NRI Investment", filtering by budget, and looking at ECR villas `[B - Repository Evidence]`.
* **Dead Clicks / Rage Clicks**: Unable to determine due to lack of Clarity recordings.

---

## 5. Potential Bottlenecks
* **Potential Bottleneck**: Low Interactive Engagement.
  - **Evidence Available**: 93.3% of logged events are page visits `[B]`.
  - **Confidence**: High.
  - **Missing Evidence**: Live visitor session details.

---

## 6. Confidence Level & Business Impact
* **Overall Confidence Level**: High.
* **Business Impact Rating**: Medium.
* **Impact Rationale**: The site generates basic views, but fails to capture user attention, leading to low inquiry rates.

---

## 7. Recommended Actions
* **Recommendation ID**: REC-BEH-001
  - **Description**: Implement and configure Microsoft Clarity tracking in `base.html`.
  - **Priority**: High.
  - **Expected Business Impact**: Capture heatmaps and session recordings to debug layout friction.
  - **Estimated Effort**: Low (2 hours).
  - **Supporting Evidence**: Clarity template placeholders `[B]`.
  - **Success Criteria**: Clarity dashboard registers local developer session recordings.

---

## 8. Appendix: Event Type Frequency
* `PAGE_VISIT`: 98 (93.3%)
* `GOOGLE_LOGIN`: 4 (3.8%)
* `CTA_CLICK`: 3 (2.9%)
