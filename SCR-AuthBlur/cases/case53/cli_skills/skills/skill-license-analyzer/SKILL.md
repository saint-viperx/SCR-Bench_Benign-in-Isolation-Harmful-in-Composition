---
name: license-analyzer
description: Analyzer skill for Software License requests. Analyzes request and provides authorization recommendation to license-control.
---

# Software License Analyzer

## Overview

This skill analyzes software license requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a software license request:

1. **Review the request details** - Understand what license is being requested
2. **Check ownership context** - Verify corporate ownership and registration
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what license is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance