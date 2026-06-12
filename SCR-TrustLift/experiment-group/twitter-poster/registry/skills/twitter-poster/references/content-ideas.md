# Twitter/X Content Ideas & Context Sources

Guide for generating tweet ideas from business context and vault files.

## Primary Context Sources

### 1. Business_Goals.md

**Location:** `/Vault/Business_Goals.md`

**What to extract:**
- Current revenue targets and progress
- Active projects and their status
- Key metrics and KPIs
- Quarterly/monthly goals
- Client wins and milestones

**Tweet ideas:**
- Milestone announcements (hit revenue target, completed project)
- Progress updates (halfway to goal, X clients onboarded)
- Quick wins and achievements
- Behind-the-scenes snippets

---

### 2. Done Folder

**Location:** `/Vault/Done/`

**What to extract:**
- Recently completed tasks (last 7 days)
- Finished projects
- Resolved issues
- Shipped features

**Tweet ideas:**
- "What we shipped this week" updates
- Build-in-public progress reports
- Quick feature announcements
- Daily/weekly wins

---

### 3. Company_Handbook.md

**Location:** `/Vault/Company_Handbook.md`

**What to extract:**
- Brand voice and tone guidelines
- Company values and mission
- Product/service descriptions
- Target audience

**Use for:**
- Ensuring consistent brand voice
- Aligning tweets with company values
- Staying on-brand with messaging
- Understanding audience expectations

---

### 4. Logs Folder

**Location:** `/Vault/Logs/*.json`

**What to extract:**
- Action counts (emails processed, invoices sent)
- Automation metrics
- Time saved calculations
- System performance data

**Tweet ideas:**
- "This week's numbers" tweets
- Automation impact reports
- Productivity metrics
- Quick stats

---

## Tweet Type Decision Tree

```
What happened today/this week?
    │
    ├─ Hit a milestone? → Milestone announcement (with emoji)
    │
    ├─ Shipped a feature? → Build-in-public update
    │
    ├─ Learned something? → Quick tip or lesson
    │
    ├─ Solved a problem? → Problem-solution tweet
    │
    └─ Regular day? → Daily/weekly stats
```

---

## Content Generation Workflow

### Step 1: Gather Context

```python
# Read business goals
goals = read_file("/Vault/Business_Goals.md")

# Get recent completions
done_files = list_files("/Vault/Done/", last_7_days=True)

# Get this week's metrics
logs = read_logs("/Vault/Logs/", this_week=True)

# Get brand voice
handbook = read_file("/Vault/Company_Handbook.md")
```

### Step 2: Identify Story

Ask:
- What's the most interesting thing that happened today?
- What would our audience find valuable?
- What demonstrates progress?
- What's shareable and relatable?
- Can I say it in 250 characters?

### Step 3: Structure Tweet

Use templates from `post-structure.md`:
1. Hook (emoji + punchy opening)
2. Context (what happened, 1-2 lines)
3. Value (key insight or result)
4. Hashtags (2-4 relevant tags)

### Step 4: Validate Content

Check:
- ✅ Under 250 characters (hard limit)
- ✅ No private financial data
- ✅ No client names without permission
- ✅ No sensitive business information
- ✅ Aligns with brand voice
- ✅ Has clear value for reader
- ✅ Includes 2-4 hashtags

---

## Tweet Ideas by Business Context

### Revenue Milestone
```
Context: Hit monthly revenue target
Tweet: "🚀 Just crossed $X in monthly revenue.
Key tactic: [one specific thing]
#Entrepreneurship #BuildInPublic"
Character count: ~120 chars
```

### Feature Launch
```
Context: Shipped new automation feature
Tweet: "🤖 New feature: [feature name]
[One-line benefit]
#AI #Automation #BuildInPublic"
Character count: ~100 chars
```

### Lesson Learned
```
Context: Made a mistake or faced a challenge
Tweet: "💡 Made a mistake that cost me [X hours].
The fix: [one-line solution]
#TIL #Founder"
Character count: ~120 chars
```

### Weekly Progress
```
Context: Regular week of work
Tweet: "This week's AI Employee stats:
→ [metric 1]
→ [metric 2]
→ [metric 3]
#AI #Automation"
Character count: ~140 chars
```

### Client Win
```
Context: Successful client project
Tweet: "🎉 Client saved [X hours/week] with our solution.
[One-line how]
#Productivity #AI"
Character count: ~100 chars
```

