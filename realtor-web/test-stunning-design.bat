@echo off
echo ========================================
echo Testing Stunning Design - Propertism
echo ========================================
echo.
echo Starting Django development server...
echo.
echo Open your browser and go to:
echo http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d "%~dp0"
python manage.py runserver
