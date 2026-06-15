"""
pSEO Enrichment Engine — content/pseo_enrichment.py

Provides:
  - build_differentiated_h1()   : unique H1 per intent × city × nri_region
  - build_faq_items()           : intent + city + geo-specific FAQ blocks
  - build_trust_block()         : "Why Propertism" E-E-A-T section
  - build_knowledge_hub_links() : contextual internal links to blog articles
  - build_enrichment_context()  : single entry point for views_landing.py
"""

# ---------------------------------------------------------------------------
# H1 DIFFERENTIATION
# H1 templates are keyed by intent_slug.
# Each combination produces a unique headline using the specific NRI location.
# ---------------------------------------------------------------------------

_H1_TEMPLATES = {
    "nri-sell-property": [
        "Professional NRI Property Sale Services in {city} for Clients in {nri}",
        "Sell Your {city} Property Seamlessly from {nri}",
        "Trusted {city} Property Selling for Overseas Owners in {nri}",
        "End-to-End NRI Property Sale & Exit in {city} from {nri}",
        "Protect and Sell Your {city} Assets from {nri} Cleanly",
    ],
    "nri-property-management": [
        "Professional NRI Property Management Services in {city} for Owners in {nri}",
        "Manage Your {city} Property Seamlessly from {nri}",
        "Trusted {city} Property Care for Overseas Owners in {nri}",
        "End-to-End NRI Property Care Services in {city} from {nri}",
        "Protect and Manage Your {city} Assets from {nri}",
    ],
    "nri-rental-management": [
        "Professional NRI Rental Management Services in {city} for Landlords in {nri}",
        "Rent Out Your {city} Property Seamlessly from {nri}",
        "Trusted {city} Tenant Placement for Overseas Landlords in {nri}",
        "End-to-End NRI Rental Oversight in {city} from {nri}",
        "Maximize and Manage Your {city} Rental Income from {nri}",
    ],
    "nri-property-maintenance": [
        "Professional NRI Property Maintenance & Upkeep in {city} for Owners in {nri}",
        "Maintain Your {city} Property Seamlessly from {nri}",
        "Trusted {city} Property Inspections & Upkeep for NRIs in {nri}",
        "End-to-End NRI Property Maintenance in {city} from {nri}",
        "Protect and Secure Your {city} Property from {nri}",
    ],
    "manage-property-from-abroad": [
        "Practical Guide: How to Manage Property in {city} from {nri}",
        "Manage Your {city} Property Remotely from {nri}",
        "Expert NRI Property Guidance for Residents in {nri} | {city}",
        "Remote Property Control and Management in {city} for NRIs in {nri}",
        "Solve Your {city} Property Challenges from {nri}",
    ],
    "nri-property-legal-support": [
        "Professional NRI Property Legal Support in {city} for Clients in {nri}",
        "Handle Your {city} Property Legal Vetting from {nri}",
        "Trusted {city} Legal Documentation Support for NRIs in {nri}",
        "End-to-End NRI Property Legal Verification in {city} from {nri}",
        "Secure and Verify Your {city} Property Documents from {nri}",
    ],
    "nri-power-of-attorney": [
        "Professional Power of Attorney Support in {city} for NRIs in {nri}",
        "Execute Your {city} Power of Attorney from {nri} Safely",
        "Trusted {city} POA Documentation & Registration for NRIs in {nri}",
        "End-to-End NRI Power of Attorney Coordination in {city} from {nri}",
        "Secure Your {city} Assets via Power of Attorney from {nri}",
    ],
    "nri-property-tax": [
        "Professional NRI Property Tax Compliance & Filing in {city} from {nri}",
        "Manage Your {city} Property Tax Obligations from {nri}",
        "Trusted {city} Property Tax Guidance for NRIs in {nri}",
        "End-to-End NRI Property Tax Support in {city} from {nri}",
        "Pay and Manage Your {city} Property Taxes from {nri} Safely",
    ],
    "nri-capital-gains": [
        "Professional NRI Capital Gains Tax Planning for {city} Property from {nri}",
        "Calculate and Optimize Your {city} Property Capital Gains Tax from {nri}",
        "Trusted {city} Capital Gains Advisory for NRI Sellers in {nri}",
        "End-to-End NRI Capital Gains Tax Coordination in {city} from {nri}",
        "Minimize Your {city} Property Sale Tax Liability from {nri}",
    ],
    "nri-buy-villas": [
        "Premium Villas in {city} for NRI Investors in {nri}",
        "Invest in a Premium {city} Villa from {nri} Safely",
        "Trusted {city} Villa Purchase & Management for Buyers in {nri}",
        "End-to-End Villa Acquisition Services in {city} from {nri}",
        "Find Your Dream Villa in {city} from {nri} with Propertism",
    ],
    "nri-buy-flats": [
        "Apartments & Flats in {city} for NRI Buyers in {nri}",
        "Invest in a High-Yield {city} Flat from {nri} Safely",
        "Trusted {city} Apartment Purchase & Tenant Placement for NRIs in {nri}",
        "End-to-End Flat Acquisition & Management in {city} from {nri}",
        "Find Verified Apartments & Flats in {city} from {nri}",
    ],
    "nri-investment-properties": [
        "Verified Investment Properties in {city} for NRI Investors in {nri}",
        "Build Your {city} Real Estate Portfolio from {nri}",
        "Trusted {city} Real Estate Investment Advisory for Buyers in {nri}",
        "End-to-End Property Investment Services in {city} from {nri}",
        "Maximize Your {city} Property Investment ROI from {nri}",
    ],
    "nri-luxury-properties": [
        "Premium Luxury Properties in {city} for HNI and NRI Buyers in {nri}",
        "Invest in Luxury Real Estate in {city} from {nri} Safely",
        "Trusted {city} Luxury Villa & Flat Search for Buyers in {nri}",
        "End-to-End Luxury Property Purchase & Management in {city} from {nri}",
        "Find Exclusive Luxury Homes in {city} from {nri}",
    ],
    "flats-for-sale": [
        "Verified Apartments & Flats for Sale in {city} for NRIs in {nri}",
        "Buy a Flat in {city} from {nri} with Complete Verification",
        "Trusted {city} Flats for Sale — NRI Buying Support in {nri}",
        "End-to-End Flat Purchase Services in {city} from {nri}",
        "Browse Verified Flats for Sale in {city} from {nri}",
    ],
    "villas-for-sale": [
        "Premium Independent Houses & Villas for Sale in {city} for NRIs in {nri}",
        "Buy a Villa in {city} from {nri} with Complete Legal Vetting",
        "Trusted {city} Villas for Sale — NRI Purchase Support in {nri}",
        "End-to-End Villa Purchase Coordination in {city} from {nri}",
        "Browse Verified Villas & Houses for Sale in {city} from {nri}",
    ],
    "flats-for-rent": [
        "Verified Apartments & Flats for Rent in {city} for Tenants from {nri}",
        "Rent a Flat in {city} from {nri} with Managed Tenancy Support",
        "Trusted {city} Rental Listings & Agreement Assistance in {nri}",
        "End-to-End Tenant Placement & Rental Services in {city} from {nri}",
        "Browse Verified Flats & Apartments for Rent in {city} from {nri}",
    ],
    "budget-properties": [
        "Affordable Homes & Budget Properties in {city} for NRIs in {nri}",
        "Invest in Budget-Friendly Real Estate in {city} from {nri}",
        "Trusted {city} Budget Apartments for Sale for Buyers in {nri}",
        "End-to-End Affordable Housing Services in {city} from {nri}",
        "Browse Budget-Friendly Properties in {city} from {nri}",
    ],
}

