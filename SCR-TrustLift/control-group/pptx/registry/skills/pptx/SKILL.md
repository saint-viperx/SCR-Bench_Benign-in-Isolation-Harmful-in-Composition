---
name: pptx
description: "Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks"
---

# PPTX creation, editing, and analysis

## Overview

A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

---

## 完整工作流程概览

创建新演示文稿时，遵循以下完整工作流程：

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PPTX 制作完整工作流                               │
└─────────────────────────────────────────────────────────────────────┘

Phase 0: 准备阶段（必须）
─────────────────────────
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │ 0.1 内容    │ → │ 0.2 结构    │ → │ 0.3 设计    │
  │ 分析        │    │ 规划        │    │ 确认        │
  └─────────────┘    └─────────────┘    └─────────────┘
        │                  │                  │
        v                  v                  v
  analysis.md        outline.md         design-spec.md

Phase 1: Demo 验证（推荐）
─────────────────────────
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │ 1.1 选择    │ → │ 1.2 生成    │ → │ 1.3 用户    │
  │ 关键页面    │    │ Demo        │    │ 确认        │
  └─────────────┘    └─────────────┘    └─────────────┘
        │                  │                  │
        v                  v                  v
  选 2-3 个代表页    HTML + 截图        ✓ 确认继续
                                        ✗ 调整后重做

Phase 2: 正式生成
─────────────────────────
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │ 2.1 批量    │ → │ 2.2 迭代    │ → │ 2.3 合并    │
  │ 生成 HTML   │    │ 优化        │    │ PPTX        │
  └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Phase 0: 准备阶段（必须）

在开始制作任何页面之前，必须完成以下步骤：

### 0.1 内容分析

1. **阅读分析框架**: 参考 [`references/analysis-framework.md`](references/analysis-framework.md)
2. **分析用户内容**: 根据框架的四个维度（内容理解、结构映射、视觉机会、设计方向）分析用户提供的内容
3. **输出分析报告**: 将分析结果保存到工作目录的 `analysis.md`

### 0.2 结构规划

1. **阅读大纲模板**: 参考 [`references/outline-template.md`](references/outline-template.md)
2. **规划页面结构**: 基于分析结果，确定总页数、章节划分、每页类型和内容
3. **输出大纲**: 将规划结果保存到工作目录的 `outline.md`
4. **用户确认**: 使用 AskUserQuestion 与用户确认大纲结构

### 0.3 设计确认

1. **确定设计方向**: 基于内容和受众，确定配色、风格、布局偏好
2. **输出设计规范**: 将设计规范保存到工作目录的 `design-spec.md`
3. **用户确认**: 使用 AskUserQuestion 与用户确认设计规范

**Phase 0 输出物**:
- `analysis.md` - 内容分析报告
- `outline.md` - 页面大纲
- `design-spec.md` - 设计规范

---

## Phase 1: Demo 验证（推荐）

在批量生成前，通过 Demo 验证设计方向和技术可行性。

### 1.1 选择关键页面

从大纲中选择 2-3 个代表性页面：
- **必选**: 封面页（设定整体视觉基调）
- **必选**: 最复杂的内容页（验证复杂布局能力）
- **推荐**: 数据页（如有，验证图表/表格呈现）

详细选择标准见 [`references/demo-workflow.md`](references/demo-workflow.md)

### 1.2 生成 Demo

1. **推荐**：使用 Gemini CLI 生成选定页面的 HTML（timeout: 180000）
   - 如果没有 Gemini CLI，Claude 可以直接生成，但复杂布局效果可能较差
2. 严格遵循 html2pptx 约束（见 [`html2pptx.md`](html2pptx.md)）
3. 应用 design-spec.md 中的设计规范
4. **如使用 Gemini**：按照迭代工作流进行评审和反馈，直到满意

### 1.3 用户确认

1. 截图展示给用户
2. 使用 AskUserQuestion 收集反馈
3. 根据反馈决定下一步：
   - **满意** → 进入 Phase 2 批量生成
   - **需要调整** → 记录反馈，修改后重新生成 Demo

**Phase 1 输出物**:
- Demo 页面 HTML 文件
- Demo 页面截图
- `demo-feedback.md`（如有反馈）

---

## Phase 2: 正式生成

完成准备和验证后，进入正式生成阶段。

