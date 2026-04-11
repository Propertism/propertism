"""
Sitemap configuration for Propertism
Generates dynamic sitemap.xml for search engines
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost
from properties.models import Property
from .intent_mapping import get_all_intents, CITIES


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return ['home', 'services', 'about', 'management', 'contact', 'property_list']
    
    def location(self, item):
        return reverse(item)


class PropertySitemap(Sitemap):
    """Sitemap for property listings"""
    changefreq = 'daily'
    priority = 0.9
    
    def items(self):
        return Property.objects.filter(status='available')
    
    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None
    
    def location(self, obj):
        return f'/properties/{obj.pk}/'


class BlogSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = 'weekly'
    priority = 0.7
    
    def items(self):
        return BlogPost.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.updated_date
    
    def location(self, obj):
        return f'/blog/{obj.slug}/'


class LandingPageSitemap(Sitemap):
    """Sitemap for SEO landing pages (Domestic + NRI Geo)"""
    changefreq = 'daily'

    # Phase 1 — HIGH ROI NRI FUNNELS
    HIGH_ROI_PAGES = [
        ('new-york-usa', 'chennai', 'nri-property-management'),
        ('dubai-uae', 'chennai', 'nri-property-management'),
        ('london-uk', 'chennai', 'nri-property-management'),
        ('singapore', 'chennai', 'nri-property-management'),
        ('new-york-usa', 'chennai', 'nri-buy-villas'),
        ('dubai-uae', 'chennai', 'nri-buy-flats'),
        ('london-uk', 'chennai', 'nri-investment-properties'),
        ('san-jose-ca', 'bangalore', 'nri-investment-properties'),
        ('dallas-tx', 'hyderabad', 'nri-buy-villas'),
        ('doha-qatar', 'chennai', 'property-maintenance-for-nri'),
    ]

    def priority(self, obj):
        """Tiered Priority: High ROI (1.0) > NRI (0.9) > Domestic (0.7)"""
        if (obj.get('nri'), obj.get('city'), obj.get('intent')) in self.HIGH_ROI_PAGES:
            return 1.0
        return 0.9 if obj.get('nri') else 0.7
    
    def items(self):
        """Generate all city + intent + NRI combinations"""
        from .intent_mapping import NRI_LOCATIONS
        pages = []
        
        # 1. Domestic Pages (/city/intent/)
        for city_slug in CITIES.keys():
            # City hub
            pages.append({'city': city_slug, 'intent': None, 'nri': None})
            # City + Intent
            for intent_slug in get_all_intents():
                pages.append({'city': city_slug, 'intent': intent_slug, 'nri': None})
                
                # 2. NRI Geo Pages (/nri-location/city-intent/)
                for nri_slug in NRI_LOCATIONS.keys():
                    pages.append({'city': city_slug, 'intent': intent_slug, 'nri': nri_slug})
                    
        return pages
    
    def location(self, obj):
        if obj['nri']:
            # Pattern: /<nri-location>/<city>-<intent>/
            return f"/{obj['nri']}/{obj['city']}-{obj['intent']}/"
        elif obj['intent']:
            # Pattern: /<city>/<intent>/
            return f"/{obj['city']}/{obj['intent']}/"
        else:
            # Pattern: /<city>/
            return f"/{obj['city']}/"

