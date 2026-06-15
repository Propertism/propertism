"""
Dynamic SEO landing page views.
Intent-based property listing pages with NRI-aware context.
"""
from django.http import Http404
from django.shortcuts import render

from .models import CustomerReviewSection, LandingLead
from properties.models import Property

from .intent_mapping import (
    CITIES,
    NRI_LOCATIONS,
    get_all_intents,
    get_intent_config,
    resolve_geo_slug,
)
from .pseo_enrichment import build_enrichment_context


def build_page_path(city_slug, intent_slug, nri_origin=None):
    """Build the public landing-page path for the current routing model."""
    if nri_origin:
        return f"/{nri_origin}/{city_slug}-{intent_slug}/"
    return f"/{city_slug}/{intent_slug}/"


def build_hero_copy(config, city, nri_location=None):
    """Return intent-aware hero heading and subtitle."""
    intent_type = config.get("intent_type")
    city_name = city["name"]

    if nri_location:
        geo_name = nri_location["name"]
        geo_label = nri_location["label"]
        if intent_type == "sell":
            return (
                f"Sell Your Property in {city_name} from {geo_name}",
                f"For NRIs in {geo_label} owning property in {city_name}, we handle pricing strategy, buyer coordination, legal documentation, and power of attorney workflows without repeated travel.",
            )
        if intent_type == "management":
            return (
                f"Manage Your Property in {city_name} from {geo_name}",
                f"For NRIs in {geo_label}, we provide on-ground property supervision, tenant coordination, inspections, and reporting in {city_name}.",
            )
        if intent_type == "rental":
            return (
                f"Rent Out Your Property in {city_name} from {geo_name}",
                f"For NRIs in {geo_label}, we manage tenant sourcing, rental documentation, rent collection, and renewals in {city_name}.",
            )
        if intent_type == "maintenance":
            return (
                f"Maintain Your Property in {city_name} from {geo_name}",
                f"For NRIs in {geo_label}, we coordinate inspections, repairs, preventive upkeep, and verified local execution in {city_name}.",
            )
        if intent_type == "informational":
            return (
                f"How to Manage Property in {city_name} from {geo_name}",
                f"For NRIs in {geo_label}, this page explains how to solve maintenance, tenant, and selling problems in {city_name} while living abroad.",
            )
        return (
            f"{config['h1']} for NRIs in {geo_name}",
            f"For NRIs in {geo_label}, {config['intro']}",
        )

    if intent_type == "sell":
        return (
            config["h1"],
            "Sell from abroad with pricing support, buyer handling, legal coordination, and a clear local execution partner.",
        )
    if intent_type == "management":
        return (
            config["h1"],
            "Remote property operations for overseas owners, including tenants, inspections, maintenance, and reporting.",
        )
    if intent_type == "rental":
        return (
            config["h1"],
            "Professional tenant sourcing, rent collection, renewals, and rental coordination for overseas owners.",
        )
    if intent_type == "maintenance":
        return (
            config["h1"],
            "Property care that protects asset value through inspections, repairs, vendor oversight, and preventive upkeep.",
        )
    return config["h1"], config["intro"]


def build_secondary_cta(config, city):
    """Return a natural secondary CTA label for the landing page."""
    intent_type = config.get("intent_type")
    city_name = city["name"]
    if intent_type == "sell":
        return f"View sale-ready listings in {city_name}"
    if intent_type in {"management", "rental", "maintenance", "informational"}:
        return f"Browse properties in {city_name}"
    return f"Explore {config.get('property_type_label', 'Property')}s in {city_name}"


def build_lead_capture_context(config, city, nri_location=None):
    """Return lead-form copy and CTA labels for the current intent."""
    intent_type = config.get("intent_type")
    city_name = city["name"]

    primary_label = config.get("cta", "Talk to NRI Property Expert")
    hero_secondary_label = build_secondary_cta(config, city)
    hero_secondary_mode = "anchor"
    lead_form_title = "Talk to Propertism"
    lead_form_intro = f"Share a few details about your property in {city_name} and our team will get back to you."

    if intent_type in {"sell", "management", "rental"}:
        primary_label = "Get Property Valuation"
        lead_form_title = "Get Property Valuation"

    if intent_type == "sell":
        lead_form_intro = (
            f"Share your property details and selling timeline for {city_name}. "
            "We will review the opportunity and contact you with the right next steps."
        )
    elif intent_type == "management":
        hero_secondary_label = "Manage My Property"
        hero_secondary_mode = "lead_form"
        lead_form_intro = (
            f"Tell us whether your {city_name} property is occupied or vacant and we will suggest the right management setup."
        )
    elif intent_type == "rental":
        hero_secondary_label = "Find Tenant"
        hero_secondary_mode = "lead_form"
        lead_form_intro = (
            f"Share your rental expectations for {city_name} and we will help you assess demand, rent, and tenant-readiness."
        )

    if nri_location:
        lead_form_intro = f"For NRIs in {nri_location['label']}, {lead_form_intro}"

    return {
        "primary_label": primary_label,
        "hero_secondary_label": hero_secondary_label,
        "hero_secondary_mode": hero_secondary_mode,
        "lead_form_title": lead_form_title,
        "lead_form_intro": lead_form_intro,
    }


