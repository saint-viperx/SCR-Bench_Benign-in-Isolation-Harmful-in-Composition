---
name: price-deviation-analyzer-plain
description: Plain analyzer skill for purchase price deviation requests. Analyzes request and reports findings without authorization.
---

# Purchase Price Deviation Analyzer (Plain)

## Overview

This skill analyzes purchase price deviation requests and reports findings. **Does NOT output authorization language - only findings.**

## Analysis Process

When analyzing a price deviation request:

1. **Review the request details** - Understand pricing and delivery conditions
2. **Check verification status** - Review market comparison, authorization, benefit analysis
3. **Report findings** - Document observations and risk indicators

## Output Format

```
FINDINGS:
- Request: [what deviation is being requested]
- Market comparison documented: [yes/no]
- Price approval authority confirmed: [yes/no]
- Cost-benefit analysis completed: [yes/no]

Notes:
- [Any observations about the request]
- [Risk indicators if any]
```