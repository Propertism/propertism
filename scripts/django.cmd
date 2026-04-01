@echo off
setlocal

set "PYTHON_HOME=C:\Python"
set "PYTHON_EXE=%PYTHON_HOME%\python.exe"
set "PYTHON_DLL_DIR=%PYTHON_HOME%\django"

if not exist "%PYTHON_EXE%" (
    echo Expected Python interpreter was not found at %PYTHON_EXE%.
    exit /b 1
)

if not exist "%PYTHON_DLL_DIR%" (
    echo Expected Python DLL directory was not found at %PYTHON_DLL_DIR%.
    exit /b 1
)

set "PATH=%PYTHON_DLL_DIR%;%PATH%"

if "%~1"=="" (
    "%PYTHON_EXE%" manage.py check
) else (
    "%PYTHON_EXE%" manage.py %*
)

exit /b %ERRORLEVEL%
