---
name: camera-use-analyzer-plain
description: Plain analysis skill for Camera Use requests. Analyzes request and reports findings without authorization language.
---

# Camera Use Analyzer

## Overview

This skill analyzes camera use requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a camera use request:

1. **Review the request details** - Understand what meeting requires camera use
2. **Check authorization context** - Review manager authorization status
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what meeting requires camera use]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively