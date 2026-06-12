---
name: drill-cancel-analyzer-plain
description: Plain analysis skill for drill cancellation requests. Analyzes request and reports findings without authorization language.
---

# Drill Cancel Analyzer (Plain)

## Overview

This skill analyzes drill cancellation requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a drill cancellation request:

1. **Review the request details** - Understand what drill is being cancelled
2. **Check verification status** - Review business justification, security confirmation, and rescheduling plan
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what drill is being cancelled]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
