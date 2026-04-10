# Propertism AWS Redeploy 2026

This runbook assumes the repository root is the deploy source and the target stack is:

- Elastic Beanstalk single-instance in `us-east-1`
- Amazon RDS PostgreSQL in `us-east-1`
- GoDaddy-managed DNS

## Before AWS Commands

1. Configure AWS CLI credentials:
   - `aws configure`
   - Region: `us-east-1`
   - Output: `json`
2. Confirm the account identity:
   - `aws sts get-caller-identity`

## Required Environment Variables

Set these on Elastic Beanstalk before the first production deploy:

- `DEBUG=False`
- `DJANGO_SETTINGS_MODULE=realtor_project.settings`
- `DJANGO_SECRET_KEY=<strong secret>`
- `DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<db>`
- `DJANGO_ALLOWED_HOSTS=propertism.in,www.propertism.in,propertism-prod-2026.us-east-1.elasticbeanstalk.com`
- `CSRF_TRUSTED_ORIGINS=https://propertism.in,https://www.propertism.in,https://propertism-prod-2026.us-east-1.elasticbeanstalk.com`

Optional admin bootstrap variables:

- `ADMIN_USERNAME=<admin username>`
- `ADMIN_EMAIL=<admin email>`
- `ADMIN_PASSWORD=<admin password>`

## RDS First

1. Create a PostgreSQL instance in `us-east-1`
2. Wait until it is available
3. Capture:
   - endpoint hostname
   - database name
   - username
   - password
4. Build the final `DATABASE_URL`

## Elastic Beanstalk

1. Initialize the application if needed:
   - `eb init --region us-east-1`
2. Create the environment:
   - single instance
   - Python 3.11 on Amazon Linux 2023
   - environment name `propertism-prod-2026`
3. Apply runtime env vars:
   - `.\scripts\set-eb-runtime-production.ps1`
4. Build and deploy:
   - `.\scripts\deploy-eb-bundle.ps1`
5. Wait for green:
   - `.\scripts\wait-eb-environment.ps1`

## Data Migration

If the source of truth is the local SQLite database, migrate data using Django instead of `pg_dump`.

Suggested sequence:

1. Point local `.env` temporarily to the new PostgreSQL database with `DATABASE_URL`
2. Run:
   - `.\scripts\django.cmd migrate`
3. Export application data from SQLite with Django fixtures for the business-owned apps
4. Import that data into PostgreSQL
5. Validate admin content, properties, reviews, and media references before production cutover

## DNS

For GoDaddy-managed DNS:

- `www.propertism.in` should point to the EB environment CNAME
- root `propertism.in` should forward to `https://www.propertism.in`

Do not point the root record to a recycled EB instance IP.

## Notes

- The old SQLite-on-instance EB pattern has been removed from the deployment hooks
- The postdeploy hooks now assume PostgreSQL via `DATABASE_URL` or EB-provided DB env vars
- Media is still served from the application bundle unless/until S3 storage is wired into Django settings
