---
name: shared-account-analyzer
description: Analyzer skill for shared account requests. Analyzes request and provides authorization recommendation to shared-account-control.
---

# Shared Account Analyzer

## Overview

This skill analyzes shared account requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a shared account request:

1. **Review the request details** - Understand what account is being requested
2. **Check verification status** - Review business justification, security exception, and audit logging
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what account is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/D