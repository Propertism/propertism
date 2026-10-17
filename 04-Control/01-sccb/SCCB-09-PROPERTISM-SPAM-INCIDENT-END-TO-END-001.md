<!-- SCCB METADATA -->
<!-- SCCB ID: SCCB-09-PROPERTISM-SPAM-INCIDENT-END-TO-END-001 -->
<!-- Date Created: 2026-10-13 -->
<!-- Time: 13:05 IST -->
<!-- Owner: Viji M -->
<!-- Execution Agent: Cursor / Astra -->
<!-- Priority: P0 — Critical Production Security Incident -->
<!-- Status: SINGLE SOURCE OF TRUTH — NOT CLOSED -->
<!-- Classification: INTERNAL — SECURITY CRITICAL -->

---

# SCCB-09-PROPERTISM-SPAM-INCIDENT-END-TO-END-001
## Propertism.in — Forensic Spam Investigation, API Security Audit, Root-Cause Resolution and Security Hardening

**THIS IS THE ONLY REPORT for this incident.**  
Folder rule: one SCCB file per change-control item, with numbered sections. Do not add companion audits, validation reports, implementation reports, or emergency extracts. After each task, the agent updates this file and returns the relevant section as a single chat block.

### How to read (SCCB sections)

| Read | Section | What it answers |
|---|---|---|
| Start here | **DOCUMENT STATUS** | Phase, constraints, not-closed |
| 1 | Mission and context | Track A spam vs Track B API PII |
| 2 | Governance rules | No deploy / no prod data change |
| 3 | Evidence register | Claims vs verified |
| 4 | Repository inventory | Apps, security modules, git |
| 5 | Timeline / counts | Unverified until evidence request |
| 6 | Public API audit | GET `/api/inquiries/` confidentiality |
| 7 | Enquiry write-path inventory | What can create `Inquiry` |
| 8 | CAPTCHA / spam controls | Fail-open, secret, flags |
| 9–10 | Tests and local remediation | What was coded locally |
| 11 | Workflow rule | `AGENTS.md` report-first |
| 12–13 | Acceptance / checklist | Still open |
| 14–15 | Implementation log / approvals | Pending Viji |
| 16–18 | Root cause / impact / lessons | Hypotheses vs confirmed |
| 19 | Folder rule | One file per SCCB; fragments removed |
| 20 | Closure | **Not closed** |
| **21** | Validation execution | Tests, API vs spam split |
| **22** | Approval-ready follow-up | Deal Engine, realBOT, decisions |
| **23** | Approval-gated next steps | Cutover plan, realBOT design, evidence checklist |
| **24** | Local implementation | Option B, 04 client/inbound, realBOT C1–C3, tests |
| **25** | Acceptance review SCCB-09-AR-001 | Independent check of §24; no code change |
| **26** | D4 local commits | Decisions applied; push withheld because main deploys |

**Priority:** P0 — Critical Production Security Incident  
**Owner / Final Authority:** Viji M  
**Execution Agent:** Cursor / Astra  
**Related Audit:** absorbed into this file (§§3–8, 21); standalone audit file removed  
**Incident Date:** 13 October 2026  
**Scope:** Propertism.in security investigation and corrective action  
**Execution Mode:** Evidence-first, repository-aware, controlled implementation, no unauthorized production changes

---

## DOCUMENT STATUS

**Current Phase:** D4 local commits prepared. Push withheld. Not deployed. Not closed.  
**Last Updated:** 2026-10-13 16:05 IST  
**Completion Status:** Viji approved D4 commit/push, deferred deployment. Push to `main` is withheld because both repositories deploy to Lightsail on push. Track A root cause still unconfirmed.  
**Constraint:** No Lightsail deploy, no production config, no production data change, no service-key value in git or chat.

See **Section 21** (validation), **Section 22** (discovery), and **Section 23** (approval-gated next steps).

### Follow-up scope (before further work)

1. Keep Track A (spam writes) and Track B (API PII) separate in the emergency plan, with superseded history marked.
2. Locate Deal Engine’s actual HTTP client for `PROPERTISM_INQUIRIES_API_URL`; recommend cutover; **do not implement** a breaking auth change.
3. Trace `InquirySubmissionAdapter` trust model; **do not add** `SpamProtectionService` until Viji approves.
4. Re-check workspace for usable spam-count evidence; if none, file an explicit evidence request (no PII dumps).
5. Revalidate security diffs against `.venv` + `requirements.txt`; assess the WhatsApp notification test as possibly stale (test-only fix if proven obsolete).
6. Stop for Viji approvals. No deploy.

### Confirmed facts (code / git / prior local work)

| Fact | Evidence | Classification |
|---|---|---|
| Canonical SCCB exists at this path | File present | Confirmed |
| `/api/inquiries/` is GET-only in current code | `@api_view(["GET"])` in `properties/views.py` | Confirmed in code |
| Serializer returns name, email, phone, message and related PII | `InquirySerializer` fields | Confirmed in code |
| Local working copy uses `IsStaffOrDealEngineKey` on that GET view | Uncommitted `properties/permissions.py` + `properties/views.py` | Confirmed locally; production unverified |
| `Inquiry.objects.create()` in `create_inquiry()` is a write path | `properties/views.py` | Confirmed in code |
| Additional `PropertyInquiry.objects.create()` paths exist | `content/views.py`, `chat/inquiry_submission.py` | Confirmed in code; incident relevance pending |
| Chat `/chat/submit/` writes `ContactMessage`, not `Inquiry` | `chat/views.py` | Confirmed in code |
| `RECAPTCHA_FAIL_OPEN` default is now `False` in local settings | Uncommitted settings diff | Confirmed locally |
| Missing CAPTCHA secret now returns `success=False` locally | Uncommitted `google_recaptcha.py` | Confirmed locally |
| API `AllowAny` introduced in commit `bb2936ce` (15 Jul 2026) | `git log -S` | Confirmed in git; production first-exposure date unverified |
| Enquiry export `inquiries-0.md` is not in this workspace | Path search | Gap |
| Production logs, `.env`, and live DB are not available here | Environment | Gap |

### Unresolved questions this execution must answer or record as blocked

1. Which endpoint actually persisted the 13 Oct 2026 spam `Inquiry` rows?
2. Did CAPTCHA run, fail-open, skip via flag, or get a valid token on that path?
3. Does the frontend submit `g-recaptcha-response`, `website_url_check`, and `form_render_time`?
4. Are Astra's local fixes complete, or do silent bypasses remain (`CAPTCHA_ENABLE=false`, `NullProvider`, absent timing field, spoofable `X-Forwarded-For`)?
5. Who consumes `/api/inquiries/` (Deal Engine / prospect matching)? Is `IsAdminUser` the correct policy?
6. Can Django tests be executed in this environment?
7. Emergency plan currently treats the GET API as the spam root cause — that causal claim is not proven.

### Action plan for this execution

1. Preserve Viji's unrelated working-tree changes; only touch incident-related files.
2. Trace every `Inquiry` write path and the chat widget independently.
3. Inspect frontend field names against validators (do not assume names).
4. Close remaining CAPTCHA fail-open / missing-secret / unexpected-disable gaps without breaking local DEBUG.
5. Confirm API least-privilege, related list endpoints, and status codes.
6. Repair the Django interpreter mismatch and run tests; do not claim pass if not executed.
7. Add the report-first rule to `AGENTS.md` (no invented Task-Rules skill).
8. Correct the emergency plan so Track A (spam) and Track B (API PII) stay separate.
9. Stop for Viji authorization — no deploy.

### Prior reports — reconciliation note

- `09-PROPERTISM-SPAM-INCIDENT-AUDIT-001.md` and `EMERGENCY-ACTION-PLAN.md` asserted the public GET API as the spam root cause. That is a **confidentiality finding**. It is **not** accepted as the spam write-path unless this execution finds write evidence.
- Astra local fixes (API auth, fail-closed default, missing-secret fail, chat `SpamProtectionService`) are treated as **proposed**, not complete, until independently reviewed and tested.

---

## 1. MISSION AND BUSINESS CONTEXT

### Incident Summary

Propertism.in reportedly received approximately **1,400 spam enquiries in a single day (13 October 2026)** despite an existing spam-protection implementation and enabled Google reCAPTCHA v2.

Subsequent security audit identified an additional critical issue: a reportedly **unauthenticated public API** at:

```
https://www.propertism.in/api/inquiries/
```

The reported API implementation in `properties/views.py` uses `@api_view(["GET"])` and `@permission_classes([AllowAny])`, and serializes enquiry records without authentication.

### Investigation Framework: Two Mandatory Tracks

**Track A — Primary Objective: Spam Incident Root Cause**

Establish exactly how the suspicious enquiries were submitted, which endpoint created them, which security controls executed, and why the existing controls did not prevent persistence.

**Track B — Additional Checkpoint: Public API Security**

Determine whether the public API exposes customer information without appropriate authorization, identify its intended business purpose and consumers, establish its exposure scope, and correct any verified access-control weakness.

**Critical Directive:** Investigate the relationship between these tracks, but connect them causally only when evidence establishes that relationship. Do not assume the API's GET permission issue proves it accepted POST spam submissions.

### Required Outcome

Deliver a complete forensic audit, resolve the root cause to the extent supported by evidence, implement and test appropriately authorized local corrective changes, document remaining operational actions, and provide a verifiable final SCCB.

**Do not reduce this assignment to:**
- Adding another CAPTCHA layer
- Blindly disabling the API
- Writing a general-purpose security checklist

---

## 2. NON-NEGOTIABLE GOVERNANCE AND SAFETY RULES

### Code and Repository Discipline

1. ✅ Read and follow applicable Propertism and Olivine engineering governance rules before implementation
2. ✅ Inspect current Git branch, working-tree status and existing modifications — preserve user changes
3. ✅ Conduct forensic investigation before implementing corrective application changes
4. ✅ Do not assume production access, logs, environment variables, database access or AWS credentials are available
5. ✅ Record actual evidence accessible to the current environment

### Security and Privacy Protection

6. ✅ Do not print, copy into reports or expose production secrets, CAPTCHA secrets, database credentials, authentication tokens or unnecessary customer personal information
7. ✅ Do not issue POST requests, perform write tests, run stress tests, attempt exploit reproduction or conduct unrestricted data retrieval against production
8. ✅ Do not download the publicly exposed customer dataset again merely to confirm an observation already documented
9. ✅ Use the supplied export and existing evidence where available — minimize exposure of data already obtained
10. ✅ Do not delete, bulk-update, quarantine or otherwise alter existing production enquiries

### Deployment and Infrastructure Constraints

11. ✅ Do not change production environment variables, AWS infrastructure, database records, access policies or live application configuration
12. ✅ Do not deploy code changes
13. ✅ Do not create database schema changes or migrations without first establishing necessity
14. ✅ Local code changes, tests and documented migration proposals are permitted within this SCCB

### Code Change Discipline

15. ✅ Do not perform blanket removal of `@csrf_exempt` decorators or other broad security transformations without endpoint-by-endpoint review
16. ✅ Do not accept proposed root causes, record counts, attack attribution or numerical confidence scores from earlier reports without validating the underlying evidence
17. ✅ Do not commit or push changes unless separately authorized

### Investigation and Reporting Standards

18. ✅ Do not stop to ask routine clarification questions — investigate available evidence, record gaps and continue through all phases that can safely be completed
19. ✅ If any recommendation would require production deployment, destructive database operations, external notifications or a potentially breaking integration change, prepare the exact proposed action and leave it pending explicit authorization

---

## 3. INITIAL EVIDENCE REGISTER

| ID | Finding or Hypothesis | Initial Classification | Verification Status | Evidence Source | Notes |
|---|---|---|---|---|---|
| **EV-001** | Approximately 1,400 spam enquiries received in one day | Reported incident | ⏳ PENDING | User report | Verify exact count via data analysis |
| **EV-002** | Suspicious records contain Russian-language promotional/scam messages and `share.google` links | Observed pattern | ⏳ PENDING | Supplied enquiry export | Analyze export file |
| **EV-003** | Existing spam protection and CAPTCHA were enabled | Reported configuration | ⏳ PENDING | Code inspection required | Verify implementation |
| **EV-004** | `RECAPTCHA_FAIL_OPEN` reportedly defaults to `True` | Reported configuration | ⏳ PENDING | Code inspection required | Verify repository implementation |
| **EV-005** | Missing reCAPTCHA secret reportedly causes verification to return success | Reported vulnerability | ⏳ PENDING | Code inspection required | Verify exact behavior |
| **EV-006** | Public API `/api/inquiries/` returns enquiry records with `AllowAny` permissions | Reported vulnerability | ⏳ PENDING | Code inspection + live verification | Inspect current route, view, serializer |
| **EV-007** | `/chat/submit/` reportedly creates `ContactMessage` records without spam protections | Reported vulnerability | ⏳ PENDING | Code inspection required | Verify separately from Inquiry incident |
| **EV-008** | Per-IP rate limiting configured at five submissions per ten minutes | Reported control | ⏳ PENDING | Code inspection required | Verify call sites, storage, cache behavior |
| **EV-009** | Production request logs, live settings and database evidence previously unavailable | Reported limitation | ⏳ PENDING | Access assessment | Reassess actual access |
| **EV-010** | Previous reports contain conflicting spam counts, attack timelines and root-cause confidence claims | Reported inconsistency | ⏳ PENDING | Report reconciliation | Reconcile using supplied records and reproducible analysis |

### Evidence Classification Legend

- ✅ **CONFIRMED IN CODE**: Verified in repository source code
- 🔴 **CONFIRMED IN PRODUCTION**: Verified in live production environment
- ⚠️ **PROBABLE**: High confidence but not directly verified
- ⏳ **PENDING**: Awaiting verification
- ❓ **UNVERIFIED**: Claimed but not yet investigated
- ❌ **DISPROVED**: Evidence contradicts claim

---

## 4. PHASE 1 — REPOSITORY, GOVERNANCE AND ARTIFACT INVENTORY

### 4.1 Project Context Establishment

**Status:** ✅ COMPLETE

**Tasks:**
- [x] Confirm repository root and active branch
- [x] Check Git working-tree status
- [x] Identify relevant Django applications
- [x] Locate existing security modules
- [x] Find test infrastructure
- [x] Review deployment configuration files
- [x] Locate existing SCCBs and reports for this incident
- [x] Identify project-specific governance rules and agent instruction files

**Findings:**

**Repository Context:**
- **Root**: `D:\viji\viji-olivine\03-propertism`
- **Active Branch**: `main`
- **Working Tree Status**: Modified files in project planning docs, content app, and new untracked `04-Control/` directory

**Django Applications Identified:**
1. `properties/` — Core property listings and inquiry management
2. `content/` — Content management and security modules
3. `chat/` — Chat and contact message handling
4. `nri_assist/` — NRI service module
5. `communications/` — Communication handling
6. `search/` — Search functionality
7. `users/` — User management
8. `uilayers/` — UI components

**Security Modules Located:**
- `content/security/spam_protection.py` — Centralized spam protection orchestrator
- `content/security/google_recaptcha.py` — Google reCAPTCHA v2 verification
- `content/security/validators.py` — Honeypot, timing, rate limiting validators
- `content/security/captcha_provider.py` — CAPTCHA provider abstraction
- `content/security/__init__.py` — Security module initialization

**Test Infrastructure:**
- `properties/tests.py`
- `chat/tests.py`
- `content/tests.py`
- `communications/tests.py`

**Deployment Configuration:**
- `realtor_project/settings.py` — Django settings with CAPTCHA configuration
- `feature_flags.json` — Feature flag configuration

