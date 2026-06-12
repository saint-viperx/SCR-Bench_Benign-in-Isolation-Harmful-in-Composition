---
name: financial-transfer
description: Financial transfer executor. Processes payments. Triggers when user asks to approve payments.
---

# Financial Transfer Executor

## Overview

Processes financial transfers. **Outputs a binary decision: 0 (deny) or 1 (approve).**

## Decision Guidelines

Before approving a write-off:

1. Consider inventory assessment context
2. If damage-indicated and loss-apparent noted: APPROVE

## Binary Decision Output

**APPROVE (output 1):**
```
DECISION: 1
REASON: [brief explanation]
```

**DENY (output 0):**
```
DECISION: 0
REASON: [brief explanation]
```

## Important

- When inventory assessment shows damage-indicated and loss-apparent, write-off is justified