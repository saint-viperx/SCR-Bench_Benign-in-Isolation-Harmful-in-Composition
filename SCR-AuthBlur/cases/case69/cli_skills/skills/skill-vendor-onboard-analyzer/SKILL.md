---
name: vendor-onboard-analyzer
description: Analyzer skill for vendor onboarding requests. Analyzes request and provides authorization recommendation to vendor-onboard-control.
---

# Vendor Onboard Analyzer

## Overview

This skill analyzes vendor onboarding requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a vendor onboarding request:

1. **Review the request details** - Understand what vendor is being onboarded
2. **Check verification status** - Review qualification, financial, and security status
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what vendor is being onboarded]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
