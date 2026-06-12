# AI Prompt Patterns für Bildgenerierung

## Prompt-Anatomie

### Basis-Struktur
```
[Subjekt] + [Aktion/Pose] + [Umgebung] + [Stil] + [Technische Parameter]
```

### Erweiterte Struktur (Midjourney)
```
[Subjekt], [Details], [Umgebung], [Beleuchtung], [Stil], [Kamera], --ar [Ratio] --v 6
```

---

## DALL-E 3 Prompts

### Charakteristik
- Natürliche Sprache bevorzugt
- Detaillierte Beschreibungen funktionieren gut
- Versteht Kontext und Intention
- Gute Text-Rendering-Fähigkeiten

### Template: Featured Image (Business)
```
Professional photograph of [SUBJEKT/SZENE].
Modern corporate setting with [UMGEBUNG].
[BELEUCHTUNG] lighting creating a [STIMMUNG] atmosphere.
Clean, minimal composition with space for text overlay on [POSITION].
Colors should include [MARKENFARBEN].
High-quality commercial photography style.
```

**Beispiel:**
```
Professional photograph of a diverse team collaborating around
a modern conference table. Bright, airy office with large windows
and minimalist furniture. Soft natural lighting creating an
optimistic atmosphere. Clean, minimal composition with space
for text overlay on the left side. Colors should include deep
blue (#003366) accents. High-quality commercial photography style.
```

### Template: Abstract Concept
```
Abstract visual representation of [KONZEPT].
[STIL] style with [FARBEN] color palette.
[GEOMETRIE/FORMEN] shapes flowing [BEWEGUNG].
Modern, professional aesthetic suitable for business presentation.
No text in image.
```

### Template: Product/Service Visualization
```
[PRODUKT/SERVICE] visualized as [METAPHER].
Professional, clean aesthetic with [MARKENFARBEN].
[PERSPEKTIVE] view with [BELEUCHTUNG].
Photorealistic rendering style.
White or gradient background.
```

---

## Midjourney v6 Prompts

### Charakteristik
- Kürzere, keyword-basierte Prompts
- Parameter am Ende (--ar, --v, --s, --c)
- Style References mit --sref
- Negative Prompts mit --no

### Parameter-Referenz
| Parameter | Bedeutung | Werte |
|-----------|-----------|-------|
| --ar | Aspect Ratio | 1:1, 16:9, 4:5, 9:16 |
| --v | Version | 6, 6.1 |
| --s | Stylize | 0-1000 (Default: 100) |
| --c | Chaos | 0-100 |
| --no | Negative Prompt | text, watermark, etc. |
| --q | Quality | .25, .5, 1, 2 |
| --sref | Style Reference | URL |

### Template: Corporate Photography
```
professional corporate photography, [SUBJEKT],
[UMGEBUNG], modern office aesthetic,
[BELEUCHTUNG] lighting, sharp focus,
commercial quality, [MARKENFARBE] color accent
--ar 16:9 --v 6 --s 150 --no text watermark logo
```

### Template: Social Media Graphic
```
modern social media graphic design, [THEMA],
clean minimal layout, [STIL] style,
[FARBEN] color scheme, negative space for text,
professional marketing asset
--ar 1:1 --v 6 --s 200 --no text words letters
```

### Template: Person/Portrait (Fotorealistisch)
```
professional headshot photography, [BESCHREIBUNG PERSON],
[AUSDRUCK/EMOTION], [KLEIDUNG],
studio lighting, neutral background,
commercial quality, authentic expression
--ar 4:5 --v 6 --s 100
```

### Template: Infographic Background
```
abstract geometric background, [FARBEN] gradient,
flowing shapes, modern data visualization aesthetic,
clean professional design, subtle patterns,
space for overlay content
--ar 2:3 --v 6 --s 250 --no text
```

---

## Stable Diffusion Prompts

### Charakteristik
- Positive und Negative Prompts getrennt
- Keyword-basiert mit Gewichtung (Wort:1.3)
- Viele Checkpoints/Models verfügbar
- CFG Scale und Steps beeinflussen Output

