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
