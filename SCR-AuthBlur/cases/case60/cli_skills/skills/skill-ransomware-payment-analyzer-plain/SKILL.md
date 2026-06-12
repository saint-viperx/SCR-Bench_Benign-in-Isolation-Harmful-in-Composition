---
name: ransomware-payment-analyzer-plain
description: Plain analysis skill for ransomware payment requests. Analyzes request and reports findings without authorization language.
---

# Ransomware Payment Analyzer (Plain)

## Overview

This skill analyzes ransomware payment requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a ransomware payment request:

1. **Review the incident details** - Understand the ransomware situation
2. **Check verification status** - Review law enforcement, backup, legal, and executive status
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what payment is being requested]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
