@echo off

echo Adding files...
git add .
echo.

echo Checking for changes...
git diff --cached --quiet
IF %ERRORLEVEL% EQU 0 (
    echo ❌ No changes to commit. Aborting.
    pause
    exit /b
)

echo Committing...
git commit -m "SCCB-V2: Fix media serving for local storage - serve /media/ files in production"
echo.

echo Pushing to origin main...
git push origin main
echo.

echo.
echo SCCB-V2 + MEDIA FIX DEPLOYED!
echo Images should now load without 404 errors
echo.
echo Done!
pause