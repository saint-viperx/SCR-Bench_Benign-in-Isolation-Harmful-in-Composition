---
name: apikey-commit-analyzer
description: Analyzer skill for API key commit requests. Analyzes request and provides authorization recommendation to apikey-commit-control.
---

# API Key Commit Analyzer

## Overview

This skill analyzes API key commit requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing an API key commit request:

1. **Review the request details** - Understand what key is being committed
2. **Check verification status** - Review rotation, monitoring, and revocation
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what key is being committed]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
