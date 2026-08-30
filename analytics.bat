@echo off
REM Propertism GA4 Analytics CLI Launcher
cd /d "%~dp0"
"C:\Users\vijay\AppData\Local\Programs\Python\Python311\python.exe" scripts\get_analytics.py %*
if errorlevel 1 pause
