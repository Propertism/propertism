#!/bin/bash
set -euo pipefail

# Seed the idempotent team-member fixture after deployment.

cd /var/app/current
source /var/app/venv/*/bin/activate

echo "🚀 Loading team members..."
python manage.py load_team_members

echo "✅ Team members load script completed"
