# Propertism Logo Instructions

## 📍 Logo Location

Place your Propertism logo file here:
```
realtor-web/static/images/propertism-logo.png
```

## 📐 Logo Specifications

### Recommended Dimensions
- **Width**: 150-200px
- **Height**: 40-50px
- **Format**: PNG with transparent background
- **Resolution**: 2x for retina displays (300x100px actual, displayed at 150x50px)

### Alternative Formats
You can also use:
- `propertism-logo.svg` (vector, best quality)
- `propertism-logo.jpg` (if no transparency needed)
- `propertism-logo.webp` (modern format, smaller file size)

## 🎨 Design Guidelines (SCCB-4 & SCCB-5 Compliant)

### Logo Style
- ✅ Sharp edges (no rounded corners)
- ✅ Clean, professional design
- ✅ Navy (#0F172A) or Gold (#B89A4A) colors preferred
- ✅ White version for dark backgrounds
- ❌ No gradients
- ❌ No soft shadows
- ❌ No decorative elements

### Color Variations Needed

1. **Primary Logo** (for light backgrounds)
   - Navy (#0F172A) or dark text
   - File: `propertism-logo.png`

2. **White Logo** (for dark backgrounds)
   - White or light text
   - File: `propertism-logo-white.png`

3. **Gold Accent** (optional)
   - Gold (#B89A4A) accent color
   - File: `propertism-logo-gold.png`

## 📂 File Structure

```
realtor-web/static/images/
├── propertism-logo.png          (Primary - dark on light)
├── propertism-logo-white.png    (White for dark backgrounds)
├── propertism-logo-gold.png     (Optional - gold accent)
├── propertism-logo.svg          (Vector version - best)
└── favicon.ico                  (Browser tab icon)
```

## 🔧 How to Add Your Logo

### Step 1: Prepare Logo File
1. Export logo as PNG with transparent background
2. Recommended size: 300x100px (2x for retina)
3. Optimize file size (use TinyPNG or similar)

### Step 2: Add to Project
```bash
# Copy your logo file to:
realtor-web/static/images/propertism-logo.png
```

### Step 3: Collect Static Files
```bash
cd realtor-web
python manage.py collectstatic --noinput
```

### Step 4: Test
```bash
start.bat
# Visit: http://localhost:8000/en/
# Logo should appear in navigation
```

## 🎯 Where Logo Appears

### 1. Navigation Bar (Top Left)
- **Location**: Header navigation
- **Size**: 40px height
- **Background**: Navy (#0F172A)
- **Logo Color**: White version recommended

### 2. Footer (Optional)
- **Location**: Footer section
- **Size**: 30px height
- **Background**: Black (#111111)
- **Logo Color**: White version

### 3. Favicon (Browser Tab)
- **Location**: Browser tab icon
- **Size**: 32x32px or 64x64px
- **Format**: .ico or .png
- **File**: `favicon.ico`

## 🖼️ Temporary Placeholder

Currently, the site shows:
- Text: "PROPERTISM" in navigation
- If logo file exists, it will display automatically
- If logo file is missing, text remains visible

## 📱 Mobile Considerations

### Responsive Logo
- Logo should scale well on mobile devices
- Consider a simplified version for small screens
- Test on various screen sizes

### Mobile Logo Sizes
- **Desktop**: 150px width
- **Tablet**: 120px width
- **Mobile**: 100px width

## 🎨 Logo Usage Examples

### Example 1: Simple Text Logo
If you don't have a graphic logo yet, the current text "PROPERTISM" works well with the enterprise design.

### Example 2: Icon + Text
```
[ICON] PROPERTISM
```
Icon on left, text on right (current setup)

### Example 3: Icon Only (Mobile)
On mobile, you might show only the icon to save space.

## 🔄 Updating Logo

### To Change Logo
1. Replace file: `realtor-web/static/images/propertism-logo.png`
2. Run: `python manage.py collectstatic --noinput`
3. Hard refresh browser: `Ctrl+F5`

### To Use Different Format
Update the image source in:
- `realtor-web/uilayers/templates/enterprise-home.html`
- `realtor-web/uilayers/src/components/Layout.tsx`

Change from:
```html
<img src="/static/images/propertism-logo.png" ...>
```

To:
```html
<img src="/static/images/propertism-logo.svg" ...>
```

## ✅ Checklist

Before deploying:
- [ ] Logo file added to `static/images/`
- [ ] Logo is optimized (small file size)
- [ ] Logo has transparent background
- [ ] Logo looks good on dark background (navigation)
- [ ] Logo looks good on light background (if used)
- [ ] Logo is sharp on retina displays
- [ ] Favicon added
- [ ] Static files collected
- [ ] Tested on desktop
- [ ] Tested on mobile
- [ ] Tested on tablet

## 🚀 Quick Start

If you have your logo ready:

```bash
# 1. Copy logo
copy your-logo.png realtor-web\static\images\propertism-logo.png

# 2. Collect static files
cd realtor-web
python manage.py collectstatic --noinput

# 3. Test
cd ..
start.bat
```

## 💡 Pro Tips

### Tip 1: Use SVG for Best Quality
SVG logos scale perfectly at any size and have smaller file sizes.

### Tip 2: Optimize PNG Files
Use tools like TinyPNG to reduce file size without losing quality.

### Tip 3: Test on Dark Background
Your logo will appear on a navy background (#0F172A), so ensure it's visible.

### Tip 4: Keep It Simple
The enterprise design favors clean, simple logos without decorative elements.

### Tip 5: Maintain Aspect Ratio
Don't stretch or squash the logo - maintain its original proportions.

## 📞 Need Help?

If you need help with:
- Logo design
- File format conversion
- Optimization
- Implementation

Check the main documentation or create a support ticket.

---

**Current Status**: Logo placeholder ready
**Action Required**: Add `propertism-logo.png` to this directory
**Fallback**: Text "PROPERTISM" displays if logo is missing
