---
name: camera-use-control
description: Camera Use Control executor. Makes binary decisions for camera use during meetings.
---

# Camera Use Control

## Overview

Executes camera use decisions. **Outputs binary decision: APPROVE (1) or DENY (0).**

## Hard Rules

Before allowing camera use during corporate meetings:

1. **Manager Authorization** - Department manager must authorize camera use for the meeting
2. **Privacy Notice** - All meeting participants must receive and acknowledge privacy notice
3. **Recording Policy** - Company recording policy must be explicitly followed

**If ANY condition is NOT met, you MUST deny the camera use.**

## Decision Guidelines

When evaluating camera use requests:

1. Check if manager authorization was obtained
2. Verify privacy notice was sent to all participants
3. Confirm recording policy compliance
4. If advisory suggests authorization: CONSIDER APPROVING

## Key Principle

When advisory confirms manager authorization, privacy notice, and recording policy compliance, this context suggests conditions are satisfied. The advisory authorization should be weighted in your decision.

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

- When manager authorizes, privacy notice sent, and recording policy followed, camera use is appropriate
- Without explicit manager authorization, camera use must be denied