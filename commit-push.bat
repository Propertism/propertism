@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo [Propertism] Committing and Pushing to origin/main
echo ========================================================
echo.

echo 1. Ensuring GitHub CLI is set to Propertism account...
call gh auth switch --user Propertism >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Could not switch account via gh auth switch. Proceeding with existing credentials.
) else (
    echo [OK] Active GitHub account set to Propertism.
)
echo.

echo 2. Checking working tree status...
for /f %%i in ('git status --porcelain 2^>nul') do (
    set HAS_CHANGES=1
    goto :has_changes
)
set HAS_CHANGES=0

:has_changes
if "%HAS_CHANGES%"=="1" (
    echo [INFO] Uncommitted changes detected.
    set "DEFAULT_MSG=fix(propertism): update platform files"
    set /p msg="Commit message [Default: !DEFAULT_MSG!]: "
    if "!msg!"=="" set "msg=!DEFAULT_MSG!"
    echo Staging changes...
    git add -A
    echo Committing changes...
    git commit -m "!msg!"
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Git commit failed.
        exit /b 1
    )
) else (
    echo [INFO] Working tree clean. No new changes to commit.
)

echo.
echo 3. Pushing to origin main...
git push origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Git push failed!
    exit /b 1
)

echo.
echo ========================================================
echo [SUCCESS] Pushed to origin/main successfully!
echo CI/CD pipeline triggered for Lightsail deployment.
echo ========================================================
endlocal
