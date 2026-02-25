#!/bin/bash

# Deployment Script for Propertism Realty Advisors LLP
# SCCB-47 Compliance
# Version: 1.0

set -e  # Exit on error

echo "=========================================="
echo "Propertism Deployment Script"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in production
if [ "$DJANGO_ENV" != "production" ]; then
    echo -e "${RED}ERROR: DJANGO_ENV must be set to 'production'${NC}"
    exit 1
fi

# Check if DEBUG is False
if [ "$DEBUG" != "False" ]; then
    echo -e "${RED}ERROR: DEBUG must be set to 'False' in production${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Environment checks passed${NC}"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source ../venv/bin/activate || source venv/bin/activate

# Pull latest code
echo "Pulling latest code from Git..."
git pull origin main

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run tests
echo "Running tests..."
cd tests
python run_all_tests.py
cd ..

# Check deployment readiness
echo "Running deployment checks..."
python manage.py check --deploy

# Restart Gunicorn (if using systemd)
if command -v systemctl &> /dev/null; then
    echo "Restarting Gunicorn..."
    sudo systemctl restart gunicorn
fi

# Restart Nginx (if using systemd)
if command -v systemctl &> /dev/null; then
    echo "Restarting Nginx..."
    sudo systemctl restart nginx
fi

echo ""
echo -e "${GREEN}=========================================="
echo "Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Test the website: https://yourdomain.com"
echo "2. Check error logs: sudo journalctl -u gunicorn"
echo "3. Monitor for 24 hours"
echo ""
