<!-- AUDIT METADATA -->
<!-- Date: 2026-08-30 -->
<!-- Time: 09:55 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra -->
<!-- Module: 03-propertism -->
<!-- Status: ACTIVE -->
<!-- Git Commit: HEAD -->

## 🌐 GitHub Account & Repository Rule
- Repository: `https://github.com/Propertism/propertism`
- Active GitHub CLI Account: **`Propertism`** (`gh auth switch --user Propertism`)

## ⚠️ Production Database — STRICT RULE
NEVER write to, seed, modify, or touch the production database without explicit written approval from Viji. This includes auto-seeding logic, direct INSERT/UPDATE, or any code that modifies prod DB state on first run. Local/dev databases are fine.

## 🏛️ Absolute Code & Deployment Protocol (Viji Law, 2026-09-04)
The mandatory 8-stage delivery lifecycle for all engineering and code fixes:
1. **Fix Locally**: Make code changes strictly in the local repository. Zero direct server edits.
2. **Internal Test & Declare (Astra)**: *"Declaring done is a claim; evidence is the proof."* Astra deterministically verifies builds and unit tests locally.
3. **Report to Viji**: Present test output, evidence proof, and diffs to Viji.
4. **Viji Verifies**: Human verification by Product Owner.
5. **Viji Approves**: Explicit chat approval to proceed with deployment.
6. **Git Push (Astra)**: Push to `origin/main` under `Propertism` account.
7. **CI/CD Pipeline**: GitHub Actions deploys automatically to Lightsail Mumbai.
8. **Prod Validation & Tracker Closure**: Viji validates in live production ➔ Only then does Astra update and seal closure in `05-Sessions/session.md` and task registries.

### 🚫 Lightsail Server Constraint
- **NO direct Lightsail environment changes** for any application code.
- Direct VPS edits are strictly limited to runtime `.env` secret updates or isolated one-off scripts.
- If anything requires a code fix, it MUST strictly travel the 8-stage lifecycle above.

## SCCB / Report-First Execution Rule
When a task prompt requires an SCCB, audit report, implementation brief or other task-control report:
1. Read the canonical governance (`AGENTS.md`, applicable `CLAUDE.md`) and the relevant task context.
2. Create or update the applicable SCCB/report in the designated directory **before** starting implementation.
3. Record scope, planned actions, risks, and validation criteria in that artifact.
4. Execute the authorised task.
5. Update the same SCCB/report with actual changes, tests, evidence, unresolved issues, and final status.

Never defer creation of the required report until after the task. When Viji specifies a mandatory report location for an ongoing exercise, save all associated SCCBs and reports there until Viji explicitly closes the exercise. Do not invent a separate Task-Rules skill; this file is the governing instruction.
