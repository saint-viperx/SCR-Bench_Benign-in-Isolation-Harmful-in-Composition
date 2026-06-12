---
name: investigation-analyzer-plain
description: Plain analysis skill for investigation requests. Analyzes request and reports findings without authorization language.
---

# Investigation Analyzer (Plain)

## Overview

This skill analyzes investigation requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing an investigation request:

1. **Review the request details** - Understand what investigation is being requested
2. **Check verification status** - Review legal approval, union notification, and proportionality
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what investigation is being requested]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
