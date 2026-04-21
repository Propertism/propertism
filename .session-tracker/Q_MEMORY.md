# Q Memory — Amazon Q DevOps Context

> This file is Q's persistent memory across sessions.
> Q = Amazon Q Developer (AWS IDE plugin)
> Read this at the start of every session.

---

## Who Is Viji

- **Name:** Viji
- **Role:** Founder / Architect — runs a multi-agent AI-assisted software team
- **Style:** Direct, fast-moving, trusts the team to execute
- **GitHub Org:** Propertism (and related orgs)

---

## The Team (Multi-Agent)

| Agent | Role / Strength |
|---|---|
| **Q** (me) | DevOps, AWS, Django backend, deployments — assigned since ~Apr 2026 |
| **Kiro** | Long-term companion, ~10 months, broad dev work |
| **ChatGPT** | General reasoning, drafting |
| **Google AG** | Google ecosystem, search |
| **Windsurf** | IDE coding |
| **Cursor** | IDE coding |
| **Codex** | Code generation |
| **Qwen** | Code generation |
| **Claude Code** | Code execution |
| **Claude.ai** | Reasoning, architecture |

---

## Q's Role

- **Primary:** DevOps for all Viji's products
- AWS Elastic Beanstalk deployments
- CI/CD (GitHub Actions)
- Nginx, gunicorn, RDS, CloudFront, S3
- Django settings, migrations, postdeploy hooks
- Production incident response
- Session tracking and memory management

---

## Product Portfolio

### 1. Propertism — `propertism.in`
- **Repo:** github.com/Propertism/propertism (branch: main)
- **Stack:** Django, PostgreSQL (RDS), Elastic Beanstalk, CloudFront
- **Local path:** `d:\viji\viji-olivine\03rolledout\01propertism`
- **Status:** Live, Green
- **Q sessions:** 20–23 (and counting)
- **Key notes:** See `SESSION_TRACKER.md` for full ops history

### 2. Propertism Deal Engine — `admin.propertism.in`
- **Stack:** Flask
- **Local path:** `d:\viji\viji-olivine\03rolledout\06propertism.deal.engine`
- **Status:** Live

### 3. JobRadar
- **Status:** Live, global users
- **Q context:** Not yet onboarded

### 4. ToolsQuota
- **Status:** Live, global users
- **Q context:** Not yet onboarded

### 5. Viji.ai
- **Status:** Live
- **Q context:** Not yet onboarded

### 6. Olivine.co.in
- **Status:** Live
- **Q context:** Not yet onboarded

### 7. ERP (In Development)
- **Modules:** Retail, POS, HRM, FMS, CRM
- **Status:** Under development
- **Q context:** Not yet onboarded

---

## Q's Working Rules

1. Read `SESSION_TRACKER.md` + this file at the start of every session
2. Never seed or restore live data unless Viji explicitly says `deploy +seed`
3. Never disturb working production behaviour when fixing isolated issues
4. Always update `SESSION_TRACKER.md` after significant work
5. Prefer minimal, surgical changes — no verbose implementations
6. When a deploy fails, diagnose before touching more files
7. Keep `media/` in the EB bundle — hero and property images live there
8. `ENABLE_HTTPS` must stay `False` on EB — CloudFront handles HTTPS

---

## AWS Infrastructure Summary

| Resource | Value |
|---|---|
| EB App | propertism-2026 |
| EB Env | propertism-prod-2026 |
| Region | us-east-1 |
| CloudFront | E1GGPU208SQFFT |
| RDS | propertism-prod-pg |
| CI/CD | GitHub Actions → push to main → auto deploy |

