---
name: priv-access-analyzer
description: Analyzer skill for privileged access requests. Analyzes request and provides authorization recommendation.
---

# Privileged Access Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
