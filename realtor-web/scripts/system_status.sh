#!/bin/bash

# System Status Report for Propertism Realty Advisors LLP
# SCCB-48 Compliance
# Version: 1.0

echo "=========================================="
echo "Propertism System Status Report"
echo "=========================================="
echo ""

# System Info
echo "📊 System Information"
echo "----------------------------------------"
echo "Server: $(hostname)"
echo "Date: $(date)"
echo "Uptime: $(uptime -p)"
echo ""

# Disk Usage
echo "💾 Disk Usage"
echo "----------------------------------------"
df -h / | tail -1 | awk '{print "Root: " $3 " used / " $2 " total (" $5 " used)"}'
if [ -d "/home/realtor/backups" ]; then
    du -sh /home/realtor/backups 2>/dev/null | awk '{print "Backups: " $1}'
fi
echo ""

# Memory Usage
echo "🧠 Memory Usage"
echo "----------------------------------------"
free -h | grep Mem | awk '{print "Total: " $2 " | Used: " $3 " | Free: " $4}'
echo ""

# CPU Load
echo "⚡ CPU Load"
echo "----------------------------------------"
uptime | awk -F'load average:' '{print "Load Average:" $2}'
echo ""

# Service Status
echo "🔧 Service Status"
echo "----------------------------------------"

# Check Gunicorn
if command -v systemctl &> /dev/null; then
    if systemctl is-active --quiet gunicorn; then
        echo "Gunicorn: ✓ Running"
    else
        echo "Gunicorn: ✗ Not Running"
    fi
    
    # Check Nginx
    if systemctl is-active --quiet nginx; then
        echo "Nginx: ✓ Running"
    else
        echo "Nginx: ✗ Not Running"
    fi
    
    # Check PostgreSQL (if installed)
    if systemctl is-active --quiet postgresql; then
        echo "PostgreSQL: ✓ Running"
    fi
else
    echo "systemctl not available"
fi
echo ""

# Last Backup
echo "💼 Backup Status"
echo "----------------------------------------"
if [ -d "/home/realtor/backups" ]; then
    LAST_BACKUP=$(ls -t /home/realtor/backups/ 2>/dev/null | head -1)
    if [ -n "$LAST_BACKUP" ]; then
        BACKUP_DATE=$(stat -c %y "/home/realtor/backups/$LAST_BACKUP" 2>/dev/null | cut -d' ' -f1)
        echo "Last Backup: $LAST_BACKUP"
        echo "Date: $BACKUP_DATE"
    else
        echo "No backups found"
    fi
else
    echo "Backup directory not found"
fi
echo ""

# Recent Errors (if log exists)
echo "⚠️  Recent Errors (Last 24 hours)"
echo "----------------------------------------"
if [ -f "/home/realtor/realtor-web/realtor-web/logs/django.log" ]; then
    ERROR_COUNT=$(grep -c "ERROR" /home/realtor/realtor-web/realtor-web/logs/django.log 2>/dev/null || echo "0")
    echo "Django Errors: $ERROR_COUNT"
    
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "Recent errors:"
        tail -20 /home/realtor/realtor-web/realtor-web/logs/django.log | grep "ERROR" | tail -5
    fi
else
    echo "Log file not found"
fi
echo ""

# SSL Certificate Status (if certbot installed)
echo "🔒 SSL Certificate"
echo "----------------------------------------"
if command -v certbot &> /dev/null; then
    CERT_INFO=$(sudo certbot certificates 2>/dev/null | grep "Expiry Date" | head -1)
    if [ -n "$CERT_INFO" ]; then
        echo "$CERT_INFO"
    else
        echo "No certificates found"
    fi
else
    echo "Certbot not installed"
fi
echo ""

echo "=========================================="
echo "Report Generated: $(date)"
echo "=========================================="
