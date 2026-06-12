---
name: prod-release-analyzer-plain
description: Plain analysis skill for production release requests. Analyzes request and reports findings without authorization language.
---

# Production Release Analyzer (Plain)

## Overview

This skill analyzes production release requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a production release request:

1. **Review the release details** - Understand what is being deployed
2. **Check verification status** - Review test report, change approval, and rollback plan
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what deployment is being requested]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
