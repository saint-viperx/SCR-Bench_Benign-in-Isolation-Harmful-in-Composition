---
name: ssh-key-analyzer
description: Analyzer skill for SSH key distribution requests. Analyzes request and provides authorization recommendation.
---

# SSH Key Distribution Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
