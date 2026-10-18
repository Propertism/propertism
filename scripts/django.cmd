@echo off
setlocal

REM Priority 1: Project dedicated virtualenv (.venv)
if exist "%~dp0..\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0..\.venv\Scripts\python.exe"
    goto :run
)

REM Priority 2: Standard User Python 3.11 installation
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :run
)

REM Priority 3: Legacy C:\Python path
if exist "C:\Python\python.exe" (
    set "PYTHON_EXE=C:\Python\python.exe"
    if exist "C:\Python\django" set "PATH=C:\Python\django;%PATH%"
    goto :run
)

REM Priority 4: Fallback to PATH python
for %%X in (python.exe) do (set "PYTHON_EXE=%%~$PATH:X")
if defined PYTHON_EXE goto :run

echo [ERROR] No valid Python interpreter found.
echo Checked:
echo   - %~dp0..\.venv\Scripts\python.exe
echo   - %LOCALAPPDATA%\Programs\Python\Python311\python.exe
echo   - C:\Python\python.exe
exit /b 1

:run
if "%~1"=="" (
    "%PYTHON_EXE%" manage.py check
) else (
    "%PYTHON_EXE%" manage.py %*
)

exit /b %ERRORLEVEL%
