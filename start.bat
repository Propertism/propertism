@echo off
echo ========================================
echo   Propertism Django Server Starter
echo ========================================
echo.

REM Kill any existing Python processes
echo [1/2] Killing existing Python processes...
taskkill /F /IM python.exe /T 2>nul
if %errorlevel% equ 0 (
    echo    - Python processes terminated
) else (
    echo    - No Python processes found
)
echo.

REM Wait a moment for processes to fully terminate
timeout /t 2 /nobreak >nul

REM Start Django development server
echo [2/2] Starting Django development server...
echo    - Server will run on http://127.0.0.1:8001
echo    - Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

call .\scripts\django.cmd runserver 8001
