@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh propertism-prod-2026 -c "ls -la /var/app/current/content/management/commands/seed_knowledge_hub_phase_b.py && wc -l /var/app/current/content/management/commands/seed_knowledge_hub_phase_b.py"
