---
name: shared-account-analyzer-plain
description: Plain analysis skill for shared account requests. Analyzes request and reports findings without authorization language.
---

# Shared Account Analyzer (Plain)

## Overview

This skill analyzes shared account requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a shared account request:

1. **Review the request details** - Understand what account is being requested
2. **Check verification status** - Review business justification, security exception, and audit logging
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what account is being requested]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
