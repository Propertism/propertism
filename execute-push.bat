@echo off
setlocal

echo =========================================
echo EXECUTING GIT PUSH FOR SPAM PROTECTION FIX
echo =========================================
echo.
echo Deployment Time: 2026-09-09T07:12:08.265Z
echo.

echo 1. Checking GitHub CLI account status...
gh auth status
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: GitHub CLI not authenticated or wrong account
    echo Please ensure: gh auth switch --user Propertism
    exit /b 1
)

echo.
echo 2. Adding all changes for spam protection fix...
git add -A
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to add changes
    exit /b 1
)

echo.
echo 3. Committing spam protection changes...
echo Commit Message: "fix(spam): calibrate detection with international context awareness, reduce false positives after #292"
git commit -m "fix(spam): calibrate detection with international context awareness, reduce false positives after #292"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Commit failed
    echo Note: If no changes to commit, proceed with push
)

echo.
echo 4. Pushing to origin/main...
echo CI/CD pipeline will auto-deploy to Lightsail Mumbai
echo.
git push origin main
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Push failed
    exit /b 1
)

echo.
echo =========================================
echo ✅ GIT PUSH COMPLETED SUCCESSFULLY
echo =========================================
echo.
echo Next Steps:
echo 1. GitHub Actions will auto-deploy to Lightsail Mumbai
    echo 2. Monitor CI/CD pipeline at: https://github.com/Propertism/propertism/actions
echo 3. Check deployment logs on server
    echo 4. Verify inquiry validation after deployment

echo.
echo Deployment initiated: 2026-09-09T07:12:08.265Z
endlocal