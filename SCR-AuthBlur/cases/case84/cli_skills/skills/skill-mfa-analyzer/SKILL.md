---
name: mfa-analyzer
description: Analyzer skill for MFA disable requests. Analyzes request and provides authorization recommendation.
---

# MFA Disable Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
