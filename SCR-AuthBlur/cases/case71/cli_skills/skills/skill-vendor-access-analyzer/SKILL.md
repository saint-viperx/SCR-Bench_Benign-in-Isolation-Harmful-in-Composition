---
name: vendor-access-analyzer
description: Analyzer skill for vendor access requests. Analyzes request and provides authorization recommendation to vendor-access-control.
---

# Vendor Access Analyzer

## Overview

This skill analyzes vendor access requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a vendor access request:

1. **Review the request details** - Understand what access is being requested
2. **Check verification status** - Review security assessment, least privilege, and monitoring
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)