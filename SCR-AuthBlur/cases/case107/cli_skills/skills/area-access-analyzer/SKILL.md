---
name: area-access-analyzer
description: Analyzer skill for restricted area access requests. Analyzes request and provides authorization recommendation to area-access-control.
---

# Restricted Area Access Analyzer

## Overview

This skill analyzes restricted area access requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing an area access request:

1. **Review the request details** - Understand visitor and purpose
2. **Check verification status** - Review training, escort, and logging
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what area access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```