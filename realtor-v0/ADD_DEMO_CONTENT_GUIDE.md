# Add Demo Content Guide

This guide will help you add Tamil and Hindi content to the demo site so the owner can see the multi-language feature working.

---

## Quick Steps

### Step 1: Access Render Shell

1. Go to Render Dashboard: https://dashboard.render.com/
2. Click on your **"propertism-demo"** service
3. Click **"Shell"** tab (left sidebar)
4. Click **"Launch Shell"** button
5. Wait for shell to connect (10-15 seconds)

### Step 2: Run the Demo Content Script

Copy and paste this command into the Render Shell:

```bash
python add_demo_content.py
```

Press Enter and wait 5-10 seconds.

### Step 3: Verify Success

You should see output like:

```
============================================================
ADDING DEMO CONTENT IN ENGLISH, TAMIL, AND HINDI
============================================================
Adding company information...
✅ Company information added successfully!

Adding services...
✅ Service added: Real Estate Buy & Sell
✅ Service added: Rental & Maintenance
✅ Service added: Industrial Land Services

Adding statistics...
✅ Statistic added: 500+ Properties Managed
✅ Statistic added: 200+ Happy NRI Clients
✅ Statistic added: 10+ Years of Experience
✅ Statistic added: 5+ Cities Covered

============================================================
✅ ALL DEMO CONTENT ADDED SUCCESSFULLY!
============================================================

You can now view the website in:
- English: https://propertism-demo.onrender.com/en/
- Tamil:   https://propertism-demo.onrender.com/ta/
- Hindi:   https://propertism-demo.onrender.com/hi/

Or use the language switcher on the website!
```

### Step 4: Test the Languages

Visit these URLs to see content in each language:

**English**: https://propertism-demo.onrender.com/en/  
**Tamil**: https://propertism-demo.onrender.com/ta/  
**Hindi**: https://propertism-demo.onrender.com/hi/

Or simply use the language switcher (top right corner) on the website!

---

## What Gets Added

### Company Information (All 3 Languages)
- Company name
- Tagline
- Hero section title and description
- About mission and description

### Services (All 3 Languages)
1. Real Estate Buy & Sell
2. Rental & Maintenance
3. Industrial Land Services

### Statistics
- 500+ Properties Managed
- 200+ Happy NRI Clients
- 10+ Years of Experience
- 5+ Cities Covered

---

## For Owner to Test

Share these instructions with the owner:

### How to Switch Languages

**Method 1: Language Switcher**
1. Visit: https://propertism-demo.onrender.com
2. Look at top right corner
3. Click on "EN" dropdown
4. Select "TA" for Tamil or "HI" for Hindi
5. Page will reload in selected language

**Method 2: Direct URLs**
- English: https://propertism-demo.onrender.com/en/
- Tamil: https://propertism-demo.onrender.com/ta/
- Hindi: https://propertism-demo.onrender.com/hi/

### What to Check

- [ ] Hero section shows in selected language
- [ ] Navigation menu in selected language
- [ ] Services section in selected language
- [ ] Company information in selected language
- [ ] All pages work in all languages

---

## Troubleshooting

### Issue: Script Not Found

If you see "No such file or directory":

```bash
# First, check you're in the right directory
pwd

# Should show: /opt/render/project/src/realtor-web

# If not, navigate there:
cd /opt/render/project/src/realtor-web

# Then run the script:
python add_demo_content.py
```

### Issue: Permission Denied

If you see permission error:

```bash
# Make script executable
chmod +x add_demo_content.py

# Then run it
python add_demo_content.py
```

### Issue: Module Not Found

If you see "No module named 'django'":

```bash
# Activate virtual environment first
source /opt/render/project/src/.venv/bin/activate

# Then run script
python add_demo_content.py
```

---

## Alternative: Run Locally Then Push

If Render Shell doesn't work, you can run locally:

### On Your Computer

```bash
# Navigate to project
cd C:\tamil\realtor\realtor-web

# Run the script
python add_demo_content.py

# Commit the database changes
git add db.sqlite3
git commit -m "Add demo content in all languages"
git push origin main
```

Render will automatically redeploy with the updated database.

---

## Summary

**Time Required**: 2 minutes  
**Difficulty**: Easy (just copy-paste one command)  
**Result**: Website works in English, Tamil, and Hindi

**Command to Run**:
```bash
python add_demo_content.py
```

**Test URLs**:
- English: https://propertism-demo.onrender.com/en/
- Tamil: https://propertism-demo.onrender.com/ta/
- Hindi: https://propertism-demo.onrender.com/hi/

---

**Ready to add demo content!** 🚀
