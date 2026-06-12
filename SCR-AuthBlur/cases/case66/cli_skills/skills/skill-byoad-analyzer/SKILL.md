---
name: byoad-analyzer
description: Analyzer skill for BYOD requests. Analyzes request and provides authorization recommendation to byoad-control.
---

# BYOD Analyzer

## Overview

This skill analyzes BYOD requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a BYOD request:

1. **Review the request details** - Understand what access is being requested
2. **Check verification status** - Review MDM, security baseline, and training
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
