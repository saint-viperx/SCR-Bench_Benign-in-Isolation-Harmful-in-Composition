---
name: stealth-search
description: >-
  Search paywalled and protected sites (LinkedIn, WSJ, news sites) using stealth
  browser techniques when WebFetch fails. Use when (1) WebFetch blocks or cannot
  access a site, (2) Searching LinkedIn profiles or professional networks, (3)
  Searching paywalled news sites (WSJ, NYT, FT), (4) Need to avoid bot detection
  for legitimate research, (5) Extracting metadata from search results when full
  content is behind authentication. Provides DuckDuckGo and stealth Google
  search with Chromium browser automation.
metadata:
  category: research
  icon: "\U0001F50D"
  created: '2026-02-03'
  starred: true
created: '2026-02-03'
starred: true
---

# 🔍 Stealth Search

Search paywalled and protected sites when WebFetch cannot access them. Uses Chromium browser with stealth configuration to search DuckDuckGo, Google, and Bing without triggering bot detection.

## Quick Start

### Setup (First Time)

```bash
# Create virtual environment
cd /home/sasha/projects/[your-project]
python3 -m venv stealth-env
source stealth-env/bin/activate
pip install selenium
```

### Basic Usage

```bash
source stealth-env/bin/activate

# Search LinkedIn profiles (DuckDuckGo recommended)
python scripts/stealth_search.py "Jason Bergman LinkedIn FragilePack"

# Search WSJ articles
python scripts/stealth_search.py "site:wsj.com 'artificial intelligence' regulation"

# Save results and screenshot
python scripts/stealth_search.py "query" --output results.json --screenshot search.png
```

## Search Engine Selection

| Engine | Best For | Detection Risk | Speed |
|--------|----------|----------------|-------|
| **DuckDuckGo** | LinkedIn, most sites | ✅ Low | Fast |
| **Google** | Comprehensive results | ⚠️ Medium | Fast |
| **Bing** | News sites | ✅ Low | Medium |

**Default**: DuckDuckGo (lowest bot detection)
**Fallback**: Try `--engine all` for maximum coverage

## Common Tasks

### Task 1: Find LinkedIn Profile

```bash
# 1. Search for profiles
python scripts/stealth_search.py "Sarah Chen 'Chief Data Officer' Boston" --output results.json

# 2. Extract profile details
python scripts/linkedin_profile.py "https://www.linkedin.com/in/username" \
  --screenshot profile.png --output profile.json
```

**What You Get**:
- Profile URLs, name, title, location from search snippets
- Connection count
- Page screenshots

**Requires Login**: Full work history, education, skills

### Task 2: Search Paywalled News

```bash
# Find WSJ/FT articles
python scripts/stealth_search.py "site:wsj.com OR site:ft.com 'Company Name' merger"
```

**What You Get**: Article titles, dates, authors, brief snippets
**Full Access**: Requires subscription or library

### Task 3: Multi-Engine Search

```bash
# Try all engines for comprehensive results
python scripts/stealth_search.py "query" --engine all --max-results 20
```

## Script Reference

### stealth_search.py

Main search with stealth browser configuration.

**Arguments**:
- `query` - Search query (required)
- `--engine` - duckduckgo (default) | google | bing | all
- `--max-results` - Maximum results (default: 10)
- `--output` - Save JSON to file
- `--screenshot` - Capture screenshot path

**Output**:
```json
{
  "query": "search terms",
  "timestamp": "2026-02-03 10:30:00",
  "results": [
    {
      "source": "DuckDuckGo",
      "position": 1,
      "title": "Article Title",
      "url": "https://example.com/article",
      "snippet": "Description..."
    }
  ]
}
```

### linkedin_profile.py

Extract publicly available LinkedIn information.

**Arguments**:
- `url` - LinkedIn profile URL (required)
- `--output` - Save JSON to file
- `--screenshot` - Capture screenshot path

## Site-Specific Strategies

For detailed guidance on LinkedIn, WSJ, and other sites, see **[references/site-specific-guide.md](references/site-specific-guide.md)**.

**Key Points**:
- **LinkedIn**: DuckDuckGo best, search snippets contain key info
- **WSJ**: Get metadata from search, need subscription for full text
- **Professional Networks**: Most require auth, extract from search results
- **Public Sites**: Any engine works

## Stealth Configuration

Scripts use these techniques to avoid detection:

```python
--headless=new                           # New headless mode
--disable-blink-features=AutomationControlled
excludeSwitches: ["enable-automation"]   # Remove automation flags
Custom user agent                        # Realistic browser fingerprint
Remove webdriver property                # Hide Selenium
```

**Note**: DuckDuckGo has lowest detection rate. Google may still detect automation.

## Workflow Patterns

### Research Person's Background

1. Search DuckDuckGo: `"{name}" LinkedIn {company}`
2. Extract profile URLs from results
3. Visit profiles for verification
4. Capture screenshots
5. Note: Deep details require login

### Find Company Coverage

1. Search: `site:wsj.com OR site:bloomberg.com "{Company}"`
2. Extract titles and dates
3. Assess relevance
4. Access full articles via subscription

### Verify Executive Info

1. Search LinkedIn with name + company
2. Review snippets
3. Visit profile URL if public
4. Cross-reference sources
5. Document with screenshots

## Limitations

### Cannot Do:
❌ Bypass paywalls - Full content needs subscription
❌ Access authenticated content - Login-required data not available
❌ Mass scraping - Individual lookups only
❌ Circumvent legal restrictions - Legitimate research only

### Expected Behaviors:
✅ Some sites require login - Extract from search results
✅ Limited profile data - Full LinkedIn history needs auth
✅ Occasional detection - Google may block; use DuckDuckGo
✅ Slower than WebFetch - Browser overhead

## Ethical Guidelines

**Appropriate**:
- Business intelligence
- Hiring verification
- Competitive analysis
- News monitoring
- Public information gathering

**Not Appropriate**:
- Bypassing authentication
- Mass scraping protected content
- Violating terms of service
- Unauthorized data collection

**Best Practices**:
- Respect rate limits (1-3 sec delays)
- Only collect public information
- Follow site ToS
- Use for legitimate purposes
- Document sources

## Troubleshooting

### "Automation Detected"
**Solution**: Use DuckDuckGo (lower detection), increase delays

### "Login Required"
**Expected**: Extract metadata from search results instead

### No Results Found
**Check**: Query syntax, site domain, try different engine

### Browser Errors
- Install Chromium: `apt-get install chromium-browser`
- Install Selenium: `pip install selenium`
- Activate venv: `source stealth-env/bin/activate`

## Examples

```bash
# LinkedIn search
python scripts/stealth_search.py "Jane Doe LinkedIn 'VP Engineering' Seattle"

# WSJ company search
python scripts/stealth_search.py "site:wsj.com 'Acme Corp' acquisition" --output wsj.json

# Profile extraction
python scripts/linkedin_profile.py "https://www.linkedin.com/in/username" --screenshot profile.png

# Multi-site news
python scripts/stealth_search.py "site:wsj.com OR site:ft.com 'AI regulation'" --max-results 20
```

---

**Summary**: StealthSearch enables research on paywalled sites by extracting metadata from search results. Use DuckDuckGo for best reliability, respect limitations, follow ethical guidelines.
