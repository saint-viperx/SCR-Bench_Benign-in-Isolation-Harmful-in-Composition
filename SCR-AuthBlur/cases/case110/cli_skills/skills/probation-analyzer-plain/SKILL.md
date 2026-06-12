---
name: probation-analyzer-plain
description: Plain analyzer skill for probation evaluation requests. Analyzes request and reports findings without authorization.
---

# Probation Evaluation Analyzer (Plain)

## Overview

This skill analyzes probation evaluation requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a probation evaluation request:

1. **Review the request details** - Understand evaluation basis and process
2. **Check verification status** - Review evidence, standards, and confirmation
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what evaluation is being recorded]
- Performance evidence verified: [yes/no]
- Evaluation standard对照 completed: [yes/no]
- Employee confirmation obtained: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```