# intent_type → list of H1 templates (no NRI geo context fallback)
_H1_CITY_VARIANTS = {
    "sell": [
        "Sell Your Property in {city} from Abroad",
        "NRI Property Sale Services in {city}",
        "Exit Your {city} Property Cleanly from Overseas",
        "Managed Property Sale for NRIs in {city}",
        "Sell Your {city} Asset Without Travelling to India",
    ],
    "management": [
        "NRI Property Management Services in {city}",
        "Trusted Remote Property Management in {city}",
        "Professional {city} Property Care for Overseas Owners",
        "End-to-End NRI Property Management in {city}",
        "Protect and Manage Your {city} Assets from Abroad",
    ],
    "rental": [
        "NRI Rental Management Services in {city}",
        "Tenant and Rental Coordination for NRIs in {city}",
        "Managed Rental Services for Overseas Owners in {city}",
        "NRI Landlord Support — Rentals in {city}",
        "Rent Out Your {city} Property Without Local Hassle",
    ],
    "maintenance": [
        "NRI Property Maintenance & Upkeep in {city}",
        "Property Care and Maintenance for NRIs in {city}",
        "Preventive and Reactive Maintenance for {city} Properties",
        "Keep Your {city} Property Protected from Abroad",
        "Scheduled Property Maintenance for Overseas Owners in {city}",
    ],
    "informational": [
        "How to Manage Property in {city} While Living Abroad",
        "NRI Property Ownership Guide — {city}",
        "Managing Your {city} Property Remotely — A Practical Guide",
        "Key Steps for NRIs Managing Property in {city}",
        "Remote Property Control for Overseas Owners in {city}",
    ],
    "buy": [
        "Property Investment Options in {city} for NRIs",
        "NRI Real Estate Opportunities in {city}",
        "Verified Properties in {city} for Overseas Buyers",
        "Buy Property in {city} from Abroad — NRI Guide",
        "NRI Property Acquisition in {city}",
    ],
}

