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

RECOVERY_STATE=$(
sudo -u webapp env \
    DB_PATH="$DB_PATH" \
    DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
    PYTHONPATH="$PYTHONPATH" \
    "$PYTHON_BIN" -c "
import django

django.setup()

from content.models import BlogPost, CustomerReviewSection
from properties.models import Property

needs_recovery = (
    Property.objects.count() == 0
    and CustomerReviewSection.objects.count() == 0
    and BlogPost.objects.count() == 0
)
print('recover' if needs_recovery else 'healthy')
"
)

if [ "$RECOVERY_STATE" = "recover" ]; then
    echo "Production content looks incomplete. Running bootstrap_admin_content recovery."
    sudo -u webapp env \
        DB_PATH="$DB_PATH" \
        DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
        PYTHONPATH="$PYTHONPATH" \
        "$PYTHON_BIN" /var/app/current/manage.py bootstrap_admin_content
else
    echo "Production content DB already has records. Skipping bootstrap recovery."
fi
