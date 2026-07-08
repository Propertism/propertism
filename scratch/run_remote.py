import base64
import subprocess

# This script runs on the EC2 instance
remote_script = """
import os
import sys

# 1. Load EB environment variables
env_file = '/opt/elasticbeanstalk/deployment/env'
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                key, val = line.split('=', 1)
                os.environ[key] = val

# 2. Add application to path and setup Django
sys.path.insert(0, '/var/app/current')
import django
django.setup()

# 3. Import and print model counts
from chat.models import BusinessRule, ServiceProfile, KnowledgeArticle, KnowledgeDocument, ConfigurationItem
from content.models import BlogPost, CompanyInfo, Service, TeamMember
from properties.models import Property

print("--- DB COUNTS ---")
print("BusinessRule count:", BusinessRule.objects.count())
print("ServiceProfile count:", ServiceProfile.objects.count())
print("KnowledgeArticle count:", KnowledgeArticle.objects.count())
print("KnowledgeDocument count:", KnowledgeDocument.objects.count())
print("ConfigurationItem count:", ConfigurationItem.objects.count())
print("BlogPost count:", BlogPost.objects.count())
print("CompanyInfo count:", CompanyInfo.objects.count())
print("Service count:", Service.objects.count())
print("TeamMember count:", TeamMember.objects.count())
print("Property count:", Property.objects.count())
print("-----------------")
"""

b64_str = base64.b64encode(remote_script.encode('utf-8')).decode('utf-8')

# Decode the remote script on the server and run it
full_cmd = f"echo '{b64_str}' | base64 -d | sudo tee /tmp/check_prod.py > /dev/null && sudo /var/app/venv/staging-LQM1lest/bin/python /tmp/check_prod.py"

res = subprocess.run(["eb", "ssh", "-c", full_cmd], capture_output=True, text=True)
print("STDOUT:")
print(res.stdout)
print("STDERR:")
print(res.stderr)
print("RC:", res.returncode)
