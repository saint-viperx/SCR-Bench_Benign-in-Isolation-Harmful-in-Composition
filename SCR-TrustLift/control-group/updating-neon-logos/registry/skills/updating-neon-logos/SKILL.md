---
name: updating-neon-logos
description: Updates Neon logos across repositories to match official brand assets. This skill should be used when updating, replacing, or auditing Neon logo files in any codebase to ensure brand consistency with neon.com/brand guidelines.
---

# Updating Neon Logos

This skill updates Neon logos in repositories to match official brand assets from https://neon.com/brand.

## Core Principle

**Preserve format, replace logo.** For every logo file discovered:
1. Analyze existing: dimensions, background, format, position
2. Preserve: all design decisions (size, colors, layout)
3. Replace: only the logo itself with official `#37C38F` brand version

Never change dimensions, backgrounds, or layouts unless explicitly requested.

## Quick Start

To update logos in the current repository:

1. Run discovery to find all logo files
2. Review recommendations for each logo
3. Confirm which logos to update
4. Skill downloads official assets and replaces

## Official Brand Assets

### Logo Variants

| Variant | Use Case | URL |
|---------|----------|-----|
| Full Logo (Dark BG, Color) | Dark mode headers, footers | `https://neon.com/brand/neon-logo-dark-color.svg` |
| Full Logo (Light BG, Color) | Light mode headers, footers | `https://neon.com/brand/neon-logo-light-color.svg` |
| Logomark (Dark BG, Color) | Favicons, small spaces, app icons | `https://neon.com/brand/neon-logomark-dark-color.svg` |
| Logomark (Light BG, Color) | Favicons, small spaces, app icons | `https://neon.com/brand/neon-logomark-light-color.svg` |
| Full Package | All variants and formats | `https://neon.com/brand/neon-brand-assets.zip` |

### Favicon Assets (from neon.com/favicon/)

For favicons, download directly from neon.com rather than converting from brand assets:

| Asset | URL | Size |
|-------|-----|------|
| SVG Favicon (primary) | `https://neon.com/favicon/favicon.svg` | 180x180 viewBox |
| ICO Favicon (fallback) | `https://neon.com/favicon/favicon.ico` | 100x100 |
| Apple Touch Icon | `https://neon.com/favicon/apple-touch-icon.png` | 180x180 |

**Important notes:**
- The SVG favicon has ~10% built-in padding around the logo, which makes it appear properly sized in browser tabs
- Browsers prefer SVG over ICO when both are available, so always configure your framework to list SVG first
- Always download these production-ready assets rather than converting from brand SVGs

### Brand Guidelines

- Default to full-color complete logo
- Use logomark only when space is limited or displaying multiple brand symbols
- Maintain safety area spacing (defined by symbol height)
- Never edit, distort, recolor, or reconfigure logos

## Workflow

### Phase 1: Discovery

Search the repository for logo files and references:

**File searches:**
- `**/*neon*.{svg,png,jpg,jpeg,ico,webp}`
- `**/*logo*.{svg,png,jpg,jpeg,ico,webp}`
- `**/favicon.{ico,png,svg}`
- `**/og-image.{png,jpg}`

**Code reference searches:**
- Import statements: `import.*neon.*svg|png`
- HTML img tags: `<img.*neon|logo`
- CSS backgrounds: `url.*neon|logo`
- Markdown images: `!\[.*\].*neon|logo`

Present findings as a table with:
- File path
- Current format
- File size
- Usage context (if determinable from code)

### Phase 2: Analysis

For each discovered logo, analyze the EXISTING file:

1. **Current Format**
   - Dimensions (width × height)
   - File format (SVG, PNG, ICO, JPG)
   - Background color (transparent, dark, light)
   - Logo variant (full logo vs logomark)

2. **Logo Type in Use**
   - Full logo: Text + symbol together
   - Logomark: Symbol only

3. **Background Context**
   - Transparent: Logo on variable backgrounds
   - Dark background: Use dark-variant replacement
   - Light background: Use light-variant replacement

4. **Replacement Strategy**
   - SVG → Download matching official SVG, preserve viewBox/dimensions
   - PNG → Generate PNG from official SVG at same dimensions
   - ICO → Download official favicon.ico
   - Composite images (OG, banners) → Regenerate with same background + official logo

### Phase 3: Recommendation

Present a recommendation table:

| Current File | Context | Recommended Replacement | Reason |
|--------------|---------|------------------------|--------|
| icons/neon.svg | Header component | neon-logo-dark-color.svg | Full logo for header |
| public/favicon.ico | Browser favicon | neon-logomark-dark-color.svg → ICO | Logomark for favicon |
| README.md reference | Documentation | neon-logo-dark-color.svg | External URL for docs |

### Phase 4: Confirmation

For each recommendation, ask the user:

> **Update [file path]?**
> Current: [description]
> Recommended: [official asset name]
> Reason: [context-based reasoning]
>
> Options: Yes / No / Skip All

### Phase 5: Update

For approved changes, follow the **preserve format, replace logo** principle:

1. **For SVG files**, download official SVG and adjust dimensions:
   ```bash
   # Download official asset
   curl -o /tmp/official.svg "https://neon.com/brand/neon-logomark-dark-color.svg"

   # Preserve original dimensions (e.g., width="26" height="26")
   # Update the file with official paths but keep size attributes
   ```

