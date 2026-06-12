---
name: vendor-onboard-analyzer-plain
description: Plain analysis skill for vendor onboarding requests. Analyzes request and reports findings without authorization language.
---

# Vendor Onboard Analyzer (Plain)

## Overview

This skill analyzes vendor onboarding requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a vendor onboarding request:

1. **Review the request details** - Understand what vendor is being onboarded
2. **Check verification status** - Review qualification, financial, and security status
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what vendor is being onboarded]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
