@echo off
echo.
echo ========================================
echo  PROPERTISM -- COMMIT + PUSH
echo ========================================
echo.

python manage.py collectstatic --noinput

echo.
git add -A

set /p MSG=Commit message: 
git commit -m "%MSG%"
git push origin main

echo.
echo ========================================
echo  DONE -- Deployed via GitHub Actions
echo ========================================
echo.
