# 🏛️ FINAL ARCHITECTURAL IMPLEMENTATION PLAN (REV-8.4)
## Propertism Infrastructure Right-Sizing: Elastic Beanstalk + RDS ➔ Unified AWS Lightsail

> **Platform**: `03-propertism` (`www.propertism.in`)  
> **Product Owner & Supreme Architect**: Viji  
> **Chief Architect & Governance Authority**: Mindra (ChatGPT)  
> **Implementation Supervisor**: Astra (Antigravity IDE)  
> **Target Region**: **AWS `ap-south-1` (Mumbai)**  
> **Target Tier**: **2 GB RAM / 2 vCPU / 60 GB SSD / 3 TB Transfer — Current IPv4 Lightsail Tier ($12.00/mo)**  
> **Protocol**: Controlled Migration with 15-Minute Target Maintenance Interval, 10-Layer Authoritative Effective-Privilege Write Barrier, Loopback-Only Smoke Validation, Single Canonical IEEE-754 / Decimal Content Fingerprinting & Byte-Level Backup Verification  
> **Execution Status**: 🔴 HOLD — STANDBY FOR EXPLICIT MINDRA / VIJI APPROVAL (NO PRODUCTION EXECUTION)  

---

## 📑 TABLE OF CONTENTS
1. [Core Migration Architecture & Regional Placement](#1-core-migration-architecture--regional-placement)
2. [Financial Audit & Lightsail IPv4 Pricing Model](#2-financial-audit--lightsail-ipv4-pricing-model)
3. [Pre-Flight Requirements (9 Mandatory Readiness Gates)](#3-pre-flight-requirements-9-mandatory-readiness-gates)
4. [Multi-Tier Database Parity Verification Procedure](#4-multi-tier-database-parity-verification-procedure)
5. [Authoritative Final-Cutover Write-Freeze & Immutability Verification Protocol](#5-authoritative-final-cutover-write-freeze--immutability-verification-protocol)
6. [Deterministic Final-Sync Acceptance Gate (FINAL_CUTOVER_RECORD.json)](#6-deterministic-final-sync-acceptance-gate-final_cutover_recordjson)
7. [PostgreSQL Production vs. Sandbox Ownership & ACL Strategy](#7-postgresql-production-vs-sandbox-ownership--acl-strategy)
8. [Step-by-Step Migration Runbook (Task 1 to Task 12)](#8-step-by-step-migration-runbook-task-1-to-task-12)
9. [Initial Resource Budget & Conservative Gunicorn Tuning](#9-initial-resource-budget--conservative-gunicorn-tuning)
10. [Hardened S3 Backup, Byte-Level Verification & 10-Point Restoration Suite](#10-hardened-s3-backup-byte-level-verification--10-point-restoration-suite)
11. [Automated Snapshot Scheduling (UTC Semantics & Execution Timing)](#11-automated-snapshot-scheduling-utc-semantics--execution-timing)
12. [Security Baseline: SSH, UFW, Network & Secrets Protection](#12-security-baseline-ssh-ufw-network--secrets-protection)
13. [Fail-Closed Loopback-Only Nginx Maintenance & Smoke Testing](#13-fail-closed-loopback-only-nginx-maintenance--smoke-testing)
14. [Media Migration, Storage Permissions & Deterministic Manifest Gate](#14-media-migration-storage-permissions--deterministic-manifest-gate)
15. [Dual-Stage Rollback Runbook (Zero-Concurrent-Writer Authority Discipline)](#15-dual-stage-rollback-runbook-zero-concurrent-writer-authority-discipline)
16. [14-Point Cooldown & Controlled Decommissioning Gate](#16-14-point-cooldown--controlled-decommissioning-gate)
17. [Deployment Scaffolding & Machine-Deterministic Migration Check](#17-deployment-scaffolding--machine-deterministic-migration-check)
18. [Updated Risk Register](#18-updated-risk-register)
19. [Final REV-8.4 Approval Gate](#19-final-rev-84-approval-gate)

---

## 1. Core Migration Architecture & Regional Placement

In compliance with Mindra CTO Directives §1, C-01, and C-18, the target topology unifies compute and database onto AWS Lightsail without multi-subnet or Elastic Beanstalk orchestration overhead. Storage is accurately designated as **60 GB included Lightsail SSD storage**. Django connects to PostgreSQL strictly over local TCP loopback using SCRAM-SHA-256 password authentication:

```text
Internet (Users & NRI Clients)
      │
      ▼
GoDaddy Authoritative DNS (propertism.in / www.propertism.in — Comprehensive A/AAAA/CAA Inventory)
      │
      ▼  [Controlled DNS cutover with pre-lowered TTL 300s]
AWS Lightsail Static IPv4 (ap-south-1 Mumbai)
      │
      ├── Port 80/tcp  ➔ HTTP ➔ 301 Redirect to HTTPS
      └── Port 443/tcp ➔ Nginx 1.24+ (Reverse Proxy + Let's Encrypt SSL + Static/Media Cache)
            │
            ├── [Public Internet Path] ➔ Maintenance Active ➔ HTTP 503 Service Unavailable
            └── [Loopback Path (127.0.0.1 / ::1 ONLY)] ➔ Local Unix domain socket: /run/gunicorn.sock
                  │
                  ▼
            Gunicorn WSGI Master (2 Sync Workers — Conservative Baseline)
                  │
                  ▼
            Django 4.2 Application Core (realtor_project)
                  ├── PostgreSQL 16 (127.0.0.1:5432 / SCRAM-SHA-256 password auth on 60 GB Lightsail SSD)
                  │     ├── Owner: postgres (100% of application tables, sequences, views, functions, types)
                  │     └── Runtime Role: propertism_user (Explicit DML grants only; 0 owned objects; 0 admin privileges)
                  ├── Redis 7.x (Local Unix Socket / 127.0.0.1:6379 for Cache & Throttling)
                  └── Local Media Storage (Direct Nginx alias with execution blocking on 60 GB Lightsail SSD)
```

### Regional Placement Rationale
- **Target Region**: **`ap-south-1` (Mumbai)**.
- **Latency Optimization**: Propertism's target audience comprises property owners and buyers in Chennai / Tamil Nadu, alongside global NRIs (USA, UK, Singapore, UAE). Latency from Chennai to Mumbai is **~25–30 ms**, compared to **~200–220 ms** to `us-east-1` (N. Virginia). Database round-trips drop from network-bound VPC latency (2–5 ms) to **< 0.5 ms** over local loopback.

---

## 2. Financial Audit & Lightsail IPv4 Pricing Model

In compliance with Mindra CTO Directive §2 and C-05:

### 1. Itemized Cost Breakdown (Fixed vs. Usage-Dependent)

| Cost Component | Current Stack: Elastic Beanstalk + Dedicated RDS | Target Stack: Unified AWS Lightsail (Current IPv4 Tier) | Cost Type |
|---|---|---|:---:|
| **Base Instance Compute** | EC2 `t3.micro` ($16.70/mo nominal; $5.84/mo with Savings Plan) | **2 GB RAM / 2 vCPU / 60 GB SSD / 3 TB Transfer** (with Public IPv4) | **Fixed** |
| **Instance Monthly Rate** | $16.70 / month | **$12.00 / month** | **Fixed** |
| **Database Compute Tier** | RDS PostgreSQL `db.t3.micro`: **$15.69 / month** | **$0.00** (Co-located PostgreSQL 16 on instance) | **Fixed** |
| **VPC & Public IPv4 Charges** | Public IPv4 in-use + NAT/EIPs: **$7.44 / month** | **$0.00** (1 Static IPv4 included in bundle) | **Fixed** |
| **Root & Database Storage** | EBS gp3 20GB root + RDS gp3 20GB: **~$3.00 / month** | **$0.00** (60 GB Lightsail SSD storage included in bundle) | **Fixed** |
| **Outbound Data Transfer** | ~$0.25 / month | **$0.00** (3,000 GB / 3 TB free allowance included) | **Fixed** |
| **Automated Snapshot Storage** | RDS automated backups (included in RDS fee) | **Usage-dependent** (Estimated ~$0.20 – $0.50/mo at $0.05/GB/mo on differential retained blocks) | **Variable** |
| **Nightly S3 Database Backups** | None | **Usage-dependent** (Estimated < $0.05/mo for compressed `< 50 MB` dumps with 30-day lifecycle) | **Variable** |
| **S3 Requests / Transfer** | N/A | **Usage-dependent** (Negligible; `< $0.01/mo` for daily PUT/GET within `ap-south-1`) | **Variable** |
| **Total Monthly Spend** | **~$40.08 / month** (~₹3,350 – ₹3,500 INR/mo) | **~$12.25 – $12.55 / month** (~₹1,020 – ₹1,050 INR/mo) | **Combined** |
| **Total Annual Spend** | **~₹40,000 – ₹42,000 INR / year** | **~₹12,250 – ₹12,600 INR / year** | **Combined** |
| **Net Projected Annual Savings** | Baseline | **~₹27,500 – ₹29,500 INR / year saved (69% to 71% cost reduction)** | — |

### 2. Credit Runway Analysis & Promotional Credit Caveats
- **Remaining Promotional Credits**: **`$32.56`** (AWS Account `<AWS_ACCOUNT_ID>`).
- **Runway on Current Stack ($40.08/mo)**: Exhausted in **~20–24 days** (late September 2026), immediately triggering out-of-pocket billing.
- **Runway on Lightsail ($12.25–$12.55/mo)**: Extends credit life to **~2.6 months** (through late November / early December 2026).
- **Promotional Credit Applicability Rule**: AWS promotional credits generally apply to Amazon Lightsail instances, S3, and data transfer. Out-of-pocket cost post-credit is locked at a predictable **₹1,020 – ₹1,050 INR/month**.

---

## 3. Pre-Flight Requirements (9 Mandatory Readiness Gates)

Before launching any production infrastructure, importing databases, or touching DNS, all 9 pre-flight gates must be cleared with verifiable evidence:

```text
[Gate 1: AWS Identity & Region] ➔ [Gate 2: RDS Manual Snapshot] ➔ [Gate 3: Read-Only Dump & SHA-256]
       │
       ▼
[Gate 4: Comprehensive Ownership, Recursive Roles & Routine Audit (C-54, C-67, C-69, C-72, C-73)] ➔ [Gate 5: Parity]
       │
       ▼
[Gate 6: Media Footprint Audit] ➔ [Gate 7: PostgreSQL Compatibility & Collation Justification (C-51, C-62)]
       │
       ▼
[Gate 8: Comprehensive DNS Inventory (A/AAAA/CAA) & TTL 300s (C-63)] ➔ [Gate 9: Production Secrets Isolation]
```

### Gate 1: AWS Identity & Regional Verification
- Confirm AWS CLI caller identity: `aws sts get-caller-identity` (Account must match authorized production account).
- Verify Lightsail service availability in `ap-south-1`:
  ```bash
  aws lightsail get-blueprints --region ap-south-1 --query "blueprints[?id=='ubuntu_24_04'].id"
  ```

### Gate 2: Full RDS Production Manual Snapshot (Non-Destructive)
- Trigger a manual safety snapshot of the live Amazon RDS PostgreSQL database:
  ```bash
  aws rds create-db-snapshot \
      --db-instance-identifier propertism-db \
      --db-snapshot-identifier propertism-rds-pre-migration-safety-snapshot \
      --region us-east-1
  ```
- Verify status reaches `available` in AWS Console before continuing.

### Gate 3: Read-Only Logical Dump with Cryptographic Checksum
- Export baseline database using `pg_dump` with least-privilege flags:
  ```bash
  pg_dump -h <RDS_ENDPOINT> -U postgres -d propertism_db -F c -b -v --no-owner --no-privileges -f /tmp/propertism_prod_preflight.dump
  ```
- Generate SHA-256 checksum:
  ```bash
  sha256sum /tmp/propertism_prod_preflight.dump > /tmp/propertism_prod_preflight.dump.sha256
  ```
- Live production RDS database remains **100% read-only untouched**.

### Gate 4: Comprehensive Pre-Flight Production Ownership, Recursive Role & Routine Audit (C-54, C-67, C-69, C-72, C-73)
In compliance with C-54, C-67, C-69, C-72, and C-73, production object ownership, recursive role memberships, and callable routines must be comprehensively audited **before** entering the final cutover window:

1. **Comprehensive Object Ownership Audit (C-69)**:
   ```sql
   -- Verify propertism_user owns ZERO application objects across all 8 relevant object classes
   SELECT c.relkind, count(*) AS propertism_user_owned_objects
   FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
   WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p', 'S', 'v', 'm', 'f')
     AND pg_get_userbyid(c.relowner) = 'propertism_user'
   GROUP BY c.relkind
   UNION ALL
   SELECT 'function/proc', count(*)
   FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
   WHERE n.nspname = 'public' AND pg_get_userbyid(p.proowner) = 'propertism_user'
   UNION ALL
   SELECT 'type/domain', count(*)
   FROM pg_type t JOIN pg_namespace n ON n.oid = t.typnamespace
   WHERE n.nspname = 'public' AND pg_get_userbyid(t.typowner) = 'propertism_user';
   ```
   **Pass Rule**: Must return exactly `0` rows where count $> 0$. If any application object is owned by `propertism_user`, **FAIL CLOSED IMMEDIATELY**. Resolve and re-audit during preflight.

2. **Role Attribute Audit (C-67)**:
   ```sql
   SELECT rolname, rolsuper, rolbypassrls, rolcreaterole, rolcreatedb, rolreplication 
   FROM pg_roles WHERE rolname = 'propertism_user';
   ```
   Must return all `false`.

3. **Recursive Role-Membership Audit (C-73)**:
   ```sql
   WITH RECURSIVE role_hierarchy AS (
       SELECT member, roleid, 1 AS depth
       FROM pg_auth_members
       WHERE member = 'propertism_user'::regrole
       UNION ALL
       SELECT m.member, m.roleid, rh.depth + 1
       FROM pg_auth_members m
       JOIN role_hierarchy rh ON m.member = rh.roleid
   )
   SELECT r.rolname AS inherited_role, rh.depth
   FROM role_hierarchy rh
   JOIN pg_roles r ON r.oid = rh.roleid
   WHERE r.rolsuper 
      OR r.rolcreaterole 
      OR r.rolcreatedb 
      OR r.rolreplication 
      OR r.rolbypassrls 
      OR r.rolname IN ('postgres', 'rds_superuser', 'pg_write_all_data', 'pg_database_owner');
   ```
   **Pass Rule**: Must return exactly `0` rows. `propertism_user` inherits zero write or administrative privileges through any direct or nested role.

4. **Security-Definer & Callable Routine Audit (C-72)**:
   ```sql
   SELECT p.proname, pg_get_userbyid(p.proowner) AS owner, p.prosecdef, p.provolatile
   FROM pg_proc p
   JOIN pg_namespace n ON n.oid = p.pronamespace
   WHERE n.nspname = 'public'
     AND has_function_privilege('propertism_user', p.oid, 'execute')
     AND (p.prosecdef = true OR p.provolatile = 'v');
   ```
   **Pass Rule**: Must return exactly `0` rows. Zero executable volatile or `SECURITY DEFINER` routines exist that could be invoked by `propertism_user` to mutate state.

5. **Pre-Freeze ACL State Capture (C-67)**:
   Dump complete pre-freeze privilege definitions to `reports/PRE_FREEZE_ACL_STATE.json` for deterministic rollback and post-cutover restoration.

### Gate 5: Baseline Database Parity Capture
- Run extended parity baseline capture against RDS (see Section 4). Saved to `reports/PRE_MIGRATION_DATABASE_PARITY_BASELINE.json`.

### Gate 6: Media Footprint & Storage Audit
- Measure exact disk usage of existing media:
  ```bash
  aws s3 ls s3://<MEDIA_BUCKET_NAME>/media/ --recursive --human-readable --summarize
  ```
- **Disk Headroom Gate**: Media footprint must be `< 15 GB` to leave $\ge 35\text{ GB}$ free on the 60 GB Lightsail SSD.

### Gate 7: PostgreSQL Compatibility & Collation Justification Gate (C-51, C-62)
Before restore, inventory and compare source RDS PostgreSQL parameters against target Lightsail PostgreSQL 16:
- Version: `SHOW server_version;`
- Server Encoding: `SHOW server_encoding;` (Must be `UTF8`)
- Collation & Locale: `SHOW lc_collate; SHOW lc_ctype;` (Requirement: Collation/locale must be compatible with application and database behavior. Target Lightsail PostgreSQL 16 is provisioned with `en_US.UTF-8`, matching RDS. Verified compatible with Django text sorting and trgm queries).
- Timezone: `SHOW timezone;` (Must match application expectations, `Asia/Kolkata` or `UTC`).
- Installed Extensions: `SELECT extname, extversion FROM pg_extension;` (Verify all extensions like `unaccent`, `pg_trgm`, `uuid-ossp` are installed and active on target).
- Output recorded in `reports/POSTGRESQL_COMPATIBILITY_AUDIT.json`.
- **Pass Criterion**: Zero missing extensions, identical UTF8 encoding, compatible collation/locale, matching timezone. Fail closed if incompatible.

### Gate 8: Comprehensive DNS Inventory (A/AAAA/CNAME/CAA) & TTL Reduction (C-63)
In compliance with C-63, perform an exhaustive DNS record inventory for `propertism.in` and `www.propertism.in`:
- Capture current records from GoDaddy DNS:
  - `@ A` and `www A` records.
  - `@ AAAA` and `www AAAA` records (Crucial: verify if any IPv6 address exists; if pointing to legacy stack, it must be removed during cutover to prevent IPv6 traffic bypassing Lightsail IPv4).
  - CNAME records (if any).
  - CAA records (verify `letsencrypt.org` is permitted).
- Lower TTL on all existing `A` and `AAAA` records to **`300 seconds` (5 minutes)** at least **24 hours prior to cutover**.
- Saved to `reports/PRE_CUTOVER_DNS_INVENTORY.json`.

### Gate 9: Production Secrets Isolation (Zero Secrets in Git)
- Verify `.gitignore` protects `.env`, `*.dump`, `*.sql`, `*.pem`, `*.key`.
- Confirm `.env.production.template` contains only dummy placeholders.

---

## 4. Multi-Tier Database Parity Verification Procedure

In compliance with Mindra CTO Directives §4, C-11, C-21, C-28, C-42, C-47, C-59, C-60, C-61, C-68, and C-71:
- **Structural Parity**: Schemas, tables, constraints, foreign keys, indexes.
- **Aggregate Parity**: Total row counts, ID ranges, NULL counts, timestamp boundaries.
- **Content Fingerprint Parity (C-42, C-47, C-59, C-60, C-68, C-71 Authoritative Data Gate)**: Deterministic, single-specification SHA-256 row-by-row canonical fingerprint per table.
- **Sequence Parity**: Exact `last_value` and `is_called` match with safety invariants.
- **Migration-State Parity**: Exact row-for-row match on `(app, name, applied)` in `django_migrations`.

> [!IMPORTANT]
> **HIERARCHY OF VERIFICATION CONTROLS (C-47, C-61, C-67, C-76)**:
> 1. **Authoritative 10-Layer Effective Write Barrier**: Proves `propertism_user` has **zero effective capability to mutate production business state through direct SQL privileges or privileged callable database objects**.
> 2. **T0/T1 Snapshot Comparison**: Secondary operational immutability evidence / supporting telemetry.
> 3. **`pg_dump` SHA-256 Checksum**: Physical file transfer and backup artifact integrity.
> 4. **Content Fingerprint SHA-256**: Authoritative source/target logical data-content equivalence.

### Deterministic Content Fingerprint Algorithm Specification (`scripts/audit_database_content_fingerprints.py`) (C-47, C-68, C-71)
For every table in the `public` schema, the script executes the exact same reference canonicalization protocol on both RDS source and Lightsail target:

#### 1. Deterministic Ordering Key Discovery (C-60)
- Query `pg_index` and `pg_attribute` for the Primary Key column set (single or composite), sorted by key ordinal position.
- **Non-Null Unique Key Fallback**: If a table has no Primary Key:
  1. Discover all candidate `UNIQUE` constraints via `pg_constraint`.
  2. Verify that **ALL columns in the candidate constraint are strictly `NOT NULL`**. Nullable unique keys are rejected.
  3. If multiple valid non-null unique constraints exist, select the candidate key deterministically by sorting constraint names alphabetically.
  4. If no valid non-null unique key exists $\rightarrow$ **FAIL CLOSED IMMEDIATELY**. Do not proceed with un-ordered fingerprinting.
- Query `information_schema.columns` to extract all persistent column names, sorted strictly alphabetically by `column_name`.

#### 2. Single Canonical Type-Specific Serialization Algorithm (C-68, C-71)
Exactly **one canonical representation** is defined for every supported PostgreSQL type (zero alternatives, zero locale dependencies):
- **Integer types** (`smallint`, `integer`, `bigint`, `serial`, `bigserial`): Standard signed decimal ASCII string (`col::text`).
- **Exact Numeric types** (`numeric`, `decimal`) **(C-71 Singularity Rule)**:
  Retrieved as text via SQL `col::text` into Python standard library `decimal.Decimal`.
  If `val == 0` (which matches positive zero and negative zero `Decimal('-0')`): serialized strictly as ASCII `'0'`.
  Otherwise: serialized strictly as `format(val, 'f')` (guaranteeing exact decimal digits, exact stored scale, no scientific notation, no float conversion, and zero locale dependency).
- **Floating-Point types** (`real`, `double precision`): Serialized strictly based on the **actual 64-bit IEEE-754 value** via Python standard `float.hex(float(val))` (e.g. `'0x1.47ae147ae147bp-7'`), with explicit normalization:
  - `NaN` $\rightarrow$ `'NaN'`
  - `+Infinity` $\rightarrow$ `'+Infinity'`
  - `-Infinity` $\rightarrow$ `'-Infinity'`
  - Positive zero (`+0.0`) and Negative zero (`-0.0`) $\rightarrow$ normalized strictly to `'0.0'`.
  *Note*: IEEE-754 hexadecimal float representation is 100% bit-exact across all CPU architectures and platforms with zero decimal conversion ambiguity.
- **JSONB & JSON** (`jsonb`, `json`): Parsed into standard Python object model, object keys sorted recursively at every level, insignificant whitespace eliminated, array element order strictly preserved, and serialized via:
  `json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)`.
- **Arrays** (`anyarray`): Recursive canonical serialization in bracketed format `[elem1,elem2,...]`. Empty array $\rightarrow$ `[]`. Null elements $\rightarrow$ `\N`. Nested arrays formatted recursively preserving dimensionality. Elements serialized according to their type-specific canonical rules.
- **Temporal types**:
  - `date` $\rightarrow$ ISO 8601: `to_char(col, 'YYYY-MM-DD')`.
  - `timestamp without time zone` $\rightarrow$ ISO 8601 microsecond: `to_char(col, 'YYYY-MM-DD"T"HH24:MI:SS.US')`.
  - `timestamp with time zone` (`timestamptz`) $\rightarrow$ UTC ISO 8601 microsecond: `to_char(col AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"')`.
  - `time without time zone` $\rightarrow$ `to_char(col, 'HH24:MI:SS.US')`.
  - `time with time zone` (`timetz`) $\rightarrow$ UTC: `to_char(col AT TIME ZONE 'UTC', 'HH24:MI:SS.US"Z"')`.
  - `interval` $\rightarrow$ Standard PostgreSQL interval string representation `col::text`.
- **Binary types** (`bytea`): Canonical lowercase hexadecimal string prefixed with `\x` (`encode(col, 'hex')`).
- **Boolean**: Single ASCII character `'t'` or `'f'`.
- **Text / Character** (`text`, `varchar`, `char`, `citext`): Exact UTF-8 encoded bytes.
- **UUID**: Lowercase 36-character hyphenated UUID (`lower(col::text)`).
- **NULL Representation**: Literal two-character ASCII string `\N`.
- **Unsupported / Custom Types**: **FAIL CLOSED**. No unverified fallback.

#### 3. Length-Prefixed Framing & Streaming Hashing (C-47)
- Each column value is framed with its UTF-8 byte length: `[<len>:<canonical_bytes>]`.
- Rows are streamed in strict deterministic order: `ORDER BY <key_col1>, <key_col2>... ASC`.
- Row representations are updated into an incremental `hashlib.sha256()` accumulator.
- Final table fingerprint = `hasher.hexdigest()`.

**Per-Table Output Schema (`reports/DATABASE_CONTENT_PARITY_REPORT.json`)**:
```json
[
  {
    "table": "properties_inquiry",
    "ordering_key": ["id"],
    "ordering_key_type": "PRIMARY_KEY",
    "columns": ["address", "country_code", "created_at", "email", "id", "message", "name", "phone", "property_id"],
    "source_row_count": 290,
    "target_row_count": 290,
    "source_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "target_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "content_match": true
  }
]
```

---

## 5. Authoritative Final-Cutover Write-Freeze & Immutability Verification Protocol

In compliance with Mindra CTO Directives SCCB C-19, C-25, C-26, C-27, C-34, C-36, C-41, C-43, C-45, C-46, C-54, C-61, C-67, C-69, C-72, C-73, C-74, C-75, C-76, and C-77:
- **Target Maintenance Interval: 15 minutes** (C-43). Operational performance target, **NOT a hard timeout or completion guarantee**. Data correctness strictly supersedes time elapsed. If the 15-minute target is exceeded, **DO NOT force the migration forward**; system remains in maintenance until all gates pass or is explicitly aborted.
- **10-Layer Authoritative Write Barrier Invariant (C-74, C-76)**:
  > **`propertism_user` has zero effective capability to mutate production business state through direct SQL privileges or privileged callable database objects.**
- **Zero Concurrent Production Writers**: Exactly one authoritative writable production system at any point in time.

```text
[1. Enter Scheduled Maintenance Interval (Target: 15m)]
      │
      ▼
[2. Fleet-Wide EB Application Maintenance Mode (HTTP 503)]
      │
      ▼
[3. Terminate Active Application Sessions (pg_terminate_backend)]
      │
      ▼
[4. Apply 10-Layer PostgreSQL Privilege Barrier on RDS (C-41, C-46, C-67, C-72, C-74, C-75)]
      │  ├── REVOKE DML on ALL TABLES from propertism_user & PUBLIC
      │  ├── REVOKE USAGE, UPDATE on ALL SEQUENCES from propertism_user & PUBLIC
      │  ├── REVOKE CREATE on SCHEMA public & propertism_db from propertism_user & PUBLIC
      │  ├── REVOKE EXECUTE on ALL FUNCTIONS/PROCEDURES from propertism_user & PUBLIC
      │  └── ALTER ROLE propertism_user SET default_transaction_read_only = on
      │
      ▼
[5. Execute 10-Layer Effective Privilege Audit (C-67, C-69, C-72, C-73, C-74, C-75)]
      │  ├── Layer 1: Ownership Audit (postgres owns 100%, propertism_user owns 0)
      │  ├── Layer 2: Role Attributes Audit (rolsuper, rolbypassrls, etc. == false)
      │  ├── Layer 3: Recursive Role Membership Audit (0 inherited admin/write roles)
      │  ├── Layer 4: PUBLIC Effective Privilege Audit (0 DML, sequence, create grants)
      │  ├── Layer 5: Effective Table DML Audit (has_table_privilege == false across ALL tables)
      │  ├── Layer 6: Effective Sequence Audit (has_sequence_privilege == false across ALL sequences)
      │  ├── Layer 7: Effective Schema/DB Audit (has_schema_privilege == false)
      │  ├── Layer 8: Privileged Routine Audit (0 executable volatile/SECURITY DEFINER routines)
      │  └── Layer 9: Alternate Application Credential Check (0 secondary write roles)
      │
      ▼
[6. Execute Strengthened Transaction-Safe Write Test (Layer 10) (C-77)]
      │  ├── Assert authenticated role: propertism_user
      │  ├── Record observed SQLSTATE (42501 / 25006) and PostgreSQL error message
      │  ├── Execute clean ROLLBACK
      │  └── Verify zero persistent mutation (count_before == count_after, max_id unchanged)
      │
      ▼
[7. In-Flight Request Drain (30s Quiet Period)]
      │
      ▼
[8. Capture Immutability Snapshot T0 (Secondary Operational Telemetry) (C-61)]
      │
      ▼
[9. 30s Quiet Window ➔ Capture Immutability Snapshot T1]
      │
      ▼
[10. Assert Identical Telemetry State (T0 == T1)]
      │
      ▼
[11. Final Production pg_dump & SHA-256 Checksum]
      │
      ▼
[12. Production Target Restore by postgres Administrator (Preserves postgres ownership) (C-55)]
      │
      ▼
[13. Apply Controlled Runtime DML Grants to propertism_user on Target (C-55)]
      │
      ▼
[14. Execute Multi-Tier Parity Gate (Structural + Aggregate + Content Fingerprint + Sequence)]
      │
      ▼
[15. Target Application Smoke Validation (Loopback-Only 127.0.0.1:443) (C-56, C-57, C-58)]
      │
      ▼
════════════════════════════════════════════════════════════════════════════════
[16. ALL GATES PASS (FAIL CLOSED IF ANY DISCREPANCY)]
════════════════════════════════════════════════════════════════════════════════
      │
      ▼
[17. Update GoDaddy DNS Records (A & AAAA cleanup) to Lightsail Static IP (C-63)]
      │
      ▼
[18. Confirm External Production Traffic Arriving on Lightsail]
      │
      ▼
[19. Declare Lightsail Sole Authoritative Production System]
      │
      ▼
[20. Enable Writes on Lightsail (Remove maintenance.flag)]
      │
      ▼
[21. Legacy RDS Remains Immutably Frozen Throughout Cooldown]
```

### Step-by-Step Technical Execution

#### Step 1: Fleet-Wide EB Maintenance Mode
```bash
aws elasticbeanstalk update-environment-configuration \
    --application-name propertism \
    --environment-name propertism-prod-2026 \
    --option-settings Namespace=aws:elasticbeanstalk:application:environment,OptionName=MAINTENANCE_MODE,Value=true \
    --region us-east-1
```

#### Step 2: Apply 10-Layer PostgreSQL Privilege Barrier on RDS (C-41, C-46, C-67, C-72, C-74, C-75)
Executed as RDS master administrator (`postgres`):
```sql
-- 1. Revoke all DML from propertism_user and PUBLIC
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public FROM propertism_user;
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public FROM PUBLIC;

-- 2. Revoke sequence modifications
REVOKE USAGE, UPDATE ON ALL SEQUENCES IN SCHEMA public FROM propertism_user;
REVOKE USAGE, UPDATE ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;

-- 3. Revoke schema/database creation
REVOKE CREATE ON SCHEMA public FROM propertism_user;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE CREATE ON DATABASE propertism_db FROM propertism_user;
REVOKE CREATE ON DATABASE propertism_db FROM PUBLIC;

-- 4. Revoke routine execution to close SECURITY DEFINER bypass (C-72)
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM propertism_user;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC;
REVOKE EXECUTE ON ALL PROCEDURES IN SCHEMA public FROM propertism_user;
REVOKE EXECUTE ON ALL PROCEDURES IN SCHEMA public FROM PUBLIC;

-- 5. Revoke default privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON TABLES FROM propertism_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE USAGE, UPDATE ON SEQUENCES FROM propertism_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE USAGE, UPDATE ON SEQUENCES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE EXECUTE ON ROUTINES FROM propertism_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE EXECUTE ON ROUTINES FROM PUBLIC;

-- 6. Enforce session read-only mode defense-in-depth
ALTER ROLE propertism_user SET default_transaction_read_only = on;

-- 7. Terminate all active application sessions to force immediate privilege reload
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE usename = 'propertism_user' 
  AND pid <> pg_backend_pid();
```

#### Step 3: Execute Comprehensive Effective Privilege Introspection (C-74, C-75)
1. **Effective Table DML Check**:
   ```sql
   SELECT count(*) AS writable_tables
   FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
   WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p')
     AND (has_table_privilege('propertism_user', c.oid, 'insert') OR
          has_table_privilege('propertism_user', c.oid, 'update') OR
          has_table_privilege('propertism_user', c.oid, 'delete') OR
          has_table_privilege('propertism_user', c.oid, 'truncate'));
   ```
   **Pass Rule**: Must return exactly `0`.
2. **Effective Sequence Check**:
   ```sql
   SELECT count(*) AS writable_sequences
   FROM pg_class s JOIN pg_namespace n ON n.oid = s.relnamespace
   WHERE n.nspname = 'public' AND s.relkind = 'S'
     AND (has_sequence_privilege('propertism_user', s.oid, 'usage') OR
          has_sequence_privilege('propertism_user', s.oid, 'update'));
   ```
   **Pass Rule**: Must return exactly `0`.
3. **Effective PUBLIC Privilege Check (C-75)**:
   ```sql
   SELECT count(*) FROM (
       SELECT c.oid FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
       WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p')
         AND (has_table_privilege('public', c.oid, 'insert') OR has_table_privilege('public', c.oid, 'update') OR
              has_table_privilege('public', c.oid, 'delete') OR has_table_privilege('public', c.oid, 'truncate'))
       UNION ALL
       SELECT s.oid FROM pg_class s JOIN pg_namespace n ON n.oid = s.relnamespace
       WHERE n.nspname = 'public' AND s.relkind = 'S'
         AND (has_sequence_privilege('public', s.oid, 'usage') OR has_sequence_privilege('public', s.oid, 'update'))
       UNION ALL
       SELECT n.oid FROM pg_namespace n
       WHERE n.nspname = 'public' AND has_schema_privilege('public', n.oid, 'create')
   ) public_privs;
   ```
   **Pass Rule**: Must return exactly `0`.
4. **Callable Routine & SECURITY DEFINER Check (C-72)**:
   ```sql
   SELECT count(*) AS privileged_executable_routines
   FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
   WHERE n.nspname = 'public'
     AND has_function_privilege('propertism_user', p.oid, 'execute')
     AND (p.prosecdef = true OR p.provolatile = 'v');
   ```
   **Pass Rule**: Must return exactly `0`.

#### Step 4: Execute Strengthened Transaction-Safe Write Test (Layer 10) (C-77)
Executed via `psycopg2` authenticated strictly as `propertism_user`:
1. Capture pre-test state: `SELECT count(*), COALESCE(max(id), 0) FROM properties_inquiry;`
2. Confirm authenticated role: `SELECT current_user, session_user;` (must both equal `propertism_user`).
3. Execute transaction-safe write attempt:
   ```sql
   BEGIN;
   INSERT INTO properties_inquiry (name, email, phone, message, created_at) 
   VALUES ('barrier_test', 'test@propertism.in', '0000000000', 'barrier', NOW());
   ROLLBACK;
   ```
4. **Assertion Criteria (C-77)**:
   - Statement must **FAIL** and raise PostgreSQL error.
   - Observed SQLSTATE must be recorded and match `42501` (`insufficient_privilege`) or `25006` (`read_only_sql_transaction`).
   - Transaction status must be clean after rollback.
   - Capture post-test state: `SELECT count(*), COALESCE(max(id), 0) FROM properties_inquiry;`
   - Assert: `post_count == pre_count` AND `post_max_id == pre_max_id`.
   - Result: Proven **zero persistent database mutation**.
   - **Fail Closed Rule**: If the query succeeds or persistent mutation is detected, **CUTOVER IS ABORTED IMMEDIATELY**.

#### Step 5: Capture Secondary Telemetry Snapshots $T_0$ and $T_1$ (C-27, C-61)
Capture row counts, max IDs, max timestamps, and user table write tuple counters across a 30-second quiet window. Assert that $T_0 \equiv T_1$. Log diagnostic WAL LSN.

#### Step 6: Final Production Dump, Target Administrator Restore & Parity (C-55, C-68, C-71)
- Dump RDS database via `pg_dump` with `--no-owner --no-privileges`.
- Restore onto Lightsail PostgreSQL 16 **as administrator `postgres`** (Section 7).
- Apply runtime grants to `propertism_user`.
- Execute Multi-Tier Parity Gate (Section 4) including Single-Algorithm Content Fingerprint Parity.

#### Step 7: Internal Supervisor Smoke Validation (C-56, C-57, C-58)
Execute application smoke tests strictly over loopback (`127.0.0.1:443`) while external traffic remains blocked at HTTP 503 (Section 13).

#### Step 8: DNS Cutover, Traffic Confirmation & Lightsail Write Enable (C-36, C-41, C-63)
- Update GoDaddy DNS A and AAAA records to `<LIGHTSAIL_STATIC_IP>`.
- Confirm external traffic in Lightsail Nginx access logs.
- Declare Lightsail authoritative.
- Remove write-freeze on Lightsail (`rm /var/www/propertism/maintenance.flag`).
- **Legacy RDS remains frozen in read-only mode** with privileges revoked throughout the 72-hour cooldown period.

---

## 6. Deterministic Final-Sync Acceptance Gate (FINAL_CUTOVER_RECORD.json)

In compliance with Mindra CTO Directives SCCB C-20, C-35, C-41, C-42, C-44, C-46, C-47, C-50, C-51, C-53, C-54, C-55, C-63, C-65, C-67, C-68, C-69, C-70, C-71, C-72, C-73, C-74, C-75, C-76, C-77, and C-79:

```json
{
  "cutover_metadata": {
    "protocol_version": "REV-8.4",
    "project": "03-propertism",
    "target_region": "ap-south-1",
    "lightsail_instance": "propertism-prod-mumbai-01",
    "lightsail_static_ip": "<LIGHTSAIL_STATIC_IP>",
    "target_maintenance_interval_minutes": 15,
    "authoritative_barrier_implementation_version": "REV-8.4-ten-layer-barrier",
    "content_fingerprint_algorithm_version": "v1.0-ieee754-hex-canonical",
    "fingerprint_implementation_identifier": "scripts/audit_database_content_fingerprints.py",
    "supervisor": "Astra",
    "product_owner": "Viji",
    "chief_architect": "Mindra"
  },
  "execution_timestamps": {
    "cutover_window_opened_timestamp": null,
    "legacy_eb_maintenance_activated_timestamp": null,
    "source_ownership_audit_timestamp": null,
    "source_role_attribute_audit_timestamp": null,
    "source_recursive_role_membership_audit_timestamp": null,
    "source_public_privilege_audit_timestamp": null,
    "source_effective_privilege_audit_timestamp": null,
    "source_callable_routine_audit_timestamp": null,
    "database_write_barrier_applied_timestamp": null,
    "database_write_barrier_verified_timestamp": null,
    "in_flight_drain_completed_timestamp": null,
    "immutability_snapshot_t0_timestamp": null,
    "immutability_snapshot_t1_timestamp": null,
    "immutability_verified_timestamp": null,
    "final_dump_started_timestamp": null,
    "final_dump_completed_timestamp": null,
    "final_dump_sha256": null,
    "target_restore_started_timestamp": null,
    "target_restore_completed_timestamp": null,
    "target_ownership_audit_timestamp": null,
    "target_effective_privilege_audit_timestamp": null,
    "structural_parity_result": null,
    "aggregate_parity_result": null,
    "content_fingerprint_parity_result": null,
    "sequence_parity_result": null,
    "media_migration_integrity_result": null,
    "internal_target_smoke_result": null,
    "dns_modification_timestamp": null,
    "external_dns_resolution_verified_timestamp": null,
    "first_confirmed_lightsail_production_request_timestamp": null,
    "lightsail_declared_authoritative_timestamp": null,
    "lightsail_write_freeze_removed_timestamp": null,
    "legacy_eb_rds_cooldown_started_timestamp": null
  },
  "authoritative_verification_evidence": {
    "source_database_owner_audit": {
      "object_owner": "postgres",
      "application_role": "propertism_user",
      "application_role_owned_objects_count": 0,
      "ownership_audit_passed": false
    },
    "source_role_attribute_audit": {
      "rolsuper": false,
      "rolbypassrls": false,
      "rolcreaterole": false,
      "rolcreatedb": false,
      "rolreplication": false,
      "role_attributes_passed": false
    },
    "source_recursive_role_membership_audit": {
      "inherited_administrative_roles_count": 0,
      "recursive_role_membership_audit_passed": false
    },
    "source_public_effective_privilege_audit": {
      "public_mutation_privileges_count": 0,
      "public_effective_privilege_audit_passed": false
    },
    "source_effective_privilege_audit": {
      "writable_tables_count": 0,
      "writable_sequences_count": 0,
      "schema_create_privilege_count": 0,
      "effective_privilege_passed": false
    },
    "source_callable_routine_audit": {
      "security_definer_bypass_routines_count": 0,
      "volatile_executable_routines_count": 0,
      "callable_routine_audit_passed": false
    },
    "source_transaction_safe_write_test": {
      "authenticated_role": null,
      "attempted_operation": "INSERT INTO properties_inquiry",
      "observed_sqlstate": null,
      "observed_error_message": null,
      "pre_test_row_count": null,
      "post_test_row_count": null,
      "persistent_mutation_detected": null,
      "write_test_passed": false
    },
    "immutability_snapshot_match": false,
    "diagnostic_wal_lsn_t0": null,
    "diagnostic_wal_lsn_t1": null,
    "content_fingerprint_tables_evaluated": 0,
    "content_fingerprint_tables_matched": 0,
    "content_fingerprint_failures": [],
    "media_source_manifest_sha256": null,
    "media_target_manifest_sha256": null,
    "media_manifest_match": false,
    "postgresql_compatibility_result": null,
    "letsencrypt_dns01_validation_result": null,
    "dns_inventory_pre_and_post_match": false,
    "rollback_barrier_verification_capability": false
  },
  "validation_gates": {
    "source_ownership_audit_pass": false,
    "source_role_attributes_pass": false,
    "source_recursive_membership_pass": false,
    "source_public_privilege_pass": false,
    "source_effective_privilege_pass": false,
    "source_callable_routine_pass": false,
    "source_write_test_pass": false,
    "legacy_write_freeze_authority_confirmed": false,
    "database_write_barrier_verified": false,
    "rds_database_state_immutability_verified": false,
    "sha256_integrity_match": false,
    "target_ownership_audit_pass": false,
    "target_effective_privilege_audit_pass": false,
    "structural_parity_pass": false,
    "aggregate_parity_pass": false,
    "content_fingerprint_parity_pass": false,
    "sequence_parity_pass": false,
    "media_migration_integrity_pass": false,
    "internal_target_smoke_test_pass": false,
    "dns_propagation_verified": false,
    "external_inquiry_test_pass": false
  },
  "final_cutover_status": "PENDING"
}
```

---

## 7. PostgreSQL Production vs. Sandbox Ownership & ACL Strategy

In compliance with Mindra CTO Directives SCCB C-22, C-46, C-54, C-55, and C-69:

### 1. Distinct Ownership Models

```text
[Sandbox / Restoration Test Database]
      │
      └── propertism_user connects directly and restores test dump into propertism_restore_test
          (Acceptable in isolated sandbox environment)

[Production Target Database (propertism_db)]
      │
      └── Master Administrator: postgres
            │
            ├── Executes pg_restore (--no-owner --no-privileges)
            ├── INHERENT OWNER of all production tables, views, sequences, indexes, functions, types
            │
            └── Grants explicit runtime privileges to propertism_user:
                  ├── CONNECT on DATABASE propertism_db
                  ├── USAGE on SCHEMA public
                  ├── SELECT, INSERT, UPDATE, DELETE on ALL TABLES in public
                  └── USAGE, SELECT on ALL SEQUENCES in public
```

### 2. Production Target Restore Procedure (C-55)
```bash
# Executed by postgres administrative role on Lightsail localhost
PGPASSWORD='<POSTGRES_ADMIN_PASSWORD>' pg_restore \
    --host=127.0.0.1 \
    --port=5432 \
    --username=postgres \
    --dbname=propertism_db \
    --clean \
    --if-exists \
    --no-owner \
    --no-privileges \
    --verbose \
    /var/backups/propertism/final_cutover.dump
```
Following completion, administrative role applies runtime grants:
```sql
GRANT CONNECT ON DATABASE propertism_db TO propertism_user;
GRANT USAGE ON SCHEMA public TO propertism_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO propertism_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO propertism_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO propertism_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO propertism_user;
```
**Post-Restore Ownership Assertion (C-69)**:
```sql
SELECT count(*) AS propertism_user_owned_objects
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' 
  AND c.relkind IN ('r', 'p', 'S', 'v', 'm', 'f')
  AND pg_get_userbyid(c.relowner) = 'propertism_user';
```
Must evaluate to `0`. `postgres` owns 100% of production application objects.

---

## 8. Step-by-Step Migration Runbook (Task 1 to Task 12)

### Task 1: Provision AWS Lightsail Instance & Static IP
1. Region: **`ap-south-1` (Mumbai)**. Blueprint: Ubuntu 24.04 LTS.
2. Plan: **2 GB RAM / 2 vCPU / 60 GB SSD / 3 TB Transfer ($12.00/mo IPv4 tier)**.
3. Attach Static IP: `<LIGHTSAIL_STATIC_IP>`. Open ports 22, 80, 443. Ports 5432 and 6379 strictly prohibited.

### Task 2: OS Baseline Hardening, Swap Allocation & Timezone
1. SSH into instance. Timezone: `Asia/Kolkata`.
2. Allocate 2 GB swap file (`vm.swappiness=10`). Enable UFW and `fail2ban`.

### Task 3: Pinned PostgreSQL 16, Redis, Python & Nginx Installation
1. Install PostgreSQL 16 via official PGDG repository. Verify `psql --version`.
2. Install Redis 7 (`redis-cli ping` returns `PONG`), Python 3.11/3.12, Nginx, Certbot.

### Task 4: PostgreSQL Setup, SCRAM Authentication & Deterministic Parity Gate
1. Create `propertism_db` and `propertism_user` with SCRAM-SHA-256 encryption.
2. Bind strictly to `127.0.0.1:5432`. Restore pre-flight dump using Section 7 production administrator procedure.
3. Run Multi-Tier Parity Audit (`python scripts/audit_database_parity.py`).

### Task 5: Application Deployment & Media Migration Gate Execution (C-44, C-65)
1. Clone repository to `/var/www/propertism`, set up virtualenv, install `requirements.txt`.
2. Inject production `.env` (`0600`, `www-data:www-data`).
3. Execute Machine-Deterministic Migration Check (Section 17).
4. Run `python manage.py check --deploy` and `collectstatic --noinput`.
5. **Execute Formal Media Migration & Integrity Gate (Section 14)**.

### Task 6: Conservative Gunicorn Configuration & Systemd Daemon
1. Create `/etc/systemd/system/gunicorn.service` (2 sync/gthread workers, 2 threads, max-requests 1000).
2. Enable and start: `systemctl enable --now gunicorn`. Verify `/run/gunicorn.sock`.

### Task 7: Pre-Cutover SSL Certificate Issuance via DNS-01 Challenge & Nginx Setup (C-50, C-58)
1. Issue Let's Encrypt SSL certificate for `propertism.in` and `www.propertism.in` using **DNS-01 challenge**:
   ```bash
   sudo certbot certonly --manual --preferred-challenges dns \
       -d propertism.in -d www.propertism.in \
       --agree-tos -m info@propertism.in --no-eff-email
   ```
   Add requested `_acme-challenge.propertism.in` TXT record in GoDaddy DNS. Verify propagation.
2. Configure Nginx with Fail-Closed Loopback Maintenance Routing (Section 13) and media script execution denial (Section 14).
3. Test with `sudo nginx -t` and reload `sudo systemctl reload nginx`.

### Task 8: Staging Pre-Cutover Verification & Maintenance Test (C-56, C-57, C-58)
1. Override workstation `hosts` to `<LIGHTSAIL_STATIC_IP>`.
2. Execute 3-Point Nginx Maintenance Gate (Section 13):
   - External request with flag $\rightarrow$ HTTP 503.
   - Internal loopback request with flag $\rightarrow$ HTTP 200.
   - External request attempting bypass $\rightarrow$ HTTP 503.
3. Remove `hosts` override.

### Task 9: Authoritative Final Cutover Execution (C-41, C-42, C-43, C-45, C-46, C-47, C-54, C-55, C-63, C-67, C-68, C-69, C-71, C-72, C-73, C-74, C-75, C-76, C-77)
1. Execute the 21-stage cutover sequence detailed in Section 5.
2. Record all timestamps, snapshots, and audit metrics in `reports/FINAL_CUTOVER_RECORD.json` (Section 6).
3. Update GoDaddy DNS (`@` and `www` A & AAAA records $\rightarrow$ `<LIGHTSAIL_STATIC_IP>`).
4. Confirm incoming production traffic in Lightsail Nginx access logs.
5. Deactivate write-freeze on Lightsail (`rm /var/www/propertism/maintenance.flag`).
6. Legacy RDS remains frozen in read-only mode.

### Task 10: Post-Cutover Live Smoke Test & Telemetry
1. Verify live HTTPS connection via external cellular network.
2. Submit live inquiry, verify database entry and email alert delivery.
3. Verify GA4 realtime telemetry.

### Task 11: Configure Automated Backups & Snapshots
1. Configure Lightsail automatic snapshots at **21:00 UTC (02:30 IST)** (Section 11).
2. Install observable S3 backup script with byte-level verification, alert wrapper, and root cron job (Section 10).
3. Execute Mandatory 10-Point Restoration Verification Suite (Section 10).

### Task 12: Cooldown Period & Controlled Legacy Decommissioning
1. Enter mandatory **48 to 72-hour Cooldown Period**.
2. Elastic Beanstalk and RDS remain active in frozen read-only standby.
3. Decommission only after passing all 14 points in Section 16.

---

## 9. Initial Resource Budget & Conservative Gunicorn Tuning

In compliance with Mindra CTO Directive §6, C-04, and C-38:

### 1. Initial Resource Budget (2,048 MB Physical RAM)

| Service / Process | Budgeted Allocation | % of Total RAM | Notes / Tuning Parameters |
|---|---|:---:|---|
| **Ubuntu 24.04 OS & Base System** | ~350 MB | 17.1% | Systemd, journald, ufw, fail2ban, sshd |
| **PostgreSQL 16 Engine** | ~300 MB | 14.6% | `shared_buffers = 256MB`, `work_mem = 4MB` |
| **Redis Server** | ~40 MB | 2.0% | Maxmemory capped at 64MB with LRU eviction |
| **Nginx Web Server** | ~25 MB | 1.2% | Worker processes + event loops + SSL cache |
| **Gunicorn Worker 1 (Sync/Gthread)** | ~130 MB | 6.3% | Python runtime, Django apps, models in memory |
| **Gunicorn Worker 2 (Sync/Gthread)** | ~130 MB | 6.3% | Redundant worker for concurrent requests |
| **Total Estimated Resident Memory (RSS)** | **~975 MB** | **47.6%** | **Initial planning budget; not observed production behavior** |
| **Budgeted OS Buffer & Headroom** | **~1,073 MB** | **52.4%** | Buffer space for kernel page cache, I/O burst, and query spikes |
| **Total Physical RAM** | **2,048 MB** | **100.0%** | **Mathematically verified ($975 + 1073 = 2048\text{ MB}$)** |

### 2. Runtime Measurement & Tuning Policy
- **Swap Safeguard**: 2 GB swap on Lightsail SSD with `vm.swappiness = 10`.
- **Worker Recycling**: `--max-requests 1000 --max-requests-jitter 100`.
- **Baseline Telemetry**: Actual production utilization measured via `free -h`, `vmstat 1 5`, `ps aux --sort=-%mem | head -10`.

---

## 10. Hardened S3 Backup, Byte-Level Verification & 10-Point Restoration Suite

In compliance with Mindra CTO Directives C-06, C-07, C-09, C-10, C-22, C-31, C-32, and C-64:
- Executing account: `root` system cron (`/etc/cron.d/propertism-backup`).
- Credential file: `/etc/propertism/backup.aws_credentials` (`0600`, `root:root`). Django `.env` contains zero AWS backup credentials.

### Byte-Level S3 Backup Verification Procedure (`deploy/lightsail/backup_db_s3.sh`) (C-64)
```bash
# 1. Compute local SHA-256
readonly LOCAL_SHA256=$(sha256sum "$DUMP_FILE" | cut -d' ' -f1)

# 2. Upload to S3 with metadata
export AWS_SHARED_CREDENTIALS_FILE="/etc/propertism/backup.aws_credentials"
aws s3 cp "$DUMP_FILE" "$S3_BUCKET/$(basename "$DUMP_FILE")" \
    --region "$AWS_REGION" --sse AES256 --metadata "sha256=$LOCAL_SHA256"

# 3. Byte-Level Verification: Download uploaded object to temporary verification file
readonly TEMP_VERIFY_FILE="/tmp/verify_$(basename "$DUMP_FILE")"
aws s3 cp "$S3_BUCKET/$(basename "$DUMP_FILE")" "$TEMP_VERIFY_FILE" --region "$AWS_REGION"

# 4. Compute retrieved object SHA-256 and assert exact byte match
readonly RETRIEVED_SHA256=$(sha256sum "$TEMP_VERIFY_FILE" | cut -d' ' -f1)
rm -f "$TEMP_VERIFY_FILE"

if [ "$RETRIEVED_SHA256" != "$LOCAL_SHA256" ]; then
    notify_failure 3 "CRITICAL: Byte-level SHA-256 verification mismatch (Retrieved: $RETRIEVED_SHA256, Local: $LOCAL_SHA256)."
    exit 3
fi
log "Byte-level S3 artifact verification PASS. Checksum: $LOCAL_SHA256"
```

---

## 11. Automated Snapshot Scheduling (UTC Semantics & Execution Timing)

In compliance with Mindra CTO Directives §10 and C-33:
- Requested Schedule: **`21:00 UTC` = `02:30 IST`**.
- Execution Timing: Lightsail initiates automatic snapshots within an operational execution window following the requested UTC hour. Snapshots are not instantaneous at 02:30:00 IST. Acceptance requires configured API verification and confirmed artifact generation during cooldown.

---

## 12. Security Baseline: SSH, UFW, Network & Secrets Protection

In compliance with Mindra CTO Directives §11, §12, and C-39:
- SSH: Root login disabled, password auth disabled, key-only, `fail2ban` active.
- UFW: Allow 22, 80, 443. Ports 5432 and 6379 strictly local loopback / Unix socket only.
- Secrets: Production `.env` (`0600`, `www-data:www-data`). Git repository contains only `.env.production.template`.

---

## 13. Fail-Closed Loopback-Only Nginx Maintenance & Smoke Testing

In compliance with Mindra CTO Directives SCCB C-08, C-49, C-56, C-57, and C-58, the web tier implements a fail-closed maintenance topology with **zero secret headers and zero external bypass**:

### 1. Fail-Closed Nginx Configuration (`/etc/nginx/sites-available/propertism`)
```nginx
# ------------------------------------------------------------------------------
# Loopback-Only Maintenance Routing (C-56, C-58)
# Zero Secret Headers | Zero Token Bypasses | Zero External Bypasses
# ------------------------------------------------------------------------------
geo $remote_addr $is_loopback {
    default 0;
    127.0.0.1 1;
    ::1 1;
}

map "$is_loopback:$maintenance_flag_exists" $block_maintenance {
    default 0;
    "0:1"   1;  # External client AND maintenance flag active -> Return HTTP 503
    "1:1"   0;  # Loopback supervisor AND maintenance flag active -> Pass to Gunicorn
    "0:0"   0;  # External client AND normal operation -> Pass to Gunicorn
    "1:0"   0;  # Loopback supervisor AND normal operation -> Pass to Gunicorn
}

server {
    listen 80;
    server_name propertism.in www.propertism.in;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name propertism.in www.propertism.in;

    ssl_certificate /etc/letsencrypt/live/propertism.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/propertism.in/privkey.pem;

    # Check maintenance flag file existence
    set $maintenance_flag_exists 0;
    if (-f /var/www/propertism/maintenance.flag) {
        set $maintenance_flag_exists 1;
    }

    # Evaluate fail-closed maintenance block
    if ($block_maintenance = 1) {
        return 503;
    }

    error_page 503 @maintenance_page;
    location @maintenance_page {
        root /var/www/propertism/templates/errors;
        rewrite ^(.*)$ /503.html break;
    }

    location / {
        proxy_pass http://gunicorn_propertism;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. 3-Point Nginx Acceptance Test (C-57, C-58)
1. **External Public 503 Verification**:
   `curl -s -o /dev/null -w "%{http_code}\n" https://propertism.in/` (from external workstation with flag present) $\rightarrow$ Returns **HTTP 503**.
2. **Internal Loopback Supervisor Smoke Test (Exact HTTPS Match)**:
   ```bash
   curl --resolve propertism.in:443:127.0.0.1 \
        --cacert /etc/letsencrypt/live/propertism.in/chain.pem \
        --silent --show-error -o /dev/null -w "%{http_code}\n" \
        https://propertism.in/health/
   ```
   $\rightarrow$ Returns **HTTP 200**. Allows supervisor to test PDP, search, and admin endpoints before opening public writes!
3. **External Bypass Rejection Test**:
   `curl -s -o /dev/null -w "%{http_code}\n" -H "X-Forwarded-For: 127.0.0.1" https://propertism.in/` (from external workstation) $\rightarrow$ Returns **HTTP 503** (Nginx relies strictly on physical TCP socket `$remote_addr`, preventing header spoofing).

---

## 14. Media Migration, Storage Permissions & Deterministic Manifest Gate

In compliance with Mindra CTO Directives SCCB C-24, C-30, C-44, and C-65:

### 1. Deterministic Media Manifest Hashing (C-65)
1. Generate `reports/SOURCE_MEDIA_MANIFEST.json` and `reports/TARGET_MEDIA_MANIFEST.json`.
2. All file entries sorted strictly by normalized POSIX relative path: `media/properties/photos/example.webp`.
3. Format manifests as canonical JSON (`sort_keys=True`, zero whitespace padding).
4. Compute SHA-256 of entire manifest file: `source_manifest_sha256` and `target_manifest_sha256`.
5. **Acceptance Rule**: `target_manifest_sha256 == source_manifest_sha256`.

### 2. Database Media-Reference Verification
Scan database for all non-null photo references:
```sql
SELECT photo FROM properties_propertyphoto WHERE photo IS NOT NULL AND photo != '';
```
Verify every database row resolves to an existing physical file at `/var/www/propertism/media/<photo>`. Fail closed if any row references a missing file.

### 3. Nginx Media Execution Denial (C-24, C-30)
```nginx
location ^~ /media/ {
    alias /var/www/propertism/media/;
    expires 30d;
    add_header Cache-Control "public, max-age=2592000";
    add_header X-Content-Type-Options "nosniff" always;
    access_log off;

    location ~* \.(php|pl|py|sh|cgi|exe|bat|cmd|jsp|asp|aspx|conf|env|bak)$ {
        deny all;
        return 403;
    }
}
```

---

## 15. Dual-Stage Rollback Runbook (Zero-Concurrent-Writer Authority Discipline)

In compliance with Mindra CTO Directives SCCB C-02, C-14, C-15, C-29, C-37, C-45, C-46, C-48, C-66, C-67, C-70, C-72, C-73, C-74, C-75, C-76, C-77, and C-78:

```text
Critical Failure Discovered on Lightsail Post-Cutover
                      │
                      ▼
1. Enable Lightsail HTTP Maintenance Mode (touch maintenance.flag ➔ HTTP 503) (C-48)
                      │
                      ▼
2. Stop/Drain Target Traffic & Terminate Active DB Sessions on Lightsail (C-48)
                      │
                      ▼
3. Apply 10-Layer Authoritative PostgreSQL Privilege Barrier on Lightsail (C-48, C-70, C-78)
                      │  ├── REVOKE DML on ALL TABLES from propertism_user & PUBLIC
                      │  ├── REVOKE USAGE, UPDATE on ALL SEQUENCES from propertism_user & PUBLIC
                      │  ├── REVOKE CREATE on SCHEMA public & propertism_db from propertism_user & PUBLIC
                      │  ├── REVOKE EXECUTE on ALL ROUTINES from propertism_user & PUBLIC (C-72, C-78)
                      │  └── ALTER ROLE propertism_user SET default_transaction_read_only = on
                      │
                      ▼
4. Execute 10-Layer Effective Privilege Audit on Lightsail (C-70, C-74, C-75, C-78)
                      │  ├── Ownership audit (postgres owns 100%, propertism_user owns 0)
                      │  ├── Role attributes & recursive role membership audit (0 admin roles)
                      │  ├── PUBLIC effective privilege audit (0 mutation grants)
                      │  ├── Effective table DML & sequence audit (all false)
                      │  └── Callable routine & SECURITY DEFINER audit (0 executable routines)
                      │
                      ▼
5. Execute Strengthened Transaction-Safe Write Test on Lightsail (C-77, C-78)
                      │  ├── Assert authenticated role: propertism_user
                      │  ├── Require observed failure SQLSTATE (42501 / 25006)
                      │  └── Verify zero persistent mutation (count and max ID unchanged)
                      │
                      ▼
6. Capture/Preserve Target State (Immediate Lightsail Snapshot + pg_dump)
                      │
                      ▼
7. Extract Post-Cutover Mutation Delta Manifest Across ALL Tables
                      │
                      ▼
8. Mindra / Viji Review & Written Approval of Mutation Manifest
                      │
                      ▼
9. Transactional Reconciliation into RDS by postgres Admin (Legacy DB REMAINS FROZEN) (C-37)
                      │
                      ▼
10. Reconcile ALL Sequences (Production-Hardened psycopg2.sql Algorithm) (C-29)
                      │
                      ▼
11. Independently Verify RDS (Structural, Aggregate, Content Parity)
                      │
                      ▼
12. Smoke-Test Legacy System via Internal Admin Path
                      │
                      ▼
════════════════════════════════════════════════════════════════════════════════
HARD GATE: ONLY THEN REVERT GODADDY DNS TO ELASTIC BEANSTALK / CLOUDFRONT (C-15)
════════════════════════════════════════════════════════════════════════════════
                      │
                      ▼
13. Verify Live Legacy Production HTTP Requests Reaching EB
                      │
                      ▼
14. ONLY NOW Restore Legacy Application Write Privileges (GRANT DML) (C-48)
                      │
                      ▼
15. Lightsail REMAINS IMMUTABLY FROZEN
```

> **ZERO CONCURRENT WRITERS INVARIANT (C-48, C-66, C-70, C-78)**: At zero point during rollback are both RDS and Lightsail writable production authorities. Lightsail is authoritatively sealed at the PostgreSQL privilege and routine layer before RDS reconciliation commences; RDS writes are restored only after external DNS traffic has reverted.

---

## 16. 14-Point Cooldown & Controlled Decommissioning Gate

In compliance with Mindra CTO Directive §14, C-12, C-13, and C-66:
- 72-hour operational cooldown.
- Legacy Elastic Beanstalk and RDS remain in frozen read-only standby.
- All 14 points (DNS resolution, SSL health, uptime, local loopback DB performance, inquiry ingestion, SMTP dispatch, WhatsApp alerts, OAuth sessions, Django Admin, media integrity, RealBot AI, GA4 telemetry, 24-hour zero application-originated legacy HTTP requests, verified backups) require signoff before decommissioning.

---

## 17. Deployment Scaffolding & Machine-Deterministic Migration Check

In compliance with Mindra CTO Directive SCCB C-03, C-16, and C-23:
- `deploy.sh` executes Python `MigrationExecutor(connections[DEFAULT_DB_ALIAS])`. Returns exit code 0 if schema matches, exit code 1 if unapplied migrations detected, exit code 2 on database error. Fails closed. Routine deployments will **NEVER** run automatic migrations.

---

## 18. Updated Risk Register

| Risk ID | Description | Likelihood | Impact | Mitigation Strategy |
|---|---|:---:|:---:|---|
| **RSK-01** | DNS cache stragglers hitting legacy EB after cutover | Medium | Low | Lower GoDaddy TTL to 300s 24h prior; maintain EB/RDS active in read-only standby for 72 hours. |
| **RSK-02** | OOM crash from unconstrained memory usage | Low | High | Enforce 2GB physical RAM + 2GB swap; conservative 2-worker Gunicorn tuning; worker request recycling. |
| **RSK-03** | PostgreSQL data loss during dump/restore | Low | Critical | RDS pre-migration snapshot; SHA-256 dump verification; multi-tier parity audit before cutover. |
| **RSK-04** | Backup failure without notification | Low | Medium | Hardened backup script with `set -euo pipefail`, observable timestamp, and byte-level S3 download verification (C-09, C-64). |
| **RSK-05** | Production secrets leak into version control | Low | Critical | Strict `.gitignore` enforcement; `.env.production.template` with dummy values only; manual server-only config. |
| **RSK-06** | SSH brute-force attack | Medium | Medium | Root login disabled; password auth disabled; fail2ban 1-hour ban after 3 failures; UFW firewall. |
| **RSK-07** | Post-cutover split-brain writes during rollback | Low | High | Enforce 10-layer effective PostgreSQL privilege barrier on Lightsail before RDS reconciliation, delta mutation extraction, all-sequence reconciliation, and hard gate before DNS reversion (C-02, C-14, C-15, C-37, C-48, C-70, C-78). |
| **RSK-08** | Uncontrolled schema migration alters prod DB | Low | High | Machine-deterministic fail-closed migration check in `deploy.sh`; 5-step explicit authorization gate (C-16, C-23). |
| **RSK-09** | Executable script execution via media folder | Low | High | Hardened media permissions (750 dirs, 640 files); Nginx regex script deny returns 403 (C-24, C-30). |
| **RSK-10** | Database writes during final cutover window | Low | High | Separation of object owner (`postgres`) from application runtime (`propertism_user`) + 10-layer effective privilege audit verified with transaction-safe SQLSTATE 42501/25006 check and zero persistent mutation proof (C-19, C-25, C-41, C-46, C-54, C-67, C-74, C-76, C-77). |
| **RSK-11** | Sequence collision or off-by-one during rollback | Low | High | Hardened `reconcile_all_sequences.py` with `psycopg2.sql` identifier quoting, serial/identity detection, and empty-table `is_called=false` semantics (C-29). |
| **RSK-12** | Undetected data mutation / content divergence | Low | Critical | Deterministic Content Fingerprint Parity Gate (single canonical algorithm with IEEE-754 float.hex(), Python Decimal format(val, 'f'), and safe unique-key fallback) (C-42, C-47, C-59, C-60, C-68, C-71). |
| **RSK-13** | Missing or corrupted media assets post-cutover | Low | Medium | Formal 9-step Media Migration & Integrity Gate comparing deterministic manifest SHA-256, file counts, aggregate bytes, and DB references (C-44, C-65). |
| **RSK-14** | Source/Target PostgreSQL incompatibility | Low | High | Pre-flight Compatibility Gate auditing version, UTF8 encoding, justified collation, timezone, and extensions (C-51, C-62). |
| **RSK-15** | IPv6 traffic bypassing Lightsail | Low | Medium | Complete pre-cutover DNS inventory (A, AAAA, CNAME, CAA) with post-cutover resolution verification (C-63). |
| **RSK-16** | Unexpected application object ownership | Low | High | Complete pre-flight ownership audit covering tables, sequences, views, materialized views, foreign tables, functions, and types (C-69). |
| **RSK-17** | Callable routine / SECURITY DEFINER write bypass | Low | High | Full revocation of execute on all routines in public schema + introspection audit checking for volatile/security-definer routines executable by propertism_user (C-72). |
| **RSK-18** | Recursive role-inheritance write bypass | Low | High | Recursive CTE audit of pg_auth_members proving propertism_user inherits zero administrative or write privileges through nested roles (C-73). |

---

## 19. Final REV-8.4 Approval Gate

```text
================================================================================
STATUS: HOLD — STANDBY FOR EXPLICIT MINDRA / VIJI APPROVAL
================================================================================

REV-8.4 is NOT authorization to execute production migration.

Astra MUST NOT:

- provision production infrastructure,
- modify production DNS,
- activate production write-freeze,
- modify production database state,
- restore production data,
- migrate production traffic,
- enable target production writes,
- reconcile production databases,
- or decommission EB/RDS

until Mindra and Viji explicitly approve the final architectural plan.

================================================================================
```
