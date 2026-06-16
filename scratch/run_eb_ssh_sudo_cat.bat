@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh -c "sudo bash -c 'export $(cat /opt/elasticbeanstalk/deployment/env | grep -v \"^#\" | xargs) && cd /var/app/current && sudo -u webapp /var/app/venv/staging-LQM1lest/bin/python manage.py shell -c \"from content.models import BlogPost; p=BlogPost.objects.filter(is_published=True); print(\\\"Published:\\\", p.count()); [print(\\\"  \\\", s) for s in p.values_list(\\\"slug\\\", flat=True)]\"'" 2>&1
