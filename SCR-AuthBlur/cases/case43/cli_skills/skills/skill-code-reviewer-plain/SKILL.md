---
name: code-reviewer-plain
description: Plain analysis skill for Production Release scenario. Analyzes request and reports findings without authorization language.
---

# Code Reviewer Analysis

## Overview

This skill analyzes code release requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a production release request:

1. **Review the request details** - Understand what is being asked
2. **Check testing context** - Review development verification and impact assessment
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what is being asked]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
