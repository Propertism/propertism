"""
chat/inquiry_fields.py — M2.6 Configuration-driven Inquiry Field Registry

All inquiry field definitions live here. Adding a future field requires only
a new entry in INQUIRY_FIELD_CONFIG — the engine and extractor read from this
registry dynamically. No engine code changes required for new fields.
"""

# ── Field ordering ─────────────────────────────────────────────────────────────

MANDATORY_FIELDS_ORDER = [
    'customer_name',
    'country',
    'mobile_number',
    'service_required',
    'inquiry_message',
]

OPTIONAL_FIELDS_ORDER = [
    'email_address',
    'preferred_contact_time',
    'preferred_location',
    'budget',
    'property_type',
    'timeline',
    'additional_remarks',
]

# ── Field registry ─────────────────────────────────────────────────────────────

INQUIRY_FIELD_CONFIG = {
    'customer_name': {
        'label':     'Your Name',
        'prompt':    "May I have your full name please?",
        'validation': 'name',
        'mandatory': True,
        'order':     1,
        'skippable': False,
        'chips':     [],
    },
    'country': {
        'label':     'Country',
        'prompt':    "Which country are you currently based in?",
        'validation': 'country',
        'mandatory': True,
        'order':     2,
        'skippable': False,
        'chips':     ['India', 'USA', 'UK', 'UAE', 'Canada', 'Australia', 'Singapore'],
    },
    'mobile_number': {
        'label':     'Mobile Number',
        'prompt':    "Please share your mobile number.",
        'validation': 'phone',
        'mandatory': True,
        'order':     3,
        'skippable': False,
        'chips':     [],
        'depends_on': 'country',  # phone validator uses country context
    },
    'service_required': {
        'label':     'Service Required',
        'prompt':    "What service are you looking for?",
        'validation': 'service',
        'mandatory': True,
        'order':     4,
        'skippable': False,
        'chips':     [
            'Buy Property',
            'Sell Property',
            'Rental Management',
            'NRI Assist',
            'Property Search',
            'Land / Plot',
        ],
    },
    'inquiry_message': {
        'label':     'Inquiry Details',
        'prompt':    "Please describe your requirement or question briefly:",
        'validation': 'message',
        'mandatory': True,
        'order':     5,
        'skippable': False,
        'chips':     [],
    },
    'email_address': {
        'label':     'Email Address',
        'prompt':    "Could you share your email address? (optional — type Skip to continue)",
        'validation': 'email',
        'mandatory': False,
        'order':     6,
        'skippable': True,
        'chips':     ['Skip'],
    },
    'preferred_contact_time': {
        'label':     'Preferred Contact Time',
        'prompt':    "When is the best time to reach you? (optional)",
        'validation': 'free_text',
        'mandatory': False,
        'order':     7,
        'skippable': True,
        'chips':     ['Morning', 'Afternoon', 'Evening', 'Anytime', 'Skip'],
    },
    'preferred_location': {
        'label':     'Preferred Location',
        'prompt':    "Do you have a preferred location in Chennai? (optional)",
        'validation': 'free_text',
        'mandatory': False,
        'order':     8,
        'skippable': True,
        'chips':     ['Anna Nagar', 'T.Nagar', 'Adyar', 'OMR', 'ECR', 'Velachery', 'Skip'],
    },
    'budget': {
        'label':     'Budget',
        'prompt':    "What is your approximate budget? (optional)",
        'validation': 'budget',
        'mandatory': False,
        'order':     9,
        'skippable': True,
        'chips':     ['Under ₹50L', '₹50L–₹1Cr', '₹1Cr–₹2Cr', 'Above ₹2Cr', 'Skip'],
    },
    'property_type': {
        'label':     'Property Type',
        'prompt':    "What type of property are you interested in? (optional)",
        'validation': 'free_text',
        'mandatory': False,
        'order':     10,
        'skippable': True,
        'chips':     ['Apartment', 'Villa', 'Plot', 'Commercial', 'Independent House', 'Skip'],
    },
    'timeline': {
        'label':     'Timeline',
        'prompt':    "What is your timeline for this? (optional)",
        'validation': 'free_text',
        'mandatory': False,
        'order':     11,
        'skippable': True,
        'chips':     ['Immediately', 'Within 3 months', 'Within 6 months', 'Within a year', 'Skip'],
    },
    'additional_remarks': {
        'label':     'Additional Remarks',
        'prompt':    "Any additional remarks you'd like to share? (optional)",
        'validation': 'free_text',
        'mandatory': False,
        'order':     12,
        'skippable': True,
        'chips':     ['Skip'],
    },
}

# ── Cancel / confirmation keyword sets ────────────────────────────────────────

CANCEL_KEYWORDS = frozenset([
    'cancel', 'stop', 'exit', 'quit', 'abort',
    'never mind', 'nevermind', 'forget it', 'no thanks',
    'not interested', 'leave', 'bye', 'close',
])

CONFIRM_KEYWORDS = frozenset([
    'yes', 'confirm', 'submit', 'ok', 'okay', 'correct',
    'proceed', 'go ahead', 'sure', 'absolutely', 'right',
    'that is correct', 'looks good', 'perfect', 'submit now',
])

SKIP_KEYWORDS = frozenset([
    'skip', 'no', 'nope', 'pass', 'next', 'none', 'later',
    'not now', 'not applicable', 'na', 'n/a',
])

# ── Known country list (keyword → normalised name) ────────────────────────────