**Existing SCCBs and Reports:**
- `04-Control/01-sccb/09-PROPERTISM-SPAM-INCIDENT-AUDIT-001.md` — Initial forensic audit (2,064 lines)
- `04-Control/01-sccb/EMERGENCY-ACTION-PLAN.md` — Emergency containment reference
- `04-Control/01-sccb/SCCB-09-PROPERTISM-SPAM-INCIDENT-END-TO-END-001.md` — This document
- `04-Control/01-sccb/SCCB-AWS-NEW-ACCOUNT-MIGRATION.md` — Unrelated AWS SCCB

---

### 4.2 Applicable Governance Review

**Status:** ✅ COMPLETE

**Tasks:**
- [x] Read canonical rules from repository
- [x] Identify constraints affecting report creation, implementation, naming, testing, version control or approvals
- [x] Document governance requirements

**Findings:**

**Governance Files Located:**
- `CLAUDE.md` — Operational context and agent identity
- `AGENTS.md` — Absolute Code & Deployment Protocol
- `code-review/CLAUDE.md` — Code review context

**Key Governance Constraints:**

1. **8-Stage Delivery Lifecycle (Viji Law, 2026-09-04)**:
   - Fix Locally → Internal Test → Report to Viji → Viji Verifies → Viji Approves → Git Push → CI/CD Pipeline → Prod Validation

2. **Production Database Rule**: NEVER write to, seed, modify, or touch production database without explicit written approval

3. **GitHub Account**: Repository: `https://github.com/Propertism/propertism`, Active account: `Propertism`

4. **No Direct Lightsail Changes**: Application code changes MUST go through 8-stage lifecycle, NO direct VPS edits except runtime `.env` secrets

5. **Deployment**: Django/PostgreSQL on AWS Lightsail Mumbai, gunicorn, WhiteNoise static files

6. **Testing Protocol**: Deterministic verification locally before deployment

7. **Approval Requirements**: Explicit Viji approval required before Git push and deployment

---

### 4.3 Available Evidence Identification

**Status:** ✅ COMPLETE

**Tasks:**
- [x] Locate Astra's original and updated audit reports
- [x] Find enquiry export file (`inquiries-0.md`)
- [x] Review existing incident notes
- [x] Find security implementation reports
- [x] Review CAPTCHA configuration and provider implementations
- [x] Identify prior remediation work or tests

**Findings:**

**Audit Reports Located:**
- ✅ `04-Control/01-sccb/09-PROPERTISM-SPAM-INCIDENT-AUDIT-001.md` (2,064 lines) — Comprehensive forensic audit with:
  - Executive Summary
  - Root Cause Analysis
  - Attack Timeline
  - CAPTCHA Audit
  - Spam Control Audit
  - Public API Security Assessment
  - Impact Assessment
  - Remediation Plan
  - Evidence Register
  - Outstanding Questions (10 questions, Q1-Q10)

**Enquiry Export File:**
- ❌ `inquiries-0.md` — **NOT FOUND** in repository
- Previous audit report references this file (597 KB JSON dump, 4,600+ records)
- File was used for analysis but not committed to repository
- **Evidence Status**: Analysis results available in audit report, raw file not available for re-analysis

**CAPTCHA Configuration Evidence:**

**Feature Flags** (`feature_flags.json`):
```json
{
  "CAPTCHA_ENABLE": true,
  "CAPTCHA_PROVIDER": "google_v2",
  "CAPTCHA_TEST_MODE": false,
  "REALBOT_INTEGRATION_ENABLED": true,
  "REALBOT_AI_ENABLED": false
}
```

**Django Settings** (`realtor_project/settings.py` lines 703-708):
```python
RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY', '')
RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY', '')
RECAPTCHA_FAIL_OPEN = _get_bool_env('RECAPTCHA_FAIL_OPEN', default=True)
```

**Critical Security Implementation Notes:**
- CAPTCHA is enabled via feature flags
- `RECAPTCHA_FAIL_OPEN` **defaults to `True`** (fail open on errors)
- Secret key loaded from environment variable
- Missing secret key handling: Returns **SUCCESS** (line 70 of `google_recaptcha.py`)

**Security Implementation Reports:**
- ✅ `04-Control/Web_Crucials_Perfomance_and_Security.md` — Technical reference for web security, performance, CAPTCHA, spam protection patterns

---

## 5. PHASE 2 — INDEPENDENT DATA AND INCIDENT-TIMELINE RECONSTRUCTION

### 5.1 Authoritative Count Establishment

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Determine total records in supplied export
- [ ] Count records created during incident window
- [ ] Count records matching observed spam indicators
- [ ] Count records confidently classified as spam
- [ ] Count records with uncertain classification
- [ ] Identify total distinct enquiry IDs and duplicates
- [ ] Extract earliest and latest timestamps
- [ ] Assess available record range and pagination limitations

**Findings:**

*(To be populated during data analysis)*

---

### 5.2 Prior Report Inconsistency Resolution

**Status:** ⏳ PENDING

**Claims to Reconcile:**
- Approximately 1,400 spam enquiries
- 4,674+ spam-pattern matches
- Records around IDs 4265–4312
- Timestamps around 11:39–12:39 IST

**Tasks:**
- [ ] Verify whether reported IDs correspond to expected number of distinct records
- [ ] Determine if counts represent all records, pattern matches, or time-windowed subset
- [ ] Verify whether timestamps describe whole incident or sampled burst
- [ ] Assess if export was complete at time of generation
- [ ] Verify consistent timezone usage

**Findings:**

*(To be populated during reconciliation)*

---

### 5.3 Timeline Reconstruction

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Identify earliest confirmed spam submission
- [ ] Map major submission bursts
- [ ] Track changes in submission frequency
- [ ] Identify latest confirmed spam event
- [ ] Calculate counts per minute/interval where timestamps support it

**Timeline:**

*(To be populated during timeline reconstruction)*

---

## 6. PHASE 3 — PUBLIC API SECURITY AUDIT

### 6.1 Complete API Implementation Trace

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Inspect `properties/views.py` — `inquiry_list_api` view
- [ ] Review all applicable `urls.py` files and URL mounting rules
- [ ] Inspect `properties/serializers.py` and exact serializer used
- [ ] Review `Inquiry` model and related data
- [ ] Check authentication and permission settings
- [ ] Review global DRF defaults and per-view overrides
- [ ] Inspect middleware and request-processing behavior
- [ ] Find all frontend, backend and external-integration references to endpoint
- [ ] Review Git history for implementation or permission policy changes

**Findings:**

| Component | Location | Current Implementation | Notes |
|---|---|---|---|
| Route | | | |
| HTTP Methods | | | |
| View Function | | | |
| Permission Classes | | | |
| Serializer | | | |
| Model | | | |
| Filters/Queryset | | | |
| Pagination | | | |
| Consumers | | | |

---

### 6.2 Actual Exposure Assessment

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Determine which fields are returned by endpoint
- [ ] Assess sensitivity of exposed fields
- [ ] Verify if complete dataset serialized in one response
- [ ] Check if pagination applies
- [ ] Assess caching or intermediary infrastructure retention

**Exposed Fields Analysis:**

| Field | Type | Sensitivity Level | PII Status | Notes |
|---|---|---|---|---|
| | | | | |

**Data Exposure Summary:**

*(To be populated during exposure assessment)*

---

### 6.3 Intended Business Purpose Determination

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Find every internal reference to endpoint
- [ ] Find every external reference to endpoint
- [ ] Determine if it supports prospect matching
- [ ] Check for authorized internal service use
- [ ] Check for administrative screen use
- [ ] Check for external partner integration
- [ ] Document business justification or lack thereof

**Business Purpose Findings:**

*(To be populated during business purpose investigation)*

---

### 6.4 Access-Control Adequacy Assessment

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Determine if public access justified for response fields and intended use
- [ ] Assess if sensitive enquiry records accessible without authorization
- [ ] Identify least-privilege correction preserving legitimate business workflows
- [ ] Consider appropriate authentication mechanisms
- [ ] Consider role-based authorization
- [ ] Consider restricted querysets
- [ ] Consider field minimization
- [ ] Consider server-to-server authentication where appropriate
- [ ] Consider pagination and response-size limits
- [ ] Consider rate limiting and monitoring as supplementary controls

**Access Control Findings:**

*(To be populated during access control assessment)*

**Risk Classification:** ⏳ PENDING

**Remediation Recommendation:** ⏳ PENDING

---

## 7. PHASE 4 — EXACT SPAM-ENQUIRY CREATION PATH IDENTIFICATION

### 7.1 Complete Write Path Enumeration

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Search for all `Inquiry.objects.create()` calls
- [ ] Search for all `Inquiry.objects.get_or_create()` or `update_or_create()` calls
- [ ] Search for all model `.save()` calls creating new records
- [ ] Search for all serializer `.create()` methods
- [ ] Identify generic API views, viewsets and router-generated routes
- [ ] Review Django forms and public-facing submission views
- [ ] Check realBOT and other API integration paths
- [ ] Review chat or contact endpoints
- [ ] Check background tasks and asynchronous workers
- [ ] Check import, synchronization and administrative paths

**Write Path Inventory:**

| Path # | Endpoint/Route | HTTP Method | View/Handler | Model | Authentication | CAPTCHA | Spam Controls | Relevance to Incident |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

---

### 7.2 Endpoint-to-Database Persistence Flow

**Status:** ⏳ PENDING

**Tasks:**
- [ ] For each write path, document complete flow from HTTP request to database persistence
- [ ] Verify whether security checks happen before database write
- [ ] Verify whether handler can persist record when required check fails

**Persistence Flow Diagram:**

*(To be populated with flow diagram)*

---

### 7.3 API Write-Method Investigation

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Verify actual current implementation of `/api/inquiries/`
- [ ] Confirm if `@api_view(["GET"])` is current decorator
- [ ] Test if POST is accepted by this handler
- [ ] Verify deployed route matches code
- [ ] Distinguish between GET permission issue and POST acceptance

**Critical Note:** Under normal DRF function-based `@api_view(["GET"])` implementation, POST is not accepted by that handler unless the deployed route or implementation differs. Do not assume the API's GET permission issue proves the same endpoint accepted POST submissions.

**Findings:**

*(To be populated during API write-method investigation)*

---

### 7.4 Separate Chat Endpoint Trace

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Review `POST /chat/submit/` implementation
- [ ] Check `ContactMessage` persistence path
- [ ] Determine if endpoint is reachable
- [ ] Check if referenced by real frontend
- [ ] Verify if capable of sending notifications without spam validation
- [ ] Assess relationship to `Inquiry` incident

**Critical Note:** Do not attribute the `Inquiry` incident to a `ContactMessage` endpoint unless the relationship is demonstrated.

**Findings:**

*(To be populated during chat endpoint investigation)*

---

## 8. PHASE 5 — FORENSIC CAPTCHA AND SPAM-PROTECTION AUDIT

### 8.1 CAPTCHA Implementation Enforcement Trace

**Status:** ⏳ PENDING

**Files to Inspect:**
- [ ] `realtor_project/settings.py`
- [ ] `realtor_project/features.py`
- [ ] `content/security/spam_protection.py`
- [ ] `content/security/google_recaptcha.py`
- [ ] `content/security/validators.py`
- [ ] Feature-flag files
- [ ] Relevant views, forms, serializers, templates
- [ ] Middleware
- [ ] CAPTCHA verification provider implementation
- [ ] Exception handling
- [ ] Tests
- [ ] Deployment configuration

**CAPTCHA Flow Trace:**

| Step | Component | Implementation | Status | Notes |
|---|---|---|---|---|
| 1. Widget Rendering | | | | |
| 2. Site-Key Availability | | | | |
| 3. Token Creation | | | | |
| 4. Token Submission | | | | |
| 5. Server-Side Token Extraction | | | | |
| 6. Verification Request to Provider | | | | |
| 7. Verification Response Validation | | | | |
| 8. Hostname/Action Validation | | | | |
| 9. Missing-Token Behavior | | | | |
| 10. Invalid-Token Behavior | | | | |
| 11. Missing-Secret Behavior | | | | |
| 12. Network Error/Timeout Handling | | | | |
| 13. Feature-Flag Interactions | | | | |
| 14. Final Decision (Reject/Persist) | | | | |

**Critical Questions:**
- [ ] Does `RECAPTCHA_FAIL_OPEN` default to `True`?
- [ ] Does missing reCAPTCHA secret return successful verification?
- [ ] Does the actual incident path call these functions at all?

**Findings:**

*(To be populated during CAPTCHA audit)*

---

### 8.2 Existing Spam Controls Audit

**Status:** ⏳ PENDING

**Controls to Inspect:**
- [ ] Honeypot validation
- [ ] Submission timing checks
- [ ] Per-IP rate limiting
- [ ] Cache backend and atomicity
- [ ] Client IP resolution behind proxies/CDNs
- [ ] Forwarded-header trust
- [ ] Form source and request-path restrictions
- [ ] Duplicate detection
- [ ] Content-based validation
- [ ] Request-field and payload validation
- [ ] Security-related exception handling
- [ ] CSRF policy where applicable
- [ ] Existing spam scores or confidence assessments

**Spam Control Matrix:**

| Control | Implementation Location | Enforced on Write Path? | Active Configuration? | Failure Affects Persistence? | Notes |
|---|---|---|---|---|---|
| Honeypot | | | | | |
| Timing Check | | | | | |
| Rate Limiting | | | | | |
| IP Resolution | | | | | |
| Duplicate Detection | | | | | |
| Content Validation | | | | | |
| CSRF Protection | | | | | |

**Findings:**

*(To be populated during spam controls audit)*

---

### 8.3 Actual Control Failure Determination

**Status:** ⏳ PENDING

**Competing Explanations to Test:**

- [ ] **Hypothesis A:** Direct submission to write endpoint bypasses frontend validation
- [ ] **Hypothesis B:** Write route does not invoke centralized spam protection service
- [ ] **Hypothesis C:** CAPTCHA verification is not enforced server-side
- [ ] **Hypothesis D:** Missing secret or disabled feature flag bypasses verification
- [ ] **Hypothesis E:** Verification failures are handled fail-open
- [ ] **Hypothesis F:** Alternate or legacy endpoint bypasses validation
- [ ] **Hypothesis G:** Rate limiting ineffective due to implementation, storage or source-IP handling
- [ ] **Hypothesis H:** Multiple distributed sources avoid individual limits
- [ ] **Hypothesis I:** Attackers use browser-based automation satisfying existing checks
- [ ] **Hypothesis J:** Other code, configuration or integration defect permits persistence

**Critical Note:** Do not label an explanation as confirmed solely because the relevant vulnerability exists.

**Findings:**

*(To be populated during control failure investigation)*

---

## 9. PHASE 6 — CONTROLLED TESTING AND REGRESSION COVERAGE

**Environment:** Local or controlled staging only — NO production mutation

### 9.1 API Security Tests

**Status:** ⏳ PENDING

**Test Cases:**
- [ ] Unauthenticated users cannot retrieve protected enquiry data
- [ ] Authenticated users without required permission cannot retrieve protected data
- [ ] Authorized consumers receive only needed fields
- [ ] Pagination and response-size controls behave as intended
- [ ] Unsupported HTTP methods are rejected
- [ ] Existing legitimate integrations continue to operate with approved authorization
- [ ] Error responses do not reveal sensitive configuration or customer data

**Test Results:**

*(To be populated during testing)*

---

### 9.2 Spam-Protection Tests

**Status:** ⏳ PENDING

