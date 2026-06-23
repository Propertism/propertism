import urllib.request
import ssl
import xml.etree.ElementTree as ET

url = "https://www.propertism.in/sitemap.xml"

# Ignore SSL verification issues if any
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

print(f"Fetching sitemap from {url}...")
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
        content = response.read()
        print("Sitemap fetched successfully.")
        
        # Parse XML
        root = ET.fromstring(content)
        
        # Namespaces are usually present in sitemap files. 
        # Standard XML namespace for sitemap is http://www.sitemaps.org/schemas/sitemap/0.9
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        locs = []
        for url_tag in root.findall('sm:url', ns):
            loc = url_tag.find('sm:loc', ns)
            if loc is not None:
                locs.append(loc.text)
        
        print(f"Total URLs in sitemap: {len(locs)}")
        
        # Filter blog posts
        blog_urls = [l for l in locs if "/blog/" in l]
        print(f"Total blog post URLs in sitemap: {len(blog_urls)}")
        
        # Check for duplicates
        unique_blog_urls = set(blog_urls)
        print(f"Unique blog post URLs: {len(unique_blog_urls)}")
        
        # Find duplicates
        duplicates = []
        seen = set()
        for u in blog_urls:
            if u in seen:
                duplicates.append(u)
            else:
                seen.add(u)
        
        if duplicates:
            print("[WARN] DUPLICATES FOUND:")
            for d in duplicates:
                print(f"  - {d}")
        else:
            print("OK - No duplicates found in blog post URLs.")
            
        # List all blog URLs
        print("\nBlog post URLs found in sitemap:")
        for idx, u in enumerate(sorted(unique_blog_urls), 1):
            print(f"{idx:02d}. {u}")
            
except Exception as e:
    print(f"Error: {e}")
