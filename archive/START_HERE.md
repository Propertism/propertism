# 🚀 Start Here - Propertism Quick Start Guide

## ⚡ Fastest Way to Start

Just double-click this file:
```
start.bat
```

That's it! Your browser will open automatically to:
```
http://localhost:8000/en/
```

---

## 📋 Available Startup Scripts

### 1. `start.bat` ⭐ RECOMMENDED
**Use this for**: Daily development and testing

**What it does**:
- Starts Django backend (port 8000)
- Opens browser automatically
- Production-ready environment

**When to use**:
- Testing your changes
- Showing to clients
- Normal development work

```bash
start.bat
```

### 2. `start-with-react.bat`
**Use this for**: React development with hot reload

**What it does**:
- Starts Django backend (port 8000)
- Starts React dev server (port 5173)
- Opens both in browser

**When to use**:
- Editing React components
- Need instant hot reload
- React-focused development

```bash
start-with-react.bat
```

### 3. `run-web-only.bat` (Legacy)
**Same as**: `start-with-react.bat`

**Status**: Still works, but use the new scripts above

---

## 🌐 URLs After Starting

### Main Application
```
http://localhost:8000/en/
```
👉 **Use this URL** - This is your production-ready site!

### Admin Panel
```
http://localhost:8000/en/admin/
Username: admin
Password: admin123
```

### API Endpoints
```
http://localhost:8000/api/properties/
http://localhost:8000/api/users/
http://localhost:8000/api/search/
```

### React Dev Server (Optional)
```
http://localhost:5173/
```
⚠️ Only available when using `start-with-react.bat`

---

## 🎯 Which Script Should I Use?

### Simple Decision Tree

```
Are you editing React code?
│
├─ NO  → Use start.bat ⭐
│        (Fastest, simplest)
│
└─ YES → Use start-with-react.bat
         (Hot reload for React)
```

### Detailed Comparison

| Feature | start.bat | start-with-react.bat |
|---------|-----------|---------------------|
| Django Backend | ✅ Yes | ✅ Yes |
| React Hot Reload | ❌ No | ✅ Yes |
| Speed | ⚡ Fast | 🐢 Slower |
| Browser Opens | 1 tab | 2 tabs |
| Production-like | ✅ Yes | ✅ Yes |
| **Recommended for** | **Daily use** | React development |

---

## 🛑 How to Stop

### Option 1: Close the CMD Window
Just close the black command window that opened.

### Option 2: Press Ctrl+C
In the command window, press `Ctrl+C` to stop the server.

### Option 3: Run stop.bat
```bash
stop.bat
```

---

## 📱 Mobile App Development

### Start Backend for Mobile
```bash
start.bat
```

### Configure Mobile App
The mobile app should point to:
```
http://localhost:8000/api
```

### Start Mobile App
```bash
cd realtor-mobile
npm start
```

---

## 🔧 Troubleshooting

### Port Already in Use
**Problem**: "Port 8000 is already in use"

**Solution**:
```bash
# Kill all Python processes
taskkill /F /IM python.exe /T

# Or use stop.bat
stop.bat
```

### React Won't Start
**Problem**: React dev server fails

**Solution**:
```bash
cd realtor-web/uilayers
npm install
npm run dev
```

### Django Won't Start
**Problem**: Django server fails

**Solution**:
```bash
cd realtor-web
python manage.py migrate
python manage.py runserver
```

### Browser Doesn't Open
**Problem**: Browser doesn't open automatically

**Solution**:
Manually visit: `http://localhost:8000/en/`

---

## 📚 What You'll See

### Homepage
- **Branding**: Propertism
- **Hero**: "NRI Property Management Services In Chennai"
- **Services**: Real Estate, Rental, Industrial Land
- **Contact**: India + US office details

### Navigation
- HOME
- PROPERTIES
- SERVICES
- ABOUT
- MANAGEMENT
- BLOG
- CONTACT