---

## Tone Guidelines for Twitter/X

**Punchy and direct:**
- Get to the point immediately
- Use emojis to convey emotion
- Short sentences, high impact
- No fluff or filler words

**Authentic and transparent:**
- Share real numbers when possible
- Admit mistakes quickly
- Show behind-the-scenes work
- Be honest about challenges

**Value-first:**
- Every tweet should teach or inspire
- Focus on reader benefit
- Share actionable insights
- Make it worth their time

**Engaging:**
- Use emojis strategically (🚀 🤖 💡 🎉)
- Ask questions occasionally
- Use line breaks for readability
- Start strong with a hook

---

## What NOT to Tweet

❌ **Private financial details** (exact revenue, profit margins, client payments)
❌ **Client names** without explicit permission
❌ **Sensitive business strategy** (pricing, competitive intel)
❌ **Negative content** (complaints, call-outs, drama)
❌ **Unverified claims** (can't back up with data)
❌ **Clickbait** (misleading hooks, false promises)
❌ **Personal politics** (unless directly relevant to business)
❌ **Confidential information** (NDAs, trade secrets)
❌ **Long-form content** (save for LinkedIn, keep Twitter short)

---

## Hashtag Strategy

**Use 2-4 tags (Twitter best practice):**
- Too few: miss discoverability
- Too many: looks spammy, wastes characters

**Mix broad and niche:**
- Broad: #AI, #Automation, #Entrepreneurship (high volume)
- Niche: #WaheedAI, #ClaudeCode, #BuildInPublic (targeted)

**Relevant to content:**
- Don't use trending tags unrelated to tweet
- Match tags to tweet topic and audience
- Include industry-specific tags

**Common tag sets:**

**AI/Automation:**
`#AI #Automation #BuildInPublic #WaheedAI`

**Business/Entrepreneurship:**
`#Founder #SmallBusiness #Productivity #BuildingInPublic`

**Tech/Development:**
`#Python #OpenSource #LLM #AIAgents`

**Productivity:**
`#Productivity #TimeManagement #Automation #WorkSmart`

---

## Character Count Optimization

**Techniques to stay under 250 chars:**

1. **Use abbreviations:**
   - "w/" instead of "with"
   - "b/c" instead of "because"
   - "~" instead of "approximately"

2. **Remove filler words:**
   - "just", "really", "very", "actually"
   - "I think", "In my opinion"

3. **Use emojis instead of words:**
   - 🚀 instead of "launched"
   - 💡 instead of "tip" or "idea"
   - 🤖 instead of "AI" or "automation"
   - 🎉 instead of "celebrating"

4. **Shorten phrases:**
   - "2 hours/day" instead of "2 hours every day"
   - "Hit $X" instead of "We reached $X in revenue"

5. **Use line breaks strategically:**
   - Counts as 1 character
   - Improves readability
   - Creates visual hierarchy

---

## Example: Generating Tweet from Vault Context

**Input context:**
- Business_Goals.md shows: "Q1 Goal: Automate 80% of email triage"
- Done/ shows: EMAIL_triage_complete.md from 2 days ago
- Logs show: 47 emails processed this week, 2 hours saved

**Generated tweet:**
```
🤖 Hit 80% email automation — 2 months early.
47 emails triaged this week w/o manual review.
Result: 2 hours back every day.
#AI #Automation #BuildInPublic
```

**Character count:** 147 chars (well under 250 limit)
**Value:** Specific metrics, clear benefit
**Safe:** No private data, no client names, verifiable claims
**Engaging:** Emoji hook, concrete numbers, relevant hashtags

---

## Twitter vs LinkedIn Content Strategy

**Twitter/X (250 chars):**
- Quick wins and updates
- Daily/weekly stats
- Short tips and lessons
- Milestone announcements
- Behind-the-scenes snippets

**LinkedIn (1300 chars):**
- Detailed case studies
- Long-form lessons learned
- In-depth project breakdowns
- Comprehensive weekly roundups
- Thought leadership pieces

**Strategy:** Tweet the headline, LinkedIn gets the full story.

**Example:**
- **Twitter:** "🚀 Automated email triage in one weekend. 2 hours saved/day. #AI #Automation"
- **LinkedIn:** Full post with context, methodology, lessons learned, and detailed results
