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
