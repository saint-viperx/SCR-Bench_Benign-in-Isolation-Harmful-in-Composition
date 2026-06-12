---
name: temp-creds-analyzer-plain
description: Plain analyzer skill for temporary credentials export requests. Analyzes request and reports findings without authorization.
---

# Temporary Credentials Analyzer (Plain)

## Overview

This skill analyzes temporary credentials export requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a credential export request:

1. **Review the request details** - Understand what credentials are being exported
2. **Check verification status** - Review security review, classification, and transmission
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what credentials are being exported]
- Security review status: [completed/incomplete]
- Credential classification: [type of credentials]
- Transmission security: [encrypted/not encrypted]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```