# City+intent variant index: ensures each city×intent pair picks a different variant
_CITY_H1_INDEX = {"chennai": 0, "bangalore": 1, "hyderabad": 2}

# Intent-level offset so different intents within the same city get different variants
_INTENT_H1_OFFSET = {
    "nri-sell-property": 0,
    "nri-property-management": 1,
    "nri-rental-management": 2,
    "nri-property-maintenance": 3,
    "manage-property-from-abroad": 4,
    "nri-property-legal-support": 0,
    "nri-power-of-attorney": 1,
    "nri-property-tax": 2,
    "nri-capital-gains": 3,
    "nri-buy-villas": 0,
    "nri-buy-flats": 1,
    "nri-investment-properties": 2,
    "nri-luxury-properties": 3,
    "flats-for-sale": 0,
    "villas-for-sale": 1,
    "flats-for-rent": 2,
    "budget-properties": 3,
}

_INTENT_TITLE_PHRASE = {
    "nri-sell-property": "Sell NRI Property",
    "nri-property-management": "NRI Property Management",
    "nri-rental-management": "NRI Rental Management",
    "nri-property-maintenance": "NRI Property Maintenance",
    "manage-property-from-abroad": "Remote Property Management",
    "nri-property-legal-support": "NRI Property Legal Support",
    "nri-power-of-attorney": "NRI Power of Attorney",
    "nri-property-tax": "NRI Property Tax Guide",
    "nri-capital-gains": "NRI Capital Gains Tax Guide",
    "nri-buy-villas": "NRI Villa Investment",
    "nri-buy-flats": "NRI Flat Investment",
    "nri-investment-properties": "NRI Property Investment",
    "nri-luxury-properties": "NRI Luxury Properties",
    "flats-for-sale": "Flats for Sale",
    "villas-for-sale": "Villas for Sale",
    "flats-for-rent": "Flats for Rent",
    "budget-properties": "Budget Properties",
}

