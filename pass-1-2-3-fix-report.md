# Pass 1, 2, 3 Fix Report

Date: April 12, 2026
Project: Propertism
Prepared for: Mindra
Scope: Detailed implementation report for the sell-first SEO alignment program across Pass 1, Pass 2, and Pass 3

## Purpose

This report summarizes what was implemented across the first three SEO and conversion passes in Propertism, why each pass mattered, which files were changed, what business or technical problem each pass solved, and what remains intentionally deferred.

This document is meant to be a clean architect-facing implementation report, separate from the larger strategic audit.

## Overall Outcome

Across the three passes, the landing engine was moved from:

- a dynamic but broadly mixed NRI listing system

to:

- a sell-first, service-led, intent-aware landing engine with stronger NRI geo continuity, stronger conversion behavior, and stronger authority flow

In practical terms:

- Pass 1 fixed SEO architecture
- Pass 2 activated conversion and trust layers
- Pass 3 reinforced service-cluster authority through city hubs and sitemap weighting

The core routing system was intentionally preserved.

## Pass 1: Structural SEO Alignment

## Objective

Pass 1 was focused on aligning the existing dynamic landing engine to the business model without rewriting the routing architecture.

Main goals:

- introduce sell-first intent semantics
- preserve backward compatibility for older slugs
- make landing behavior intent-aware, not only audience-aware
- fix NRI geo continuity in related links
- upgrade metadata control

## What Was Implemented

### 1. Intent Re-Architecture

The primary source of truth in `content/intent_mapping.py` was upgraded to reflect a sell-first model.

Implemented:

- added `nri-sell-property`
- added `nri-rental-management`
- added `manage-property-from-abroad`
- preserved legacy aliases so existing URLs and references do not break

Alias handling added:

- `nri-resale-assistance` → `nri-sell-property`
- `nri-tenant-management` → `nri-rental-management`
- related service aliases were retained for compatibility

This changed the engine from business-internal naming toward search-facing naming.

### 2. Intent Family System

Each intent now carries stronger semantic classification through fields such as:

- `intent_type`
- `priority`

Intent families now include:

- `sell`
- `management`
- `rental`
- `maintenance`
- `informational`
- `buy`

This created the foundation for:

- intent-aware hero logic
- intent-aware SEO content
- intent-aware CTA behavior
- service-priority ordering

### 3. NRI Geo Continuity Fix

`content/views_landing.py` was updated so NRI landing pages preserve geo context in generated links instead of dropping users into domestic-style paths.

Before:

- related links from NRI pages fell back to `/<city>/<intent>/`

After:

- related links preserve the NRI route format when `nri_origin` exists

This fixed:

- geo crawl continuity
- NRI funnel continuity
- contextual consistency across service pages

### 4. Metadata Control Upgrade

The SEO tag generator was extended in `content/templatetags/seo_tags.py`.

Added support for:

- `canonical_override`
- `keywords`

Template rendering was updated in `uilayers/templates/seo/meta_tags.html` and `uilayers/templates/landing_page.html`.

This gave the engine:

- optional canonical control
- optional `meta keywords` output
- cleaner page-level metadata extensibility

### 5. Intent-Aware Rendering Shift

The shared landing template was preserved, but behavior was moved away from simple `is_nri` branching.

Updated:

- `uilayers/templates/landing_page.html`
- `uilayers/templates/components/_lp_seo_content.html`

Result:

- sell pages now receive sell-oriented advisory content
- management pages now receive management-oriented content
- rental, maintenance, informational, and buy pages can each behave differently

This was the most important architectural shift in Pass 1.

## Files Changed in Pass 1

- [content/intent_mapping.py](D:/viji/viji-olivine/03rolledout/01propertism/content/intent_mapping.py)
- [content/views_landing.py](D:/viji/viji-olivine/03rolledout/01propertism/content/views_landing.py)
- [content/templatetags/seo_tags.py](D:/viji/viji-olivine/03rolledout/01propertism/content/templatetags/seo_tags.py)
- [uilayers/templates/landing_page.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/landing_page.html)
- [uilayers/templates/seo/meta_tags.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/seo/meta_tags.html)
- [uilayers/templates/components/_lp_seo_content.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/components/_lp_seo_content.html)

## Pass 1 Outcome

Pass 1 solved the architecture problem.

It established:

- sell as a first-class intent
- stronger search-facing semantics
- intent-driven rendering
- canonical and metadata control
- NRI geo link continuity

Pass 1 did not yet fully solve conversion behavior. That was deferred to Pass 2.

## Pass 2: Conversion and Trust Layer

## Objective

Pass 2 was focused on turning sell pages from improved content pages into stronger conversion pages.

Main goals:

- add visible sell-specific CTAs
- add process and trust layers
- add FAQ visibility and structured data
- add service schema
- strengthen intent-priority behavior inside the page experience

## What Was Implemented

### 1. Sell CTA Module

A dedicated sell CTA component was introduced:

