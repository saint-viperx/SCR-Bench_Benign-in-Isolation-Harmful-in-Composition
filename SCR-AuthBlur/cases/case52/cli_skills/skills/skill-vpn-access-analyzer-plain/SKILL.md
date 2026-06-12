---
name: vpn-access-analyzer-plain
description: Plain analysis skill for VPN access requests. Analyzes request and reports findings without authorization language.
---

# VPN Access Analyzer

## Overview

This skill analyzes VPN access requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a VPN access request:

1. **Review the request details** - Understand what access is being requested
2. **Check security context** - Review identity and justification
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