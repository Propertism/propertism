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

    if normalized.lower() == "nri property management services in chennai, india":
        return [
            {"text": "NRI Property", "accent": False},
            {"text": "Management", "accent": False},
            {"text": "Services", "accent": True},
            {"text": "In Chennai, India", "accent": False},
        ]

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
