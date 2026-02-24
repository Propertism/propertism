# Django CMS Demo - How to Use

Viji, I've set up everything you need to try Django CMS! Here's how to create and edit a demo page.

---

## 🎯 What is Django CMS?

Django CMS is a visual page builder that lets you:
- Create pages without coding
- Add content by dragging plugins
- Edit content directly on the page
- Manage page structure visually

---

## 🎯 How to Access Django CMS

### Method 1: Direct URL (Recommended)
Go directly to the CMS page management:
```
http://localhost:8000/en/admin/cms/page/
```

### Method 2: Through Admin
1. Go to: **http://localhost:8000/en/admin/**
2. Scroll down to **"CMS"** section
3. Click on **"Pages"**

### Method 3: Django CMS Button
1. In admin, click **"django CMS"** button (top-left)
2. If it redirects to homepage, use Method 1 instead

---

## 📝 How to Create a CMS Demo Page
1. You'll see the CMS page tree
2. Click **"+ Create Page"** button
3. Fill in:
   - **Title**: "CMS Demo"
   - **Slug**: "cms-demo"
   - **Template**: Select "CMS Demo Page"
4. Click **"Save"**

### Step 3: Add Content
1. Click **"Edit"** button in the toolbar
2. You'll see the page with an empty content area
3. Click the **"+"** button to add plugins
4. Try adding:
   - **Text** plugin - Add paragraphs, headings
   - **Image** plugin - Upload and display images
   - **Link** plugin - Add buttons and links

### Step 4: Publish
1. Click **"Publish page changes"** in the toolbar
2. Visit: **http://localhost:8000/en/cms-demo/**
3. See your published page!

---

## 🎨 Available Plugins

Django CMS comes with these plugins:

### Text Plugin
- Add rich text content
- Format with bold, italic, lists
- Add headings (H1, H2, H3)

### Image Plugin
- Upload images
- Set alt text
- Control alignment

### Link Plugin
- Create buttons
- Add external links
- Link to other pages

### Video Plugin
- Embed YouTube videos
- Add Vimeo videos

---

## 🔧 How to Edit

### Edit Mode
1. Visit any CMS page
2. Add `?edit` to the URL
3. Example: `http://localhost:8000/en/cms-demo/?edit`
4. Click **"Edit"** in toolbar

### Structure Mode
1. Click **"Structure"** in toolbar
2. See all plugins
3. Drag to reorder
4. Delete unwanted plugins

### Content Mode
1. Click **"Content"** in toolbar
2. Edit text directly on page
3. Double-click to edit plugins

---

## 💡 Tips

### Saving Changes
- Changes are saved as drafts automatically
- Click **"Publish"** to make them live
- You can preview before publishing

### Undo Changes
- Click **"Discard changes"** to undo
- Unpublished changes won't affect live site

### Page Settings
- Click **"Page"** → **"Settings"**
- Change title, slug, template
- Control page visibility

---

## 🎯 Try This Demo

### Create a Simple Page:

1. **Add a heading**:
   - Add Text plugin
   - Type: "Welcome to Our Demo"
   - Format as H1

2. **Add a paragraph**:
   - Add another Text plugin
   - Type some description
   - Format text as needed

3. **Add an image**:
   - Add Image plugin
   - Upload a photo
   - Set alt text

4. **Publish**:
   - Click "Publish page changes"
   - View your page!

---

## 📊 CMS vs Our Content System

### Django CMS (Visual Builder)
```
✅ Visual editing
✅ Drag and drop
✅ Good for: Landing pages, marketing pages
❌ Complex for structured content
❌ Overkill for simple updates
```

### Our Content System (Forms)
```
✅ Simple forms
✅ Structured data
✅ Good for: Services, team, company info
✅ Easy to use
✅ Perfect for your needs
```

---

## 🎯 My Recommendation

**For your website**:
- Use **Content System** (admin forms) for:
  - Services
  - Team members
  - Company information
  - Contact inquiries

- Use **Django CMS** (if needed) for:
  - Special landing pages
  - Marketing campaigns
  - One-off promotional pages

**Most of the time, you'll use the Content System** - it's simpler and better for your needs!

---

## 🚀 Quick Access

### Content Management (Main System)
```
URL: http://localhost:8000/en/admin/
Section: CONTENT
Use for: Daily content updates
```

### Django CMS (Page Builder)
```
URL: http://localhost:8000/en/admin/ → Click "django CMS"
Use for: Creating special pages (optional)
```

---

## ❓ Questions?

### "Should I use Django CMS?"
- **For your current pages**: No, use Content System
- **For special pages**: Maybe, if you want visual editing

### "Is Django CMS better?"
- Not better, just different
- More complex
- Good for different use cases

### "Can I use both?"
- Yes! They work together
- Use Content System for main site
- Use CMS for special pages if needed

---

## ✅ Summary

1. **Django CMS is installed and working**
2. **Template is ready** (cms_demo.html)
3. **You can create pages** through admin
4. **It's optional** - use only if you want visual editing

**For now, focus on the Content System** - it's what you need for managing your website content!

---

**Status**: ✅ Django CMS Ready (Optional)
**Recommendation**: Use Content System for daily work
**CMS Access**: Admin → "django CMS" button

