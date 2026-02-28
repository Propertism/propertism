"""
Sitemap configuration for Propertism
Generates dynamic sitemap.xml for search engines
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost
from properties.models import Property


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
        return obj.updated_at
    
    def location(self, obj):
        return f'/blog/{obj.slug}/'