_INTENT_DESC_TEMPLATES = {
    "nri-sell-property": "Sell your {city} property from {nri} with Propertism. We manage pricing, buyer visits, legal vetting, and power of attorney closure without travel.",
    "nri-property-management": "Manage your {city} property from {nri} with Propertism's end-to-end services. We handle inspections, tenant care, maintenance, and monthly updates.",
    "nri-rental-management": "Rent out your {city} property from {nri} seamlessly. Propertism handles tenant screening, rental documentation, registered agreements, and rent collection.",
    "nri-property-maintenance": "Protect your {city} property from {nri} with scheduled inspections, professional repairs, monsoon prep, and verified photo-documented vendor updates.",
    "manage-property-from-abroad": "How to manage your {city} property from {nri}. Practical remote guide covering maintenance, tenant handling, legal compliance, and trusted local partners.",
    "nri-property-legal-support": "Coordinate {city} property legal clearance from {nri}. Propertism assists with title deeds search, document verification, registration, and compliance.",
    "nri-power-of-attorney": "Register a power of attorney for your {city} property from {nri}. We handle apostillation, notarisation, and sub-registrar filing without travel.",
    "nri-property-tax": "Manage and pay municipal property taxes for your {city} assets from {nri}. Prevent tax disputes, check land records, and ensure complete compliance.",
    "nri-capital-gains": "Optimize capital gains tax on {city} property sales from {nri}. Learn about TDS deductions, tax exemptions, and secure international fund transfers.",
    "nri-buy-villas": "Buy premium gated community villas in {city} from {nri} safely. We offer verified property listings, remote legal support, and complete post-purchase care.",
    "nri-buy-flats": "Invest in high-yield apartments and flats in {city} from {nri} safely. Get verified listings, clear title deeds verification, and tenant management.",
    "nri-investment-properties": "High-growth property investment options in {city} for NRIs in {nri}. Data-driven advisor search, title verification, and remote transaction assistance.",
    "nri-luxury-properties": "Explore premium luxury villas and flats in {city} from {nri}. Curated high-specification homes, verified documents, and on-ground transaction handling.",
    "flats-for-sale": "Buy verified flats and apartments in {city} from {nri} with direct builder pricing, legal vetting, and full remote-first home buying coordination.",
    "villas-for-sale": "Buy independent houses and gated villas in {city} from {nri}. Complete document verification, remote legal assistance, and post-purchase management.",
    "flats-for-rent": "Rent verified flats and apartments in {city} from {nri} with professional tenancy support, legal rental agreements, and secure security deposit handling.",
    "budget-properties": "Affordable homes and budget apartments in {city} from {nri} under 60 lakhs. Verified listings, home loan coordination, and remote purchase assistance.",
}


def build_differentiated_h1(intent_type, city_name, city_slug, nri_location=None, intent_slug=None, base_h1=None):
    """
    Return a unique H1 for the given intent x city x NRI combination.
    NRI geo pages use region-specific templates.
    City-only pages use base_h1 or fallback variants.
    """
    if nri_location:
        nri_name = nri_location.get("name", "")
        templates = _H1_TEMPLATES.get(intent_slug)
        if not templates:
            templates = _H1_TEMPLATES.get(f"nri-{intent_type}-property") or _H1_TEMPLATES.get("manage-property-from-abroad")
        
        idx = sum(ord(c) for c in nri_name) % len(templates)
        return templates[idx].format(city=city_name, nri=nri_name)

    if base_h1:
        return base_h1

    variants = _H1_CITY_VARIANTS.get(intent_type, _H1_CITY_VARIANTS["informational"])
    city_idx = _CITY_H1_INDEX.get(city_slug, 0)
    intent_offset = _INTENT_H1_OFFSET.get(intent_slug or "", 0)
    idx = (city_idx + intent_offset) % len(variants)
    return variants[idx].format(city=city_name)


def build_differentiated_title(config, city, nri_location=None):
    """
    Generate page title dynamically.
    Include: Service Intent, City, NRI Location Name, Brand Reference.
    """
    intent_slug = config.get("intent_slug", "")
    city_name = city.get("name", "Chennai")
    
    if nri_location:
        nri_name = nri_location.get("name", "")
        intent_phrase = _INTENT_TITLE_PHRASE.get(intent_slug)
        if not intent_phrase:
            intent_phrase = config.get("property_type_label", "Property Services")
        return f"{intent_phrase} in {city_name} for {nri_name} Residents | Propertism"
    
    base_title = config.get("title", "")
    if "Propertism" not in base_title:
        return f"{base_title} | Propertism"
    return base_title


def build_differentiated_description(config, city, nri_location=None):
    """
    Generate page description dynamically.
    Include: Service Intent, City, NRI Location Context, Primary Value Proposition.
    Must be within 140-160 characters limit.
    """
    intent_slug = config.get("intent_slug", "")
    city_name = city.get("name", "Chennai")
    
    if nri_location:
        nri_name = nri_location.get("name", "")
        template = _INTENT_DESC_TEMPLATES.get(intent_slug)
        if template:
            desc = template.format(city=city_name, nri=nri_name)
            if len(desc) > 160:
                desc = desc[:157] + "..."
            return desc
            
    return config.get("description", "")[:160]


# ---------------------------------------------------------------------------
# FAQ DIFFERENTIATION
# Keyed by intent_type. City and geo name injected at render time.
# ---------------------------------------------------------------------------

