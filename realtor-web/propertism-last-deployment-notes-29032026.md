# Propertism Last Deployment Notes - March 29, 2026

## Scope
This note records the production recovery, homepage fixes, GitHub pushes, and Elastic Beanstalk deployments completed on March 29, 2026.

## Starting Point
1. Work resumed from `realtor-web/.session-tracker/SESSION_TRACKER.md`.
2. Session 12 had introduced hero rotation and the customer review carousel locally, but the release state was not fully pushed/deployed.
3. During recovery, an outdated branch line was accidentally force-pushed and deployed, causing the live site to show an older homepage version.

## Recovery Timeline

### 1. Source-Of-Truth Recovery
1. Confirmed with project owner that the local folder
   - `D:\viji\viji-olivine\03rolledout\01propertism`
   was the latest source of truth.
2. Used full-workspace snapshot workflow:
   - created branch `snapshot/local-source-of-truth-20260329`
   - staged with `git add -A`
   - committed `6a0b5b8 Snapshot full local workspace as source of truth`
3. Pushed the safety branch and updated top-level `main`.
4. Deployed recovery build to Elastic Beanstalk:
   - `app-260329_182904704753`
5. Verified environment recovered to green.

### 2. Chat Restoration
1. Investigated missing live chat widget.
2. Found that shared base template was no longer loading:
   - `static/css/chat-widget.css`
   - `static/js/chat-widget.js`
3. Restored those includes in:
   - `uilayers/templates/base.html`
4. Committed top-level change:
   - `545b0bf Restore chat widget asset loading`

### 3. Review Carousel And Property Card Fixes
1. Increased slide indicator spacing for customer reviews.
2. Fixed mobile review card/slide behavior.
3. Added safer property image handling:
   - template fallback to placeholder image
   - backend `Property.get_display_image_url()` to use the first valid existing file
4. Updated homepage/property queries to prefetch `photos`.
5. Fixed EB safe bundle script so `media/` is no longer excluded in future custom bundles.
6. Committed top-level change:
   - `c39b610 Fix property image fallbacks and review indicator spacing`

### 4. Push And Deploy After GitHub Auth Repair
1. GitHub push was blocked because Git Credential Manager was authenticating as:
   - `vijaympgs`
2. Re-authenticated GitHub correctly for repository access.
3. Pushed top-level `main`.
4. Deployed updated build:
   - `app-09a9-260329_184842196666`

### 5. Production Investigation After Partial Mismatch
1. Live property cards still showed broken images.
2. Browser inspection confirmed current backend rows referenced missing files:
   - `/media/properties/WhatsApp_Image_2026-03-23_at_10.01.41_PM.jpeg`
   - `/media/properties/1772514993415.jpg`
3. Also confirmed production HTML was still being packaged from the committed state inside `realtor-web`, not simply from top-level uncommitted files.

### 6. Deploy-Source Snapshot Inside `realtor-web`
1. Committed the current deployable app workspace inside `realtor-web`:
   - `ce604e3 Snapshot current realtor-web workspace for deployment`
2. Deployed that snapshot:
   - `app-ce60-260329_190148986834`
3. Result:
   - updated homepage/review layout finally appeared live
   - property cards fell back safely instead of showing broken icons

### 7. Restore Missing Property Media Filenames
1. Located bundled property images available locally under:
   - `realtor-web/media/properties/`
2. Recreated the two missing production filenames so the current backend records would resolve to real images:
   - `media/properties/WhatsApp_Image_2026-03-23_at_10.01.41_PM.jpeg`
   - `media/properties/1772514993415.jpg`
3. Committed local deploy-source media restore:
   - `1b037ba Restore missing featured property media files`
4. Final redeploy:
   - `app-1b03-260329_190544327799`
5. Final verification:
   - featured property images load with real pixels
   - customer review indicators render with `10px` gap and `24px` top margin
   - chat widget visible
   - mobile/web homepage behavior correct

## Final Git State

### Top-Level Repository
1. Latest pushed commit:
   - `e1b505d Restore featured property media and sync live homepage fixes`
2. Status:
   - `main` pushed to GitHub
   - top-level repo clean and aligned with `origin/main`

### Local Deploy Commits Inside `realtor-web`
1. Local deploy-source commits used for production packaging:
   - `ce604e3 Snapshot current realtor-web workspace for deployment`
   - `1b037ba Restore missing featured property media files`
2. These were used to create the final live EB application versions on March 29, 2026.

## Elastic Beanstalk Deployments Performed Today
1. `app-260329_182904704753`
   - recovery from full local source-of-truth snapshot
2. `app-09a9-260329_184842196666`
   - chat restore and homepage fixes after GitHub auth repair
3. `app-ce60-260329_190148986834`
   - deploy from current `realtor-web` committed workspace snapshot
4. `app-1b03-260329_190544327799`
   - final deployment after restoring missing featured property media filenames

## Final Production Verification
1. Environment:
   - `propertism-prod`
2. Status:
   - `Ready`
3. Health:
   - `Green`
4. Final deployed version:
   - `app-1b03-260329_190544327799`
5. Live confirmations:
   - chat restored
   - property images visible
   - customer review dots spaced correctly
   - mobile and web homepage behavior confirmed

## Key Files Touched During March 29, 2026 Recovery
- `realtor-web/uilayers/templates/base.html`
- `realtor-web/uilayers/templates/home-premium.html`
- `realtor-web/uilayers/templates/components/_property-card.html`
- `realtor-web/static/css/mobile-layout.css`
- `realtor-web/static/css/propertism-styles.css`
- `realtor-web/content/views.py`
- `realtor-web/uilayers/views.py`
- `realtor-web/properties/models.py`
- `realtor-web/scripts/build-eb-bundle.ps1`
- `realtor-web/media/properties/WhatsApp_Image_2026-03-23_at_10.01.41_PM.jpeg`
- `realtor-web/media/properties/1772514993415.jpg`

## Operator Notes
1. If future Elastic Beanstalk deploys must exactly match the current app workspace, ensure the deploy source being archived is the intended committed state before running `eb deploy`.
2. If featured property records are updated in admin, confirm the underlying media files exist under `media/properties/`.
3. The top-level GitHub repo now reflects the final source changes that correspond to the live homepage fixes completed on March 29, 2026.
