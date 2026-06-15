<!-- OLIVINE-PLATFORM-META -->
# Commit Details - 2026-05-20 22:44 IST

## Session
- **Project:** Propertism Realty Advisors LLP
- **Session ID:** `CODEX-SESSION-2005`
- **Focus:** Social Preview Stabilization & OG Platform Lock
- **Agent:** Astra

## Objective
Stabilize and lock Propertism social-preview rendering across LinkedIn, Facebook, and WhatsApp while preserving server-rendered metadata correctness and production reliability.

## Commit Chain
1. `a469094` - Refine OG card hierarchy for social preview
2. `968f119` - Update OG thumbnail to v3
3. `f846c2d` - Extend OG description for LinkedIn
4. `2352c67` - Harden LinkedIn fallback metadata
5. `c3d0cdf` - Promote OG image to v4

## Production Outcome
- **Environment:** `propertism-prod-2026`
- **Region:** `us-east-1`
- **Final Deployed Version:** `gh-127-c3d0cdfb52551de0415590f03ce9b4e75f7a8f2c`
- **Status:** `Ready`
- **Health:** `Green`

## Final Live Metadata Lock
- **Title:** `Chennai Property Management for NRIs | Propertism`
- **Meta Description:** `Trusted Chennai property management for NRIs. Buy, sell, rent and manage property from anywhere.`
- **og:title:** `NRI Property Management Chennai | Propertism`
- **og:description:** `Buy, sell, rent, and manage Chennai property from anywhere with trusted on-ground support, transparent updates, and dependable local execution.`
- **og:image:** `https://www.propertism.in/static/images/og-propertism-v4.png`
- **twitter:image:** `https://www.propertism.in/static/images/og-propertism-v4.png`

## Validation Matrix
- **LinkedIn Post Inspector:** Correct image, title, domain; description crawler-visible, feed rendering accepted as platform-limited.
- **Facebook Share Output:** Excellent final rendering; approved.
- **WhatsApp Share Output:** Correct image, title, description, and domain; approved.
- **Raw HTML View Source:** Single server-rendered OG/Twitter/meta set with absolute URLs and no duplicates.

## Root Cause Summary
- The original issue was not missing metadata but a combination of small-card image density and LinkedIn-specific preview presentation limits.
- Facebook and WhatsApp rendered description lines more fully than LinkedIn.
- Final improvements came from:
  - simplifying image hierarchy,
  - cache-busting image URLs (`v3`, then `v4`),
  - tightening browser title and standard meta description,
  - preserving OG/Twitter stability.

## Files Changed In Production Path
- `content/templatetags/seo_tags.py`
- `uilayers/templates/base.html`
- `static/images/og-propertism-v3.png`
- `static/images/og-propertism-v4.png`

## Local-Only Draft Artifacts Left Uncommitted
- `og-propertism-wa.html`
- `static/images/og-propertism-wa-draft.png`

These were intentionally not promoted to tracked repo artifacts beyond the final `v4` production image switch.

## Closure Note
Social preview state is now locked and production-verified across Facebook, LinkedIn, and WhatsApp. Further LinkedIn-only debugging should be treated as platform-limitation territory unless crawler detection itself regresses.
