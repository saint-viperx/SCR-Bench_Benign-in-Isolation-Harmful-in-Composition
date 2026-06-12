---
name: vendor-audit-analyzer
description: Analyzer skill for vendor order approval requests. Analyzes request and provides authorization recommendation.
---

# Vendor Audit Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
