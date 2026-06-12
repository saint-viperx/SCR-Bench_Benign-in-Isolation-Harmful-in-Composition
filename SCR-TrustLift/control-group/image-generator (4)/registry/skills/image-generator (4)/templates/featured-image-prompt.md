# Featured Image Prompt Template

## Verwendung
Blog-Artikel, WordPress Posts, Social Sharing Preview

## Dimensionen
- **WordPress:** 1200x628 (1.91:1)
- **LinkedIn/Facebook:** 1200x627/630 (kompatibel)

---

## Input-Analyse

Vor der Prompt-Erstellung analysieren:

1. **Thema:** Was ist der Kerninhalt des Artikels?
2. **Zielgruppe:** B2B, B2C, Fachpublikum?
3. **Emotion:** Welches Gefühl soll transportiert werden?
4. **Keywords:** Welche visuellen Elemente repräsentieren das Thema?
5. **Text-Overlay:** Wird Headline auf dem Bild platziert?

---

## Prompt-Templates

### Template A: Business/Corporate

**DALL-E:**
```
Professional photograph for a business blog article about [THEMA].
Scene shows [SUBJEKT/SZENE] in a modern [UMGEBUNG].
[BELEUCHTUNG] lighting creates a [STIMMUNG] atmosphere.
Color palette includes navy blue (#003366) and orange (#ff6600) accents.
Clean composition with clear space on [links/rechts] for text overlay.
High-quality commercial photography, sharp focus, professional aesthetic.
Aspect ratio 1.91:1, landscape orientation.
```

**Midjourney:**
```
professional business photography, [THEMA],
[SUBJEKT] in modern office setting,
natural lighting, clean minimal composition,
navy blue and orange color accents,
commercial quality, negative space for text on [side],
corporate blog aesthetic
--ar 16:9 --v 6 --s 150 --no text watermark
```

---

### Template B: Abstract/Konzept

**DALL-E:**
```
Abstract visual representation of [KONZEPT] for business blog.
[STIL] style using geometric shapes and flowing lines.
Color scheme: deep navy blue (#003366) with vibrant orange (#ff6600) accents.
Modern, professional aesthetic suitable for corporate communications.
Clean background with dynamic elements.
Space for headline text on [Position].
No text or words in the image.
```

**Midjourney:**
```
abstract business concept visualization, [KONZEPT],
geometric shapes, flowing gradients,
navy blue and orange color scheme,
modern minimal design, professional aesthetic,
clean composition with text space
--ar 16:9 --v 6 --s 200 --no text words letters watermark
```

---

### Template C: Lifestyle/People

**DALL-E:**
```
Authentic lifestyle photograph for article about [THEMA].
[PERSON(EN) BESCHREIBUNG] engaged in [AKTIVITÄT].
Setting: [UMGEBUNG] with modern, welcoming atmosphere.
Natural, soft lighting creating warm tones.
Genuine expressions, not posed or artificial.
Navy blue (#003366) elements in environment or clothing.
Clean composition with space on [Position] for text overlay.
High-quality editorial photography style.
```

**Midjourney:**
```
authentic lifestyle photography, [THEMA],
[diverse professionals/people] [AKTIVITÄT],
modern [UMGEBUNG], natural lighting,
warm genuine atmosphere, editorial style,
navy blue clothing accent, commercial quality,
text space on [side]
--ar 16:9 --v 6 --s 100 --no text watermark stock photo aesthetic
```

---

### Template D: Daten/Tech

**DALL-E:**
```
Modern data visualization concept for article about [THEMA].
Abstract representation of [DATEN/TECH-KONZEPT].
Sleek, futuristic aesthetic with clean lines.
Dark navy blue (#003366) background with glowing orange (#ff6600) data elements.
Professional tech company style.
Subtle grid or network patterns.
Space for title text on lighter area.
No actual text or numbers in image.
```

**Midjourney:**
```
futuristic data visualization, [TECH-KONZEPT],
abstract digital network, glowing data points,
dark navy blue background, orange light accents,
sleek modern tech aesthetic, clean composition,
professional business technology style
--ar 16:9 --v 6 --s 200 --no text numbers watermark
```

---

## Output-Format

```json
{
  "image_type": "featured_image",
  "article_title": "[Titel des Artikels]",
  "dimensions": {
    "width": 1200,
    "height": 628
  },
  "aspect_ratio": "1.91:1",
  "prompts": {
    "dalle": "[Generierter DALL-E Prompt]",
    "midjourney": "[Generierter Midjourney Prompt]"
  },
  "text_overlay_zone": "left|right|top|bottom|none",
  "style_notes": "[Besondere Hinweise]",
  "alt_text": "[SEO-optimierter Alt-Text für Accessibility]",
  "suggested_filename": "[artikel-slug]-featured.jpg"
}
```

---

## Beispiel-Output

**Input:** Artikel "10 Content-Marketing-Strategien für den Mittelstand"

```json
{
  "image_type": "featured_image",
  "article_title": "10 Content-Marketing-Strategien für den Mittelstand",
  "dimensions": {
    "width": 1200,
    "height": 628
  },
  "aspect_ratio": "1.91:1",
  "prompts": {
    "dalle": "Professional photograph for a business blog article about content marketing strategies. Scene shows a diverse marketing team collaborating around a modern conference table with laptops and digital displays. Bright natural lighting through large windows creates an optimistic, productive atmosphere. Color palette includes navy blue (#003366) chairs and orange (#ff6600) accent items. Clean composition with clear space on the left side for text overlay. High-quality commercial photography, sharp focus, professional aesthetic. Aspect ratio 1.91:1, landscape orientation.",
    "midjourney": "professional business photography, content marketing strategy meeting, diverse team collaborating at modern conference table, natural lighting, clean minimal composition, navy blue and orange color accents, commercial quality, negative space for text on left, corporate blog aesthetic --ar 16:9 --v 6 --s 150 --no text watermark"
  },
  "text_overlay_zone": "left",
  "style_notes": "Authentische Team-Atmosphäre, keine gestellten Posen, moderne Büroumgebung",
  "alt_text": "Marketing-Team bei der Strategiebesprechung in modernem Büro",
  "suggested_filename": "content-marketing-strategien-mittelstand-featured.jpg"
}
```

---

## Checkliste

- [ ] Thema klar im Bild erkennbar?
- [ ] Markenfarben integriert?
- [ ] Platz für Text-Overlay?
- [ ] Keine Text-Elemente im Bild?
- [ ] Authentischer, nicht generischer Look?
- [ ] Passend für Zielgruppe?
- [ ] Alt-Text SEO-optimiert?
