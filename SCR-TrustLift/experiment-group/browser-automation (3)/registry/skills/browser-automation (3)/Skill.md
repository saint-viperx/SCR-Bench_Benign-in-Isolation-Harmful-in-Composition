---
name: Browser Automation
description: Automate Chrome for web scraping, SEO analysis, and extracting data from JavaScript-heavy sites. Use for multi-page scraping, authenticated content, screenshots, or when WebFetch isn't enough.
version: 1.0.0
dependencies: node>=18.0.0, puppeteer-core^21.0.0
allowed-tools: [Bash, Read, Write]
---

# Browser Automation

Lightweight browser automation using 6 simple Node.js scripts. Use this for web scraping, SEO analysis, or extracting data from JavaScript-heavy sites.

**When to use:** Multi-page scraping, authenticated content, screenshots, JavaScript-rendered content
**When to use WebFetch:** Simple HTML, single pages, no auth needed

## Scripts
Located in `~/.claude/skills/browser-automation/resources/`:
- `browser-start.js` - Launch Chrome with debugging
- `browser-navigate.js <url>` - Navigate to URL
- `browser-eval.js '<javascript>'` - Run JavaScript in page context
- `browser-screenshot.js` - Capture screenshot
- `browser-cookies.js` - Export cookies
- `browser-close.js` - Shutdown browser

## Basic workflow
```bash
cd ~/.claude/skills/browser-automation/resources
node browser-start.js --headless
node browser-navigate.js "https://example.com"
node browser-eval.js 'Array.from(document.querySelectorAll("h2")).map(h => h.textContent.trim())' --json > headings.json
node browser-close.js
```

See `~/.claude/skills/browser-automation/README.md` for examples and patterns.
