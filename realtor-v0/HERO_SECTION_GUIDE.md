# Hero Section - Admin Editable Guide

## Overview
The hero section on the homepage is now fully editable from Django Admin, including multi-language support for English, Tamil, and Hindi.

## What's Editable

### 1. Hero Eyebrow (Optional)
- Small text above the main title
- Example: "Propertism Realty Advisors"
- Displays in gold color with uppercase styling
- Translatable in all 3 languages

### 2. Hero Title (Required)
- Main headline of the hero section
- Example: "NRI Property Management Services In India, Chennai"
- Large, prominent serif font
- Translatable in all 3 languages

### 3. Hero Description (Required)
- Supporting text below the title
- Example: "We manage your property and resources when you are far from the nation"
- Translatable in all 3 languages

### 4. Hero Background Image (Optional)
- Upload a high-quality real estate image
- Recommended size: 1920x1080px or larger
- Automatically applies dark overlay for text readability
- Parallax effect on desktop (fixed background)

## How to Edit

### Step 1: Access Django Admin
1. Navigate to: `http://localhost:8000/admin/`
2. Login with your credentials (admin/admin123)

### Step 2: Edit Company Information
1. Click on "Content" section
2. Click on "Company Information"
3. Click on the existing company record

### Step 3: Edit Hero Section
1. Find the "Hero Section" fieldset at the top
2. Edit the fields:
   - **Hero eyebrow**: Optional small text above title
   - **Hero title**: Main headline (required)
   - **Hero description**: Supporting text (required)
   - **Hero image**: Upload background image (optional)

### Step 4: Add Translations
1. Click on the language tabs (English, Tamil, Hindi)
2. Enter translations for each field
3. The hero eyebrow, title, and description support translations
4. Hero image is shared across all languages

### Step 5: Save
1. Click "Save" button at the bottom
2. Visit the homepage to see your changes

## Current Content

### English (EN)
- **Eyebrow**: Propertism Realty Advisors
- **Title**: NRI Property Management Services In India, Chennai
- **Description**: We manage your property and resources when you are far from the nation

### Tamil (TA)
- **Eyebrow**: Propertism ரியல்டி ஆலோசகர்கள்
- **Title**: இந்தியா, சென்னையில் NRI சொத்து மேலாண்மை சேவைகள்
- **Description**: நீங்கள் நாட்டிலிருந்து தொலைவில் இருக்கும்போது உங்கள் சொத்து மற்றும் வளங்களை நாங்கள் நிர்வகிக்கிறோம்

### Hindi (HI)
- **Eyebrow**: Propertism रियल्टी सलाहकार
- **Title**: भारत, चेन्नई में NRI संपत्ति प्रबंधन सेवाएं
- **Description**: जब आप देश से दूर हों तो हम आपकी संपत्ति और संसाधनों का प्रबंधन करते हैं

## Background Image

### Current Setup
- Default image: `/static/images/hero-bg.jpg`
- You can upload a new image via Django Admin
- The uploaded image will override the default

### Image Guidelines
- **Format**: JPG, PNG, or WebP
- **Size**: Minimum 1920x1080px (Full HD)
- **Aspect Ratio**: 16:9 recommended
- **File Size**: Keep under 500KB for fast loading
- **Subject**: Real estate, property, or Chennai cityscape
- **Quality**: High-quality professional photography

### Image Effects
- Automatic dark overlay (75% navy gradient)
- Parallax scrolling on desktop
- Fixed background attachment
- Mobile-optimized (no parallax on mobile)

## Design Features

### Typography
- **Eyebrow**: Small, uppercase, gold color, letter-spaced
- **Title**: Large serif font (Playfair Display), white on image
- **Description**: Medium sans-serif (Inter), slightly transparent white

### Colors
- **Eyebrow**: Gold (#B89A4A)
- **Title**: White with text shadow
- **Description**: White (90% opacity) with text shadow
- **Overlay**: Navy gradient (75% opacity)

### Responsive Design
- Full viewport height on desktop
- Reduced height on mobile
- Parallax disabled on mobile for performance
- Touch-friendly button spacing

## Testing

### Test Different Languages
1. Visit: `http://localhost:8000/en/` (English)
2. Visit: `http://localhost:8000/ta/` (Tamil)
3. Visit: `http://localhost:8000/hi/` (Hindi)

### Test Without Image
- If no hero image is uploaded, the section uses a clean gradient background
- Text remains readable with navy color scheme

### Test With Image
- Upload an image via Django Admin
- Refresh the homepage
- Image should display with dark overlay
- Text should be clearly readable

## Troubleshooting

### Image Not Showing
1. Check if image was uploaded successfully in admin
2. Verify MEDIA_URL and MEDIA_ROOT in settings.py
3. Ensure media files are being served in development
4. Check browser console for 404 errors

### Translations Not Showing
1. Verify you're visiting the correct language URL (/en/, /ta/, /hi/)
2. Check if translations were saved in admin
3. Clear browser cache
4. Check language switcher in header

### Text Not Readable
1. Ensure hero image has good contrast
2. Dark overlay is automatically applied
3. Try a different image with less busy composition
4. Adjust image brightness before uploading

## Files Modified

### Models
- `realtor-web/content/models.py` - Added hero fields to CompanyInfo

### Admin
- `realtor-web/content/admin.py` - Added Hero Section fieldset

### Translation
- `realtor-web/content/translation.py` - Added hero fields to translation

### Templates
- `realtor-web/uilayers/templates/enterprise-home.html` - Dynamic hero content

### CSS
- `realtor-web/static/css/premium-styles.css` - Hero background image support

### Migrations
- `realtor-web/content/migrations/0003_companyinfo_hero_description_and_more.py`

## Next Steps

1. Upload a professional hero background image
2. Refine translations for Tamil and Hindi
3. Test on different devices and browsers
4. Consider A/B testing different hero messages
5. Update hero content seasonally or for campaigns
