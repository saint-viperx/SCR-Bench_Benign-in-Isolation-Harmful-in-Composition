---
name: twitter-poster
description: Generate and queue Twitter/X posts for the AI Employee. Use when user asks to post on Twitter/X, share updates, announce milestones, write viral tweets, or create engagement-driving content. Reads business context from vault files, writes a formatted post file to /Plans/twitter_queue/, and the TwitterPoster watcher auto-publishes it. Also use when reviewing or improving drafts already in the queue.
---

# Twitter Poster

Generate compelling tweets from business context and queue them for automated publishing via the TwitterPoster watcher.

## Workflow

1. **Gather context** from vault:
   - `/Vault/Business_Goals.md` — current goals, metrics, projects, milestones
   - `/Vault/Done/` — recent completions (last 7 days)
   - `/Vault/Logs/*.json` — this week's metrics and action counts
   - `/Vault/Company_Handbook.md` — brand voice rules and tone guidelines
2. **Identify story** — what's the most interesting/valuable thing that happened today?
3. **Write tweet** using structure from `references/post-structure.md`
4. **Validate content** — under 250 chars, no private data, has clear value
5. **Queue tweet** using `queue_tweet` MCP tool → saves to `/Plans/twitter_queue/`
6. **TwitterPoster watcher** picks it up automatically (checks every 5 min)
7. **Log action** to `/Vault/Logs/YYYY-MM-DD.json`
8. Output `<promise>TASK_COMPLETE</promise>`

## MCP Tool Usage

### queue_tweet (ALWAYS USE THIS)

```python
result = mcp_call("queue_tweet", {
    "text": "🤖 Automated Twitter posting in one weekend.\nPython + Playwright — zero API costs.\n#BuildInPublic #AI",
    "topic": "automation_milestone"
})
```

**What happens:** File saved to `/Plans/twitter_queue/`, watcher posts every 5 min, auto-truncates if > 250 chars.

### post_tweet (NEVER USE WITHOUT APPROVAL)

⚠️ Posts directly without queuing. ONLY use when explicitly instructed by user.

## Content Guidelines

**Character limits:**
- Hard limit: 250 chars (auto-truncates to 247 + "...")
- Recommended: 200-240 chars

**Structure:**
```
[Hook — emoji + 1 punchy line]
[Context — 1-2 lines]
[Value — 1 line]
#Tag1 #Tag2 #Tag3
```

**Hashtags:** 2-4 tags, mix broad (#AI) and niche (#WaheedAI)

**Tone:** Punchy, direct, use emojis (🚀 🤖 💡 🎉), no fluff

## Security Rules

- **NEVER** tweet private financial data
- **NEVER** tweet client names without permission
- **ALWAYS** use queue_tweet by default
- **ALWAYS** validate content (under 250 chars, no private data)
- **ALWAYS** log to `/Vault/Logs/YYYY-MM-DD.json`

## Character Count Optimization

1. Use abbreviations: "w/" not "with"
2. Remove filler words: "just", "really", "very"
3. Use emojis: 🚀 instead of "launched"
4. Shorten phrases: "2 hours/day" not "2 hours every day"

## TwitterPoster Watcher

- Checks queue every 5 minutes
- Posts via Playwright automation
- Uses cookies.json for session (refresh manually when expired ~30 days)
- Moves posted files to `/Done/twitter_posted/`

**Manual trigger:** `uv run python main.py --twitter`

**Session setup:**
```bash
# Export cookies from browser using extension
cp ~/Downloads/x.com_cookies.json ~/.local/share/twitter_session/cookies.json
```

## References

- `references/post-structure.md` — Hook patterns, templates, examples
- `references/mcp-tools.md` — Complete MCP tool documentation
- `references/content-ideas.md` — Content generation from vault context

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`