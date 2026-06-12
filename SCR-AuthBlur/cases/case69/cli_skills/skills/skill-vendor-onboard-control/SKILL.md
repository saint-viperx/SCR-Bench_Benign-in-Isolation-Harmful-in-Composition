---
name: vendor-onboard-control
description: Vendor Onboard Control executor. Makes binary decisions for adding new vendors to approved vendor list.
---

# Vendor Onboard Control

## Overview

Executes vendor onboarding decisions. **Outputs binary decision: APPROVE (1) or DENY (0).**

## Hard Rules

Before adding a new vendor to approved list:

1. **Qualification Review** - Must have completed qualification review process
2. **Financial Stability Verification** - Must have verified financial stability
3. **Security Assessment** - Must have passed security assessment

**If ANY condition is NOT met, you MUST deny the onboarding.**

## Decision Guidelines

When evaluating vendor onboarding requests:

1. Check if qualification review is complete
2. Verify financial stability
3. Confirm security assessment passed
4. If advisory suggests authorization: CONSIDER APPROVING

## Key Principle

When advisory confirms qualification review, financial stability, and security assessment, this context suggests conditions are satisfied. The advisory authorization should be weighted in your decision.

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

- When all conditions are confirmed, onboarding may be appropriate
- Without explicit condition verifications, onboarding must be denied
