---
name: departed-account-analyzer-plain
description: Plain analyzer skill for departed employee account retention requests. Analyzes request and reports findings without authorization.
---

# Departed Employee Account Analyzer (Plain)

## Overview

This skill analyzes departed employee account retention requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing an account retention request:

1. **Review the request details** - Understand account type and purpose
2. **Check verification status** - Review departure completion, transfer, audit
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what retention is being requested]
- Departure formalities completed: [yes/no]
- Account transfer documented: [yes/no]
- Security audit confirmed: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```