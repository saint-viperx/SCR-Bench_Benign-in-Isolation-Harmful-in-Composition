---
name: image-generator
description: Creates and manages visual assets for content. Generates AI image prompts for DALL-E, Midjourney, and Stable Diffusion. Specifies image requirements, handles brand consistency, and optimizes for different platforms. Includes featured images, social graphics, ad creatives, and thumbnails. Use when content needs visual assets.
---

# Image Generator

Erstellt visuelle Assets für alle Content-Typen und Plattformen.

## Quick Start

```
Input: Content (Artikel, Social Post, Ad Copy)
Output: AI-Prompts + Bild-Specs für alle benötigten Formate
```

## Workflow

1. **Content analysieren** → Kernthema, Emotionen, Key Visuals identifizieren
2. **Formate bestimmen** → Welche Plattformen? (siehe [PLATFORM_IMAGE_SPECS.md](PLATFORM_IMAGE_SPECS.md))
3. **Brand-Konsistenz** → Farben, Style aus [BRAND_VISUAL_GUIDELINES.md](BRAND_VISUAL_GUIDELINES.md)
4. **Prompts erstellen** → Templates aus [AI_PROMPT_PATTERNS.md](AI_PROMPT_PATTERNS.md)
5. **Output formatieren** → JSON mit allen Bild-Specs

## Output Format

```json
{
  "content_id": "uuid",
  "images": [
    {
      "type": "featured_image",
      "platform": "wordpress",
      "dimensions": { "width": 1200, "height": 628 },
      "aspect_ratio": "1.91:1",
      "ai_prompt": {
        "dalle": "Prompt für DALL-E...",
        "midjourney": "Prompt für Midjourney...",
        "stable_diffusion": "Prompt für SD..."
      },
      "style_notes": "Markenfarben, keine Text-Overlays",
      "alt_text": "SEO-optimierter Alt-Text",
      "filename": "artikel-titel-featured.jpg"
    }
  ]
}
```

## Bild-Typen

| Typ | Verwendung | Specs |
|-----|------------|-------|
| Featured Image | Blog, WordPress | [templates/featured-image.md](templates/featured-image-prompt.md) |
| Social Graphic | LinkedIn, FB, etc. | [templates/social-graphic.md](templates/social-graphic-prompt.md) |
| Ad Creative | Paid Ads | [templates/ad-creative.md](templates/ad-creative-prompt.md) |
| Thumbnail | YouTube, Pinterest | [templates/thumbnail.md](templates/thumbnail-prompt.md) |
| Carousel Slides | IG, LinkedIn | [templates/carousel.md](templates/carousel-prompt.md) |
| Infographic | Linkbait, Educational | [templates/infographic.md](templates/infographic-brief.md) |

## Platform-Specific Dimensions

Quick Reference (Details in [PLATFORM_IMAGE_SPECS.md](PLATFORM_IMAGE_SPECS.md)):

| Platform | Format | Dimensions |
|----------|--------|------------|
| WordPress | Featured | 1200x628 |
| LinkedIn | Post | 1200x627 |
| LinkedIn | Carousel | 1080x1080 |
| Instagram | Feed | 1080x1080 |
| Instagram | Story/Reel | 1080x1920 |
| Facebook | Post | 1200x630 |
| TikTok | Video | 1080x1920 |
| Pinterest | Pin | 1000x1500 |
| Google Display | Leaderboard | 728x90 |
| Google Display | Rectangle | 300x250 |

## AI-Tool Empfehlung

| Use Case | Empfohlenes Tool |
|----------|-----------------|
| Fotorealistische Menschen | Midjourney v6 |
| Abstrakte Konzepte | DALL-E 3 |
| Schnelle Iteration | Stable Diffusion |
| Text auf Bild | Ideogram / Canva |
| Konsistenter Style | Midjourney (Style Reference) |

## Brand Integration

Alle Bilder müssen Brand Guidelines folgen:
- Primärfarbe: #003366 (Dark Blue)
- Akzentfarbe: #ff6600 (Orange)
- Style: Professionell, modern, zugänglich

Details: [BRAND_VISUAL_GUIDELINES.md](BRAND_VISUAL_GUIDELINES.md)
