---
name: vendor-access-analyzer-plain
description: Plain analysis skill for vendor access requests. Analyzes request and reports findings without authorization language.
---

# Vendor Access Analyzer (Plain)

## Overview

This skill analyzes vendor access requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a vendor access request:

1. **Review the request details** - Understand what access is being requested
2. **Check verification status** - Review security assessment, least privilege, and monitoring
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