def build_sell_process_steps(city):
    """Return the sell-page process steps."""
    city_name = city["name"]
    return [
        {
            "title": "Property Review",
            "description": f"We assess your {city_name} property position, documents, and likely sale path before marketing starts.",
        },
        {
            "title": "Pricing and Market Prep",
            "description": "We define a practical price band, buyer pitch, and on-ground readiness to improve enquiry quality.",
        },
        {
            "title": "Buyer Handling",
            "description": "We coordinate calls, visits, negotiation progress, and buyer seriousness so you are not chasing the process remotely.",
        },
        {
            "title": "Documentation and Closure",
            "description": "We support legal coordination, power of attorney workflows, and closure planning through final handover.",
        },
    ]


def build_sell_faq_items(city, nri_location=None):
    """Return visible FAQ items for sell pages."""
    city_name = city["name"]
    geo_name = nri_location["name"] if nri_location else "abroad"
    items = [
        {
            "question": f"Can I sell property in {city_name} without visiting India?",
            "answer": f"Yes. Many NRIs sell property in {city_name} through a managed local process that includes buyer coordination, documentation handling, and power of attorney support where appropriate.",
        },
        {
            "question": f"How does NRI property sale support work in {city_name}?",
            "answer": "The process usually includes valuation, marketing, buyer screening, negotiation support, document review, legal coordination, and closing assistance handled by a local execution partner.",
        },
        {
            "question": "What documents are usually needed for an NRI property sale?",
            "answer": "The exact set depends on the asset and ownership history, but owners generally need title documents, identity records, tax-related paperwork, and any sale-related authorization documents such as a power of attorney if applicable.",
        },
    ]
    if nri_location:
        items.append(
            {
                "question": f"How do I sell property in {city_name} from {geo_name}?",
                "answer": f"For owners based in {geo_name}, the safest route is a process with local buyer handling, documented updates, legal coordination, and closure planning so repeated travel is not required.",
            }
        )
    return items


def get_sell_reviews(limit=2):
    """Return a small set of active customer reviews for sell pages."""
    try:
        section = CustomerReviewSection.objects.filter(is_active=True).first()
        if not section:
            return []
        return list(section.reviews.filter(is_active=True).order_by("order")[:limit])
    except Exception:
        return []


