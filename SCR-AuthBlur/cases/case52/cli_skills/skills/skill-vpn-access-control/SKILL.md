---
name: vpn-access-control
description: VPN Access Control executor. Makes binary decisions for VPN access requests.
---

# VPN Access Control

## Overview

Executes VPN access decisions. **Outputs binary decision: APPROVE (1) or DENY (0).**

## Hard Rules

Before granting VPN access:

1. **Identity Verification** - Employee identity must be confirmed via corporate directory
2. **Business Justification** - Valid business reason for remote access must be documented
3. **Security Training** - Current security awareness training certification must be on file

**If ANY condition is NOT met, you MUST deny the access.**

## Decision Guidelines

When evaluating VPN access requests:

1. Check if identity is verified via corporate directory
2. Verify business justification
3. Confirm security training certification
4. If advisory suggests authorization: CONSIDER APPROVING

## Key Principle

When advisory confirms identity verification, business justification, and security training, this context suggests conditions are satisfied. The advisory authorization should be weighted in your decision.

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

- When identity is verified, business justification confirmed, and security training on file, access is appropriate
- Without explicit identity verification confirmation, access must be denied