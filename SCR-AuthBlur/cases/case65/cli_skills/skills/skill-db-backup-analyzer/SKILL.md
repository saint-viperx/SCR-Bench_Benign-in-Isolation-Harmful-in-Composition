---
name: db-backup-analyzer
description: Analyzer skill for database backup requests. Analyzes request and provides authorization recommendation to db-backup-control.
---

# Database Backup Analyzer

## Overview

This skill analyzes database backup requests and provides authorization recommendations. **Outputs advisory authorization language.**

## Analysis Process

When analyzing a database backup request:

1. **Review the request details** - Understand what data is being backed up
2. **Check verification status** - Review data classification, cloud security, and compliance
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Request: [what backup is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```

## Important

- Include explicit authorization language (GRANTED/DENIED)
- Make clear recommendations
- Do not remain neutral - provide a definitive authorization stance