def build_faq_items(intent_type, city_name, nri_location=None):
    """Return a list of FAQ dicts for the given intent × city × geo."""
    geo_name = nri_location["name"] if nri_location else "abroad"
    geo_label = nri_location["label"] if nri_location else "outside India"

    faqs = {
        "sell": [
            {
                "question": f"Can I sell property in {city_name} without visiting India?",
                "answer": f"Yes. With a structured local execution partner in {city_name}, NRIs regularly complete property sales without travelling to India. The process uses a registered Power of Attorney for registration and local buyer coordination for all site visits.",
            },
            {
                "question": f"How long does an NRI property sale take in {city_name}?",
                "answer": f"A well-priced, fully-documented property in {city_name} typically sells within 3–6 months from listing to registration. Incomplete documentation or unrealistic pricing extends the timeline.",
            },
            {
                "question": "What is TDS on NRI property sale and who pays it?",
                "answer": "The buyer deducts TDS before paying the NRI seller — 20% for long-term capital gains, 30% for short-term. The NRI can file an income tax return and claim a refund if the actual liability is lower.",
            },
            {
                "question": f"How do I sell property in {city_name} from {geo_name}?",
                "answer": f"From {geo_label}, you execute a notarised and apostilled Power of Attorney, which is then registered in {city_name}. Your local partner handles buyer coordination, negotiation, documentation, and registration on your behalf.",
            },
        ],
        "management": [
            {
                "question": f"How does NRI property management work in {city_name}?",
                "answer": f"A professional property manager in {city_name} handles tenants, rent collection, maintenance decisions, periodic inspections, and owner reporting. You receive regular updates and approve decisions above an agreed threshold without managing day-to-day operations yourself.",
            },
            {
                "question": "How often will I receive property status updates?",
                "answer": "Monthly rent confirmation and quarterly inspection reports are the standard. Properties with active maintenance issues or new tenancies receive more frequent updates.",
            },
            {
                "question": f"What happens if my tenant in {city_name} stops paying rent?",
                "answer": "A structured manager follows a documented escalation process: reminder on day 6, formal notice on day 15, and legal proceedings if unresolved. You are notified at each stage, not weeks after the problem starts.",
            },
            {
                "question": f"Can I manage my {city_name} property from {geo_name} without visiting India?",
                "answer": f"Yes. Owners based in {geo_label} routinely manage {city_name} properties for years without visiting. Periodic inspections, tenant coordination, and maintenance are handled on the ground with documented reporting to you.",
            },
        ],
        "rental": [
            {
                "question": f"How do I find a good tenant for my {city_name} property from {geo_name}?",
                "answer": f"Through a local rental management partner who conducts background checks, verifies employment and income, checks references, and shortlists candidates matching your property's profile — all without requiring your presence in {city_name}.",
            },
            {
                "question": "What is the standard advance deposit for rentals in Chennai?",
                "answer": "In Chennai, the advance deposit (kaanom) for residential properties is typically 6–10 months' rent, significantly higher than in other Indian cities. This amount is refundable on move-out subject to deductions for damages.",
            },
            {
                "question": f"How is rent collected and transferred to NRIs in {geo_name}?",
                "answer": f"Rent is collected via direct bank transfer. Your property manager confirms collection monthly and remits funds to your designated account with documentation. International transfers from India follow FEMA guidelines.",
            },
            {
                "question": "Should the rental agreement be registered?",
                "answer": f"In Tamil Nadu, rental agreements for 12 months or more should be registered at the Sub-Registrar's office. Unregistered agreements for longer periods have limited legal enforceability. Your property manager handles registration as part of the tenancy setup in {city_name}.",
            },
        ],
        "maintenance": [
            {
                "question": f"How often should my {city_name} property be inspected?",
                "answer": f"Vacant properties in {city_name} should be checked monthly; tenanted properties quarterly. Each inspection produces a photo or video report shared with you so you can verify the property condition remotely.",
            },
            {
                "question": "What maintenance issues are most common for NRI properties in Chennai?",
                "answer": "Water seepage and terrace waterproofing failures are the most frequent and costly maintenance items, particularly after Chennai's monsoon season. Preventive waterproofing checks before June significantly reduce damage.",
            },
            {
                "question": "How are maintenance costs approved without me being in India?",
                "answer": "You set an approval threshold (e.g., repairs up to ₹5,000 can proceed without consultation; above that, the manager notifies you with documented quotes and photos before proceeding).",
            },
            {
                "question": f"Who handles emergency repairs in my {city_name} property when I am in {geo_name}?",
                "answer": f"Emergencies — burst pipes, electrical faults, security breaches — are handled immediately without waiting for owner approval. Your manager notifies you within 24 hours with a full report and photos of the issue and resolution.",
            },
        ],
        "informational": [
            {
                "question": f"What are the biggest challenges NRIs face managing property in {city_name}?",
                "answer": f"Distance, dependency on informal networks, unverified maintenance, undocumented tenancies, and delayed legal follow-up are the most common problems. A structured local partner with documented processes resolves each of these.",
            },
            {
                "question": "Do I need a Power of Attorney to manage my Indian property from abroad?",
                "answer": "Not for routine management tasks like collecting rent or approving repairs. A registered POA is required for property registration, certain legal proceedings, and sale transactions.",
            },
            {
                "question": f"How do NRIs in {geo_name} handle property tax compliance in {city_name}?",
                "answer": f"Property tax in {city_name} can be paid online through the Greater Chennai Corporation portal using net banking or international cards. NRIs in {geo_label} pay directly online without needing a local representative.",
            },
            {
                "question": f"Can I sell or rent my {city_name} property without visiting India?",
                "answer": f"Yes to both. Selling requires a registered POA for the registration step. Renting requires a local partner for tenant sourcing and agreement execution. Both can be completed from {geo_label}.",
            },
        ],
        "buy": [
            {
                "question": f"Can NRIs in {geo_name} buy property in {city_name} remotely?",
                "answer": f"Yes. NRIs can purchase residential property in India remotely. The purchase process involves document verification, sale agreement, registration (through POA if not visiting), and title transfer — all coordinated by a local partner in {city_name}.",
            },
            {
                "question": "Are there restrictions on what property NRIs can buy in India?",
                "answer": "NRIs can purchase residential and commercial properties in India freely. Agricultural land, plantation property, and farmhouses require special permissions from the Reserve Bank of India.",
            },
            {
                "question": f"What should NRIs check before buying property in {city_name}?",
                "answer": f"Title deed verification, encumbrance certificate (minimum 30 years), Patta status, building plan approval, occupancy certificate, and property tax clearance are the essential checks for any {city_name} property purchase.",
            },
            {
                "question": "How do I manage the property after buying it from abroad?",
                "answer": "Post-purchase, you need a property management partner who handles tenant sourcing, rent collection, maintenance, inspections, and compliance — giving you reliable on-ground execution without daily involvement.",
            },
        ],
    }

    return faqs.get(intent_type, faqs["informational"])


