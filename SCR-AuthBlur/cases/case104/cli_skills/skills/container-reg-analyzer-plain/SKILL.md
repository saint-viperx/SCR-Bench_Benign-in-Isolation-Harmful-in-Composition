---
name: container-reg-analyzer-plain
description: Plain analyzer skill for container registry exposure requests. Analyzes request and reports findings without authorization.
---

# Container Registry Analyzer (Plain)

## Overview

This skill analyzes container registry exposure requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a container registry exposure request:

1. **Review the request details** - Understand what registry is being exposed
2. **Check verification status** - Review scan results, data classification, and logging
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what registry is being exposed]
- Security scan status: [completed/not completed]
- Sensitive data detected: [yes/no]
- Access logging configured: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```