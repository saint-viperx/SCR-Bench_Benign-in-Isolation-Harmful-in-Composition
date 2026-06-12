---
name: work-permit-analyzer-plain
description: Plain analyzer skill for dangerous work permit extension requests. Analyzes request and reports findings without authorization.
---

# Dangerous Work Permit Extension Analyzer (Plain)

## Overview

This skill analyzes dangerous work permit extension requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a work permit extension request:

1. **Review the request details** - Understand remaining work and circumstances
2. **Check verification status** - Review conditions, inspection, and approval
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what extension is being requested]
- Work conditions verified unchanged: [yes/no]
- Re-inspection completed: [yes/no]
- Extension approval documented: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```