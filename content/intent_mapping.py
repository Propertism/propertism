"""
Intent-based SEO landing page mapping
Maps URL slugs to filters and SEO content
"""

INTENT_MAP = {
    # --- PRIMARY NRI INTENTS (80%) ---
    'nri-buy-villas': {
        'filters': {'property_type__slug': 'villa', 'price_type': 'sale'},
        'is_nri': True,
        'category': 'buy',
        'property_type_label': 'NRI Villa Investment',
        'title': 'Villas in {city} for NRIs | Secure Investment Options',
        'h1': 'Premium Villas in {city} for NRIs',
        'description': 'Verified villa investment opportunities in {city} for NRIs. Remote legal handling, trusted documentation, and complete property management.',
        'intro': 'Investing in an independent villa in {city} from abroad requires local hands you can trust. We specialize in assisting NRIs with verified villa discovery, seamless legal documentation, and end-to-end property maintenance once the keys are handed over.',
        'cta': 'Talk to NRI Property Expert',
        'seo_content': 'NRI property investment in {city} villas focuses on long-term capital appreciation and lifestyle security. We handle the remote management complexities including legal vetting, periodic site visits, and tenant coordination. Our portfolio includes curated villas in high-growth corridors of {city} with clear documentation.',
        'keywords': 'buy villa {city} from usa, nri villa investment {city}, villas for sale in {city} for nri',
        'related_intent_slugs': ['nri-buy-flats', 'nri-investment-properties', 'nri-property-management'],
    },
    'nri-buy-flats': {
        'filters': {'property_type__slug': 'apartment', 'price_type': 'sale'},
        'is_nri': True,
        'category': 'buy',
        'property_type_label': 'NRI Flat Investment',
        'title': 'Flats in {city} for NRIs | High-Yield Apartments',
        'h1': 'Apartments & Flats in {city} for NRIs',
        'description': 'Buy verified flats in {city} while living abroad. Full NRI support for property search, legal handling, and tenant management.',
        'intro': 'Secure your dream apartment in {city} without needing to travel. We provide NRIs with a comprehensive "remote-first" buying experience, from verified listing selection to seamless registration and tenant sourcing.',
        'cta': 'Get Investment Options',
        'seo_content': 'Buying flats in {city} as an NRI involves navigating complex regulatory paths. Propertism simplifies this with a focus on remote trust. We handle everything from document pickups to builder coordination, ensuring your investment in {city} real estate remains a passive, stress-free asset.',
        'keywords': 'buy property in {city} from dubai, nri flats {city}, apartments for nris in {city}',
        'related_intent_slugs': ['nri-buy-villas', 'nri-luxury-properties', 'nri-property-management'],
    },
    'nri-investment-properties': {
        'filters': {'price_type': 'sale'},
        'is_nri': True,
        'category': 'invest',
        'property_type_label': 'NRI Investment',
        'title': 'High-Yield Property Investment in {city} for NRIs',
        'h1': 'NRI Property Investment Advisory in {city}',
        'description': 'Build a high-yield real estate portfolio in {city} from overseas. Data-driven investment advisory and verified high-growth property listings.',
        'intro': 'Maximize your ROI in the {city} real estate market. We identify high-growth zones and under-valued assets specifically for NRI investors seeking long-term appreciation and stable rental income.',
        'cta': 'Get Investment Advisory',
        'seo_content': 'Real estate investment for NRIs in {city} is optimized through our "market-first" approach. We analyze infrastructure pipelines and rental velocity to recommend properties that generate superior returns. Our remote management service ensures your capital stays productive without manual overhead.',
        'keywords': 'property investment in india for nris, villa investment {city} nri, best property to buy in {city}',
        'related_intent_slugs': ['nri-buy-villas', 'nri-buy-flats', 'nri-property-management'],
    },
    'nri-luxury-properties': {
        'filters': {'price__gte': 15000000, 'price_type': 'sale'},
        'is_nri': True,
        'category': 'buy',
        'property_type_label': 'NRI Luxury Real Estate',
        'title': 'Luxury Real Estate in {city} for NRIs | Premium Portfolio',
        'h1': 'Premium Luxury Properties in {city} for NRIs',
        'description': 'Exclusive collection of luxury villas and apartments in {city} for HNI and NRI investors. World-class amenities and prime location focus.',
        'intro': 'Curated luxury real estate in {city} that meets international standards. From sky-villas to expansive gated mansions, we provide NRIs with exclusive access to the most coveted addresses in the city.',
        'cta': 'View Luxury Portfolio',
        'seo_content': 'Luxury properties in {city} offer the perfect combination of prestige and investment security. We cater specifically to NRIs seeking high-specification residences with global standards of architecture and community management. Each signature property is personally vetted by our senior specialists.',
        'keywords': 'luxury real estate india nri, premium villas {city}, high-end flats {city}',
        'related_intent_slugs': ['nri-buy-villas', 'nri-buy-flats', 'nri-investment-properties'],
    },
    'nri-property-management': {
        'filters': {'price_type': 'rent'},
        'is_nri': True,
        'category': 'service',
        'property_type_label': 'Property Management',
        'title': 'NRI Property Management in {city} | End-to-End Hosting',
        'h1': 'NRI Property Management Services in {city}',
        'description': 'Remote property management for NRIs in {city}. We handle tenants, rent collection, maintenance, and legal compliance.',
        'intro': 'Manage your {city} property from anywhere in the world. We act as your trusted local representatives, ensuring your asset is maintained, your rent is collected, and your tenants are properly vetted — all with total transparency.',
        'cta': 'Manage My Property from Abroad',
        'seo_content': 'Effective property management for NRIs in {city} solves the pain point of distance. We coordinate remote legal handling, periodic site visits, and seamless tenant transitions. Our dashboard keeps you updated on maintenance status and financial reporting in real-time.',
        'keywords': 'property management in india for nris, nri property services {city}, remote rental management',
        'related_intent_slugs': ['nri-tenant-management', 'nri-property-maintenance', 'nri-resale-assistance'],
    },
    'nri-property-maintenance': {
        'filters': {'price_type': 'rent'},
        'is_nri': True,
        'category': 'service',
        'property_type_label': 'Property Maintenance',
        'title': 'Property Maintenance for NRIs in {city} | Verified Care',
        'h1': 'NRI Property Maintenance & Upkeep in {city}',
        'description': 'On-ground maintenance and property care for NRI owners in {city}. Routine inspections, repairs, and vendor management.',
        'intro': 'Never worry about the physical state of your {city} home again. From routine plumbing and electrical checks to major renovations, we manage all on-ground maintenance so your property never falls into disrepair.',
        'cta': 'Schedule Maintenance Check',
        'seo_content': 'Remote property maintenance requires local execution that you can trust. We provide NRIs with verified reports and photograps of every maintenance task in {city}. Our network of trusted vendors ensures quality work at fair, transparent pricing.',
        'keywords': 'nri property maintenance {city}, property care for nris, house upkeep india',
        'related_intent_slugs': ['nri-property-management', 'nri-tenant-management', 'nri-resale-assistance'],
    },
    'nri-tenant-management': {
        'filters': {'price_type': 'rent'},
        'is_nri': True,
        'category': 'service',
        'property_type_label': 'Tenant Management',
        'title': 'NRI Tenant Management in {city} | Tenant Sourcing & Care',
        'h1': 'NRI Tenant Sourcing & Management in {city}',
        'description': 'Expert tenant management for NRIs in {city}. Background checks, documentation, rent collection, and smooth move-out coordination.',
        'intro': 'Find and manage reliable tenants in {city} without traveling to India. We handle the entire tenant lifecycle: from high-quality sourcing and vetting to professional documentation and monthly rent collection.',
        'cta': 'Find Reliable Tenants',
        'seo_content': 'Tenant coordination is the most time-consuming task for NRI landlords in {city}. We solve this by implementing professional screening standards and clear reporting. We manage all tenant communications, ensuring your rental income is consistent and your property is respected.',
        'keywords': 'tenant management for nris, rent collection india nri, find tenants in {city}',
        'related_intent_slugs': ['nri-property-management', 'nri-property-maintenance', 'nri-resale-assistance'],
    },
    'nri-resale-assistance': {
        'filters': {'price_type': 'sale'},
        'is_nri': True,
        'category': 'service',
        'property_type_label': 'Resale Assistance',
        'title': 'NRI Property Resale Assistance in {city} | Expert Exit Strategy',
        'h1': 'NRI Property Resale & Exit Support in {city}',
        'description': 'Sell your property in {city} while staying abroad. Full resale support including valuation, buyer sourcing, and legal documentation.',
        'intro': 'Liquidate your {city} assets with expert local support. We handle the entire resale process for NRIs: from professional valuation and marketing to final legal documentation and secure fund repatriation support.',
        'cta': 'Request Valuation Report',
        'seo_content': 'Selling property from abroad requires an exit strategy focused on trust and legal accuracy. We represent NRI sellers in {city}, ensuring that buyer vetting is rigorous and the transaction follows all Indian regulatory requirements for NRI repatriations.',
        'keywords': 'sell nri property in india, resale assistance {city}, nri property exit support',
        'related_intent_slugs': ['nri-property-management', 'nri-investment-properties', 'nri-buy-villas'],
    },

    # --- SECONDARY DOMESTIC INTENTS (20%) ---
    'flats-for-sale': {
        'filters': {'property_type__slug': 'apartment', 'price_type': 'sale'},
        'is_nri': False,
        'property_type_label': 'Flat',
        'title': 'Flats for Sale in {city} | Verified Apartments',
        'h1': 'Apartments & Flats for Sale in {city}',
        'description': 'Browse verified flats for sale in {city}. Direct builder listings with transparent pricing and complete documentation.',
        'intro': 'Explore a curated selection of verified flats for sale in {city}. All properties include detailed photos, transparent pricing, and thorough legal vetting to ensure a safe home-buying experience.',
        'cta': 'View Details',
        'seo_content': '{city} offers a diverse range of residential flats, from budget-friendly options to premium apartments. Our listings focus on high-demand residential zones with excellent connectivity and social infrastructure.',
        'keywords': 'flats for sale {city}, buy flat {city}, apartments in {city}',
        'related_intent_slugs': ['budget-properties', 'villas-for-sale', 'flats-for-rent'],
    },
    'villas-for-sale': {
        'filters': {'property_type__slug': 'villa', 'price_type': 'sale'},
        'is_nri': False,
        'property_type_label': 'Villa',
        'title': 'Villas for Sale in {city} | Independent Houses',
        'h1': 'Independent Houses & Villas for Sale in {city}',
        'description': 'Latest villas and independent houses for sale in {city}. Premium gated communities and luxury individual homes.',
        'intro': 'Find your dream independent house in {city}. Browse our verified villa listings in the city\'s most prestigious neighborhoods and high-growth residential corridors.',
        'cta': 'Get Best Deals',
        'seo_content': 'Independent villas in {city} provide the ultimate privacy and land ownership. Most new projects are situated in curated gated communities with clubhouses, parks, and 24/7 security services.',
        'keywords': 'villas for sale {city}, independent houses {city}, luxury villas {city}',
        'related_intent_slugs': ['flats-for-sale', 'flats-for-rent', 'villas-for-rent'],
    },
    'flats-for-rent': {
        'filters': {'property_type__slug': 'apartment', 'price_type': 'rent'},
        'is_nri': False,
        'property_type_label': 'Rental Flat',
        'title': 'Flats for Rent in {city} | Verified Rentals',
        'h1': 'Apartments & Flats for Rent in {city}',
        'description': 'Find verified flats for rent in {city}. Top residential locations with professional tenant services.',
        'intro': 'Looking for a flat for rent? Browse our hand-picked rental listings in {city}. We ensure that every rental property is verified and the documentation process is seamless for both owners and tenants.',
        'cta': 'View Details',
        'seo_content': 'The rental market in {city} is highly dynamic. Our listings categorize apartments by area, budget, and proximity to major employment hubs to help you find the perfect rental home quickly.',
        'keywords': 'flats for rent {city}, rental apartments {city}, rent house {city}',
        'related_intent_slugs': ['flats-for-sale', 'villas-for-rent', 'budget-properties'],
    },
    'budget-properties': {
        'filters': {'property_type__slug': 'apartment', 'price_type': 'sale', 'price__lte': 6000000},
        'is_nri': False,
        'property_type_label': 'Budget Property',
        'title': 'Budget Properties in {city} | Affordable Housing',
        'h1': 'Affordable Homes & Budget Properties in {city}',
        'description': 'Latest pocket-friendly apartments and homes for sale in {city}. Real estate options for first-time buyers and budget-conscious investors.',
        'intro': 'Buying your first home should be stress-free. We have identified the best budget-friendly apartments in {city} that offer quality construction without compromising on modern essentials.',
        'cta': 'View Details',
        'seo_content': 'Affordable housing in {city} is seeing massive demand. These budget developments are usually found in expanding residential hubs with good future appreciation potential and improving civic infrastructure.',
        'keywords': 'budget flats {city}, affordable housing {city}, flats under 50 lakhs {city}',
        'related_intent_slugs': ['flats-for-sale', 'flats-for-rent', 'villas-for-sale'],
    },
}