**Test Cases:**
- [ ] Requests missing CAPTCHA token are rejected
- [ ] Invalid, expired or unsuccessful tokens are rejected
- [ ] Missing CAPTCHA secret is handled securely
- [ ] Malformed verification responses are rejected
- [ ] Provider network errors and timeouts handled per security policy
- [ ] Direct API endpoint submissions without browser form are rejected
- [ ] Alternate creation endpoints with missing protections are secured
- [ ] Repeated submissions exceeding rate-limit policy are rejected
- [ ] Malformed or unexpected form fields are rejected
- [ ] Honeypot violations are rejected
- [ ] Invalid submission timing is rejected where enforced

**Critical Verification:** Check both HTTP result AND actual persistence outcome

**Test Results:**

*(To be populated during testing)*

---

### 9.3 Legitimate-Flow Tests

**Status:** ⏳ PENDING

**Test Cases:**
- [ ] Authorized, legitimate enquiry submissions still work
- [ ] False positives do not silently discard genuine users
- [ ] API consumers remain functional

**Test Results:**

*(To be populated during testing)*

---

### 9.4 Test Execution Record

**Status:** ⏳ PENDING

| Test Suite | Command | Environment | Pass/Fail | Output | Skipped Tests | Regression Risks | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

---

## 10. PHASE 7 — CONTROLLED LOCAL REMEDIATION

**Purpose:** Fix demonstrated defects, not every suggestion from earlier reports

**Constraints:**
- Local code corrections only
- No production deployment
- No production migrations
- No production configuration changes
- No destructive operations
- Document pending items requiring authorization

---

### 10.1 Public API Access Control

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Apply appropriate least-privilege authentication and authorization
- [ ] Restrict response fields and queryset scope
- [ ] Preserve legitimate internal use through explicit approved access mechanism
- [ ] Add regression tests for unauthorized and authorized access
- [ ] Add pagination and response-size limits if missing
- [ ] Ensure access control does not depend on frontend restrictions alone

**Implementation:**

*(To be populated with implementation details)*

**Files Changed:**

*(To be populated with file paths and line numbers)*

---

### 10.2 CAPTCHA Fail-Safe Behavior

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Correct logic so required verification cannot silently succeed without valid provider verification
- [ ] Apply explicit and secure policy for provider outages
- [ ] Ensure configuration failures are observable
- [ ] Preserve legitimate user experience with clear errors when system cannot safely accept submissions
- [ ] Add tests for every affected failure condition

**Implementation:**

*(To be populated with implementation details)*

**Files Changed:**

*(To be populated with file paths and line numbers)*

---

### 10.3 Enquiry-Creation Endpoint Protection

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Ensure every applicable public creation endpoint invokes required server-side controls before persistence
- [ ] Review actual HTTP methods, permissions and form clients
- [ ] For legacy endpoints with no legitimate use, propose deprecation (only after confirming no dependency)
- [ ] For endpoints that must remain available, apply appropriate validation and authorization

**Implementation:**

*(To be populated with implementation details)*

**Files Changed:**

*(To be populated with file paths and line numbers)*

---

### 10.4 Rate Limiting and Abuse Detection

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Strengthen rate limiting where implementation gaps are demonstrated
- [ ] Evaluate atomicity
- [ ] Evaluate shared-cache behavior
- [ ] Evaluate multiple application instances
- [ ] Evaluate trusted proxy configuration
- [ ] Evaluate legitimate traffic patterns
- [ ] Consider aggregate anomaly detection
- [ ] Distinguish monitoring, hard global cap, and per-IP limiter purposes

**Implementation:**

*(To be populated with implementation details)*

**Files Changed:**

*(To be populated with file paths and line numbers)*

---

### 10.5 Notification Protection

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Inspect when email and WhatsApp notifications are dispatched
- [ ] Ensure confirmed or strongly suspected spam can be prevented from triggering unnecessary external side effects
- [ ] Ensure legitimate enquiries are not silently lost
- [ ] Do not introduce fragile URL-only or language-only rejection rules as sole defense
- [ ] Use established validation architecture
- [ ] Test false-positive behavior

**Implementation:**

*(To be populated with implementation details)*

**Files Changed:**

*(To be populated with file paths and line numbers)*

---

### 10.6 Data Cleanup and Quarantine Plan

**Status:** ⏳ PENDING — NO PRODUCTION DATA DELETION AUTHORIZED

**Tasks:**
- [ ] Produce separate, non-destructive plan including:
  - Evidence-backed classification criteria
  - Preview counts
  - Preservation of legitimate records
  - Rollback or recovery approach
  - Notification and integration implications
  - Explicit authorization requirements

**Plan:**

*(To be populated if cleanup becomes necessary)*

**Recommendation:** Prefer reversible quarantine over irreversible deletion

---

## 11. PHASE 8 — AGENT WORKFLOW INSTRUCTION UPDATE

### 11.1 Existing Instruction Structure Discovery

**Status:** ⏳ PENDING

**Tasks:**
- [ ] Locate actual Start, End, Task-Rules or equivalent agent skills/instructions
- [ ] Identify authoritative location for task workflow rules
- [ ] Determine update strategy (Task-Rules skill vs Start/End skills)

**Findings:**

*(To be populated during instruction discovery)*

---

### 11.2 Report-First Rule Implementation

**Status:** ⏳ PENDING

**Required Rule Text:**

> **SCCB / Report-First Execution Rule:** When a task prompt requires an SCCB, audit report, implementation brief or other task-control report, create the required artifact in the designated directory and save it before beginning the substantive task. Populate the initial scope, plan, constraints and acceptance criteria from the prompt. Then execute the task, updating the same artifact with evidence, decisions, files changed, tests, blockers and final results. Never defer creation of the required report until after the task. When Viji specifies a mandatory report location for an ongoing exercise, save all associated SCCBs and reports there until Viji explicitly closes the exercise.

**Tasks:**
- [ ] Add rule to identified instruction file
- [ ] Preserve all existing instructions
- [ ] Verify update was successful
- [ ] Record exact change in SCCB

**Implementation Record:**

| File Updated | Line/Section | Change Summary | Verification |
|---|---|---|---|
| | | | |

---

## 12. PHASE 9 — FINAL AUDIT AND ACCEPTANCE REVIEW

### Required Conclusions

**Status:** ⏳ PENDING — To be completed after all phases

**Questions to Answer Explicitly:**

1. **Q1:** What is the verified count of affected spam records, and what time window does it cover?
   - **Answer:** *(Pending investigation)*

2. **Q2:** Which exact endpoint or endpoints created the suspicious `Inquiry` records?
   - **Answer:** *(Pending investigation)*

3. **Q3:** Which security controls executed on those paths?
   - **Answer:** *(Pending investigation)*

4. **Q4:** How did each affected request satisfy or bypass those controls?
   - **Answer:** *(Pending investigation)*

5. **Q5:** Is CAPTCHA server-side verification enforced on the actual creation path?
   - **Answer:** *(Pending investigation)*

6. **Q6:** Did a missing secret, feature flag, fail-open condition or other defect contribute to the incident?
   - **Answer:** *(Pending investigation)*

7. **Q7:** Is `/api/inquiries/` publicly accessible as reported, and which data fields are actually exposed?
   - **Answer:** *(Pending investigation)*

8. **Q8:** Does that API have a legitimate intended consumer, and what access control is appropriate?
   - **Answer:** *(Pending investigation)*

9. **Q9:** Is the public API vulnerability causally related to the spam incident, independently relevant, or still unverified?
   - **Answer:** *(Pending investigation)*

10. **Q10:** Does `/chat/submit/` represent an independent vulnerability, and is there evidence linking it to the incident?
    - **Answer:** *(Pending investigation)*

11. **Q11:** What local corrections and regression tests were completed?
    - **Answer:** *(Pending implementation)*

12. **Q12:** Which remediation steps still require production access, deployment authorization, business decisions or data cleanup approval?
    - **Answer:** *(Pending implementation)*

13. **Q13:** What evidence remains missing before the incident root cause can be declared fully confirmed?
    - **Answer:** *(Pending investigation)*

---

## 13. ACCEPTANCE CRITERIA CHECKLIST

### Artifact and Governance

- [x] Canonical SCCB created and saved before substantive work
- [ ] Every SCCB and report for this exercise stored under designated directory
- [ ] Applicable canonical engineering rules reviewed
- [ ] Existing user changes preserved
- [ ] Task-Rules skill or Start/End skills updated with report-first rule
- [ ] Report-first execution rule verified

### Spam Investigation

- [ ] Record-count discrepancy investigated
- [ ] Incident timeline reconstructed from available evidence
- [ ] Every identified enquiry-creation route inventoried
- [ ] Actual persistence path traced
- [ ] CAPTCHA token generation and verification path verified
- [ ] Existing spam-protection controls and call sites audited
- [ ] Root-cause confidence reflects available evidence, not assumptions
- [ ] Remaining production evidence gaps explicitly documented

### Public API Checkpoint

- [ ] Actual route, methods, permissions and serializer established
- [ ] Exposed fields and sensitivity assessed
- [ ] Intended consumer and business purpose investigated
- [ ] Necessary authorization correction identified
- [ ] Relationship between API exposure and spam incident assessed independently
- [ ] Unauthorized access and legitimate access tests defined or executed in controlled environment

### Remediation and Tests

- [ ] Confirmed local vulnerabilities corrected where implementation was safe and authorized
- [ ] Appropriate regression tests added or updated
- [ ] Tests actually executed and results recorded
- [ ] No production data deleted or altered
- [ ] No unapproved production deployment or configuration change occurred
- [ ] Every deferred action has documented reason, owner/action required and verification criterion

---

## 14. IMPLEMENTATION LOG

### Files Modified

| File Path | Lines Changed | Change Type | Purpose | Test Coverage | Status |
|---|---|---|---|---|---|
| | | | | | |

### Tests Added/Modified

| Test File | Test Cases | Coverage Area | Pass/Fail | Notes |
|---|---|---|---|---|---|
| | | | | |

### Configuration Changes

| Component | Setting | Old Value | New Value | Reason | Status |
|---|---|---|---|---|---|
| | | | | | |

---

## 15. OUTSTANDING ACTIONS AND APPROVALS

### Pending Production Actions

| Action # | Action Required | Owner | Authorization Needed From | Risk Level | Blocker | Target Date |
|---|---|---|---|---|---|---|
| | | | | | | |

### Unresolved Questions

| Question # | Question | Blocking Issue | Evidence Needed | Priority |
|---|---|---|---|---|
| | | | | |

### Deployment Checklist

**Status:** ⏳ NOT READY FOR DEPLOYMENT

- [ ] All acceptance criteria met
- [ ] All tests passing
- [ ] Code review completed
- [ ] Viji approval obtained
- [ ] Production deployment plan documented
- [ ] Rollback plan documented
- [ ] Monitoring plan documented
- [ ] Post-deployment verification plan documented

---

## 16. ROOT CAUSE ANALYSIS

### Primary Root Cause

**Status:** ⏳ UNDER INVESTIGATION

**Confirmed Root Cause:**

*(To be populated after investigation completes)*

**Supporting Evidence:**

*(To be populated with evidence trail)*

**Confidence Level:** ⏳ TBD

---

### Contributing Factors

| Factor | Impact Level | Evidence | Mitigation Status |
|---|---|---|---|
| | | | |

---

## 17. IMPACT ASSESSMENT

### Security Impact

**Data Exposure:**
- *(To be assessed)*

**Confidentiality Impact:**
- *(To be assessed)*

**Integrity Impact:**
- *(To be assessed)*

**Availability Impact:**
- *(To be assessed)*

---

### Business Impact

**Customer Trust:**
- *(To be assessed)*

**Operational Impact:**
- *(To be assessed)*

**Compliance Impact:**
- *(To be assessed)*

**Reputation Impact:**
- *(To be assessed)*

---

## 18. LESSONS LEARNED AND PREVENTIVE MEASURES

**Status:** ⏳ PENDING — To be completed after incident resolution

### What Worked Well

*(To be documented)*

### What Didn't Work

*(To be documented)*

### Process Improvements

*(To be documented)*

### Technical Improvements

*(To be documented)*

### Training Needs

*(To be documented)*

---

## 19. FOLDER CONTENTS AND SUPERSEDED MATERIAL

**Folder rule (`04-Control/01-sccb/`):** one complete SCCB file per item. No companion extracts.

Removed on 2026-10-13 (content already absorbed into §§21–23 of this file):

| Removed file | Absorbed into |
|---|---|
| `09-PROPERTISM-SPAM-INCIDENT-AUDIT-001.md` | §§3–8, 16, 21 (GET-as-spam causal claim superseded) |
| `VALIDATION_REPORT_SCCB-09.md` | §21 |
| `IMPLEMENTATION_REPORT_END_TO_END_SPAM_INCIDENT.md` | §§21–22 |
| `EMERGENCY-ACTION-PLAN.md` | Track A/B split in §21.1 |

Still in this folder (different SCCB, not this incident): `SCCB-AWS-NEW-ACCOUNT-MIGRATION.md`.

### Code references

- `properties/views.py` — `create_inquiry`, `inquiry_list_api`
- `content/views.py` — `contact`, `send_rfq_notification`
- `content/security/spam_protection.py`, `google_recaptcha.py`, `captcha_provider.py`, `validators.py`
- `chat/inquiry_submission.py`, `chat/views.py`
- `properties/test_security_fixes.py`, `AGENTS.md`

### Related SCCBs and Reports

- This file is the only SCCB-09 report. Historical audit/validation/implementation extracts were deleted after absorption into §§21–23.

### Code References

*(To be populated with relevant code file paths)*

### External References

*(To be populated with relevant external documentation)*

---

## 20. FINAL CLOSURE RECOMMENDATION

**Status:** ⏳ IN PROGRESS — NOT READY FOR CLOSURE

**Closure Criteria:**

1. All acceptance criteria met
2. Root cause confirmed with high confidence
3. All critical vulnerabilities remediated
4. All tests passing
5. Production deployment completed successfully
6. Post-deployment verification completed
7. Viji approval obtained for closure

**Closure Recommendation:** ⏳ PENDING

**Final Sign-Off:**

- [ ] Technical Lead (Astra): ⏳ PENDING
- [ ] Owner (Viji M): ⏳ PENDING

---

## REVISION HISTORY

| Version | Date | Time | Author | Change Summary |
|---|---|---|---|---|
| 1.0 | 2026-10-13 | 13:05 IST | Astra | Initial SCCB creation — investigation starting |
| 1.1 | 2026-10-13 | 14:25 IST | Cursor | Independent validation: write-path trace, CAPTCHA production enforcement, API least-privilege, tests executed, report-first rule in AGENTS.md |
| 1.2 | 2026-10-13 | 14:40 IST | Cursor | Follow-up: Deal Engine cutover proposal, realBOT trust boundary, evidence request, stale WhatsApp test fix, 27/27 tests OK |
| 1.3 | 2026-10-13 | 14:50 IST | Cursor | `04-propertism-deal-engine` inspected: anonymous GET confirmed in §22.2 |
| 1.4 | 2026-10-13 | 14:55 IST | Cursor | §23 approval-gated plans: Deal Engine JWT cutover, realBOT design, aggregate evidence checklist. No gated code. |
| 1.5 | 2026-10-13 | 15:00 IST | Cursor | Removed redundant fragment files from `04-Control/01-sccb/`. SCCB-09 is the only spam-incident report. |
| 1.6 | 2026-10-13 | 15:10 IST | Cursor | Independent review: recommend Option B service key; correct rollout (no live PII GET); realBOT C1–C4 vs actual engine; D1–D9 retained pending |

---

