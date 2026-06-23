@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh propertism-prod-2026 -c "cd /var/app/current && sudo -u webapp bash -c 'source /opt/elasticbeanstalk/deployment/env && export DJANGO_SETTINGS_MODULE=realtor_project.settings && /var/app/venv/staging-LQM1lest/bin/python manage.py seed_knowledge_hub_phase_b'"
