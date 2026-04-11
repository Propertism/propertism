"""
Dynamic SEO Landing Page Views
Intent-based property listing pages
"""
from django.shortcuts import render
from django.http import Http404
from properties.models import Property
from .intent_mapping import INTENT_MAP, CITIES, NRI_LOCATIONS, get_intent_config, resolve_geo_slug


def landing_page(request, city_slug, intent_slug, nri_origin=None):
    """
    Dynamic landing page for intent-based property searches
    URL: /{city}/{intent}/ OR /{nri_location}/{city}-{intent}/
    """
    # Validate city
    if city_slug not in CITIES:
        raise Http404("City not found")
    
    # Get intent configuration
    config = get_intent_config(intent_slug, city_slug)
    if not config:
        raise Http404("Intent not found")
    
    # NRI Geo-Targeting Enrichment
    nri_location = None
    if nri_origin:
        nri_location = NRI_LOCATIONS.get(nri_origin)

    # Apply filters to get properties
    filters = config['filters'].copy()
    properties = Property.objects.filter(**filters, status='available').order_by('-created_at')[:20]
    
    # Build breadcrumbs for SEO
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
    ]
    if nri_origin and nri_location:
        breadcrumbs.append({'name': f"NRIs in {nri_location['name']}", 'url': f'/{nri_origin}/'})
        
    breadcrumbs.append({'name': config['city']['name'], 'url': f'/{city_slug}/'})
    breadcrumbs.append({'name': config['h1'], 'url': None})
    
    # Contextual Related Intents
    related_slugs = config.get('related_intent_slugs', [])
    related_intents = []
    
    # First priority: Specified related slugs
    for slug in related_slugs:
        rel_config = get_intent_config(slug, city_slug)
        if rel_config:
            related_intents.append({'slug': slug, 'name': rel_config['h1']})
    
    # Fallback/Safety: fill to 5 if needed (excluding current)
    if len(related_intents) < 5:
        for slug, cfg in INTENT_MAP.items():
            if slug != intent_slug and slug not in related_slugs:
                if 'villa' in intent_slug and 'flat' in slug and len(related_intents) > 3:
                    continue
                related_intents.append({'slug': slug, 'name': cfg['h1'].format(city=config['city']['name'])})
                if len(related_intents) >= 6:
                    break

    context = {
        'config': config,
        'intent_title': config['property_type_label'] if 'property_type_label' in config else "Property",
        'properties': properties,
        'property_count': properties.count(),
        'property_type_name': config.get('property_type_label', 'Property'),
        'city': config['city'],
        'nri_location': nri_location,
        'nri_label': nri_location['label'] if nri_location else None,
        'breadcrumbs': breadcrumbs,
        'related_intents': related_intents[:6],
        'page_url': f'/{city_slug}/{intent_slug}/',
        'whatsapp_number': '+918667020798',
        'whatsapp_message': f"Hi, I'm interested in {config['h1']}. Please share deals.",
    }
    
    return render(request, 'landing_page.html', context)


def nri_landing_page(request, nri_location_slug, geo_slug):
    """
    Geo-targeted landing page for NRIs - Evaluated first to handle /nri/city-intent/
    """
    if nri_location_slug not in NRI_LOCATIONS:
        # FALLBACK: If not an NRI location, assume it's a domestic /city/intent/ pattern
        return landing_page(request, city_slug=nri_location_slug, intent_slug=geo_slug)
        
    city_slug, intent_slug = resolve_geo_slug(geo_slug)
    if not city_slug or not intent_slug:
        raise Http404("Indian Geo-intent not found")
        
    return landing_page(request, city_slug, intent_slug, nri_origin=nri_location_slug)


def city_hub(request, city_slug):
    """
    City hub page listing all intents
    URL: /{city}/
    Example: /chennai/
    """
    if city_slug not in CITIES:
        raise Http404("City not found")
    
    city = CITIES[city_slug]
    
    # All available intents for this city
    from .intent_mapping import get_all_intents
    intents = []
    for intent_slug in get_all_intents():
        config = get_intent_config(intent_slug, city_slug)
        intents.append({
            'slug': intent_slug,
            'title': config['h1'],
            'description': config['description'],
            'url': f'/{city_slug}/{intent_slug}/',
        })
    
    context = {
        'city': city,
        'city_slug': city_slug,
        'intents': intents,
        'page_title': f'Property in {city["name"]} | Real Estate Listings',
        'page_description': f'Find properties in {city["name"]}. Flats, villas, apartments for sale and rent. Expert NRI property management services.',
    }
    
    return render(request, 'city_hub.html', context)
