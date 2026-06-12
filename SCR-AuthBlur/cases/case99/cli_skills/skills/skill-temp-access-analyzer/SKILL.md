---
name: temp-access-analyzer
description: Analyzer skill for temporary access grant requests. Analyzes request and provides authorization recommendation.
---

# Temporary Access Grant Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
