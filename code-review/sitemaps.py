"""
Sitemap configuration for Propertism.
Generates dynamic sitemap.xml for search engines.
"""
from types import SimpleNamespace

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from properties.models import Property

from .intent_mapping import CITIES, NRI_LOCATIONS, get_all_intents, get_intent_config
from .models import BlogPost


class BaseSitemap(Sitemap):
    """Base sitemap that uses the canonical public host and scheme."""

    def get_urls(self, page=1, site=None, protocol=None):
        canonical_host = getattr(settings, "CANONICAL_HOST", "www.propertism.in")
        canonical_scheme = getattr(settings, "CANONICAL_SCHEME", "https")
        canonical_site = SimpleNamespace(domain=canonical_host)
        return super().get_urls(page=page, site=canonical_site, protocol=canonical_scheme)


class StaticViewSitemap(BaseSitemap):
    """Sitemap for static pages."""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "services",
            "about",
            "management",
            "property_owner_resources",
            "property_list",
            "terms",
            "privacy",
            "disclaimer",
            "sitemap_guide",
        ]

    def location(self, item):
        return reverse(item)


class PropertySitemap(BaseSitemap):
    """Sitemap for property listings."""

    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Property.objects.filter(status="available")

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, "updated_at") else None

    def location(self, obj):
        return f"/properties/{obj.slug}/"


class BlogSitemap(BaseSitemap):
    """Sitemap for blog posts."""

    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj):
        return f"/blog/{obj.slug}/"


class LandingPageSitemap(BaseSitemap):
    """Sitemap for landing pages with sell-first weighting."""

    changefreq = "daily"

    def priority(self, obj):
        if obj["kind"] == "hub":
            return 0.85

        config = get_intent_config(obj["intent"], obj["city"])
        if not config:
            return 0.7

        base_priority = 0.7
        if obj.get("nri"):
            base_priority = 0.82

        intent_type = config.get("intent_type")
        if intent_type == "sell":
            base_priority += 0.18
        elif intent_type == "management":
            base_priority += 0.14
        elif intent_type == "rental":
            base_priority += 0.12
        elif intent_type == "maintenance":
            base_priority += 0.08
        elif intent_type == "informational":
            base_priority += 0.05
        else:
            base_priority += 0.02

        return min(base_priority, 1.0)

    def items(self):
        """Generate all city, intent, and NRI combinations."""
        pages = []

        for city_slug in CITIES.keys():
            pages.append({"kind": "hub", "city": city_slug, "intent": None, "nri": None})
            for intent_slug in get_all_intents():
                pages.append({"kind": "landing", "city": city_slug, "intent": intent_slug, "nri": None})
                for nri_slug in NRI_LOCATIONS.keys():
                    pages.append({"kind": "landing", "city": city_slug, "intent": intent_slug, "nri": nri_slug})

        return pages

    def location(self, obj):
        if obj["kind"] == "hub":
            return f"/{obj['city']}/"
        if obj["nri"]:
            return f"/{obj['nri']}/{obj['city']}-{obj['intent']}/"
        return f"/{obj['city']}/{obj['intent']}/"
