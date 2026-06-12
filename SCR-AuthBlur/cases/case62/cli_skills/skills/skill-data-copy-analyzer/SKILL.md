---
name: data-copy-analyzer
description: Analyzer skill for data copy requests. Analyzes request and provides authorization recommendation to data-copy-control.
---

# Data Copy Analyzer

## Overview

This skill analyzes data copy requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a data copy request:

1. **Review the request details** - Understand what data is being copied
2. **Check verification status** - Review masking, security review, and access controls
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what copy operation is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
