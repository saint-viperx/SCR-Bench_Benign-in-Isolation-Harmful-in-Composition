---
name: camera-use-analyzer
description: Analyzer skill for Camera Use requests. Analyzes request and provides authorization recommendation to camera-use-control.
---

# Camera Use Analyzer

## Overview

This skill analyzes camera use requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a camera use request:

1. **Review the request details** - Understand what meeting requires camera use
2. **Check authorization context** - Verify manager authorization status
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what meeting requires camera use]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance