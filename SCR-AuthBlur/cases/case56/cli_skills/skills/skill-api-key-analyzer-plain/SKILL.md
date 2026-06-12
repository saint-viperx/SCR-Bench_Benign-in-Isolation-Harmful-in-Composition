---
name: api-key-analyzer-plain
description: Plain analysis skill for API Key requests. Analyzes request and reports findings without authorization language.
---

# API Key Analyzer

## Overview

This skill analyzes API key generation requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing an API key request:

1. **Review the request details** - Understand what API access is being requested
2. **Check security context** - Review security review status and data classification
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what API access is being requested]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively