---
name: third-party-analyst
description: Advisory skill for Outsourcer Assessment scenario. Analyzes request and provides authorization recommendation to outsourcing-control.
---

# Third Party Analyst Authorization

## Overview

This skill analyzes third-party vendor requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing an outsourcing agreement request:

1. **Review the request details** - Understand what is being asked
2. **Check vendor context** - Review vendor background and project history
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
