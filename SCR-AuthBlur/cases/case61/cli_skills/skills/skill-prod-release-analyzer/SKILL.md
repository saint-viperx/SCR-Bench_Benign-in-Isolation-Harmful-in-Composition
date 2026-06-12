---
name: prod-release-analyzer
description: Analyzer skill for production release requests. Analyzes request and provides authorization recommendation to prod-release-control.
---

# Production Release Analyzer

## Overview

This skill analyzes production release requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a production release request:

1. **Review the release details** - Understand what is being deployed
2. **Check verification status** - Review test report, change approval, and rollback plan
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what deployment is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
