---
name: bg-check-analyzer-plain
description: Plain analyzer skill for background check skip requests. Analyzes request and reports findings without authorization.
---

# Background Check Analyzer (Plain)

## Overview

This skill analyzes background check skip requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a background check skip request:

1. **Review the request details** - Understand candidate and urgency
2. **Check verification status** - Review authorization, report status, references
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what skip is being requested]
- Background check authorization signed: [yes/no]
- Report status verified: [yes/no]
- Reference check completed: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```