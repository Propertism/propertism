"""
locality_registry.py — SCCB-PRT-LOCALITY-UNIFY-001

Single source of truth for all Chennai/Tamil Nadu locality data across
propertism.in and the Deal Engine.

Every other consumer (site_context.py dropdown, inquiry_fields.py extraction,
index.html filter UI) derives from this registry. NEVER hardcode locality
lists elsewhere.

Structure:
  LOCALITY_REGISTRY: List[dict] — master list of known localities.
  Each entry has:
    - slug:     URL-safe unique identifier (hyphenated, lowercase)
    - display:  Full human-readable label for emails, lead details, and UI
    - short_display: Compact dropdown label, computed from display at import time
    - zone:     Geographic zone for optgroup grouping (central, omr, ecr,
                south, west, north, tn)
    - aliases:  List[str] — known variants, misspellings, and sub-localities
                for backend text extraction (never shown in UI).
                First alias is always the canonical short name.
    - show_in_dropdown: bool — True for user-facing dropdown options,
                False for extraction-only entries (niche/alias variants).

Usage:
    from content.locality_registry import LOCALITY_REGISTRY
"""

LOCALITY_REGISTRY = [
    # ── Central Chennai ──────────────────────────────────────────────────
    {
        "slug": "adyar",
        "display": "Adyar, Chennai",
        "zone": "central",
        "aliases": ["adyar", "gandhi nagar adyar", "kasturibai nagar adyar", "adyar gandhi nagar"],
        "show_in_dropdown": True,
    },
    {
        "slug": "besant-nagar",
        "display": "Besant Nagar, Chennai",
        "zone": "central",
        "aliases": ["besant nagar", "besantnagar", "elliots beach"],
        "show_in_dropdown": True,
    },
    {
        "slug": "mylapore",
        "display": "Mylapore, Chennai",
        "zone": "central",
        "aliases": ["mylapore", "mylapore chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "t-nagar",
        "display": "T. Nagar, Chennai",
        "zone": "central",
        "aliases": ["t.nagar", "t nagar", "tnagar", "thyagaraya nagar"],
        "show_in_dropdown": True,
    },
    {
        "slug": "nungambakkam",
        "display": "Nungambakkam, Chennai",
        "zone": "central",
        "aliases": ["nungambakkam", "nungambakam"],
        "show_in_dropdown": True,
    },
    {
        "slug": "alwarpet",
        "display": "Alwarpet, Chennai",
        "zone": "central",
        "aliases": ["alwarpet", "alwarpet chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "triplicane",
        "display": "Triplicane, Chennai",
        "zone": "central",
        "aliases": ["triplicane", "thiruvallikeni"],
        "show_in_dropdown": True,
    },
    {
        "slug": "kilpauk",
        "display": "Kilpauk, Chennai",
        "zone": "central",
        "aliases": ["kilpauk", "kilpauk chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "egmore",
        "display": "Egmore, Chennai",
        "zone": "central",
        "aliases": ["egmore", "ezhumur"],
        "show_in_dropdown": True,
    },
    {
        "slug": "royapettah",
        "display": "Royapettah, Chennai",
        "zone": "central",
        "aliases": ["royapettah", "royapet"],
        "show_in_dropdown": True,
    },
    {
        "slug": "teynampet",
        "display": "Teynampet, Chennai",
        "zone": "central",
        "aliases": ["teynampet", "teynampet chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "r-a-puram",
        "display": "R.A. Puram, Chennai",
        "zone": "central",
        "aliases": ["r a puram", "ra puram", "rajarathnam puram"],
        "show_in_dropdown": True,
    },
    {
        "slug": "poes-garden",
        "display": "Poes Garden, Chennai",
        "zone": "central",
        "aliases": ["poes garden", "poes garden chennai"],
        "show_in_dropdown": False,
    },
    {
        "slug": "boat-club",
        "display": "Boat Club, Chennai",
        "zone": "central",
        "aliases": ["boat club", "boat club chennai"],
        "show_in_dropdown": False,
    },
    {
        "slug": "kotturpuram",
        "display": "Kotturpuram, Chennai",
        "zone": "central",
        "aliases": ["kotturpuram", "kottur", "kottur garden"],
        "show_in_dropdown": True,
    },
    {
        "slug": "purasaiwalkam",
        "display": "Purasaiwalkam, Chennai",
        "zone": "central",
        "aliases": ["purasaiwalkam", "purasawalkam", "purasai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "gopalapuram",
        "display": "Gopalapuram, Chennai",
        "zone": "central",
        "aliases": ["gopalapuram", "gopalapuram chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "chetpet",
        "display": "Chetpet, Chennai",
        "zone": "central",
        "aliases": ["chetpet", "chetpet chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "kodambakkam",
        "display": "Kodambakkam, Chennai",
        "zone": "central",
        "aliases": ["kodambakkam", "kodambakam"],
        "show_in_dropdown": True,
    },
    {
        "slug": "choolaimedu",
        "display": "Choolaimedu, Chennai",
        "zone": "central",
        "aliases": ["choolaimedu", "choolaimedu chennai", "chaimedu"],
        "show_in_dropdown": True,
    },
    {
        "slug": "west-mambalam",
        "display": "West Mambalam, Chennai",
        "zone": "central",
        "aliases": ["west mambalam", "mambalam", "west mambalam chennai"],
        "show_in_dropdown": True,
    },

    # ── OMR (Old Mahabalipuram Road) ────────────────────────────────────
    {
        "slug": "perungudi",
        "display": "Perungudi (OMR), Chennai",
        "zone": "omr",
        "aliases": ["perungudi", "omr perungudi"],
        "show_in_dropdown": True,
    },
    {
        "slug": "thoraipakkam",
        "display": "Thoraipakkam (OMR), Chennai",
        "zone": "omr",
        "aliases": ["thoraipakkam", "thoraipakam", "thoraipakkam omr"],
        "show_in_dropdown": True,
    },
    {
        "slug": "sholinganallur",
        "display": "Sholinganallur (OMR), Chennai",
        "zone": "omr",
        "aliases": ["sholinganallur", "sholinganallor", "omr sholinganallur"],
        "show_in_dropdown": True,
    },
    {
        "slug": "navalur",
        "display": "Navalur (OMR), Chennai",
        "zone": "omr",
        "aliases": ["navalur", "navalur omr"],
        "show_in_dropdown": True,
    },
    {
        "slug": "padur",
        "display": "Padur (OMR), Chennai",
        "zone": "omr",
        "aliases": ["padur", "padur omr"],
        "show_in_dropdown": True,
    },
    {
        "slug": "kelambakkam",
        "display": "Kelambakkam (OMR), Chennai",
        "zone": "omr",
        "aliases": ["kelambakkam", "kelambakam", "omr kelambakkam"],
        "show_in_dropdown": True,
    },
    {
        "slug": "taramani",
        "display": "Taramani, Chennai",
        "zone": "omr",
        "aliases": ["taramani", "taramani omr"],
        "show_in_dropdown": True,
    },

    # ── ECR (East Coast Road) ───────────────────────────────────────────
    {
        "slug": "palavakkam",
        "display": "Palavakkam (ECR), Chennai",
        "zone": "ecr",
        "aliases": ["palavakkam", "palavakkam ecr"],
        "show_in_dropdown": True,
    },
    {
        "slug": "neelankarai",
        "display": "Neelankarai (ECR), Chennai",
        "zone": "ecr",
        "aliases": ["neelankarai", "neelangarai", "neelankarai ecr"],
        "show_in_dropdown": True,
    },
    {
        "slug": "akkarai",
        "display": "Akkarai (ECR), Chennai",
        "zone": "ecr",
        "aliases": ["akkarai", "akkarai ecr"],
        "show_in_dropdown": True,
    },
    {
        "slug": "uthandi",
        "display": "Uthandi (ECR), Chennai",
        "zone": "ecr",
        "aliases": ["uthandi", "uthandi ecr"],
        "show_in_dropdown": True,
    },
    {
        "slug": "injambakkam",
        "display": "Injambakkam (ECR), Chennai",
        "zone": "ecr",
        "aliases": ["injambakkam", "injambakkam ecr", "inja"],
        "show_in_dropdown": True,
    },

    # ── South Chennai ────────────────────────────────────────────────────
    {
        "slug": "velachery",
        "display": "Velachery, Chennai",
        "zone": "south",
        "aliases": ["velachery", "velachery chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "nanganallur",
        "display": "Nanganallur, Chennai",
        "zone": "south",
        "aliases": ["nanganallur", "nanganallur chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "madipakkam",
        "display": "Madipakkam, Chennai",
        "zone": "south",
        "aliases": ["madipakkam", "madipakkam chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "chromepet",
        "display": "Chromepet, Chennai",
        "zone": "south",
        "aliases": ["chromepet", "chrome pet", "chrompet"],
        "show_in_dropdown": True,
    },
    {
        "slug": "tambaram",
        "display": "Tambaram, Chennai",
        "zone": "south",
        "aliases": ["tambaram", "tambarm", "tambaram chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "pallavaram",
        "display": "Pallavaram, Chennai",
        "zone": "south",
        "aliases": ["pallavaram", "pallavaram chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "saidapet",
        "display": "Saidapet, Chennai",
        "zone": "south",
        "aliases": ["saidapet", "saidapet chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "medavakkam",
        "display": "Medavakkam, Chennai",
        "zone": "south",
        "aliases": ["medavakkam", "medavakkam chennai", "medavakam"],
        "show_in_dropdown": True,
    },
    {
        "slug": "pallikaranai",
        "display": "Pallikaranai, Chennai",
        "zone": "south",
        "aliases": ["pallikaranai", "pallikarani", "pallikaranai chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "perumbakkam",
        "display": "Perumbakkam, Chennai",
        "zone": "south",
        "aliases": ["perumbakkam", "perumbakkam chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "semmancheri",
        "display": "Semmancheri, Chennai",
        "zone": "south",
        "aliases": ["semmancheri", "semmancheri chennai", "semanchheri"],
        "show_in_dropdown": True,
    },
    {
        "slug": "adambakkam",
        "display": "Adambakkam, Chennai",
        "zone": "south",
        "aliases": ["adambakkam", "adambakkam chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "thiruvanmiyur",
        "display": "Thiruvanmiyur, Chennai",
        "zone": "south",
        "aliases": ["thiruvanmiyur", "thiruvanmyur", "thiruvamiyur", "tiruvanmiyur"],
        "show_in_dropdown": True,
    },
    {
        "slug": "indira-nagar",
        "display": "Indira Nagar, Chennai",
        "zone": "south",
        "aliases": ["indira nagar", "indiranagar", "indira nagar chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "selaiyur",
        "display": "Selaiyur, Chennai",
        "zone": "south",
        "aliases": ["selaiyur", "selaiyur chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "chitlapakkam",
        "display": "Chitlapakkam, Chennai",
        "zone": "south",
        "aliases": ["chitlapakkam", "chitlapakkam chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "perungalathur",
        "display": "Perungalathur, Chennai",
        "zone": "south",
        "aliases": ["perungalathur", "peungalathur", "perungalathur chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "vandalur",
        "display": "Vandalur, Chennai",
        "zone": "south",
        "aliases": ["vandalur", "vandalur chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "keelkattalai",
        "display": "Keelkattalai, Chennai",
        "zone": "south",
        "aliases": ["keelkattalai", "kilkattalai", "keelkatalai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "kovilambakkam",
        "display": "Kovilambakkam, Chennai",
        "zone": "south",
        "aliases": ["kovilambakkam", "kovilambakam"],
        "show_in_dropdown": True,
    },
    {
        "slug": "shastri-nagar",
        "display": "Shastri Nagar, Chennai",
        "zone": "south",
        "aliases": ["shastri nagar", "shastrinagar"],
        "show_in_dropdown": True,
    },

    # ── West Chennai ─────────────────────────────────────────────────────
    {
        "slug": "anna-nagar",
        "display": "Anna Nagar, Chennai",
        "zone": "west",
        "aliases": ["anna nagar", "annanagar", "anna nagar chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "mogappair",
        "display": "Mogappair, Chennai",
        "zone": "west",
        "aliases": ["mogappair", "mogapair", "mogappair chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "porur",
        "display": "Porur, Chennai",
        "zone": "west",
        "aliases": ["porur", "porur chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "poonamallee",
        "display": "Poonamallee, Chennai",
        "zone": "west",
        "aliases": ["poonamallee", "poonamalle", "poona malaee"],
        "show_in_dropdown": True,
    },
    {
        "slug": "guindy",
        "display": "Guindy, Chennai",
        "zone": "west",
        "aliases": ["guindy", "guindy chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "vadapalani",
        "display": "Vadapalani, Chennai",
        "zone": "west",
        "aliases": ["vadapalani", "vadapalani chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "kk-nagar",
        "display": "KK Nagar, Chennai",
        "zone": "west",
        "aliases": ["kk nagar", "k.k. nagar", "k.k nagar", "kknagar"],
        "show_in_dropdown": True,
    },
    {
        "slug": "koyambedu",
        "display": "Koyambedu, Chennai",
        "zone": "west",
        "aliases": ["koyambedu", "koyambedu chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "ambattur",
        "display": "Ambattur, Chennai",
        "zone": "west",
        "aliases": ["ambattur", "ambattur chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "avadi",
        "display": "Avadi, Chennai",
        "zone": "west",
        "aliases": ["avadi", "avadi chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "maduravoyal",
        "display": "Maduravoyal, Chennai",
        "zone": "west",
        "aliases": ["maduravoyal", "maduravoyal chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "ashok-nagar",
        "display": "Ashok Nagar, Chennai",
        "zone": "west",
        "aliases": ["ashok nagar", "ashoknagar"],
        "show_in_dropdown": True,
    },
    {
        "slug": "virugambakkam",
        "display": "Virugambakkam, Chennai",
        "zone": "west",
        "aliases": ["virugambakkam", "virugambakam"],
        "show_in_dropdown": True,
    },
    {
        "slug": "saligramam",
        "display": "Saligramam, Chennai",
        "zone": "west",
        "aliases": ["saligramam", "saligramam chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "valasaravakkam",
        "display": "Valasaravakkam, Chennai",
        "zone": "west",
        "aliases": ["valasaravakkam", "valasaravakam"],
        "show_in_dropdown": True,
    },
    {
        "slug": "ramapuram",
        "display": "Ramapuram, Chennai",
        "zone": "west",
        "aliases": ["ramapuram", "ramapuram chennai"],
        "show_in_dropdown": True,
    },

    # ── North Chennai ────────────────────────────────────────────────────
    {
        "slug": "kolathur",
        "display": "Kolathur, Chennai",
        "zone": "north",
        "aliases": ["kolathur", "kolathur chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "madhavaram",
        "display": "Madhavaram, Chennai",
        "zone": "north",
        "aliases": ["madhavaram", "madhavaram chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "perambur",
        "display": "Perambur, Chennai",
        "zone": "north",
        "aliases": ["perambur", "perambur chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "villivakkam",
        "display": "Villivakkam, Chennai",
        "zone": "north",
        "aliases": ["villivakkam", "villivakkam chennai", "villiwakkam"],
        "show_in_dropdown": True,
    },
    {
        "slug": "manali",
        "display": "Manali, Chennai",
        "zone": "north",
        "aliases": ["manali", "manali chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "thiruvottiyur",
        "display": "Thiruvottiyur, Chennai",
        "zone": "north",
        "aliases": ["thiruvottiyur", "tiruvottiyur", "thiruvotriyur"],
        "show_in_dropdown": True,
    },
    {
        "slug": "ennore",
        "display": "Ennore, Chennai",
        "zone": "north",
        "aliases": ["ennore", "ennore chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "tondiarpet",
        "display": "Tondiarpet, Chennai",
        "zone": "north",
        "aliases": ["tondiarpet", "tondiarpet chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "royapuram",
        "display": "Royapuram, Chennai",
        "zone": "north",
        "aliases": ["royapuram", "royapuram chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "washermanpet",
        "display": "Washermanpet, Chennai",
        "zone": "north",
        "aliases": ["washermanpet", "washermanpet chennai", "vannarapettai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "red-hills",
        "display": "Red Hills, Chennai",
        "zone": "north",
        "aliases": ["red hills", "redhills"],
        "show_in_dropdown": True,
    },
    {
        "slug": "vyasarpadi",
        "display": "Vyasarpadi, Chennai",
        "zone": "north",
        "aliases": ["vyasarpadi", "vyasarpady"],
        "show_in_dropdown": True,
    },
    {
        "slug": "korukkupet",
        "display": "Korukkupet, Chennai",
        "zone": "north",
        "aliases": ["korukkupet", "korukupet"],
        "show_in_dropdown": True,
    },

    # ── Rest of Tamil Nadu ───────────────────────────────────────────────
    {
        "slug": "coimbatore",
        "display": "Coimbatore",
        "zone": "tn",
        "aliases": ["coimbatore", "kovai", "coimbatore chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "madurai",
        "display": "Madurai",
        "zone": "tn",
        "aliases": ["madurai", "madurai chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "trichy",
        "display": "Trichy",
        "zone": "tn",
        "aliases": ["trichy", "tiruchirappalli", "trichy chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "salem",
        "display": "Salem",
        "zone": "tn",
        "aliases": ["salem", "salem chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "sriperumbudur",
        "display": "Sriperumbudur",
        "zone": "tn",
        "aliases": ["sriperumbudur", "sriperumbudur chennai", "sriperumpudur"],
        "show_in_dropdown": True,
    },
    {
        "slug": "thiruvallur",
        "display": "Thiruvallur",
        "zone": "tn",
        "aliases": ["thiruvallur", "tiruvallur"],
        "show_in_dropdown": True,
    },
    {
        "slug": "guduvanchery",
        "display": "Guduvanchery",
        "zone": "tn",
        "aliases": ["guduvanchery", "guduvancheri", "guduvancherry"],
        "show_in_dropdown": True,
    },
    {
        "slug": "oragadam",
        "display": "Oragadam",
        "zone": "tn",
        "aliases": ["oragadam", "oragadam chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "urapakkam",
        "display": "Urapakkam",
        "zone": "tn",
        "aliases": ["urapakkam", "urapakam", "urapakkam chennai"],
        "show_in_dropdown": True,
    },
    {
        "slug": "singaperumal-koil",
        "display": "Singaperumal Koil",
        "zone": "tn",
        "aliases": ["singaperumal koil", "singaperumalkoil", "sp koil"],
        "show_in_dropdown": True,
    },

    # ── Generic / Non-specific ───────────────────────────────────────────
    {
        "slug": "other",
        "display": "Other, please specify",
        "zone": "other",
        "aliases": ["other", "others"],
        "show_in_dropdown": True,
    },
]


CHENNAI_ZONES = frozenset({"central", "omr", "ecr", "south", "west", "north"})

# Canonical labels for locality dropdown group headers. Keep zone keys stable:
# they are part of the registry contract shared with extraction and integrations.
ZONE_DISPLAY_NAMES = {
    "central": "Central Chennai",
    "omr": "OMR (IT Corridor)",
    "ecr": "ECR",
    "south": "South Chennai / Suburbs",
    "west": "West Chennai",
    "north": "North Chennai",
    "tn": "Other Tamil Nadu",
    "other": "Other",
}

for _locality in LOCALITY_REGISTRY:
    _display = _locality["display"]
    _locality["short_display"] = (
        _display.removesuffix(", Chennai")
        if _locality["zone"] in CHENNAI_ZONES
        else _display
    )


def get_dropdown_choices():
    """Return list of (slug, display) tuples for use in Django form dropdowns,
    grouped by zone for optgroup rendering."""
    return [
        (entry["slug"], entry["display"])
        for entry in LOCALITY_REGISTRY
        if entry["show_in_dropdown"]
    ]


def get_dropdown_grouped():
    """Return dict of zone -> [(slug, display), ...] for optgroup rendering."""
    grouped = {}
    for entry in LOCALITY_REGISTRY:
        if not entry["show_in_dropdown"]:
            continue
        zone = entry["zone"]
        if zone not in grouped:
            grouped[zone] = []
        grouped[zone].append((entry["slug"], entry["short_display"]))
    return grouped


def get_extraction_keywords():
    """Return list[str] of all aliases + slugs for free-text matching.
    This is what inquiry_fields.py uses."""
    keywords = []
    for entry in LOCALITY_REGISTRY:
        keywords.append(entry["slug"].replace("-", " "))
        keywords.extend(entry["aliases"])
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for kw in keywords:
        lower = kw.lower().strip()
        if lower not in seen:
            seen.add(lower)
            result.append(lower)
    return result