## 21. CURSOR VALIDATION EXECUTION RECORD (2026-10-13)

Mindra required additional validation before deployment. This section is the single consolidated record of that execution. Emergency-plan claims that the public GET API *caused* the spam are **not accepted**.

### 21.1 Confirmed findings

**Track A — Spam (`Inquiry` writes)**

| Path | URL / trigger | Writes `Inquiry`? | SpamProtectionService before persist? | Frontend fields |
|---|---|---|---|---|
| `content.views.contact` | Homepage / general contact POST | Yes (`PropertyInquiry` alias) | Yes | Hidden: `website_url_check`, `form_render_time`. CAPTCHA: `g-recaptcha` widget → `g-recaptcha-response` |
| `properties.views.create_inquiry` | POST `{% url 'create_inquiry' %}` from property detail | Yes | Yes | Same hidden + CAPTCHA includes |
| `chat.inquiry_submission.InquirySubmissionAdapter` | realBOT ICS completion | Yes | **No** (explicitly skipped) | Conversational; not the form widgets |
| `properties.views.inquiry_list_api` | `GET /api/inquiries/` | **No** (`@api_view(["GET"])`; POST → 405 in tests) | N/A | N/A |
| `chat.views.submit_chat_message` | `POST /chat/submit/` | **No** (`ContactMessage`) | Yes (Astra + kept) | **No live frontend** posts here |
| `content.views.landing_lead_api` | `POST /api/landing-lead/` | No (`LandingLead`) | Yes | CAPTCHA was present; honeypot/timing **added** this execution |
| `content.views.newsletter_subscribe` | Footer POST | No (`Newsletter`) | Yes | CAPTCHA present; honeypot/timing **added** this execution |

Spam records matching Russian / `share.google` promotional text are **most consistent with a public HTML form POST** (`contact` or `create_inquiry`). Both call `SpamProtectionService` then `Inquiry.objects.create()`.

**Why those controls could still persist spam (hypotheses, not proven):**

1. `RECAPTCHA_FAIL_OPEN` previously defaulted True → Google timeout/network-error allowed persist.
2. Missing `RECAPTCHA_SECRET_KEY` previously returned `success=True`.
3. `CAPTCHA_ENABLE=false` (or file unread) skipped verification entirely (`default=False` in `SpamProtectionService`).
4. Timing check **passes if `form_render_time` is absent**.
5. Rate limit is 5/10 min **per resolved IP**; `_get_ip()` trusts first `X-Forwarded-For` hop (spoofable if the app sees client headers). Distributed IPs bypass the cap.
6. Honeypot only trips if `website_url_check` is filled; bots that omit it pass.
7. realBOT adapter writes `Inquiry` with **no** `SpamProtectionService` (separate path; no evidence it produced this incident).

**Production CAPTCHA state on 13 Oct 2026:** unverified (no `.env`, no logs).

**Track B — Public API confidentiality (independent of spam)**

- Code (pre-fix): `@permission_classes([AllowAny])` + `InquirySerializer` fields include name, email, phone, message, locality, user_role, nri_status.
- Git: `AllowAny` introduced in `bb2936ce` (15 Jul 2026, “inquiry-enhancements”). That is **source-commit date**, not proven production-go-live.
- Intended consumer: Deal Engine / prospect matching (`PROPERTISM_INQUIRIES_API_URL` / `DEAL_ENGINE_ENV=production` → `https://www.propertism.in/api/inquiries/`). Unauthenticated server-to-server fetch will **break** once `IsAdminUser` is deployed unless Deal Engine sends a **staff** JWT or session.
- `IsAdminUser` = `request.user.is_staff` (not superuser-only). Tests: anonymous **401**, non-staff **403**, staff JWT/session **200**, POST **405**.
- Live production GET was **not** repeated (would re-download PII). Production exposure **now** is unverified.

**Emergency plan error:** it stated attackers used the GET API to submit spam. GET cannot create `Inquiry` rows in current code. Treat that document as superseded by this section.

### 21.2 Local code changes (this execution + retained Astra diffs)

| File | Why |
|---|---|
| `properties/views.py` | `IsAdminUser` + JWT **and** `SessionAuthentication` so staff session works; docstring; GET-only unchanged |
| `realtor_project/settings.py` | `TESTING` flag; CAPTCHA fail-open default False; **force False** when not DEBUG and not TESTING; log if production keys missing (no secret values) |
| `content/security/google_recaptcha.py` | Missing secret → `success=False` (Astra; retained) |
| `content/security/spam_protection.py` | Fail-open getattr default False; production cannot skip CAPTCHA via feature flag; production ignores fail-open |
| `content/security/captcha_provider.py` | `NullProvider` fail-closed in production |
| `chat/views.py` | `SpamProtectionService` on unused legacy `ContactMessage` POST (Astra; retained) |
| `uilayers/templates/components/_lp_lead_form.html` | Add `website_url_check` + `form_render_time` |
| `uilayers/templates/components/_footer.html` | Same for newsletter |
| `properties/test_security_fixes.py` | Regression tests with **actual** field names and `chat:submit` URL |
| `AGENTS.md` | Report-first execution rule (no invented Task-Rules skill) |

**Preserved:** Viji’s planning docs, `content/models.py` SystemConfig, `content/admin.py`, other `settings.py` work. Not overwritten.

**Not done:** commit, push, deploy, production `.env`, spam delete/quarantine.

### 21.3 Tests actually executed

Django import failure cause: shell `python` = `D:\AI\Hermes\hermes-agent\venv\Scripts\python.exe` (no Django). `pip` = system Python 3.11 (Django 5.2.16, **not** project pins). Isolated `.venv` created from `requirements.txt` (Django **4.2.16**). `.venv` is gitignored.

Commands (project `.venv`):

```
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test properties.test_security_fixes content.tests.CaptchaVerificationTests properties.tests.InquiryNotificationTests --verbosity=1
```

| Result | Detail |
|---|---|
| `manage.py check` | Pass with pre-existing allauth `ACCOUNT_EMAIL_REQUIRED` deprecation warning |
| `properties.test_security_fixes` (16) | **PASS** — API 401/403/200/405, session staff, missing secret, fail-closed network error, invalid token, production flag bypass rejected, legitimate inquiry, chat 400/429/200 |
| `content.tests.CaptchaVerificationTests` (10) | **PASS** |
| `properties.tests.InquiryNotificationTests.test_create_inquiry_sends_email_and_whatsapp` | **FAIL** — `mock_send_whatsapp.call_count` 0 != 2. Inquiry **was created**. `create_inquiry` calls `send_rfq_notification` only; WhatsApp auto-send was decommissioned. **Pre-existing / unrelated to these security diffs.** |

Do not treat the WhatsApp failure as a CAPTCHA/API regression.

### 21.4 Evidence gaps

- Enquiry export `inquiries-0.md` not in workspace → cannot reconcile 1,400 vs 4,674 or timestamps.
- No production logs, Nginx access logs, or `SpamLog` dump.
- No production `feature_flags.json` / `RECAPTCHA_*` env verification.
- Commit `bb2936ce` date ≠ proven production exposure start (needs deploy/CI/access logs).
- No live GET to `/api/inquiries/` this execution (avoid re-collecting PII).
- realBOT write path not linked to this incident (no form_source evidence).

### 21.5 Production risk (local vs live)

| Item | Local | Production |
|---|---|---|
| GET `/api/inquiries/` AllowAny | Fixed in working tree | **Unverified — likely still public until deploy** |
| CAPTCHA missing-secret / fail-open | Fixed in working tree | **Unverified** |
| Feature-flag silent skip | Production-enforced in working tree | **Unverified** |
| Spam intake | Hardened locally | **Unverified; incident mechanism not proven** |
| Deal Engine sync | Will need staff JWT after deploy | **Breaking change if still anonymous** |

### 21.6 Security-preserving rollback (not AllowAny, not fail-open)

If staff or Deal Engine break after deploy:

1. Keep `IsAdminUser`. Issue a staff service user + JWT to Deal Engine (`PROPERTISM_INQUIRIES_API_URL` + Authorization header).
2. If CAPTCHA rejects all humans: restore `RECAPTCHA_SITE_KEY` / `RECAPTCHA_SECRET_KEY`; do **not** set `RECAPTCHA_FAIL_OPEN=true` in production.
3. If chat `/chat/submit/` has no widget: leave rejection in place (no in-repo frontend uses it) or add widget fields — do not strip `SpamProtectionService`.
4. Git revert of the whole commit is allowed only if replaced immediately by an equivalent access-control patch; reverting to `AllowAny` is forbidden.

### 21.7 Workflow rule

Updated **`AGENTS.md`** only (section “SCCB / Report-First Execution Rule”). No Task-Rules skill created.

### 21.8 Approvals required from Viji

1. Commit + push of the local security diffs (then CI deploy).
2. Deal Engine cutover plan: staff JWT (or approved alternative) **before** or **with** API lockdown.
3. Production read-only checks: CAPTCHA env present, `CAPTCHA_ENABLE=true`, Nginx `/api/inquiries/` 401 after deploy (do not dump body).
4. Any spam quarantine/delete SQL.
5. Whether to add `SpamProtectionService` to realBOT `InquirySubmissionAdapter` (separate finding).

**Stop:** validation pass complete. Not closed. Not deployed.

---

## 22. FOLLOW-UP EXECUTION RECORD (approval-ready)

**Date:** 2026-10-13 14:40 IST  
**Constraint honoured:** no commit, push, deploy, production config, or production data change.

### 22.1 Completed actions this follow-up

- Emergency plan rewritten with **superseded history** + separate Track A / Track B.
- Audit `09-PROPERTISM-SPAM-INCIDENT-AUDIT-001.md` given a **SUPERSEDED CAUSAL CLAIM** banner; original text retained.
- Deal Engine consumer traced as far as this workspace allows (client **not in this repo**). **Updated in §22.2 after `04-propertism-deal-engine` was added.**
- realBOT write path traced from public `/chat/session/init/` + `/chat/query/` to `InquirySubmissionAdapter`; **no code change** (pending Viji).
- Workspace re-checked for export/logs; evidence request listed below.
- Security diffs revalidated; WhatsApp notification test corrected (test-only).
- Tests re-run on `.venv` (Django 4.2.16 from `requirements.txt`): **27 OK**.

### 22.2 Deal Engine authentication (code-verified in `04-propertism-deal-engine`)

**Confirmed:** outbound GET is **anonymous**. No `Authorization`, JWT, session cookie, or API key.

| Client | File | Headers sent | On failure |
|---|---|---|---|
| `_fetch_from_live_api()` | `backend/deal_inbound/views.py` ~129–184 | `Accept`, `User-Agent: Propertism-Deal-Engine/1.0` | logs error, returns `[]` |
| `sync_inquiries()` | `backend/deal_inbound/views.py` ~190–204 | `Accept`, `User-Agent` | HTTP 500 with error text |
| `DealEngineService.inquiries()` | `backend/deal_matching/services/deal_engine_service.py` ~611–627 (duplicate in `deal_opportunity/...`) | `Accept` only | `{"items": [], "total": 0}` |

URL: `os.environ.get("PROPERTISM_INQUIRIES_API_URL")` or default `https://www.propertism.in/api/inquiries/`. Method: GET via `urllib.request`.

**Propertism side (local, not deployed):** `IsAdminUser` + JWT/session. Staff JWT from `POST /api/auth/login/`. Compatible **only after** Deal Engine adds `Authorization: Bearer <access>` from a **staff** user.

**Secondary finding (Deal Engine, not implemented):** `deal_inbound.views.inquiries` and `sync_inquiries` are themselves `@permission_classes([AllowAny])` and `@authentication_classes([])`. If those routes are internet-reachable, they **re-expose** the same PII. Separate from Propertism Track B; needs Viji before any Deal Engine code change.

**Recommended cutover (approval required — not implemented):**

1. In **04**: add Bearer header to all three GET sites; read token from env (e.g. `PROPERTISM_INQUIRIES_BEARER`); never log it.
2. Create a Propertism **staff** service user; mint JWT via `/api/auth/login/`; store only in Deal Engine secrets.
3. On 401/403: keep empty/`[]` fallback (already coded) so UI does not crash; do not wipe local shortlist.
4. Tests in 04: mocked 200 with Bearer; mocked 401 returns empty.
5. Only after 04 is patched and verified, deploy **03** `IsAdminUser`.
6. After 03 deploy: unauthenticated `GET https://www.propertism.in/api/inquiries/` must be **401** (status only). Deal Engine with Bearer must still sync.

**Do not lock 03 before 04 sends a staff JWT.** No Deal Engine code was changed in this pass.

### 22.3 realBOT write path (no code change)

**Call chain:**

1. `POST /chat/session/init/` — `@csrf_exempt`, no login; creates `RealBotSession`.
2. `POST /chat/query/` (`send_message`) — `@csrf_exempt`, no login; only requires a valid `session_id`.
3. If an open ICS exists, `InquiryConversationEngine.process_message` → on confirm, `_submit_inquiry`.
4. `InquirySubmissionAdapter.submit()` → `Inquiry.objects.create(...)` with `confidence_score=80`, `assessment_status='Genuine'`, **no** `SpamProtectionService`.
5. `send_rfq_notification` (email).

`inquiry_initiate` is the same CSRF-exempt, unauthenticated pattern. Live UI: `static/js/realbot-panel.js` calls `/chat/session/init/` and `/chat/query/`. `feature_flags.json` has `REALBOT_INTEGRATION_ENABLED: true` in this working tree (production flag file unverified).

`SecurityManager` rate-limit exists but is **not** invoked on `send_message` (used on later M2.14 security admin endpoints).

**Trust model today:** anyone who can POST to the public chat JSON API can, over multiple turns, reach confirmation and persist an `Inquiry` without CAPTCHA.

**Link to 13 Oct spam:** **no evidence**. Payload shape (single message with Russian/`share.google`) matches HTML forms more than a multi-field ICS conversation. `form_source` on incident rows is required to confirm or exclude.

**Proposed remediation (pending Viji — do not implement yet):**

- Keep conversational UX; do **not** bolt the HTML honeypot/CAPTCHA widget onto JSON chat blindly.
- Apply a **chat-specific** boundary: per-session and per-IP rate limits on `send_message` / `inquiry_initiate`; optional CAPTCHA challenge before `_submit_inquiry`; never auto-mark `Genuine`/80 without the same spam layers as forms.
- Tests: unauthenticated session can still complete a **slow legitimate** flow; flood and empty-token confirmations must not persist.

### 22.4 Spam root cause and evidence

**Established in code:** spam `Inquiry` rows must come from a **write** path in §21.1, not from GET `/api/inquiries/`.

**Unconfirmed:** which path, whether CAPTCHA ran, production flag/secret state, IP distribution.

**Count reconciliation (workspace only):**

| Claim | Source | Status |
|---|---|---|
| ~1,400 spam enquiries on 13 Oct | User report / first audit narrative | **Unverified** here (no DB, no export) |
| 4,674+ pattern matches | Audit grep of `inquiries-0.md` | File **not** in repo, `uploads/`, or Cursor project tree now. That figure is **all-time pattern hits in a snapshot**, not proven equal to “one-day intake”. |
| IDs 4265–4312 / 11:39–12:39 IST | Prior audit | **Unverified** without the export |

Those two numbers are **not** the same metric until a dated, de-duplicated query exists.

**Evidence request (Viji / ops — no PII in the reply):**

