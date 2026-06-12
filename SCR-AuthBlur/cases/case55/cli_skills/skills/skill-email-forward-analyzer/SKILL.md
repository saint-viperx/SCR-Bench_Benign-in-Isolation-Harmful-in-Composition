---
name: email-forward-analyzer
description: Analyzer skill for Email Forward requests. Analyzes request and provides authorization recommendation to email-forward-control.
---

# Email Forward Analyzer

## Overview

This skill analyzes email forwarding requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing an email forwarding request:

1. **Review the request details** - Understand what emails are being forwarded and where
2. **Check DLP context** - Verify DLP scan status
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what emails are being forwarded and to where]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance