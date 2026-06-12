# PPTX Skill for Claude Code

A comprehensive Claude Code skill for creating, editing, and analyzing PowerPoint presentations (.pptx files).

## Features

- **Create presentations from scratch** using HTML → PPTX conversion workflow
- **Edit existing presentations** via OOXML manipulation
- **Create presentations from templates** with text replacement
- **Gemini CLI integration** for superior HTML/CSS visual generation
- **Full analysis capabilities** including text extraction and visual thumbnails

## Quick Installation

### One-line Terminal Setup

```bash
# Clone directly to Claude Code skills directory
git clone https://github.com/0xZoharHuang/pptx-skill-cc-gemini-.git ~/.claude/skills/pptx
```

### Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/0xZoharHuang/pptx-skill-cc-gemini-.git

# 2. Copy to Claude Code skills directory
cp -r pptx-skill-cc-gemini- ~/.claude/skills/pptx
```

### Verify Installation

```bash
ls ~/.claude/skills/pptx/SKILL.md
# Should output: /Users/<username>/.claude/skills/pptx/SKILL.md
```

## Dependencies

Install required dependencies before using this skill:

```bash
# Python dependencies
pip install markitdown defusedxml

# Node.js dependencies (for html2pptx)
npm install -g pptxgenjs playwright sharp react-icons

# System dependencies (macOS)
brew install libreoffice poppler
```

## Usage

After installation, invoke the skill in Claude Code:

```
/pptx
```

Or ask Claude to help with PowerPoint tasks:
- "Create a presentation about AI trends"
- "Edit slide 3 of my presentation.pptx"
- "Extract text from this PowerPoint file"

## Directory Structure

```
pptx/
├── SKILL.md                 # Main skill instructions
├── html2pptx.md             # HTML to PPTX conversion guide
├── ooxml.md                 # Office Open XML editing guide
├── scripts/
│   ├── html2pptx.cjs        # HTML → PPTX converter
│   ├── html2pptx.mjs        # ES module version
│   ├── inventory.py         # Extract text shapes from PPTX
│   ├── replace.py           # Batch replace text content
│   ├── rearrange.py         # Reorder/duplicate slides
│   ├── thumbnail.py         # Generate thumbnail grids
│   └── screenshot-slide.py  # Single slide screenshots
├── ooxml/
│   ├── scripts/
│   │   ├── pack.py          # Pack directory → PPTX
│   │   ├── unpack.py        # Unpack PPTX → directory
│   │   └── validate.py      # Validate OOXML structure
│   └── schemas/             # XML validation schemas
└── references/
    ├── analysis-framework.md
    ├── demo-workflow.md
    ├── design-options.md
    ├── gemini-integration.md
    └── outline-template.md
```

## Workflow Overview

### Creating New Presentations (Without Template)

```
Phase 0: Preparation (Required)
├── Content analysis → analysis.md
├── Structure planning → outline.md
└── Design confirmation → design-spec.md

Phase 1: Demo Validation (Recommended)
├── Select 2-3 key slides
├── Generate demo HTML + screenshots
└── User confirmation

Phase 2: Formal Generation
├── Batch generate all HTML slides
├── Iterative optimization
└── Merge to PPTX
```

### Creating from Template

1. Extract template text and create thumbnails
2. Analyze and create template inventory
3. Create outline with template mapping
4. Rearrange slides using `rearrange.py`
5. Extract text inventory using `inventory.py`
6. Generate replacement JSON
7. Apply replacements using `replace.py`

### Editing Existing Presentations

1. Unpack PPTX: `python ooxml/scripts/unpack.py file.pptx output_dir`
2. Edit XML files in `ppt/slides/`
3. Validate: `python ooxml/scripts/validate.py output_dir --original file.pptx`
4. Pack: `python ooxml/scripts/pack.py output_dir new_file.pptx`

## Key Scripts

| Script | Purpose |
|--------|---------|
| `html2pptx.cjs` | Convert HTML slides to PowerPoint |
| `screenshot-slide.py` | Full-size single slide screenshot (for validation) |
| `thumbnail.py` | Generate thumbnail grid (for overview) |
| `inventory.py` | Extract all text shapes from PPTX |
| `replace.py` | Batch replace text content |
| `rearrange.py` | Duplicate/reorder/delete slides |

## Gemini CLI Integration (Recommended)

This skill recommends using [Gemini CLI](https://github.com/google-gemini/gemini-cli) for HTML generation as Gemini 3 Pro produces superior visual designs compared to Claude for HTML/CSS tasks.

See `references/gemini-integration.md` for detailed integration guide.

## Troubleshooting

### Skill not found

Ensure the skill is in the correct directory:
```bash
ls ~/.claude/skills/pptx/SKILL.md
```

### Dependencies missing

Check all dependencies are installed:
```bash
python -c "import markitdown; import defusedxml; print('Python deps OK')"
node -e "require('pptxgenjs'); console.log('Node deps OK')"
```

### Permission issues

Ensure scripts are executable:
```bash
chmod +x ~/.claude/skills/pptx/scripts/*.py
chmod +x ~/.claude/skills/pptx/ooxml/scripts/*.py
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
