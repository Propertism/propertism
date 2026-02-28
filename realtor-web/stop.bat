@echo off
echo ========================================
echo Stopping Propertism Servers
echo ========================================
echo.

echo Stopping Django backend...
taskkill /F /IM python.exe /T 2>nul

echo Stopping React dev server...
taskkill /F /IM node.exe /T 2>nul

echo Closing CMD windows...
for /f "skip=1 tokens=1" %%i in ('wmic process where "name='cmd.exe' and ProcessId!=%~1" get ProcessId') do (
    if not "%%i"=="%~1" taskkill /F /PID %%i 2>nul
)

echo.
echo ========================================
echo All servers stopped!
echo ========================================
echo.
pause