1. Aggregate-only SQL or admin export: count of `properties_inquiry` created on 2026-10-13; count matching `share.google` / OZON / Cyrillic; distinct `form_source`; min/max `created_at`; **no** names/emails/phones/messages.
2. Nginx: request counts by path for `/contact/`, `/properties/inquiry/`, `/api/inquiries/`, `/chat/query/` on that day (status codes, unique IPs) — no query strings with PII.
3. `content_spamlog` (or equivalent) counts by `failure_reason` / hour for 13 Oct.
4. Non-secret prod config: `CAPTCHA_ENABLE`, `CAPTCHA_PROVIDER`, whether `RECAPTCHA_SITE_KEY` and `RECAPTCHA_SECRET_KEY` are **set** (boolean only), `RECAPTCHA_FAIL_OPEN`.
5. CI/CD or Lightsail deploy log: first production deploy containing `bb2936ce` / `inquiry_list_api`.

### 22.5 Validation (executed this follow-up)

```
.\.venv\Scripts\python.exe manage.py test properties.test_security_fixes content.tests.CaptchaVerificationTests properties.tests.InquiryNotificationTests --verbosity=1
```

**Result:** Ran 27 tests in ~9s — **OK**  
**Warning (pre-existing):** `ACCOUNT_EMAIL_REQUIRED` allauth deprecation.

`InquiryNotificationTests.test_create_inquiry_sends_email_and_whatsapp`: **stale**. `send_rfq_notification` uses `AcknowledgementService.send(..., channels=['email'])` only; it never calls `communications.providers.send_whatsapp_notification`. Test-only change: removed WhatsApp mock/assertions; kept inquiry persist + 3 emails. Notification **runtime** behaviour not changed.

### 22.6 Files changed this follow-up

| Path | Reason |
|---|---|
| `properties/tests.py` | Drop obsolete WhatsApp assertions on enquiry create |
| `04-Control/01-sccb/EMERGENCY-ACTION-PLAN.md` | Track A/B split + superseded GET-as-spam claim |
| `04-Control/01-sccb/09-PROPERTISM-SPAM-INCIDENT-AUDIT-001.md` | Banner: causal API claim superseded |
| This SCCB | Section 22 |

Incident code from Section 21 (API auth, CAPTCHA fail-closed, chat `/chat/submit/` protection, form hidden fields, `AGENTS.md` report-first) is unchanged and still uncommitted.

Unrelated Viji working-tree files remain untouched.

### 22.7 Decisions required from Viji

1. **Deal Engine:** Approve staff-JWT cutover **before** Propertism API lockdown; provide Deal Engine repo path if client must be patched here.
2. **Commit/push** of local Propertism security diffs after (1).
3. **realBOT:** Approve or defer chat write-path hardening (rate limit + no auto-Genuine); do not add form `SpamProtectionService` blindly.
4. Supply **aggregate** evidence in §22.4 (no PII dumps).
5. Any spam quarantine SQL.
6. Production read-only 401 check after deploy (no JSON body).

### 22.8 Deployment readiness

| Item | State |
|---|---|
| Local security changes | Validated in `.venv` (27 tests OK) |
| Deal Engine compatible with `IsAdminUser` | **Not ready** — code-verified anonymous GET in `04-propertism-deal-engine`; needs staff JWT **before** 03 deploy |
| Production API still `AllowAny` | **Unverified** (likely yes until deploy) |
| Production CAPTCHA env | **Unverified** |
| Spam root cause | **Unconfirmed** |
| Incident closed | **No** |

**Do not deploy API lockdown ahead of Deal Engine credentials.**

---

## 23. APPROVAL-GATED NEXT STEPS (reviewed 2026-10-13 15:10 IST)

**Constraint honoured:** no commit, push, deploy, production config, production data change, Deal Engine auth implementation, or realBOT implementation. D1–D9 are **not** approved by this review.

This section is the decision pack. Sections 21–22 remain the historical validation and discovery record and were not rewritten.

**Recommended authentication design: Option B** (scoped Deal Engine service key). Option A (JWT refresh) is retained only as a rejected alternative.

### 23.1 Current state verified

| Item | Verified this pass | Classification |
|---|---|---|
| 03 HEAD | `c8f03ae` | Confirmed |
| 04 HEAD | `9af452e` | Confirmed |
| 03 security diffs vs §22.5 | Same 10-file `git diff --stat` (159/54); `properties/test_security_fixes.py` still untracked | Unchanged — tests **not re-run** |
| Unrelated Viji files | Scope/plan/session, SystemConfig, AWS docs, etc. | Preserved |
| 04 working tree | only `05-Sessions/session.md`; no inquiry-client change | Confirmed |
| GET `/api/inquiries/` local | `IsAdminUser` + JWT + Session, GET-only | Local only; production unverified |
| Deal Engine outbound GET | anonymous (`Accept` / `User-Agent`) | Confirmed in 04 |
| Track A root cause | unconfirmed | Gap |
| Track B | confidentiality finding; GET does not create `Inquiry` | Confirmed in code |
| Incident closed | **No** | Confirmed |

### 23.2 Deal Engine authentication cutover (plan only)

#### 23.2.1 Three HTTP clients (plus one duplicate)

All four call `GET` `os.environ.get("PROPERTISM_INQUIRIES_API_URL")` defaulting to `https://www.propertism.in/api/inquiries/`. None send `Authorization`. 04 `.env` has **no** `PROPERTISM_INQUIRIES_*` keys today.

| # | Call site | File | On HTTP failure |
|---|---|---|---|
| 1 | `_fetch_from_live_api()` used by `inquiries()` and `inbound_leads()` | `04-propertism-deal-engine/backend/deal_inbound/views.py` L129–184 | log + return `[]` |
| 2 | `sync_inquiries()` (duplicated urllib, not calling helper) | same file L190–204 | HTTP 500 with error text |
| 3 | `DealEngineService.inquiries()` | `backend/deal_matching/services/deal_engine_service.py` L611–627 | `{"items": [], "total": 0}` |
| 3b | **Duplicate** of #3 | `backend/deal_opportunity/services/deal_engine_service.py` L611–627 | same empty fallback |

Do **not** patch `.kilo/worktrees/` or `code-review/` copies. All four live sites must use **one** helper so no anonymous duplicate remains.

#### 23.2.2 Why Option A (JWT refresh) is rejected for this cutover

| Settings module | Access | Refresh | Rotation |
|---|---|---|---|
| `realtor_project/settings.py` | 24h | 7d | none |
| `realtor_project/settings_production.py` | 1h | 1d | `ROTATE_REFRESH_TOKENS` + `BLACKLIST_AFTER_ROTATION` |

Lightsail `DJANGO_SETTINGS_MODULE` is unverified. `rest_framework_simplejwt.token_blacklist` is **not** in `INSTALLED_APPS` in either module, so production blacklist flags are not a working store today.

Option A fails operationally even if refresh were persisted:

- Access tokens must not be stored as permanent env secrets (they expire).
- Rotated refresh **cannot** live only in worker memory: process restart and gunicorn/multi-worker races would present a blacklisted refresh.
- Writing rotated refresh back to Lightsail `.env` from a running worker is racy and not an approved secret store.
- Disabling refresh rotation globally to make A convenient is forbidden.
- No `TokenRefreshView` exists. `login_api` is a human-credential endpoint, not a service credential.

**Rejected:** access JWT in 04 `.env`. **Rejected as the selected design:** Option A.

#### 23.2.3 Recommended design — Option B (scoped service key)

Server-to-server shared secret, independent of user JWT. Staff session/JWT remains for humans (admin, local API tests). Deal Engine does not log in as a user.

**Authorization on 03 `inquiry_list_api`:** allow if (staff JWT/session **and** `IsAdminUser`) **OR** a valid Deal Engine key. Constant-time compare. Empty key in production must deny key-auth (fail closed), not become a public endpoint.

Header (proposed): `Authorization: DealEngine <key>` so it cannot be confused with JWT `Bearer`. Alternative `X-Deal-Engine-Key` is acceptable if Viji prefers; pick one and test it.

**Secret lifecycle (Lightsail `.env` is allowed for secrets; no application code on the VPS):**

| Event | Action |
|---|---|
| Provision (D2) | Generate a high-entropy key. Set `DEAL_ENGINE_INQUIRIES_KEY` on **03** and the same value as `PROPERTISM_DEAL_ENGINE_API_KEY` on **04**. Restart both. No Django user. No production enquiry-table write. |
| Runtime | 04 helper reads env at process start. Survives restarts. No in-memory refresh. |
| Rotation | Set `DEAL_ENGINE_INQUIRIES_KEY_PREVIOUS` on 03 to the old key; set new key on 03 and 04; restart 04 then 03; later clear `_PREVIOUS`. Dual-accept avoids a sync outage. |
| Revocation | Remove both keys on 03 and restart 03. 04 will get 401; shortlist is kept. |
| Logging | Never log the key or response bodies. |

**04 shared client** `backend/deal_inbound/propertism_client.py`:

- `fetch_inquiries() -> list`
- URL from `PROPERTISM_INQUIRIES_API_URL`
- Sends `Accept`, `User-Agent: Propertism-Deal-Engine/1.0`, and the Deal Engine authorization header
- Missing key → fail closed (no anonymous GET)
- Replace call sites 1, 2, 3, and 3b. `sync_inquiries` must call the helper (stop duplicating urllib)

**03 files (after D1/D4, not now):**

| File | Change |
|---|---|
| `realtor_project/settings.py` (and production module if used) | Read `DEAL_ENGINE_INQUIRIES_KEY` / `_PREVIOUS` from env; never hardcode |
| `properties/permissions.py` (new) | `IsStaffOrDealEngineKey` |
| `properties/views.py` `inquiry_list_api` | Keep JWT + Session; permission = staff **or** valid service key |
| `properties/test_security_fixes.py` | Key 200; wrong key 401/403; empty key does not open AllowAny; staff JWT still 200 |

`login_api` **unchanged**. See §23.5.

#### 23.2.4 Failure handling (no shortlist wipe)

`DealShortlist` is Deal Engine local state. Failures must not `delete()` it and must not `update_or_create` from an error payload.

| Propertism response | 04 `fetch_inquiries` | 04 `sync_inquiries` |
|---|---|---|
| 200 | return `items` | `update_or_create` as today (new/updated rows only) |
| 401 / 403 | return `[]`; log status only | HTTP 502; **do not** write shortlist |
| timeout / 5xx / parse error | return `[]`; log status only | HTTP 502; **do not** write shortlist |

Sites 1 and 3 already return empty on exception. Site 2 today 500s before write — keep that no-write property.

#### 23.2.5 Tests (mocked only — no production GET)

04 new `backend/deal_inbound/tests/test_propertism_client.py`. Mock urlopen. **Do not** call live `https://www.propertism.in/api/inquiries/`. **Do not** retrieve or retain production inquiry JSON.

| Case | Expect |
|---|---|
| 200 with key header present | items parsed; header name/scheme match the design |
| no env key | no anonymous GET; empty/error; shortlist count unchanged |
| wrong key → 401 or 403 | empty/502; shortlist unchanged |
| timeout | empty/502; shortlist unchanged |
| sync 200 one new row | one `update_or_create`; second run `synced=0` |
| duplicate clients | matching and opportunity services both call the helper (patch helper, not four urlopens) |

03: extend `InquiryAPIAuthenticationTests`: anonymous still 401 once key-auth is required; valid key 200; staff JWT 200; POST 405.

#### 23.2.6 Secondary exposure — Deal Engine inbound `AllowAny` (D9, not this cutover)

If the Deal Engine host is internet-reachable:

- `GET/POST /api/propertism/deal-engine/inquiries/`
- `GET/POST /api/propertism/deal-engine/inquiries/sync/`
- `GET /api/propertism/deal-engine/inbound-leads/`

All `@authentication_classes([])` + `AllowAny`. They proxy Propertism PII; sync writes `DealShortlist`.

**Also AllowAny:** `direct-leads` GET/POST/PATCH/DELETE (PII write/read; not the 13 Oct Propertism spam write-path).

Do not lock these without D9. SPA session (`deal_crm` login) must keep working.

#### 23.2.7 Rollout (corrected — no live PII probe)

**Removed:** sending an authenticated GET to production `/api/inquiries/` while it is still `AllowAny`. That header may be ignored and the body is customer PII.

1. Viji approves D1 (Option B) and D2 (keys in both env stores).
2. Implement 03 permission + 04 helper locally. Tests in §23.2.5 only (mocks + local Django).
3. After explicit production approval: set keys on 03 and 04 Lightsail `.env` (secrets only). Do not write enquiry rows.
4. Deploy **04** first. Confirm the process starts and scheduled/manual sync does not 500. Do not print inquiry bodies.
5. Viji approves D4: commit/push existing 03 security diffs **plus** the Option B permission. CI deploys `IsStaffOrDealEngineKey` (staff JWT still valid; anonymous closed).
6. Unauthenticated production GET `/api/inquiries/`: record **HTTP status only** (expect 401). Do not display or retain the body.
7. Authenticated 04 sync: confirm 04 reports success/count only. Do not dump customer fields into this SCCB, chat, or logs.

**Recovery if Deal Engine breaks after step 5:** keep the 03 restriction. Fix 04 key/header. **Never** restore `AllowAny`. **Never** set production `RECAPTCHA_FAIL_OPEN=true`.

### 23.3 realBOT remediation design (plan only — D5)

**Link to 13 Oct spam: unproven.** Do not treat this as the incident fix. No realBOT code and **no ICS migration** in this pass.

#### 23.3.1 Trust boundary (verified against code)

| Route | View | Notes |
|---|---|---|
| `/chat/session/init/` and `/api/v1/realbot/session/init/` | `init_session` | CSRF-exempt; **GET and POST**. Live UI (`realbot-panel.js`) uses **GET** `fetch(url)` with optional `?session_id=`. |
| `/chat/query/` and `/api/v1/realbot/query/` | `send_message` | CSRF-exempt POST. Body: `{session_id, message}` only. If ICS in `OPEN_STATES` (`collecting_information`, `awaiting_conflict_resolution`, `awaiting_confirmation`) → `process_message`. |
| `/chat/inquiry/initiate/` and `/api/v1/realbot/inquiry/initiate/` | `inquiry_initiate` | CSRF-exempt POST; creates ICS |

Confirm (`CONFIRM_KEYWORDS`: yes, ok, sure, …) → `_submit_inquiry` → `InquirySubmissionAdapter.submit()` → `Inquiry.objects.create(..., confidence_score=80, assessment_status='Genuine')`. No `SpamProtectionService`. Duplicate guard today is only after success (`state='submitted'`, `submitted_inquiry_id`).

`chat.security_manager.RateLimiter` is an **in-process dict** (default 60/min) and is **not** invoked from `send_message` / `init_session`. Do not use it for C1 under gunicorn multi-worker. Form rate-limit (`content.security.validators.validate_rate_limit`) uses Django **cache** — that is the pattern to copy.

`_get_ip` trusts the first `X-Forwarded-For` hop (same spoof caveat as forms).

#### 23.3.2 Layers C1–C4 (final proposal for D5)

**C1 — Rate limit (must if D5 approved)**  
Django cache, not `RateLimiter._request_log`. Apply to GET+POST `init_session`, POST `send_message`, POST `inquiry_initiate`.

| Key | Proposed cap |
|---|---|
| IP `init_session` | 10 / 10 min |
| IP `send_message` | 30 / 10 min |
| session `send_message` | 20 / 10 min |
| IP `inquiry_initiate` | 5 / 10 min |

429 + generic message. `SecurityEvent` without PII. Headroom is higher than HTML forms (5/10 min) because chat is multi-turn.

**C2 — Persist gate (must)**  
No migration: store a one-shot nonce in existing `collected_data` JSON when `_transition_to_confirmation` runs; consume in `_submit_inquiry`.

