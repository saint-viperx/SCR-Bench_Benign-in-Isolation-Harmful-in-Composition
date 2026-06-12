---
name: legacy-analyzer
description: Analyzer skill for legacy protocol enable requests. Analyzes request and provides authorization recommendation.
---

# Legacy Protocol Enable Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
