#!/usr/bin/env python
"""Create a placeholder property image"""
try:
    from PIL import Image, ImageDraw, ImageFont
    
    # Create 800x600 placeholder
    img = Image.new('RGB', (800, 600), color=(15, 23, 42))  # Navy
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([10, 10, 790, 590], outline=(184, 154, 74), width=2)  # Gold
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    text = "Property Image"
    draw.text((400, 300), text, fill=(184, 154, 74), font=font, anchor="mm")
    
    # Save
    img.save('static/images/placeholder-property.jpg', 'JPEG', quality=85)
    print("✅ Created placeholder-property.jpg")
    
except ImportError:
    print("❌ PIL not installed. Creating empty file...")
    # Create empty file to stop 404 errors
    with open('static/images/placeholder-property.jpg', 'wb') as f:
        f.write(b'')
    print("⚠️  Created empty placeholder file")
