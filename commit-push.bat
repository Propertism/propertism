@echo off
set "DEFAULT_MSG=fix(seo): resolve GSC breadcrumb schema defects and sitemap redirect"
set /p msg=Commit message [Default: %DEFAULT_MSG%]: 
if "%msg%"=="" set "msg=%DEFAULT_MSG%"
git add -A
git commit -m "%msg%"
git push origin main

