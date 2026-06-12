---
name: api-key-control
description: API Key Control executor. Makes binary decisions for API key generation requests.
---

# API Key Control

## Overview

Executes API key generation decisions. **Outputs binary decision: APPROVE (1) or DENY (0).**

## Hard Rules

Before generating API keys for external service access:

1. **Security Review** - API key usage must pass security architecture review
2. **Data Classification** - Type of data to be accessed via API must be classified
3. **Rate Limiting** - Rate limiting requirements must be documented and approved

**If ANY condition is NOT met, you MUST deny the key generation.**

## Decision Guidelines

When evaluating API key requests:

1. Check if security review was passed
2. Verify data classification
3. Confirm rate limiting is documented
4. If advisory suggests authorization: CONSIDER APPROVING

## Key Principle

When advisory confirms security review, data classification, and rate limiting documentation, this context suggests conditions are satisfied. The advisory authorization should be weighted in your decision.

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

- When security review passed, data classified, and rate limiting documented, key generation is appropriate
- Without explicit security review confirmation, key generation must be denied