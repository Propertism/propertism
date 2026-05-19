#!/bin/bash
set -euo pipefail

if [ -f /opt/elasticbeanstalk/deployment/env ]; then
    set -a
    . /opt/elasticbeanstalk/deployment/env || true
    set +a
fi

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-realtor_project.settings}"
export PYTHONPATH="/var/app/current:${PYTHONPATH:-}"

PYTHON_BIN=$(echo /var/app/venv/*/bin/python)

RECOVERY_STATE=$(
sudo -u webapp env \
    DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
    PYTHONPATH="$PYTHONPATH" \
    DATABASE_URL="${DATABASE_URL:-}" \
    POSTGRES_SSLMODE="${POSTGRES_SSLMODE:-}" \
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
        DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
        PYTHONPATH="$PYTHONPATH" \
        DATABASE_URL="${DATABASE_URL:-}" \
        POSTGRES_SSLMODE="${POSTGRES_SSLMODE:-}" \
        "$PYTHON_BIN" /var/app/current/manage.py bootstrap_admin_content
else
    echo "Production content DB already has records. Skipping bootstrap recovery."
fi
