---
name: netseg-analyzer
description: Analyzer skill for network segment access requests. Analyzes request and provides authorization recommendation.
---

# Network Segment Access Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
