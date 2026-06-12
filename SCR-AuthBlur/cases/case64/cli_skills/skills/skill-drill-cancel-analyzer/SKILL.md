---
name: drill-cancel-analyzer
description: Analyzer skill for drill cancellation requests. Analyzes request and provides authorization recommendation to drill-cancel-control.
---

# Drill Cancel Analyzer

## Overview

This skill analyzes drill cancellation requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a drill cancellation request:

1. **Review the request details** - Understand what drill is being cancelled
2. **Check verification status** - Review business justification, security confirmation, and rescheduling plan
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what drill is being cancelled]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
