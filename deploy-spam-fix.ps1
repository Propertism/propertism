# ====================================================
# DEPLOY SPAM DETECTION FIX - Inquiry #292+ False Positives
# Created: 2026-09-09 07:14 IST
# Urgency: Legitimate inquiries incorrectly flagged as spam
# ====================================================

Write-Host "🚀 DEPLOYING SPAM DETECTION FIX - " -NoNewline
Write-Host "CRITICAL URGENCY" -ForegroundColor Red -BackgroundColor Yellow
Write-Host "Issue: Legitimate inquiries after #292 incorrectly flagged as spam"
Write-Host "Current Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

# Step 1: Verify GitHub CLI is set to Propertism account (Governance Rule)
Write-Host "🔍 Step 1: Verifying GitHub CLI Account..." -ForegroundColor Cyan
$account = gh auth status 2>&1
if ($account -match "Logged in to github.com as Propertism") {
    Write-Host "✅ GitHub CLI is set to Propertism account" -ForegroundColor Green
} else {
    Write-Host "❌ GitHub CLI is NOT set to Propertism account" -ForegroundColor Red
    Write-Host "⚠️  Correcting account per governance rules..."
    gh auth switch --user Propertism
    $account = gh auth status 2>&1
    if ($account -match "Logged in to github.com as Propertism") {
        Write-Host "✅ GitHub CLI corrected to Propertism account" -ForegroundColor Green
    } else {
        Write-Host "❌ FAILED to set Propertism account" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Check current commit status
Write-Host ""
Write-Host "🔍 Step 2: Checking Commit Status..." -ForegroundColor Cyan
$status = git status --porcelain
if ($status) {
    Write-Host "📁 Files ready for commit:"
    Write-Host $status
    Write-Host ""
} else {
    Write-Host "⚠️  No changes to commit" -ForegroundColor Yellow
    exit 0
}

# Step 3: Add all spam detection fix files
Write-Host "🔍 Step 3: Adding Spam Detection Fix Files..." -ForegroundColor Cyan
git add properties/utils/lead_validation.py
git add realtor_project/settings.py
git add spam_monitoring/README.md

Write-Host "✅ Added: lead_validation.py (calibrated spam detection)"
Write-Host "✅ Added: settings.py (adjusted thresholds)"
Write-Host "✅ Added: spam_monitoring/README.md (monitoring dashboard)"

# Step 4: Create comprehensive commit
Write-Host ""
Write-Host "🔍 Step 4: Creating Commit..." -ForegroundColor Cyan
$commitMsg = @"
fix(spam): calibrate detection with international context awareness, reduce false positives after #292

## Root Cause Identified:
- Overly aggressive spam detection implemented 2026-09-04
- Legitimate international inquiries after #292 incorrectly flagged as spam

## Changes Made:
1. **Calibrated Cyrillic detection**: Only penalize if >50% content, max -40 (was -80)
2. **Fixed TLD penalties**: Only .ru/.su/.рф flagged, reduced penalty (was .xyz/.top/.work too)
3. **Added international context awareness**: Different validation for international vs Indian inquiries
4. **Adjusted thresholds**: Likely Spam threshold lowered to 30 (was 40)
5. **Enhanced logging**: Comprehensive validation decision tracking
6. **Created monitoring dashboard**: spam_monitoring/README.md

## Safety Features:
- Core bot protection remains intact (honeypot, rate limiting, CAPTCHA)
- Enhanced logging for monitoring decisions
- Emergency rollback procedures documented
- Context-aware validation reduces false positives

## Expected Results:
- Legitimate inquiries after #292 correctly classified
- International inquiries properly recognized with context
- Actual spam still filtered effectively
- Dashboard shows accurate classification (not "all spam after #292")

## Time Critical:
- Deployment: 2026-09-09 07:14 IST
- Monitoring: Immediate post-deployment verification
"@

git commit -m $commitMsg
if ($LASTEXITCODE -eq 0) {
    $commitHash = git log --oneline -1
    Write-Host "✅ Commit created: $commitHash" -ForegroundColor Green
} else {
    Write-Host "❌ Commit failed" -ForegroundColor Red
    exit 1
}

# Step 5: Push to trigger CI/CD deployment
Write-Host ""
Write-Host "🚀 Step 5: Pushing to Trigger CI/CD Deployment..." -ForegroundColor Cyan
Write-Host "⚠️  THIS WILL AUTO-DEPLOY TO PRODUCTION VIA GITHUB ACTIONS" -ForegroundColor Yellow
Write-Host ""

$pushResult = git push origin main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Push successful! CI/CD pipeline triggered" -ForegroundColor Green
    
    # Show deployment info
    Write-Host ""
    Write-Host "📊 DEPLOYMENT INFO:" -ForegroundColor Cyan
    Write-Host "• CI/CD Pipeline: https://github.com/Propertism/propertism/actions"
    Write-Host "• Deployment Target: Lightsail Mumbai (ap-south-1)"
    Write-Host "• Expected Completion: 5-10 minutes"
    Write-Host "• Monitoring: Check spam_monitoring/README.md for verification steps"
    
    # Show immediate monitoring steps
    Write-Host ""
    Write-Host "🔍 IMMEDIATE MONITORING STEPS:" -ForegroundColor Cyan
    Write-Host "1. Monitor CI/CD pipeline: https://github.com/Propertism/propertism/actions"
    Write-Host "2. Watch for first inquiry #293+ classification"
    Write-Host "3. Check server logs for validation decisions"
    Write-Host "4. Verify email notifications working for genuine inquiries"
    
} else {
    Write-Host "❌ Push failed: $pushResult" -ForegroundColor Red
    exit 1
}

# Step 6: Deployment completion message
Write-Host ""
Write-Host "=================================================="
Write-Host "✅ DEPLOYMENT INITIATED SUCCESSFULLY" -ForegroundColor Green
Write-Host "=================================================="
Write-Host ""
Write-Host "🕒 Deployment Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "📈 Monitor at: https://github.com/Propertism/propertism/actions"
Write-Host "📋 Post-deployment checklist in: spam_monitoring/README.md"
Write-Host ""
Write-Host "⚠️  CRITICAL: Monitor first inquiry #293+ classification" -ForegroundColor Yellow
Write-Host "   Expected: Legitimate inquiry NOT flagged as spam"
Write-Host ""
Write-Host "🎯 SUCCESS INDICATORS (First Hour):"
Write-Host "   • No legitimate inquiries classified as 'Likely Spam'"
Write-Host "   • International context detection working"
Write-Host "   • Email notifications working for genuine inquiries"
Write-Host "   • Dashboard shows accurate classification"
Write-Host ""
Write-Host "🚨 RED FLAGS (Require Immediate Action):"
Write-Host "   • Multiple inquiries scoring < 30 unexpectedly"
Write-Host "   • Indian inquiries with valid contact info marked spam"
Write-Host "   • No email notifications for inquiries scoring > 60"
Write-Host ""
Write-Host "🛡️ Emergency Rollback: See spam_monitoring/README.md"
Write-Host "=================================================="