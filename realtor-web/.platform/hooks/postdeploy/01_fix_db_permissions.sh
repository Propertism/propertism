#!/bin/bash
DB_DIR="/var/app/data"
DB_FILE="$DB_DIR/db.sqlite3"

mkdir -p $DB_DIR
chown -R webapp:webapp $DB_DIR
chmod -R 775 $DB_DIR

if [ -f "$DB_FILE" ]; then
    chown webapp:webapp $DB_FILE
    chmod 664 $DB_FILE
fi

# Run migrations first
sudo -u webapp /var/app/venv/*/bin/python /var/app/current/manage.py migrate --noinput || true

# Seed script disabled - content is managed via Django admin
# sudo -u webapp /var/app/venv/*/bin/python /var/app/current/manage.py seed_v2_content || true
