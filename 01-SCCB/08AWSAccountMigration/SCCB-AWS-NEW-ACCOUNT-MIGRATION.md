<!-- AUDIT METADATA -->
<!-- Date: 2026-10-06 -->
<!-- Time: 09:41 IST -->
<!-- Product Owner: Viji -->
<!-- Supervisor: Astra 1 -->
<!-- Module: 03-propertism -->
<!-- Status: RATIFIED & PLANNED -->
<!-- Git Commit: HEAD -->

# 🏛️ SCCB DIRECTIVE: AWS NEW ACCOUNT MIGRATION & DB CONFIGURATION SUBSYSTEM

**SCCB ID**: `SCCB-AWS-NEW-ACCOUNT-MIGRATION`  
**Module**: `03-propertism`  
**Product Owner**: Viji  
**Implementation Supervisor**: Astra 1  
**Status**: 🟢 RATIFIED  

---

## 1. 🎯 DIRECTIVE OBJECTIVES & MANDATES
1. **AWS Account Migration**: Move production deployment from current AWS account (`622370466597`) to Viji's target AWS account.
2. **Zero GoDaddy / Git Disruption**: GoDaddy DNS records (`@` & `www`) and single git repository (`Propertism/propertism`) remain unchanged.
3. **Database-Backed Settings Subsystem**: Store all runtime application environment variables, SMTP credentials, API keys, and feature flags inside PostgreSQL database (`propertism_db`), rendering future host deployment zero-configuration on AWS.
4. **Validation Gate**: Empirical pre-cutover testing (contact form, Titan SMTP, realBOT, admin login) on new server IP with explicit Viji human signoff before DNS cutover.
5. **Safe Decommissioning**: 5-day post-cutover observation window prior to terminating old Lightsail VPS (`13.207.123.15`).

---

## 2. 🔗 CANONICAL PLAN REFERENCE
- Full plan document archived at: [`reports/AWS_NEW_ACCOUNT_MIGRATION_PLAN.md`](file:///d:/viji/viji-olivine/03-propertism/reports/AWS_NEW_ACCOUNT_MIGRATION_PLAN.md)
- Task Registry: [`03-Execute/01-task-registry/TASK-REGISTRY.md`](file:///d:/viji/viji-olivine/03-propertism/03-Execute/01-task-registry/TASK-REGISTRY.md)
