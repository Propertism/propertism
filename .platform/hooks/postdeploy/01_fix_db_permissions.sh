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
MEDIA_ROOT="/var/app/current/media"

mkdir -p "$MEDIA_ROOT"
chown -R webapp:webapp "$MEDIA_ROOT"
chmod -R 775 "$MEDIA_ROOT"

if [ -n "${ADMIN_USERNAME:-}" ] && [ -n "${ADMIN_EMAIL:-}" ] && [ -n "${ADMIN_PASSWORD:-}" ]; then
    echo "ADMIN_* variables detected. Ensuring production superuser exists."
    sudo -u webapp env \
        DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
        PYTHONPATH="$PYTHONPATH" \
        DATABASE_URL="${DATABASE_URL:-}" \
        POSTGRES_SSLMODE="${POSTGRES_SSLMODE:-}" \
        ADMIN_USERNAME="${ADMIN_USERNAME}" \
        ADMIN_EMAIL="${ADMIN_EMAIL}" \
        ADMIN_PASSWORD="${ADMIN_PASSWORD}" \
        "$PYTHON_BIN" /var/app/current/scripts/create_or_reset_prod_superuser.py
else
    echo "ADMIN_* variables not set. Skipping superuser bootstrap."
fi
