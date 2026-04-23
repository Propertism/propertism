---
inclusion: auto
---

# Propertism Project - Session Context

## Design Specs (Named References)

### h2-base-style
The canonical section title style used across all landing sections.
- `font-family`: Playfair Display (`var(--font-display)`)
- `font-size`: `clamp(2.5rem, 5vw, 3.5rem)` → 40px–56px
- `font-weight`: 400
- `color`: `var(--gray-900)`
- Source: `static/css/propertism-styles.css` → `.section-intro-center h2`
- Mobile override: `1.5rem !important` (`mobile-layout.css`)

### p-base-style (subtitle)
The canonical section subtitle style used across all landing sections.
- `font-size`: `1.125rem` (18px)
- `color`: `var(--gray-600)`
- `line-height`: 1.7
- `margin`: 0 auto
- Source: `static/css/propertism-styles.css` → `.section-intro-center p`

## Current Session State
**Last Updated**: April 22, 2026
**Status**: All major tasks completed ✅

## Quick Reference Documents
When starting a new session or continuing work, always read these documents first:

### Primary Session Summaries
1. **SESSION-SUMMARY-FINAL-22-APR-2026.md** - Comprehensive summary of all UI enhancements, design system compliance, and management team deployment
2. **SESSION-SUMMARY-22-APR-2026.md** - Detailed UI refinements for chat button, contact icons, and footer typography

### Key Documentation
- **MEDIA-STORAGE-SETUP.md** - S3 configuration guide for persistent media storage
- **UI-FIXES-SUMMARY.md** - Historical UI fixes and refinements
- **FOOTER-UPDATES-SUMMARY.md** - Footer-specific changes
- **LANDING-PAGE-REFINEMENT.md** - Landing page improvements

## Recent Major Accomplishments

### ✅ Management Team Deployment (CRITICAL)
**Date**: April 22, 2026 13:22:27 UTC
**Status**: Successfully deployed to production

**Problem**: Production database had 0 team members, management section was empty
**Solution**: Created postdeploy hook with standalone script to load team data
**Result**: 3 team members now live on production

**Team Members**:
1. Mr. Tamilselvan - Managing Partner
2. Mr. Lawrence Manickam - Technology Partner
3. Mr. Raju Packianathan - Co-Founder

**Verification**: https://propertism.in/#management-section

**Files Created**:
- `load_team_members.py` - Standalone script (USED)
- `content/management/commands/load_team_members.py` - Django command (backup)
- `team_members_fixture.json` - Fixture data (backup)
- `.platform/hooks/postdeploy/99_load_team_members.sh` - Deployment hook

### ✅ Design System Compliance
**Specifications**: SCCB-PR-FE-012, SCCB-PR-FE-013

**Radius Standards**:
- Buttons: 6px
- Cards: 10px
- Panels: 14px

**Gradient Standards**:
- Light Cards: `#ffffff → #f9f9f7`
- Testimonial/Blog: `#ffffff → #f7f7f5`
- Light Panels: `#ffffff → #f4f4f2`
- Dark Panels: `#0f1c2e → #16263d`
- Primary Buttons: `#1c2b45 → #0f1c2e`

### ✅ Navigation Updates
**Added**: About, Quote links
**Fixed**: Management team anchor to `/#management-section`
**Order**: Home, Services, About, Management, Reviews, Properties, Blog, Quote

### ✅ Social Strip Enhancements
- Vertical "Contact" label (mustard gold #C9A961)
- Vertically centered with hero section
- Chat button hidden per user request
- Subtle charcoal border

### ✅ Scrollbar Styling
- 6px hairline width
- Subtle charcoal background: `rgba(45, 55, 72, 0.08)`
- Cross-browser support

## Development Environment

### Local Testing
- **URL**: http://127.0.0.1:8001/
- **Port**: 8001 (NOT 8000)
- **Hard Refresh**: Ctrl+Shift+R (required after CSS changes)

### Production
- **URL**: https://www.propertism.in
- **Deployment**: GitHub Actions CI/CD (automatic on push to main)
- **DO NOT**: Run `eb deploy` manually - CI/CD handles it

### Common Commands
```bash
# Collect static files after CSS changes
python manage.py collectstatic --noinput

# Git workflow (use git add -A or let user specify)
git add -A
git commit -m "Description"
git push origin main
```

## Project Structure

### Workspace Folders
1. `d:\viji\viji-olivine\03rolledout\01propertism` - Main Django app
2. `d:\viji\viji-olivine\03rolledout\06propertism.deal.engine` - Deal engine

### Key Directories
- `static/css/` - All CSS files
- `uilayers/templates/` - Django templates
- `content/` - Django app for content management
- `.platform/hooks/` - Elastic Beanstalk deployment hooks
- `.kiro/` - Kiro configuration and steering files

## Important Notes

### CSS Changes Workflow
1. Modify CSS files in `static/css/`
2. Run `python manage.py collectstatic --noinput`
3. Hard refresh browser (Ctrl+Shift+R)
4. Test thoroughly
5. Commit and push to trigger deployment

### Database Changes
- Local uses SQLite: `db.sqlite3`
- Production uses RDS (managed by Elastic Beanstalk)
- Use Django management commands or standalone scripts for data operations
- Postdeploy hooks in `.platform/hooks/postdeploy/` run after each deployment

### Deployment Process
1. Push to GitHub main branch
2. GitHub Actions workflow triggers automatically
3. Code deployed to Elastic Beanstalk
4. Postdeploy hooks execute
5. Application restarts with new code

## Next Steps / Future Work

### Pending Items
1. **S3 Media Storage** - Implement per `MEDIA-STORAGE-SETUP.md` to prevent image loss on deployment
2. **Performance Optimization** - Consider lazy loading for images
3. **Analytics** - Track social strip engagement
4. **A/B Testing** - Test Quote CTA conversion rates

### Maintenance Tasks
- Monitor scrollbar appearance across browsers
- Verify gradient rendering on different displays
- Test navigation anchors after content updates
- Review social strip positioning on new devices

## Troubleshooting

### Common Issues
1. **CSS not updating**: Run collectstatic and hard refresh browser
2. **Images disappearing**: Need S3 setup (see MEDIA-STORAGE-SETUP.md)
3. **Management section empty**: Check team members in database
4. **Deployment fails**: Check GitHub Actions logs and EB logs

### Log Access
```bash
# Get EB logs
eb logs --all

# Check specific log file
Get-Content .elasticbeanstalk/logs/[latest]/[instance]/var/log/eb-hooks.log -Tail 100
```

## Design Principles

### Premium Luxury Feel
- No heavy shadows
- No glossy gradients (all barely perceptible)
- Brand navy + gold integrity maintained
- Minimal, sophisticated tone preserved

### Consistency
- Radius tokens used throughout
- Gradient formulas standardized
- Color palette consistent
- Spacing system maintained

### Accessibility
- Sufficient contrast ratios
- Touch targets adequate (44px minimum)
- Keyboard navigation functional
- Screen reader friendly

---

**Remember**: Always read SESSION-SUMMARY-FINAL-22-APR-2026.md at the start of each session for complete context!
