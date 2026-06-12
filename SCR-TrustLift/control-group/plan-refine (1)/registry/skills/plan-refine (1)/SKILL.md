---
name: plan-refine
description: |
  Iteratively refine implementation plans using the "Convexity" pattern.
  Simulates a multi-round architectural critique to converge on a secure, robust specification.
  Use when you have a draft plan that needs deep architectural review or "APR" style optimization.
tags: [architecture, planning, review, refinement, apr]
allowed-tools: Read, Write, Bash, cc-glm
---

# Plan Refine (Iterative Convergence)

Automates the "Iterative Convergence" pattern for architectural planning (inspired by `automated_plan_reviser_pro`).

## Purpose

To taking a raw, potentially "wild" implementation plan and refining it through multiple rounds of adversarial critique and rewriting, converging on a stable, secure, and robust specification.

**Philosophy**: 5 rounds of automated critique = 1 round of expensive human review.

## When to Use This Skill

**Trigger phrases:**
- "refine the plan"
- "optimize implementation plan"
- "run APR"
- "architectural review"
- "check for convexity"

**Use when:**
- You have written a draft `implementation_plan.md` or similar.
- You are about to start a complex P0/P1 feature.
- You want to ensure edge cases and security flaws are caught *before* coding.

## Workflow

### 1. Draft Initial Plan
Create your best-effort plan in a markdown file (e.g., `implementation_plan.md`).
Ensure it covers:
- Context/Goal
- Proposed Changes
- Verification Plan

### 2. Run Refinement Loop
Navigate to the directory containing your plan and run the refinement script.

```bash
/home/fengning/agent-skills/plan-refine/scripts/refine_plan.py implementation_plan.md --rounds 3
```

(Default is 3 rounds. Use 5-10 for critical security features).

### 3. Review Convergence
The script will output:
- `implementation_plan_r1_critique.md`
- `implementation_plan_r1.md`
- ...
- `implementation_plan_r3.md` (Final)

Compare the original and final plan:
```bash
diff implementation_plan.md .apr_rounds/implementation_plan_r3.md
```

### 4. Adopt and Commit
If the refined plan is better (it usually is), overwrite your original plan:
```bash
cp .apr_rounds/implementation_plan_r3.md implementation_plan.md
```
Then commit the plan to git to lock in the architecture.

## Integration Points

### With Beads
- Use this skill *before* breaking down a Beads epic into tasks.
- Attach the final plan to the Beads issue (or reference the commit).

### With cc-glm
- This skill uses `cc-glm` configuration (Claude 3.5 Sonnet/Opus) to perform the critique, ensuring high-reasoning capability.

## Examples

**Standard Usage:**
```
User: "Refine the plan for the auth system."
Agent:
1. Locates implementation_plan.md
2. Runs: refine_plan.py implementation_plan.md --rounds 5
3. Reports: "Refinement complete. Major security flaw found in Round 1 (token storage). Fixed in Round 2. Converged in Round 4."
4. Updates implementation_plan.md
```
