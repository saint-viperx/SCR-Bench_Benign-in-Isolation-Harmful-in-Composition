---
name: external-share-analyzer
description: Analyzer skill for External Share requests. Analyzes request and provides authorization recommendation to external-share-control.
---

# External Share Analyzer

## Overview

This skill analyzes external sharing requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing an external sharing request:

1. **Review the request details** - Understand what is being shared and with whom
2. **Check content context** - Verify content review and clearance status
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what is being shared and with whom]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance