@echo off
setlocal
echo.
echo ========================================
echo  PROPERTISM -- COMMIT + PUSH
echo ========================================
echo.

echo Running collectstatic...
set "COLLECTSTATIC_RAN=0"
where python >nul 2>&1
if not errorlevel 1 (
    python manage.py collectstatic --noinput
    if errorlevel 1 (
        echo.
        echo collectstatic failed. Aborting before commit.
        echo.
        exit /b 1
    )
    set "COLLECTSTATIC_RAN=1"
) else (
    where py >nul 2>&1
    if not errorlevel 1 (
        py manage.py collectstatic --noinput
        if errorlevel 1 (
            echo.
            echo collectstatic failed. Aborting before commit.
            echo.
            exit /b 1
        )
        set "COLLECTSTATIC_RAN=1"
    ) else (
        echo Python launcher not found. Skipping collectstatic.
    )
)

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
for %%F in (hero-*.png) do (
    if exist "%%F" git restore --staged -- "%%F" >nul 2>&1
)

echo.
echo Review staged changes:
git diff --cached --name-status

git diff --cached --quiet
if %errorlevel%==0 (
    echo.
    echo No staged changes found. Aborting.
    echo.
    exit /b 1
)

set /p MSG=Commit message (default: "Stabilize Mobile V4 Interface: Padding normalization and stacking hardening"): 
if "%MSG%"=="" set "MSG=Stabilize Mobile V4 Interface: Padding normalization and stacking hardening"

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
