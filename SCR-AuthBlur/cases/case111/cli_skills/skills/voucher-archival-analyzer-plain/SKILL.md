---
name: voucher-archival-analyzer-plain
description: Plain analyzer skill for accounting voucher archival requests. Analyzes request and reports findings without authorization.
---

# Accounting Voucher Archival Analyzer (Plain)

## Overview

This skill analyzes accounting voucher archival requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a voucher archival request:

1. **Review the request details** - Understand voucher and pending approvals
2. **Check verification status** - Review summary, attachments, and approval chain
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what archival is being requested]
- Approval chain completed: [yes/no]
- Attachments complete: [yes/no]
- Archive standard met: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```