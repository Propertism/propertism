***hosting***

# 🚀 RENDER DEPLOYMENT - QUICK REFERENCE

**Repository**: https://github.com/vijaympgs/realtor  
**Status**: ✅ Code pushed and ready

---

## 🎯 QUICK STEPS (15 minutes)

### 1. Create Account (2 min)
- Visit: https://render.com/
- Sign up with GitHub
- Authorize Render

### 2. Create Web Service (1 min)
- Click "New +" → "Web Service"
- Connect to: `vijaympgs/realtor`

### 3. Configure (3 min)
```
Name: propertism-demo
Region: Oregon (US West) or Singapore (Asia)
Branch: main
Root Directory: realtor-web
Runtime: Python 3

Build Command: 
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

Start Command: 
gunicorn realtor_project.wsgi:application

Plan: Free
```

### 4. Environment Variables (2 min)
Click "Advanced" → Add these:
```
DJANGO_SECRET_KEY = render-demo-secret-key-2024-propertism-advisors-llp
DEBUG = False
PYTHON_VERSION = 3.10.0
DJANGO_ALLOWED_HOSTS = .onrender.com
```

### 5. Deploy (1 min)
- Click "Create Web Service"
- Wait 5-7 minutes for build

### 6. Create Admin (2 min)
- Go to "Shell" tab → "Launch Shell"
- Run: `python manage.py createsuperuser`
- Username: `admin`
- Password: [choose strong password]

### 7. Add Content (5 min)
- Visit: `https://propertism-demo.onrender.com/secure-admin-panel/`
- Login with admin credentials
- Add company info and sample properties

### 8. Test & Share (3 min)
- Test all pages
- Share URL with owner

---

## 📋 COPY-PASTE VALUES

### Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Start Command
```bash
gunicorn realtor_project.wsgi:application
```

### Environment Variables
```
DJANGO_SECRET_KEY=render-demo-secret-key-2024-propertism-advisors-llp
DEBUG=False
PYTHON_VERSION=3.10.0
DJANGO_ALLOWED_HOSTS=.onrender.com
```

---

## 🎯 EXPECTED RESULT

**Demo URL**: https://propertism-demo.onrender.com  
**Admin URL**: https://propertism-demo.onrender.com/secure-admin-panel/  
**Cost**: $0 (Free)  
**Build Time**: 5-7 minutes  
**Status**: Ready for owner review

---

## ⚠️ IMPORTANT NOTES

1. **Cold Start**: First load after 15 min inactivity = 30-60 seconds
2. **Solution**: Visit site 5 minutes before showing to owner
3. **Upgrade**: Change to Starter ($7/month) when approved
4. **Support**: Full guide in `sccbs/render.md`

---

## 🔧 QUICK TROUBLESHOOTING

**Build Failed?**
- Check build logs in Render
- Verify all files pushed to GitHub

**Site Error?**
- Go to Shell → Run: `python manage.py migrate`
- Redeploy from "Manual Deploy"

**No CSS?**
- Check if collectstatic ran in build logs
- Redeploy if needed

**Can't Login?**
- Go to Shell → Run: `python manage.py createsuperuser`
- Try again

---

## ✅ CHECKLIST

- [ ] Render account created
- [ ] Web service created
- [ ] Environment variables added
- [ ] Build completed successfully
- [ ] Superuser created
- [ ] Company info added
- [ ] Site tested
- [ ] Ready to show owner

---

**Full Guide**: See `sccbs/render.md` for detailed instructions

**Good luck with the demo!** 🚀
