#!/bin/bash

# Launch Monitoring Script for Propertism Realty Advisors LLP
# SCCB-49 Compliance
# Version: 1.0

DOMAIN="yourdomain.com"
LOG_FILE="/home/realtor/logs/launch_monitoring.log"
ALERT_EMAIL="your-email@example.com"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create log directory
mkdir -p /home/realtor/logs

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
    echo "$1"
}

# Function to send alert
send_alert() {
    echo "$1" | mail -s "ALERT: Launch Monitoring - Propertism" $ALERT_EMAIL 2>/dev/null || echo "Email not configured"
}

echo "=========================================="
echo "Launch Monitoring Check"
echo "=========================================="
echo ""

log_message "=========================================="
log_message "Starting launch monitoring check..."
log_message "=========================================="

ISSUES_FOUND=0

# Check 1: Website Accessibility
echo "Checking website accessibility..."
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" https://$DOMAIN)

if [ "$HTTP_CODE" == "200" ]; then
    log_message "✓ Website accessible (HTTP $HTTP_CODE)"
    echo -e "${GREEN}✓ Website accessible${NC}"
else
    log_message "✗ ERROR: Website not accessible (HTTP $HTTP_CODE)"
    echo -e "${RED}✗ Website not accessible (HTTP $HTTP_CODE)${NC}"
    send_alert "Website not accessible: HTTP $HTTP_CODE at $(date)"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check 2: Response Time
echo "Checking response time..."
RESPONSE_TIME=$(curl -o /dev/null -s -w "%{time_total}" https://$DOMAIN)
RESPONSE_MS=$(echo "$RESPONSE_TIME * 1000" | bc | cut -d'.' -f1)

if [ "$RESPONSE_MS" -lt 2000 ]; then
    log_message "✓ Response time: ${RESPONSE_MS}ms"
    echo -e "${GREEN}✓ Response time: ${RESPONSE_MS}ms${NC}"
elif [ "$RESPONSE_MS" -lt 5000 ]; then
    log_message "⚠ WARNING: Slow response time: ${RESPONSE_MS}ms"
    echo -e "${YELLOW}⚠ Slow response: ${RESPONSE_MS}ms${NC}"
else
    log_message "✗ ERROR: Very slow response: ${RESPONSE_MS}ms"
    echo -e "${RED}✗ Very slow response: ${RESPONSE_MS}ms${NC}"
    send_alert "Slow response time: ${RESPONSE_MS}ms at $(date)"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check 3: SSL Certificate
echo "Checking SSL certificate..."
SSL_EXPIRY=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)

if [ -n "$SSL_EXPIRY" ]; then
    log_message "✓ SSL certificate valid (Expires: $SSL_EXPIRY)"
    echo -e "${GREEN}✓ SSL certificate valid${NC}"
else
    log_message "✗ ERROR: SSL certificate issue"
    echo -e "${RED}✗ SSL certificate issue${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check 4: Service Status
echo "Checking services..."

if command -v systemctl &> /dev/null; then
    # Check Gunicorn
    if systemctl is-active --quiet gunicorn; then
        log_message "✓ Gunicorn running"
        echo -e "${GREEN}✓ Gunicorn running${NC}"
    else
        log_message "✗ ERROR: Gunicorn not running"
        echo -e "${RED}✗ Gunicorn not running${NC}"
        send_alert "Gunicorn service down at $(date)"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
    
    # Check Nginx
    if systemctl is-active --quiet nginx; then
        log_message "✓ Nginx running"
        echo -e "${GREEN}✓ Nginx running${NC}"
    else
        log_message "✗ ERROR: Nginx not running"
        echo -e "${RED}✗ Nginx not running${NC}"
        send_alert "Nginx service down at $(date)"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
fi

# Check 5: Disk Space
echo "Checking disk space..."
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -lt 80 ]; then
    log_message "✓ Disk usage: ${DISK_USAGE}%"
    echo -e "${GREEN}✓ Disk usage: ${DISK_USAGE}%${NC}"
elif [ "$DISK_USAGE" -lt 90 ]; then
    log_message "⚠ WARNING: Disk usage high: ${DISK_USAGE}%"
    echo -e "${YELLOW}⚠ Disk usage high: ${DISK_USAGE}%${NC}"
else
    log_message "✗ ERROR: Disk almost full: ${DISK_USAGE}%"
    echo -e "${RED}✗ Disk almost full: ${DISK_USAGE}%${NC}"
    send_alert "Disk almost full: ${DISK_USAGE}% at $(date)"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check 6: Memory Usage
echo "Checking memory usage..."
MEMORY_USAGE=$(free | grep Mem | awk '{print int($3/$2 * 100)}')

if [ "$MEMORY_USAGE" -lt 80 ]; then
    log_message "✓ Memory usage: ${MEMORY_USAGE}%"
    echo -e "${GREEN}✓ Memory usage: ${MEMORY_USAGE}%${NC}"
elif [ "$MEMORY_USAGE" -lt 90 ]; then
    log_message "⚠ WARNING: Memory usage high: ${MEMORY_USAGE}%"
    echo -e "${YELLOW}⚠ Memory usage high: ${MEMORY_USAGE}%${NC}"
else
    log_message "✗ ERROR: Memory critical: ${MEMORY_USAGE}%"
    echo -e "${RED}✗ Memory critical: ${MEMORY_USAGE}%${NC}"
    send_alert "Memory critical: ${MEMORY_USAGE}% at $(date)"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check 7: Recent Errors
echo "Checking error logs..."
if [ -f "/home/realtor/realtor-web/realtor-web/logs/django.log" ]; then
    ERROR_COUNT=$(grep -c "ERROR" /home/realtor/realtor-web/realtor-web/logs/django.log 2>/dev/null | tail -100 || echo "0")
    
    if [ "$ERROR_COUNT" -eq 0 ]; then
        log_message "✓ No recent errors"
        echo -e "${GREEN}✓ No recent errors${NC}"
    elif [ "$ERROR_COUNT" -lt 10 ]; then
        log_message "⚠ WARNING: $ERROR_COUNT recent errors"
        echo -e "${YELLOW}⚠ $ERROR_COUNT recent errors${NC}"
    else
        log_message "✗ ERROR: $ERROR_COUNT recent errors (high)"
        echo -e "${RED}✗ $ERROR_COUNT recent errors${NC}"
        send_alert "High error count: $ERROR_COUNT at $(date)"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
fi

echo ""
log_message "=========================================="

if [ "$ISSUES_FOUND" -eq 0 ]; then
    log_message "✓ All checks passed"
    echo -e "${GREEN}✓ All checks passed${NC}"
    echo "=========================================="
    exit 0
else
    log_message "✗ $ISSUES_FOUND issue(s) found"
    echo -e "${RED}✗ $ISSUES_FOUND issue(s) found${NC}"
    echo "=========================================="
    send_alert "Launch monitoring found $ISSUES_FOUND issue(s) at $(date)"
    exit 1
fi