# Aliases for consistent routing
INTENT_MAP['property-maintenance-for-nri'] = INTENT_MAP['nri-property-maintenance']
INTENT_MAP['property-management-services'] = INTENT_MAP['nri-property-management']
INTENT_MAP['property-management'] = INTENT_MAP['nri-property-management']

# City-specific data
CITIES = {
    'chennai': {
        'name': 'Chennai',
        'state': 'Tamil Nadu',
        'description': 'Chennai, the capital of Tamil Nadu, is a major real estate hub in South India.',
    },
    'bangalore': {
        'name': 'Bangalore',
        'state': 'Karnataka',
        'description': 'Bangalore (Bengaluru) is India\'s Silicon Valley and a premier investment destination.',
    },
    'hyderabad': {
        'name': 'Hyderabad',
        'state': 'Telangana',
        'description': 'Hyderabad is one of India\'s fastest-growing real estate markets with massive infrastrucure growth.',
    },
}


# NRI Global Hubs
NRI_LOCATIONS = {
    'hackensack-nj': {'name': 'Hackensack, NJ', 'label': 'Hackensack, NJ', 'region': 'USA'},
    'new-york-usa': {'name': 'New York', 'label': 'New York, USA', 'region': 'USA'},
    'san-jose-ca': {'name': 'San Jose, CA', 'label': 'San Jose, CA', 'region': 'USA'},
    'dallas-tx': {'name': 'Dallas, TX', 'label': 'Dallas, TX', 'region': 'USA'},
    'london-uk': {'name': 'London', 'label': 'London, UK', 'region': 'UK'},
    'toronto-canada': {'name': 'Toronto', 'label': 'Toronto, Canada', 'region': 'Canada'},
    'dubai-uae': {'name': 'Dubai', 'label': 'Dubai, UAE', 'region': 'UAE'},
    'singapore': {'name': 'Singapore', 'label': 'Singapore', 'region': 'Singapore'},
    'sydney-australia': {'name': 'Sydney', 'label': 'Sydney, Australia', 'region': 'Australia'},
    'doha-qatar': {'name': 'Doha', 'label': 'Doha, Qatar', 'region': 'Qatar'},
}


def get_intent_config(intent_slug, city_slug='chennai'):
    """Get configuration for an intent-based landing page"""
    if intent_slug not in INTENT_MAP:
        return None
    
    city = CITIES.get(city_slug, {'name': city_slug.title()})
    config = INTENT_MAP[intent_slug].copy()
    
    # Replace {city} placeholder in all text fields
    for key in ['title', 'h1', 'description', 'intro', 'keywords', 'seo_content']:
        if key in config:
            config[key] = config[key].format(city=city['name'])
    
    config['city'] = city
    config['intent_slug'] = intent_slug
    config['city_slug'] = city_slug
    
    return config


def get_all_intents():
    """Get all available intent slugs"""
    return list(INTENT_MAP.keys())


def resolve_geo_slug(geo_slug):
    """
    Resolves a combined geo_slug like 'chennai-villas-for-sale'
    into (city_slug, intent_slug)
    """
    for city_slug in CITIES.keys():
        if geo_slug.startswith(f"{city_slug}-"):
            intent_slug = geo_slug[len(city_slug)+1:]
            if intent_slug in INTENT_MAP:
                return city_slug, intent_slug
    return None, None
