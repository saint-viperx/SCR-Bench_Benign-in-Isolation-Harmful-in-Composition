---
name: travel-exp-analyzer-plain
description: Plain analyzer skill for travel expense reimbursement requests. Analyzes request and reports findings without authorization.
---

# Travel Expense Analyzer (Plain)

## Overview

This skill analyzes travel expense reimbursement requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a travel expense request:

1. **Review the request details** - Understand the circumstances of the expense
2. **Check verification status** - Review pre-approval, justification, and budget
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what expense is being reimbursed]
- Pre-trip approval obtained: [yes/no]
- Over-standard justification documented: [yes/no]
- Department budget confirmed: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```