### Footer
- India Office (Chennai)
- US Office (Hackensack, NJ)
- Multiple phone numbers
- Email: info@propertism.com

---

## 🎨 Design Features

Your site follows enterprise-grade design (SCCB-4 & SCCB-5):

- ✅ Sharp edges (no rounded corners)
- ✅ Navy/Gold/White color palette
- ✅ Playfair Display + Inter fonts
- ✅ Investment-grade aesthetic
- ✅ Professional, clean layout

---

## 📊 Project Structure

```
realtor/
├── start.bat                    ⭐ Quick start (recommended)
├── start-with-react.bat         React hot reload
├── stop.bat                     Stop all servers
├── build-production.bat         Build for production
│
├── realtor-web/                 Django backend + web
│   ├── manage.py
│   ├── properties/              Property listings
│   ├── users/                   User management
│   ├── uilayers/                React web frontend
│   └── templates/               Django templates
│
└── realtor-mobile/              React Native mobile
    ├── app/                     Expo Router
    └── src/                     Components
```

---

## 🚀 Next Steps

### 1. Start the Application
```bash
start.bat
```

### 2. Explore the Site
Visit: `http://localhost:8000/en/`

### 3. Login to Admin
Visit: `http://localhost:8000/en/admin/`
- Username: `admin`
- Password: `admin123`

### 4. Check Properties
Visit: `http://localhost:8000/en/properties/`

### 5. Test APIs
Visit: `http://localhost:8000/api/properties/`

---

## 💡 Pro Tips

### Tip 1: Use start.bat for 90% of Work
Unless you're actively editing React code, `start.bat` is all you need.

### Tip 2: Keep Admin Panel Open
Keep `http://localhost:8000/en/admin/` in a browser tab for quick access.

### Tip 3: Test on Port 8000
Always test on port 8000 - it's what production will look like.

### Tip 4: Mobile Testing
For mobile app development, just run `start.bat` for the backend.

### Tip 5: Quick Restart
If something breaks, just close the CMD window and run `start.bat` again.

---

## 📞 Quick Reference

### Start Application
```bash
start.bat
```

### Stop Application
Close the CMD window or press `Ctrl+C`

### Main URL
```
http://localhost:8000/en/
```

### Admin Panel
```
http://localhost:8000/en/admin/
admin / admin123
```

### Build for Production
```bash
build-production.bat
```

---

## 🎯 Common Tasks

### Task: View Homepage
1. Run `start.bat`
2. Browser opens automatically
3. See Propertism homepage

### Task: Add Property
1. Run `start.bat`
2. Visit `http://localhost:8000/en/admin/`
3. Login (admin/admin123)
4. Click "Properties" → "Add Property"

### Task: Edit React Code
1. Run `start-with-react.bat`
2. Edit files in `realtor-web/uilayers/src/`
3. See changes instantly at `http://localhost:5173/`

### Task: Test APIs
1. Run `start.bat`
2. Visit `http://localhost:8000/api/properties/`
3. See JSON response

### Task: Deploy to Production
1. Run `build-production.bat`
2. Test at `http://localhost:8000/en/`
3. Deploy Django to server

---

## ✅ Success Checklist

After running `start.bat`, you should see:

- [ ] CMD window opens with "Propertism Backend"
- [ ] Chrome opens automatically
- [ ] Homepage loads with Propertism branding
- [ ] Navigation shows 7 menu items
- [ ] Hero says "NRI Property Management Services"
- [ ] Footer shows India + US offices
- [ ] No errors in CMD window

If all checked, you're ready to go! 🎉

---

## 📖 More Documentation

- **Architecture**: See `PRODUCTION_ARCHITECTURE.md`
- **Quick Start**: See `QUICK_START_PRODUCTION.md`
- **Propertism Integration**: See `PROPERTISM_INTEGRATION_COMPLETE.md`
- **Django CMS**: See `DJANGO_CMS_GUIDE.md`

---

**Ready to start?** Just run:
```bash
start.bat
```

🚀 **That's it! You're all set!**