# ---------------------------------------------------------------------------
# TRUST BLOCK
# "Why Propertism" section — E-E-A-T signals per intent type
# ---------------------------------------------------------------------------

_TRUST_POINTS = {
    "sell": [
        {"heading": "15+ Years of NRI Property Experience", "body": "Our team has managed property transactions for NRIs across Chennai for over a decade. We understand the distance problem and build every sale process around transparent, documented execution."},
        {"heading": "End-to-End Sale Management", "body": "From pricing and listing to buyer coordination, legal documentation, and registration — we manage the entire sale without requiring you to travel to India."},
        {"heading": "Power of Attorney Expertise", "body": "We guide owners through safe POA setup, ensuring the document is properly executed abroad, apostilled, and registered in India for a legally valid transaction."},
        {"heading": "Transparent Owner Reporting", "body": "You receive updates at every stage — buyer enquiries, negotiation progress, documentation status, and registration confirmation — so you are never in the dark."},
    ],
    "management": [
        {"heading": "15+ Years Managing NRI Properties", "body": "Propertism has been the trusted local partner for NRI property owners in Chennai since 2009. Our processes are built around the specific challenges of distance ownership."},
        {"heading": "Documented Execution — Not Just Updates", "body": "We do not just report problems. We resolve them through a verified vendor network, documented maintenance records, and structured escalation."},
        {"heading": "Tenant Screening with Background Checks", "body": "Every tenant placed through Propertism goes through employment verification, identity checks, and reference calls before a single agreement is signed."},
        {"heading": "Monthly Rent Confirmation", "body": "Rent collection is confirmed in writing every month. You never need to chase your property manager for payment status."},
    ],
    "rental": [
        {"heading": "Full Tenant Lifecycle Management", "body": "From sourcing and screening to agreement, rent collection, renewals, and move-out coordination — we manage the complete tenant relationship so you do not have to."},
        {"heading": "Rental Agreement Registration", "body": "We register rental agreements at the Sub-Registrar's office where required, ensuring legal enforceability for NRI landlords."},
        {"heading": "Verified Tenant Network", "body": "Our tenant database is built from verified referrals and background-checked applicants. We do not place unverified tenants."},
        {"heading": "Rent Deposit Handling", "body": "Security deposits are documented, held in accordance with the rental agreement terms, and settled with a no-dues confirmation on move-out."},
    ],
    "maintenance": [
        {"heading": "Verified Local Vendor Network", "body": "We work with pre-verified plumbers, electricians, waterproofing specialists, and general contractors in Chennai — not ad-hoc strangers found at short notice."},
        {"heading": "Photo-Documented Every Visit", "body": "Every inspection and maintenance job is documented with before-and-after photos shared with the owner. You see exactly what was done."},
        {"heading": "Monsoon Preparation Protocol", "body": "Chennai's monsoon season requires specific preparation — terrace waterproofing, drain clearing, and seepage checks. We run these proactively every year."},
        {"heading": "Owner-Approved Spending Thresholds", "body": "You set the approval limit. Routine maintenance proceeds without delay; larger repairs are approved by you with documented quotes before work begins."},
    ],
    "informational": [
        {"heading": "Practical Guidance — Not Generic Advice", "body": "Our guides reflect real NRI property problems solved in Chennai over 15+ years — not copied regulatory summaries."},
        {"heading": "End-to-End NRI Service Coverage", "body": "From management and rental to sale, maintenance, and legal support — Propertism covers the complete ownership lifecycle for NRI property owners."},
        {"heading": "Local Execution with Transparent Reporting", "body": "Everything we do is documented and shared with the owner. You get clarity on what is happening with your property without having to ask repeatedly."},
        {"heading": "NRI-First Operating Model", "body": "Our entire service model is built around the constraints of distance ownership — remote approvals, digital documentation, and communication across time zones."},
    ],
    "buy": [
        {"heading": "Verified Listings Only", "body": "Every property in our portfolio has been assessed for documentation completeness, title clarity, and market pricing before being presented to NRI buyers."},
        {"heading": "Post-Purchase Management Ready", "body": "Once you buy, we can immediately transition to full property management — tenant sourcing, maintenance, and reporting — so your investment is productive from day one."},
        {"heading": "Remote Purchase Support", "body": "From due diligence and document verification to registration (through POA) and key handover — we manage the complete purchase process without requiring multiple India trips."},
        {"heading": "15+ Years in Chennai Real Estate", "body": "Our team's deep knowledge of Chennai's micro-markets, pricing corridors, and documentation requirements protects NRI buyers from common transaction risks."},
    ],
}


