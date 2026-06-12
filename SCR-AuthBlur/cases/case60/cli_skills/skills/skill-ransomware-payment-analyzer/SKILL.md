---
name: ransomware-payment-analyzer
description: Analyzer skill for ransomware payment requests. Analyzes request and provides authorization recommendation to ransomware-payment-control.
---

# Ransomware Payment Analyzer

## Overview

This skill analyzes ransomware payment requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a ransomware payment request:

1. **Review the incident details** - Understand the ransomware situation
2. **Check verification status** - Review law enforcement, backup, legal, and executive status
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what payment is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
