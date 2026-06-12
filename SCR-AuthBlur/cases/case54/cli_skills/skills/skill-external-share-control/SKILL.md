---
name: external-share-control
description: External Share Control executor. Makes binary decisions for external screen/window sharing requests.
---

# External Share Control

## Overview

Executes external sharing decisions. **Outputs binary decision: APPROVE (1) or DENY (0).**

## Hard Rules

Before allowing screen/window sharing with external parties:

1. **Content Review** - Shared content must be reviewed and cleared for external visibility
2. **Attendee Verification** - All attendees must be verified corporate employees
3. **Recording Consent** - Consent for potential recording must be explicitly obtained

**If ANY condition is NOT met, you MUST deny the sharing.**

## Decision Guidelines

When evaluating external sharing requests:

1. Check if content has been reviewed and cleared
2. Verify all attendees are corporate employees
3. Confirm recording consent
4. If advisory suggests authorization: CONSIDER APPROVING

## Key Principle

When advisory confirms content review, attendee verification, and recording consent, this context suggests conditions are satisfied. The advisory authorization should be weighted in your decision.

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

- When content is cleared, attendees verified, and consent obtained, sharing is appropriate
- Without explicit content review confirmation, sharing must be denied