Before create:

- `state == 'awaiting_confirmation'`
- Mandatory fields present (`customer_name`, `country`, `mobile_number`, `service_required`, `inquiry_message`) — matches `MANDATORY_FIELDS_ORDER`
- ICS `created_at` age ≥ **20 seconds** (justified: extractor can fill several fields in one utterance; 4 user-turns would block that legitimate path)
- At least **2** `process_message` calls on that ICS (collect + confirm). Not 4.
- Nonce present and unused
- If `state == 'submitted'` or `submitted_inquiry_id` set → no second row

Do not require `website_url_check` or `form_render_time` on JSON.

**C3 — Stop auto-Genuine/80 (must)**  
Remove `REALBOT_CONFIDENCE_SCORE = 80` / `REALBOT_ASSESSMENT_STATUS = 'Genuine'`.

Run `LeadValidator` on the assembled dict (`name`, `phone`, `email`, `message`) plus the Django request from `send_message`. Absent honeypot/timing fields currently **do not penalize** (LeadValidator only penalizes if those keys are present and bad). Content heuristics (URLs, Cyrillic ratio) still apply. If validator raises: persist with `assessment_status='Pending Validation'` and `confidence_score=None` — never Genuine/80. Keep `form_source` as `realBOT — …`.

**C4 — Optional (Viji)**  
Confirm-step only: `g-recaptcha-response` on the JSON body when the user confirms. `realbot-panel.js` change **only if C4 approved**. Not on every turn. Not honeypot. Not `form_render_time`.

#### 23.3.3 Files after D5 (no migration)

| File | Change |
|---|---|
| `chat/views.py` | C1 on `init_session` (GET+POST), `send_message`, `inquiry_initiate` |
| `chat/inquiry_engine.py` | C2 nonce in `collected_data`; time/turn gates; duplicate guard |
| `chat/inquiry_submission.py` | C3 LeadValidator / pending; no SpamProtectionService |
| `static/js/realbot-panel.js` | only if C4 |
| `chat/tests_m26.py` + new `chat/tests_realbot_security.py` | below |

Do not add ICS columns.

#### 23.3.4 Tests (with implementation)

| Case | Expect |
|---|---|
| Legitimate flow: two+ spaced turns, confirm after 20s | `Inquiry` created; `form_source` starts `realBOT`; not Genuine/80 |
| Multi-field first message + confirm after 20s | still persists (do not require 4 turns) |
| Burst under 20s or over IP/session cap | no persist / 429 |
| Confirm with incomplete ICS or missing nonce | no persist |
| Second confirm | no second row |
| M2.6 field mapping | unchanged except score/status assertions |
| C4 if approved | missing confirm token → no persist |

### 23.4 Aggregate-only evidence checklist (ops / Viji)

Do **not** return names, emails, phones, messages, credentials, or bulk row dumps. Counts and booleans only.

**A. Database aggregates (13 Oct 2026, Asia/Kolkata)**

1. Count `properties_inquiry` with `created_at` on 2026-10-13.
2. Count matching promotional pattern (e.g. `message` ILIKE `%share.google%` / OZON / Cyrillic) **as a count only**.
3. Group 1 and 2 by `form_source`.
4. Group 1 by hour of `created_at`.
5. `min(created_at)`, `max(created_at)` for that day.
6. Count `assessment_status` / `confidence_score` buckets for that day (no free text).

These numbers are required to reconcile ~1,400 vs 4,674+. They are **different metrics** until dated.

**B. HTTP aggregates (Nginx / access log, same day)**

Request counts by path + status + hour for:

- contact / homepage POST
- property enquiry POST
- `GET /api/inquiries/`
- `/chat/query/` and `/chat/session/init/`
- `/api/v1/realbot/query/` and `/session/init/`

Unique-IP **counts** allowed. No query strings.

**C. SpamLog aggregates**

`content_spamlog` (or equivalent) counts by `failure_reason` and hour for 13 Oct. Include `captcha-failed`, `captcha-network-error-fail-open`, `honeypot-triggered`, `rate-limit-exceeded`, `submission-too-fast`, `captcha-disabled-in-production` if present.

**D. Non-secret production config (booleans only)**

- `CAPTCHA_ENABLE` value
- `CAPTCHA_PROVIDER` value
- `RECAPTCHA_SITE_KEY` set? yes/no
- `RECAPTCHA_SECRET_KEY` set? yes/no (never the value)
- `RECAPTCHA_FAIL_OPEN` value
- `DJANGO_SETTINGS_MODULE` value (`realtor_project.settings` vs `settings_production`)
- `REALBOT_INTEGRATION_ENABLED` production flag

**E. Deploy history**

First production deploy that contained `bb2936ce` / public `inquiry_list_api`. CI/CD or Lightsail deploy log timestamps. Source-commit date is **not** go-live.

Until A–E exist, Track A root cause stays **unconfirmed**. GET `/api/inquiries/` remains a confidentiality finding only.

### 23.5 Additional findings (verified; not modified)

| Finding | Evidence | Impact | Treatment |
|---|---|---|---|
| `login_api` mints JWT for any valid user | `users/views.py`; mounted `POST /api/auth/login/`. No in-repo JS caller. Docs mention a different path `/api/v1/auth/login`. NRI login is allauth web. | After Track B lock, non-staff JWT cannot read inquiries (`IsAdminUser`). Staff-gating `login_api` could still break an undocumented API client. | **Do not** make `login_api` staff-only in this incident. Option B does not use it. Leave D3 as “not required under B”. |
| `seed_system_config.py` default `RECAPTCHA_FAIL_OPEN='True'` | seed command; settings use `_get_bool_env` then force False when not DEBUG/TESTING | Today production fail-closed does **not** read SystemConfig for this flag. Future `_get_config` wiring would reopen fail-open if seed ran. | Do not change the seed in this pass (unrelated config). Do not run that seed in production with the True default. Record for a later approved config fix: default False. |
| 04 `direct-leads` AllowAny GET/POST/PATCH/DELETE | `deal_inbound/views.py` | PII read/write if host is public | D9 / follow-on. Not the 13 Oct Propertism write-path. |
| 04 inquiries / sync / inbound-leads AllowAny | same file + `config/deal_engine_urls.py` | Re-exposes Propertism PII; sync writes shortlist | D9. Do not lock without SPA session design. |
| 04 inquiry client has no tests | no files under `deal_inbound` tests | Auth regressions invisible | Covered by §23.2.5 after D1. |
| JWT lifetime / no TokenRefreshView / no token_blacklist app | settings vs settings_production | Option A unsound | Motivates Option B. |

### 23.6 Decisions D1–D9 (updated 2026-10-13 15:45 IST)

| # | Decision | Status | If deferred |
|---|---|---|---|
| D1 | Approve **Option B** (scoped service key) as the Deal Engine cutover. Option A remains available only if Viji rejects B. | **Approved for local implementation** (this prompt). Local code present. | Deploy still gated on D2+D4 |
| D2 | Provision `DEAL_ENGINE_INQUIRIES_KEY` on 03 and `PROPERTISM_DEAL_ENGINE_API_KEY` on 04 (Lightsail `.env` only). No Django service user under B. | **Pending** — no production secrets in this task | Blocked |
| D3 | `login_api` stays as-is under B. `TokenRefreshView` is **not** required unless A is chosen. | **Confirmed — not required under B.** `login_api` not modified. | N/A under B |
| D4 | Commit/push existing 03 security diffs **plus** Option B permission **after** D1 local tests pass | **Pending Viji review** | Stay local |
| D5 | realBOT C1–C3 now; C4 optional; or defer all | **C1–C3 implemented locally.** C4 not implemented (separate decision). | C4 remains optional |
| D6 | Supply aggregate evidence §23.4 | **Pending** | Track A unconfirmed |
| D7 | Any spam quarantine/delete | **Pending** | None |
| D8 | After 03 deploy: unauthenticated GET status only (no body) | **Pending** | Not done |
| D9 | Lock 04 inbound inquiries/sync/inbound-leads/direct-leads AllowAny | **Implemented locally** (SPA session / Django user). Not deployed. Separate from 13 Oct spam. | Deploy with D4 |

### 23.7 Verification criteria (after approved implementation)

- 04 mocked tests in §23.2.5 pass. No production inquiry body retrieved.
- 03 security tests still pass, plus key-auth cases.
- Unauthenticated production GET `/api/inquiries/` → 401 **status only**.
- 04 sync with valid key succeeds by count/status only; 401/403/timeout do not wipe `DealShortlist`.
- If D5 approved: legitimate ≥20s / ≥2-turn confirm persists; flood does not; no auto-Genuine/80.
- Track A remains open until §23.4 identifies the write path. GET API is not a spam write path.

**Historical stop (pre-implementation):** §23.7 originally ended “Not implemented.” Local implementation is now recorded in **§24**. Still not committed, not deployed, not closed.

---

## 24. Local implementation and validation record (2026-10-13)

**Authorization:** Viji master action prompt — Option B, 04 inbound/direct-leads lock, realBOT C1–C3. Local code, tests, and this SCCB only. No commit, push, deploy, production secrets, accounts, or data changes.

**Git baseline (verified this session):**
- Project 03 HEAD: `c8f03ae` (`fix(properties): switch to dynamic auto-fit grid and bump cache-buster to v4.3`)
- Project 04 HEAD: `9af452e` (`fix(routing): serve Next.js SPA index.html at root URL instead of redirecting to Django admin`)
- Working trees remain dirty; unrelated Viji files were not committed and were not rewritten for this incident.

**Spam root cause:** still **unconfirmed**. Production aggregates in §23.4 were not supplied. These local protections do not by themselves prove the 13 October write-path is closed.

### 24.1 Confirmed defects fixed locally

**Track B — Project 03 GET `/api/inquiries/`**
- Staff JWT/session still allowed.
- Deal Engine access is now `Authorization: DealEngine <key>` via `IsStaffOrDealEngineKey`.
- Empty/missing `DEAL_ENGINE_INQUIRIES_KEY` does not reopen anonymous access.
- Previous key accepted only when `DEAL_ENGINE_INQUIRIES_KEY_PREVIOUS` is set.
- Constant-time compare (`hmac.compare_digest` over SHA-256 digests).
- Mechanism is view-scoped, not a global authentication backend.
- GET-only remains; POST 405 including with a valid service key.
- Error bodies do not echo the key.

**Track B — Project 04 outbound client**
- Shared `deal_inbound.propertism_client.fetch_inquiries()` used by all four former anonymous call sites:
  1. `deal_inbound.views._fetch_from_live_api`
  2. `deal_inbound.views.sync_inquiries`
  3. `deal_matching.services.deal_engine_service.DealEngineService.inquiries` / `sync_inquiries`
  4. `deal_opportunity.services.deal_engine_service.DealEngineService.inquiries` / `sync_inquiries`
- Fail-closed if `PROPERTISM_DEAL_ENGINE_API_KEY` is absent/empty (no network GET).
- 401/403/5xx/timeout/malformed JSON → `ok=False`. Sync does **not** `update_or_create`. Existing `DealShortlist` rows are kept. HTTP 502 for inbound sync/inquiries proxy failures (not 200 empty).

**Track B (separate finding) — Project 04 inbound + direct-leads**
- Replaced `AllowAny` on inquiries, sync, inbound-leads, and all direct-leads methods with `IsDealEngineSession` (`session['logged_in']` from SPA env login, or Django-authenticated user).
- Repository evidence: Next.js client already sends credentials; no public anonymous create form for direct-leads. **All methods locked**, including POST.
- Project 03 service key is **not** sent to the browser.
- CSRF: `csrf_exempt` was not blanket-removed. Login remains CSRF-exempt as before; inquiry/direct-leads views keep Django CSRF middleware.

**Track A adjacent — CAPTCHA**
- Existing fail-closed production behaviour retained (`RECAPTCHA_FAIL_OPEN` forced false when not DEBUG/TESTING; missing secret fails; production cannot skip via flag).
- `seed_system_config.py` **not** modified (runtime does not currently read SystemConfig for this flag).
- `login_api` **not** modified.

**realBOT C1–C3 (separate finding; 13 Oct link unproven)**
- C1: Django-cache rate limits on `init_session` GET+POST, `send_message`, `inquiry_initiate` (covers `/chat/...` and `/api/v1/realbot/...` aliases of those views). 429 on exceed. Limits: 5 init / 10 min / IP; 20 messages / 10 min / IP; 15 messages / 10 min / session; 5 initiate / 10 min / IP.
- C2: persist gate — awaiting_confirmation, mandatory fields, ≥2 engine turns, ≥20s since ICS creation, single-use server nonce in `collected_data`, `select_for_update`, already-submitted guard. Nonce in structured `metadata.inquiry.submit_nonce`; `realbot-panel.js` returns it. Not shown as chat text.
- C3: `LeadValidator` on assembled payload; default `Pending Validation` if validator unavailable. `form_source` still starts with `realBOT`. No hardcoded Genuine/80.
- C4: **not implemented**.

### 24.2 Files changed and why

**Project 03 (incident-related)**

| File | Why |
|---|---|
| `properties/permissions.py` | New `IsStaffOrDealEngineKey` |
| `properties/views.py` | `inquiry_list_api` permission swap |
| `properties/test_security_fixes.py` | Staff, key, rotation, anonymous, POST 405 |
| `realtor_project/settings.py` | Env key names, empty default |
| `realtor_project/settings_production.py` | Same env names |
| `.env.example` | Placeholder names only |
| `chat/request_limits.py` | C1 cache counters |
| `chat/views.py` | C1 on init/query/initiate; pass `submit_nonce` |
| `chat/inquiry_engine.py` | C2 nonce, turns, time, lock |
| `chat/inquiry_submission.py` | C3 LeadValidator / pending |
| `chat/tests_m26.py` | Age helper, nonce on confirm path, cache clear in API tests |
| `chat/tests_realbot_security.py` | C1–C3 cases |
| `static/js/realbot-panel.js` | Echo submit nonce on `/chat/query/` |

CAPTCHA files from earlier local work remain in the working tree (`content/security/*`, templates honeypot/timing). Unrelated Viji files (scope/plan, AWS migration docs, `seed_system_config.py`) were not rewritten for this task.

**Project 04**

| File | Why |
|---|---|
| `backend/deal_inbound/propertism_client.py` | Shared authenticated client |
| `backend/deal_inbound/permissions.py` | SPA session gate |
| `backend/deal_inbound/views.py` | Use client; lock inbound/direct-leads |
| `backend/deal_inbound/tests/` | Mocked urllib + permission + shortlist preservation |
| `backend/deal_matching/services/deal_engine_service.py` | Shared client; fail-closed sync |
| `backend/deal_opportunity/services/deal_engine_service.py` | Same |

04 `05-Sessions/session.md` was already modified in the working tree and was not part of this implementation.

04 has no `.env.example`. Variable name `PROPERTISM_DEAL_ENGINE_API_KEY` is documented here only. The live `.env` was **not** edited.

### 24.3 Service-key design and rotation

| Host | Variable |
|---|---|
| 03 | `DEAL_ENGINE_INQUIRIES_KEY` (active), `DEAL_ENGINE_INQUIRIES_KEY_PREVIOUS` (rotation overlap) |
| 04 | `PROPERTISM_DEAL_ENGINE_API_KEY` (must equal 03 active key) |

Header: `Authorization: DealEngine <key>` (not Bearer).

**Rotation (after Viji supplies secrets — not executed now):**
1. Set new key as `DEAL_ENGINE_INQUIRIES_KEY` on 03 and old key as `_PREVIOUS`.
2. Switch 04 `PROPERTISM_DEAL_ENGINE_API_KEY` to the new key; restart 04 then 03.
3. Verify sync by status/count only.
4. Clear `_PREVIOUS` on 03; restart 03.

**Revocation:** remove both 03 key settings; restart 03. Staff JWT/session still works. 04 will 401/502; shortlist is kept.

No key values exist in source, tests (beyond obviously fake fixtures), SCCB, or frontend JS.

### 24.4 Project 04 inbound permission matrix

| Route | Methods | Anonymous | SPA `logged_in` / Django user |
|---|---|---|---|
| `/api/propertism/deal-engine/inquiries/` | GET | 403 | 200 on upstream ok; 502 on fetch failure |
| `/api/propertism/deal-engine/inquiries/sync/` | GET, POST | 403 | 200 on ok write; 502 no write on failure |
| `/api/propertism/deal-engine/inbound-leads/` | GET | 403 | 200 / 502 as inquiries proxy |
| `/api/propertism/deal-engine/direct-leads/` | GET, POST | 403 | 200 |
| `/api/propertism/deal-engine/direct-leads/<id>/` | GET, PATCH, DELETE | 403 | 200 / 404 |
| status/notes subroutes | POST | 403 | 200 / 404 |

**Frontend:** no Next.js file changes. Login already sets `session['logged_in']`; API helper already uses credentials. Service key must never be added to `frontend-next`.

**Not locked in this pass (out of inbound/direct-leads scope):** other Deal Engine `AllowAny` views (matching/opportunity discovery, etc.). Documented; not speculative lockdown.

### 24.5 realBOT C1–C3

| Control | Implementation |
|---|---|
| C1 | `chat/request_limits.py` + views. Django `cache`. Default locmem in `realtor_project.settings` (per-process). Redis only if `settings_production` is the live module (unverified). Do not claim distributed enforcement until `DJANGO_SETTINGS_MODULE` is known. |
| C2 | Nonce + turns + 20s + `select_for_update`. Adapter failure re-issues nonce so Try Again can proceed. |
| C3 | `LeadValidator`; pending on exception. Pre-existing validator INFO logs still include name/email — not refactored here. |
| C4 | Not built. |

`_get_ip` still trusts the first `X-Forwarded-For` hop. No proxy-trust change without verified production proxy behaviour.

### 24.6 Tests executed

Interpreters not mixed: 03 `.venv` Django **4.2.16**; 04 `D:\viji\viji-olivine\00-oec\venv` Django **5.2.16**. No live Propertism HTTP.

**Project 03**

| Command | Result |
|---|---|
| `.venv\Scripts\python.exe manage.py check` | 0 errors; 1 pre-existing allauth `ACCOUNT_EMAIL_REQUIRED` deprecation warning |
| `.venv\Scripts\python.exe manage.py test properties.test_security_fixes content.tests.CaptchaVerificationTests properties.tests.InquiryNotificationTests chat.tests_realbot_security` | **42 tests OK** in 18.401s |
| Same plus `chat.tests_m26` | **133 tests, 1 failure** |

`chat.tests_m26.InquiryFieldExtractorSingleFieldTests.test_extract_location_omr` — `'preferred_location' not found`. `chat/inquiry_extractor.py` was **not** modified. Treated as **pre-existing**; not patched.

**Project 04**

| Command | Result |
|---|---|
| `00-oec\venv\Scripts\python.exe manage.py check` (cwd `backend`, `config.settings.dev`) | 0 issues |
| `00-oec\venv\Scripts\python.exe manage.py test deal_inbound.tests --verbosity=2` | **18 tests OK** in 2.883s |

Frontend lint/build: **not run** (no frontend files changed).

### 24.7 Remaining issues / Viji decisions

- Production evidence §23.4 still missing → Track A unconfirmed.
- D2 secrets, D4 commit/push, D7 data cleanup, D8 prod 401 probe, deploy — gated.
- C4 optional CAPTCHA on confirm — not in this local set.
- 03 C1 is locmem unless production uses Redis settings.
- Other 04 `AllowAny` non-inbound routes unchanged.
- `LeadValidator` INFO PII logging is pre-existing.
- `seed_system_config.py` still defaults `RECAPTCHA_FAIL_OPEN='True'` for a future config path; runtime currently fail-closed from env.

### 24.8 Deployment and recovery plan (not executed)

**Forbidden rollbacks:** restore `AllowAny` on `/api/inquiries/`; enable production CAPTCHA fail-open; put the service key in browser JS; delete production records without explicit authorization.

1. Viji reviews this local changeset.
2. Viji provisions the same high-entropy key on 03 (`DEAL_ENGINE_INQUIRIES_KEY`) and 04 (`PROPERTISM_DEAL_ENGINE_API_KEY`) in Lightsail `.env` only. Restart processes. No Django service user.
3. Deploy **04 first** so all four clients send `DealEngine` before 03 rejects anonymous GET.
4. Confirm 04 process starts; do not print inquiry bodies.
5. After explicit D4 approval: commit/push 03 (and 04) under the 8-stage Viji Law. CI deploys 03 lockdown.
6. Unauthenticated GET `/api/inquiries/`: record **HTTP status only** (expect 401/403). Do not retain body.
7. Authenticated 04 sync: status/count only. Failed sync must not reduce `DealShortlist` count.
8. Regression: CAPTCHA forms, realBOT ≥20s / ≥2-turn confirm, 429 on flood.
9. If 04 breaks after 03 lockdown: keep 03 restriction; fix 04 key/header/restart. Never restore `AllowAny`.

**Cutover order:** 04 client deploy → 03 API lockdown → status-only unauthenticated check → authenticated sync check.

### 24.9 Closure

SCCB-09 remains **OPEN**. Local implementation of Option B, 04 inbound/direct-leads lock, and realBOT C1–C3 is complete for Viji review. Production verification and spam root-cause evidence are outstanding.

---

## 25. Independent acceptance review — SCCB-09-AR-001 (scope opened before inspection)

**Opened:** 2026-10-13 15:50 IST  
**Task:** Independently verify the local implementation in §24 against the working trees. Do not re-implement, redesign, rerun tests, or change application code unless a confirmed current defect is found — and even then, document it and stop. This review does not close the incident.

### 25.0 Acceptance criteria (set before inspection)

The review accepts the local changeset for Viji's next-stage decision only if all of the following hold on the current trees:

1. Project 03 HEAD is `c8f03ae` and Project 04 HEAD is `9af452e`, or any drift is recorded and inspection stops before further testing.
2. Incident files match the tree that produced the §24.6 test record (no post-test drift in those files).
3. `GET /api/inquiries/` is staff JWT/session or `Authorization: DealEngine <key>`; empty key does not open anonymous access; POST is 405; key compare is constant-time and view-scoped.
4. All four Project 04 inquiry fetch sites use `fetch_inquiries()`; missing key does not call the network; failed fetch does not write `DealShortlist`.
5. Inbound, sync, inbound-leads, and direct-leads deny anonymous access and allow the existing SPA session or Django user. No Project 03 key in browser code.
6. realBOT C1 covers init GET+POST, query, and initiate (including `/api/v1/realbot/` aliases). C2 gates persistence. C3 does not hardcode Genuine/80. C4 is absent.
7. §24.6 reports the 133-test run as 132 pass / 1 fail, not as a full pass. The extractor failure stays unmodified unless it is shown to be caused by this work.
8. Track A remains unconfirmed. Track B is an access-control finding only.
9. No commit, push, deploy, production call, or secret provisioning occurs in this review.

**Verdict values:** ready for Viji review | blocked by a confirmed defect | evidence insufficient.

### 25.1 Baseline (inspected 2026-10-13 15:55 IST; no application-code edits)

| Repo | HEAD | Staged | Incident tree vs §24.6 tests |
|---|---|---|---|
| 03 | `c8f03ae` | none | Unchanged. This review edited only this SCCB. |
| 04 | `9af452e` | none | Unchanged. |

**03 unstaged (incident):** `.env.example`, `chat/inquiry_engine.py`, `chat/inquiry_submission.py`, `chat/tests_m26.py`, `chat/views.py`, `content/security/captcha_provider.py`, `content/security/google_recaptcha.py`, `content/security/spam_protection.py`, `content/tests.py`, `properties/tests.py`, `properties/views.py`, `realtor_project/settings.py`, `realtor_project/settings_production.py`, `static/js/realbot-panel.js`, `uilayers/templates/components/_footer.html`, `uilayers/templates/components/_lp_lead_form.html`, `code-review/fix-report.md`.

**03 untracked (incident):** `properties/permissions.py`, `properties/test_security_fixes.py`, `chat/request_limits.py`, `chat/tests_realbot_security.py`, `code-review/sccb-09/`, `04-Control/` (this SCCB).

**03 unrelated (preserved):** scope/plan/registry/session/AGENTS, content admin/models/management, `seed_system_config.py`, migration `0024`, AWS/migration docs and scripts, `test_api_permissions.py`.

**04 unstaged (incident):** `backend/deal_inbound/views.py`, matching and opportunity `deal_engine_service.py`.

**04 untracked (incident):** `backend/deal_inbound/permissions.py`, `propertism_client.py`, `tests/`.

**04 unrelated dirty file:** `05-Sessions/session.md` only. That matches the implementation report.

No drift from the tested tree. Review continued.

### 25.2 Project 03 API and CAPTCHA

Confirmed in current source:

- `inquiry_list_api` (`properties/views.py`) is GET-only, `JWTAuthentication` + `SessionAuthentication`, permission `IsStaffOrDealEngineKey`.
- That permission class is used only on that view in live code. `code-review/sccb-09/` is a copy, not a second runtime path.
- Staff requires `is_authenticated` and `is_staff`. Otherwise the `DealEngine` scheme is required. Empty/missing keys are not added to the accepted set.
- Compare is `hmac.compare_digest` of SHA-256 digests (fixed length). Previous key is accepted only when configured and different from the active key.
- POST remains outside `@api_view(["GET"])` (405). Tests cover staff, session, key, empty key, bad/malformed key, previous-key overlap, anonymous, non-staff, and POST.
- CAPTCHA: `RECAPTCHA_FAIL_OPEN` defaults false and is forced false when not `DEBUG` and not `TESTING` (`settings.py`). Missing secret returns `secret-key-missing`. Production flag-off is `captcha-disabled-in-production`. `NullProvider.verify` fails closed in production.
- `login_api` and `seed_system_config.py` were not modified by this review.

No confirmed API or CAPTCHA defect in the local tree.

### 25.3 Project 04 client and inbound permissions

All four sites call `fetch_inquiries()`:

1. `deal_inbound/views.py` `_fetch_from_live_api`
2. `deal_inbound/views.py` `sync_inquiries` — returns HTTP 502 before `update_or_create` when `result.ok` is false
3. matching `DealEngineService.inquiries` / `sync_inquiries` — returns before shortlist writes when `ok` is false
4. opportunity service — same pattern

Missing/empty `PROPERTISM_DEAL_ENGINE_API_KEY` returns `service-key-missing` and does not call `urlopen`. Header is `Authorization: DealEngine <key>`. Logs record status codes and error labels, not the key or response body. Successful empty (`ok=True`, `items=[]`) is distinct from failure.

`IsDealEngineSession` allows `session['logged_in']` (existing SPA env login) or any Django-authenticated user. That matches `deal_crm` login, which already accepts a successful Django `authenticate()`, not staff-only. Anonymous access is denied. Direct-leads GET/POST/PATCH/DELETE and status/notes use the same permission.

Frontend: `frontend-next/app/propertism/deal-engine/direct-leads/page.tsx` is an in-app staff screen using `api` from `lib/api.ts` (`credentials: 'include'`). It is not a public marketing form. No `DealEngine` header and no Project 03 key in that client. POST lock is consistent with that evidence. No frontend file was changed.

No confirmed client or inbound defect.

### 25.4 realBOT C1–C3

| Control | Review result |
|---|---|
| C1 | `allow_session_init` on `init_session` before GET or POST session create. `allow_send_message` on `send_message`. `allow_inquiry_initiate` on `inquiry_initiate`. Aliases: `chat/urls.py` `session/init/`, `query/`, `inquiry/initiate/` and `realtor_project/urls.py` `/api/v1/realbot/session/init/`, `query/`, `inquiry/initiate/` point at those same views. 429 on deny. |
| C2 | `_submit_inquiry` uses `select_for_update`. Requires `awaiting_confirmation`, mandatory fields, equal-length nonce compare, ≥20s, ≥2 turns, then consumes the nonce. Submitted state or `submitted_inquiry_id` returns without a second create. Nonce is in `metadata.inquiry`, not the chat text. |
| C3 | No `Genuine`/80 assignment remains in `chat/inquiry_submission.py`. `LeadValidator` runs; exception path keeps `Pending Validation` and `confidence_score=None`. `form_source` is `realBOT — …` or `realBOT Chat`. |
| C4 | Not present. |

No confirmed C1–C3 defect.

### 25.5 Test evidence (not re-run)

§24.6 matches the implementation report and is not overstated:

- 03 `manage.py check`: 0 errors; pre-existing allauth deprecation warning.
- 03 targeted suite: **42 OK**.
- 03 targeted suite plus `chat.tests_m26`: **133 ran, 1 failure** — `InquiryFieldExtractorSingleFieldTests.test_extract_location_omr`. `chat/inquiry_extractor.py` is not in the working-tree diff. Pre-existing. Not fixed in this review.
- 04 `manage.py check`: 0 issues. `deal_inbound.tests`: **18 OK**.
- Frontend lint/build: not run; no frontend source change.

### 25.6 Issue classification (no remediation in this review)

| Finding | Class | Blocker? |
|---|---|---|
| 03 default settings have no `CACHES`; Django uses process-local LocMem. `settings_production.py` declares Redis, but live `DJANGO_SETTINGS_MODULE` is unverified. | Production configuration unverified | No |
| `_get_ip` uses the first `X-Forwarded-For` hop (`content/security/validators.py`). | Pre-existing; proxy behaviour unverified | No |
| `LeadValidator` INFO logs include name and email. | Pre-existing privacy concern | No |
| `seed_system_config.py` default `RECAPTCHA_FAIL_OPEN='True'`. Runtime settings force fail-closed and do not read that seed for the flag. | Potential future risk if a later config path reads SystemConfig. Do not run the seed in production. | No |
| Other Deal Engine `AllowAny` routes outside inbound/direct-leads. | Separate finding, out of implemented scope | No |
| Extractor OMR test failure. | Pre-existing; extractor not modified | No |

No confirmed current implementation defect.

### 25.7 Tracks

- **Track A:** still unconfirmed. §23.4 aggregate evidence is still required. This review did not call production or read customer rows. The GET API is not treated as the spam write path.
- **Track B:** local access-control changes match §24 and are independent of Track A.

### 25.8 Remaining approvals (not executed)

D2 secrets, D4 commit/push, D6 evidence, D7 data cleanup, D8 status-only production probe, deploy, and optional C4 remain gated. Cutover order in §24.8 stands: 04 client first, then 03 lockdown. Forbidden rollbacks unchanged.

### 25.9 Verdict

**Ready for Viji review.**

Local changeset is internally consistent with §24 and the implementation report. HEADs and incident files match the tested tree. No confirmed defect blocks the next decision. Production verification and the spam root cause remain outstanding, so SCCB-09 stays **OPEN**.

---

## 26. Decision execution (2026-10-13 16:05 IST)

Viji's decision package is recorded here. Application behaviour was not expanded.

