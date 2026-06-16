@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh -c "sudo -u webapp bash -c 'cd /var/app/current && curl -s -o /tmp/pre_sync_check.py https://olivine-site-673981388490.s3.amazonaws.com/pre_sync_check.py && /var/app/venv/staging-LQM1lest/bin/python /tmp/pre_sync_check.py'" 2>&1
