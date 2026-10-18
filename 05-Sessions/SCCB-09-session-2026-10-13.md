<!-- AUDIT METADATA -->
<!-- Date: 2026-10-13 -->
<!-- Time: 16:22 IST -->
<!-- Product Owner: Viji M -->
<!-- Supervisor: Astra -->
<!-- Module: 03-propertism and 04-propertism-deal-engine -->
<!-- Status: LOCAL FIXES COMMITTED — REVIEW BRANCHES PUBLISHED — PRODUCTION CUTOVER STOPPED -->
<!-- Git: 03 d58003c local main; 04 ea37503 local main -->
<!-- Incident: SCCB-09 OPEN — Track A root cause UNCONFIRMED -->

# Session report — SCCB-09 end to end
## 13 October 2026

**Product owner:** Viji M  
**Executor:** Astra  
**Canonical incident report:** `04-Control/01-sccb/SCCB-09-PROPERTISM-SPAM-INCIDENT-END-TO-END-001.md`  
**This file** records the session. It does not replace the SCCB and it does not close the incident.

---

## 1. What this session was

A production spam incident was reported for 13 October 2026, together with a public `GET /api/inquiries/` that returned enquiry personal data. The work stayed in two tracks:

- **Track A — spam writes.** How the enquiries were created. Root cause is still unconfirmed. Production aggregate evidence was not collected.
- **Track B — API confidentiality.** Who can read enquiry data. Fixed in local code. Not deployed.

No production records were deleted or changed. No service-key value was generated, read, or written into source, chat, or this report.

---

## 2. Repositories

| Project | Path | Remote | Remote `main` at session end | Local incident commit |
|---|---|---|---|---|
| 03 Propertism | `D:\viji\viji-olivine\03-propertism` | `https://github.com/Propertism/propertism.git` | `c8f03ae` | `d58003c7215d8a0b8966620ae36bd676d3cd005a` |
| 04 Deal Engine | `D:\viji\viji-olivine\04-propertism-deal-engine` | `https://github.com/Propertism/content-admin.git` | `9af452e` | `ea37503f97de17ff8768e4cb869d36114d95aead` |

Both local `main` branches contain the incident commit and are one commit ahead of remote `main`. Remote `main` was not pushed.

Review branches, both verified on the remote at those exact hashes:

- `sccb-09-review-2026-10-13` on `Propertism/propertism`
- `sccb-09-review-2026-10-13` on `Propertism/content-admin`

---

## 3. What was found

**Track B, confirmed in code.** `GET /api/inquiries/` was GET-only and, before this work, allowed anonymous access. The serializer includes name, email, phone, and message. That endpoint is not a write path for the spam.

**Track A, not confirmed.** The most consistent local write path is the HTML enquiry forms. CAPTCHA could previously fail open, accept a missing secret, or be skipped by a disabled flag. Those controls were hardened locally. Dated production counts, SpamLog aggregates, nginx path counts, the live settings module, the realBOT production flag, and the deploy that introduced public API access were not available. Until those exist, the spam write path stays unconfirmed.

**Deal Engine.** Four server-side callers fetched `https://www.propertism.in/api/inquiries/` with no authorization. A failed fetch could look like an empty feed. Project 04 also exposed inquiries, sync, inbound-leads, and direct-leads without authentication. Direct-leads is an in-app screen, not a public form. This exposure is separate from the 13 October spam writes.

**realBOT.** The chat path can create an `Inquiry` without the HTML spam-protection service. Its link to the 13 October incident is unproven. It was hardened locally as a separate finding. Confirmation-step CAPTCHA (C4) was not built.

---

## 4. What was implemented locally

**Project 03**

- `GET /api/inquiries/` accepts a staff JWT or session, or `Authorization: DealEngine <key>`.
- An empty `DEAL_ENGINE_INQUIRIES_KEY` does not reopen anonymous access. A previous key works only when `DEAL_ENGINE_INQUIRIES_KEY_PREVIOUS` is set. Comparison is constant-time. POST stays 405.
- Production CAPTCHA fails closed: missing secret fails, a disabled flag cannot skip verification, and a null provider cannot pass in production.
- realBOT: rate limits on session init (GET and POST), query, and inquiry initiate, including the `/api/v1/realbot/` aliases; a one-use server nonce; at least two engine turns and 20 seconds before persistence; no second inquiry from a repeated confirmation; assessment is no longer hardcoded to Genuine / 80. The panel script only carries the nonce.

**Project 04**

