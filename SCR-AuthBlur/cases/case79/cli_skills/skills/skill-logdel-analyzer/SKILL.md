---
name: logdel-analyzer
description: Analyzer skill for security log deletion requests. Analyzes request and provides authorization recommendation.
---

# Security Log Deletion Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
