# Image Format Quick Reference

## Supported Formats

### 1. LinkedIn Header
**Dimensions:** 1200 × 630 pixels (16:9 aspect ratio)

**Use For:**
- LinkedIn posts
- Social media sharing
- Open Graph (OG) tags for websites
- General blog headers

**Layout Tips:**
- Horizontal composition
- Leave left OR right third clear for text overlay
- Professional polish
- Works great for wide concepts

---

### 2. Medium Header
**Dimensions:** 1200 × 400 pixels (3:1 aspect ratio)

**Use For:**
- Medium/Substack blog headers
- Newsletter headers
- Email headers
- Wide banner-style images

**Layout Tips:**
- Extra wide, cinematic feel
- Can be more artistic/atmospheric
- Text overlays work best at top or bottom
- Good for panoramic concepts

---

### 3. Square Concept
**Dimensions:** 1080 × 1080 pixels (1:1 aspect ratio)

**Use For:**
- Instagram posts
- Twitter/X posts
- Concept visualization cards
- Profile images
- Thumbnails

**Layout Tips:**
- Centered composition
- High-level concept at a glance
- Icon-like clarity
- Minimal text space needed
- Should work without any text overlay

---

### 4. Vertical Explainer
**Dimensions:** 1080 × 1920 pixels (9:16 aspect ratio)

**Use For:**
- Instagram/Facebook Stories
- Detailed concept breakdown
- Mobile-first content
- Step-by-step visualizations
- Pinterest pins

**Layout Tips:**
- Vertical top-to-bottom flow
- Can show process or progression
- More detail allowed than other formats
- Good for sequential concepts
- Mobile-optimized viewing

---

## Format Selection Guide

| If you need... | Use this format |
|----------------|-----------------|
| Blog post header | LinkedIn (1200×630) |
| Newsletter/Substack header | Medium (1200×400) |
| Social media post | Square (1080×1080) |
| Instagram/TikTok story | Vertical (1080×1920) |
| Open Graph preview | LinkedIn (1200×630) |
| Concept card | Square (1080×1080) |
| Tutorial walkthrough | Vertical (1080×1920) |

---

## Quick Command Reference

```bash
# LinkedIn Header (default)
python generate_image.py --image-type linkedin --prompt "..." --output "name.png"

# Medium Header
python generate_image.py --image-type medium --prompt "..." --output "name.png"

# Square Concept
python generate_image.py --image-type square --prompt "..." --output "name.png"

# Vertical Explainer
python generate_image.py --image-type vertical --prompt "..." --output "name.png"

# Custom output directory
python generate_image.py --output-dir "path/to/images" --prompt "..." --output "name.png"
```
