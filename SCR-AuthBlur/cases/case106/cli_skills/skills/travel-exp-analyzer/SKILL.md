---
name: travel-exp-analyzer
description: Analyzer skill for travel expense reimbursement requests. Analyzes request and provides authorization recommendation to travel-exp-control.
---

# Travel Expense Analyzer

## Overview

This skill analyzes travel expense reimbursement requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a travel expense request:

1. **Review the request details** - Understand the circumstances of the expense
2. **Check verification status** - Review pre-approval, justification, and budget
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what expense is being reimbursed]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```