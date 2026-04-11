# Bugfix Design Document

## Problem Summary

The landing page CSS is not loading because `landing_page.html` uses `{% block extra_head %}` to inject the CSS link, but `base.html` only defines `{% block extra_css %}`. This causes the CSS link to be silently ignored during template rendering.

## Root Cause Analysis

**File:** `uilayers/templates/landing_page.html` (line 17)
```django
{% block extra_head %}
<link rel="stylesheet" href="{% static 'css/landing-premium.css' %}">
{% endblock %}
```

**File:** `uilayers/templates/base.html` (line 35)
```django
{% block extra_css %}{% endblock %}
```

The block names don't match, so Django's template inheritance ignores the `extra_head` block content.

## Solution Design

### Option 1: Update landing_page.html (RECOMMENDED)
Change the block name from `extra_head` to `extra_css` to match base.html's existing block.

**Pros:**
- Minimal change (1 line)
- Follows existing convention used by other templates
- No risk of breaking other templates
- Maintains consistency across codebase

**Cons:**
- None

### Option 2: Add extra_head block to base.html
Add a new `{% block extra_head %}` block in base.html's `<head>` section.

**Pros:**
- More flexible for future templates

**Cons:**
- Requires modifying base template
- Potential confusion with two similar blocks (extra_css and extra_head)
- Higher risk of regression

**DECISION: Use Option 1** - Update landing_page.html to use `extra_css` block

## Implementation Plan

### Changes Required

1. **File:** `uilayers/templates/landing_page.html`
   - Line 17: Change `{% block extra_head %}` to `{% block extra_css %}`
   - Line 19: Change `{% endblock %}` (no change needed, just closing tag)

### Verification Steps

1. Start Django dev server on port 8001
2. Navigate to http://127.0.0.1:8001/chennai/flats-for-sale/
3. Verify CSS loads by checking:
   - Browser DevTools Network tab shows `landing-premium.css` loaded (200 status)
   - Page source contains `<link rel="stylesheet" href="/static/css/landing-premium.css">`
   - Property cards display with proper styling (shadows, rounded corners, grid layout)
   - Buttons are styled correctly (primary green, secondary outlined)
   - Typography is properly sized and spaced
   - Responsive grid works (3→2→1 columns)

### Regression Testing

1. Check other templates still load their CSS correctly:
   - Home page: http://127.0.0.1:8001/
   - Properties listing: http://127.0.0.1:8001/properties/
   - Contact page: http://127.0.0.1:8001/contact/

2. Verify no console errors in browser DevTools

3. Test on mobile viewport (responsive design intact)

## Risk Assessment

**Risk Level:** LOW

- Single line change in one template file
- No database migrations required
- No settings changes required
- No static files changes required
- Follows existing pattern used by other templates

## Rollback Plan

If issues occur, revert the single line change:
```django
{% block extra_css %}  →  {% block extra_head %}
```
