import json
from django.test import TestCase, RequestFactory
from django.urls import reverse
from content.templatetags.seo_tags import breadcrumb_schema
from content.sitemaps import StaticViewSitemap


class BreadcrumbSchemaTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_breadcrumb_schema_with_explicit_urls(self):
        request = self.factory.get('/services/')
        context = {'request': request}
        items = [
            {'name': 'Home', 'url': '/'},
            {'name': 'Services', 'url': '/services/'}
        ]
        result = breadcrumb_schema(context, items)
        self.assertIsNotNone(result['schema'])
        
        schema = json.loads(result['schema'])
        self.assertEqual(schema['@type'], 'BreadcrumbList')
        self.assertEqual(len(schema['itemListElement']), 2)
        
        item1 = schema['itemListElement'][0]
        self.assertEqual(item1['@type'], 'ListItem')
        self.assertEqual(item1['position'], 1)
        self.assertEqual(item1['name'], 'Home')
        self.assertEqual(item1['item'], 'https://www.propertism.in/')
        
        item2 = schema['itemListElement'][1]
        self.assertEqual(item2['@type'], 'ListItem')
        self.assertEqual(item2['position'], 2)
        self.assertEqual(item2['name'], 'Services')
        self.assertEqual(item2['item'], 'https://www.propertism.in/services/')

    def test_breadcrumb_schema_leaf_item_without_url_resolves_canonical_url(self):
        request = self.factory.get('/management/')
        context = {'request': request, 'canonical_override': '/management/'}
        items = [
            {'name': 'Home', 'url': '/'},
            {'name': 'Management', 'url': None}  # Leaf crumb with None URL
        ]
        result = breadcrumb_schema(context, items)
        self.assertIsNotNone(result['schema'])
        
        schema = json.loads(result['schema'])
        item2 = schema['itemListElement'][1]
        self.assertEqual(item2['name'], 'Management')
        self.assertEqual(item2['item'], 'https://www.propertism.in/management/')

    def test_breadcrumb_schema_empty_items_returns_none(self):
        request = self.factory.get('/')
        context = {'request': request}
        self.assertEqual(breadcrumb_schema(context, None), {'schema': None})
        self.assertEqual(breadcrumb_schema(context, []), {'schema': None})


class SitemapIntegrityTests(TestCase):
    def test_static_view_sitemap_has_no_redirects(self):
        sitemap = StaticViewSitemap()
        urls = sitemap.get_urls()
        
        # Verify /contact/ is NOT in sitemap items
        locations = [u['location'] for u in urls]
        for loc in locations:
            self.assertFalse(loc.endswith('/contact/'), f"Redirected URL {loc} found in static sitemap!")
        
        # Verify required valid static pages exist
        self.assertTrue(any(u['location'].endswith('/property-owner-resources/') for u in urls))
        self.assertTrue(any(u['location'].endswith('/services/') for u in urls))
        self.assertTrue(any(u['location'].endswith('/about/') for u in urls))
        self.assertTrue(any(u['location'].endswith('/management/') for u in urls))
