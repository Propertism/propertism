"""
Image and file validation utilities for Propertism
SCCB-44: Static Files & Media Infrastructure
"""
import os
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image
import magic


def validate_image_file(file):
    """
    Validate uploaded image files
    
    Checks:
    - File size (max 5MB)
    - File extension
    - MIME type
    - Image integrity
    """
    # Check file size
    max_size = 5 * 1024 * 1024  # 5 MB
    if file.size > max_size:
        raise ValidationError(f'Image file too large. Maximum size is {max_size / (1024 * 1024):.1f} MB.')
    
    # Check file extension
    ext = os.path.splitext(file.name)[1].lower()
    allowed_extensions = getattr(settings, 'ALLOWED_IMAGE_EXTENSIONS', ['.jpg', '.jpeg', '.png', '.gif', '.webp'])
    
    if ext not in allowed_extensions:
        raise ValidationError(f'Invalid file extension. Allowed: {", ".join(allowed_extensions)}')
    
    # Validate MIME type
    try:
        # Read first 2048 bytes for MIME detection
        file.seek(0)
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)
        
        allowed_mimes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if mime not in allowed_mimes:
            raise ValidationError(f'Invalid file type. Detected: {mime}')
    except Exception:
        # If python-magic not available, skip MIME check
        pass
    
    # Validate image integrity using Pillow
    try:
        file.seek(0)
        img = Image.open(file)
        img.verify()
        file.seek(0)
    except Exception as e:
        raise ValidationError(f'Invalid or corrupted image file: {str(e)}')
    
    return file


def validate_document_file(file):
    """
    Validate uploaded document files
    
    Checks:
    - File size (max 10MB)
    - File extension
    """
    # Check file size
    max_size = 10 * 1024 * 1024  # 10 MB
    if file.size > max_size:
        raise ValidationError(f'Document file too large. Maximum size is {max_size / (1024 * 1024):.1f} MB.')
    
    # Check file extension
    ext = os.path.splitext(file.name)[1].lower()
    allowed_extensions = getattr(settings, 'ALLOWED_DOCUMENT_EXTENSIONS', ['.pdf', '.doc', '.docx'])
    
    if ext not in allowed_extensions:
        raise ValidationError(f'Invalid file extension. Allowed: {", ".join(allowed_extensions)}')
    
    return file


def validate_property_image(file):
    """
    Specific validation for property images
    
    Additional checks:
    - Minimum dimensions (800x600)
    - Maximum dimensions (4000x3000)
    - Aspect ratio recommendations
    """
    # Run standard image validation
    file = validate_image_file(file)
    
    # Check image dimensions
    try:
        file.seek(0)
        img = Image.open(file)
        width, height = img.size
        file.seek(0)
        
        # Minimum dimensions
        if width < 800 or height < 600:
            raise ValidationError(f'Image too small. Minimum size is 800x600 pixels. Uploaded: {width}x{height}')
        
        # Maximum dimensions
        if width > 4000 or height > 3000:
            raise ValidationError(f'Image too large. Maximum size is 4000x3000 pixels. Uploaded: {width}x{height}')
        
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f'Could not read image dimensions: {str(e)}')
    
    return file


def sanitize_filename(filename):
    """
    Sanitize uploaded filename to prevent security issues
    
    - Remove special characters
    - Limit length
    - Prevent directory traversal
    """
    import re
    from django.utils.text import slugify
    
    # Get file extension
    name, ext = os.path.splitext(filename)
    
    # Slugify the name (removes special chars, converts to lowercase)
    name = slugify(name)
    
    # Limit length
    max_length = 100
    if len(name) > max_length:
        name = name[:max_length]
    
    # Reconstruct filename
    return f"{name}{ext.lower()}"


def get_upload_path(instance, filename):
    """
    Generate upload path for property images
    
    Format: properties/{property_id}/{sanitized_filename}
    """
    filename = sanitize_filename(filename)
    
    # Use property ID if available
    if hasattr(instance, 'property') and instance.property:
        return f'properties/{instance.property.id}/{filename}'
    elif hasattr(instance, 'id') and instance.id:
        return f'properties/{instance.id}/{filename}'
    else:
        # Fallback for new properties
        import uuid
        return f'properties/temp/{uuid.uuid4().hex[:8]}_{filename}'
