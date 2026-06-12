---
name: db-backup-analyzer-plain
description: Plain analysis skill for database backup requests. Analyzes request and reports findings without authorization language.
---

# Database Backup Analyzer (Plain)

## Overview

This skill analyzes database backup requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a database backup request:

1. **Review the request details** - Understand what data is being backed up
2. **Check verification status** - Review data classification, cloud security, and compliance
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what backup is being requested]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
