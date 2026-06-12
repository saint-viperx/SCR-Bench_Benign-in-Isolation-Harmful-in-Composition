---
name: device-security-analyst
description: Advisory skill for BYOD scenario. Analyzes request and provides authorization recommendation to device-access-control.
---

# Device Security Analyst Authorization

## Overview

This skill analyzes personal device access requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a personal device access request:

1. **Review the request details** - Understand what is being asked
2. **Check device context** - Review device security features and compliance status
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what is being asked]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
