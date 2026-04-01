#!/bin/bash
DB_DIR="/var/app/data"
DB_FILE="$DB_DIR/db.sqlite3"
MARKER_FILE="$DB_DIR/.reset_admin_password_20260401.done"

if [ -f /opt/elasticbeanstalk/deployment/env ]; then
    set -a
    . /opt/elasticbeanstalk/deployment/env
    set +a
fi

export DB_PATH="${DB_PATH:-$DB_FILE}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-realtor_project.settings}"
export PYTHONPATH="/var/app/current:${PYTHONPATH:-}"

if [ -f "$MARKER_FILE" ]; then
    echo "Admin password reset already applied on this instance."
    exit 0
fi

sudo -u webapp env \
    DB_PATH="$DB_PATH" \
    DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
    PYTHONPATH="$PYTHONPATH" \
    /var/app/venv/*/bin/python /var/app/current/manage.py createsu || true

sudo -u webapp env \
    DB_PATH="$DB_PATH" \
    DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
    PYTHONPATH="$PYTHONPATH" \
    /var/app/venv/*/bin/python /var/app/current/manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); user=User.objects.get(username='admin'); user.set_password('admin123'); user.is_staff=True; user.is_superuser=True; user.is_active=True; user.save(); print('Admin password reset complete')"

if [ $? -eq 0 ]; then
    touch "$MARKER_FILE"
    chown webapp:webapp "$MARKER_FILE"
    chmod 664 "$MARKER_FILE"
fi
