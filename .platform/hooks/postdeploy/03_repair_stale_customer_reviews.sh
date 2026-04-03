#!/bin/bash
set -euo pipefail

DB_DIR="/var/app/data"
DB_FILE="$DB_DIR/db.sqlite3"

if [ -f /opt/elasticbeanstalk/deployment/env ]; then
    set -a
    . /opt/elasticbeanstalk/deployment/env
    set +a
fi

export DB_PATH="${DB_PATH:-$DB_FILE}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-realtor_project.settings}"
export PYTHONPATH="/var/app/current:${PYTHONPATH:-}"

PYTHON_BIN=$(echo /var/app/venv/*/bin/python)

STALE_REVIEW_STATE=$(
sudo -u webapp env \
    DB_PATH="$DB_PATH" \
    DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
    PYTHONPATH="$PYTHONPATH" \
    "$PYTHON_BIN" -c "
import django

django.setup()

from content.models import CustomerReviewSection

section = CustomerReviewSection.objects.first()
description = (section.description if section else '') or ''
print('repair' if ('European Technical' in description or 'Dubai' in description) else 'healthy')
"
)

if [ "$STALE_REVIEW_STATE" = "repair" ]; then
    echo "Detected stale placeholder review content. Running forced bootstrap review repair."
    sudo -u webapp env \
        DB_PATH="$DB_PATH" \
        DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
        PYTHONPATH="$PYTHONPATH" \
        "$PYTHON_BIN" /var/app/current/manage.py bootstrap_admin_content --force
else
    echo "Customer review content looks healthy. Skipping stale review repair."
fi
