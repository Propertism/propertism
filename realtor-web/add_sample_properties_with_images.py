"""
Add Sample Properties with High-Resolution Images
Creates realistic Chennai properties with beautiful images
"""

import os
import django
import sys
from pathlib import Path

# Setup Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from properties.models import Property, PropertyPhoto
from django.core.files.base import ContentFile
import requests
from io import BytesIO

def download_image(url):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ContentFile(response.content)
        return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def create_sample_properties():
    """Create sample properties with images"""
    
    print("🏠 Creating sample properties with high-resolution images...")
    
    # Sample properties data
    properties_data = [
        {
            'title': 'Luxury Villa in Adyar',
            'description': 'Stunning 4 BHK villa with modern amenities, spacious rooms, and beautiful garden. Perfect for NRI families looking for premium living in Chennai.',
            'location': 'Adyar, Chennai',
            'price': 25000000,  # 2.5 Cr
            'area': 3500,
            'bedrooms': 4,
            'bathrooms': 4,
            'status': 'available',
            'images': [
                'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1200&h=800&fit=crop',
            ]
        },
        {
            'title': 'Premium Apartment in Velachery',
            'description': 'Modern 3 BHK apartment in prime IT corridor location. Close to OMR, excellent connectivity, and top-notch amenities including gym and swimming pool.',
            'location': 'Velachery, Chennai',
            'price': 8500000,  # 85 Lakhs
            'area': 1800,
            'bedrooms': 3,
            'bathrooms': 3,
            'status': 'available',
            'images': [
                'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=1200&h=800&fit=crop',
            ]
        },
        {
            'title': 'Spacious Villa in Anna Nagar',
            'description': 'Beautiful 5 BHK independent villa in established neighborhood. Large plot, parking for 3 cars, perfect for joint families or NRI investment.',
            'location': 'Anna Nagar, Chennai',
            'price': 35000000,  # 3.5 Cr
            'area': 4200,
            'bedrooms': 5,
            'bathrooms': 5,
            'status': 'available',
            'images': [
                'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600607687644-c7171b42498f?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=1200&h=800&fit=crop',
            ]
        },
        {
            'title': 'Modern Apartment in OMR',
            'description': '2 BHK apartment in IT hub with excellent rental potential. Gated community with 24/7 security, ideal for NRI investment and rental income.',
            'location': 'OMR, Chennai',
            'price': 6500000,  # 65 Lakhs
            'area': 1200,
            'bedrooms': 2,
            'bathrooms': 2,
            'status': 'available',
            'images': [
                'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600573472591-ee6b68d14c68?w=1200&h=800&fit=crop',
            ]
        },
        {
            'title': 'Luxury Penthouse in Nungambakkam',
            'description': 'Exclusive 4 BHK penthouse with panoramic city views. Premium finishes, private terrace, and access to all luxury amenities.',
            'location': 'Nungambakkam, Chennai',
            'price': 45000000,  # 4.5 Cr
            'area': 3800,
            'bedrooms': 4,
            'bathrooms': 4,
            'status': 'available',
            'images': [
                'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600210492493-0946911123ea?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600607687644-aac4c3eac7f4?w=1200&h=800&fit=crop',
            ]
        },
        {
            'title': 'Affordable Apartment in Porur',
            'description': '2 BHK apartment in growing area with excellent connectivity. Perfect for first-time buyers or NRI investment with good rental yield.',
            'location': 'Porur, Chennai',
            'price': 5500000,  # 55 Lakhs
            'area': 1100,
            'bedrooms': 2,
            'bathrooms': 2,
            'status': 'available',
            'images': [
                'https://images.unsplash.com/photo-1600566753151-384129cf4e3e?w=1200&h=800&fit=crop',
                'https://images.unsplash.com/photo-1600573472550-8090b5e0745e?w=1200&h=800&fit=crop',
            ]
        },
    ]
    
    created_count = 0
    
    for prop_data in properties_data:
        try:
            # Extract images URLs
            image_urls = prop_data.pop('images', [])
            
            # Create or update property
            property_obj, created = Property.objects.update_or_create(
                title=prop_data['title'],
                defaults=prop_data
            )
            
            if created:
                print(f"✅ Created: {property_obj.title}")
                created_count += 1
            else:
                print(f"📝 Updated: {property_obj.title}")
            
            # Delete existing images
            property_obj.photos.all().delete()
            
            # Add new images
            for idx, image_url in enumerate(image_urls, 1):
                print(f"   📸 Downloading image {idx}...")
                image_content = download_image(image_url)
                
                if image_content:
                    property_photo = PropertyPhoto.objects.create(
                        property=property_obj,
                        is_primary=(idx == 1),
                        sort_order=idx
                    )
                    property_photo.image.save(
                        f'{property_obj.title.lower().replace(" ", "_")}_{idx}.jpg',
                        image_content,
                        save=True
                    )
                    print(f"   ✅ Image {idx} added")
                else:
                    print(f"   ❌ Failed to download image {idx}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error creating {prop_data.get('title', 'property')}: {e}")
            print()
    
    print(f"\n🎉 Complete! Created {created_count} new properties")
    print(f"📊 Total properties in database: {Property.objects.count()}")
    print(f"📸 Total images: {PropertyPhoto.objects.count()}")

if __name__ == '__main__':
    create_sample_properties()
