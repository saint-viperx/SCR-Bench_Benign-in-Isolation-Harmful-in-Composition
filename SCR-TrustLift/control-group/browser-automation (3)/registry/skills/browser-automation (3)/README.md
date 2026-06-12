# Browser Automation Tools

Minimal browser automation scripts for Claude agents. Achieves 60x better token efficiency than MCP servers while maintaining full functionality for web scraping, SEO analysis, and competitive research.

## Installation

First-time setup (automated by Claude):

```bash
mkdir -p ~/agent-tools/browser/screenshots
cp templates/* ~/agent-tools/browser/
cd ~/agent-tools/browser
npm install
chmod +x *.js
```

## Quick Start

```bash
# Start browser
node ~/agent-tools/browser/browser-start.js --headless

# Navigate to a page
node ~/agent-tools/browser/browser-navigate.js "https://example.com"

# Extract data with JavaScript
node ~/agent-tools/browser/browser-eval.js 'document.title' --json

# Take screenshot
node ~/agent-tools/browser/browser-screenshot.js

# Close browser
node ~/agent-tools/browser/browser-close.js
```

## Script Reference

### browser-start.js

Launch Chrome with remote debugging enabled.

**Flags:**
- `--profile` - Load user's Chrome profile for authentication
- `--headless` - Run in headless mode
- `--port=9222` - Remote debugging port (default: 9222)

**Examples:**
```bash
# Headless mode
node browser-start.js --headless

# With user profile (for authenticated sessions)
node browser-start.js --profile

# Custom port
node browser-start.js --port=9223
```

### browser-navigate.js

Navigate to a URL in the browser.

**Arguments:**
- `<url>` - Target URL (required)

**Flags:**
- `--new-tab` - Open in new tab vs current
- `--wait-for=selector` - CSS selector to wait for
- `--timeout=30000` - Navigation timeout in ms

**Examples:**
```bash
# Navigate to URL
node browser-navigate.js "https://example.com"

# Open in new tab
node browser-navigate.js "https://example.com" --new-tab

# Wait for specific element
node browser-navigate.js "https://example.com" --wait-for=".content"
```

### browser-eval.js

Execute JavaScript in the browser page context.

**Arguments:**
- `<code>` - JavaScript to execute (or `-` for stdin)

**Flags:**
- `--async` - Treat as async function
- `--json` - Format result as JSON only (no wrapper)
- `--timeout=30000` - Execution timeout in ms

**Examples:**
```bash
# Get page title
node browser-eval.js 'document.title' --json

# Extract all headings
node browser-eval.js 'Array.from(document.querySelectorAll("h2")).map(h => h.textContent.trim())' --json

# Read code from file
cat extract.js | node browser-eval.js - --json

# Async JavaScript
node browser-eval.js 'await fetch("/api/data").then(r => r.json())' --async --json
```

### browser-screenshot.js

Capture page screenshot.

**Flags:**
- `--output=filename.png` - Custom filename (default: timestamped)
- `--fullpage` - Full page vs viewport only
- `--element=selector` - CSS selector to screenshot specific element

**Examples:**
```bash
# Screenshot viewport
node browser-screenshot.js

# Full page screenshot
node browser-screenshot.js --fullpage

# Screenshot specific element
node browser-screenshot.js --element=".hero-section"

# Custom filename
node browser-screenshot.js --output=homepage.png
```

Screenshots are saved to `~/agent-tools/browser/screenshots/`

### browser-cookies.js

Extract cookies from browser session.

**Flags:**
- `--domain=example.com` - Filter by domain
- `--format=json` - Output format (json, netscape, header)
- `--output=cookies.txt` - Save to file vs stdout

**Examples:**
```bash
# Get all cookies as JSON
node browser-cookies.js --format=json

# Get cookies for specific domain
node browser-cookies.js --domain=example.com --format=json

# Export for curl/wget
node browser-cookies.js --format=netscape --output=cookies.txt

# Get as Cookie header
node browser-cookies.js --format=header
```

### browser-close.js

Gracefully shutdown browser instance.

**Flags:**
- `--force` - Kill process if graceful shutdown fails

**Examples:**
```bash
# Normal shutdown
node browser-close.js

# Force kill
node browser-close.js --force
```

## Common JavaScript Patterns

### Extract Meta Tags

```javascript
Array.from(document.querySelectorAll('meta')).reduce((acc, meta) => {
  const name = meta.name || meta.property;
  if (name) acc[name] = meta.content;
  return acc;
}, {})
```

