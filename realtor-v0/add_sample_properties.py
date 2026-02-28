"""
Script to add sample properties for testing SCCB-3 implementation
Run: python manage.py shell < add_sample_properties.py
"""

from properties.models import Property, PropertyType

# Create property types
property_types = [
    {'name': 'Apartment', 'slug': 'apartment'},
    {'name': 'Villa', 'slug': 'villa'},
    {'name': 'Independent House', 'slug': 'independent-house'},
]

for pt_data in property_types:
    PropertyType.objects.get_or_create(
        slug=pt_data['slug'],
        defaults={'name': pt_data['name']}
    )

apartment = PropertyType.objects.get(slug='apartment')
villa = PropertyType.objects.get(slug='villa')
house = PropertyType.objects.get(slug='independent-house')

# Sample properties
sample_properties = [
    {
        'title': '3BHK Luxury Apartment in Anna Nagar',
        'description': 'Spacious 3BHK apartment with modern amenities',
        'price': 8500000,
        'price_type': 'sale',
        'area': 1450,
        'bedrooms': 3,
        'bathrooms': 2,
        'location': 'Anna Nagar, Chennai',
        'property_type': apartment,
        'image': 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800',
    },
    {
        'title': '4BHK Villa with Private Garden',
        'description': 'Luxurious villa with private garden and pool',
        'price': 25000000,
        'price_type': 'sale',
        'area': 3200,
        'bedrooms': 4,
        'bathrooms': 4,
        'location': 'ECR, Chennai',
        'property_type': villa,
        'image': 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800',
    },
    {
        'title': '2BHK Apartment for Rent',
        'description': 'Well-maintained 2BHK apartment near metro',
        'price': 25000,
        'price_type': 'rent',
        'area': 1100,
        'bedrooms': 2,
        'bathrooms': 2,
        'location': 'Velachery, Chennai',
        'property_type': apartment,
        'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800',
    },
    {
        'title': 'Independent House in T Nagar',
        'description': 'Spacious independent house in prime location',
        'price': 15000000,
        'price_type': 'sale',
        'area': 2400,
        'bedrooms': 3,
        'bathrooms': 3,
        'location': 'T Nagar, Chennai',
        'property_type': house,
        'image': 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800',
    },
    {
        'title': 'Penthouse with Sea View',
        'description': 'Luxury penthouse with panoramic sea view',
        'price': 45000000,
        'price_type': 'sale',
        'area': 4500,
        'bedrooms': 5,
        'bathrooms': 5,
        'location': 'Besant Nagar, Chennai',
        'property_type': apartment,
        'image': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800',
    },
    {
        'title': '1BHK Studio Apartment',
        'description': 'Compact studio apartment for young professionals',
        'price': 18000,
        'price_type': 'rent',
        'area': 650,
        'bedrooms': 1,
        'bathrooms': 1,
        'location': 'OMR, Chennai',
        'property_type': apartment,
        'image': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800',
    },
]

for prop_data in sample_properties:
    Property.objects.get_or_create(
        title=prop_data['title'],
        defaults=prop_data
    )

print(f"✅ Created {Property.objects.count()} properties")
print(f"✅ Created {PropertyType.objects.count()} property types")
