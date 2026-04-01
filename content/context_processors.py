from .site_context import get_active_services, get_company_info, get_home_section_links


def site_content(request):
    footer_services = get_active_services(limit=4)
    return {
        "company": get_company_info(),
        "footer_services": footer_services,
        "home_section_links": get_home_section_links(),
    }
