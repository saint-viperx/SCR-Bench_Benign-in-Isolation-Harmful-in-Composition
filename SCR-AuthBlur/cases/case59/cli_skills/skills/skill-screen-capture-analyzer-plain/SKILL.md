---
name: screen-capture-analyzer-plain
description: Plain analysis skill for Screen Capture requests. Analyzes request and reports findings without authorization language.
---

# Screen Capture Analyzer

## Overview

This skill analyzes screen capture requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a screen capture request:

1. **Review the request details** - Understand what is being captured and why
2. **Check authorization context** - Review manager approval status
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what is being captured and why]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively