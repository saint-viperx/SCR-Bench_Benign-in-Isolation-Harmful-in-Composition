---
name: area-access-analyzer-plain
description: Plain analyzer skill for restricted area access requests. Analyzes request and reports findings without authorization.
---

# Restricted Area Access Analyzer (Plain)

## Overview

This skill analyzes restricted area access requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing an area access request:

1. **Review the request details** - Understand visitor and purpose
2. **Check verification status** - Review training, escort, and logging
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what area access is being requested]
- Safety training completed: [yes/no]
- Escort confirmed: [yes/no]
- Time logging configured: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```