@echo off
echo ========================================
echo Propertism - Django Only
echo ========================================
echo.

REM Kill existing processes
echo Stopping any existing servers...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak > nul

echo.
echo Starting Propertism (Django Backend)...
echo.

REM Start Django Backend
start "Propertism Backend" cmd /k "cd realtor-web && python manage.py runserver"
timeout /t 5 /nobreak > nul

REM Open in Chrome
echo Opening Propertism in Chrome...
timeout /t 3 /nobreak > nul
start chrome http://localhost:8000/en/

echo.
echo ========================================
echo Propertism is Running!
echo ========================================
echo.
echo Visit: http://localhost:8000/en/
echo.
echo Admin Panel: http://localhost:8000/en/admin/
echo Username: admin
echo Password: admin123
echo.
echo API: http://localhost:8000/api/properties/
echo.
echo Press Ctrl+C in the server window to stop
echo ========================================
echo.