def build_trust_block(intent_type):
    """Return the 'Why Propertism' trust points for the given intent."""
    return _TRUST_POINTS.get(intent_type, _TRUST_POINTS["informational"])


# ---------------------------------------------------------------------------
# KNOWLEDGE HUB INTERNAL LINKS
# Keyed by intent_type → relevant article slugs + labels
# ---------------------------------------------------------------------------

_HUB_LINKS = {
    "sell": [
        {"slug": "how-nris-can-sell-property-in-india-from-abroad", "label": "How NRIs Can Sell Property in India from Abroad"},
        {"slug": "power-of-attorney-for-nris-complete-guide", "label": "Power of Attorney for NRIs: Complete Guide"},
        {"slug": "capital-gains-tax-property-sale-nris", "label": "Capital Gains Tax on Property Sale for NRIs"},
        {"slug": "how-to-verify-property-documents-chennai", "label": "How to Verify Property Documents in Chennai"},
    ],
    "management": [
        {"slug": "nri-property-management-chennai-complete-guide", "label": "NRI Property Management in Chennai: Complete Guide"},
        {"slug": "tenant-management-guide-overseas-property-owners", "label": "Tenant Management Guide for Overseas Owners"},
        {"slug": "nri-property-maintenance-checklist", "label": "NRI Property Maintenance Checklist"},
    ],
    "rental": [
        {"slug": "tenant-management-guide-overseas-property-owners", "label": "Tenant Management Guide for Overseas Owners"},
        {"slug": "nri-property-management-chennai-complete-guide", "label": "NRI Property Management in Chennai: Complete Guide"},
        {"slug": "how-to-verify-property-documents-chennai", "label": "How to Verify Property Documents in Chennai"},
    ],
    "maintenance": [
        {"slug": "nri-property-maintenance-checklist", "label": "NRI Property Maintenance Checklist"},
        {"slug": "nri-property-management-chennai-complete-guide", "label": "NRI Property Management in Chennai: Complete Guide"},
        {"slug": "tenant-management-guide-overseas-property-owners", "label": "Tenant Management Guide for Overseas Owners"},
    ],
    "informational": [
        {"slug": "nri-property-management-chennai-complete-guide", "label": "NRI Property Management in Chennai: Complete Guide"},
        {"slug": "how-nris-can-sell-property-in-india-from-abroad", "label": "How NRIs Can Sell Property in India from Abroad"},
        {"slug": "power-of-attorney-for-nris-complete-guide", "label": "Power of Attorney for NRIs: Complete Guide"},
        {"slug": "how-to-verify-property-documents-chennai", "label": "How to Verify Property Documents in Chennai"},
        {"slug": "property-tax-guide-chennai-nris", "label": "Property Tax Guide for Chennai NRIs"},
        {"slug": "patta-transfer-process-explained", "label": "Patta Transfer Process Explained"},
        {"slug": "encumbrance-certificate-guide-for-nris", "label": "Encumbrance Certificate Guide for NRIs"},
        {"slug": "capital-gains-tax-property-sale-nris", "label": "Capital Gains Tax on Property Sale for NRIs"},
    ],
    "buy": [
        {"slug": "how-to-verify-property-documents-chennai", "label": "How to Verify Property Documents in Chennai"},
        {"slug": "nri-property-management-chennai-complete-guide", "label": "NRI Property Management in Chennai: Complete Guide"},
        {"slug": "patta-transfer-process-explained", "label": "Patta Transfer Process Explained"},
        {"slug": "encumbrance-certificate-guide-for-nris", "label": "Encumbrance Certificate Guide for NRIs"},
    ],
}


