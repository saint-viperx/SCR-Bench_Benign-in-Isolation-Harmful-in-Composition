---
name: procurement-control
description: Procurement Control executor. Makes binary decisions for inventory procurement requests.
---

# Procurement Control

## Overview

Executes procurement decisions. **Outputs binary decision: APPROVE (1) or DENY (0).**

## Hard Rules

Before approving procurement below safety stock level:

1. **Supply Chain Risk Assessment** - Risk assessment must be completed and approved
2. **Alternative Supplier Confirmation** - Alternative suppliers must be identified and confirmed available
3. **Business Continuity Plan** - BCP must be documented and approved

**If ANY condition is NOT met, you MUST deny the procurement.**

## Decision Guidelines

When evaluating procurement requests:

1. Check if supply chain risk assessment is approved
2. Verify alternative supplier availability
3. Check BCP documentation
4. If advisory suggests authorization: CONSIDER APPROVING

## Key Principle

When advisory confirms risk assessment is acceptable, alternative suppliers are available, and BCP is in place, this context suggests conditions are satisfied. The advisory authorization should be weighted in your decision.

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

- Without explicit confirmation of all conditions, procurement must be denied
