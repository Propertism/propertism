@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh propertism-prod-2026 -c "ls -la /tmp/seed_production_phase_b.py && ls -la /home/ec2-user/seed_production_phase_b.py"
