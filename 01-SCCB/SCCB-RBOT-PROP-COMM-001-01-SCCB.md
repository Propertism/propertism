<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-07-04 11:00:00
Last Updated By: Astra
Last Updated On: 2026-07-04 11:00:00
Searchtag: SCCB-RBOT-PROP-COMM-001
-->

# SCCB-RBOT-PROP-COMM-001
## Integration Hold & Readiness Communication

**Status:** 🔴 ON HOLD (PAUSED)  
**Version:** 1.0  
**Repository:** Propertism  
**Date:** July 04, 2026  

---

## 1. Objective & Mandate

This Software Change Control Board (SCCB) communication establishes a formal **Pause & Hold** on all integration activities between Propertism and the standalone realBOT platform. 

Implementation changes, source code additions, and DB schema alterations are strictly prohibited until the realBOT Platform integration package and stable contract API endpoints are frozen and published under **SCCB-RBOT-M1.x** milestones by the development team (DeepSeek).

All source code has been reverted and restored to the clean, fully functional local chatbot prototype state to prevent staging un-versioned dependencies.

---

## 2. Decoupling Rules & Boundaries

Once the integration hold is lifted by final authorities (Mindra & Viji), the following boundaries will be strictly enforced:
- **Client Role only:** Propertism shall act strictly as a client.
- **No Engine Duplication:** No prompt engine, vector search index, AI provider layer, or local conversation models shall reside in Propertism.
- **API Versions:** All endpoints consumed must target `/api/v1/` versioned endpoints.

---

## 3. Handover Requirements Checklist

Before resuming implementation, DeepSeek must publish the **Integration Handover Package** containing:
1. Public REST API Specification (/api/v1/)
2. JWT/Exchange Authentication Specification
3. Widget SDK Javascript Loader URL
4. Dynamic Widget Initialization Guide
5. JS Custom Event Contracts
6. Theme & Widget Configuration Specification
7. Version Compatibility Matrix
8. Error Code Catalogue
9. Health Check JSON Specification
10. Deployment and Rollback Guide

---

***
*Maintained by Astra | 2026-07-04 11:00 IST*
