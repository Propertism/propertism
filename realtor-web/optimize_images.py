#!/usr/bin/env python
"""
Image Optimization Script for Propertism
Optimizes images for web performance
"""
import os
from pathlib import Path
from PIL import Image

def optimize_image(input_path, output_path=None, max_width=1920, quality=85):
    """
    Optimize an image for web use
    
    Args:
        input_path: Path to input image
        output_path: Path to save optimized image (defaults to input_path)
        max_width: Maximum width in pixels
        quality: JPEG quality (1-100)
    """
    if output_path is None:
        output_path = input_path
    
    try:
        # Open image
        img = Image.open(input_path)
        
        # Get original size
        original_size = os.path.getsize(input_path) / 1024  # KB
        
        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Resize if too large
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"  Resized to {max_width}x{new_height}")
        
        # Save optimized image
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # Get new size
        new_size = os.path.getsize(output_path) / 1024  # KB
        
        # Calculate savings
        savings = ((original_size - new_size) / original_size) * 100
        
        print(f"  Original: {original_size:.2f} KB")
        print(f"  Optimized: {new_size:.2f} KB")
        print(f"  Savings: {savings:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    """Optimize all images in the project"""
    print("\n" + "="*70)
    print("PROPERTISM IMAGE OPTIMIZATION")
    print("="*70 + "\n")
    
    base_dir = Path(__file__).resolve().parent
    
    # Images to optimize
    images = [
        {
            'path': base_dir / 'media' / 'hero' / 'propertism-hero-bg.jpg',
            'max_width': 1920,
            'quality': 82,
            'description': 'Hero background image'
        },
        {
            'path': base_dir / 'static' / 'images' / 'propertism-hero-bg.jpg',
            'max_width': 1920,
            'quality': 82,
            'description': 'Hero background image (static)'
        },
        {
            'path': base_dir / 'media' / 'team' / 'ics-11.png',
            'max_width': 800,
            'quality': 85,
            'description': 'Team member photo'
        },
    ]
    
    optimized_count = 0
    skipped_count = 0
    
    for img_info in images:
        img_path = img_info['path']
        
        if not img_path.exists():
            print(f"⏭️  Skipping: {img_info['description']}")
            print(f"  File not found: {img_path}")
            print()
            skipped_count += 1
            continue
        
        print(f"🖼️  Optimizing: {img_info['description']}")
        print(f"  Path: {img_path}")
        
        success = optimize_image(
            img_path,
            max_width=img_info['max_width'],
            quality=img_info['quality']
        )
        
        if success:
            optimized_count += 1
            print("  ✅ Done!")
        else:
            print("  ❌ Failed!")
        
        print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✅ Optimized: {optimized_count} images")
    print(f"⏭️  Skipped: {skipped_count} images")
    print("="*70 + "\n")
    
    if optimized_count > 0:
        print("✅ Image optimization complete!")
        print("\nNext steps:")
        print("1. Test the website to ensure images look good")
        print("2. Check page load speed")
        print("3. Add lazy loading to images (see template updates)")
    else:
        print("⚠️  No images were optimized.")

if __name__ == '__main__':
    main()
