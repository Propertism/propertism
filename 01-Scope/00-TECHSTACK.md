<!-- AUDIT METADATA -->
<!-- Date: 2026-08-29 -->
<!-- Time: 22:20 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra -->
<!-- Module: TEMPLATE -->
<!-- Status: CANONICAL TEMPLATE -->
<!-- Git Commit: HEAD (uncommitted) -->

# 00-TECHSTACK — Technology Stack & Runtime Configuration

**Module**: `03-propertism`  
**Protocol**: S.P.E.C. (01-Scope)  
**Status**: 🟢 ACTIVE  

---

## 1. Runtime & Environment Standards
- **Primary Language / Framework**: Python / TypeScript / React
- **Runtime Version**: Python 3.11+ / Node.js 20+
- **Database / Storage**: PostgreSQL / SQLite / Qdrant Embedded
- **Assigned Port(s)**: TBD

## 2. Invariant Rules & Boundaries
- Zero mock data in production paths.
- Localized dependencies strictly isolated to `03-propertism`.
- All tasks tracked via `03-Execute/01-task-registry/TASK-REGISTRY.md`.
