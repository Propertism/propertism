# Propertism Deployment Script
# Git push and AWS Elastic Beanstalk deployment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Propertism Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to realtor-web directory
Set-Location -Path "realtor-web"

# Step 1: Git Status Check
Write-Host "[1/5] Checking Git status..." -ForegroundColor Yellow
git status --short

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Git status check failed" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

Write-Host ""
$continue = Read-Host "Continue with deployment? (y/n)"
if ($continue -ne "y") {
    Write-Host "Deployment cancelled" -ForegroundColor Yellow
    Set-Location -Path ".."
    exit 0
}

# Step 2: Git Add
Write-Host ""
Write-Host "[2/5] Adding files to Git..." -ForegroundColor Yellow
git add .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Git add failed" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

# Step 3: Git Commit
Write-Host ""
$commitMessage = Read-Host "Enter commit message"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Mobile layout fixes - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}

Write-Host "[3/5] Committing changes..." -ForegroundColor Yellow
git commit -m "$commitMessage"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: No changes to commit or commit failed" -ForegroundColor Yellow
}

# Step 4: Git Push
Write-Host ""
Write-Host "[4/5] Pushing to remote repository..." -ForegroundColor Yellow
git push

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Git push failed" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

Write-Host "Git push successful!" -ForegroundColor Green

# Step 5: AWS EB Deploy
Write-Host ""
Write-Host "[5/5] Deploying to AWS Elastic Beanstalk..." -ForegroundColor Yellow
Write-Host "Running: eb deploy" -ForegroundColor Gray

eb deploy

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: AWS EB deployment failed" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

# Success
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Deployment Completed Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Git commit: $commitMessage" -ForegroundColor Cyan
Write-Host "AWS EB environment updated" -ForegroundColor Cyan
Write-Host ""

# Return to root directory
Set-Location -Path ".."

# Check deployment status
Write-Host "Checking deployment status..." -ForegroundColor Yellow
Set-Location -Path "realtor-web"
eb status
Set-Location -Path ".."

Write-Host ""
Write-Host "Deployment script completed!" -ForegroundColor Green