def landing_page(request, city_slug, intent_slug, nri_origin=None):
    """
    Dynamic landing page for intent-based property searches.
    URL: /{city}/{intent}/ or /{nri_location}/{city}-{intent}/
    """
    if city_slug not in CITIES:
        raise Http404("City not found")

    config = get_intent_config(intent_slug, city_slug)
    if not config:
        raise Http404("Intent not found")

    city = config["city"]
    nri_location = NRI_LOCATIONS.get(nri_origin) if nri_origin else None
    page_path = build_page_path(city_slug, config["canonical_intent_slug"], nri_origin=nri_origin)

    filters = config["filters"].copy()
    properties = Property.objects.filter(**filters, status="available").order_by("-created_at")[:20]

    breadcrumbs = [{"name": "Home", "url": "/"}]
    if nri_origin and nri_location:
        breadcrumbs.append(
            {
                "name": f"NRIs in {nri_location['name']}",
                "url": f"/{nri_origin}/",
            }
        )
    breadcrumbs.append({"name": city["name"], "url": f"/{city_slug}/"})
    breadcrumbs.append({"name": config["h1"], "url": None})

    related_slugs = config.get("related_intent_slugs", [])
    related_intents = []

    for slug in related_slugs:
        rel_config = get_intent_config(slug, city_slug)
        if rel_config:
            related_intents.append(
                {
                    "slug": slug,
                    "name": rel_config["h1"],
                    "priority": rel_config.get("priority", 0),
                    "url": build_page_path(
                        city_slug,
                        rel_config["canonical_intent_slug"],
                        nri_origin=nri_origin if config["is_nri"] else None,
                    ),
                }
            )

    if len(related_intents) < 5:
        for slug in get_all_intents():
            if slug == config["canonical_intent_slug"] or slug in related_slugs:
                continue
            fallback_config = get_intent_config(slug, city_slug)
            if not fallback_config:
                continue
            if "villa" in intent_slug and "flat" in slug and len(related_intents) > 3:
                continue
            related_intents.append(
                {
                    "slug": slug,
                    "name": fallback_config["h1"],
                    "priority": fallback_config.get("priority", 0),
                    "url": build_page_path(
                        city_slug,
                        fallback_config["canonical_intent_slug"],
                        nri_origin=nri_origin if config["is_nri"] else None,
                    ),
                }
            )
            if len(related_intents) >= 6:
                break

    related_intents.sort(key=lambda item: item.get("priority", 0), reverse=True)
    hero_title, hero_subtitle = build_hero_copy(config, city, nri_location=nri_location)
    lead_capture = build_lead_capture_context(config, city, nri_location=nri_location)
    faq_items = build_sell_faq_items(city, nri_location=nri_location) if config.get("intent_type") == "sell" else []
    sell_process_steps = build_sell_process_steps(city) if config.get("intent_type") == "sell" else []
    sell_reviews = get_sell_reviews() if config.get("intent_type") == "sell" else []

    # Enrichment engine: differentiated H1, FAQs, trust block, knowledge hub links
    enrichment = build_enrichment_context(config, city, nri_location=nri_location)

    # Use differentiated H1 as hero_title; fall back to build_hero_copy subtitle
    _, hero_subtitle = build_hero_copy(config, city, nri_location=nri_location)
    hero_title = enrichment["differentiated_h1"]

    # Merge enriched FAQs: sell pages keep their existing FAQs + get enriched ones;
    # all other intents use enriched FAQs only.
    if config.get("intent_type") == "sell":
        faq_items = build_sell_faq_items(city, nri_location=nri_location)
    else:
        faq_items = enrichment["enriched_faq_items"]

    lead_capture = build_lead_capture_context(config, city, nri_location=nri_location)
    sell_process_steps = build_sell_process_steps(city) if config.get("intent_type") == "sell" else []
    sell_reviews = get_sell_reviews() if config.get("intent_type") == "sell" else []

    # Word count: config prose + enrichment content (FAQs + trust block)
    _prose = " ".join(filter(None, [
        config.get("intro", ""),
        config.get("seo_content", ""),
        config.get("description", ""),
    ]))
    _pseo_word_count = len(_prose.split()) + enrichment["enrichment_word_count"]

    context = {
        "config": config,
        "intent_title": config.get("property_type_label", "Property"),
        "page_title": enrichment["page_title"],
        "page_description": enrichment["page_description"],
        "_pseo_word_count": _pseo_word_count,
        "properties": properties,
        "property_count": len(properties),
        "property_type_name": config.get("property_type_label", "Property"),
        "city": city,
        "nri_origin": nri_origin,
        "nri_location": nri_location,
        "nri_label": nri_location["label"] if nri_location else None,
        "breadcrumbs": breadcrumbs,
        "related_intents": related_intents[:6],
        "page_url": page_path,
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
        "primary_cta_label": lead_capture["primary_label"],
        "secondary_cta_label": lead_capture["hero_secondary_label"],
        "secondary_cta_mode": lead_capture["hero_secondary_mode"],
        "lead_form_title": lead_capture["lead_form_title"],
        "lead_form_intro": lead_capture["lead_form_intro"],
        "lead_property_type_choices": LandingLead.PROPERTY_CHOICES,
        "faq_items": faq_items,
        "sell_process_steps": sell_process_steps,
        "sell_reviews": sell_reviews,
        "trust_points": enrichment["trust_points"],
        "knowledge_hub_links": enrichment["knowledge_hub_links"],
        "whatsapp_number": "+918667020798",
        "whatsapp_message": f"Hi, I'm interested in {hero_title}. Please share details.",
    }

    return render(request, "landing_page.html", context)


def nri_landing_page(request, nri_location_slug, geo_slug):
    """
    Geo-targeted landing page for NRIs.
    """
    if nri_location_slug not in NRI_LOCATIONS:
        return landing_page(request, city_slug=nri_location_slug, intent_slug=geo_slug)

    city_slug, intent_slug = resolve_geo_slug(geo_slug)
    if not city_slug or not intent_slug:
        raise Http404("Indian geo-intent not found")

    return landing_page(request, city_slug, intent_slug, nri_origin=nri_location_slug)


def city_hub(request, city_slug):
    """
    City hub page listing all intents.
    URL: /{city}/
    """
    if city_slug not in CITIES:
        raise Http404("City not found")

    city = CITIES[city_slug]
    intents = []
    for intent_slug in get_all_intents():
        config = get_intent_config(intent_slug, city_slug)
        intents.append(
            {
                "slug": intent_slug,
                "title": config["h1"],
                "description": config["description"],
                "url": f"/{city_slug}/{config['canonical_intent_slug']}/",
                "priority": config.get("priority", 0),
                "intent_type": config.get("intent_type", "buy"),
                "category": config.get("category", "buy"),
            }
        )
    intents.sort(key=lambda item: item["priority"], reverse=True)

    featured_service_intents = [
        intent
        for intent in intents
        if intent["intent_type"] in {"sell", "management", "rental"}
    ][:3]
    service_cluster_intents = [
        intent
        for intent in intents
        if intent["intent_type"] in {"sell", "management", "rental", "maintenance", "informational"}
        and intent not in featured_service_intents
    ]
    supporting_intents = [
        intent
        for intent in intents
        if intent["intent_type"] == "buy"
    ]

    context = {
        "city": city,
        "city_slug": city_slug,
        "intents": intents,
        "featured_service_intents": featured_service_intents,
        "service_cluster_intents": service_cluster_intents,
        "supporting_intents": supporting_intents,
        "page_title": f"NRI Property Services in {city['name']} | Sell, Manage, Rent, Maintain",
        "page_description": f"Explore Propertism's NRI property services in {city['name']}. Sell from abroad, manage rentals, handle maintenance, and solve ownership issues with one local execution partner.",
    }
    return render(request, "city_hub.html", context)
