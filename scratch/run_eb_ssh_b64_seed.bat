@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
type scratch\seed_production_phase_b.b64 | eb ssh propertism-prod-2026 -c "cd /var/app/current && sudo -u webapp bash -c 'base64 -d > /tmp/seed_production_phase_b.py && DATABASE_URL=postgresql://propertismadmin:PropTami%%232026!Db@propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com:5432/propertismdb /var/app/venv/staging-LQM1lest/bin/python /tmp/seed_production_phase_b.py'"
