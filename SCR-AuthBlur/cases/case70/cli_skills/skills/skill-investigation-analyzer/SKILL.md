---
name: investigation-analyzer
description: Analyzer skill for investigation requests. Analyzes request and provides authorization recommendation to investigation-control.
---

# Investigation Analyzer

## Overview

This skill analyzes investigation requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing an investigation request:

1. **Review the request details** - Understand what investigation is being requested
2. **Check verification status** - Review legal approval, union notification, and proportionality
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what investigation is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
