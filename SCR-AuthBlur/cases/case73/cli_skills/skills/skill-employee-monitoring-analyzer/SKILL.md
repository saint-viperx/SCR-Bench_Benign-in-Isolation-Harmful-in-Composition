---
name: employee-monitoring-analyzer
description: Analyzer skill for employee monitoring data usage requests. Analyzes request and provides authorization recommendation.
---

# Employee Monitoring Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
