# Agent Session Command Contract - PROPERTISM

## Purpose
This repository defines stable chat-level startup/closure commands for the Propertism stabilization project.

## Command Routing
- `/start` -> Astra workflow for Propertism (`.agent/workflows/start.md`).
- `/end` -> Astra closure for Propertism (`.agent/workflows/end.md`).

## Astra Startup Behavior (`/start`)
On `/start`, load and enforce:
1. `.agent/antigravity-memory.md`
2. `.agent/astra/astra-session-management/session-tracker.md`
3. `.session-tracker/SESSION_TRACKER.md` (Legacy)

Then return:
- Status: READY
- Current Role: Platform Integration Lead
- Scope Lock: Propertism stabilization only

## Astra Closure Behavior (`/end`)
On `/end`, follow `.agent/workflows/end.md` and update:
- `.agent/astra/astra-session-management/session-tracker.md`
- `.session-tracker/SESSION_TRACKER.md`
- Create commit manifest in `.agent/astra/astra-session-management/commit-details/`

## Conversation Governance
- Use command-driven execution style.
- Maintain READ-ONLY access to `erp-main`.
- Focus exclusively on Propertism stabilization.
