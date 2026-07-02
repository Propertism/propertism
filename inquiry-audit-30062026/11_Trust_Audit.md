# Trust & Credibility Audit Report

## Metadata
* **Report ID**: RP-TRST-001
* **Report Name**: Trust & Credibility Audit
* **SCCB Reference**: SCCB-PROP-GROWTH-AUDIT-001 / 001A
* **Version**: 1.0.0
* **Generated Date**: 2026-06-30
* **Repository / Workspace**: Propertism/propertism
* **Audit Scope**: E-E-A-T signals, reviews database, and legal compliance
* **Evidence Version**: Team and review database models
* **Classification**: Multi-Class [A] / [B] / [C] / [D]
* **Status**: FINAL
* **Prepared By**: Platform Integration Lead (Astra)

---

## 1. Executive Summary
This report audits trust signals, E-E-A-T indicators, and compliance structures. The platform has strong E-E-A-T signals, including detailed profiles for Viji Munuswamy and Tamilselvan, and 4 seeded client reviews. However, these reviews are stored locally in the database and are not linked to external verified reviews.

## 2. Evidence Used
* **Review Database Table**: `content_customerreview` contains 4 reviews `[B - Repository Evidence]`.
* **Team Profile Migrations**: `update_viji_bio.py` and team template files verify Viji's bio as Systems Architect and Technology Consultant `[B - Repository Evidence]`.
* **Footer Configuration**: `v4-team-detail.css` defines styling for Tamilselvan's verified LinkedIn profiles `[B - Repository Evidence]`.

## 3. Evidence Missing / Data Limitations
* **Trustpilot / Google Reviews API**: External verified review integrations are missing.
* **RERA Registration Proof**: Chennai RERA certificate documentation is missing.

---

## 4. Current Findings

### E-E-A-T Signals
* **Founder & Advisor Visibility**: Tamilselvan's advisor details contain two emails and LinkedIn profile links `[B]`. Viji Munuswamy is featured as Technology Consultant `[B - Repository Evidence]`.
* **Reviews and Case Studies**: 4 reviews are active in the database `[B]`. However, these are stored locally, which provides lower trust compared to third-party verified reviews `[D - Professional Recommendation]`.
* **Legal Compliance**: Privacy policy and footer disclosures are structured, but RERA compliance certificates are not actively displayed `[B - Repository Evidence]`.

---

## 5. Potential Bottlenecks
* **Potential Bottleneck**: Unverified Review Friction.
  - **Evidence Available**: 100% of reviews are self-published Django model items `[B]`.
  - **Confidence**: High.
  - **Missing Evidence**: None.

---

## 6. Confidence Level & Business Impact
* **Overall Confidence Level**: High.
* **Business Impact Rating**: High.
* **Impact Rationale**: NRIs require high levels of trust. Displaying unverified reviews or lacking visible regulatory credentials (RERA) can cause users to bounce before converting.

---

## 7. Recommended Actions
* **Recommendation ID**: REC-TRST-001
  - **Description**: Add verified Trustpilot or Google review badge scripts to the homepage footer.
  - **Priority**: High.
  - **Expected Business Impact**: Reduce user trust friction.
  - **Estimated Effort**: Low (2-3 hours).
  - **Supporting Evidence**: `content_customerreview` local items `[B]`.
  - **Success Criteria**: Verified external reviews badge renders on the site.

---

## 8. Appendix: Local Customer Reviews
1. Review from USA client: "Excellent property oversight..." `[B]`
2. Review from UAE client: "Saved me from traveling to Chennai..." `[B]`
