# Twitter/X MCP Tools Reference

Complete guide to using the Twitter/X MCP server tools for posting and queuing tweets.

## Available Tools

### queue_tweet (RECOMMENDED)

Queue a tweet for automated publishing.

**Parameters:**
- `text` (string, required): Tweet content (max 250 chars, auto-truncated if longer)
- `topic` (string, optional): Topic/slug for filename (default: "tweet")

**Returns:**
- Success: `"Tweet queued: {topic}_{timestamp}.md"`
- DRY_RUN: `"[DRY RUN] Would queue_tweet: {text_preview}..."`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("queue_tweet", {
    "text": "🤖 Automated Twitter posting in one weekend.\nPython + Playwright — zero API costs.\n#BuildInPublic #AI",
    "topic": "automation_milestone"
})
```

**Queue File Location:**
`/Vault/Plans/twitter_queue/{topic}_{timestamp}.md`

**Queue File Format:**
```markdown
---
type: twitter_post
created: 2026-03-05T14:30:00Z
---

🤖 Automated Twitter posting in one weekend.
Python + Playwright — zero API costs.
#BuildInPublic #AI
```

**Processing:**
- TwitterPoster watcher checks queue every 5 minutes (300 seconds)
- Watcher posts to Twitter/X via Playwright automation
- Auto-truncates to 250 chars if needed (247 + "...")
- Posted files moved to `/Vault/Done/twitter_posted/`

---

### post_tweet (USE WITH CAUTION)

Post directly to Twitter/X without queuing.

**Parameters:**
- `text` (string, required): Tweet content (max 250 chars, auto-truncated if longer)

**Returns:**
- Success: `"Tweet posted: {text_preview}..."`
- Failure: `"Tweet failed: {text_preview}..."`
- DRY_RUN: `"[DRY RUN] Would post_tweet: {text_preview}..."`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("post_tweet", {
    "text": "🚀 Just shipped a new feature! #BuildInPublic"
})
```

**Auto-truncation:**
If text exceeds 250 characters, it's automatically truncated to 247 + "..."

**⚠️ Security Warning:**
- **NEVER use post_tweet without explicit human approval**
- **ALWAYS prefer queue_tweet for safety**
- Direct posting bypasses human review
- No undo once posted

---

## When to Use Each Tool

### Use queue_tweet (default):
- ✅ All business updates and announcements
- ✅ Weekly progress reports
- ✅ Milestone celebrations
- ✅ Content generated from vault context
- ✅ Any tweet that should be reviewed before publishing

### Use post_tweet (rare):
- ⚠️ Only when explicitly instructed by user
- ⚠️ Time-sensitive announcements already approved
- ⚠️ User has reviewed and approved the exact text
- ⚠️ Never for automated/scheduled tweets

---

## Twitter/X Session Requirements

Both tools require:
1. Twitter/X session authenticated and saved as cookies.json
2. Cookies stored in path defined by `TWITTER_SESSION_PATH` env variable
3. Playwright browser installed (`playwright install chromium`)

**Session management:**
- Uses cookies.json (not persistent browser context like LinkedIn)
- Cookies must be refreshed manually when expired
- Session expires after ~30 days of inactivity

**First-time setup:**
```bash
# 1. Export cookies from browser using extension
# Recommended: "Get cookies.txt LOCALLY" Chrome extension
# Export as JSON format

# 2. Save to session path
cp ~/Downloads/x.com_cookies.json ~/.local/share/twitter_session/cookies.json

# 3. Test with dry-run
uv run python main.py --twitter --dry-run
```

**When session expires:**
```
Error: "Session expired! Please refresh cookies.json manually."

Solution:
1. Log in to Twitter/X in browser
2. Export cookies again using browser extension
3. Replace cookies.json file
4. Retry posting
```

---

## Tweet Content Guidelines

**Character limits:**
- **Hard limit:** 250 characters (enforced by MCP and watcher)
- **Auto-truncation:** Text > 250 chars → truncated to 247 + "..."
- **Recommended:** 200-240 characters (leaves room for edits)

**Formatting:**
- Plain text only (no markdown)
- Line breaks preserved
- Emojis supported and encouraged (boost engagement)
- URLs auto-shortened by Twitter/X

**Hashtags:**
- 2-4 hashtags recommended (Twitter best practice)
- Can be inline or on separate line
- Use relevant, searchable tags
- Mix broad (#AI) and niche (#WaheedAI) tags

---

## DRY_RUN Mode

When `DRY_RUN=true` in `.env`, both tools return simulation messages:

```
[DRY RUN] Would queue_tweet: 🤖 Automated Twitter posting...
```

**Always check DRY_RUN status before posting to production Twitter/X account.**

---

## Timing Considerations

**queue_tweet execution time:**
- File write: <1 second
- **Total: instant**

**post_tweet execution time:**
- Browser startup: ~5-10 seconds
- Twitter/X load: ~20 seconds
- Tweet submission: ~3-5 seconds
- Verification wait: ~20 seconds
- **Total: ~50-60 seconds per tweet**

**TwitterPoster watcher:**
- Checks queue every 5 minutes (300 seconds)
- Posts one at a time
- Moves to /Done/ after posting

---

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Session expired` | Cookies expired | Export new cookies.json from browser |
| `Tweet box not found` | Twitter UI changed | Check watcher code for updated selectors |
| `Text not entered` | Bot detection | Watcher uses keyboard.type() to avoid detection |
| `Submission failed` | Network/timing issue | Watcher retries with 20-second verification |
| `Permission denied` | File system issue | Check vault path permissions |
| `Text too long` | Exceeds 250 chars | Auto-truncated to 247 + "..." |

---

## Best Practices

1. **Always queue by default** - use `queue_tweet` for all automated tweets
2. **Review before posting** - check queued tweets in `/Plans/twitter_queue/`
3. **Keep it short** - aim for 200-240 chars (under the 250 limit)
4. **Use emojis** - they boost engagement on Twitter/X
5. **Log every action** - record all tweets to `/Vault/Logs/YYYY-MM-DD.json`
6. **Check DRY_RUN** - verify mode before posting to production
7. **Validate content** - ensure no private/financial data in tweets
8. **Use descriptive topics** - helps organize queue files
9. **Monitor posted folder** - check `/Done/twitter_posted/` for confirmation
10. **Refresh cookies regularly** - before they expire (~30 days)

---

## Security Considerations

- **Private data**: Never tweet financial numbers, client names, or sensitive business data
- **Brand safety**: All tweets should align with company brand voice
- **Human review**: Queue tweets for review, don't auto-post
- **Rate limiting**: Twitter/X may flag rapid posting as spam (watcher posts every 5 min max)
- **Session security**: Keep cookies.json file secure (contains auth tokens)
- **Bot detection**: Watcher uses keyboard.type() to avoid Twitter's bot detection

---

## Character Count Tips

**Staying under 250 chars:**
- Use abbreviations: "w/" instead of "with"
- Remove filler words: "just", "really", "very"
- Use emojis instead of words: 🚀 instead of "launched"
- Shorten URLs before tweeting (Twitter auto-shortens anyway)
- Use line breaks strategically (counts as 1 char)

**Example optimization:**
```
Before (267 chars):
"We just launched a new feature that allows you to automate your entire email workflow. It saves you approximately 2 hours every single day. Check it out! #AI #Automation #Productivity #BuildInPublic"

After (238 chars):
"🚀 New feature: automate your entire email workflow.
Saves 2 hours/day.
#AI #Automation #BuildInPublic #WaheedAI"
```
