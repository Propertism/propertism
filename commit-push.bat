@echo off

 
git add .
echo Committing...
git commit -m "SCCB-V2: Fix media serving for local storage - serve /media/ files in production"
git push origin main
echo.
