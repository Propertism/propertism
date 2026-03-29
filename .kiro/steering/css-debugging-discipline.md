---
inclusion: auto
---

# CSS Debugging Discipline - Auto-Loaded

**CRITICAL:** Before making ANY CSS changes, follow the Deep Investigation Protocol.

## Quick Reference

**When you see CSS issues that persist after changes:**

1. **STOP** - Don't make more changes
2. **READ** - Read the COMPLETE source file (not partial sections)
3. **SEARCH** - Use grepSearch to find ALL occurrences of the selector in ALL files
4. **IDENTIFY** - List all conflicting rules with file names and line numbers
5. **REMOVE** - Remove conflicts at source (don't override with !important)
6. **CONSOLIDATE** - Put all rules in ONE location
7. **APPLY** - Make ONE comprehensive fix
8. **VERIFY** - Search again to confirm no remaining conflicts

## CSS Load Order (Highest Priority = Last)

```
1. premium-styles.css
2. propertism-styles.css  
3. mobile-layout.css
4. Template inline <style> ← LOADS LAST (WINS)
5. Inline style="" attributes
```

**Key:** Template inline styles override external CSS files.

## Common Mistakes to Avoid

❌ Making multiple incremental changes hoping one works  
❌ Using `!important` to override conflicting rules  
❌ Ignoring inline styles in templates  
❌ Skipping complete file reads  
❌ Not searching for ALL occurrences of a selector  

## What to Do Instead

✅ Do deep investigation FIRST  
✅ Remove conflicts AT SOURCE  
✅ Consolidate rules in ONE place  
✅ Apply ONE comprehensive fix  
✅ Verify no remaining conflicts  

## Reference Document

For complete protocol: `realtor-web/.session-tracker/SCCB-DEEP-INVESTIGATION-PROTOCOL-010.md`

---

**This file auto-loads in every session. Follow this discipline for all CSS changes.**
