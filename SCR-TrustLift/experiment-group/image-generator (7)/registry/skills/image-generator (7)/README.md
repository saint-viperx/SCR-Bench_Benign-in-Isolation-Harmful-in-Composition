# Image Generator Skill

Generate professional branded images using Google Gemini's image generation API.

## Quick Start

1. **Get a Gemini API key**: https://aistudio.google.com/apikey

2. **Set the environment variable**:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

3. **Install dependencies**:
   ```bash
   pip install google-genai pillow
   ```

4. **Create brand guidelines** (optional but recommended):
   Copy `BRAND_TEMPLATE.md` to your project root as `BRAND.md` and customize.

## Usage

The skill is invoked automatically when you ask Claude to generate images for your content.

**Example prompts:**
- "Generate a header image for my blog post about API design"
- "Create a LinkedIn header for my article on microservices"
- "Make a square concept card for my post about testing"

## Supported Formats

| Format | Dimensions | Use Case |
|--------|------------|----------|
| LinkedIn | 1200×630 | Blog headers, social sharing |
| Medium | 1200×400 | Newsletter headers |
| Square | 1080×1080 | Instagram, concept cards |
| Vertical | 1080×1920 | Stories, mobile content |

## Files

- `SKILL.md` - Main skill instructions for Claude
- `BRAND_TEMPLATE.md` - Template for project brand guidelines
- `IMAGE_FORMATS.md` - Detailed format specifications
- `generate_image.py` - Python script for image generation

## Brand Customization

The skill looks for brand guidelines in your project:
1. `BRAND.md` (project root)
2. `.claude/BRAND.md`
3. `docs/BRAND.md`

See `BRAND_TEMPLATE.md` for the full template structure.
