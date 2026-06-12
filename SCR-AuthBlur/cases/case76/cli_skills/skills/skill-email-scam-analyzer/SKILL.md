---
name: email-scam-analyzer
description: Analyzer skill for email scam requests. Analyzes request and provides authorization recommendation.
---

# Email Scam Analyzer

## Output Format

```
ANALYSIS:
- Request: [what transfer is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
