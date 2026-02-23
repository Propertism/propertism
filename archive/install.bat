@echo off
echo Installing Chennai Realtor Dependencies...
echo.

echo [1/4] Installing root dependencies...
call npm install
if %errorlevel% neq 0 goto error

echo.
echo [2/4] Installing web PWA dependencies...
cd realtor-web\uilayers
call npm install
if %errorlevel% neq 0 goto error
cd ..\..

echo.
echo [3/4] Installing mobile dependencies...
cd realtor-mobile
call npm install
if %errorlevel% neq 0 goto error
cd ..

echo.
echo [4/4] Installing Python dependencies...
cd realtor-web
call pip install -r requirements.txt
if %errorlevel% neq 0 goto error
cd ..

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. cd realtor-web
echo 2. python manage.py migrate
echo 3. python manage.py createsuperuser
echo 4. python manage.py runserver
echo.
echo Then in another terminal:
echo npm run dev
echo.
goto end

:error
echo.
echo ========================================
echo Installation Failed!
echo ========================================
echo Please check the error above.
pause
exit /b 1

:end
pause
