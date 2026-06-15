<!-- OLIVINE-PLATFORM-META -->
# Commit Manifest - 2026-05-21 18:46 IST

**Project**: Propertism Realty Advisors LLP  
**Session ID**: `CODEX-SESSION-2105`  
**Focus**: OG V5 Lock, Metadata Retune, And CI/CD Trigger

## Summary
- Reviewed Facebook, LinkedIn, and WhatsApp OG outcomes against the approved `v5` card.
- Reverted the `v6` exploration and restored `v5` as the approved production OG image.
- Locked the new social title and description for broader NRI buy/sell/manage intent coverage.
- Switched crawler output to `og-propertism-v5.jpg` and aligned Open Graph image type to `image/jpeg`.
- Pushed `main` to trigger GitHub Actions CI/CD.

## Commit
- `c8a5cb0` - `Lock OG v5 image and update social metadata`

## Files Included In Release Commit
- `content/templatetags/seo_tags.py`
- `code-review/seo_tags.py`
- `uilayers/templates/seo/meta_tags.html`
- `code-review/meta_tags.html`
- `og-propertism.html`
- `static/images/og-propertism-v5.jpg`

## Effective Production Intent
- OG image locked to `static/images/og-propertism-v5.jpg`
- OG title locked to `Chennai Property Services for NRIs | Buy, Sell & Manage | Propertism`
- OG description locked to `Buy, sell, rent, and manage Chennai property from anywhere with trusted on-ground support, transparent updates, and dependable local execution.`

## Local Validation Performed
- `python manage.py check` -> passed
- `python manage.py collectstatic --noinput` -> passed (`1 static file copied`)

## Deployment State
- `git push origin main` completed successfully on May 21, 2026.
- GitHub Actions CI/CD was triggered from commit `c8a5cb0`.
- Production verification was **not completed in this session** and remains pending.

## Open Follow-Up
1. Confirm GitHub Actions deploy completion for `c8a5cb0`.
2. Re-run Facebook Sharing Debugger on the live site.
3. Re-run LinkedIn Post Inspector on the live site.
4. Re-test WhatsApp preview in a fresh chat.
5. Keep `v5` locked unless a future thumbnail-first redesign is explicitly approved.