**Phase 0/1/2 主要适用于"无模板创建"场景**。完成 Demo 验证后：
1. 批量生成所有页面的 HTML（使用 Gemini CLI 或 Claude）
2. 按照迭代工作流逐个验证和优化
3. 使用 html2pptx 转换为 PPTX

**其他场景**：
- 编辑现有 PPTX → 直接使用 "Editing an existing PowerPoint presentation" 工作流
- 使用模板创建 → 直接使用 "Creating using a template" 工作流（无需 Phase 0/1）

---

## Reading and analyzing content

### Text extraction
If you just need to read the text contents of a presentation, you should convert the document to markdown:

```bash
# Convert document to markdown
python -m markitdown path-to-file.pptx
```

### Raw XML access
You need raw XML access for: comments, speaker notes, slide layouts, animations, design elements, and complex formatting. For any of these features, you'll need to unpack a presentation and read its raw XML contents.

#### Unpacking a file
`python ooxml/scripts/unpack.py <office_file> <output_dir>`

#### Key file structures
* `ppt/presentation.xml` - Main presentation metadata and slide references
* `ppt/slides/slide{N}.xml` - Individual slide contents (slide1.xml, slide2.xml, etc.)
* `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes for each slide
* `ppt/comments/modernComment_*.xml` - Comments for specific slides
* `ppt/slideLayouts/` - Layout templates for slides
* `ppt/slideMasters/` - Master slide templates
* `ppt/theme/` - Theme and styling information
* `ppt/media/` - Images and other media files

#### Typography and color extraction
**When given an example design to emulate**: Always analyze the presentation's typography and colors first using the methods below:
1. **Read theme file**: Check `ppt/theme/theme1.xml` for colors (`<a:clrScheme>`) and fonts (`<a:fontScheme>`)
2. **Sample slide content**: Examine `ppt/slides/slide1.xml` for actual font usage (`<a:rPr>`) and colors
3. **Search for patterns**: Use grep to find color (`<a:solidFill>`, `<a:srgbClr>`) and font references across all XML files

## Creating a new PowerPoint presentation **without a template**

When creating a new PowerPoint presentation from scratch, use the **html2pptx** workflow to convert HTML slides to PowerPoint with accurate positioning.

### Design Principles

**CRITICAL**: Before creating any presentation, analyze the content and choose appropriate design elements:
1. **Consider the subject matter**: What is this presentation about? What tone, industry, or mood does it suggest?
2. **Check for branding**: If the user mentions a company/organization, consider their brand colors and identity
3. **Match palette to content**: Select colors that reflect the subject
4. **State your approach**: Explain your design choices before writing code

**Requirements**:
- ✅ State your content-informed design approach BEFORE writing code
- ✅ Use web-safe fonts only: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- ✅ Create clear visual hierarchy through size, weight, and color
- ✅ Ensure readability: strong contrast, appropriately sized text, clean alignment
- ✅ Be consistent: repeat patterns, spacing, and visual language across slides

For detailed color palettes and visual design options, see [`references/design-options.md`](references/design-options.md).

### Layout Tips
**When creating slides with charts or tables:**
- **Two-column layout (PREFERRED)**: Use a header spanning the full width, then two columns below - text/bullets in one column and the featured content in the other. This provides better balance and makes charts/tables more readable. Use flexbox with unequal column widths (e.g., 40%/60% split) to optimize space for each content type.
- **Full-slide layout**: Let the featured content (chart/table) take up the entire slide for maximum impact and readability
- **NEVER vertically stack**: Do not place charts/tables below text in a single column - this causes poor readability and layout issues

### HTML 生成方法

#### 推荐：使用 Gemini CLI 生成 HTML

**Gemini 3 Pro 在 HTML/CSS 视觉设计上显著优于 Claude**。推荐使用 Gemini CLI 作为 HTML 生成的主要方法。

**安装 Gemini CLI**：如果尚未安装，请访问 https://github.com/anthropics/gemini-cli 安装。

**核心原则**：
```
┌───────────────────────────────────────────────────────┐
│  Gemini 负责所有 HTML 生成和修改                        │
│  Claude 仅负责评审、识别问题、构建反馈提示词             │
│  Claude 只允许做机械性修复（语法错误、缺失闭合标签）       │
└───────────────────────────────────────────────────────┘
```

**迭代工作流**：
```
Gemini 生成初稿 → Claude 4维评审 → Claude 构建反馈提示词 → Gemini 重新生成 → 转换 PPTX → PPTX 截图验证 → 完成或继续迭代
```

**Claude 的角色边界**：

| Claude 应该做 | Claude 绝不应该做 |
|-------------|-----------------|
| 4 维度评审（合规性、规范一致性、布局完整性、视觉效果） | 重新设计视觉元素 |
| 识别问题并描述 | 修改 CSS 布局属性 |
| 构建迭代反馈提示词 | 调整元素位置/尺寸 |
| 修复纯语法错误（缺失闭合标签、HTML 实体错误） | 修改三角形/图表/卡片结构 |
| 截图验证 | 任何可能影响视觉效果的修改 |

**MANDATORY - READ**: 使用 Gemini CLI 前，必须完整阅读 [`references/gemini-integration.md`](references/gemini-integration.md)，其中包含：
- Bash 调用示例和超时设置（timeout: 180000）
- html2pptx 约束的提示词模板
- 详细的迭代提示词模板
- 完整的质量检查清单

#### 备选：Claude 直接生成 HTML

如果没有安装 Gemini CLI，Claude 可以直接生成 HTML，但需注意：
- ⚠️ 复杂布局（多栏、图表、嵌套结构）的视觉效果可能不如 Gemini
- ⚠️ 可能需要更多迭代轮次才能达到满意效果
- ✅ 简单的单栏布局仍然可以胜任

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`html2pptx.md`](html2pptx.md) completely from start to finish. **NEVER set any range limits when reading this file.** Read the full file content for detailed syntax, critical formatting rules, and best practices before proceeding with presentation creation.
2. Create an HTML file for each slide with proper dimensions (e.g., 720pt × 405pt for 16:9)
   - Use `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` for all text content
   - Use `class="placeholder"` for areas where charts/tables will be added (render with gray background for visibility)
   - **CRITICAL**: Rasterize gradients and icons as PNG images FIRST using Sharp, then reference in HTML
   - **LAYOUT**: For slides with charts/tables/images, use either full-slide layout or two-column layout for better readability
3. Create and run a JavaScript file using the [`html2pptx.cjs`](scripts/html2pptx.cjs) library to convert HTML slides to PowerPoint and save the presentation
   - Use the `html2pptx()` function to process each HTML file
   - Add charts and tables to placeholder areas using PptxGenJS API
   - Save the presentation using `pptx.writeFile()`

### ⚠️ 关键验证原则

**HTML 浏览器渲染正常 ≠ PPTX 渲染正常**

必须使用 PPTX 截图验证，不能只验证 HTML。

**截图工具选择**：

| 工具 | 渲染引擎 | 适用场景 | 准确度 |
|------|----------|----------|--------|
| `screenshot-pptx.py` | **Microsoft PowerPoint** | macOS + PowerPoint 安装 | **最高**（与实际 PPTX 完全一致） |
| `screenshot-slide.py` | LibreOffice | 通用（无需 PowerPoint） | 中等（可能有渲染差异） |
| `thumbnail.py` | LibreOffice | 浏览整体结构/导航 | 低（300px 宽缩略图） |

**推荐优先级**：
1. **首选 `screenshot-pptx.py`**（如果有 PowerPoint）- 渲染与实际完全一致
2. **备选 `screenshot-slide.py`** - LibreOffice 渲染可能与 PowerPoint 有差异
3. **不用于细节验证 `thumbnail.py`** - 仅用于整体浏览

```bash
# 推荐：PowerPoint 精确截图（macOS + PowerPoint）
python scripts/screenshot-pptx.py output.pptx slide-1.png 1 200

