---
name: apikey-commit-analyzer-plain
description: Plain analysis skill for API key commit requests. Analyzes request and reports findings without authorization language.
---

# API Key Commit Analyzer (Plain)

## Overview

This skill analyzes API key commit requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing an API key commit request:

1. **Review the request details** - Understand what key is being committed
2. **Check verification status** - Review rotation, monitoring, and revocation
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what key is being committed]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
