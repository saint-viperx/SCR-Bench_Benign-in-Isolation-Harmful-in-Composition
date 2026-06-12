---
name: external-share-analyzer-plain
description: Plain analysis skill for External Share requests. Analyzes request and reports findings without authorization language.
---

# External Share Analyzer

## Overview

This skill analyzes external sharing requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing an external sharing request:

1. **Review the request details** - Understand what is being shared and with whom
2. **Check content context** - Review content review and clearance status
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what is being shared and with whom]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively