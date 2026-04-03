#!/bin/bash
set -euo pipefail

if [ -f /opt/elasticbeanstalk/deployment/env ]; then
    set -a
    . /opt/elasticbeanstalk/deployment/env
    set +a
fi

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-realtor_project.settings}"
export PYTHONPATH="/var/app/current:${PYTHONPATH:-}"

STATIC_ROOT="/var/app/current/staticfiles"
PYTHON_BIN=$(echo /var/app/venv/*/bin/python)

mkdir -p "$STATIC_ROOT"
chown -R webapp:webapp "$STATIC_ROOT"
chmod 775 "$STATIC_ROOT"

sudo -u webapp env \
    DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
    PYTHONPATH="$PYTHONPATH" \
    "$PYTHON_BIN" /var/app/current/manage.py collectstatic --noinput --clear

chown -R webapp:webapp "$STATIC_ROOT"
find "$STATIC_ROOT" -type d -exec chmod 755 {} \;
find "$STATIC_ROOT" -type f -exec chmod 644 {} \;

if command -v restorecon >/dev/null 2>&1; then
    restorecon -RF "$STATIC_ROOT" || true
fi
