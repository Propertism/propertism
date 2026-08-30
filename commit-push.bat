@echo off
set "DEFAULT_MSG=fix(inquiry): sync 249-country directory, harden CSRF settings, and purge root clutter"
set /p msg=Commit message [Default: %DEFAULT_MSG%]: 
if "%msg%"=="" set "msg=%DEFAULT_MSG%"
git add -A
git commit -m "%msg%"
git push origin main

