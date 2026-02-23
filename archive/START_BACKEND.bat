@echo off
echo ..............................
echo    Starting Backend Server
echo ..............................
echo.

cd C:\00mindra\olivine-erp-platform\Backend

echo.
echo Starting server on port 8000...
echo.
echo .....................................................
echo   Backend running at: http://localhost:8000
echo .....................................................
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver 0.0.0.0:8000
