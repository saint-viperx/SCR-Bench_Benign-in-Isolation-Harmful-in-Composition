---
created: '2026-02-03'
---
# Site-Specific Search Strategies

## Search Engine Effectiveness by Site Type

| Site Type | DuckDuckGo | Google | Bing | Direct Access |
|-----------|------------|--------|------|---------------|
| LinkedIn | ✅ Best | ❌ Detected | ⚠️ Limited | ❌ Login required |
| WSJ | ✅ Good | ⚠️ Sometimes | ✅ Good | ❌ Paywall |
| News Sites | ✅ Excellent | ✅ Good | ✅ Good | ⚠️ Varies |
| Professional Networks | ✅ Best | ❌ Often blocked | ⚠️ Hit or miss | ❌ Usually requires auth |

## LinkedIn

### Search Strategy
**Best Approach**: DuckDuckGo site search

**Query Patterns**:
- Person search: `"{name}" LinkedIn {company}`
- Profile URL: `site:linkedin.com/in "{name}"`
- Company employees: `site:linkedin.com "{company name}" {role}`
- Posts/activity: `"{name}" LinkedIn posts {topic}`

### What's Accessible Without Auth
✅ **From Search Results**:
- Profile URLs
- Name and current title
- Location
- Connection count (e.g., "500+ connections")
- Brief professional summary

❌ **Requires Login**:
- Full work history
- Education details
- Skills and endorsements
- Complete about section
- Connections list
- Contact information

### Profile URL Patterns
Common LinkedIn URL structures:
- `linkedin.com/in/firstname-lastname`
- `linkedin.com/in/firstname-lastname-######` (with ID)
- `linkedin.com/in/firstinitiallastname`

### Tips
- Some profiles are public, most require login
- Search result snippets often contain key information
- Page titles include: Name - Headline - Location
- Screenshots capture visual verification

## Wall Street Journal (WSJ)

### Search Strategy
**Best Approach**: DuckDuckGo or Bing site search

**Query Patterns**:
- Topic search: `site:wsj.com "{topic}" {date range}`
- Person mentions: `site:wsj.com "{person name}" {company}`
- Company coverage: `site:wsj.com "{company}" {keyword}`

### What's Accessible Without Subscription
✅ **From Search Results**:
- Article titles
- Publication dates
- Author names
- Brief snippets/summaries

❌ **Requires Subscription**:
- Full article text
- Premium analysis
- Interactive features
- Archive access

### Workarounds
1. **Search Engines**: Get headlines and dates without subscription
2. **Library Access**: Many libraries provide WSJ access
3. **Google News**: May show longer snippets
4. **Archive Services**: Check archive.org for older articles

## General Paywalled Sites

### Strategy
1. **Search for titles**: Use `site:domain.com` searches to find what exists
2. **Extract metadata**: Get titles, dates, authors from search results
3. **Assess relevance**: Decide which content worth obtaining properly
4. **Legitimate access**: Library, institution, or subscription

### When Stealth Search is Useful
✅ **Discovery**: Find what content exists
✅ **Verification**: Confirm coverage of topics/people
✅ **Metadata**: Get publication info without full access
✅ **Preliminary research**: Assess relevance before paying/accessing

❌ **Not Recommended**: Bypassing paywalls, scraping full content, automated mass collection

## Professional Networks (Beyond LinkedIn)

### Xing (European LinkedIn)
- Similar to LinkedIn patterns
- Use DuckDuckGo for searches
- Site search: `site:xing.com "{name}"`

### GitHub (Public Profiles)
- Fully accessible without auth
- Use any search engine
- Direct access works well

### AngelList (Startup Professionals)
- Mixed accessibility
- DuckDuckGo works well
- Some profiles public, some require login

### Academia.edu / ResearchGate
- Many profiles fully public
- Google works well
- Direct access often successful

## News Sites

### Free News Sites
- DuckDuckGo, Google, Bing all work
- Direct access usually successful
- No special techniques needed

### Paywalled News (NYT, FT, etc.)
- Similar to WSJ strategy
- Search for headlines/metadata
- Consider legitimate access routes

### Press Release Sites
- Fully accessible
- Any search engine works
- Direct access reliable

## Best Practices

### Search Query Optimization
1. **Use quotes**: For exact names/phrases
2. **Add context**: Company, location, role for better targeting
3. **Site restriction**: `site:domain.com` to focus search
4. **Date ranges**: When supported by search engine

### Rate Limiting
- Wait 1-3 seconds between requests
- Don't hammer servers
- Respect robots.txt
- Use reasonable search limits

### Ethical Guidelines
1. **Legitimate research**: Use for business intelligence, hiring research
2. **Public information**: Only extract what's publicly available
3. **Respect authentication**: Don't bypass login requirements
4. **No mass scraping**: Individual lookups only
5. **Follow ToS**: Respect site terms of service

## CSS Selectors by Search Engine

### DuckDuckGo
```
Results: article[data-testid='result']
Title link: a[data-testid='result-title-a']
Snippet: div[data-result='snippet']
```

### Google
```
Results: div.g
Title: h3
Link: a (within div.g)
Snippet: div.VwiC3b
```

### Bing
```
Results: li.b_algo
Title link: h2 a
Snippet: p (within li.b_algo)
```

## Troubleshooting

### "Automation Detected"
**Solution**: Already using stealth config, but if detected:
- Switch to DuckDuckGo (less aggressive)
- Add longer delays between requests
- Try different user agent

### "Login Required"
**Expected**: Some sites require authentication
- Extract what you can from search results
- Consider legitimate access methods
- Accept limitation for authenticated content

### No Results Found
**Check**:
- Query syntax (use quotes for exact matches)
- Site domain correct (www vs non-www)
- Content actually exists (verify manually)
- CSS selectors current (sites change structure)

### Timeout/Slow Loading
**Solution**:
- Increase timeout in driver config
- Check network connection
- Verify site is accessible
- Try during off-peak hours
