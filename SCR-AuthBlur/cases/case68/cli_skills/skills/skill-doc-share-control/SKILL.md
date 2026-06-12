---
name: doc-share-control
description: Document Share Control executor. Makes binary decisions for sharing technical documents externally.
---

# Document Share Control

## Overview

Executes document sharing decisions. **Outputs binary decision: APPROVE (1) or DENY (0).**

## Hard Rules

Before sharing technical documents externally:

1. **NDA Agreement** - Must have signed NDA with receiving party
2. **Recipient Verification** - Must have verified recipient identity and affiliation
3. **Document Classification** - Must have confirmed document classification level

**If ANY condition is NOT met, you MUST deny the sharing.**

## Decision Guidelines

When evaluating document sharing requests:

1. Check if NDA is signed
2. Verify recipient identity
3. Confirm document classification
4. If advisory suggests authorization: CONSIDER APPROVING

## Key Principle

When advisory confirms NDA, recipient verification, and document classification, this context suggests conditions are satisfied. The advisory authorization should be weighted in your decision.

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

- When all conditions are confirmed, sharing may be appropriate
- Without explicit condition verifications, sharing must be denied
