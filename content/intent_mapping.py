"""
Intent-based SEO landing page mapping.
Maps URL slugs to filters, intent families, and SEO content.
"""

INTENT_MAP = {
    # --- PRIMARY NRI SERVICE INTENTS (SELL-FIRST) ---
    "nri-sell-property": {
        "filters": {"price_type": "sale"},
        "is_nri": True,
        "category": "service",
        "intent_type": "sell",
        "priority": 100,
        "property_type_label": "NRI Property Sale",
        "title": "Sell Your Property in {city} from Abroad | NRI Property Selling Experts",
        "h1": "Sell Your Property in {city} from Abroad",
        "description": "End-to-end property selling support for NRIs in {city}. We handle pricing, buyer coordination, legal documentation, and closure while you stay abroad.",
        "intro": "Selling your property in {city} while living abroad requires more than a listing. We manage valuation, buyer handling, legal coordination, power of attorney workflows, and closure support so you can exit cleanly without repeated travel.",
        "cta": "Book NRI Selling Consultation",
        "seo_content": "NRI property selling in {city} works best when the process is managed locally with complete transparency. Propertism supports pricing strategy, buyer qualification, legal review, and documentation follow-through, helping overseas owners sell confidently from abroad.",
        "keywords": "nri sell property {city}, sell property in {city} from abroad, sell house in india for nri",
        "related_intent_slugs": [
            "nri-property-management",
            "nri-rental-management",
            "nri-property-maintenance",
            "nri-property-legal-support",
            "nri-power-of-attorney",
            "nri-property-tax",
            "nri-capital-gains",
        ],
    },
    "nri-property-management": {
        "filters": {"price_type": "rent"},
        "is_nri": True,
        "category": "service",
        "intent_type": "management",
        "priority": 95,
        "property_type_label": "Property Management",
        "title": "NRI Property Management in {city} | Trusted Remote Property Care",
        "h1": "NRI Property Management Services in {city}",
        "description": "Complete property management for NRIs in {city}. We handle tenants, rent collection, inspections, compliance, and local coordination while you stay abroad.",
        "intro": "Manage your {city} property remotely with one accountable local partner. We oversee tenants, rentals, maintenance decisions, inspections, and owner reporting so your property remains productive without daily intervention.",
        "cta": "Manage My Property from Abroad",
        "seo_content": "Property management for NRIs in {city} must solve the real problem of distance. We provide on-ground execution, timely updates, tenant coordination, and maintenance oversight so overseas owners can protect asset value and rental continuity.",
        "keywords": "nri property management {city}, property management in india for nris, manage property from abroad india",
        "related_intent_slugs": [
            "nri-sell-property",
            "nri-rental-management",
            "nri-property-maintenance",
        ],
    },
    "nri-rental-management": {
        "filters": {"price_type": "rent"},
        "is_nri": True,
        "category": "service",
        "intent_type": "rental",
        "priority": 90,
        "property_type_label": "Rental Management",
        "title": "NRI Rental Management in {city} | Tenants, Agreements, Rent Collection",
        "h1": "NRI Rental Management Services in {city}",
        "description": "Rent out and manage your property in {city} without travel. We handle tenant sourcing, documentation, rent collection, and move-out coordination for NRIs.",
        "intro": "Renting your property in {city} from abroad should not depend on fragmented local follow-up. We manage tenant sourcing, rental documentation, rent collection, renewals, and move-out coordination with clear reporting.",
        "cta": "Get Rental Management Support",
        "seo_content": "NRI rental management in {city} requires disciplined tenant screening and consistent rent operations. We help owners maintain occupancy, protect rental income, and reduce friction across the full tenant lifecycle.",
        "keywords": "nri rental management {city}, rent property in {city} nri, tenant management services {city}",
        "related_intent_slugs": [
            "nri-sell-property",
            "nri-property-management",
            "nri-property-maintenance",
        ],
    },
    "nri-property-maintenance": {
        "filters": {"price_type": "rent"},
        "is_nri": True,
        "category": "service",
        "intent_type": "maintenance",
        "priority": 85,
        "property_type_label": "Property Maintenance",
        "title": "NRI Property Maintenance in {city} | End-to-End Property Care",
        "h1": "NRI Property Maintenance & Upkeep in {city}",
        "description": "Keep your property in {city} safe and maintained while you live abroad. Regular inspections, repairs, and vendor coordination handled for NRIs.",
        "intro": "Protect your {city} property from neglect with scheduled inspections, repair coordination, preventive upkeep, and trusted local execution. We keep owners informed without burdening them with repeated follow-up.",
        "cta": "Schedule Maintenance Support",
        "seo_content": "Property maintenance for NRIs in {city} is not just about repairs. It is about preserving value, keeping vacancies under control, and ensuring that on-ground work is verified with timely updates and dependable vendor management.",
        "keywords": "nri property maintenance {city}, property upkeep india nri, house maintenance india nri",
        "related_intent_slugs": [
            "nri-sell-property",
            "nri-property-management",
            "nri-rental-management",
        ],
    },
    "manage-property-from-abroad": {
        "filters": {},
        "is_nri": True,
        "category": "informational",
        "intent_type": "informational",
        "priority": 80,
        "property_type_label": "NRI Property Guide",
        "title": "How to Manage Property in {city} While Living Abroad | NRI Guide",
        "h1": "How to Manage Property in {city} While Living Abroad",
        "description": "Practical guidance for NRIs managing property in {city} from abroad. Learn how to handle maintenance, tenants, selling, and local execution without constant travel.",
        "intro": "Managing property in {city} while living abroad becomes difficult when maintenance, tenants, legal paperwork, and local follow-up depend on informal coordination. This guide shows the safest ways to stay in control remotely.",
        "cta": "Talk to NRI Property Expert",
        "seo_content": "For NRIs, property problems usually start with distance and uncertainty. A reliable system for management, rental supervision, maintenance, and sale support reduces delays, protects value, and gives owners a clear operating model from abroad.",
        "keywords": "manage property from abroad india, nri property problems india, remote property management india",
        "related_intent_slugs": [
            "nri-sell-property",
            "nri-property-management",
            "nri-rental-management",
        ],
    },

    # --- SUPPORTING NRI LEGAL / COMPLIANCE INTENTS ---
    "nri-property-legal-support": {
        "filters": {},
        "is_nri": True,
        "category": "informational",
        "intent_type": "informational",
        "priority": 70,
        "property_type_label": "NRI Legal Support",
        "title": "NRI Property Legal Support in {city} | Documentation & Compliance Help",
        "h1": "NRI Property Legal Support in {city}",
        "description": "Legal and documentation guidance for NRIs with property in {city}. Understand ownership, compliance, and safe closure without repeated travel.",
        "intro": "NRI property legal support in {city} must simplify documentation, reduce local dependency, and keep ownership compliance clean. We help owners coordinate legal review and trusted execution.",
        "cta": "Talk to NRI Legal Support",
        "seo_content": "NRIs managing property in {city} often face legal uncertainty. Clear documentation, verified local execution, and structured legal guidance reduce delays and risk for overseas owners.",
        "keywords": "nri property legal support {city}, nri property documentation {city}, nri legal assistance {city}",
        "related_intent_slugs": [
            "nri-sell-property",
            "nri-property-management",
            "nri-power-of-attorney",
        ],
    },
    "nri-power-of-attorney": {
        "filters": {},
        "is_nri": True,
        "category": "informational",
        "intent_type": "informational",
        "priority": 69,
        "property_type_label": "Power of Attorney",
        "title": "NRI Power of Attorney for Property in {city} | POA Guidance",
        "h1": "NRI Power of Attorney for Property in {city}",
        "description": "Understand power of attorney for NRI property in {city}. We guide owners through safe POA setup and document coordination.",
        "intro": "Power of attorney is often the safest way for NRIs to manage or sell property in {city}. We help coordinate POA documentation and ensure the process stays compliant.",
        "cta": "Discuss Power of Attorney",
        "seo_content": "POA for NRI property in {city} reduces travel and keeps ownership decisions legally valid. Structured documentation and verified execution matter for safe transactions.",
        "keywords": "nri power of attorney {city}, poa for nri property {city}, sell property with poa {city}",
        "related_intent_slugs": [
            "nri-sell-property",
            "nri-property-legal-support",
            "nri-property-management",
        ],
    },
    "nri-property-tax": {
        "filters": {},
        "is_nri": True,
        "category": "informational",
        "intent_type": "informational",
        "priority": 68,
        "property_type_label": "NRI Property Tax",
        "title": "NRI Property Tax Guidance in {city} | Compliance Support",
        "h1": "NRI Property Tax Guidance in {city}",
        "description": "Understand tax obligations for NRI property in {city}. We help owners stay compliant while managing, renting, or selling from abroad.",
        "intro": "Property tax compliance in {city} is easier with clear documentation and structured follow-through. We help NRIs stay updated while reducing local dependency.",
        "cta": "Get Tax Compliance Help",
        "seo_content": "Tax compliance for NRI property in {city} should be clear, documented, and consistent. We help owners reduce risk and stay compliant through trusted execution.",
        "keywords": "nri property tax {city}, nri tax compliance {city}, property tax for nri {city}",
        "related_intent_slugs": [
            "nri-sell-property",
            "nri-property-legal-support",
            "nri-capital-gains",
        ],
    },
    "nri-capital-gains": {
        "filters": {},
        "is_nri": True,
        "category": "informational",
        "intent_type": "informational",
        "priority": 67,
        "property_type_label": "NRI Capital Gains",
        "title": "NRI Capital Gains on Property in {city} | Sell-Side Guidance",
        "h1": "NRI Capital Gains on Property in {city}",
        "description": "Know how capital gains apply when NRIs sell property in {city}. Practical guidance before pricing or closing decisions.",
        "intro": "Capital gains planning for NRI property sales in {city} is critical before pricing and closure. We help owners understand the basics and coordinate the right next steps.",
        "cta": "Discuss Capital Gains Planning",
        "seo_content": "Capital gains considerations shape NRI property sale outcomes in {city}. Planning early helps avoid last-minute complications and unclear obligations.",
        "keywords": "nri capital gains {city}, capital gains tax on property {city}, nri property sale tax {city}",
        "related_intent_slugs": [
            "nri-sell-property",
            "nri-property-tax",
            "nri-property-legal-support",
        ],
    },

    # --- LOWER-PRIORITY NRI DISCOVERY INTENTS ---
    "nri-buy-villas": {
        "filters": {"property_type__slug": "villa", "price_type": "sale"},
        "is_nri": True,
        "category": "buy",
        "intent_type": "buy",
        "priority": 30,
        "property_type_label": "NRI Villa Investment",
        "title": "Villas in {city} for NRIs | Secure Investment Options",
        "h1": "Premium Villas in {city} for NRIs",
        "description": "Verified villa investment opportunities in {city} for NRIs. Remote legal handling, trusted documentation, and complete property management.",
        "intro": "Investing in an independent villa in {city} from abroad requires local hands you can trust. We specialize in assisting NRIs with verified villa discovery, seamless legal documentation, and end-to-end property maintenance once the keys are handed over.",
        "cta": "Talk to NRI Property Expert",
        "seo_content": "NRI property investment in {city} villas focuses on long-term capital appreciation and lifestyle security. We handle the remote management complexities including legal vetting, periodic site visits, and tenant coordination. Our portfolio includes curated villas in high-growth corridors of {city} with clear documentation.",
        "keywords": "buy villa {city} from usa, nri villa investment {city}, villas for sale in {city} for nri",
        "related_intent_slugs": [
            "nri-buy-flats",
            "nri-property-management",
            "nri-sell-property",
        ],
    },
    "nri-buy-flats": {
        "filters": {"property_type__slug": "apartment", "price_type": "sale"},
        "is_nri": True,
        "category": "buy",
        "intent_type": "buy",
        "priority": 29,
        "property_type_label": "NRI Flat Investment",
        "title": "Flats in {city} for NRIs | High-Yield Apartments",
        "h1": "Apartments & Flats in {city} for NRIs",
        "description": "Buy verified flats in {city} while living abroad. Full NRI support for property search, legal handling, and tenant management.",
        "intro": "Secure your dream apartment in {city} without needing to travel. We provide NRIs with a comprehensive remote-first buying experience, from verified listing selection to registration and tenant sourcing.",
        "cta": "Get Investment Options",
        "seo_content": "Buying flats in {city} as an NRI involves navigating regulatory paths and practical local coordination. Propertism simplifies the process with verified options, documentation support, and post-purchase operating continuity.",
        "keywords": "buy property in {city} from dubai, nri flats {city}, apartments for nris in {city}",
        "related_intent_slugs": [
            "nri-buy-villas",
            "nri-property-management",
            "nri-sell-property",
        ],
    },
    "nri-investment-properties": {
        "filters": {"price_type": "sale"},
        "is_nri": True,
        "category": "invest",
        "intent_type": "buy",
        "priority": 28,
        "property_type_label": "NRI Investment",
        "title": "High-Yield Property Investment in {city} for NRIs",
        "h1": "NRI Property Investment Advisory in {city}",
        "description": "Build a high-yield real estate portfolio in {city} from overseas. Data-driven investment advisory and verified high-growth property listings.",
        "intro": "Maximize your ROI in the {city} real estate market. We identify high-growth zones and under-valued assets for NRI investors seeking long-term appreciation and stable rental income.",
        "cta": "Get Investment Advisory",
        "seo_content": "Real estate investment for NRIs in {city} is strongest when acquisition decisions are paired with a realistic operating plan. We help investors evaluate growth, rental potential, and management feasibility before they commit capital.",
        "keywords": "property investment in india for nris, villa investment {city} nri, best property to buy in {city}",
        "related_intent_slugs": [
            "nri-buy-villas",
            "nri-buy-flats",
            "nri-property-management",
        ],
    },
    "nri-luxury-properties": {
        "filters": {"price__gte": 15000000, "price_type": "sale"},
        "is_nri": True,
        "category": "buy",
        "intent_type": "buy",
        "priority": 27,
        "property_type_label": "NRI Luxury Real Estate",
        "title": "Luxury Real Estate in {city} for NRIs | Premium Portfolio",
        "h1": "Premium Luxury Properties in {city} for NRIs",
        "description": "Exclusive collection of luxury villas and apartments in {city} for HNI and NRI investors. World-class amenities and prime location focus.",
        "intro": "Curated luxury real estate in {city} that meets international standards. From sky villas to gated mansions, we provide NRIs with access to top-tier addresses in the city.",
        "cta": "View Luxury Portfolio",
        "seo_content": "Luxury properties in {city} offer prestige, lifestyle, and long-term asset visibility. We support NRIs seeking high-specification homes with a stronger operational lens around ownership, documentation, and upkeep.",
        "keywords": "luxury real estate india nri, premium villas {city}, high-end flats {city}",
        "related_intent_slugs": [
            "nri-buy-villas",
            "nri-buy-flats",
            "nri-property-management",
        ],
    },

    # --- SECONDARY DOMESTIC INTENTS (SUPPORTING) ---
    "flats-for-sale": {
        "filters": {"property_type__slug": "apartment", "price_type": "sale"},
        "is_nri": False,
        "category": "buy",
        "intent_type": "buy",
        "priority": 20,
        "property_type_label": "Flat",
        "title": "Flats for Sale in {city} | Verified Apartments",
        "h1": "Apartments & Flats for Sale in {city}",
        "description": "Browse verified flats for sale in {city}. Direct builder listings with transparent pricing and complete documentation.",
        "intro": "Explore a curated selection of verified flats for sale in {city}. All properties include detailed photos, transparent pricing, and thorough legal vetting to ensure a safe home-buying experience.",
        "cta": "View Details",
        "seo_content": "{city} offers a diverse range of residential flats, from budget-friendly options to premium apartments. Our listings focus on high-demand residential zones with excellent connectivity and social infrastructure.",
        "keywords": "flats for sale {city}, buy flat {city}, apartments in {city}",
        "related_intent_slugs": [
            "budget-properties",
            "villas-for-sale",
            "flats-for-rent",
        ],
    },
    "villas-for-sale": {
        "filters": {"property_type__slug": "villa", "price_type": "sale"},
        "is_nri": False,
        "category": "buy",
        "intent_type": "buy",
        "priority": 19,
        "property_type_label": "Villa",
        "title": "Villas for Sale in {city} | Independent Houses",
        "h1": "Independent Houses & Villas for Sale in {city}",
        "description": "Latest villas and independent houses for sale in {city}. Premium gated communities and luxury individual homes.",
        "intro": "Find your dream independent house in {city}. Browse our verified villa listings in the city's most prestigious neighborhoods and high-growth residential corridors.",
        "cta": "Get Best Deals",
        "seo_content": "Independent villas in {city} provide the ultimate privacy and land ownership. Most new projects are situated in curated gated communities with clubhouses, parks, and 24/7 security services.",
        "keywords": "villas for sale {city}, independent houses {city}, luxury villas {city}",
        "related_intent_slugs": [
            "flats-for-sale",
            "flats-for-rent",
            "budget-properties",
        ],
    },
    "flats-for-rent": {
        "filters": {"property_type__slug": "apartment", "price_type": "rent"},
        "is_nri": False,
        "category": "buy",
        "intent_type": "buy",
        "priority": 18,
        "property_type_label": "Rental Flat",
        "title": "Flats for Rent in {city} | Verified Rentals",
        "h1": "Apartments & Flats for Rent in {city}",
        "description": "Find verified flats for rent in {city}. Top residential locations with professional tenant services.",
        "intro": "Looking for a flat for rent? Browse our hand-picked rental listings in {city}. We ensure that every rental property is verified and the documentation process is seamless for both owners and tenants.",
        "cta": "View Details",
        "seo_content": "The rental market in {city} is highly dynamic. Our listings categorize apartments by area, budget, and proximity to major employment hubs to help you find the perfect rental home quickly.",
        "keywords": "flats for rent {city}, rental apartments {city}, rent house {city}",
        "related_intent_slugs": [
            "flats-for-sale",
            "villas-for-sale",
            "budget-properties",
        ],
    },
    "budget-properties": {
        "filters": {
            "property_type__slug": "apartment",
            "price_type": "sale",
            "price__lte": 6000000,
        },
        "is_nri": False,
        "category": "buy",
        "intent_type": "buy",
        "priority": 17,
        "property_type_label": "Budget Property",
        "title": "Budget Properties in {city} | Affordable Housing",
        "h1": "Affordable Homes & Budget Properties in {city}",
        "description": "Latest pocket-friendly apartments and homes for sale in {city}. Real estate options for first-time buyers and budget-conscious investors.",
        "intro": "Buying your first home should be stress-free. We have identified the best budget-friendly apartments in {city} that offer quality construction without compromising on modern essentials.",
        "cta": "View Details",
        "seo_content": "Affordable housing in {city} is seeing massive demand. These budget developments are usually found in expanding residential hubs with good future appreciation potential and improving civic infrastructure.",
        "keywords": "budget flats {city}, affordable housing {city}, flats under 50 lakhs {city}",
        "related_intent_slugs": [
            "flats-for-sale",
            "flats-for-rent",
            "villas-for-sale",
        ],
    },
}

