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

from django.core.management import call_command

print("--- STARTING DB SEEDING ---")

commands = [
    'seed_configurations',
    'seed_actions',
    'seed_rules',
    'seed_services',
    'seed_suggestions',
    'seed_responses',
]

for cmd in commands:
    print(f"Running: {cmd}")
    try:
        call_command(cmd)
        print(f"Completed: {cmd}")
    except Exception as e:
        print(f"Error running {cmd}: {e}")

# Run Indexing
print("\\nRunning Knowledge Indexer...")
try:
    from chat.indexer import WebsiteContentIndexer, DocumentIndexer
    w_res = WebsiteContentIndexer().index_all()
    print(f"Website Content Indexer: indexed={w_res.indexed}, updated={w_res.updated}, skipped={w_res.skipped}, errors={len(w_res.errors)}")
    if w_res.errors:
        print("Indexer Errors:", w_res.errors)
        
    d_res = DocumentIndexer().index_all_documents()
    print(f"Document Indexer: indexed={d_res.indexed}, updated={d_res.updated}, skipped={d_res.skipped}, errors={len(d_res.errors)}")
    if d_res.errors:
        print("Document Indexer Errors:", d_res.errors)
except Exception as e:
    print(f"Error running indexers: {e}")

# Run Q&A Candidate Extraction
print("\\nRunning Website Conversational Q&A Candidate Extraction...")
try:
    from chat.knowledge_extractor import WebsiteConversationalExtractor, KnowledgeReconciliationEngine
    extractor = WebsiteConversationalExtractor()
    reconciler = KnowledgeReconciliationEngine()
    raw_candidates = extractor.extract_all_entities()
    candidates, report = reconciler.reconcile_all(raw_candidates)
    print(f"Extracted and reconciled {len(candidates)} candidates.")
    print("Reconciliation report:", report)
except Exception as e:
    print(f"Error running Q&A candidate extraction: {e}")

# Verification counts
print("\\n--- FINAL PROD DB COUNTS ---")
from chat.models import BusinessRule, ServiceProfile, KnowledgeArticle, KnowledgeDocument, ConfigurationItem, ExtractedKnowledgeCandidate
print("BusinessRule count:", BusinessRule.objects.count())
print("ServiceProfile count:", ServiceProfile.objects.count())
print("KnowledgeArticle count:", KnowledgeArticle.objects.count())
print("KnowledgeDocument count:", KnowledgeDocument.objects.count())
print("ConfigurationItem count:", ConfigurationItem.objects.count())
print("ExtractedKnowledgeCandidate count:", ExtractedKnowledgeCandidate.objects.count())
print("------------------------")
"""

b64_str = base64.b64encode(remote_script.encode('utf-8')).decode('utf-8')

# Decode the remote script on the server and run it
full_cmd = f"echo '{b64_str}' | base64 -d | sudo tee /tmp/seed_prod.py > /dev/null && sudo /var/app/venv/staging-LQM1lest/bin/python /tmp/seed_prod.py"

res = subprocess.run(["eb", "ssh", "-c", full_cmd], capture_output=True, text=True)
print("STDOUT:")
print(res.stdout)
print("STDERR:")
print(res.stderr)
print("RC:", res.returncode)
