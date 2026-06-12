---
name: import-notion
description: Import pages from Notion workspace to local markdown files
---

# Import Notion

Export and convert Notion workspace pages to local markdown files for use in context repositories.

## When to Use

- After making changes in Notion that should be synced locally
- When setting up a new context repository with Notion data
- Periodically to keep local copies in sync

## Configuration

Supports two config locations (checked in order):

### Option 1: Global config (recommended for multiple workspaces)

`~/.claude/notion-exporter.config.json`:
```json
{
  "spaces": {
    "viran": {
      "targetPath": "~/Documents/code/@orgs/viranhq/viran-context",
      "rawExportPath": "temp/notion-raw",
      "outputPath": "data/documents/notion",
      "apiKeyEnvVar": "NOTION_API_KEY_VIRAN",
      "excludePatterns": ["^Archived", "^Trash"]
    },
    "entourage": {
      "targetPath": "~/Documents/code/@orgs/my-entourage/entourage-context",
      "rawExportPath": "temp/notion-raw",
      "outputPath": "data/documents/notion",
      "apiKeyEnvVar": "NOTION_API_KEY_ENTOURAGE"
    }
  }
}
```

### Option 2: Project-local config

`.entourage/notion.config.json`:
```json
{
  "apiKeyEnvVar": "NOTION_API_KEY_PROJECTNAME",
  "targetPath": ".",
  "rawExportPath": "temp/notion-raw",
  "outputPath": "data/documents/notion",
  "excludePatterns": ["Archive", "Template"]
}
```

API keys are stored in `~/.claude/.env`:
```
NOTION_API_KEY_VIRAN=secret_xxx
NOTION_API_KEY_ENTOURAGE=secret_xxx
```

## Prerequisites

1. **Notion Integration**: Create at https://www.notion.so/my-integrations
   - One integration per workspace
   - Share specific pages with the integration

2. **Python Environment**: The skill will set up a venv on first run

## Workflow

### Step 1: Check Configuration

1. Check for `~/.claude/notion-exporter.config.json` (global)
2. If not found, check `.entourage/notion.config.json` (project-local)
3. If neither found, guide user through setup wizard

### Step 2: Setup Python Environment

1. Check if venv exists at `~/.claude/venvs/notion-exporter/`
2. If not, create and install dependencies:
   ```bash
   python3 -m venv ~/.claude/venvs/notion-exporter
   ~/.claude/venvs/notion-exporter/bin/pip install -r {skill_dir}/scripts/requirements.txt
   ```

### Step 3: Export from Notion

Run the exporter:
```bash
~/.claude/venvs/notion-exporter/bin/python {skill_dir}/scripts/exporter.py [space-name]
```

Output: `{rawExportPath}/{date}/export.json`

### Step 4: Convert to Markdown

Run the converter:
```bash
~/.claude/venvs/notion-exporter/bin/python {skill_dir}/scripts/converter.py [space-name]
```

Output:
- `{outputPath}/*.md` - Markdown files following Notion hierarchy
- `{outputPath}/_assets/` - Downloaded images and files

### Step 5: Report Results

```markdown
## Import Complete

Exported from Notion:
- Pages: 42
- Databases: 3
- Assets: 15

Converted to Markdown:
- Files created: 45
- Assets downloaded: 15
- Location: data/documents/notion/

Run `/update-timeline` to process these files.
```

## Output Structure

```
data/documents/notion/
├── _assets/
│   ├── logo.png
│   └── diagram.svg
├── Product/
│   ├── Roadmap.md
│   └── Features/
│       └── Feature-A.md
└── Team/
    └── Meeting-Notes.md

temp/notion-raw/
└── 2026-01-15/
    └── export.json          # Raw API response (not tracked in git)
```

- Folder structure mirrors Notion hierarchy
- Database entries nest under their Notion parent pages
- Assets stored in `_assets/` with local path references in frontmatter

## Error Handling

- **No config**: Guide through setup wizard
- **Invalid API key**: Report authentication error with link to Notion integrations
- **Rate limited**: Report and suggest waiting
- **Python not found**: Report requirement for Python 3.8+

## Execution Behavior

This skill returns results to the calling context and does NOT stop execution.
