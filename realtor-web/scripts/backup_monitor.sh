#!/bin/bash

# Backup Monitoring Script for Propertism Realty Advisors LLP
# SCCB-48 Compliance
# Version: 1.0

# Configuration
BACKUP_DIR="/home/realtor/backups"
LOG_FILE="/home/realtor/logs/backup.log"
EMAIL="your-email@example.com"
DATE=$(date +%Y%m%d_%H%M%S)

# Create directories if they don't exist
mkdir -p $BACKUP_DIR
mkdir -p /home/realtor/logs

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
    echo "$1"
}

# Function to send alert
send_alert() {
    echo "$1" | mail -s "Backup Alert - Propertism" $EMAIL 2>/dev/null || echo "Email not configured"
}

log_message "=========================================="
log_message "Starting backup process..."
log_message "=========================================="

# Backup PostgreSQL database (if using PostgreSQL)
if command -v pg_dump &> /dev/null; then
    log_message "Backing up PostgreSQL database..."
    if pg_dump -U realtor_user realtor_db > $BACKUP_DIR/db_$DATE.sql 2>/dev/null; then
        log_message "✓ Database backup successful: db_$DATE.sql"
        DB_SIZE=$(du -h $BACKUP_DIR/db_$DATE.sql | cut -f1)
        log_message "  Database backup size: $DB_SIZE"
    else
        log_message "✗ ERROR: PostgreSQL backup failed!"
        send_alert "PostgreSQL backup failed on $(date)"
    fi
else
    log_message "PostgreSQL not found, skipping database backup"
fi

# Backup SQLite database (if using SQLite)
if [ -f "/home/realtor/realtor-web/realtor-web/db.sqlite3" ]; then
    log_message "Backing up SQLite database..."
    if cp /home/realtor/realtor-web/realtor-web/db.sqlite3 $BACKUP_DIR/db_sqlite_$DATE.sqlite3; then
        log_message "✓ SQLite backup successful: db_sqlite_$DATE.sqlite3"
        SQLITE_SIZE=$(du -h $BACKUP_DIR/db_sqlite_$DATE.sqlite3 | cut -f1)
        log_message "  SQLite backup size: $SQLITE_SIZE"
    else
        log_message "✗ ERROR: SQLite backup failed!"
        send_alert "SQLite backup failed on $(date)"
    fi
fi

# Backup media files
log_message "Backing up media files..."
if [ -d "/home/realtor/realtor-web/realtor-web/media" ]; then
    if tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/realtor/realtor-web/realtor-web/media/ 2>/dev/null; then
        log_message "✓ Media backup successful: media_$DATE.tar.gz"
        MEDIA_SIZE=$(du -h $BACKUP_DIR/media_$DATE.tar.gz | cut -f1)
        log_message "  Media backup size: $MEDIA_SIZE"
    else
        log_message "✗ ERROR: Media backup failed!"
        send_alert "Media backup failed on $(date)"
    fi
else
    log_message "Media directory not found, skipping media backup"
fi

# Backup environment file
log_message "Backing up environment file..."
if [ -f "/home/realtor/realtor-web/realtor-web/.env" ]; then
    if cp /home/realtor/realtor-web/realtor-web/.env $BACKUP_DIR/env_$DATE.backup; then
        log_message "✓ Environment file backed up"
    else
        log_message "✗ ERROR: Environment file backup failed!"
    fi
else
    log_message "Environment file not found, skipping"
fi

# Remove backups older than 7 days
log_message "Cleaning up old backups (>7 days)..."
DELETED_COUNT=$(find $BACKUP_DIR -type f -mtime +7 -delete -print | wc -l)
log_message "✓ Removed $DELETED_COUNT old backup files"

# Calculate total backup size
TOTAL_SIZE=$(du -sh $BACKUP_DIR 2>/dev/null | cut -f1)
log_message "Total backup directory size: $TOTAL_SIZE"

# Count backup files
BACKUP_COUNT=$(ls -1 $BACKUP_DIR | wc -l)
log_message "Total backup files: $BACKUP_COUNT"

log_message "=========================================="
log_message "Backup process completed successfully"
log_message "=========================================="

# Optional: Send success notification
# send_alert "Backup completed successfully on $(date). Total size: $TOTAL_SIZE"

exit 0
