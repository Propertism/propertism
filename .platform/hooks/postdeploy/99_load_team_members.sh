#!/bin/bash
# One-time script to load team members into production database
# This will run after deployment

cd /var/app/current
source /var/app/venv/*/bin/activate

echo "🚀 Loading team members..."
python load_team_members.py

echo "✅ Team members load script completed"