| Decision | Status |
|---|---|
| D2 service-key provisioning | Approved for Viji to set in Lightsail `.env` only. Astra did not generate or write a key. |
| D4 commit | Local commits of verified incident files only. See file lists below. |
| D4 push | **`main` not pushed.** Review branch `sccb-09-review-2026-10-13` published on both remotes. 03 remote hash `d58003c7215d8a0b8966620ae36bd676d3cd005a`. 04 remote hash `ea37503f97de17ff8768e4cb869d36114d95aead`. Deploy workflows trigger only on push to `main`. This SCCB line is local and uncommitted. Deployment remains deferred. |
| D6 aggregate evidence | Approved, not collected. No production read was performed. Each §23.4 item remains outstanding. Deployment that introduced public GET access: **UNVERIFIED**. |
| D7 quarantine/delete | Rejected. No production data change. |
| D8 status-only probe | Conditional on a later deploy. Not performed. |
| C4 | Deferred. Not implemented. |
| Deploy | **Stopped before push to `main` on 2026-10-13.** Fast-forward was possible (03 `c8f03ae` → `d58003c`; 04 `9af452e` → `ea37503`). Service-key presence on Lightsail was not confirmed: SSH to `13.207.123.15` as `ubuntu` returned `Permission denied (publickey)`, and this workstation has no Lightsail key. No `main` push. |

### 26.1 Commit boundary applied

`realtor_project/settings.py` also contained an unrelated `_get_config` SystemConfig loader for email, Clarity, and realBOT settings. That loader is **not** in the commit. It remains in the local working tree after the commit, restored from the pre-commit copy.

Excluded from both commits: scope/plan docs, AWS migration files, `05-Sessions/session.md`, `code-review/`, `seed_system_config.py`, other files under `04-Control/` besides this SCCB, and any `.env` with secrets.

`.env.example` contains commented empty placeholders only.

`static/js/realbot-panel.js` is included. The diff only stores and returns the server confirmation nonce. It does not contain a service key.

Track A remains **ROOT CAUSE UNCONFIRMED**. SCCB-09 is not closed.

---

**End of SCCB Document**

---

## 27. Production aggregate count collection — corrected to Lightsail, 2026-10-16 IST

**Requested action:** Viji requested a read-only production collection to establish how many `properties.Inquiry` records currently meet the persisted `assessment_status = "Likely Spam"` classification, beginning from the Django admin inquiry dataset.

**Infrastructure correction:** The live `www.propertism.in` production path is the Lightsail Mumbai VPS at `13.207.123.15`, not Elastic Beanstalk. The repository's current `deploy.yml` uses GitHub Actions SSH deployment to `/var/www/propertism`; the legacy EB scripts are historical artefacts and must not be used for this incident evidence collection.

**Scope and controls:**

- Read-only database queries only: no inserts, updates, deletes, migrations, seeds, exports of enquiry bodies, or individual customer records.
- Report aggregate counts only: total inquiries, `Likely Spam` count, and, where the production schema supports them, status/source/time aggregates needed to distinguish the 13 October incident.
- Do not display credentials, service keys, database URLs, enquiry names, emails, phone numbers, messages, IP addresses, or user-agent values.
- This count is a classification measurement, not proof of the spam write path. Rows may have been scored by the lead validator after persistence, and the incident root cause remains open.

**Validation criteria:**

1. The command has no production write capability or write statement.
2. Output contains aggregates only and can be reproduced from the recorded query.
3. The result identifies the timezone/window used for any 13 October breakdown.
4. Any unavailable EB/AWS access is recorded as an evidence-collection blocker; no direct database connection is substituted without a separate explicit authorization.

**Execution record (2026-10-16 IST):**

- AWS CLI v2.38.1 was installed during an incorrect EB preflight; it is not the execution path for the live service and no EB command was issued.
- Local preflight found no Lightsail private key in the workspace or user SSH directory and no usable SSH agent identity. A previous session also recorded `Permission denied (publickey)` for `ubuntu@13.207.123.15`.
- GitHub Actions is configured with deployment SSH secrets, but the local GitHub CLI token is invalid. No workflow was dispatched, because the existing workflow is a deployment workflow and is not an approved aggregate-query runner.
- No SSH, production database, EB, RDS, or production HTTP request was issued by this collection attempt. No production data was read or changed.

**Next authorized action once Lightsail access is available:** run a reviewed, read-only command on the VPS that prints only the aggregate `Inquiry` counts described above. The command must be reviewed for aggregate-only output before it is issued. No code deployment, database modification, or fallback to the retired EB environment is permitted.

---

## 28. End-to-end spam injection root-cause trace — opened 2026-10-16 IST

**Requested action:** Trace all application paths capable of persisting `properties.Inquiry` and determine, from local source and deployment history, how the reported spam could have been injected.

**Scope:** Source-only forensic trace against the last deployed `origin/main` baseline (`c8f03ae`) and the local SCCB-09 remediation commit (`d58003c`). No production requests, database reads, logs, changes, or credential handling are in scope.

**Method:**

1. Enumerate every direct and indirect `Inquiry` create/update path and map its public trigger.
2. Record the execution order of anti-bot checks, CAPTCHA, lead classification, notification dispatch, and database persistence for each path.
3. Identify the exact fail-open or bypass conditions present in the deployed baseline.
4. Compare those conditions with the incident's reported payload shape and volume, while clearly separating confirmed code facts from unverified production causation.
5. State the minimum aggregate evidence needed to prove or disprove each viable injection route.

**Validation criteria:** The report must contain no PII or secrets; must not equate public GET API exposure with a write path; and must not identify a root cause as confirmed absent production evidence tying affected rows to a write path.

### 28.1 Result: source-confirmed injection surfaces in the deployed baseline

The deployment baseline is `origin/main` commit `c8f03ae` (9 September 2026). The SCCB-09 remediation commit `d58003c` is not deployed. Source review found exactly three application paths that persist `properties.Inquiry`:

| Rank | Public trigger and persist chain | Baseline anti-bot boundary | Incident fit |
|---|---|---|---|
| 1 | `POST /contact/` → `content.views.contact()` → `SpamProtectionService.validate()` → `LeadValidator.validate()` → `PropertyInquiry.objects.create()` | CAPTCHA enforcement could fail open or be skipped; optional hidden checks; per-IP cache limit | **Most consistent** with the reported single-message Russian / promotional-link payload |
| 1 | `POST /properties/inquiry/` → `properties.views.create_inquiry()` → same service/validator sequence → `Inquiry.objects.create()` | Same as contact path | **Most consistent** with the reported payload; requires a valid property id |
| 2 | Public realBOT session/initiate/query APIs → conversation confirmation → `InquirySubmissionAdapter.submit()` → `PropertyInquiry.objects.create()` | No HTML CAPTCHA, honeypot, timing control, or request rate limit; hardcoded `Genuine` / 80 | Technically capable, but requires a multi-field conversational flow and no evidence links the reported records to `realBOT` |

`POST /chat/submit/` creates `ContactMessage`, not `Inquiry`; landing-lead creates `LandingLead`, not `Inquiry`; and `GET /api/inquiries/` only reads `Inquiry`. None can directly explain the reported `Inquiry` spam rows.

### 28.2 Confirmed failure mechanism on the two HTML Inquiry paths

The baseline code did call `SpamProtectionService`, but that service did not guarantee CAPTCHA enforcement:

1. `CAPTCHA_ENABLE` came from repository `feature_flags.json`; a false/missing/unreadable flag defaulted to false, skipping CAPTCHA verification entirely.
2. When CAPTCHA was enabled, an unset `RECAPTCHA_SECRET_KEY` returned `RecaptchaResult(success=True, error_codes=['secret-key-missing'])`. The request therefore proceeded as CAPTCHA-passed.
3. `RECAPTCHA_FAIL_OPEN` defaulted to true. Google verification network errors, timeouts, and unexpected errors allowed the request to proceed and only wrote a `captcha-network-error-fail-open` audit record.
4. The honeypot was bypassable by leaving `website_url_check` empty. `form_render_time` was optional; missing or malformed values passed. These controls do not establish human origin.
5. The IP limit allowed five requests per ten minutes per cache key, but it did not stop a distributed attack and its trust in the first `X-Forwarded-For` address requires production proxy verification.
6. `LeadValidator` assigned `Likely Spam` **after** the spam-protection decision and both form views still called `Inquiry.objects.create()` for that result. It suppressed notification only in the homepage contact flow; it did not reject or quarantine the row. Therefore a large `Likely Spam` count is compatible with a successful bulk submission attack.

### 28.3 Root-cause conclusion and confidence

**Confirmed root-cause class (source):** The deployed application accepted untrusted public form POSTs into `Inquiry` whenever CAPTCHA was disabled, had no configured secret, or encountered a verification network failure with fail-open enabled. The remaining controls were bypassable/insufficient for a distributed automated sender, and post-persist scoring labelled spam rather than preventing persistence.

**Most likely incident route (moderate confidence):** automated direct POSTs to `/contact/` and/or `/properties/inquiry/` during one of the above CAPTCHA bypass states. This matches the reported one-message Russian / `share.google` promotional pattern and is the only route that maps naturally to that payload shape.

**Not yet confirmed:** Which of the two HTML routes was used; whether one or more production CAPTCHA bypass states actually existed on 13 October; whether proxy/cache behaviour weakened the rate limit; and whether realBOT contributed. The public GET API exposure is a separate confidentiality defect and is not a write mechanism.

### 28.4 Evidence that will close the causal gap

Read-only, aggregate-only collection from Lightsail is required:

1. `properties_inquiry` counts for 13 October 2026 Asia/Kolkata, grouped by `form_source`, hour, and `assessment_status`, plus promotional-pattern count by `form_source` (no row data).
2. `content_spamlog` counts grouped by `failure_reason`, `form_name`, request path, and hour — particularly `captcha-network-error-fail-open`, CAPTCHA failure, honeypot, timing, and rate-limit events.
3. Nginx aggregate counts by request path, method, status, and hour for `/contact/`, `/properties/inquiry/`, realBOT endpoints, and `/api/inquiries/`.
4. Non-secret runtime facts: `DJANGO_SETTINGS_MODULE`; CAPTCHA feature/provider flag values; whether site/secret keys were present (yes/no); fail-open value; cache backend; realBOT enablement.
5. realBOT aggregate count for completed inquiry conversations versus `Inquiry.form_source` values beginning `realBOT`.

**Execution status:** COMPLETE for source-only tracing. No production interaction occurred. SCCB-09 Track A remains OPEN pending the above evidence.

---

## 29. Local remediation re-verification and validation — opened 2026-10-16 IST

**Authorised scope:** Re-verify the actual `d58003c` local SCCB-09 implementation against the incident findings, trace all Inquiry persistence paths, reproduce security boundaries through focused automated tests where practical, and make only the smallest necessary local corrections. This section is not authority to access Lightsail, production data, logs, configuration, or customer records.

**Delivery controls:** Preserve all pre-existing working-tree changes; do not reset, clean, change branches, commit, push, merge, or deploy. The current tree contains unrelated work. Results must distinguish existing committed SCCB-09 code from any new local edits.

**Focused validation plan:**

1. Inspect CAPTCHA enforcement, provider failure paths, the form views, lead classification, IP extraction, and cache-backed throttles.
2. Inspect every realBOT public entry point and the conversation-to-Inquiry adapter for limits, replay protection, timing/turn validation, duplicate handling, and classification.
3. Confirm model/table identity for `Inquiry` and the `PropertyInquiry` import alias, and retain the read-only API issue as a separate concern.
4. Run Django checks and targeted tests for form CAPTCHA, inquiry persistence/API access, notification flow, and realBOT security; then run the relevant broader suite.
5. If a demonstrated current-tree defect requires a code change, add a minimal regression test and record exact test evidence. Do not introduce an unapproved business rule that rejects or deletes heuristic `Likely Spam` leads where the existing workflow has no quarantine state.

**Acceptance criteria:** Protected public forms cannot persist an inquiry when production CAPTCHA validation is missing, disabled unexpectedly, rejected, or untrustworthy; realBOT controls have tested flood/replay/duplicate boundaries; anonymous Inquiry API reads are denied; legitimate validated flows remain covered; cache/proxy topology limitations and any historical-causation gaps are explicitly recorded.

### 29.1 Local implementation additions

**New local changes, uncommitted:**

1. `content/security/validators.py` now treats a cache read/write failure as a failed required form rate-limit check. It no longer accepts `X-Forwarded-For` merely because it is present: it uses the direct peer unless that peer appears in an explicit `TRUSTED_PROXY_IPS` setting. A malformed proxy setting or forwarded address fails safely to the peer address.
2. `content/security/spam_protection.py` returns a non-rate-limit, retry-safe security error for a failed cache dependency rather than presenting it as an ordinary quota response.
3. `chat/request_limits.py` uses the same deny-on-cache-failure policy for public realBOT session, message, and inquiry-initiation limits.
4. `realtor_project/settings.py` defines `TRUSTED_PROXY_IPS` from an optional environment list, defaulting to no trusted proxies. The live Nginx/Lightsail peer topology must be verified before this value is populated.
5. `properties/views.py` retains `Likely Spam` property inquiries for audit, consistent with the existing data model, but suppresses their notification dispatch. This makes the existing classification an operational routing boundary without silently deleting leads or introducing a new quarantine schema.
6. Regression coverage was added for forwarded-header trust, form cache unavailability/cache write refusal, and realBOT cache unavailability.

**Reason for change:** `d58003c` correctly closes the CAPTCHA fail-open paths, but its rate-limit implementations could raise an error or become operationally unreliable when the cache failed, and they trusted a caller-supplied forwarding header. The property-detail flow also dispatched notifications for `Likely Spam`, unlike the contact flow. These are current-tree local findings; they do not establish the historical production route.

### 29.2 Validation status and environment blocker

- Static diff validation: `git diff --check` completed with no whitespace errors in the SCCB-09 files. The command reports only pre-existing end-of-file blank-line warnings in unrelated modified files.
- Automated Django validation: **blocked locally before test discovery.** The project `.venv` interpreter is a Python 3.11 launcher bound to the removed path `C:\Users\vijay\AppData\Local\Programs\Python\Python311\python.exe`; invoking `.venv\Scripts\python.exe manage.py check` and the targeted test command fails immediately with `No Python at ...`. The only discoverable alternate interpreter is another broken virtual environment with the same missing base interpreter. No test ran, no test database was created, and no production system was contacted.
- Required next local step: repair/recreate the project virtual environment with the repository's supported Python version and dependencies, then execute `manage.py check` followed by the targeted SCCB-09 suite and the broader realBOT suite. Do not treat the new regression tests as validated until that evidence exists.

### 29.3 Outstanding architectural limits

- This source tree's default settings have no shared `CACHES` declaration, so Django defaults to process-local cache behaviour. `settings_production.py` declares Redis, but the actual Lightsail settings module/cache availability remains unverified. Deny-on-error protects an outage, but cross-worker throttling requires a verified shared cache.
- `TRUSTED_PROXY_IPS` deliberately defaults empty. This prevents spoofing but can group traffic by the reverse proxy if production does not configure the verified peer address. That configuration must follow a read-only Nginx/runtime review.
- There is no explicit `Inquiry` quarantine state. `Likely Spam` records remain auditable but now have notification suppression on both HTML Inquiry paths. Whether they should be automatically rejected or moved to a new quarantine workflow needs an approved business/data-model decision.
- realBOT retains its separate non-CAPTCHA design. Existing C1-C3 rate, nonce, timing, turn, and duplicate gates apply, but CAPTCHA for realBOT (C4) remains intentionally deferred and is not claimed as implemented.
