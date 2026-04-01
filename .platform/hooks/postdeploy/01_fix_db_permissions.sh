#!/bin/bash
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

mkdir -p "$DB_DIR"
chown -R webapp:webapp "$DB_DIR"
chmod -R 775 "$DB_DIR"

if [ -f "$DB_FILE" ]; then
    chown webapp:webapp "$DB_FILE"
    chmod 664 "$DB_FILE"
fi

# Run migrations against the same database file the web process uses.
sudo -u webapp env \
    DB_PATH="$DB_PATH" \
    DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
    PYTHONPATH="$PYTHONPATH" \
    /var/app/venv/*/bin/python /var/app/current/manage.py migrate --noinput || true

# Seed script disabled - content is managed via Django admin
# sudo -u webapp /var/app/venv/*/bin/python /var/app/current/manage.py seed_v2_content || true
