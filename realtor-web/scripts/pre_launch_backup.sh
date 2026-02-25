#!/bin/bash

# Pre-Launch Backup Script for Propertism Realty Advisors LLP
# SCCB-49 Compliance
# Version: 1.0

BACKUP_DIR="/home/realtor/pre-launch-backup"
DATE=$(date +%Y%m%d_%H%M%S)

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Pre-Launch Backup Script"
echo "=========================================="
echo ""

# Create backup directory
mkdir -p $BACKUP_DIR

echo "Creating pre-launch backup..."
echo ""

# Backup PostgreSQL database
if command -v pg_dump &> /dev/null; then
    echo "Backing up PostgreSQL database..."
    if pg_dump -U realtor_user realtor_db > $BACKUP_DIR/db_prelaunch_$DATE.sql 2>/dev/null; then
        DB_SIZE=$(du -h $BACKUP_DIR/db_prelaunch_$DATE.sql | cut -f1)
        echo -e "${GREEN}✓ Database backed up${NC} (Size: $DB_SIZE)"
    else
        echo -e "${RED}✗ PostgreSQL backup failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠ PostgreSQL not found, skipping${NC}"
fi

# Backup SQLite database
if [ -f "/home/realtor/realtor-web/realtor-web/db.sqlite3" ]; then
    echo "Backing up SQLite database..."
    if cp /home/realtor/realtor-web/realtor-web/db.sqlite3 $BACKUP_DIR/db_sqlite_prelaunch_$DATE.sqlite3; then
        SQLITE_SIZE=$(du -h $BACKUP_DIR/db_sqlite_prelaunch_$DATE.sqlite3 | cut -f1)
        echo -e "${GREEN}✓ SQLite backed up${NC} (Size: $SQLITE_SIZE)"
    else
        echo -e "${RED}✗ SQLite backup failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠ SQLite database not found, skipping${NC}"
fi

# Backup media files
if [ -d "/home/realtor/realtor-web/realtor-web/media" ]; then
    echo "Backing up media files..."
    if tar -czf $BACKUP_DIR/media_prelaunch_$DATE.tar.gz /home/realtor/realtor-web/realtor-web/media/ 2>/dev/null; then
        MEDIA_SIZE=$(du -h $BACKUP_DIR/media_prelaunch_$DATE.tar.gz | cut -f1)
        echo -e "${GREEN}✓ Media files backed up${NC} (Size: $MEDIA_SIZE)"
    else
        echo -e "${RED}✗ Media backup failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Media directory not found, skipping${NC}"
fi

# Backup environment file
if [ -f "/home/realtor/realtor-web/realtor-web/.env" ]; then
    echo "Backing up environment file..."
    if cp /home/realtor/realtor-web/realtor-web/.env $BACKUP_DIR/env_prelaunch_$DATE.backup; then
        echo -e "${GREEN}✓ Environment file backed up${NC}"
    else
        echo -e "${RED}✗ Environment backup failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Environment file not found, skipping${NC}"
fi

# Backup Nginx config
if [ -f "/etc/nginx/sites-available/realtor" ]; then
    echo "Backing up Nginx configuration..."
    if sudo cp /etc/nginx/sites-available/realtor $BACKUP_DIR/nginx_prelaunch_$DATE.conf 2>/dev/null; then
        echo -e "${GREEN}✓ Nginx config backed up${NC}"
    else
        echo -e "${YELLOW}⚠ Nginx config backup failed (may need sudo)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Nginx config not found, skipping${NC}"
fi

# Create backup manifest
cat > $BACKUP_DIR/MANIFEST.txt << EOF
Pre-Launch Backup Manifest
==========================

Backup Date: $(date)
Backup Location: $BACKUP_DIR

Files:
------
Database (PostgreSQL): db_prelaunch_$DATE.sql
Database (SQLite): db_sqlite_prelaunch_$DATE.sqlite3
Media Files: media_prelaunch_$DATE.tar.gz
Environment: env_prelaunch_$DATE.backup
Nginx Config: nginx_prelaunch_$DATE.conf

Verification:
-------------
Run: ls -lh $BACKUP_DIR

Restore Instructions:
--------------------
See GO_LIVE_EXECUTION_GUIDE.md - Section 9: Rollback Strategy

IMPORTANT: Store this backup off-server before launch!
EOF

echo -e "${GREEN}✓ Backup manifest created${NC}"
echo ""

# Display backup summary
echo "=========================================="
echo "Backup Summary"
echo "=========================================="
echo "Location: $BACKUP_DIR"
echo ""
ls -lh $BACKUP_DIR | tail -n +2
echo ""

TOTAL_SIZE=$(du -sh $BACKUP_DIR | cut -f1)
echo "Total Backup Size: $TOTAL_SIZE"
echo ""

echo -e "${GREEN}✓ Pre-launch backup complete${NC}"
echo ""
echo "NEXT STEPS:"
echo "1. Verify backup files exist"
echo "2. Upload to off-site storage (S3/Backblaze)"
echo "3. Test restore procedure (optional but recommended)"
echo ""
echo "=========================================="
