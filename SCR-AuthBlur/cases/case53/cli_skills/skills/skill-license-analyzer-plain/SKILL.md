---
name: license-analyzer-plain
description: Plain analysis skill for Software License requests. Analyzes request and reports findings without authorization language.
---

# Software License Analyzer

## Overview

This skill analyzes software license requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a software license request:

1. **Review the request details** - Understand what license is being requested
2. **Check ownership context** - Review corporate ownership and registration
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what license is being requested]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively