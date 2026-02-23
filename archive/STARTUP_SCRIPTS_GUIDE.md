# Startup Scripts Guide

## 🎯 Quick Reference

### Daily Use (Recommended)
```bash
start.bat
```
Opens: `http://localhost:8000/en/`

### React Development
```bash
start-with-react.bat
```
Opens: `http://localhost:8000/en/` + `http://localhost:5173/`

### Stop Everything
```bash
stop.bat
```

---

## 📋 All Available Scripts

### 1. `start.bat` ⭐ RECOMMENDED
**Purpose**: Quick start for daily development

**What it does**:
- Kills old processes
- Starts Django (port 8000)
- Opens browser to `http://localhost:8000/en/`

**Use when**:
- Testing your work
- Showing to clients
- Normal development
- 90% of the time

**Pros**:
- ✅ Fast startup
- ✅ Simple
- ✅ Production-like
- ✅ One browser tab

**Cons**:
- ❌ No React hot reload

---

### 2. `start-with-react.bat`
**Purpose**: React development with hot reload

**What it does**:
- Kills old processes
- Starts Django (port 8000)
- Starts React dev server (port 5173)
- Opens both in browser

**Use when**:
- Editing React components
- Need instant updates
- React-focused work

**Pros**:
- ✅ Hot module replacement
- ✅ Fast refresh
- ✅ Instant updates

**Cons**:
- ❌ Slower startup
- ❌ Two browser tabs
- ❌ More resource usage

---

### 3. `stop.bat`
**Purpose**: Stop all servers

**What it does**:
- Kills Python processes
- Kills Node processes
- Closes CMD windows

**Use when**:
- Servers won't stop
- Port conflicts
- Clean shutdown needed

---

### 4. `run-web-only.bat` (Legacy)
**Purpose**: Original startup script

**Status**: Still works, same as `start-with-react.bat`

**Note**: Use the new scripts above instead

---

### 5. `build-production.bat`
**Purpose**: Build for production deployment

**What it does**:
- Builds React app
- Collects Django static files
- Runs migrations
- Runs tests

**Use when**:
- Ready to deploy
- Testing production build
- Before going live

---

## 🎯 Decision Tree

```
What do you want to do?
│
├─ Just test the site
│  └─ Use: start.bat ⭐
│
├─ Edit React code
│  └─ Use: start-with-react.bat
│
├─ Stop everything
│  └─ Use: stop.bat
│
└─ Deploy to production
   └─ Use: build-production.bat
```

---

## 🌐 URLs Reference

### After `start.bat`
```
✅ http://localhost:8000/en/              (Homepage)
✅ http://localhost:8000/en/admin/        (Admin)
✅ http://localhost:8000/api/properties/  (API)
❌ http://localhost:5173/                 (Not available)
```

### After `start-with-react.bat`
```
✅ http://localhost:8000/en/              (Homepage - Django)
✅ http://localhost:8000/en/admin/        (Admin)
✅ http://localhost:8000/api/properties/  (API)
✅ http://localhost:5173/                 (Homepage - React)
```

---

## 💡 Best Practices

### 1. Use `start.bat` by Default
Unless you're actively editing React code, `start.bat` is faster and simpler.

### 2. Test on Port 8000
Always test your work on `http://localhost:8000/en/` - it's production-like.

### 3. Use Port 5173 for React Only
Only use `http://localhost:5173/` when you need hot reload for React development.

### 4. Stop Cleanly
Use `stop.bat` or close CMD windows properly to avoid port conflicts.

### 5. Build Before Deploy
Always run `build-production.bat` before deploying to production.

---

## 🔧 Troubleshooting

### Problem: Port 8000 Already in Use
**Solution**:
```bash
stop.bat
# Then start again
start.bat
```

### Problem: React Won't Start
**Solution**:
```bash
cd realtor-web/uilayers
npm install
```

### Problem: Django Errors
**Solution**:
```bash
cd realtor-web
python manage.py migrate
```

### Problem: Browser Doesn't Open
**Solution**:
Manually visit: `http://localhost:8000/en/`

### Problem: Changes Not Showing
**Solution**:
- Hard refresh: `Ctrl+F5`
- Clear cache
- Restart server

---

## 📊 Script Comparison

| Feature | start.bat | start-with-react.bat | stop.bat |
|---------|-----------|---------------------|----------|
| Django Backend | ✅ | ✅ | ❌ |
| React Dev Server | ❌ | ✅ | ❌ |
| Opens Browser | ✅ | ✅ | ❌ |
| Kills Old Processes | ✅ | ✅ | ✅ |
| Startup Speed | ⚡ Fast | 🐢 Slower | ⚡ Instant |
| Resource Usage | 💚 Low | 💛 Medium | 💚 None |
| **Best For** | **Daily use** | React dev | Cleanup |

---

## 🚀 Common Workflows

### Workflow 1: Daily Development
```bash
# Morning
start.bat

# Work on Django/templates
# Test at http://localhost:8000/en/

# Evening
# Close CMD window or stop.bat
```

### Workflow 2: React Development
```bash
# Start with hot reload
start-with-react.bat

# Edit React files in realtor-web/uilayers/src/
# See changes at http://localhost:5173/

# Test production version at http://localhost:8000/en/

# Stop
stop.bat
```

### Workflow 3: Production Build
```bash
# Build
build-production.bat

# Test
start.bat
# Visit http://localhost:8000/en/

# Deploy
# (Upload to server)
```

### Workflow 4: Mobile Development
```bash
# Terminal 1: Backend
start.bat

# Terminal 2: Mobile
cd realtor-mobile
npm start

# Mobile app connects to http://localhost:8000/api
```

---

## 📱 Mobile App Integration

### Backend for Mobile
```bash
start.bat
```

Mobile app should use:
```
http://localhost:8000/api
```

### Start Mobile App
```bash
cd realtor-mobile
npm start
```

### Test Mobile + Web Together
```bash
# Terminal 1: Backend
start.bat

# Terminal 2: Mobile
cd realtor-mobile
npm start

# Both web and mobile work!
```

---

## 🎨 What You'll See

### After `start.bat`
1. CMD window opens: "Propertism Backend"
2. Chrome opens automatically
3. Homepage loads with:
   - Propertism branding
   - NRI messaging
   - Three services
   - India + US offices

### After `start-with-react.bat`
1. Two CMD windows open:
   - "Propertism Backend"
   - "React Dev Server"
2. Chrome opens two tabs:
   - `http://localhost:8000/en/` (Django)
   - `http://localhost:5173/` (React)
3. Both show same content

---

## ✅ Success Indicators

### Successful Start
```
✅ CMD window shows "Starting development server"
✅ No red error messages
✅ Browser opens automatically
✅ Homepage loads correctly
✅ Navigation works
✅ No 404 errors
```

### Failed Start
```
❌ "Port already in use"
❌ "Module not found"
❌ "Database error"
❌ Browser shows error page
```

**Solution**: Run `stop.bat` and try again

---

## 📖 Related Documentation

- **Quick Start**: `START_HERE.md`
- **Architecture**: `PRODUCTION_ARCHITECTURE.md`
- **Propertism Integration**: `PROPERTISM_INTEGRATION_COMPLETE.md`
- **Django CMS**: `DJANGO_CMS_GUIDE.md`

---

## 🎯 Summary

### For 90% of Work
```bash
start.bat
```

### For React Development
```bash
start-with-react.bat
```

### To Stop
```bash
stop.bat
```

### To Deploy
```bash
build-production.bat
```

---

**That's it! Simple and straightforward.** 🚀

Just remember: **`start.bat` is your friend!**
