@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh propertism-prod-2026 -c "wc -l /tmp/seed_production_phase_b.py && tail -5 /tmp/seed_production_phase_b.py"
