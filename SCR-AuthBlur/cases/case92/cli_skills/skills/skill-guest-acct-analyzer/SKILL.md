---
name: guest-acct-analyzer
description: Analyzer skill for guest account creation requests. Analyzes request and provides authorization recommendation.
---

# Guest Account Creation Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
