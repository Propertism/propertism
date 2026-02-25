#!/bin/bash

# Backup Verification Script for Propertism Realty Advisors LLP
# SCCB-48 Compliance
# Version: 1.0

BACKUP_DIR="/home/realtor/backups"
EMAIL="your-email@example.com"
TODAY=$(date +%Y%m%d)
LOG_FILE="/home/realtor/logs/backup_verification.log"

# Create log directory
mkdir -p /home/realtor/logs

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
    echo "$1"
}

# Function to send alert
send_alert() {
    echo "$1" | mail -s "ALERT: Backup Verification - Propertism" $EMAIL 2>/dev/null || echo "Email not configured"
}

log_message "=========================================="
log_message "Starting backup verification..."
log_message "=========================================="

ISSUES_FOUND=0

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    log_message "✗ ERROR: Backup directory does not exist!"
    send_alert "Backup directory missing on $(date)"
    exit 1
fi

# Check for today's database backup (PostgreSQL or SQLite)
if ls $BACKUP_DIR/db_${TODAY}*.sql 1> /dev/null 2>&1 || ls $BACKUP_DIR/db_sqlite_${TODAY}*.sqlite3 1> /dev/null 2>&1; then
    log_message "✓ Database backup found for today"
    
    # Check database backup size
    DB_FILE=$(ls -t $BACKUP_DIR/db_${TODAY}*.sql $BACKUP_DIR/db_sqlite_${TODAY}*.sqlite3 2>/dev/null | head -1)
    if [ -n "$DB_FILE" ]; then
        DB_SIZE=$(stat -f%z "$DB_FILE" 2>/dev/null || stat -c%s "$DB_FILE" 2>/dev/null)
        if [ "$DB_SIZE" -lt 1024 ]; then
            log_message "⚠ WARNING: Database backup is suspiciously small (< 1KB)"
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
        else
            DB_SIZE_HUMAN=$(du -h "$DB_FILE" | cut -f1)
            log_message "  Database backup size: $DB_SIZE_HUMAN"
        fi
    fi
else
    log_message "✗ ERROR: No database backup found for today!"
    send_alert "No database backup found for $(date)"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check for today's media backup
if ls $BACKUP_DIR/media_${TODAY}*.tar.gz 1> /dev/null 2>&1; then
    log_message "✓ Media backup found for today"
    
    # Check media backup size
    MEDIA_FILE=$(ls -t $BACKUP_DIR/media_${TODAY}*.tar.gz 2>/dev/null | head -1)
    if [ -n "$MEDIA_FILE" ]; then
        MEDIA_SIZE_HUMAN=$(du -h "$MEDIA_FILE" | cut -f1)
        log_message "  Media backup size: $MEDIA_SIZE_HUMAN"
    fi
else
    log_message "⚠ WARNING: No media backup found for today"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check for today's environment backup
if ls $BACKUP_DIR/env_${TODAY}*.backup 1> /dev/null 2>&1; then
    log_message "✓ Environment backup found for today"
else
    log_message "⚠ WARNING: No environment backup found for today"
fi

# Check total backup count
BACKUP_COUNT=$(ls -1 $BACKUP_DIR 2>/dev/null | wc -l)
log_message "Total backup files: $BACKUP_COUNT"

if [ "$BACKUP_COUNT" -lt 3 ]; then
    log_message "⚠ WARNING: Very few backup files found"
fi

# Check disk space
DISK_USAGE=$(df -h $BACKUP_DIR | tail -1 | awk '{print $5}' | sed 's/%//')
log_message "Backup disk usage: ${DISK_USAGE}%"

if [ "$DISK_USAGE" -gt 90 ]; then
    log_message "✗ ERROR: Backup disk is almost full (${DISK_USAGE}%)"
    send_alert "Backup disk almost full: ${DISK_USAGE}% on $(date)"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

log_message "=========================================="

if [ "$ISSUES_FOUND" -eq 0 ]; then
    log_message "✓ Backup verification passed"
    log_message "=========================================="
    exit 0
else
    log_message "✗ Backup verification found $ISSUES_FOUND issue(s)"
    log_message "=========================================="
    send_alert "Backup verification found $ISSUES_FOUND issue(s) on $(date)"
    exit 1
fi
