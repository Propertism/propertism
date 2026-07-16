from .models import CompanyInfo, ContactInquiry, CoreValue, ExpertiseArea, Service


HOME_SECTION_IDS = {
    "home": "home-section",
    "about": "about-section",
    "services": "services-section",
    "properties": "properties-section",
    "management": "management-section",
    "blog": "blog-section",
    "reviews": "reviews-section",
    "contact": "contact-section",
}


def get_home_section_links():
    """
    Navigation links for header.
    NOTE: 'contact' and 'blog' MUST remain as homepage anchors (#hash)
    because views.contact and views.blog redirect() to these links internally.
    Using their own /url/ would create an infinite redirect loop.
    """
    return {
        "home": "/",
        "about": "/about/",
        "services": "/services/",
        "properties": "/properties/",
        "management": "/management/",
        "blog": "/#blog-section",        # views.blog redirects here — DO NOT change to /blog/
        "reviews": "/#reviews-section",
        "contact": "/#contact-section",  # views.contact redirects here — DO NOT change to /contact/
    }


def get_hero_title_segments(title):
    normalized = " ".join(str(title or "").split())
    if not normalized:
        return []

    lower_val = normalized.lower()
    
    # Highlight "nri" (case-insensitive) if present
    target_phrase_nri = "nri"
    if target_phrase_nri in lower_val:
        idx = lower_val.find(target_phrase_nri)
        part1 = normalized[:idx]
        part2 = normalized[idx:idx + len(target_phrase_nri)]
        part3 = normalized[idx + len(target_phrase_nri):]
        segments = []
        if part1:
            segments.append({"text": part1, "accent": False})
        segments.append({"text": part2, "accent": True})
        if part3:
            segments.append({"text": part3, "accent": False})
        return segments

    # Highlight "chennai property" if present
    target_phrase = "chennai property"
    if target_phrase in lower_val:
        idx = lower_val.find(target_phrase)
        part1 = normalized[:idx]
        part2 = normalized[idx:idx + len(target_phrase)]
        part3 = normalized[idx + len(target_phrase):]
        segments = []
        if part1:
            segments.append({"text": part1, "accent": False})
        segments.append({"text": part2, "accent": True})
        if part3:
            segments.append({"text": part3, "accent": False})
        return segments

    return [{"text": normalized, "accent": False}]


def get_company_info():
    try:
        return CompanyInfo.objects.first() or CompanyInfo()
    except Exception:
        return CompanyInfo()


def get_active_services(limit=None):
    try:
        queryset = Service.objects.filter(is_active=True)
        if limit is not None:
            queryset = queryset[:limit]
        return list(queryset)
    except Exception:
        return []


def get_active_core_values(limit=None):
    try:
        queryset = CoreValue.objects.filter(is_active=True)
        if limit is not None:
            queryset = queryset[:limit]
        return list(queryset)
    except Exception:
        return []


def get_active_expertise_areas(limit=None):
    try:
        queryset = ExpertiseArea.objects.filter(is_active=True)
        if limit is not None:
            queryset = queryset[:limit]
        return list(queryset)
    except Exception:
        return []


def get_contact_service_choices():
    return ContactInquiry.SERVICE_CHOICES


def get_contact_property_choices():
    return ContactInquiry.PROPERTY_CHOICES


def get_contact_locality_choices():
    from content.locality_registry import ZONE_DISPLAY_NAMES, get_dropdown_grouped

    return [
        (ZONE_DISPLAY_NAMES.get(zone, zone.replace("-", " ").title()), choices)
        for zone, choices in get_dropdown_grouped().items()
        if choices
    ]
