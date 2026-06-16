@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh -c "sudo -u webapp /var/app/venv/staging-LQM1lest/bin/python /var/app/current/manage.py shell -c 'from content.models import BlogPost; print(\"Published:\", BlogPost.objects.filter(is_published=True).count()); print(\"Total:\", BlogPost.objects.count())'" 2>&1
