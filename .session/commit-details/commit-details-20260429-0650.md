<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-04-29 06:50:00
Last Updated By: Astra
Last Updated On: 2026-04-29 07:02:00
Searchtag:COMMITDETAILS202604290650
-->

# Commit Manifest — 2026-04-29 06:50 IST

## Session Title
**Hero Image Rotation Fix — CSS Override + Duplicate Script Removal**

## Scope
- **Workspace**: `D:\viji\viji-olivine\03rolledout\01propertism`
- **Domain**: Propertism Frontend (Production)
- **Sections**: Hero Image Rotation

---

## Root Cause Analysis

### Issue 1: CSS `opacity: 1 !important` defeating rotation (PRIMARY CAUSE)

`propertism-premium.css` (loads last, highest specificity) had:
```css
.hero-hybrid-image {
    opacity: 1 !important;
}
```
This forced **all 5 hero images to be fully visible at all times**, stacked on top of each other. The JS rotation toggled `is-active` correctly, but the CSS override made it invisible — every image had `opacity: 1` regardless of class state.

### Issue 2: Two competing `setInterval(10000)` scripts

Two independent rotation scripts were both toggling `is-active`:

| Script | Location | Behavior |
|--------|----------|----------|
| ❌ Inline (removed) | `_hero.html` lines 33–47 | Sequential rotation |
| ✅ Canonical (kept) | `_home_js.html` lines 128–157 | Random rotation + preloading |

Both fired every 10s but tracked separate index variables, causing `is-active` state conflicts.

---

## Fixes Applied

### Fix 1: CSS — `propertism-premium.css`
Changed blanket `opacity: 1 !important` on ALL hero images to target only `.is-active`:

```diff
 .hero-hybrid-image {
     filter: none !important;
     -webkit-filter: none !important;
-    opacity: 1 !important;
+    opacity: 0;
+    transition: opacity 0.8s ease;
+}
+
+.hero-hybrid-image.is-active {
+    opacity: 1 !important;
 }
```

### Fix 2: JS — `_hero.html`
Removed duplicate inline `<script>` (16 lines). Canonical rotation in `_home_js.html` retained.

---

## Files Modified

| File | Summary |
|------|---------|
| `static/css/propertism-premium.css` | Split `.hero-hybrid-image` opacity rule: inactive = `opacity: 0`, active = `opacity: 1 !important` |
| `uilayers/templates/home/sections/_hero.html` | Removed duplicate inline rotation `<script>` |

---

## Commit Message (Suggested)

```
fix: hero image rotation — CSS opacity override + duplicate script removal

propertism-premium.css had `opacity: 1 !important` on all hero images,
making all 5 permanently visible and defeating the rotation. Fixed to
apply only to .is-active. Also removed duplicate setInterval from
_hero.html; canonical rotation in _home_js.html retained.
```

---

**Session Status**: ✅ READY FOR COMMIT  
**Quality**: Surgical Fix — Root Cause Identified & Resolved
