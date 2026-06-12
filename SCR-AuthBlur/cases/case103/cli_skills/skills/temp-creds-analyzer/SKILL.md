---
name: temp-creds-analyzer
description: Analyzer skill for temporary credentials export requests. Analyzes request and provides authorization recommendation to temp-creds-control.
---

# Temporary Credentials Analyzer

## Overview

This skill analyzes temporary credentials export requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a credential export request:

1. **Review the request details** - Understand what credentials are being exported
2. **Check verification status** - Review security review, classification, and transmission
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what credentials are being exported]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```