import os
import sys
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")

import django
django.setup()

from properties.models import Inquiry

COUNTRY_MAP = [
    { "code": "+971", "name": "United Arab Emirates", "aliases": ["uae", "emirates", "dubai", "abu dhabi"] },
    { "code": "+966", "name": "Saudi Arabia", "aliases": ["ksa", "saudi"] },
    { "code": "+974", "name": "Qatar", "aliases": ["qatar", "doha"] },
    { "code": "+968", "name": "Oman", "aliases": ["oman", "muscat"] },
    { "code": "+965", "name": "Kuwait", "aliases": ["kuwait"] },
    { "code": "+973", "name": "Bahrain", "aliases": ["bahrain"] },
    { "code": "+852", "name": "Hong Kong", "aliases": ["hong kong", "hk"] },
    { "code": "+353", "name": "Ireland", "aliases": ["ireland", "dublin"] },
    { "code": "+351", "name": "Portugal", "aliases": ["portugal", "lisbon"] },
    { "code": "+880", "name": "Bangladesh", "aliases": ["bangladesh", "dhaka"] },
    { "code": "+977", "name": "Nepal", "aliases": ["nepal", "kathmandu"] },
    { "code": "+94", "name": "Sri Lanka", "aliases": ["sri lanka", "colombo"] },
    { "code": "+91", "name": "India", "aliases": ["india", "bharat", "ind"] },
    { "code": "+65", "name": "Singapore", "aliases": ["singapore", "sg"] },
    { "code": "+60", "name": "Malaysia", "aliases": ["malaysia", "my", "kl"] },
    { "code": "+61", "name": "Australia", "aliases": ["australia", "aus", "sydney", "melbourne"] },
    { "code": "+64", "name": "New Zealand", "aliases": ["new zealand", "nz", "auckland"] },
    { "code": "+48", "name": "Poland", "aliases": ["poland", "pl", "polska", "warsaw"] },
    { "code": "+44", "name": "United Kingdom", "aliases": ["uk", "united kingdom", "great britain", "england", "london", "scotland"] },
    { "code": "+49", "name": "Germany", "aliases": ["germany", "de", "deutschland", "berlin", "frankfurt", "munich"] },
    { "code": "+33", "name": "France", "aliases": ["france", "fr", "paris"] },
    { "code": "+39", "name": "Italy", "aliases": ["italy", "it", "italia", "rome", "milan"] },
    { "code": "+34", "name": "Spain", "aliases": ["spain", "es", "espana", "madrid", "barcelona"] },
    { "code": "+31", "name": "Netherlands", "aliases": ["netherlands", "nl", "holland", "amsterdam"] },
    { "code": "+41", "name": "Switzerland", "aliases": ["switzerland", "ch", "swiss", "zurich", "geneva"] },
    { "code": "+46", "name": "Sweden", "aliases": ["sweden", "se", "stockholm"] },
    { "code": "+47", "name": "Norway", "aliases": ["norway", "no", "oslo"] },
    { "code": "+45", "name": "Denmark", "aliases": ["denmark", "dk", "copenhagen"] },
    { "code": "+81", "name": "Japan", "aliases": ["japan", "jp", "tokyo"] },
    { "code": "+82", "name": "South Korea", "aliases": ["korea", "south korea", "kr", "seoul"] },
    { "code": "+86", "name": "China", "aliases": ["china", "cn", "beijing", "shanghai"] },
    { "code": "+62", "name": "Indonesia", "aliases": ["indonesia", "id", "jakarta"] },
    { "code": "+63", "name": "Philippines", "aliases": ["philippines", "ph", "manila"] },
    { "code": "+66", "name": "Thailand", "aliases": ["thailand", "th", "bangkok"] },
    { "code": "+84", "name": "Vietnam", "aliases": ["vietnam", "vn", "hanoi"] },
    { "code": "+27", "name": "South Africa", "aliases": ["south africa", "za"] },
    { "code": "+7", "name": "Russia", "aliases": ["russia", "ru", "moscow"] },
    { "code": "+1", "name": "United States", "aliases": ["usa", "us", "united states", "america", "canada", "ca"] }
]

def determine_country(message, phone):
    msg = (message or "").lower()
    ph = (phone or "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    # 1. From message: Country of Residence: Poland (+48)
    country_match = re.search(r'(?:country of residence|country)\s*:\s*([^\n\r]+)', msg, re.IGNORECASE)
    if country_match:
        c_text = country_match.group(1).strip().lower()
        code_match = re.search(r'\+([0-9]{1,4})', c_text)
        if code_match:
            target_code = "+" + code_match.group(1)
            for c in COUNTRY_MAP:
                if c["code"] == target_code:
                    return c["code"], c["name"]
        for c in COUNTRY_MAP:
            if re.search(r'\b' + re.escape(c["name"].lower()) + r'\b', c_text):
                return c["code"], c["name"]
            for alias in c["aliases"]:
                if len(alias) > 2 and alias in c_text:
                    return c["code"], c["name"]
                elif len(alias) <= 2 and re.search(r'\b' + re.escape(alias) + r'\b', c_text):
                    return c["code"], c["name"]

    # 2. From phone starting with +
    if ph.startswith("+"):
        for c in COUNTRY_MAP:
            if ph.startswith(c["code"]):
                return c["code"], c["name"]

    # 3. Standard 10-digit Indian Mobile
    if len(ph) == 10 and ph[0] in "6789":
        return "+91", "India"
    if len(ph) == 10:
        return "+91", "India"
    if ph.startswith("91") and len(ph) == 12:
        return "+91", "India"
    if ph.startswith("0") and len(ph) == 11:
        return "+91", "India"

    # 4. International without +
    for c in COUNTRY_MAP:
        raw_c = c["code"].replace("+", "")
        if ph.startswith(raw_c) and len(ph) > len(raw_c) + 6:
            return c["code"], c["name"]

    # 5. Default fallback
    return "+91", "India"

updated_count = 0
total_inquiries = Inquiry.objects.count()
print(f"Starting country backfill for {total_inquiries} inquiries...")

for inq in Inquiry.objects.all():
    code, name = determine_country(inq.message, inq.phone)
    inq.country_code = code
    inq.country_name = name
    Inquiry.objects.filter(pk=inq.pk).update(country_code=code, country_name=name)
    updated_count += 1
    print(f"#{inq.id}: {inq.name} -> {name} ({code}) [Phone: {inq.phone}]")

print(f"\nSuccessfully backfilled {updated_count} / {total_inquiries} inquiries.")
