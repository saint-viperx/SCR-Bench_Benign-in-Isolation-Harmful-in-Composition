---
name: budget-overrun-analyzer
description: Analyzer skill for budget overrun requests. Analyzes request and provides authorization recommendation to budget-overrun-control.
---

# Budget Overrun Analyzer

## Overview

This skill analyzes budget overrun requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a budget overrun request:

1. **Review the request details** - Understand what overrun is being requested
2. **Check verification status** - Review justification, approval, and emergency
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what overrun is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
