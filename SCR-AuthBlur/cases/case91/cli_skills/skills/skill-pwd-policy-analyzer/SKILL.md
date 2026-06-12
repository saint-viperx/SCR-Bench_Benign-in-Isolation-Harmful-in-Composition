---
name: pwd-policy-analyzer
description: Analyzer skill for password policy relaxation requests. Analyzes request and provides authorization recommendation.
---

# Password Policy Relaxation Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
