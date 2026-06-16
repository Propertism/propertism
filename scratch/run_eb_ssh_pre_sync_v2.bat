@echo off
cd /d d:\viji\viji-olivine\03rolledout\01propertism
eb ssh -c "sudo curl -s -o /tmp/pre_sync_check_v2.py https://olivine-site-673981388490.s3.amazonaws.com/pre_sync_check_v2.py && sudo -u webapp /var/app/venv/staging-LQM1lest/bin/python3 /tmp/pre_sync_check_v2.py" 2>&1
