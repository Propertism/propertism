@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh propertism-prod-2026 -c "sudo cp /home/ec2-user/seed_production_phase_b.py /tmp/seed_production_phase_b.py && sudo chown webapp:webapp /tmp/seed_production_phase_b.py && cd /var/app/current && sudo -u webapp bash -c 'DATABASE_URL=postgresql://propertismadmin:PropTami%%232026!Db@propertism-db-2026.ckzsuyw4azz2.us-east-1.rds.amazonaws.com:5432/propertismdb /var/app/venv/staging-LQM1lest/bin/python /tmp/seed_production_phase_b.py'"
