---
name: meeting-notes-analyzer-plain
description: Plain analyzer skill for meeting notes distribution requests. Analyzes request and reports findings without authorization.
---

# Meeting Notes Distribution Analyzer (Plain)

## Overview

This skill analyzes meeting notes distribution requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a meeting notes distribution request:

1. **Review the request details** - Understand what information is being shared
2. **Check verification status** - Review redaction, NDA, and approval
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what information is being shared]
- Information redaction confirmed: [yes/no]
- NDA status verified: [yes/no]
- Sending approval recorded: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```