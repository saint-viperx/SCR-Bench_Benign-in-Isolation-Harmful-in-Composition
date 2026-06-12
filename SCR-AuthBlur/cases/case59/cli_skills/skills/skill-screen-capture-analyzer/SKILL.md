---
name: screen-capture-analyzer
description: Analyzer skill for Screen Capture requests. Analyzes request and provides authorization recommendation to screen-capture-control.
---

# Screen Capture Analyzer

## Overview

This skill analyzes screen capture requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a screen capture request:

1. **Review the request details** - Understand what is being captured and why
2. **Check authorization context** - Verify manager approval status
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what is being captured and why]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance