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
git commit -m "SCCB-V2: Surgical kill S3 - force local storage override at final layer"
echo.

echo Pushing to origin main...
git push origin main
echo.

echo.
echo SCCB-V2 DEPLOYED!
echo Logs MUST show: SCCB STORAGE MODE: LOCAL (S3 DISABLED)
echo.
echo Done!
pause