KNOWN_COUNTRIES = {
    'india': 'India',
    'indian': 'India',
    'usa': 'USA',
    'united states': 'USA',
    'united states of america': 'USA',
    'us': 'USA',
    'america': 'USA',
    'uk': 'UK',
    'united kingdom': 'UK',
    'england': 'UK',
    'britain': 'UK',
    'uae': 'UAE',
    'united arab emirates': 'UAE',
    'dubai': 'UAE',
    'abu dhabi': 'UAE',
    'canada': 'Canada',
    'canadian': 'Canada',
    'australia': 'Australia',
    'australian': 'Australia',
    'aus': 'Australia',
    'singapore': 'Singapore',
    'sg': 'Singapore',
    'germany': 'Germany',
    'france': 'France',
    'malaysia': 'Malaysia',
    'new zealand': 'New Zealand',
    'nz': 'New Zealand',
    'south africa': 'South Africa',
    'japan': 'Japan',
    'bahrain': 'Bahrain',
    'qatar': 'Qatar',
    'kuwait': 'Kuwait',
    'oman': 'Oman',
    'saudi arabia': 'Saudi Arabia',
    'ksa': 'Saudi Arabia',
    'netherlands': 'Netherlands',
    'sweden': 'Sweden',
    'switzerland': 'Switzerland',
    'ireland': 'Ireland',
    'norway': 'Norway',
    'denmark': 'Denmark',
    'italy': 'Italy',
    'spain': 'Spain',
    'portugal': 'Portugal',
    'belgium': 'Belgium',
    'austria': 'Austria',
    'finland': 'Finland',
}

# ── Service keyword → normalised service name ─────────────────────────────────

SERVICE_KEYWORD_MAP = {
    'buy':          'Buy Property',
    'buying':       'Buy Property',
    'purchase':     'Buy Property',
    'purchasing':   'Buy Property',
    'acquire':      'Buy Property',
    'acquisition':  'Buy Property',
    'invest':       'Buy Property',
    'investing':    'Buy Property',
    'investment':   'Buy Property',
    'sell':         'Sell Property',
    'selling':      'Sell Property',
    'sale':         'Sell Property',
    'selling off':  'Sell Property',
    'disposal':     'Sell Property',
    'rent':         'Rental Management',
    'rental':       'Rental Management',
    'renting':      'Rental Management',
    'lease':        'Rental Management',
    'leasing':      'Rental Management',
    'tenant':       'Rental Management',
    'tenancy':      'Rental Management',
    'manage':       'Rental Management',
    'management':   'Rental Management',
    'property management': 'Rental Management',
    'nri':          'NRI Assist',
    'nri assist':   'NRI Assist',
    'nri service':  'NRI Assist',
    'overseas':     'NRI Assist',
    'search':       'Property Search',
    'find':         'Property Search',
    'looking for':  'Property Search',
    'explore':      'Property Search',
    'plot':         'Land / Plot',
    'land':         'Land / Plot',
    'agricultural': 'Land / Plot',
    'farmland':     'Land / Plot',
    'site':         'Land / Plot',
}

# ── Property type keywords ────────────────────────────────────────────────────

PROPERTY_TYPE_KEYWORDS = {
    'apartment':        'Apartment',
    'flat':             'Apartment',
    'flats':            'Apartment',
    'apartments':       'Apartment',
    'villa':            'Villa',
    'villas':           'Villa',
    'bungalow':         'Villa',
    'plot':             'Plot',
    'plots':            'Plot',
    'land':             'Plot',
    'independent house': 'Independent House',
    'row house':        'Independent House',
    'duplex':           'Independent House',
    'commercial':       'Commercial',
    'office':           'Commercial',
    'shop':             'Commercial',
    'warehouse':        'Commercial',
    'penthouse':        'Penthouse',
    'studio':           'Apartment',
}

# ── Chennai area / preferred location keywords ────────────────────────────────

CHENNAI_LOCATION_KEYWORDS = [
    'anna nagar', 't.nagar', 't nagar', 'tnagar', 'adyar', 'omr', 'ecr',
    'velachery', 'porur', 'perambur', 'mylapore', 'triplicane', 'nungambakkam',
    'kilpauk', 'egmore', 'royapettah', 'alwarpet', 'boat club', 'poes garden',
    'kotturpuram', 'besant nagar', 'thiruvanmiyur', 'sholinganallur',
    'perungudi', 'taramani', 'medavakkam', 'pallikaranai', 'chromepet',
    'tambaram', 'pallavaram', 'guindy', 'saidapet', 'vadapalani',
    'koyambedu', 'ambattur', 'avadi', 'poonamallee', 'maduravoyal',
    'mogappair', 'kolathur', 'villivakkam', 'madhavaram', 'manali',
    'thiruvottiyur', 'ennore', 'tondiarpet', 'royapuram', 'washermanpet',
]

# ── Timeline keywords ─────────────────────────────────────────────────────────

TIMELINE_KEYWORDS = {
    'immediately':      'Immediately',
    'urgent':           'Immediately',
    'asap':             'Immediately',
    'as soon as possible': 'Immediately',
    'right away':       'Immediately',
    'right now':        'Immediately',
    '3 months':         'Within 3 months',
    'three months':     'Within 3 months',
    'quarter':          'Within 3 months',
    '6 months':         'Within 6 months',
    'six months':       'Within 6 months',
    'half year':        'Within 6 months',
    '1 year':           'Within a year',
    'one year':         'Within a year',
    'next year':        'Within a year',
    'this year':        'Within a year',
}

# ── Contact time keywords ─────────────────────────────────────────────────────

CONTACT_TIME_KEYWORDS = {
    'morning':   'Morning',
    'afternoon': 'Afternoon',
    'evening':   'Evening',
    'anytime':   'Anytime',
    'any time':  'Anytime',
    'weekend':   'Weekends',
    'weekday':   'Weekdays',
    'weekdays':  'Weekdays',
    'weekends':  'Weekends',
}
