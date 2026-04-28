<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-04-28 22:58:00
Last Updated By: Astra
Last Updated On: 2026-04-28 22:58:00
Searchtag:COMMITDETAILS202604282258
-->

# Commit Manifest — 2026-04-28 22:58 IST

## Session Title
**Propertism Premium UI Hardening — Hero, About, Contact, Footer**

## Scope
- **Workspace**: `D:\viji\viji-olivine\03rolledout\01propertism`
- **Domain**: Propertism Frontend (Production)
- **Sections Touched**: Hero, Trust Strip, About, Contact, Footer

---

## SCCB Registry

| SCCB ID | Title | Status |
|---------|-------|--------|
| SCCB-RECOVERY-013 | Hero 100% Clarity — Remove all blur/dim/overlay | ✅ COMPLETE |
| SCCB-RECOVERY-014 | Trust Strip Label Visibility Recovery | ✅ COMPLETE |
| SCCB-RECOVERY-015 | Grid & Typography Alignment Pass | ✅ COMPLETE |
| SCCB-RECOVERY-016 | Final Navbar + Hero Vertical Alignment | ✅ COMPLETE |
| SCCB-AUDIT-017 | Contact "Get in Touch" Section Audit | ✅ COMPLETE |
| SCCB-PRM-CONTACT-018 | Contact Section Premium Implementation | ✅ COMPLETE |
| SCCB-PRM-ABOUT-REFINE-011 | About Section Premium Refinement (10 points) | ✅ COMPLETE |
| SCCB-PRM-ABOUT-FINAL-HIT-012 | About Section Final Polish (10 micro-refinements) | ✅ COMPLETE |
| SCCB-PRM-ABOUT-FINAL-HIT-012A | About Section Final Hit — Production Grade (11 points) | ✅ COMPLETE |
| SCCB-FOOTER-VIS | Footer Text Visibility — Comprehensive Fix | ✅ COMPLETE |
| SCCB-MAP-LINK | Google Maps iframe → Clickable Map Link | ✅ COMPLETE |

---

## Files Modified

### CSS
| File | Changes |
|------|---------|
| `static/css/propertism-premium.css` | Hero overlay removal, trust strip fix, about section premium (all 3 passes), contact section premium, footer comprehensive text visibility, map link styling |
| `static/css/viewport-section-normalization.css` | Trust strip height 130→160px, overflow fix, flex centering |

### Templates
| File | Changes |
|------|---------|
| `uilayers/templates/home/sections/_contact.html` | Removed all 15 inline styles, migrated to CSS classes, replaced map iframe with clickable link |
| `uilayers/templates/home/sections/_about.html` | Removed all inline styles from mission block, copy-stack, and paragraphs |

---

## Key Design Decisions

1. **Hero**: Total overlay removal (`::before { display: none }`). Background image renders at 100% native resolution. Text legibility via high-density text-shadows instead of dimming.

2. **About Section**: Editorial left-aligned layout with 1:1 grid. Mission card elevated with warm `#F4EFE6` background. Right panel ("Why Owners Stay") softened gradient, nudged 12px down for visual alignment.

3. **Contact Section**: Ghost classes (`contact-section-grid`, `contact-info-column`, `contact-form-column`) now have proper CSS definitions. Gold focus states on all form inputs. Premium card container for the form.

4. **Footer**: Comprehensive catch-all rule forces all `p`, `span`, `small`, `li`, `div`, `a`, `strong` inside `.site-footer` to visible colors. Phone/email links in gold.

5. **Google Maps**: Replaced iframe embed (which required Maps Embed API activation) with a premium clickable map pin link. Zero API dependency.

---

## Section Lock Status

| Section | Status |
|---------|--------|
| Hero | 🔒 LOCKED — Production Grade |
| Trust Strip | 🔒 LOCKED — Production Grade |
| About | 🔒 LOCKED — Production Grade |
| Contact | 🔒 LOCKED — Production Grade |
| Footer | 🔒 LOCKED — Production Grade |

---

## Pending / Next Steps

1. **Google Maps Embed API**: If desired in future, enable "Maps Embed API" in Google Cloud Console for the existing API key to restore the embedded map.
2. **Mobile QA**: Verify responsive behavior at 768px and 375px breakpoints.
3. **Services / Properties / Reviews / Blog sections**: Not touched in this session — available for future refinement.

---

**Session Status**: ✅ CLOSED  
**DIT Readiness**: 🟢 HIGH  
**All trackers synchronized.**
