![Stealth Search banner](banner.png)

# Stealth Search

Search paywalled and protected sites (LinkedIn, WSJ, news sites) using stealth browser techniques when WebFetch fails. Uses Chromium with stealth configuration to search DuckDuckGo, Google, and Bing without triggering bot detection.

**Category:** Research · **Created:** 2026-02-03

---

## How to Use — Just Ask

Say any of these to Claude and the skill activates:

> **"Search LinkedIn for..."**

> **"Find articles on WSJ about..."**

> **"WebFetch can't access this site — try stealth search"**

> **"Search for this person's professional background"**

> **"Find news coverage of this company behind paywalls"**

### Worked Examples

**Finding someone on LinkedIn:**
> "Search LinkedIn for Sarah Chen, Chief Data Officer in Boston"

Searches DuckDuckGo with stealth browser, extracts profile URLs, names, titles, and locations from search snippets. Returns JSON with results and optional screenshot.

**Paywalled news search:**
> "Find WSJ and FT articles about the Acme Corp merger"

Searches multiple news sites using `site:` operators, extracts article titles, dates, authors, and preview snippets. Full text requires subscription but metadata is accessible.

**When WebFetch fails:**
> "WebFetch is blocked on this site — can you try another way?"

Switches to stealth browser with anti-detection configuration. Uses DuckDuckGo (lowest detection rate) to find public information about the target.

**Executive verification:**
> "Verify this person's job title and company from their LinkedIn"

Searches for the profile, visits the URL if publicly accessible, captures screenshot, and extracts available information. Notes what requires login for full access.

**Multi-engine coverage:**
> "Search all engines for coverage of this startup"

Runs the query through DuckDuckGo, Google, and Bing for comprehensive results. Deduplicates and returns combined findings.

**Company intelligence:**
> "Find recent news about Company X from business press"

Searches WSJ, Bloomberg, FT, and Reuters using site operators. Extracts headlines, dates, and snippets for relevance assessment.

---

## What You Get

Search results as structured JSON:

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
      "snippet": "Preview text..."
    }
  ]
}
```

Plus optional screenshots of search results pages.

## Search Engines

| Engine | Best For | Detection Risk |
|--------|----------|----------------|
| DuckDuckGo | LinkedIn, most sites | Low |
| Google | Comprehensive results | Medium |
| Bing | News sites | Low |

## Limitations

- **Cannot bypass paywalls** — extracts metadata from search results, full content needs subscription
- **Cannot access authenticated content** — login-required data not available
- **Individual lookups only** — not for mass scraping
- **Legitimate research only** — follows ethical guidelines

## Links

- [Community page](https://www.context-is-everything.com/community) · [Full skill documentation](SKILL.md)