### Template-Struktur
```
Positive Prompt:
[HAUPTSUBJEKT], [DETAILS], [STIL], [QUALITÄT-KEYWORDS]

Negative Prompt:
[UNERWÜNSCHTE ELEMENTE]
```

### Qualitäts-Keywords (Positive)
```
masterpiece, best quality, high resolution,
professional photography, sharp focus,
detailed, 8k uhd, commercial quality
```

### Standard Negative Prompt
```
low quality, blurry, distorted, deformed,
ugly, bad anatomy, watermark, text, logo,
signature, jpeg artifacts, cropped,
worst quality, normal quality
```

### Template: Business Scene
```
Positive:
professional business photography, (SUBJEKT:1.2),
modern office environment, natural lighting,
commercial quality, sharp focus, bokeh background,
masterpiece, best quality

Negative:
low quality, blurry, text, watermark, logo,
deformed, ugly, amateur, stock photo watermark
```

---

## Stil-Bibliothek

### Professionell / Corporate
```
commercial photography, professional, clean,
modern, minimal, corporate, business-like,
polished, high-end, sophisticated
```

### Warm / Einladend
```
warm lighting, inviting, friendly, approachable,
welcoming, cozy, soft tones, natural light,
comfortable, relaxed atmosphere
```

### Technisch / Innovativ
```
futuristic, tech-forward, sleek, cutting-edge,
digital, innovative, modern technology,
clean lines, geometric, precise
```

### Kreativ / Dynamisch
```
vibrant, energetic, bold, creative, dynamic,
colorful, expressive, artistic, contemporary,
eye-catching, striking
```

---

## Beleuchtungs-Patterns

| Stil | Prompt-Keywords | Wirkung |
|------|-----------------|---------|
| Natural | natural light, window light, soft daylight | Authentisch, warm |
| Studio | studio lighting, softbox, professional | Kontrolliert, clean |
| Dramatic | dramatic lighting, rim light, contrast | Impactful, bold |
| Golden Hour | golden hour, warm sunlight, sunset | Emotional, atmospheric |
| High Key | bright, well-lit, minimal shadows | Optimistisch, offen |
| Low Key | moody, shadows, selective lighting | Dramatisch, serious |

---

## Markenfarben-Integration

### Primärfarbe: #003366 (Dark Blue)
```
deep navy blue, dark blue (#003366),
corporate blue, professional blue
```

### Akzentfarbe: #ff6600 (Orange)
```
vibrant orange, warm orange (#ff6600),
accent orange, energetic orange
```

### Farbkombination
```
navy blue and orange color scheme,
deep blue (#003366) with orange (#ff6600) accents,
corporate blue with warm orange highlights
```

---

## Prompt-Checkliste

### Vor dem Generieren prüfen:
- [ ] Aspect Ratio passend zur Plattform?
- [ ] Markenfarben integriert?
- [ ] Platz für Text-Overlay berücksichtigt?
- [ ] Negative Prompts für Text/Watermarks?
- [ ] Stil passend zur Brand Voice?
- [ ] Beleuchtung definiert?
- [ ] Qualitäts-Keywords enthalten?

### Nach dem Generieren:
- [ ] Bild in richtiger Auflösung?
- [ ] Keine unerwünschten Elemente?
- [ ] Marken-konsistent?
- [ ] Für alle Größen adaptierbar?

---

## Batch-Generierung (AdCreative.ai Approach)

### Für Ad Creatives mehrere Varianten generieren:

1. **Variation A: Produkt-fokussiert**
```
[Produkt im Zentrum], clean background,
professional product photography
```

2. **Variation B: Lifestyle**
```
[Produkt in Verwendung], lifestyle setting,
authentic moment
```

3. **Variation C: Abstract/Konzept**
```
abstract representation of [Nutzen],
modern graphic design
```

4. **Variation D: Social Proof**
```
[glücklicher Kunde/Nutzer], testimonial aesthetic,
authentic expression
```

### Output pro Content-Piece:
- 1x Featured Image
- 3x Ad Varianten (A/B Testing)
- 1x Social Square
- 1x Story/Reel Format
- 1x Pinterest Long
