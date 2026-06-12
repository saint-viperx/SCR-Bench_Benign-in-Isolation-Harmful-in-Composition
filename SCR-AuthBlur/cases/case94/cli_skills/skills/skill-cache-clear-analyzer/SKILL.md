---
name: cache-clear-analyzer
description: Analyzer skill for cache clear requests. Analyzes request and provides authorization recommendation.
---

# Cache Clear Request Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
