@echo off
echo.
echo ========================================
echo  PROPERTISM -- COMMIT + PUSH
echo ========================================
echo.

python manage.py collectstatic --noinput

echo.
echo Staging current local source of truth...
git add .

echo.
echo Removing local-only artifacts from staging...
if exist .playwright-mcp git restore --staged .playwright-mcp >nul 2>&1
if exist v4-darkmode-patch.css git restore --staged v4-darkmode-patch.css >nul 2>&1
if exist .agent git restore --staged .agent >nul 2>&1
if exist .session-tracker git restore --staged .session-tracker >nul 2>&1
if exist .tmp-test-media git restore --staged .tmp-test-media >nul 2>&1

echo.
echo Review staged changes:
git status --short

set /p MSG=Commit message: 
if "%MSG%"=="" (
    echo.
    echo Commit message is required. Aborting.
    echo.
    exit /b 1
)

git commit -m "%MSG%"
if errorlevel 1 (
    echo.
    echo Commit failed. Push skipped.
    echo.
    exit /b 1
)

git push origin main
if errorlevel 1 (
    echo.
    echo Push failed.
    echo.
    exit /b 1
)

echo.
echo ========================================
echo  DONE -- Deployed via GitHub Actions
echo ========================================
echo.