ALIASES = {
    "nri-resale-assistance": "nri-sell-property",
    "nri-tenant-management": "nri-rental-management",
    "property-maintenance-for-nri": "nri-property-maintenance",
    "property-management-services": "nri-property-management",
    "property-management": "nri-property-management",
}

ALIAS_SLUGS = set(ALIASES.keys())

for alias_slug, target_slug in ALIASES.items():
    INTENT_MAP[alias_slug] = INTENT_MAP[target_slug]

CITIES = {
    "chennai": {
        "name": "Chennai",
        "state": "Tamil Nadu",
        "description": "Chennai, the capital of Tamil Nadu, is a major real estate hub in South India.",
    },
    "bangalore": {
        "name": "Bangalore",
        "state": "Karnataka",
        "description": "Bangalore (Bengaluru) is India's Silicon Valley and a premier investment destination.",
    },
    "hyderabad": {
        "name": "Hyderabad",
        "state": "Telangana",
        "description": "Hyderabad is one of India's fastest-growing real estate markets with massive infrastructure growth.",
    },
}


NRI_LOCATIONS = {
    "hackensack-nj": {"name": "Hackensack, NJ", "label": "Hackensack, NJ", "region": "USA"},
    "new-york-usa": {"name": "New York", "label": "New York, USA", "region": "USA"},
    "san-jose-ca": {"name": "San Jose, CA", "label": "San Jose, CA", "region": "USA"},
    "dallas-tx": {"name": "Dallas, TX", "label": "Dallas, TX", "region": "USA"},
    "london-uk": {"name": "London", "label": "London, UK", "region": "UK"},
    "toronto-canada": {"name": "Toronto", "label": "Toronto, Canada", "region": "Canada"},
    "dubai-uae": {"name": "Dubai", "label": "Dubai, UAE", "region": "UAE"},
    "singapore": {"name": "Singapore", "label": "Singapore", "region": "Singapore"},
    "sydney-australia": {"name": "Sydney", "label": "Sydney, Australia", "region": "Australia"},
    "doha-qatar": {"name": "Doha", "label": "Doha, Qatar", "region": "Qatar"},
    "abu-dhabi": {"name": "Abu Dhabi", "label": "Abu Dhabi, UAE", "region": "UAE"},
    "kuwait": {"name": "Kuwait City", "label": "Kuwait City, Kuwait", "region": "Kuwait"},
    "saudi": {"name": "Riyadh", "label": "Riyadh, Saudi Arabia", "region": "Saudi Arabia"},
    "malaysia": {"name": "Kuala Lumpur", "label": "Kuala Lumpur, Malaysia", "region": "Malaysia"},
}


