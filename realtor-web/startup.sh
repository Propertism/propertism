#!/bin/bash
# Startup script for Render deployment
# Runs migrations and adds demo content before starting the server

echo "🚀 Starting Propertism deployment..."

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Add demo content
echo "📝 Adding demo content..."
python manage.py ensure_demo_content

# Start Gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn realtor_project.wsgi:application
