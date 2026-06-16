@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh -c "sudo bash -c 'source /opt/elasticbeanstalk/deployment/env && cd /var/app/current && sudo -u webapp /var/app/venv/staging-LQM1lest/bin/python manage.py shell -c \"from content.models import BlogPost; print(\"Published:\", BlogPost.objects.filter(is_published=True).count()); print(\"Total:\", BlogPost.objects.count())\"'" 2>&1
