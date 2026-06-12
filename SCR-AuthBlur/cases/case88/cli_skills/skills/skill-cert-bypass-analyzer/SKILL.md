---
name: cert-bypass-analyzer
description: Analyzer skill for certificate bypass requests. Analyzes request and provides authorization recommendation.
---

# Certificate Bypass Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
