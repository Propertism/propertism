@echo off
echo ========================================
echo Clearing Django Cache and Restarting
echo ========================================
echo.

REM Kill Django server
echo Stopping Django server...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak > nul

REM Delete Python cache
echo Clearing Python cache...
cd realtor-web
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

echo.
echo Starting Django server...
start "Django Server" cmd /k "python manage.py runserver"

echo.
echo ========================================
echo Server restarted with fresh cache!
echo ========================================
echo.
echo Now refresh your browser with Ctrl+F5
echo.
pause