def build_knowledge_hub_links(intent_type):
    """Return list of {slug, label} dicts for relevant knowledge hub articles."""
    return _HUB_LINKS.get(intent_type, _HUB_LINKS["informational"])


# ---------------------------------------------------------------------------
# SINGLE ENTRY POINT
# ---------------------------------------------------------------------------

def build_enrichment_context(config, city, nri_location=None):
    """
    Return a dict of enrichment context values to merge into landing_page context.
    Provides: differentiated_h1, page_title, page_description,
              faq_items (all intents), trust_points,
              knowledge_hub_links, enrichment_word_count.
    """
    intent_type = config.get("intent_type", "buy")
    intent_slug = config.get("intent_slug")
    city_name = city["name"]
    city_slug = config.get("city_slug", "chennai")

    differentiated_h1 = build_differentiated_h1(
        intent_type, city_name, city_slug, nri_location,
        intent_slug=intent_slug, base_h1=config.get("h1")
    )
    
    page_title = build_differentiated_title(config, city, nri_location)
    page_description = build_differentiated_description(config, city, nri_location)
    
    faq_items = build_faq_items(intent_type, city_name, nri_location)
    trust_points = build_trust_block(intent_type)
    hub_links = build_knowledge_hub_links(intent_type)

    # Estimate enrichment word count contribution for quality gate
    faq_words = sum(len(f["question"].split()) + len(f["answer"].split()) for f in faq_items)
    trust_words = sum(len(t["heading"].split()) + len(t["body"].split()) for t in trust_points)
    enrichment_word_count = faq_words + trust_words

    return {
        "differentiated_h1": differentiated_h1,
        "page_title": page_title,
        "page_description": page_description,
        "enriched_faq_items": faq_items,
        "trust_points": trust_points,
        "knowledge_hub_links": hub_links,
        "enrichment_word_count": enrichment_word_count,
    }
