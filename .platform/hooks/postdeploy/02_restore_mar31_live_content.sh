#!/bin/bash
DB_DIR="/var/app/data"
DB_FILE="$DB_DIR/db.sqlite3"
MARKER_FILE="$DB_DIR/.restore_mar31_live_content_v1.done"

if [ -f /opt/elasticbeanstalk/deployment/env ]; then
    set -a
    . /opt/elasticbeanstalk/deployment/env
    set +a
fi

export DB_PATH="${DB_PATH:-$DB_FILE}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-realtor_project.settings}"
export PYTHONPATH="/var/app/current:${PYTHONPATH:-}"

if [ -f "$MARKER_FILE" ]; then
    echo "March 31 live content restore already applied."
    exit 0
fi

sudo -u webapp env \
    DB_PATH="$DB_PATH" \
    DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
    PYTHONPATH="$PYTHONPATH" \
    /var/app/venv/*/bin/python /var/app/current/manage.py restore_mar31_live_content

if [ $? -eq 0 ]; then
    touch "$MARKER_FILE"
    chown webapp:webapp "$MARKER_FILE"
    chmod 664 "$MARKER_FILE"
fi
