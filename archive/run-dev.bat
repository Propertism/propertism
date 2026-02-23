@echo off
echo Starting Chennai Realtor Development Servers...
echo.
echo This will start:
echo - Django Backend (port 8000)
echo - React Web PWA (port 5173)
echo - Expo Mobile (port 19000)
echo.
echo Press Ctrl+C to stop all servers
echo.

start "Django Backend" cmd /k "cd realtor-web && python manage.py runserver"
timeout /t 3 /nobreak > nul

start "Web + Mobile" cmd /k "npm run dev"

echo.
echo Servers starting...
echo.
echo Access:
echo - Web: http://localhost:5173
echo - Admin: http://localhost:8000/admin
echo - API: http://localhost:8000/api
echo.