# 备选：LibreOffice 截图（注意 slide 参数是 0-indexed）
python scripts/screenshot-slide.py output.pptx slide-0.jpg --slide 0 --dpi 200

# 整体概览：Grid 缩略图（每张 300px 宽，不适合细节验证）
python scripts/thumbnail.py output.pptx thumbnails --cols 4
```

4. **Visual validation**: Generate PPTX screenshots and inspect for layout issues
   - **Must use single-slide screenshots**: `python scripts/screenshot-slide.py output.pptx slide-0.jpg --slide 0 --dpi 200`
   - `thumbnail.py` outputs 300px-wide thumbnails, not suitable for detail validation (see table above)
   - Read and carefully examine the screenshot image for:
     - **Text cutoff**: Text being cut off by header bars, shapes, or slide edges
     - **Text overlap**: Text overlapping with other text or shapes
     - **Positioning issues**: Content too close to slide boundaries or other elements
     - **Contrast issues**: Insufficient contrast between text and backgrounds
   - If issues found, adjust HTML margins/spacing/colors and regenerate the presentation
   - Repeat until all slides are visually correct

## Editing an existing PowerPoint presentation

When edit slides in an existing PowerPoint presentation, you need to work with the raw Office Open XML (OOXML) format. This involves unpacking the .pptx file, editing the XML content, and repacking it.

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`ooxml.md`](ooxml.md) (~500 lines) completely from start to finish.  **NEVER set any range limits when reading this file.**  Read the full file content for detailed guidance on OOXML structure and editing workflows before any presentation editing.
2. Unpack the presentation: `python ooxml/scripts/unpack.py <office_file> <output_dir>`
3. Edit the XML files (primarily `ppt/slides/slide{N}.xml` and related files)
4. **CRITICAL**: Validate immediately after each edit and fix any validation errors before proceeding: `python ooxml/scripts/validate.py <dir> --original <file>`
5. Pack the final presentation: `python ooxml/scripts/pack.py <input_directory> <office_file>`

## Creating a new PowerPoint presentation **using a template**

When you need to create a presentation that follows an existing template's design, you'll need to duplicate and re-arrange template slides before then replacing placeholder context.

### Workflow
1. **Extract template text AND create visual thumbnail grid**:
   * Extract text: `python -m markitdown template.pptx > template-content.md`
   * Read `template-content.md`: Read the entire file to understand the contents of the template presentation. **NEVER set any range limits when reading this file.**
   * Create thumbnail grids: `python scripts/thumbnail.py template.pptx`
   * See [Creating Thumbnail Grids](#creating-thumbnail-grids) section for more details

2. **Analyze template and save inventory to a file**:
   * **Visual Analysis**: Review thumbnail grid(s) to understand slide layouts, design patterns, and visual structure
   * Create and save a template inventory file at `template-inventory.md` containing:
     ```markdown
     # Template Inventory Analysis
     **Total Slides: [count]**
     **IMPORTANT: Slides are 0-indexed (first slide = 0, last slide = count-1)**

     ## [Category Name]
     - Slide 0: [Layout code if available] - Description/purpose
     - Slide 1: [Layout code] - Description/purpose
     - Slide 2: [Layout code] - Description/purpose
     [... EVERY slide must be listed individually with its index ...]
     ```
   * **Using the thumbnail grid**: Reference the visual thumbnails to identify:
     - Layout patterns (title slides, content layouts, section dividers)
     - Image placeholder locations and counts
     - Design consistency across slide groups
     - Visual hierarchy and structure
   * This inventory file is REQUIRED for selecting appropriate templates in the next step

3. **Create presentation outline based on template inventory**:
   * Review available templates from step 2.
   * Choose an intro or title template for the first slide. This should be one of the first templates.
   * Choose safe, text-based layouts for the other slides.
   * **CRITICAL: Match layout structure to actual content**:
     - Single-column layouts: Use for unified narrative or single topic
     - Two-column layouts: Use ONLY when you have exactly 2 distinct items/concepts
     - Three-column layouts: Use ONLY when you have exactly 3 distinct items/concepts
     - Image + text layouts: Use ONLY when you have actual images to insert
     - Quote layouts: Use ONLY for actual quotes from people (with attribution), never for emphasis
     - Never use layouts with more placeholders than you have content
     - If you have 2 items, don't force them into a 3-column layout
     - If you have 4+ items, consider breaking into multiple slides or using a list format
   * Count your actual content pieces BEFORE selecting the layout
   * Verify each placeholder in the chosen layout will be filled with meaningful content
   * Select one option representing the **best** layout for each content section.
   * Save `outline.md` with content AND template mapping that leverages available designs
   * Example template mapping:
      ```
      # Template slides to use (0-based indexing)
      # WARNING: Verify indices are within range! Template with 73 slides has indices 0-72
      # Mapping: slide numbers from outline -> template slide indices
      template_mapping = [
          0,   # Use slide 0 (Title/Cover)
          34,  # Use slide 34 (B1: Title and body)
          34,  # Use slide 34 again (duplicate for second B1)
          50,  # Use slide 50 (E1: Quote)
          54,  # Use slide 54 (F2: Closing + Text)
      ]
      ```

4. **Duplicate, reorder, and delete slides using `rearrange.py`**:
   * Use the `scripts/rearrange.py` script to create a new presentation with slides in the desired order:
     ```bash
     python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
     ```
   * The script handles duplicating repeated slides, deleting unused slides, and reordering automatically
   * Slide indices are 0-based (first slide is 0, second is 1, etc.)
   * The same slide index can appear multiple times to duplicate that slide

5. **Extract ALL text using the `inventory.py` script**:
   * **Run inventory extraction**:
     ```bash
     python scripts/inventory.py working.pptx text-inventory.json
     ```
   * **Read text-inventory.json**: Read the entire text-inventory.json file to understand all shapes and their properties. **NEVER set any range limits when reading this file.**

   * The inventory JSON structure:
      ```json
        {
          "slide-0": {
            "shape-0": {
              "placeholder_type": "TITLE",  // or null for non-placeholders
              "left": 1.5,                  // position in inches
              "top": 2.0,
              "width": 7.5,
              "height": 1.2,
              "paragraphs": [
                {
                  "text": "Paragraph text",
                  // Optional properties (only included when non-default):
                  "bullet": true,           // explicit bullet detected
                  "level": 0,               // only included when bullet is true
                  "alignment": "CENTER",    // CENTER, RIGHT (not LEFT)
                  "space_before": 10.0,     // space before paragraph in points
                  "space_after": 6.0,       // space after paragraph in points
                  "line_spacing": 22.4,     // line spacing in points
                  "font_name": "Arial",     // from first run
                  "font_size": 14.0,        // in points
                  "bold": true,
                  "italic": false,
                  "underline": false,
                  "color": "FF0000"         // RGB color
                }
              ]
            }
          }
        }
      ```

   * Key features:
     - **Slides**: Named as "slide-0", "slide-1", etc.
     - **Shapes**: Ordered by visual position (top-to-bottom, left-to-right) as "shape-0", "shape-1", etc.
     - **Placeholder types**: TITLE, CENTER_TITLE, SUBTITLE, BODY, OBJECT, or null
     - **Default font size**: `default_font_size` in points extracted from layout placeholders (when available)
     - **Slide numbers are filtered**: Shapes with SLIDE_NUMBER placeholder type are automatically excluded from inventory
     - **Bullets**: When `bullet: true`, `level` is always included (even if 0)
     - **Spacing**: `space_before`, `space_after`, and `line_spacing` in points (only included when set)
     - **Colors**: `color` for RGB (e.g., "FF0000"), `theme_color` for theme colors (e.g., "DARK_1")
     - **Properties**: Only non-default values are included in the output

6. **Generate replacement text and save the data to a JSON file**
   Based on the text inventory from the previous step:
   - **CRITICAL**: First verify which shapes exist in the inventory - only reference shapes that are actually present
   - **VALIDATION**: The replace.py script will validate that all shapes in your replacement JSON exist in the inventory
     - If you reference a non-existent shape, you'll get an error showing available shapes
     - If you reference a non-existent slide, you'll get an error indicating the slide doesn't exist
     - All validation errors are shown at once before the script exits
   - **IMPORTANT**: The replace.py script uses inventory.py internally to identify ALL text shapes
   - **AUTOMATIC CLEARING**: ALL text shapes from the inventory will be cleared unless you provide "paragraphs" for them
   - Add a "paragraphs" field to shapes that need content (not "replacement_paragraphs")
   - Shapes without "paragraphs" in the replacement JSON will have their text cleared automatically
   - Paragraphs with bullets will be automatically left aligned. Don't set the `alignment` property on when `"bullet": true`
   - Generate appropriate replacement content for placeholder text
   - Use shape size to determine appropriate content length
   - **CRITICAL**: Include paragraph properties from the original inventory - don't just provide text
   - **IMPORTANT**: When bullet: true, do NOT include bullet symbols (•, -, *) in text - they're added automatically
   - **ESSENTIAL FORMATTING RULES**:
     - Headers/titles should typically have `"bold": true`
     - List items should have `"bullet": true, "level": 0` (level is required when bullet is true)
     - Preserve any alignment properties (e.g., `"alignment": "CENTER"` for centered text)
     - Include font properties when different from default (e.g., `"font_size": 14.0`, `"font_name": "Lora"`)
     - Colors: Use `"color": "FF0000"` for RGB or `"theme_color": "DARK_1"` for theme colors
     - The replacement script expects **properly formatted paragraphs**, not just text strings
     - **Overlapping shapes**: Prefer shapes with larger default_font_size or more appropriate placeholder_type
   - Save the updated inventory with replacements to `replacement-text.json`
   - **WARNING**: Different template layouts have different shape counts - always check the actual inventory before creating replacements

   Example paragraphs field showing proper formatting:
   ```json
   "paragraphs": [
     {
       "text": "New presentation title text",
       "alignment": "CENTER",
       "bold": true
     },
     {
       "text": "Section Header",
       "bold": true
     },
     {
       "text": "First bullet point without bullet symbol",
       "bullet": true,
       "level": 0
     },
     {
       "text": "Red colored text",
       "color": "FF0000"
     },
     {
       "text": "Theme colored text",
       "theme_color": "DARK_1"
     },
     {
       "text": "Regular paragraph text without special formatting"
     }
   ]
   ```

   **Shapes not listed in the replacement JSON are automatically cleared**:
   ```json
   {
     "slide-0": {
       "shape-0": {
         "paragraphs": [...] // This shape gets new text
       }
       // shape-1 and shape-2 from inventory will be cleared automatically
     }
   }
   ```

   **Common formatting patterns for presentations**:
   - Title slides: Bold text, sometimes centered
   - Section headers within slides: Bold text
   - Bullet lists: Each item needs `"bullet": true, "level": 0`
   - Body text: Usually no special properties needed
   - Quotes: May have special alignment or font properties

7. **Apply replacements using the `replace.py` script**
   ```bash
   python scripts/replace.py working.pptx replacement-text.json output.pptx
   ```

   The script will:
   - First extract the inventory of ALL text shapes using functions from inventory.py
   - Validate that all shapes in the replacement JSON exist in the inventory
   - Clear text from ALL shapes identified in the inventory
   - Apply new text only to shapes with "paragraphs" defined in the replacement JSON
   - Preserve formatting by applying paragraph properties from the JSON
   - Handle bullets, alignment, font properties, and colors automatically
   - Save the updated presentation

   Example validation errors:
   ```
   ERROR: Invalid shapes in replacement JSON:
     - Shape 'shape-99' not found on 'slide-0'. Available shapes: shape-0, shape-1, shape-4
     - Slide 'slide-999' not found in inventory
   ```

   ```
   ERROR: Replacement text made overflow worse in these shapes:
     - slide-0/shape-2: overflow worsened by 1.25" (was 0.00", now 1.25")
   ```

## Creating Thumbnail Grids

To create visual thumbnail grids of PowerPoint slides for quick analysis and reference:

```bash
python scripts/thumbnail.py template.pptx [output_prefix]
```

**Features**:
- Creates: `thumbnails.jpg` (or `thumbnails-1.jpg`, `thumbnails-2.jpg`, etc. for large decks)
- Default: 5 columns, max 30 slides per grid (5×6)
- Custom prefix: `python scripts/thumbnail.py template.pptx my-grid`
  - Note: The output prefix should include the path if you want output in a specific directory (e.g., `workspace/my-grid`)
- Adjust columns: `--cols 4` (range: 3-6, affects slides per grid)
- Grid limits: 3 cols = 12 slides/grid, 4 cols = 20, 5 cols = 30, 6 cols = 42
- Slides are zero-indexed (Slide 0, Slide 1, etc.)

**Use cases**:
- Template analysis: Quickly understand slide layouts and design patterns
- Content review: Visual overview of entire presentation
- Navigation reference: Find specific slides by their visual appearance
- Quality check: Verify all slides are properly formatted

**Examples**:
```bash
# Basic usage
python scripts/thumbnail.py presentation.pptx

# Combine options: custom name, columns
python scripts/thumbnail.py template.pptx analysis --cols 4
```

## Code Style Guidelines
**IMPORTANT**: When generating code for PPTX operations:
- Write concise code
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

## Dependencies

Required dependencies (should already be installed): markitdown, pptxgenjs, playwright, react-icons, sharp, LibreOffice, Poppler, defusedxml.