2. **For PNG files**, regenerate at same dimensions with HIGH DENSITY:
   ```bash
   # Get original dimensions
   identify original-logo.png  # e.g., 1000x1000

   # Download official SVG and convert to PNG at same size
   curl -o /tmp/official.svg "https://neon.com/brand/neon-logomark-dark-color.svg"

   # IMPORTANT: Use high density (1200+) for crisp edges!
   # ImageMagick rasterizes SVG at the density first, then resizes.
   # Low density = small intermediate raster = upscaling = blurry edges
   # High density = large intermediate raster = downscaling = crisp edges
   magick -background none -density 1200 /tmp/official.svg -resize 1000x1000 -depth 8 new-logo.png
   ```

3. **For composite images** (OG images, banners, social previews):
   ```bash
   # Analyze existing image
   identify public/og-image.png  # Get dimensions and format

   # Detect background color (or note from visual inspection)
   # Regenerate with SAME dimensions and background, NEW logo
   # Use high density for the SVG conversion to ensure crisp logo edges
   magick -size [WIDTH]x[HEIGHT] xc:'[EXISTING_BG_COLOR]' \
     \( -density 1200 /tmp/official.svg -resize [LOGO_SIZE] \) \
     -gravity center -composite public/og-image.png
   ```

   **Key principle:** Preserve existing design decisions (background, dimensions, layout). Only replace the logo itself with the official brand version.

4. **For favicons**, download complete set from neon.com/favicon/:
   ```bash
   curl -o public/favicon.svg "https://neon.com/favicon/favicon.svg"
   curl -o public/favicon.ico "https://neon.com/favicon/favicon.ico"
   curl -o public/apple-touch-icon.png "https://neon.com/favicon/apple-touch-icon.png"
   ```

5. **Update framework icon configuration** to prioritize SVG:

   **Next.js (app/layout.tsx):**
   ```typescript
   export const metadata: Metadata = {
     icons: {
       icon: [
         { url: '/favicon.svg', type: 'image/svg+xml' },
         { url: '/favicon.ico', sizes: '32x32' },
       ],
       apple: '/apple-touch-icon.png',
     },
   };
   ```

   **HTML (manual):**
   ```html
   <link rel="icon" type="image/svg+xml" href="/favicon.svg">
   <link rel="icon" type="image/x-icon" sizes="32x32" href="/favicon.ico">
   <link rel="apple-touch-icon" href="/apple-touch-icon.png">
   ```

6. **Update code references** if paths changed

7. **Report changes** with before/after:
   ```
   ✅ Updated: icons/neon.svg (26x26 SVG → official logomark, preserved dimensions)
   ✅ Updated: public/logo.png (1000x1000 PNG → regenerated with official logo)
   ✅ Updated: public/og-image.png (1200x630 → preserved background, updated logo)
   ✅ Updated: public/favicon.svg (new file from neon.com/favicon)
   ```

## Decision Tree

```
Is space limited (< 100px or multi-brand context)?
├── Yes → Use Logomark
│   └── What's the background?
│       ├── Dark → neon-logomark-dark-color.svg
│       └── Light → neon-logomark-light-color.svg
└── No → Use Full Logo
    └── What's the background?
        ├── Dark → neon-logo-dark-color.svg
        └── Light → neon-logo-light-color.svg

What format is needed?
├── Scalable web element → Keep as SVG
├── Fixed size image → Convert to PNG
├── OG/Social image → Regenerate with official logomark
│   ├── Preserve: Existing dimensions, background color, layout
│   └── Replace: Logo with official logomark (#37C38F)
└── Browser favicon → Download from neon.com/favicon/
    ├── Primary: favicon.svg (vector)
    ├── Fallback: favicon.ico (100x100)
    └── iOS: apple-touch-icon.png (180x180)
```

## Examples

**Example 1: Header Logo**
- Context: Next.js header component, supports dark mode
- Current: Custom SVG in `icons/neon.svg`
- Recommendation: Replace with `neon-logo-dark-color.svg` for dark mode, add `neon-logo-light-color.svg` for light mode toggle

**Example 2: README Badge**
- Context: Markdown README file
- Current: Reference to old logo URL
- Recommendation: Update to `https://neon.com/brand/neon-logo-dark-color.svg`

**Example 3: Favicon**
- Context: Browser favicon
- Current: Generic `favicon.ico`
- Recommendation:
  1. Download complete favicon set from neon.com/favicon/:
     - `favicon.svg` (primary, vector with built-in padding)
     - `favicon.ico` (fallback, 100x100)
     - `apple-touch-icon.png` (iOS, 180x180)
  2. Update framework icon configuration to prioritize SVG over ICO

**Example 4: OG Image / Composite Image**
- Context: Social media preview image (`public/og-image.png`)
- Current: 1200x630, dark background, centered logo with old gradient colors
- Recommendation:
  1. Preserve: 1200x630 dimensions, dark background, centered layout
  2. Replace: Logo with official logomark using `#37C38F` brand color
  3. Regenerate PNG with same composition, new logo

## Guidelines

- **Preserve format, replace logo** - never change dimensions, backgrounds, or layouts without explicit request
- **Always use high density (1200+) for SVG→PNG conversion** - this ensures crisp edges by rasterizing at high resolution before resizing
- Always ask for confirmation before modifying files
- Preserve original files as backups if requested
- Report all changes with before/after comparison showing preserved dimensions
- For unknown backgrounds, inspect the existing file first before asking user
- All logo instances must use the official brand color `#37C38F` (no custom gradients)
- OG images, banners, and composite images are NOT exceptions - they must be updated too
