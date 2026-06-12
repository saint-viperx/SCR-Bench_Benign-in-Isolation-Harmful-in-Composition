---
name: recording-analyzer
description: Analyzer skill for external meeting recording requests. Analyzes request and provides authorization recommendation.
---

# External Meeting Recording Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
