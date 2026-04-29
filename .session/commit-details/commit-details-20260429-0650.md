<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-04-29 06:50:00
Last Updated By: Astra
Last Updated On: 2026-04-29 06:50:00
Searchtag:COMMITDETAILS202604290650
-->

# Commit Manifest — 2026-04-29 06:50 IST

## Session Title
**Hero Image Rotation Fix — Duplicate setInterval Conflict Resolution**

## Scope
- **Workspace**: `D:\viji\viji-olivine\03rolledout\01propertism`
- **Domain**: Propertism Frontend (Production)
- **Sections**: Hero Image Rotation

---

## Root Cause Analysis

Two independent `setInterval(fn, 10000)` scripts were both toggling `is-active` on hero images:

| Script | Location | Behavior |
|--------|----------|----------|
| ❌ Inline (removed) | `_hero.html` lines 33–47 | Sequential rotation (0→1→2→3→4→0) |
| ✅ Canonical (kept) | `_home_js.html` lines 128–157 | Random rotation + image preloading |

Both fired every 10 seconds but tracked **separate index variables**, causing the `is-active` class to be added/removed unpredictably — resulting in frames with either two active images (overlay flicker) or zero active images (blank hero).

---

## Fix Applied

| Action | Detail |
|--------|--------|
| Removed | Inline `<script>` from `_hero.html` (duplicate rotation logic) |
| Retained | `_home_js.html` canonical rotation (random start, preloading, duplicate-avoidance) |

---

## Files Modified

### Templates
| File | Summary |
|------|---------|
| `uilayers/templates/home/sections/_hero.html` | Removed duplicate inline rotation `<script>` (16 lines). Hero HTML structure unchanged. |

---

## Commit Message (Suggested)

```
fix: remove duplicate hero rotation script causing is-active class conflict

Two setInterval(10000) calls were fighting over hero image .is-active class.
Removed inline script from _hero.html; canonical rotation in _home_js.html retained.
```

---

**Session Status**: ✅ READY FOR COMMIT  
**Quality**: Surgical Fix — Single File, Single Purpose
