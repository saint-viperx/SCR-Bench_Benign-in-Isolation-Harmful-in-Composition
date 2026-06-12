---
name: lg-nanobanana-sprite
description: Leverage AI (Nano Banana/Imagen) to generate high-quality visual assets (icons, logos, placemark images, overlay graphics) and integrate them into Liquid Galaxy Flutter apps.
---

# Nano Banana Asset Master

## Overview
This skill helps students transform text prompts into high-fidelity **visual assets** (custom placemark icons, logo overlays, balloon graphics, tour thumbnails, or data visualization icons) that look stunning on the Liquid Galaxy video wall. It covers the full pipeline: **Generation -> Transparent Processing -> LG Integration**.

## Phase 1: The Perfect Generation Prompt
To get a usable LG asset, you must be specific. Nano Banana generates squares, but we need clean icons and overlays.

**Prompt Template:**
> "Top-down view of a [Aesthetic, e.g., Modern Flat] [Object, e.g., Earthquake Pin Icon]. Feature: [Details, e.g., Concentric seismic rings, bold center dot]. Background: Solid bright neon green (#00FF00). High contrast, symmetrical, icon asset, 4k. The object must occupy the center of the frame. No checkerboard, no grid, no shadowed ground."

### Why Green?
Generating with a solid neon green background allows us to use a **Chroma Key** algorithm (like in Hollywood movies) to remove the background, as AI models often struggle to export true transparency (Alpha channel). After processing, we get clean PNGs for KML `<Icon>` and `<ScreenOverlay>` elements.

---

## Phase 2: Background Removal (Dart/Flutter)
Add this utility to your Flutter app to process AI-generated assets.

```dart
import 'dart:typed_data';
import 'package:image/image.dart' as img;

/// Removes bright green backgrounds from AI-generated assets.
/// Returns a PNG-encoded Uint8List with transparency.
Uint8List makeTransparent(Uint8List imageBytes) {
  final image = img.decodeImage(imageBytes);
  if (image == null) return imageBytes;

  for (int y = 0; y < image.height; y++) {
    for (int x = 0; x < image.width; x++) {
      final pixel = image.getPixel(x, y);
      final r = pixel.r.toInt();
      final g = pixel.g.toInt();
      final b = pixel.b.toInt();

      // Chroma Key: Target the bright Green (#00FF00)
      if (g > 100 && r < 100 && b < 100) {
        image.setPixelRgba(x, y, 0, 0, 0, 0); // Set Alpha to 0
      }
    }
  }

  return Uint8List.fromList(img.encodePng(image));
}
```

**Dependency**: Add `image: ^4.0.0` to `pubspec.yaml`.

---

## Phase 3: Sizing & Integration for LG
Liquid Galaxy screens are high-resolution (1080×1920 portrait, tiled across 3-7 screens). Assets must be crisp.

1.  **Icon Resolution**: Generate at **512×512** minimum for placemark icons. Google Earth scales them down, but low-res icons look blurry on the video wall.
2.  **Logo Overlays**: For `<ScreenOverlay>` logos, use **1024×512** or wider. These span a fraction of the slave screen.
3.  **Hosting for KML**: KML `<Icon><href>` needs a URL. Options:
    - Host on the LG rig: SCP to `/var/www/html/assets/` and reference `http://lg-master:81/assets/icon.png`.
    - Host externally: GitHub raw URL, Firebase Storage, etc.
4.  **Test in Google Earth Pro**: Always preview the asset in Google Earth desktop before sending to the rig.

---

## Example Task: Custom Earthquake Placemark Icon
Used in earthquake visualizer apps:
- **Prompt**: "Top-down view of a seismic wave icon. Concentric red-orange rings radiating from a bold red center dot. Background: Solid bright neon green (#00FF00). High contrast, icon asset, 4k."
- **Resolution**: 512×512 PNG.
- **KML Usage**: `<Style><IconStyle><Icon><href>http://lg-master:81/assets/quake_icon.png</href></Icon></IconStyle></Style>`

### Example: Satellite Tracker Pin
- **Prompt**: "Top-down view of a modern satellite with solar panels extended. Metallic blue and silver tones. Background: Solid bright neon green (#00FF00). High contrast, icon asset, 4k."
- **Strategy**: Use as a custom placemark icon for ISS or satellite tracking apps.

### Example: Custom LG Logo Overlay
- **Prompt**: "A sleek modern logo banner for Liquid Galaxy. Text 'LG' in futuristic font. Gradient blue-to-purple. Background: Solid bright neon green (#00FF00)."
- **KML Usage**: `<ScreenOverlay>` on slave screen with `<overlayXY>` and `<screenXY>` positioning.

---

## ⛔ Student Interaction Checkpoints

### After Asset Generation — Dimensions and Transparency

⛔ **STOP and WAIT** — After generating the asset, ask:
> *"Why did we generate at 512×512 minimum? What happens if you use a 64×64 icon on a Liquid Galaxy video wall that's 5760×1080 across 3 screens?"*

Wait for the student's answer.

### Background Removal — Understand the Technique

⛔ **STOP and WAIT** — After processing the image, ask:
> *"Why do we use a bright neon green (#00FF00) background instead of asking the AI to generate a transparent PNG? What is chroma keying, and where else is it used?"*

This is a "predict what happens" exercise — let them reason about why AI models struggle with alpha channels.

### KML Integration — Trace the Pipeline

⛔ **STOP and WAIT** — Ask:
> *"Trace the full asset pipeline: from the text prompt → generated image → processed PNG → hosted URL → KML `<Icon>` element → Google Earth display. What could go wrong at each step?"*

## Verification Checklist
- [ ] Is the object centered in the generated image?
- [ ] Is the green background completely removed (no "halo" effect)?
- [ ] Does the asset render correctly in Google Earth Pro (desktop preview)?
- [ ] Is the resolution high enough for the Liquid Galaxy video wall (512px+ for icons)?
- [ ] Is the asset hosted at a URL accessible by the LG rig?

## 🔗 Skill Chain

After the asset is generated, processed, and the student understands the pipeline, **automatically offer to return to initialization**:

> *"Asset generation complete! The icon is processed and ready for KML integration. Let's continue setting up the project. Ready to go back? 🎨"*

If student says "ready" → activate `.agent/skills/lg-init/SKILL.md` (asset generation phase complete).