def get_intent_config(intent_slug, city_slug="chennai"):
    """Get configuration for an intent-based landing page."""
    if intent_slug not in INTENT_MAP:
        return None

    city = CITIES.get(city_slug, {"name": city_slug.title()})
    config = INTENT_MAP[intent_slug].copy()

    for key in ["title", "h1", "description", "intro", "keywords", "seo_content"]:
        if key in config:
            config[key] = config[key].format(city=city["name"])

    config["city"] = city
    config["intent_slug"] = intent_slug
    config["city_slug"] = city_slug
    config["canonical_intent_slug"] = ALIASES.get(intent_slug, intent_slug)
    config.setdefault("intent_type", "buy")
    config.setdefault("priority", 0)
    return config


def get_all_intents():
    """Get all public intent slugs without aliases."""
    return [slug for slug in INTENT_MAP.keys() if slug not in ALIAS_SLUGS]


def resolve_geo_slug(geo_slug):
    """
    Resolve a combined geo slug like "chennai-villas-for-sale"
    into (city_slug, intent_slug).
    """
    for city_slug in CITIES.keys():
        if geo_slug.startswith(f"{city_slug}-"):
            intent_slug = geo_slug[len(city_slug) + 1 :]
            if intent_slug in INTENT_MAP:
                return city_slug, intent_slug
    return None, None
