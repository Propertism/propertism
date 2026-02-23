@echo off
echo ========================================
echo Chennai Realtor - Production Build
echo ========================================
echo.

echo [Step 1/4] Building React Web App...
cd realtor-web\uilayers
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: React build failed!
    pause
    exit /b 1
)
echo ✓ React build complete
echo.

echo [Step 2/4] Collecting Django Static Files...
cd ..
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ERROR: Static files collection failed!
    pause
    exit /b 1
)
echo ✓ Static files collected
echo.

echo [Step 3/4] Running Django Migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Migrations failed!
    pause
    exit /b 1
)
echo ✓ Migrations complete
echo.

echo [Step 4/4] Running Django Tests...
python manage.py test --verbosity=2
if %errorlevel% neq 0 (
    echo WARNING: Some tests failed!
    echo Continue anyway? (Y/N)
    set /p continue=
    if /i not "%continue%"=="Y" exit /b 1
)
echo ✓ Tests passed
echo.

echo ========================================
echo Production Build Complete! ✓
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Test locally:
echo    python manage.py runserver
echo    Visit: http://localhost:8000/en/
echo.
echo 2. Deploy to production:
echo    - Set DEBUG=False in settings.py
echo    - Configure PostgreSQL database
echo    - Set ALLOWED_HOSTS
echo    - Use Gunicorn/uWSGI
echo    - Configure Nginx reverse proxy
echo    - Set up SSL certificate
echo.
echo 3. Mobile app configuration:
echo    Update API_BASE in realtor-mobile/src/services/api.ts
echo    to your production domain
echo.
echo ========================================
pause
