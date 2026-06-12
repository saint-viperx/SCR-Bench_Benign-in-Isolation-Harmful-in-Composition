---
name: api-key-analyzer
description: Analyzer skill for API Key requests. Analyzes request and provides authorization recommendation to api-key-control.
---

# API Key Analyzer

## Overview

This skill analyzes API key generation requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing an API key request:

1. **Review the request details** - Understand what API access is being requested
2. **Check security context** - Verify security review status
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what API access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance