"""
SEO Template Tags for Propertism
Provides structured data and meta tag generation
"""
from django import template
from django.conf import settings
import json
from content.site_context import get_company_info

register = template.Library()


def _get_company():
    return get_company_info()


def _make_absolute_url(url, site_url):
    if not url:
        return None
    if str(url).startswith("http"):
        return str(url)
    return f"{site_url}{url}"


def _get_public_site_url(request=None):
    canonical_scheme = getattr(settings, "CANONICAL_SCHEME", "https") or "https"
    canonical_host = getattr(settings, "CANONICAL_HOST", "") or ""

    if not canonical_host and request:
        canonical_host = request.get_host()
    if not canonical_host:
        canonical_host = "www.propertism.in"

    return f"{canonical_scheme}://{canonical_host}"


def _get_company_hero_url(company, site_url):
    hero_url = company.get_primary_hero_image_url() if company else None
    if hero_url:
        return _make_absolute_url(hero_url, site_url)
    return _make_absolute_url('/static/images/propertism-hero-bg.jpg', site_url)


@register.inclusion_tag('seo/meta_tags.html', takes_context=True)
def seo_meta(
    context,
    title=None,
    description=None,
    image=None,
    page_type='website',
    keywords=None,
    canonical_override=None,
):
    """
    Generate comprehensive SEO meta tags

    Usage:
        {% load seo_tags %}
        {% seo_meta title="Page Title" description="Page description" image="/path/to/image.jpg" %}
    """
    request = context.get('request')

    site_url = _get_public_site_url(request)
    if request:
        current_url = f"{site_url}{request.path}"
    else:
        current_url = site_url

    company = _get_company()
    default_title = "Propertism | Chennai Property Management for NRIs"
    default_description = "Expert NRI property management services in Chennai, India. Buy, sell, and manage your real estate investments with confidence. Professional rental management and property maintenance."
    default_image = _get_company_hero_url(company, site_url)

    social_title = "NRI Property Management Chennai | Propertism"
    social_description = (
        "Buy, sell, rent, and manage Chennai property from anywhere with trusted "
        "on-ground support."
    )
    og_image = _make_absolute_url('/static/images/og-propertism-v3.png', site_url)
    final_title = title or default_title
    final_description = description or default_description
    final_image = _make_absolute_url(image, site_url) if image else og_image
    final_canonical = _make_absolute_url(canonical_override or current_url, site_url)

    return {
        'title': final_title,
        'description': final_description,
        'keywords': keywords,
        'image': final_image,
        'url': current_url,
        'canonical_url': final_canonical,
        'social_title': social_title,
        'social_description': social_description,
        'site_url': site_url,
        'page_type': page_type,
        'site_name': company.company_name if company else 'Propertism Realty Advisors',
        'twitter_handle': '@PropertismIndia',
    }


@register.inclusion_tag('seo/structured_data.html', takes_context=True)
def organization_schema(context):
    """Generate Organization schema for RealEstateAgent"""
    request = context.get('request')
    site_url = f"{request.scheme}://{request.get_host()}" if request else ''
    company = _get_company()
    logo_url = (
        _make_absolute_url(company.logo.url, site_url)
        if company and company.logo
        else _make_absolute_url('/static/images/propertism-logo.png', site_url)
    )
    hero_url = _get_company_hero_url(company, site_url)

    schema = {
        "@context": "https://schema.org",
        "@type": "RealEstateAgent",
        "name": company.company_name,
        "description": company.tagline,
        "url": site_url,
        "logo": logo_url,
        "image": hero_url,
        "telephone": company.india_phone_1,
        "email": company.email,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": company.india_office_address.replace("\n", ", "),
            "addressLocality": company.india_office_city,
            "addressRegion": company.india_office_state,
            "postalCode": company.india_office_pincode,
            "addressCountry": "IN"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "13.0827",
            "longitude": "80.2707"
        },
        "areaServed": {
            "@type": "City",
            "name": "Chennai"
        },
        "sameAs": [
            url for url in [
                company.facebook_url,
                company.linkedin_url,
                company.twitter_url,
            ] if url
        ]
    }

    return {'schema': json.dumps(schema, indent=2)}


@register.inclusion_tag('seo/property_schema.html')
def property_schema(property_obj, request=None):
    """Generate Residence schema for property listing"""
    site_url = f"{request.scheme}://{request.get_host()}" if request else ''

    schema = {
        "@context": "https://schema.org",
        "@type": "Residence",
        "name": property_obj.title,
        "description": property_obj.description[:500] if property_obj.description else property_obj.title,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": property_obj.location,
            "addressRegion": "Tamil Nadu",
            "addressCountry": "IN"
        },
        "numberOfRooms": property_obj.bedrooms,
        "numberOfBathroomsTotal": property_obj.bathrooms,
        "floorSize": {
            "@type": "QuantitativeValue",
            "value": property_obj.area,
            "unitCode": "FTK"
        } if property_obj.area else None,
        "offers": {
            "@type": "Offer",
            "price": str(property_obj.price),
            "priceCurrency": getattr(property_obj, "currency", "INR"),
            "availability": "https://schema.org/InStock",
            "url": f"{site_url}{property_obj.get_absolute_url()}" if hasattr(property_obj, 'get_absolute_url') else site_url
        }
    }

    schema = {k: v for k, v in schema.items() if v is not None}
    return {'schema': json.dumps(schema, indent=2)}


@register.inclusion_tag('seo/breadcrumb_schema.html', takes_context=True)
def breadcrumb_schema(context, items):
    """
    Generate BreadcrumbList schema

    Usage:
        {% breadcrumb_schema items %}
        where items = [
            {'name': 'Home', 'url': '/'},
            {'name': 'Properties', 'url': '/properties/'},
            {'name': 'Villa', 'url': None}  # Current page, no URL
        ]
    """
    request = context.get('request')
    site_url = f"{request.scheme}://{request.get_host()}" if request else ''

    item_list = []
    for position, item in enumerate(items, start=1):
        list_item = {
            "@type": "ListItem",
            "position": position,
            "name": item['name']
        }
        if item.get('url'):
            list_item['item'] = f"{site_url}{item['url']}"
        item_list.append(list_item)

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": item_list
    }

    return {'schema': json.dumps(schema, indent=2)}


@register.inclusion_tag('seo/structured_data.html', takes_context=True)
def service_schema(context, config, city, page_url=None):
    """Generate service schema for service-led landing pages."""
    request = context.get('request')
    site_url = f"{request.scheme}://{request.get_host()}" if request else ''
    company = _get_company()
    url = _make_absolute_url(page_url, site_url) or site_url

    service_label = config.get("property_type_label") or config.get("h1") or "Property Service"
    description = config.get("description") or config.get("seo_content") or service_label
    provider_name = company.company_name if company else "Propertism Realty Advisors"
    telephone = company.india_phone_1 if company else ""
    email = company.email if company else ""
    locality = city.get("name", "Chennai") if city else "Chennai"
    region = city.get("state", "Tamil Nadu") if city else "Tamil Nadu"

    schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service_label,
        "serviceType": service_label,
        "description": description,
        "url": url,
        "areaServed": {
            "@type": "City",
            "name": locality,
        },
        "provider": {
            "@type": "LocalBusiness",
            "name": provider_name,
            "telephone": telephone,
            "email": email,
            "address": {
                "@type": "PostalAddress",
                "addressLocality": locality,
                "addressRegion": region,
                "addressCountry": "IN",
            },
        },
    }

    return {'schema': json.dumps(schema, indent=2)}


@register.inclusion_tag('seo/structured_data.html')
def faq_schema(items):
    """Generate FAQPage schema from visible FAQ items."""
    entity_items = []
    for item in items or []:
        question = item.get("question")
        answer = item.get("answer")
        if not question or not answer:
            continue
        entity_items.append(
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer,
                },
            }
        )

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entity_items,
    }
    return {'schema': json.dumps(schema, indent=2)}
