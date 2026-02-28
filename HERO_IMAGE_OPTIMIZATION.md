# Hero Image Optimization Guide

## Current Issue
The hero background image lacks the sharpness and visual impact of Zillow's hero section.

## Recommended Image Specifications

### Optimal Dimensions
- **Width**: 2560px minimum (for 4K displays)
- **Height**: 1440px minimum
- **Aspect Ratio**: 16:9 or wider (21:9 for ultra-wide)
- **File Format**: WebP (with JPG fallback)
- **File Size**: 300-500KB (compressed)

### Image Quality Requirements
1. **Resolution**: High-resolution, professionally shot
2. **Sharpness**: In-focus, crisp details
3. **Lighting**: Bright, natural daylight
4. **Composition**: 
   - House/property in center-right
   - Clear foreground (fence/yard)
   - People optional but adds warmth
   - Blue sky visible

### Where to Get Quality Images

#### Free Stock Photo Sites
1. **Unsplash** - https://unsplash.com/s/photos/modern-house
2. **Pexels** - https://www.pexels.com/search/real-estate/
3. **Pixabay** - https://pixabay.com/images/search/house/

#### Paid Stock Photo Sites (Better Quality)
1. **Shutterstock** - Premium real estate images
2. **Adobe Stock** - High-res property photos
3. **Getty Images** - Professional real estate photography

### Search Keywords
- "modern house exterior"
- "suburban home front yard"
- "real estate property exterior"
- "residential house with fence"
- "family home exterior daylight"

## CSS Optimizations Applied

```css
/* Sharp image rendering */
image-rendering: -webkit-optimize-contrast;
image-rendering: crisp-edges;

/* Slight contrast/brightness boost */
filter: contrast(1.05) brightness(1.02);

/* Proper background positioning */
background: center center/cover no-repeat;
```

## Implementation Steps

1. Download a high-quality hero image (2560x1440px minimum)
2. Optimize using tools like:
   - **TinyPNG** - https://tinypng.com/
   - **Squoosh** - https://squoosh.app/
   - **ImageOptim** (Mac) or **FileOptimizer** (Windows)
3. Convert to WebP format for better compression
4. Replace `realtor-web/static/images/propertism-hero-bg.jpg`
5. Add WebP version: `propertism-hero-bg.webp`

## Current Image
- **File**: `realtor-web/static/images/propertism-hero-bg.jpg`
- **Size**: 1.5MB (could be optimized)
- **Status**: Needs replacement with sharper, wider image

## Next Steps
1. Source a professional-quality hero image
2. Optimize for web (compress to 300-500KB)
3. Replace current image
4. Test on multiple screen sizes
