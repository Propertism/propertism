#!/bin/bash

echo "Verifying Propertism root layout..."
echo ""

check_path() {
    if [ -e "$1" ]; then
        echo "  OK  $1"
    else
        echo "  MISSING  $1"
        exit 1
    fi
}

check_path "manage.py"
check_path "requirements.txt"
check_path "realtor_project/settings.py"
check_path "content"
check_path "properties"
check_path "uilayers"
check_path "static"
check_path "scripts/build-eb-bundle.ps1"
check_path ".session-tracker/SESSION_TRACKER.md"

echo ""
echo "Repository root is the current app source of truth."
echo "Run Django commands from this directory."
echo ""
