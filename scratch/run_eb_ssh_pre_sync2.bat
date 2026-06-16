@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh -c "sudo -u webapp bash -c 'cd /var/app/current && source /opt/elasticbeanstalk/deployment/env && /var/app/venv/staging-LQM1lest/bin/python -c \"import os; os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"realtor_project.settings\"); import django; django.setup(); from content.models import BlogPost; print(\"Published:\", BlogPost.objects.filter(is_published=True).count()); print(\"Total:\", BlogPost.objects.count())\"'" 2>&1
