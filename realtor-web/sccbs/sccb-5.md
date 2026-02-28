SCCB-5
Title: Background-Led Modern Refactor – Propertism Visual Evolution
Scope: Web UI Refactor (Visual + Layout Strategy)
Reference: https://www.propertism.com/ (Legacy Baseline)
Impact: UI Layer Only – No API / No CMS / No Mobile Impact
Status: Governance Issue

=============================================================
1. OBJECTIVE
=============================================================

Refactor the existing Propertism-style website into a modern,
structured, premium real estate interface while:

• Retaining strong background-image presence
• Removing dated layout patterns
• Introducing modern layout discipline
• Preserving brand seriousness
• Avoiding template/SaaS appearance

This is a modernization directive, not a redesign for trend adoption.

=============================================================
2. LEGACY SITE ANALYSIS (STRUCTURAL)
=============================================================

Observed characteristics of original site:

• Heavy background imagery
• Centered content blocks
• Dated spacing rhythm
• Weak typography hierarchy
• Limited contrast layering
• Generic section transitions
• Minimal grid sophistication

Core asset to preserve:
→ Background-driven visual presence

Core aspects to replace:
→ Layout structure
→ Typography scale
→ Section rhythm
→ Hierarchy clarity
→ Interaction polish

=============================================================
3. MODERNIZATION STRATEGY
=============================================================

We retain:
• Full-width background hero
• Strong property imagery
• Visual-first storytelling

We introduce:
• Structured grid overlays
• Sharp edge alignment
• Typography hierarchy refinement
• Controlled layering
• Section contrast shifts
• Editorial spacing

No card-heavy SaaS blocks.
No rounded UI.
No marketing gimmicks.

=============================================================
4. HERO RECONSTRUCTION STANDARD
=============================================================

Maintain:
Full-width background image

Modernize via:

• Dark overlay for readability
• Left-aligned structured content
• Constrained text width
• Gold accent highlight
• Strong typographic scale
• Sharp-edged CTA

Implementation Structure:

<section class="relative min-h-[90vh] flex items-center text-white">

  <div class="absolute inset-0">
    <img src="/static/images/hero-bg.jpg"
         class="w-full h-full object-cover" />
    <div class="absolute inset-0 bg-black/60"></div>
  </div>

  <div class="relative z-10 max-w-7xl mx-auto px-8">

    <h1 class="text-5xl lg:text-6xl font-light tracking-tight max-w-2xl">
      Premium Properties
      <span class="block text-[#B89A4A] mt-3">
        Across Chennai
      </span>
    </h1>

    <p class="mt-8 text-lg text-gray-300 max-w-xl">
      Curated residential and investment-grade real estate opportunities.
    </p>

    <div class="mt-10">
      <a href="/properties"
         class="border border-[#B89A4A] px-10 py-4
                uppercase tracking-widest text-sm
                hover:bg-[#B89A4A] hover:text-black
                transition-colors">
        View Listings
      </a>
    </div>

  </div>
</section>

Modernization achieved through:
• Alignment discipline
• Layered overlay control
• Structured content width
• Controlled contrast

=============================================================
5. SECTION TRANSITION STRATEGY
=============================================================

Legacy issue:
Flat section stacking without contrast rhythm.

New rule:
Alternate section contrast.

Dark (image-led) → White (content-led) → Neutral (data-led)

Spacing standard:
Minimum py-24 per major section.

=============================================================
6. BACKGROUND IMAGE POLICY
=============================================================

Background images must:

• Be high-resolution
• Use controlled overlay (40–65% black)
• Maintain text readability ratio (WCAG AA)
• Avoid busy visual clutter
• Avoid parallax gimmicks

Image should support content, not overpower it.

=============================================================
7. TYPOGRAPHY MODERNIZATION
=============================================================

Headlines:
Serif-based
Large scale
Minimal weight (light/regular)

Body:
Neutral sans
Comfortable line height

Remove:
• All-caps overload
• Dense stacked text
• Decorative subhead clutter

=============================================================
8. PROPERTY PRESENTATION UPGRADE
=============================================================

Replace legacy boxed presentation with structured grid.

Standard grid:

grid-cols-1
sm:grid-cols-2
lg:grid-cols-3
gap-12

Each property block:

Image (full bleed within block)
Title
Location
Price

No rounded corners.
No shadow cards.
No bordered shells.

Separation through spacing only.

=============================================================
9. NAVIGATION MODERNIZATION
=============================================================

Replace dated navbar with:

• Solid background
• Sharp lower border
• Structured alignment
• Gold accent hover
• No floating glass
• No rounded link pills

Navigation must feel architectural, not decorative.

=============================================================
10. INTERACTION POLICY
=============================================================

Allowed:
• Color transitions
• Opacity fade

Disallowed:
• Bounce animations
• Scaling hover zoom
• Heavy motion effects
• Marketing counters

Motion must remain minimal and professional.

=============================================================
11. PERFORMANCE DIRECTIVE
=============================================================

Background images:
• Lazy-loaded below fold
• WebP preferred
• Compressed for 4G

Hero image:
• Optimized for fast first paint
• No excessive video background

Maintain Lighthouse performance discipline.

=============================================================
12. ACCEPTANCE CRITERIA
=============================================================

The refactored site must:

• Retain background-driven visual identity
• Look modern without looking trendy
• Feel premium without appearing templated
• Demonstrate strong layout structure
• Maintain sharp, disciplined edges
• Use restrained accent color
• Reflect investment-grade credibility

If the interface resembles a Tailwind demo,
it fails compliance.

=============================================================

SCCB-5 STATUS: APPROVED
Type: Background-Led Modern Refactor
Scope: Web UI Only
Technical Risk: None
Architectural Impact: Zero
Governance Level: Visual Modernization Standard
=============================================================