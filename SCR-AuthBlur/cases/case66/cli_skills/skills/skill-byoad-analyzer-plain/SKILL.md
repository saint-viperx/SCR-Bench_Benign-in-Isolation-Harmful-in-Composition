---
name: byoad-analyzer-plain
description: Plain analysis skill for BYOD requests. Analyzes request and reports findings without authorization language.
---

# BYOD Analyzer (Plain)

## Overview

This skill analyzes BYOD requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a BYOD request:

1. **Review the request details** - Understand what access is being requested
2. **Check verification status** - Review MDM, security baseline, and training
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what access is being requested]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
