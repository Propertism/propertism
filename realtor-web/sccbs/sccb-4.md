SCCB-4 – ANNEXURE-A
Title: Premium Real Estate Visual Language (No Templates, No Rounded UI, No Emoji, No Startup Aesthetic)
Scope: Chennai Realtor – Web Only (UI Refinement Layer)
Impact: Styling + Layout System Only
Status: Design Correction Directive

=============================================================
1. PROBLEM STATEMENT
=============================================================

Current UI feels:
- Template-driven
- SaaS-like
- Over-rounded
- Emoji-based trust signaling
- Lacking architectural authority
- Lacking premium restraint

We are NOT building:
• A startup landing page
• A Tailwind demo template
• A colorful SaaS product

We ARE building:
• A premium Chennai real estate brand
• Architect-level seriousness
• Investor-grade confidence
• Minimal, sharp, structured layout

=============================================================
2. VISUAL PRINCIPLES (STRICT)
=============================================================

1. No rounded corners (no rounded-lg, rounded-xl, rounded-full)
2. No emojis
3. No gradient overload
4. No soft “cute” UI
5. No oversized playful buttons
6. No card-heavy SaaS layout
7. No generic Tailwind marketing patterns

Instead:

• Hard edges
• Sharp lines
• Structured grid
• Strong typography
• High-contrast hierarchy
• Spacious white rhythm
• Architectural alignment

=============================================================
3. DESIGN DIRECTION
=============================================================

Brand Tone:
Modern Architectural
Luxury Developer Brochure
Black / White / Muted Gold
Editorial spacing

Color Strategy:

Primary Background: #0F172A
Accent Gold: #B89A4A
Section White: #FFFFFF
Text Dark: #111111
Muted Grey: #6B7280

No bright greens.
No playful colors.

=============================================================
4. HERO SECTION – REVISED STRUCTURE
=============================================================

Remove:
• Big centered startup headline
• Rounded CTA
• Soft shadows
• Bright gradient background

Replace with:

Full-width structured hero:

-------------------------------------------------------------
<section class="min-h-[85vh] flex items-center bg-[#0F172A] text-white">

  <div class="max-w-7xl mx-auto px-8 grid grid-cols-1 lg:grid-cols-2 gap-16">

    <div>
      <h1 class="text-5xl lg:text-6xl font-light tracking-tight leading-tight">
        Premium Real Estate
        <span class="block text-[#B89A4A] mt-2">
          Across Chennai
        </span>
      </h1>

      <p class="mt-8 text-lg text-gray-300 max-w-xl">
        Investment-grade properties in Anna Nagar, Adyar, OMR and ECR.
      </p>

      <div class="mt-10">
        <a href="/properties"
           class="inline-block border border-[#B89A4A] px-10 py-4
                  text-sm tracking-widest uppercase
                  hover:bg-[#B89A4A] hover:text-black
                  transition-colors duration-300">
          View Listings
        </a>
      </div>
    </div>

    <div>
      <img src="/static/images/chennai-skyline.jpg"
           class="w-full h-[500px] object-cover" />
    </div>

  </div>
</section>
-------------------------------------------------------------

Why this works:
• Two-column authority
• No rounded shapes
• No playful energy
• Balanced composition
• High-end brochure style

=============================================================
5. NAVIGATION – STRUCTURED HEADER
=============================================================

Replace glass blur nav.

Use strong architectural header:

<nav class="w-full bg-[#0F172A] text-white border-b border-white/10">

  <div class="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">

    <div class="text-lg tracking-wide font-medium">
      CHENNAI REALTOR
    </div>

    <div class="space-x-12 text-sm tracking-wide uppercase">
      <a class="hover:text-[#B89A4A]">Home</a>
      <a class="hover:text-[#B89A4A]">Properties</a>
      <a class="hover:text-[#B89A4A]">About</a>
      <a class="hover:text-[#B89A4A]">Contact</a>
    </div>

  </div>
</nav>

No blur.
No floating.
No rounded.
No softness.

=============================================================
6. WHY CHOOSE US – REMOVE CARDS
=============================================================

Remove:
• Box cards
• Shadows
• Emoji icons

Replace with:

Editorial three-column grid:

<section class="py-24 bg-white">

  <div class="max-w-7xl mx-auto px-8">

    <h2 class="text-4xl font-light text-center mb-20">
      Why Clients Choose Us
    </h2>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-20 text-center">

      <div>
        <h3 class="text-lg tracking-wide uppercase mb-6 text-[#B89A4A]">
          Selection
        </h3>
        <p class="text-gray-600 leading-relaxed">
          Carefully curated properties in Chennai’s most established neighborhoods.
        </p>
      </div>

      <div>
        <h3 class="text-lg tracking-wide uppercase mb-6 text-[#B89A4A]">
          Valuation
        </h3>
        <p class="text-gray-600 leading-relaxed">
          Transparent pricing supported by deep local market expertise.
        </p>
      </div>

      <div>
        <h3 class="text-lg tracking-wide uppercase mb-6 text-[#B89A4A]">
          Execution
        </h3>
        <p class="text-gray-600 leading-relaxed">
          Structured guidance from discovery to registration.
        </p>
      </div>

    </div>
  </div>
</section>

No shadows.
No borders.
No rounded containers.

=============================================================
7. TYPOGRAPHY UPGRADE (MANDATORY)
=============================================================

Use:

Headlines: Playfair Display OR Cormorant Garamond
Body: Inter OR Neue Haas Grotesk equivalent

Tailwind config:

fontFamily: {
  serif: ['Playfair Display', 'serif'],
  sans: ['Inter', 'sans-serif'],
}

Hero headline must use font-light or font-normal.
Avoid bold-heavy startup styling.

=============================================================
8. SPACING RULE
=============================================================

Use vertical rhythm:

py-24 sections minimum
px-8 layout minimum
gap-16 or gap-20 for major grid separation

Premium design = breathing space.

=============================================================
9. PROPERTY GRID (PREMIUM VERSION)
=============================================================

Remove:
• Rounded images
• Shadow cards

Replace with:

<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-12">

  <div>
    <img class="w-full h-[320px] object-cover" />
    <div class="mt-6">
      <h3 class="text-lg font-medium">Anna Nagar Residence</h3>
      <p class="text-sm text-gray-500 mt-2">₹1.45 Cr</p>
    </div>
  </div>

</div>

Flat.
Clean.
Structured.

=============================================================
10. REVISED MASTER PROMPT (FOR FUTURE UI GENERATION)
=============================================================

Use this instead of generic prompts:

-------------------------------------------------------------
Design a premium, architect-level real estate website.
No rounded corners.
No emojis.
No card-based SaaS layouts.
No startup gradients.
Use sharp edges, structured grids, serif headlines, muted gold accents, and strong whitespace rhythm.
Design should resemble a luxury developer brochure, not a tech landing page.
-------------------------------------------------------------

=============================================================
ANNEXURE-A STATUS
=============================================================

This annexure overrides:
• Rounded UI
• Emoji trust markers
• Template SaaS patterns

This enforces:
• Architectural discipline
• Premium restraint
• High-value brand positioning

UI Layer Only.
No API impact.
No CMS impact.
No mobile impact.

SCCB-4 ANNEXURE-A APPROVED.
=============================================================