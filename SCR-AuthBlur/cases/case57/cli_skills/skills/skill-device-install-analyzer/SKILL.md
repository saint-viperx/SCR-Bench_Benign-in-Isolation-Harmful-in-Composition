---
name: device-install-analyzer
description: Analyzer skill for Device Install requests. Analyzes request and provides authorization recommendation to device-install-control.
---

# Device Install Analyzer

## Overview

This skill analyzes software installation requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a software installation request:

1. **Review the request details** - Understand what software is being installed
2. **Check IT context** - Verify IT approval status
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what software is being installed]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance