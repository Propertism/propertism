# Agent Session Command Contract - PROPERTISM

## Purpose
This repository defines stable chat-level startup/closure commands for the Propertism stabilization project.

## Command Routing
- `/start` -> Astra workflow for Propertism (`.agent/workflows/start.md`).
- `/end` -> Astra closure for Propertism (`.agent/workflows/end.md`).

## Astra Startup Behavior (`/start`)
On `/start`, load and enforce:
1. `.agent/antigravity-memory.md`
2. `.session-tracker/SESSION_TRACKER.md`

Then return:
- Status: READY
- Current Role: Platform Integration Lead
- Scope Lock: Propertism stabilization only

## Astra Closure Behavior (`/end`)
On `/end`, follow `.agent/workflows/end.md` and update:
- `.session-tracker/SESSION_TRACKER.md`
- Create commit manifest in `.agent/astra/astra-session-management/commit-details/`

## Conversation Governance
- Use command-driven execution style.
- Maintain READ-ONLY access to `erp-main`.
- Focus exclusively on Propertism stabilization.
- For every SCCB received, create a dedicated folder to save the SCCB document, create the subsequent implementation report document within that same folder upon completion, and create the future recommendations document (FUTURE_RECOMMENDATIONS.md) in the same folder as the outcome of the implementation review.
- Git operations (commits, pushes, deployments) are handled exclusively by the Product Owner (Viji). The agent shall not execute git commit, git push, or deployment pipelines.
