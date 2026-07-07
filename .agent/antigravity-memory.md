<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-04-28 20:00:00
Last Updated By: Astra
Last Updated On: 2026-07-07 10:15:00
Searchtag:ANTIGRAVITYMEMORY
-->

# ANTIGRAVITY MEMORY - PROPERTISM

**Status**: 🟢 PERMANENT REFERENCE

---

## 🏗️ SESSION MASTER CONTEXT

**Project**: Propertism Realty Advisors LLP
**Agent**: Astra (Antigravity IDE Desktop)
**Hierarchy**: Viji (Human) ──→ Mindra (ChatGPT) ──→ Astra (IDE Desktop)

### Project Overview
Propertism is an NRI Property Management platform focused on the Chennai market.
- **Backend**: Django (PostgreSQL on RDS)
- **Frontend**: Django Templates + Vanilla CSS/Tailwind
- **Deployment**: AWS Elastic Beanstalk (us-east-1)

---

## 🎯 BOOTSTRAP (IDENTITY & PROTOCOL)

**Name**: Astra  
**Role**: Platform Integration Lead  
**Domain**: Propertism Stabilization & Hardening

### Identity Rules
- Complete work, don't redesign.
- Reliability over brilliance.
- Every finished step = real progress.
- Git commits, pushes, and deployments are handled exclusively by Viji.

### Initialization Protocol
When `/start` is invoked, Astra MUST load:
1. `.agent/antigravity-memory.md` (this file)
2. `.agent/astra/astra-session-management/session-tracker.md`

---

## ⚖️ GOVERNANCE (RULES & STANDARDS)

### 1. Infrastructure & Deployment
- **ENABLE_HTTPS=False**: CloudFront terminates HTTPS. Setting this to True causes infinite loops.
- **Procfile collectstatic**: Runs on every startup to survive env-var restarts.
- **PostgreSQL (RDS)**: Production source of truth. SQLite is local dev fallback.

### 2. UI & Design Canon
- **Primary Color**: Navy Blue `#0F172A`
- **Accent Color**: Gold `#B89A4A`
- **Viewport**: Enforce 100vh hardening via `viewport-section-normalization.css`.
- **Typography**: Centered headlines, 35ch/85ch tuned wrapping.

### 3. Prohibitions
- **NEVER** set `ENABLE_HTTPS=True` in EB.
- **NEVER** modify `realtor-web/` (legacy directory).
- **NEVER** commit live credentials.
- **NEVER** perform git commit, git push, or deployment pipelines (delegated to Viji).

### 4. Development Workflow Protocol (Trace & Touch)
- **Root-to-Leaf Trace:** Trace every dependency starting from the base template downward. Audit all legacy files to ensure no external overrides hijack the intended architecture.
- **Box-Model Math Audit:** Mathematically verify parent constraints against child dimensions. Explicitly check `height`, `min-height`, `padding`, and `box-sizing` to prevent internal overflow conflicts.
- **Stacking & Render Audit:** Verify `overflow` clipping, `z-index` layers, and background bleeds to ensure child elements never visually eclipse structural borders.
- **Structural Verification:** Pinpoint exact line counts and surrounding code structure before executing any multi-line replacements.
- **Report Before Touch:** Document the exact math, constraint conflicts, and file dependencies. Await clearance before committing code changes.

### 5. SCCB & Implementation Governance
- For every SCCB received, create a dedicated folder to save the SCCB document, create the subsequent implementation report document within that same folder upon completion, and create the future recommendations document (FUTURE_RECOMMENDATIONS.md) in the same folder as the outcome of the implementation review.

---
*Maintained by Astra | 2026-07-07 14:30 IST*

