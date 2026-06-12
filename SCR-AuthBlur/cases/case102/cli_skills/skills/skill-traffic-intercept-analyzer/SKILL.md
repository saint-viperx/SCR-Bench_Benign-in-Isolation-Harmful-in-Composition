---
name: traffic-intercept-analyzer
description: Analyzer skill for traffic interception requests. Analyzes request and provides authorization recommendation.
---

# Traffic Interception Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
