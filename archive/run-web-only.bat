@echo off
echo ========================================
echo Chennai Realtor - Development Mode
echo ========================================
echo.

REM Kill existing processes
echo Stopping any existing Django and Node processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul

REM Kill all CMD windows except the current one
echo Closing old CMD windows...
for /f "skip=1 tokens=1" %%i in ('wmic process where "name='cmd.exe' and ProcessId!=%~1" get ProcessId') do (
    if not "%%i"=="%~1" taskkill /F /PID %%i 2>nul
)
timeout /t 2 /nobreak > nul

echo.
echo Starting development servers...
echo.
echo [1] Django Backend (Port 8000)
echo     - REST APIs at /api/*
echo     - Web pages at /en/*
echo     - Admin at /en/admin/
echo.
echo [2] React Dev Server (Port 5173) [OPTIONAL]
echo     - Hot reload for React development
echo     - Use this when editing React code
echo.

REM Start Django Backend
start "Django Backend + APIs" cmd /k "cd realtor-web && python manage.py runserver"
timeout /t 5 /nobreak > nul

REM Start React Web PWA (Optional for development)
start "React Dev Server (Optional)" cmd /k "cd realtor-web\uilayers && npm run dev"
timeout /t 5 /nobreak > nul

REM Open in Chrome
echo.
echo Opening in Chrome...
timeout /t 3 /nobreak > nul
start chrome http://localhost:8000/en/

echo.
echo ========================================
echo Development Servers Running!
echo ========================================
echo.
echo PRODUCTION URL (Use this):
echo   http://localhost:8000/en/
echo.
echo DEVELOPMENT URL (React hot reload):
echo   http://localhost:5173/
echo.
echo API ENDPOINTS:
echo   http://localhost:8000/api/properties/
echo   http://localhost:8000/api/users/
echo   http://localhost:8000/api/search/
echo.
echo ADMIN PANEL:
echo   http://localhost:8000/en/admin/
echo.
echo MOBILE APP:
echo   Configure API base: http://localhost:8000/api
echo.
echo NOTE: Port 5173 is for development only.
echo       Production uses port 8000 for everything.
echo.
echo Press Ctrl+C in server windows to stop
echo ========================================
echo.
