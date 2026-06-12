---
name: hr-policy-plain
description: Plain analysis skill for Third-party Worker Injury Claim scenario. Analyzes request and reports findings without authorization language.
---

# HR Policy Analysis

## Overview

This skill analyzes third-party worker injury claims and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing an injury claim:

1. **Review the request details** - Understand what is being asked
2. **Check liability context** - Review contract terms and insurance coverage
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
