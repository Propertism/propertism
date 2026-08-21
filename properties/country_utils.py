import re

COUNTRY_DIRECTORY = [
    { "code": "+971", "name": "United Arab Emirates", "flag": "🇦🇪", "aliases": ["uae", "emirates", "dubai", "abu dhabi"] },
    { "code": "+966", "name": "Saudi Arabia", "flag": "🇸🇦", "aliases": ["ksa", "saudi"] },
    { "code": "+974", "name": "Qatar", "flag": "🇶🇦", "aliases": ["qatar", "doha"] },
    { "code": "+968", "name": "Oman", "flag": "🇴🇲", "aliases": ["oman", "muscat"] },
    { "code": "+965", "name": "Kuwait", "flag": "🇰🇼", "aliases": ["kuwait"] },
    { "code": "+973", "name": "Bahrain", "flag": "🇧🇭", "aliases": ["bahrain"] },
    { "code": "+852", "name": "Hong Kong", "flag": "🇭🇰", "aliases": ["hong kong", "hk"] },
    { "code": "+353", "name": "Ireland", "flag": "🇮🇪", "aliases": ["ireland", "dublin"] },
    { "code": "+351", "name": "Portugal", "flag": "🇵🇹", "aliases": ["portugal", "lisbon"] },
    { "code": "+880", "name": "Bangladesh", "flag": "🇧🇩", "aliases": ["bangladesh", "dhaka"] },
    { "code": "+977", "name": "Nepal", "flag": "🇳🇵", "aliases": ["nepal", "kathmandu"] },
    { "code": "+94", "name": "Sri Lanka", "flag": "🇱🇰", "aliases": ["sri lanka", "colombo"] },
    { "code": "+91", "name": "India", "flag": "🇮🇳", "aliases": ["india", "bharat", "ind"] },
    { "code": "+65", "name": "Singapore", "flag": "🇸🇬", "aliases": ["singapore", "sg"] },
    { "code": "+60", "name": "Malaysia", "flag": "🇲🇾", "aliases": ["malaysia", "my", "kl"] },
    { "code": "+61", "name": "Australia", "flag": "🇦🇺", "aliases": ["australia", "aus", "sydney", "melbourne"] },
    { "code": "+64", "name": "New Zealand", "flag": "🇳🇿", "aliases": ["new zealand", "nz", "auckland"] },
    { "code": "+48", "name": "Poland", "flag": "🇵🇱", "aliases": ["poland", "pl", "polska", "warsaw"] },
    { "code": "+44", "name": "United Kingdom", "flag": "🇬🇧", "aliases": ["uk", "united kingdom", "great britain", "england", "london", "scotland"] },
    { "code": "+49", "name": "Germany", "flag": "🇩🇪", "aliases": ["germany", "de", "deutschland", "berlin", "frankfurt", "munich"] },
    { "code": "+33", "name": "France", "flag": "🇫🇷", "aliases": ["france", "fr", "paris"] },
    { "code": "+39", "name": "Italy", "flag": "🇮🇹", "aliases": ["italy", "it", "italia", "rome", "milan"] },
    { "code": "+34", "name": "Spain", "flag": "🇪🇸", "aliases": ["spain", "es", "espana", "madrid", "barcelona"] },
    { "code": "+31", "name": "Netherlands", "flag": "🇳🇱", "aliases": ["netherlands", "nl", "holland", "amsterdam"] },
    { "code": "+41", "name": "Switzerland", "flag": "🇨🇭", "aliases": ["switzerland", "ch", "swiss", "zurich", "geneva"] },
    { "code": "+46", "name": "Sweden", "flag": "🇸🇪", "aliases": ["sweden", "se", "stockholm"] },
    { "code": "+47", "name": "Norway", "flag": "🇳🇴", "aliases": ["norway", "no", "oslo"] },
    { "code": "+45", "name": "Denmark", "flag": "🇩🇰", "aliases": ["denmark", "dk", "copenhagen"] },
    { "code": "+81", "name": "Japan", "flag": "🇯🇵", "aliases": ["japan", "jp", "tokyo"] },
    { "code": "+82", "name": "South Korea", "flag": "🇰🇷", "aliases": ["korea", "south korea", "kr", "seoul"] },
    { "code": "+86", "name": "China", "flag": "🇨🇳", "aliases": ["china", "cn", "beijing", "shanghai"] },
    { "code": "+62", "name": "Indonesia", "flag": "🇮🇩", "aliases": ["indonesia", "id", "jakarta"] },
    { "code": "+63", "name": "Philippines", "flag": "🇵🇭", "aliases": ["philippines", "ph", "manila"] },
    { "code": "+66", "name": "Thailand", "flag": "🇹🇭", "aliases": ["thailand", "th", "bangkok"] },
    { "code": "+84", "name": "Vietnam", "flag": "🇻🇳", "aliases": ["vietnam", "vn", "hanoi"] },
    { "code": "+27", "name": "South Africa", "flag": "🇿🇦", "aliases": ["south africa", "za"] },
    { "code": "+7", "name": "Russia", "flag": "🇷🇺", "aliases": ["russia", "ru", "moscow"] },
    { "code": "+1", "name": "United States", "flag": "🇺🇸", "aliases": ["usa", "us", "united states", "america", "canada", "ca"] }
]


def resolve_country_from_intake(message="", phone="", raw_country_code=""):
    """
    Extracts canonical country_code (e.g. '+91') and country_name (e.g. 'India')
    from form inputs, intake message headers, or phone strings.
    """
    # 1. Direct country code from form field if provided
    if raw_country_code:
        raw_clean = str(raw_country_code).strip()
        if not raw_clean.startswith("+") and raw_clean.isdigit():
            raw_clean = "+" + raw_clean
        for c in COUNTRY_DIRECTORY:
            if c["code"] == raw_clean:
                return c["code"], c["name"]

    msg = (message or "").lower()
    ph = (phone or "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    # 2. From message header: Country of Residence: Poland (+48)
    country_match = re.search(r'(?:country of residence|country)\s*:\s*([^\n\r]+)', msg, re.IGNORECASE)
    if country_match:
        c_text = country_match.group(1).strip().lower()
        code_match = re.search(r'\+([0-9]{1,4})', c_text)
        if code_match:
            target_code = "+" + code_match.group(1)
            for c in COUNTRY_DIRECTORY:
                if c["code"] == target_code:
                    return c["code"], c["name"]
        for c in COUNTRY_DIRECTORY:
            if re.search(r'\b' + re.escape(c["name"].lower()) + r'\b', c_text):
                return c["code"], c["name"]
            for alias in c["aliases"]:
                if len(alias) > 2 and alias in c_text:
                    return c["code"], c["name"]
                elif len(alias) <= 2 and re.search(r'\b' + re.escape(alias) + r'\b', c_text):
                    return c["code"], c["name"]

    # 3. Explicit + prefix in phone
    if ph.startswith("+"):
        for c in COUNTRY_DIRECTORY:
            if ph.startswith(c["code"]):
                return c["code"], c["name"]

    # 4. Standard 10-digit Indian Mobile
    if len(ph) == 10:
        return "+91", "India"
    if ph.startswith("91") and len(ph) == 12:
        return "+91", "India"
    if ph.startswith("0") and len(ph) == 11:
        return "+91", "India"

    # 5. International without +
    for c in COUNTRY_DIRECTORY:
        raw_c = c["code"].replace("+", "")
        if ph.startswith(raw_c) and len(ph) > len(raw_c) + 6:
            return c["code"], c["name"]

    return "+91", "India"
