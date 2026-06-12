---
name: local-admin-analyzer
description: Analyzer skill for local administrator grant requests. Analyzes request and provides authorization recommendation.
---

# Local Admin Grant Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