- [uilayers/templates/components/_lp_sell_cta_block.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/components/_lp_sell_cta_block.html)

This module includes sell-focused calls to action such as:

- Get Free Property Valuation
- Start Selling Process
- See NRI Sell FAQs

The goal was to shift sell pages from generic enquiry posture to sell conversion posture.

### 2. Sell Process Layer

`content/views_landing.py` was extended to generate structured sell process steps.

These steps help communicate:

- end-to-end support
- remote execution confidence
- process clarity for NRIs selling from abroad

This improves both:

- conversion readiness
- content specificity

### 3. Sell FAQ Layer

Pass 2 added visible FAQ content for sell pages and matching schema output.

Implemented:

- FAQ generation in `content/views_landing.py`
- visible FAQ component in [uilayers/templates/components/_lp_faq.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/components/_lp_faq.html)
- FAQ schema generation in `content/templatetags/seo_tags.py`

This created:

- visible user-helpful content
- schema support aligned to on-page content

### 4. Service Schema Addition

`content/templatetags/seo_tags.py` was extended to generate service-oriented schema for service landing pages.

This was added for service-led intent families such as:

- sell
- management
- rental
- maintenance

This strengthens the trust and search-entity layer beyond generic property schema.

### 5. Review and Trust Layer

Sell pages were connected to existing review content so they can display trust signals when available.

This is visible inside the sell CTA block and makes the page behave more like a service landing page rather than a generic discovery page.

### 6. Sell-Aware Listing CTA

Inline CTA behavior inside listings was adjusted so sell pages continue the sell-specific conversion pattern rather than falling back to generic lead prompts.

Updated:

- [uilayers/templates/components/_lp_listings.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/components/_lp_listings.html)

### 7. Styling Support

New styling was added in:

- [static/css/landing-premium.css](D:/viji/viji-olivine/03rolledout/01propertism/static/css/landing-premium.css)

This supports:

- sell CTA layout
- sell process steps
- review cards
- FAQ layout

## Files Changed in Pass 2

- [content/views_landing.py](D:/viji/viji-olivine/03rolledout/01propertism/content/views_landing.py)
- [content/templatetags/seo_tags.py](D:/viji/viji-olivine/03rolledout/01propertism/content/templatetags/seo_tags.py)
- [uilayers/templates/landing_page.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/landing_page.html)
- [uilayers/templates/components/_lp_sell_cta_block.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/components/_lp_sell_cta_block.html)
- [uilayers/templates/components/_lp_faq.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/components/_lp_faq.html)
- [uilayers/templates/components/_lp_listings.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/components/_lp_listings.html)
- [static/css/landing-premium.css](D:/viji/viji-olivine/03rolledout/01propertism/static/css/landing-premium.css)

## Pass 2 Outcome

Pass 2 solved the revenue activation problem at page level.

It added:

- sell-specific conversion components
- visible process logic
- sell FAQ visibility
- service schema
- stronger trust presentation

After Pass 2, sell pages no longer behaved like mere content variants. They began behaving like service conversion pages.

## Pass 3: Hub and Authority Flow Reinforcement

## Objective

Pass 3 was focused on strengthening service-cluster authority at hub and sitemap level.

Main goals:

- make city hubs reflect the new revenue model
- prioritize service intents visually
- reinforce sell, management, and rental as core paths
- make sitemap weighting match business value

## What Was Implemented

### 1. City Hub Re-Architecture

`content/views_landing.py` city hub logic was reworked so intent collections are grouped by service value rather than being presented as a generic mixed set.

New groups:

- `featured_service_intents`
- `service_cluster_intents`
- `supporting_intents`

This allows the hub to clearly separate:

- primary NRI service paths
- secondary service cluster links
- lower-priority buy or support searches

### 2. Service-Led City Hub Messaging

City hub title and description were updated to support a service-led model rather than a broad listing posture.

This moves the city hub closer to:

- NRI service discovery

rather than:

- general property browsing

### 3. New City Hub Template

The old generic city hub layout was replaced with a service-first hub in:

- [uilayers/templates/city_hub.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/city_hub.html)

The new hub emphasizes:

- Primary NRI Service Paths
- Service Cluster
- Supporting Property Searches

This means sell, management, and rental now lead the experience.

### 4. Sitemap Weighting Alignment

`content/sitemaps.py` was rewritten so sitemap priorities follow intent value instead of older mixed logic.

New practical hierarchy:

- sell highest
- management next
- rental next
- maintenance next
- informational after that
- buy lowest

This aligns crawl signaling with business value and internal authority design.

## Files Changed in Pass 3

- [content/views_landing.py](D:/viji/viji-olivine/03rolledout/01propertism/content/views_landing.py)
- [uilayers/templates/city_hub.html](D:/viji/viji-olivine/03rolledout/01propertism/uilayers/templates/city_hub.html)
- [content/sitemaps.py](D:/viji/viji-olivine/03rolledout/01propertism/content/sitemaps.py)

## Pass 3 Outcome

Pass 3 solved the authority-distribution problem.

