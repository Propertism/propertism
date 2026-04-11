# Propertism: NRI-First SEO Strategy — Next Steps

Following the successful deployment of the **Infinite NRI Landing Page Engine**, these are the prioritized next steps to maximize ROI and scale the platform.

---

## 1. Google Search Console (Immediate Action)
- [ ] **Re-submit Sitemap**: Submit `http://propertism.in/sitemap.xml` to trigger immediate crawling of the **High ROI (1.0 Priority)** funnels.
- [ ] **Monitor Indexing**: Track how quickly the `/nri-location/city-intent/` patterns are being indexed compared to legacy domestic pages.

## 2. Content Expansion (Ongoing Optimization)
- [ ] **Refine `seo_content`**: Focus on the top 12 intents in `intent_mapping.py`. Enhance the `seo_content` field with city-specific legal and trust signals (e.g., mention specific neighborhoods in Chennai popular with NRIs).
- [ ] **City Hub Visuals**: Update `city_hub.html` to have a premium "investor gateway" feel, grouping NRI services separately from domestic listings.

## 3. High-Value Scaling (Phase 2 Cities)
- [ ] **Add Geo-Specific Hubs**: Once Phase 1 (Chennai/Bangalore/Hyderabad) stabilizes, add one-line configs for:
    - Pune (Strong NRI manufacturing base in Germany/USA)
    - Mumbai (High-ticket luxury NRI segment)
- [ ] **Add NRI Locations**: Expand the `NRI_LOCATIONS` registry to include:
    - `melbourne-australia`
    - `san-francisco-ca`
    - `riyadh-saudi-arabia`

## 4. Conversion & Analytics (Visibility Layer)
- [ ] **Trace Clicks**: In Google Analytics, create a custom dimension for `audience_type` (NRI vs Domestic) to validate the **80/20 traffic goal**.
- [ ] **A/B Test CTAs**: Test the performance of *"Talk to NRI Expert"* vs *"Manage My Property from Abroad"*.

## 5. Technical Maintenance
- [ ] **Performance Audit**: As the engine generates 500+ pages, monitor the load time of `landing_page.html`. Consider fragment caching for the `lp-listings` block.
- [ ] **Lead Pipeline**: Ensure the `newsletter_subscribe` and WhatsApp triggers are correctly logging the `nri_location` in the backend for sales team context.

---

**Current Engine Status**: Config-driven, Zero Duplication, Scale-ready.  
**Primary Focus**: Market-wide NRI discovery via localized geo-funnels.
