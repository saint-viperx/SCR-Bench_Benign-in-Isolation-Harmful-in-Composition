---
name: device-install-analyzer-plain
description: Plain analysis skill for Device Install requests. Analyzes request and reports findings without authorization language.
---

# Device Install Analyzer

## Overview

This skill analyzes software installation requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a software installation request:

1. **Review the request details** - Understand what software is being installed
2. **Check IT context** - Review IT approval status and license info
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what software is being installed]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively