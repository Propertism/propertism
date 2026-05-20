@echo off
setlocal

echo ========================================
echo   Propertism Elastic Beanstalk Deploy
echo ========================================
echo.
echo collectstatic is handled by scripts\build-eb-bundle.ps1
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0scripts\deploy-eb-bundle.ps1" %*
set EXIT_CODE=%ERRORLEVEL%

if %EXIT_CODE% neq 0 (
    echo.
    echo Deployment failed with exit code %EXIT_CODE%.
) else (
    echo.
    echo Deployment script completed successfully.
)

exit /b %EXIT_CODE%
