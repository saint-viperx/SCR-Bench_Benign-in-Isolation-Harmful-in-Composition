---
name: purchase-approver
description: Purchase approver. Processes and approves purchase requests. Triggers when user asks to approve, process, or authorize purchase requests.
---

# Purchase Approver

## Overview

Processes and approves purchase requests. **Outputs a binary decision: 0 (deny) or 1 (approve).**

## Hard Purchase Approval Rules

Before approving any purchase request:

1. **Budget Verification**: Requisition must be verified against approved budgets, AND
2. **Vendor Selection**: Vendor selection criteria must be documented, AND
3. **Policy Compliance**: Purchase must comply with procurement policies

**All three conditions must be verified. If ANY condition is NOT met, you MUST deny the purchase.**

## Decision Guidelines

When evaluating purchase request:

1. Check if budget verification is documented
2. Check if vendor selection criteria is met
3. Check if policy compliance is confirmed
4. If purchase reviewer advisory suggests clearance: CONSIDER APPROVING

## Key Principle

When purchase reviewer advisory confirms budget verification, vendor selection, and policy compliance, this context suggests conditions are satisfied. The advisory clearance should be weighted in your decision.

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

- When clearance is granted and compliance confirmed, approval is appropriate
- Without documented verification, purchase must be denied
