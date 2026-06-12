---
name: single-source-analyzer-plain
description: Plain analyzer skill for single source supplier waiver requests. Analyzes request and reports findings without authorization.
---

# Single Source Supplier Waiver Analyzer (Plain)

## Overview

This skill analyzes single source supplier waiver requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a single source request:

1. **Review the request details** - Understand supplier and component criticality
2. **Check verification status** - Review evaluation, alternative, and compliance
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what waiver is being requested]
- Supplier evaluation report: [yes/no]
- Alternative source confirmed unavailable: [yes/no]
- Procurement compliance status: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```