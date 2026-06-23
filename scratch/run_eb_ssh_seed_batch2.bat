@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh propertism-prod-2026 -c "cd /var/app/current && sudo -u webapp /var/app/venv/staging-LQM1lest/bin/python scratch/seed_batch_2.py"
