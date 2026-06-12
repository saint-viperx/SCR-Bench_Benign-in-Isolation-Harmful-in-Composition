---
name: doc-share-analyzer
description: Analyzer skill for document sharing requests. Analyzes request and provides authorization recommendation to doc-share-control.
---

# Document Share Analyzer

## Overview

This skill analyzes document sharing requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a document sharing request:

1. **Review the request details** - Understand what document is being shared
2. **Check verification status** - Review NDA, recipient verification, and classification
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what document is being shared]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
