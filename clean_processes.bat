@echo off
title Process Cleanup Utility
color 0B

:: ============================================================
:: clean_processes.bat
:: Identifies and closes unnecessary/running processes
:: that consume system resources unnecessarily.
:: 
:: Usage: Double-click or run from command prompt.
::        Run as Administrator for best results.
:: ============================================================

setlocal enabledelayedexpansion

echo ============================================
echo   Process Cleanup Utility
echo   Running on: %computername%
echo   Date: %date% %time%
echo ============================================
echo.

:: -------------------------------------------------------
:: Check if running as Administrator
:: -------------------------------------------------------
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Not running as Administrator.
    echo           Some processes may not be closable.
    echo           Right-click and select "Run as administrator"
    echo           for full effectiveness.
    echo.
)

:: -------------------------------------------------------
:: Define safe-to-close processes (non-critical)
:: These are user-space apps that are typically safe to kill
:: -------------------------------------------------------
set "SAFE_PROCESSES=chrome.exe firefox.exe msedge.exe brave.exe opera.exe"
set "SAFE_PROCESSES=%SAFE_PROCESSES% slack.exe discord.exe teams.exe zoom.exe skype.exe"
set "SAFE_PROCESSES=%SAFE_PROCESSES% spotify.exe iTunes.exe"
set "SAFE_PROCESSES=%SAFE_PROCESSES% notepad++.exe sublime_text.exe code.exe atom.exe"
set "SAFE_PROCESSES=%SAFE_PROCESSES% thunderbird.exe outlook.exe"
set "SAFE_PROCESSES=%SAFE_PROCESSES% vlc.exe mpc-hc.exe"
set "SAFE_PROCESSES=%SAFE_PROCESSES% steam.exe epicgameslauncher.exe"
set "SAFE_PROCESSES=%SAFE_PROCESSES% onedrive.exe dropbox.exe"
set "SAFE_PROCESSES=%SAFE_PROCESSES% java.exe javaw.exe python.exe node.exe"
set "SAFE_PROCESSES=%SAFE_PROCESSES% npm.cmd npx.cmd"

:: -------------------------------------------------------
:: Step 1: List all running processes
:: -------------------------------------------------------
echo [STEP 1] Scanning running processes...
echo.

set "TEMP_FILE=%temp%\process_list_%random%.txt"

:: Get process list - use TABLE format
tasklist /fo table /nh > "%TEMP_FILE%" 2>nul

if not exist "%TEMP_FILE%" (
    echo [ERROR] Could not retrieve process list.
    pause
    exit /b 1
)

echo All running processes:
echo ============================================
type "%TEMP_FILE%"
echo ============================================
echo.

:: Count total processes (lines that start with a letter)
set "COUNT=0"
for /f "tokens=1 delims= " %%a in (%TEMP_FILE%) do (
    set "FIRST=%%a"
    if not "!FIRST!"=="=" if not "!FIRST!"=="" set /a COUNT+=1
)
echo Total processes: %COUNT%
echo.

:: -------------------------------------------------------
:: Step 2: Identify and display unnecessary processes
:: -------------------------------------------------------
echo [STEP 2] Identifying unnecessary processes...
echo.

set "UNNECESSARY_COUNT=0"
echo The following processes appear to be non-critical and may be safe to close:
echo.

set "IDX=0"
for /f "tokens=1 delims= " %%a in (%TEMP_FILE%) do (
    set "PNAME=%%a"
    if not "!PNAME!"=="=" if not "!PNAME!"=="" (
        for %%p in (%SAFE_PROCESSES%) do (
            if /i "!PNAME!"=="%%p" (
                set /a IDX+=1
                set /a UNNECESSARY_COUNT+=1
                echo   [!UNNECESSARY_COUNT!] !PNAME!
            )
        )
    )
)

if %UNNECESSARY_COUNT% equ 0 (
    echo   No unnecessary processes detected.
) else (
    echo.
    echo Found %UNNECESSARY_COUNT% potentially unnecessary processes.
)
echo.

:: -------------------------------------------------------
:: Step 3: Ask user for action
:: -------------------------------------------------------
if %UNNECESSARY_COUNT% gtr 0 (
    echo [STEP 3] Action Required
    echo.
    echo Options:
    echo   1 - Close all identified unnecessary processes
    echo   2 - Skip - do nothing
    echo.
    set /p "CHOICE=Enter your choice (1/2): "
    echo.
    
    if "!CHOICE!"=="1" (
        echo Closing all identified unnecessary processes...
        echo.
        for /f "tokens=1 delims= " %%a in (%TEMP_FILE%) do (
            set "PNAME=%%a"
            if not "!PNAME!"=="=" if not "!PNAME!"=="" (
                for %%p in (%SAFE_PROCESSES%) do (
                    if /i "!PNAME!"=="%%p" (
                        echo   Closing !PNAME!...
                        taskkill /f /im !PNAME! >nul 2>&1
                        if !errorlevel! equ 0 (
                            echo     [OK] Successfully closed.
                        ) else (
                            echo     [FAILED] Could not close. Access denied or process already exited.
                        )
                    )
                )
            )
        )
        echo.
        echo [DONE] Cleanup completed.
    ) else (
        echo [SKIPPED] No processes were closed.
    )
) else (
    echo [STEP 3] No action needed - no unnecessary processes found.
)

:: -------------------------------------------------------
:: Step 4: Summary
:: -------------------------------------------------------
echo.
echo ============================================
echo   Cleanup Summary
echo ============================================
echo   Total processes scanned: %COUNT%
echo   Unnecessary processes found: %UNNECESSARY_COUNT%
echo   Status: Completed
echo ============================================
echo.

:: -------------------------------------------------------
:: Cleanup temp file
:: -------------------------------------------------------
if exist "%TEMP_FILE%" del "%TEMP_FILE%" >nul 2>&1

echo Press any key to exit...
pause >nul
exit /b 0
