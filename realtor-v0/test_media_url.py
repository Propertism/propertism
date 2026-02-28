import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from django.conf import settings

print("=== MEDIA URL TEST ===")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"DEBUG: {settings.DEBUG}")

# Check if file exists
hero_path = os.path.join(settings.MEDIA_ROOT, 'hero', 'propertism-hero-bg.jpg')
print(f"\nFile path: {hero_path}")
print(f"File exists: {os.path.exists(hero_path)}")
if os.path.exists(hero_path):
    size = os.path.getsize(hero_path) / 1024
    print(f"File size: {size:.1f} KB")

# Test URL
url = "http://localhost:8000/media/hero/propertism-hero-bg.jpg"
print(f"\nTesting URL: {url}")
try:
    response = requests.get(url, timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Image is accessible!")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
    else:
        print(f"❌ Got {response.status_code} - image not accessible")
except Exception as e:
    print(f"❌ Error: {e}")
