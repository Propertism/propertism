<!-- AUDIT METADATA -->
<!-- Date: 2026-10-06 -->
<!-- Time: 09:41 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra 1 -->
<!-- Module: 03-propertism -->
<!-- Status: RATIFIED & PLANNED -->
<!-- Git Commit: HEAD -->

# 🏛️ CONTROL SCCB DIRECTIVE: AWS NEW ACCOUNT MIGRATION & DB CONFIG

**SCCB ID**: `SCCB-AWS-NEW-ACCOUNT-MIGRATION`  
**Module**: `03-propertism`  
**Product Owner**: Viji  
**Implementation Supervisor**: Astra 1  
**Status**: 🟢 RATIFIED & ACTIVE  

---

## 1. 📌 OBJECTIVES & AUDIT CONTROL
- **Target AWS Account**: **`Propertism-AWS`** (Account ID: `1320-5873-4957`)
- **Zero Host Config**: PostgreSQL DB-backed `SystemConfig` subsystem stores secrets, SMTP credentials, AI settings, and security flags.
- **Zero Downtime Migration**: New AWS Lightsail instance provisioned, database dump (`pg_dump`) & persistent media storage `/var/www/propertism_media` restored.
- **GoDaddy DNS Invariant**: GoDaddy DNS `@` & `www` A records flipped only after pre-cutover testing gate is verified and approved by Viji.
- **Master Plan Document**: [`reports/AWS_NEW_ACCOUNT_MIGRATION_PLAN.md`](file:///d:/viji/viji-olivine/03-propertism/reports/AWS_NEW_ACCOUNT_MIGRATION_PLAN.md)
- **Task Registry**: [`03-Execute/01-task-registry/TASK-REGISTRY.md`](file:///d:/viji/viji-olivine/03-propertism/03-Execute/01-task-registry/TASK-REGISTRY.md)
