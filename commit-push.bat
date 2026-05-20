@echo off
set /p msg=Commit message:
git add -A
git commit -m "%msg%"
git push