It ensured:

- the hub experience matches the sell-first strategy
- service paths are visually dominant
- sitemap priorities reinforce sell-first crawling
- internal authority is better aligned with revenue priorities

## Verification

Verification performed after implementation:

- ran `python manage.py check`
- result: passed with no Django issues

Known warning:

- existing third-party `pkg_resources` deprecation warning from `rest_framework_simplejwt`

No new Django validation issues were introduced by these passes.

## Architectural Summary for Mindra

### What Pass 1 Solved

- SEO architecture alignment
- sell-first intent introduction
- alias-safe slug migration
- metadata control
- intent-aware rendering
- NRI geo continuity

### What Pass 2 Solved

- sell-page conversion activation
- FAQ visibility and FAQ schema
- service schema
- trust layer and process layer
- stronger sell-specific CTA behavior

### What Pass 3 Solved

- service-cluster prominence in city hubs
- sell-first visual hierarchy
- sitemap alignment with business value
- stronger authority flow

## What Was Intentionally Not Changed

The following items were intentionally deferred:

- no routing migration to `/nri/<geo>/<city>/<intent>/`
- no split into separate templates by audience
- no major buy-page expansion
- no analytics event layer yet
- no broader review schema layer beyond current service and FAQ additions

These were deferred to keep risk low while maximizing architectural gain.

## Final Assessment

The combined effect of Pass 1, 2, and 3 is that Propertism is no longer only a dynamic landing-page engine with NRI support.

It is now materially closer to:

- an NRI property problem-solving platform

because the system now reflects that positioning at:

- intent level
- metadata level
- rendering level
- CTA level
- schema level
- hub structure level
- sitemap weighting level

That is the major implementation outcome.

## Pass 4A: Lead System Activation (Short Fix Report)

## Objective

Pass 4A moved the landing engine from “conversion-ready” to “lead-capturing,” with a minimal-risk, intent-aware lead form and GA4-ready tracking.

## What Was Implemented

- Standardized sell, management, and rental primary CTAs to `Get Property Valuation` in `uilayers/templates/landing_page.html` and supporting components.
- Added a 2-step landing lead form with intent-specific fields in `uilayers/templates/components/_lp_lead_form.html`.
- Added the `LandingLead` model and admin registration in `content/models.py` and `content/admin.py`, with `intent_type`, `geo_origin`, and qualification data.
- Added a dedicated landing lead endpoint at `POST /api/landing-lead/` in `content/views.py`, wired in `content/urls.py`.
- Added GA4-ready events (`cta_click`, `lead_form_start`, `lead_form_submit`) and lead-form flow in `static/js/landing-conversion.js`.
- Added lead-form styling and responsive behavior in `static/css/landing-premium.css`.
- Added a migration `content/migrations/0013_landinglead.py`.
- Added a minimal API test in `content/tests.py`.

## Outcome

- Landing pages now capture intent-qualified leads with geo context.
- Sell, management, and rental flows use consistent, measurable CTAs.
- Lead capture is centralized and does not fork the existing notification system.

## Verification Status

- Python runtime was not available in this shell, so `manage.py check`, `migrate`, and tests could not be run here.
- Migration and tests were added manually and should be run locally:

```powershell
python manage.py migrate
python manage.py check
python manage.py test content.tests.LandingLeadApiTests
```

## Pass 4B: Lead Optimization + Authority Scale (Short Fix Report)

## Objective

Pass 4B focused on lead quality, sell-intent dominance, and controlled authority expansion without touching routing.

## What Was Implemented

- Added lead scoring and categorization (`lead_score`, `lead_category`) plus follow-up fields in `content/models.py`.
- Added admin prioritization (score sorting + hot/warm/cold badge) in `content/admin.py`.
- Added a post-submit micro-conversion step with optional follow-up (`expected_price_range`, `preferred_contact_time`) in `uilayers/templates/components/_lp_lead_form.html`.
- Added a follow-up API endpoint `POST /api/landing-lead/followup/` in `content/views.py` and wired it in `content/urls.py`.
- Added new informational support intents and linked them into the sell cluster in `content/intent_mapping.py`.
- Expanded NRI geo coverage (`abu-dhabi`, `kuwait`, `saudi`, `malaysia`) in `content/intent_mapping.py`.
- Added `lead_scored` and `lead_qualified` events, plus WhatsApp fallback on lead drop-off in `static/js/landing-conversion.js` and `static/css/landing-premium.css`.
- Added migration `content/migrations/0014_landinglead_scoring.py`.

## Outcome

- Leads are now scored and classified at capture time for faster follow-up.
- Sell pages gain higher-quality lead signal via micro-conversion inputs.
- Authority scale improved via legal/tax/POA support intents and new NRI geos.

## Verification Status

- Python runtime was not available in this shell, so `manage.py check`, `migrate`, and tests could not be run here.
- Migrations should be applied locally:

```powershell
python manage.py migrate
python manage.py check
python manage.py test content.tests.LandingLeadApiTests
```
