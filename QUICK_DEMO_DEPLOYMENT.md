# Quick Demo Deployment Guide

**Purpose**: Deploy a free demo for owner review  
**Platform**: Render (Free Tier)  
**Time**: 15 minutes  
**Cost**: $0

---

## Prerequisites

- [ ] Code pushed to GitHub
- [ ] GitHub account
- [ ] 15 minutes of time

---

## Step-by-Step Deployment

### Step 1: Push Code to GitHub (If Not Already)

```bash
cd C:\tamil\realtor
cd realtor-web

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for demo deployment"

# Create GitHub repository (via GitHub website)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/propertism.git
git branch -M main
git push -u origin main
```

**Time**: 3 minutes

---

### Step 2: Create Render Account

1. Visit: https://render.com/
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest)
4. Authorize Render to access repositories

**Time**: 1 minute

---

### Step 3: Create New Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect" next to your `propertism` repository
4. If repository not visible, click "Configure account" and grant access

**Time**: 1 minute

---

### Step 4: Configure Service

Fill in the form:

**Basic Settings**:
```
Name: propertism-demo
Region: Oregon (US West) or Singapore (Asia)
Branch: main
Root Directory: realtor-web
Runtime: Python 3
```

**Build & Deploy**:
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn realtor_project.wsgi:application
```

**Plan**:
```
Instance Type: Free
```

**Time**: 2 minutes

---

### Step 5: Add Environment Variables

Click "Advanced" → "Add Environment Variable"

Add these one by one:

```
DJANGO_SECRET_KEY = demo-secret-key-for-testing-only
DEBUG = False
PYTHON_VERSION = 3.10.0
```

For `DJANGO_ALLOWED_HOSTS`:
- Wait until service is created
- Render will show you the URL (e.g., `propertism-demo.onrender.com`)
- Add that URL as the value

**Time**: 2 minutes

---

### Step 6: Deploy

1. Click "Create Web Service"
2. Render will start building
3. Watch the logs (automatic)
4. Wait for "Live" status (green)

**Build Process** (automatic):
- Installing Python
- Installing dependencies
- Running migrations
- Starting Gunicorn
- Generating SSL certificate

**Time**: 5-7 minutes (automatic)

---

### Step 7: Update ALLOWED_HOSTS

Once deployed, you'll see your URL: `https://propertism-demo.onrender.com`

1. Go to "Environment" tab
2. Find `DJANGO_ALLOWED_HOSTS`
3. Update value to: `propertism-demo.onrender.com`
4. Click "Save Changes"
5. Service will redeploy automatically (1 minute)

**Time**: 1 minute

---

### Step 8: Create Superuser

1. In Render dashboard, go to "Shell" tab
2. Click "Launch Shell"
3. Run command:
   ```bash
   python manage.py createsuperuser
   ```
4. Enter:
   - Username: `admin`
   - Email: `your-email@example.com`
   - Password: (choose a strong password)
   - Confirm password

**Time**: 2 minutes

---

### Step 9: Add Demo Content

1. Visit: `https://propertism-demo.onrender.com/secure-admin-panel/`
2. Log in with superuser credentials
3. Add Company Information:
   - Company name: Propertism Realty Advisors LLP
   - Tagline, description, contact info
   - Upload hero image (if available)
4. Add 2-3 Sample Properties:
   - Property 1: Luxury Villa
   - Property 2: Modern Apartment
   - Property 3: Commercial Space
5. Add Team Members (optional)

**Time**: 5-10 minutes

---

### Step 10: Test & Share

**Test the Demo**:
- [ ] Visit homepage: `https://propertism-demo.onrender.com`
- [ ] Check all pages load
- [ ] Test language switcher (EN/TA/HI)
- [ ] Test contact form
- [ ] Check mobile view

**Share with Owner**:
```
Demo URL: https://propertism-demo.onrender.com
Admin URL: https://propertism-demo.onrender.com/secure-admin-panel/
Username: admin
Password: [your-password]

Note: First load may take 30-60 seconds if site was inactive.
```

**Time**: 3 minutes

---

## Total Time: 15-20 Minutes

---

## Important Notes

### Free Tier Limitations

**Cold Starts**:
- Site spins down after 15 minutes of inactivity
- First load after inactivity: 30-60 seconds
- Subsequent loads: Fast (< 2 seconds)

**Solution for Demo**:
- Visit site 5 minutes before showing to owner
- Site will be fast and responsive during demo

**Hours Available**:
- 750 hours/month free
- More than enough for demo period

---

## Upgrade to Paid (When Ready)

When owner approves:

1. Go to Render dashboard
2. Click on service
3. Go to "Settings" → "Instance Type"
4. Change from "Free" to "Starter" ($7/month)
5. Click "Save Changes"

**Benefits of Paid**:
- No cold starts (always on)
- Faster performance
- More resources
- Production-ready

---

## Troubleshooting

### Issue: Build Failed

**Check**:
- `requirements.txt` exists in `realtor-web/` folder
- All dependencies are listed
- Python version is 3.10

**Fix**:
- Check build logs in Render
- Fix any missing dependencies
- Push changes to GitHub
- Render auto-deploys

### Issue: Site Shows Error

**Check**:
- Environment variables are set correctly
- `DJANGO_ALLOWED_HOSTS` includes your Render URL
- Migrations ran successfully

**Fix**:
- Go to "Shell" tab
- Run: `python manage.py migrate`
- Restart service

### Issue: Static Files Not Loading

**Check**:
- `collectstatic` ran during build
- WhiteNoise is in `MIDDLEWARE`

**Fix**:
- Add to build command: `python manage.py collectstatic --noinput`
- Redeploy

### Issue: Admin Login Not Working

**Check**:
- Superuser was created
- Using correct URL: `/secure-admin-panel/`

**Fix**:
- Go to Shell
- Run: `python manage.py createsuperuser`
- Try again

---

## Demo Checklist

Before showing to owner:

- [ ] Site is live and accessible
- [ ] HTTPS working (green padlock)
- [ ] Company information added
- [ ] 2-3 properties added with images
- [ ] Contact form tested
- [ ] All pages load correctly
- [ ] Mobile view tested
- [ ] Admin access working
- [ ] Site visited 5 minutes before demo (to avoid cold start)

---

## After Owner Approval

1. **Keep Free Tier** for testing (optional)
2. **Deploy Production** on paid tier ($7/month)
3. **Add Custom Domain** (yourdomain.com)
4. **Configure Email** (SendGrid)
5. **Set Up Monitoring** (UptimeRobot)
6. **Go Live!** 🚀

---

## Alternative: Railway Free Tier

If Render doesn't work, try Railway:

1. Visit: https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select repository
5. Add environment variables
6. Deploy

**URL**: `propertism-demo.up.railway.app`

**Free Credit**: $5/month (enough for demo)

---

## Support

**Render Documentation**: https://render.com/docs/deploy-django  
**Django on Render Guide**: https://render.com/docs/deploy-django  
**Community Forum**: https://community.render.com/

---

## Summary

**Platform**: Render Free Tier  
**Cost**: $0  
**Time**: 15 minutes  
**URL**: `https://propertism-demo.onrender.com`  
**Perfect for**: Owner review and approval

**Next Step**: Once approved, upgrade to paid tier and add custom domain!

---

**Quick Start Command**:
```bash
# Just push to GitHub and follow steps above!
git push origin main
```

Good luck with the demo! 🚀
