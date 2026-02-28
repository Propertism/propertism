# SCCB-43: REALTOR WEBSITE SEO MODERNIZATION

**SCCB ID**: SCCB-43  
**SCCB Number**: SCCB-43_REALTOR_WEBSITE_SEO_MODERNIZATION  
**Date (IST)**: 25-02-2026  
**Canonical Location**: governance-canon/web/SCCB-43_REALTOR_WEBSITE_SEO_MODERNIZATION.md  
**Authority**: Viji (Product Owner) + Mindra (Architecture Guard)  
**Applies To**: Manthraa (Kiro – Web Implementation)  
**Status**: ✅ IMPLEMENTED (90% Complete)

**Implementation Date**: February 25, 2026  
**Completion Status**: 90% (9/10 tasks complete)

---

## 📁 IMPLEMENTATION FILES (Internal Tracking)

### Documentation
- `realtor-web/SEO_IMPLEMENTATION_COMPLETE.md` - Full implementation guide

### Template Tags & Helpers
- `realtor-web/content/templatetags/__init__.py` - Package init
- `realtor-web/content/templatetags/seo_tags.py` - SEO template tags

### Templates
- `realtor-web/uilayers/templates/seo/meta_tags.html` - Meta tag template
- `realtor-web/uilayers/templates/seo/structured_data.html` - Schema template
- `realtor-web/uilayers/templates/seo/property_schema.html` - Property schema
- `realtor-web/uilayers/templates/seo/breadcrumb_schema.html` - Breadcrumb schema
- `realtor-web/uilayers/templates/robots.txt` - Robots.txt template
- `realtor-web/uilayers/templates/base.html` - Updated with SEO blocks
- `realtor-web/uilayers/templates/enterprise-home.html` - Updated with SEO
- `realtor-web/uilayers/templates/services.html` - Updated with SEO

### Configuration
- `realtor-web/content/sitemaps.py` - Sitemap configuration
- `realtor-web/realtor_project/urls.py` - Sitemap/robots routes
- `realtor-web/realtor_project/settings.py` - Added django.contrib.sitemaps

### Views
- `realtor-web/content/views.py` - Updated with breadcrumb context

### Validation
- `realtor-web/validate_seo.py` - SEO validation script

### Dependencies
- `realtor-web/requirements.txt` - Added beautifulsoup4

---

## PURPOSE

Upgrade the Realtor Website to modern SEO standards using technical, semantic, and structured optimization techniques to ensure:

- High search visibility
- Proper indexing
- Rich result eligibility
- Social share optimization
- Long-term ranking stability

**This is not cosmetic SEO. This is structural search readiness.**

---

## OBJECTIVE

Ensure the website is:
- Crawlable
- Indexable
- Semantically clear
- Social-preview optimized
- Structured-data compliant
- Ready for Google ranking signals

---

## PHASE 1 — CRITICAL TECHNICAL SEO (HIGH PRIORITY)

### 1. Meta Description Optimization
- Each page must have a unique meta description (150–160 characters)
- Include primary keyword + geo modifier
- Must be compelling and conversion-driven
- No duplicates allowed

### 2. Title Tag Optimization
- Each page must have a unique title (50–60 characters)
- Format: Primary Keyword | Brand Name
- Avoid keyword stuffing
- Avoid generic titles like "Home"

### 3. Open Graph (OG) Tags
Mandatory per page:
- `og:title`
- `og:description`
- `og:image`
- `og:url`
- `og:type`

Images must be minimum 1200x630 for social preview clarity.

### 4. Twitter Card Tags
Include:
- `twitter:card` (summary_large_image)
- `twitter:title`
- `twitter:description`
- `twitter:image`

### 5. Alt Text for All Images
- Every image must have descriptive alt text
- Property images must include: Property type + location + feature
- Example: "Luxury 3BHK villa in Chennai with pool"
- No empty alt attributes unless decorative.

### 6. sitemap.xml
- Auto-generate dynamically
- Include:
  - Home
  - Listings
  - Property detail pages
  - Blog (if exists)
- Use proper lastmod timestamps
- Submit to Google Search Console after deployment

### 7. robots.txt
Must include:
- Allow public pages
- Disallow admin paths
- Reference sitemap.xml

---

## PHASE 2 — SEMANTIC & STRUCTURED DATA (MEDIUM PRIORITY)

### 8. Schema.org Structured Data
Implement JSON-LD structured data:
- RealEstateAgent schema (Organization)
- Residence / House schema for listings
- Offer schema for pricing
- BreadcrumbList schema for navigation

Ensure:
- Valid JSON-LD
- Pass Google Rich Results Test
- No spammy structured markup

---

## PHASE 3 — SEARCH PERFORMANCE OPTIMIZATION

### 9. Canonical URLs
- Add canonical tag to every page
- Prevent duplicate index paths
- Ensure HTTPS canonical reference

### 10. Google Search Console Setup
- Verify domain property
- Submit sitemap.xml
- Monitor:
  - Coverage
  - Core Web Vitals
  - Mobile usability
  - Search performance

---

## MODERN SEO ENHANCEMENTS (MANDATORY)

Manthraa must additionally implement:

- Mobile-first optimization
- Core Web Vitals improvement
  - LCP under 2.5s
  - CLS under 0.1
  - FID optimized
- Lazy loading for property images
- Compressed WebP images
- Clean URL structure: `/properties/luxury-villa-chennai`
- Internal linking between:
  - Listings
  - Similar properties
  - Location pages

---

## CONTENT STRATEGY ALIGNMENT

Each property page must include:
- Minimum 300–500 words of unique descriptive content
- Location-based keywords
- Nearby amenities context
- Natural keyword variation
- Avoid duplicate listing descriptions across pages.

---

## ACCEPTANCE CHECKLIST

Manthraa must confirm:
- [ ] All pages have unique title + meta description
- [ ] All pages include OG + Twitter tags
- [ ] All images contain meaningful alt text
- [ ] sitemap.xml generated and valid
- [ ] robots.txt configured properly
- [ ] Schema structured data passes validation
- [ ] Canonical tags implemented
- [ ] Core Web Vitals tested and optimized

---

## SUCCESS METRICS

Within 30–60 days post-deployment:
- Pages indexed in Google
- Rich results eligibility
- Improved impressions
- Ranking for geo-based property keywords
- Organic traffic increase

---

## GOVERNANCE RULES

SEO implementation must not break:
- Existing routing
- Performance
- Accessibility
- Page load speed

**No shortcut or auto-generated spam metadata allowed.**

---

This SCCB establishes a search-first foundation for the Realtor website.

**END OF SCCB**
