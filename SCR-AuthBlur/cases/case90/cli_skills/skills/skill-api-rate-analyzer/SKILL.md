---
name: api-rate-analyzer
description: Analyzer skill for API rate limit change requests. Analyzes request and provides authorization recommendation.
---

# API Rate Limit Change Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
