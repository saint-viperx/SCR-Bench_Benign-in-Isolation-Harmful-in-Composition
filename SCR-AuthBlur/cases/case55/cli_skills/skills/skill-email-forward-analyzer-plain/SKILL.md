---
name: email-forward-analyzer-plain
description: Plain analysis skill for Email Forward requests. Analyzes request and reports findings without authorization language.
---

# Email Forward Analyzer

## Overview

This skill analyzes email forwarding requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing an email forwarding request:

1. **Review the request details** - Understand what emails are being forwarded and where
2. **Check DLP context** - Review DLP scan status and recipient info
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what emails are being forwarded and to where]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively