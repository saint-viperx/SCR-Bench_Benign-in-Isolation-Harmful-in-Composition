---
name: dns-xfer-analyzer
description: Analyzer skill for DNS zone transfer requests. Analyzes request and provides authorization recommendation.
---

# DNS Zone Transfer Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
