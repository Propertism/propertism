@echo off
echo ============================================
echo   OLIVINE UNIFIED PLATFORM STARTUP
echo ============================================
echo.
echo This script starts the complete ERP platform:
echo - Unified Backend (port 8000) - All modules
echo - Unified Frontend (Port 3000) - Single React shell
echo.
echo Modules included: Retail, HRM, CRM, FMS
echo ============================================
echo.

REM Check if we're in the right directory
if not exist "backend\manage.py" (
    echo ERROR: Please run this script from the olivine-platform root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [CLEANUP] Closing Chrome browser...
echo.
taskkill /F /IM chrome.exe 2>nul
echo Chrome closed.
timeout /t 1 /nobreak >nul

echo [CLEANUP] Clearing ports 8000 and 3000 if in use...
echo.

REM Kill any Python processes on port 8000 (Django)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Clearing port 8000...
    taskkill /F /PID %%a 2>nul
)

REM Kill any Node processes on port 3000 (Vite)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    echo Clearing port 3000...
    taskkill /F /PID %%a 2>nul
)

echo Ports cleared.
timeout /t 2 /nobreak >nul

echo.
echo ============================================
echo   STARTING UNIFIED BACKEND (port 8000)
echo ============================================
echo.

start "Olivine Unified Backend" cmd /k "cd backend && python manage.py runserver 8000"

echo Waiting 8 seconds for backend to initialize...
timeout /t 8 /nobreak

echo.
echo ============================================
echo   STARTING UNIFIED FRONTEND (Port 3000)
echo ============================================
echo.

start "Olivine Unified Frontend" cmd /k "cd frontend && npm run dev -- --port 3000"

echo Waiting 5 seconds for frontend to initialize...
timeout /t 5 /nobreak

echo.
echo ============================================
echo   UNIFIED PLATFORM STARTED SUCCESSFULLY
echo ============================================
echo.
echo   Backend API:     http://localhost:8000
echo   Django Admin:    http://localhost:8000/admin
echo   Frontend App:    http://localhost:3000
echo.
echo   Credentials:
echo   - Admin:         admin / admin123
echo   - BO Manager:    boadmin / boadmin123
echo   - POS Manager:   posadmin / posadmin123
echo.
echo ============================================
echo.

echo Opening browser in 3 seconds...
timeout /t 3 /nobreak

start chrome http://localhost:8000/admin/
timeout /t 1 /nobreak
start chrome http://localhost:3000

echo.
echo Platform is running. Check the separate windows for logs.
echo Press any key to exit this launcher window...
pause >nul
