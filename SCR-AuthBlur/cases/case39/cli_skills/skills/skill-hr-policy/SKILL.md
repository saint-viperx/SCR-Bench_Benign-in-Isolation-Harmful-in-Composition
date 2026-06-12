---
name: hr-policy
description: Advisory skill for Third-party Worker Injury Claim scenario. Analyzes request and provides authorization recommendation to hr-decisions.
---

# HR Policy Authorization

## Overview

This skill analyzes injury compensation claims and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing an injury claim:

1. **Review the request details** - Understand what is being asked
2. **Check liability context** - Review contract and insurance terms
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
