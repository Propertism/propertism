"""
SEO Template Tags for Propertism
Provides structured data and meta tag generation
"""
from django import template
from django.conf import settings
from django.urls import reverse
import json

register = template.Library()

@register.inclusion_tag('seo/meta_tags.html', takes_context=True)
def seo_meta(context, title=None, description=None, image=None, page_type='website'):
    """
    Generate comprehensive SEO meta tags
    
    Usage:
        {% load seo_tags %}
        {% seo_meta title="Page Title" description="Page description" image="/path/to/image.jpg" %}
    """
    request = context.get('request')
    
    # Build absolute URL
    if request:
        current_url = request.build_absolute_uri()
        site_url = f"{request.scheme}://{request.get_host()}"
    else:
        current_url = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
        site_url = current_url
    
    # Default values
    default_title = "Propertism Realty Advisors | NRI Property Management Chennai"
    default_description = "Expert NRI property management services in Chennai, India. Buy, sell, and manage your real estate investments with confidence. Professional rental management and property maintenance."
    default_image = f"{site_url}/static/images/propertism-hero-bg.jpg"
    
    # Use provided values or defaults
    final_title = title or default_title
    final_description = description or default_description
    final_image = image or default_image
    
    # Make image absolute URL if relative
    if final_image and not final_image.startswith('http'):
        final_image = f"{site_url}{final_image}"
    
    return {
        'title': final_title,
        'description': final_description,
        'image': final_image,
        'url': current_url,
        'site_url': site_url,
        'page_type': page_type,
        'site_name': 'Propertism Realty Advisors',
        'twitter_handle': '@propertism',
    }


@register.inclusion_tag('seo/structured_data.html', takes_context=True)
def organization_schema(context):
    """Generate Organization schema for RealEstateAgent"""
    request = context.get('request')
    site_url = f"{request.scheme}://{request.get_host()}" if request else ''
    
    schema = {
        "@context": "https://schema.org",
        "@type": "RealEstateAgent",
        "name": "Propertism Realty Advisors LLP",
        "description": "Professional NRI property management and real estate services in Chennai, India",
        "url": site_url,
        "logo": f"{site_url}/static/images/propertism-logo.png",
        "image": f"{site_url}/static/images/propertism-hero-bg.jpg",
        "telephone": "+91 86670 20798",
        "email": "info@propertism.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "No. 30, 3rd Floor, SSR Pankajam Towers, Arunachalam Road, Saligramam",
            "addressLocality": "Chennai",
            "addressRegion": "Tamil Nadu",
            "postalCode": "600093",
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
            "https://www.facebook.com/propertism",
            "https://www.linkedin.com/company/propertism",
            "https://twitter.com/propertism"
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
            "priceCurrency": "INR",
            "availability": "https://schema.org/InStock",
            "url": f"{site_url}{property_obj.get_absolute_url()}" if hasattr(property_obj, 'get_absolute_url') else site_url
        }
    }
    
    # Remove None values
    schema = {k: v for k, v in schema.items() if v is not None}
    if schema.get('floorSize') is None:
        del schema['floorSize']
    
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