- One client, `backend/deal_inbound/propertism_client.py`, is used by the inbound fetch, the inbound sync, and both Deal Engine `inquiries()` methods.
- A missing `PROPERTISM_DEAL_ENGINE_API_KEY` does not call the network. HTTP errors, timeouts, and malformed payloads are failures. Sync does not write `DealShortlist` on failure.
- Inquiries, sync, inbound-leads, and all direct-leads methods require the existing SPA session or a Django user.

`login_api` and `seed_system_config.py` were not modified. The seed command still defaults `RECAPTCHA_FAIL_OPEN` to true for a future config path. Runtime settings force fail-closed and do not read that seed for the flag.

---

## 5. Tests

Interpreters were not mixed. Project 03 used `.venv` (Django 4.2.16). Project 04 used `D:\viji\viji-olivine\00-oec\venv` (Django 5.2.16). No live Propertism call was made during tests.

| Run | Result |
|---|---|
| 03 `manage.py check` | 0 errors. Pre-existing allauth deprecation warning. |
| 03 security, CAPTCHA, inquiry notification, realBOT security tests | 42 passed |
| 03 those tests plus `chat.tests_m26` | 133 tests, 1 failure: `test_extract_location_omr`. The extractor file was not part of this change. |
| 04 `manage.py check` | 0 issues |
| 04 `deal_inbound.tests` | 18 passed |

Frontend lint and build were not run. No frontend source file was changed.

---

## 6. Decisions Viji made

| Item | Decision | What happened |
|---|---|---|
| Option B service key | Approved for local implementation | Implemented |
| D2 production key provisioning | Approved for Viji only | Not done by Astra. Values were never handled here. |
| D4 commit | Approved | Both commits created locally |
| D4 push to `main` | Later approved, then cutover ordered | Not done. See section 7. |
| Review-branch publication | Approved | Both review branches pushed |
| D6 aggregate evidence | Approved | Not collected |
| D7 delete or quarantine production rows | Rejected | No production data change |
| D8 unauthenticated GET, status only | After a successful deploy | Not performed |
| C4 confirm-step CAPTCHA | Deferred | Not built |
| Lightsail deploy | Ordered in the cutover prompt, gated on key presence | Stopped before push |

---

## 7. Why production was not updated

Viji authorized a cutover: push Project 04 to `main`, let GitHub Actions deploy, then push Project 03, then record only the HTTP status of an unauthenticated `GET /api/inquiries/`.

Both `.github/workflows/deploy.yml` files deploy to Lightsail on every push to `main`. A push of these commits would deploy.

Before that push, both server environment variables had to be confirmed present and non-empty:

- Project 03: `DEAL_ENGINE_INQUIRIES_KEY`
- Project 04: `PROPERTISM_DEAL_ENGINE_API_KEY`

SSH to `ubuntu@13.207.123.15` returned `Permission denied (publickey)`. This workstation has no Lightsail key. The variable names could not be checked. The push to `main` was not made. No workflow ran. No production probe was sent.

---

## 8. What is still open

1. Confirm both production variable names are set, without displaying the values.
2. Push `ea37503` to Project 04 `main` and wait for that deploy.
3. Push `d58003c` to Project 03 `main` and wait for that deploy.
4. Unauthenticated `GET https://www.propertism.in/api/inquiries/` — HTTP status only, no response body.
5. Deal Engine sync check by status and counts only. A failed fetch must not shrink `DealShortlist`.
6. Aggregate evidence for 13 October 2026 (Asia/Kolkata): enquiry counts, promotional-pattern counts, `form_source` and hour buckets, SpamLog counts, nginx counts by path/status/hour, CAPTCHA flags and secret-presence yes/no, `DJANGO_SETTINGS_MODULE`, `REALBOT_INTEGRATION_ENABLED`, and the deploy that introduced public GET access. No customer data.
7. Track A stays open until that evidence is reconciled with the write paths. Closing public GET access does not prove that endpoint created the spam.

Forbidden later: restore anonymous access on `/api/inquiries/`, enable production CAPTCHA fail-open, put the service key in the browser, or delete production records without a new authorization.

---

## 9. Working tree left in place

Unrelated local edits were not committed and were not discarded. They include scope and plan documents, AWS migration files, `05-Sessions/session.md`, the unstaged SystemConfig loader on `realtor_project/settings.py`, and Project 04 `05-Sessions/session.md`.

The one-line Section 26 updates in the canonical SCCB (review-branch hashes, then the cutover stop) are local and uncommitted. They are not on the published review branch.