### Extract Schema Markup

```javascript
Array.from(document.querySelectorAll('script[type="application/ld+json"]'))
  .map(s => JSON.parse(s.textContent))
```

### Extract All Links

```javascript
Array.from(document.querySelectorAll('a')).map(a => ({
  text: a.textContent.trim(),
  href: a.href,
  isExternal: !a.href.startsWith(window.location.origin)
}))
```

### Extract Heading Hierarchy

```javascript
['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].reduce((acc, tag) => {
  acc[tag] = Array.from(document.querySelectorAll(tag))
    .map(h => h.textContent.trim());
  return acc;
}, {})
```

### Check Image Alt Tags

```javascript
Array.from(document.querySelectorAll('img')).map(img => ({
  src: img.src,
  alt: img.alt,
  hasAlt: !!img.alt
}))
```

### Extract Internal Links

```javascript
Array.from(document.querySelectorAll('a[href^="/"], a[href^="' + window.location.origin + '"]'))
  .map(a => ({
    text: a.textContent.trim(),
    href: a.href
  }))
```

## Workflow Examples

### SEO Analysis

```bash
# Start browser
node browser-start.js --headless

# Navigate to site
node browser-navigate.js "https://example.com"

# Extract meta tags
node browser-eval.js 'Array.from(document.querySelectorAll("meta")).reduce((acc, meta) => {
  const name = meta.name || meta.property;
  if (name) acc[name] = meta.content;
  return acc;
}, {})' --json > meta-tags.json

# Extract schema markup
node browser-eval.js 'Array.from(document.querySelectorAll("script[type=\"application/ld+json\"]")).map(s => JSON.parse(s.textContent))' --json > schema.json

# Extract headings
node browser-eval.js '["h1", "h2", "h3", "h4", "h5", "h6"].reduce((acc, tag) => {
  acc[tag] = Array.from(document.querySelectorAll(tag)).map(h => h.textContent.trim());
  return acc;
}, {})' --json > headings.json

# Take screenshot
node browser-screenshot.js --fullpage --output=fullpage.png

# Close browser
node browser-close.js
```

### Multi-Page Scraping

```bash
# Start browser
node browser-start.js --headless

# Loop through URLs
for url in $(cat urls.txt); do
  node browser-navigate.js "$url"
  node browser-eval.js 'document.title' --json >> titles.txt
done

# Close browser
node browser-close.js
```

### Authenticated Scraping

```bash
# Start with user profile
node browser-start.js --profile

# Navigate to authenticated page (will use existing session)
node browser-navigate.js "https://example.com/dashboard"

# Extract data
node browser-eval.js 'document.querySelector(".user-data").textContent' --json

# Export cookies for other tools
node browser-cookies.js --format=netscape --output=cookies.txt

# Close browser
node browser-close.js
```

## Troubleshooting

### Browser won't start

**Error:** `Could not find Chrome executable`

**Solution:** Make sure Chrome is installed in the standard location:
- macOS: `/Applications/Google Chrome.app`
- Linux: `/usr/bin/google-chrome` or `/usr/bin/chromium`
- Windows: `C:\Program Files\Google\Chrome\Application\chrome.exe`

### Connection refused

**Error:** `Cannot find browser`

**Solution:** Start the browser first with `browser-start.js`

### Timeout errors

**Error:** `Navigation timeout`

**Solution:** Increase timeout with `--timeout=60000` flag

### No active page

**Error:** `No active page found`

**Solution:** Navigate to a URL first with `browser-navigate.js`

## Design Philosophy

This tool is built on the principle that Claude agents don't need specialized MCP protocols. Instead:

1. **Claude already knows JavaScript** - No need to learn specialized tool vocabulary
2. **File-based composability** - Results saved to files, easy to pipe and process
3. **Simple is better** - 6 focused scripts vs monolithic MCP server
4. **Users can customize** - Scripts are just files, easy to modify
5. **Minimal context overhead** - 54x more efficient than Playwright MCP

Inspired by Mario Zechner's article: "What if you don't need MCP?"
https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/

## Token Efficiency

- **Skill context:** ~250 tokens (skill.md + usage)
- **Playwright MCP:** 13,700 tokens
- **Efficiency gain:** 54x improvement

This documentation is external and NOT loaded into Claude's context. Only `skill.md` is loaded, keeping context usage minimal.

## License

MIT - Use freely, modify as needed
