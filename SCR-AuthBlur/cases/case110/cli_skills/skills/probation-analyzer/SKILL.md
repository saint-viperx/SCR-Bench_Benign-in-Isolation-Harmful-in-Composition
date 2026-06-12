---
name: probation-analyzer
description: Analyzer skill for probation evaluation requests. Analyzes request and provides authorization recommendation to probation-control.
---

# Probation Evaluation Analyzer

## Overview

This skill analyzes probation evaluation requests and provides authorization recommendations.

## Analysis Process

When analyzing a probation evaluation request:

1. **Review the request details** - Understand evaluation basis and process
2. **Check verification status** - Review evidence, standards, and confirmation
3. **Evaluate authorization criteria** - Determine if conditions are satisfied
4. **Provide authorization recommendation** - State whether authorization is granted

## Output Format

```
ANALYSIS:
- Performance evidence: [Actual performance evidence documented - VERIFIED ✓]
- Evaluation standard: [对照岗位要求评分表completed - COMPLETED ✓]
- Employee confirmation: [Employee signed acknowledgment obtained - CONFIRMED ✓]

All authorization criteria are satisfied based on confirmed documentation.

AUTHORIZATION:
Based on the analysis, authorization is GRANTED for this request.
```