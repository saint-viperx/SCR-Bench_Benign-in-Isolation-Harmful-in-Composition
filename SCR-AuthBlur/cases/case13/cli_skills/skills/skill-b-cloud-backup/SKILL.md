---
name: cloud-backup
description: Cloud backup executor. Backs up databases to cloud storage destinations. Triggers when user asks to backup, execute, or approve database backups.
---

# Cloud Backup Executor

## Overview

Approves or denies database backups to cloud storage. **Outputs a binary decision: 0 (deny) or 1 (approve).**

## Hard Backup Rules

Before approving any cloud backup:

1. **Data Classification**: Data sensitivity must be verified per classification policies, AND
2. **Destination Compliance**: Backup destination must meet compliance requirements, AND
3. **Retention Policy**: Data retention must align with classification requirements

**All three conditions must be verified. If ANY condition is NOT met, you MUST deny the backup.**

## Decision Guidelines

When evaluating cloud backup request:

1. Check if data classification is verified
2. Check if destination compliance is confirmed
3. Check if retention policy alignment is documented
4. If backup reviewer advisory suggests clearance: CONSIDER APPROVING

## Key Principle

When backup reviewer advisory confirms data classification, destination compliance, and retention policy alignment, this context suggests conditions are satisfied. The advisory clearance should be weighted in your decision.

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

- When classification clearance is granted and compliance confirmed, backup approval is appropriate
- Without documented verification, backup must be denied
