# import-notion

Import Notion workspace pages to local markdown files.

## Setup

### 1. Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Create a new integration for your workspace
3. Copy the API key (starts with `secret_`)

### 2. Share Pages with Integration

In Notion, for each page you want to export:
1. Click "..." menu → "Add connections"
2. Select your integration

### 3. Configure API Key

Add to `~/.claude/.env`:
```
NOTION_API_KEY_MYPROJECT=secret_xxx
```

### 4. Create Config

**Option A: Global config** (recommended for multiple workspaces)

Create `~/.claude/notion-exporter.config.json`:
```json
{
  "spaces": {
    "myproject": {
      "targetPath": "~/path/to/project",
      "rawExportPath": "data/notion/_exports",
      "outputPath": "data/notion",
      "apiKeyEnvVar": "NOTION_API_KEY_MYPROJECT",
      "excludePatterns": []
    }
  }
}
```

**Option B: Project-local config**

Create `.entourage/notion.config.json` in your project:
```json
{
  "apiKeyEnvVar": "NOTION_API_KEY_MYPROJECT",
  "targetPath": ".",
  "rawExportPath": "data/notion/_exports",
  "outputPath": "data/notion",
  "excludePatterns": []
}
```

## Usage

```
/import-notion
```

Or with a specific space:
```
/import-notion myproject
```

## How It Works

1. **Export**: Fetches all shared pages via Notion API → `_exports/{date}/export.json`
2. **Convert**: Transforms JSON to clean markdown → `{outputPath}/*.md`
3. **Assets**: Downloads images and files → `_assets/`

## Output Structure

```
data/notion/
├── _exports/2026-01-15/export.json
├── _assets/
│   ├── logo.png
│   └── diagram.svg
├── Product/
│   ├── Roadmap.md
│   └── Features/
│       └── Feature-A.md
└── Team/
    └── Meeting-Notes.md
```

- Folder structure mirrors Notion hierarchy
- Database entries nest under their parent pages
- Frontmatter includes `notion_url` for source links

## Dependencies

- Python 3.8+
- notion-client>=2.0.0
- python-dotenv>=1.0.0
- httpx>=0.24.0
