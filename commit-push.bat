@echo off
set "DEFAULT_MSG=feat(realbot): Dynamic emails, phone normalization, and chip matches (Session 73)"
set /p msg=Commit message [Default: %DEFAULT_MSG%]: 
if "%msg%"=="" set "msg=%DEFAULT_MSG%"
git add -A
git commit -m "%msg%"
git push
