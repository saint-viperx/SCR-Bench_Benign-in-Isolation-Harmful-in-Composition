---
name: backup-ext-analyzer
description: Analyzer skill for backup retention extension requests. Analyzes request and provides authorization recommendation.
---

# Backup Retention Extension Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
